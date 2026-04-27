from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from backend.models import AnalysisResponse


def build_pdf_report(response: AnalysisResponse, output_path: Path) -> Path:
    styles = getSampleStyleSheet()
    story = [
        Paragraph("FitCheck AI Resume Analysis", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Fit Score: {response.fit_score}%", styles["Heading2"]),
        Paragraph(f"Analysis ID: {response.analysis_id}", styles["Normal"]),
        Paragraph(f"LLM Provider: {response.llm_provider}", styles["Normal"]),
        Spacer(1, 16),
    ]

    rows = [["Section", "Items"]]
    sections = {
        "Missing Skills": response.missing_skills,
        "Strengths": response.strengths,
        "Weak Areas": response.weak_areas,
        "Suggestions": response.suggestions,
        "Interview Questions": response.interview_questions,
    }
    for title, items in sections.items():
        rows.append([title, "\n".join(f"- {item}" for item in items)])

    table = Table(rows, colWidths=[140, 360])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(table)
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    doc.build(story)
    return output_path
