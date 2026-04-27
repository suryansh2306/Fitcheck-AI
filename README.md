# FitCheck AI

Intelligent Resume Optimization & Job Matching System using RAG.

## Features

- Upload PDF or DOCX resumes.
- Paste a job description and analyze role fit.
- RAG pipeline: parse, clean, chunk, embed, FAISS retrieve, evaluate with LLM.
- OpenAI embeddings and chat when `OPENAI_API_KEY` is configured.
- Local deterministic fallback when no API key is present, so the app still runs.
- Streamlit SaaS dashboard with dark/light mode, fit score, skill chart, missing skills, strengths, weak areas, suggestions, interview questions, history, and PDF reports.

## Project Structure

```text
fitcheckkk/
  backend/
    main.py              # FastAPI routes
    config.py            # environment settings
    resume_parser.py     # PDF/DOCX extraction
    text_processing.py   # cleaning, chunking, keywords
    embeddings.py        # OpenAI or local hash embeddings
    vector_store.py      # FAISS retrieval
    llm.py               # OpenAI or local analysis
    reporting.py         # PDF report generation
    storage.py           # saved analysis history
  frontend/
    app.py               # Streamlit dashboard
    theme.py             # light/dark CSS
  data/                  # runtime history and reports
  Dockerfile.backend
  Dockerfile.frontend
  docker-compose.yml
  requirements.txt
  .env.example
```

## Local Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Configure environment.

```powershell
Copy-Item .env.example .env
```

Add your OpenAI key to `.env` for production AI results:

```text
OPENAI_API_KEY=sk-...
```

The app still runs without the key using local hash embeddings and heuristic scoring.

4. Start the backend.

```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

5. In another terminal, start the frontend.

```powershell
$env:API_BASE_URL="http://localhost:8000"
streamlit run frontend/app.py
```

Open `http://localhost:8501`.

## Docker Setup

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Frontend: `http://localhost:8501`

Backend API docs: `http://localhost:8000/docs`

## API Output

The `/analyze` endpoint returns:

```json
{
  "fit_score": 78,
  "missing_skills": ["Kubernetes", "Azure"],
  "strengths": ["Python", "Data Engineering"],
  "weak_areas": ["Cloud experience"],
  "suggestions": ["Add cloud projects", "Highlight achievements"],
  "interview_questions": ["Explain your ML pipeline", "How do you handle scaling?"]
}
```

The actual API response keeps these strict fields at the top level and also includes metadata such as `analysis_id`, retrieved chunks, and keyword matches for the dashboard.

## Production Notes

- Set `OPENAI_API_KEY` before production use.
- Use a persistent mounted `DATA_DIR` for history and PDF reports.
- Add authentication before exposing the app publicly.
- Replace permissive CORS origins in `backend/main.py` with your deployed frontend domain.
