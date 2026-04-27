import json
import re

from openai import OpenAI

from backend.config import Settings
from backend.models import AnalysisResult
from backend.text_processing import extract_keywords, keyword_match_map


SYSTEM_PROMPT = """You are FitCheck AI, a precise resume optimization analyst.
Return only valid JSON matching this schema:
{
  "fit_score": 0,
  "missing_skills": [],
  "strengths": [],
  "weak_areas": [],
  "suggestions": [],
  "interview_questions": []
}
Use an integer fit_score from 0 to 100. Keep arrays concise and practical."""


class AnalysisService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    @property
    def provider(self) -> str:
        return "openai" if self.client else "local-heuristic"

    def analyze(self, resume_text: str, job_description: str, relevant_chunks: list[str]) -> AnalysisResult:
        if self.client:
            try:
                return self._analyze_with_openai(job_description, relevant_chunks)
            except Exception:
                return self._heuristic_analysis(resume_text, job_description)
        return self._heuristic_analysis(resume_text, job_description)

    def _analyze_with_openai(self, job_description: str, relevant_chunks: list[str]) -> AnalysisResult:
        context = "\n\n---\n\n".join(relevant_chunks)
        response = self.client.chat.completions.create(
            model=self.settings.openai_chat_model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Resume context retrieved by RAG:\n"
                        f"{context}\n\nJob description:\n{job_description}\n\n"
                        "Evaluate the candidate against the role. Include missing skills, strengths, weak areas, "
                        "specific resume improvements, and interview preparation questions."
                    ),
                },
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content or "{}"
        return AnalysisResult.model_validate(json.loads(content))

    def _heuristic_analysis(self, resume_text: str, job_description: str) -> AnalysisResult:
        matches = keyword_match_map(job_description, resume_text)
        jd_keywords = list(matches.keys())
        matched = [keyword for keyword, present in matches.items() if present]
        missing = [keyword for keyword, present in matches.items() if not present]
        density_score = int(round((len(matched) / max(len(jd_keywords), 1)) * 100))
        resume_length_score = min(20, len(resume_text.split()) // 35)
        fit_score = max(15, min(95, int(density_score * 0.8 + resume_length_score)))

        strengths = _title_items(matched[:6]) or ["Relevant experience reflected in resume"]
        missing_skills = _title_items(missing[:8])
        weak_areas = _weak_areas(job_description, resume_text, missing)
        suggestions = [
            f"Add concrete examples showing {skill} experience." for skill in _title_items(missing[:3])
        ]
        suggestions.extend(
            [
                "Quantify impact with metrics such as revenue, latency, cost, accuracy, or users served.",
                "Mirror the job description language in your summary, skills, and project bullets.",
                "Move the most relevant achievements into the top third of the resume.",
            ]
        )
        questions = [
            f"How have you used {skill} in a production or project setting?" for skill in _title_items((matched + missing)[:4])
        ]
        questions.extend(
            [
                "Walk me through the most relevant project on your resume.",
                "What trade-offs did you make in a recent technical implementation?",
            ]
        )

        return AnalysisResult(
            fit_score=fit_score,
            missing_skills=missing_skills,
            strengths=strengths[:6],
            weak_areas=weak_areas[:5],
            suggestions=list(dict.fromkeys(suggestions))[:7],
            interview_questions=list(dict.fromkeys(questions))[:7],
        )


def _title_items(items: list[str]) -> list[str]:
    return [item.upper() if item in {"aws", "gcp", "sql", "nlp", "rag", "llm", "ci/cd"} else item.title() for item in items]


def _weak_areas(job_description: str, resume_text: str, missing: list[str]) -> list[str]:
    weak = []
    lowered_resume = resume_text.lower()
    if missing:
        weak.append("Limited evidence for " + ", ".join(_title_items(missing[:3])))
    if not re.search(r"\d+%|\$\d+|\b\d+x\b|\b\d+\+?\s+(users|customers|projects|models|pipelines)\b", resume_text, re.I):
        weak.append("Resume impact is not strongly quantified")
    if "lead" in job_description.lower() and "lead" not in lowered_resume:
        weak.append("Leadership ownership is not clearly highlighted")
    if "cloud" in job_description.lower() and not any(cloud in lowered_resume for cloud in ["aws", "azure", "gcp", "cloud"]):
        weak.append("Cloud platform experience is thin")
    return weak or ["No major weak areas detected from keyword alignment"]
