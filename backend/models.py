from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    fit_score: int = Field(ge=0, le=100)
    missing_skills: list[str]
    strengths: list[str]
    weak_areas: list[str]
    suggestions: list[str]
    interview_questions: list[str]


class AnalysisResponse(AnalysisResult):
    analysis_id: str
    llm_provider: str
    relevant_chunks: list[str]
    keyword_matches: dict[str, bool]


class HistoryItem(BaseModel):
    analysis_id: str
    created_at: str
    resume_filename: str
    fit_score: int
    missing_skills: list[str]
    strengths: list[str]
