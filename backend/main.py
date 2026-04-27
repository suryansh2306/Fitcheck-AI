from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.config import get_settings
from backend.embeddings import EmbeddingService
from backend.llm import AnalysisService
from backend.models import AnalysisResponse, HistoryItem
from backend.reporting import build_pdf_report
from backend.resume_parser import SUPPORTED_EXTENSIONS, extract_resume_text
from backend.storage import AnalysisStore
from backend.text_processing import chunk_text, keyword_match_map, preprocess_text
from backend.vector_store import ResumeVectorStore

settings = get_settings()
embedding_service = EmbeddingService(settings)
analysis_service = AnalysisService(settings)
store = AnalysisStore(settings)

app = FastAPI(
    title="FitCheck AI API",
    description="RAG-powered resume optimization and job matching system.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "embedding_provider": embedding_service.provider,
        "analysis_provider": analysis_service.provider,
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalysisResponse:
    suffix = Path(resume.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Upload a PDF or DOCX resume.")

    content = await resume.read()
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail=f"File is larger than {settings.max_upload_mb} MB.")
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    try:
        raw_resume_text = extract_resume_text(resume.filename or "resume", content)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not parse resume: {exc}") from exc

    resume_text = preprocess_text(raw_resume_text)
    jd_text = preprocess_text(job_description)
    if len(resume_text.split()) < 30:
        raise HTTPException(status_code=422, detail="Resume text extraction produced too little text.")

    chunks = chunk_text(resume_text)
    resume_embeddings = embedding_service.embed_texts(chunks)
    jd_embedding = embedding_service.embed_texts([jd_text])
    vector_store = ResumeVectorStore(chunks, resume_embeddings)
    relevant_chunks = vector_store.search(jd_embedding, settings.top_k_chunks)

    result = analysis_service.analyze(resume_text, jd_text, relevant_chunks)
    response = AnalysisResponse(
        **result.model_dump(),
        analysis_id=str(uuid4()),
        llm_provider=analysis_service.provider,
        relevant_chunks=relevant_chunks,
        keyword_matches=keyword_match_map(jd_text, resume_text),
    )
    store.save(response, resume.filename or "resume")
    return response


@app.get("/history", response_model=list[HistoryItem])
def history() -> list[HistoryItem]:
    return store.list()


@app.get("/report/{analysis_id}")
def report(analysis_id: str) -> FileResponse:
    response = store.get(analysis_id)
    if not response:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    output_path = settings.data_dir / "reports" / f"{analysis_id}.pdf"
    if not output_path.exists():
        build_pdf_report(response, output_path)
    return FileResponse(output_path, media_type="application/pdf", filename=f"fitcheck-{analysis_id}.pdf")
