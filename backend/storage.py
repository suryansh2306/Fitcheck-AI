import json
from datetime import UTC, datetime
from pathlib import Path

from backend.config import Settings
from backend.models import AnalysisResponse, HistoryItem


class AnalysisStore:
    def __init__(self, settings: Settings):
        self.path = Path(settings.data_dir) / "analyses.json"
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def save(self, response: AnalysisResponse, resume_filename: str):
        records = self._read()
        records.insert(
            0,
            {
                "created_at": datetime.now(UTC).isoformat(),
                "resume_filename": resume_filename,
                **response.model_dump(),
            },
        )
        self.path.write_text(json.dumps(records[:50], indent=2), encoding="utf-8")

    def list(self):
        records = self._read()
        result = []
        for record in records:
            result.append(
                HistoryItem(
                    analysis_id=record["analysis_id"],
                    created_at=record["created_at"],
                    resume_filename=record["resume_filename"],
                    fit_score=record["fit_score"],
                    missing_skills=record["missing_skills"],
                    strengths=record["strengths"],
                )
            )
        return result

    def get(self, analysis_id: str):
        for record in self._read():
            if record["analysis_id"] == analysis_id:
                return AnalysisResponse.model_validate(record)
        return None

    def _read(self):
        return json.loads(self.path.read_text(encoding="utf-8"))