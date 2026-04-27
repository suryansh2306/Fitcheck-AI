import os
from io import BytesIO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from frontend.theme import css


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def render_list(column, title: str, items: list[str], pill_class: str) -> None:
    with column:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(title)
        body = '<div class="pill-grid">' + "".join(f'<span class="pill {pill_class}">{item}</span>' for item in items) + "</div>"
        st.markdown(body, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_cards(column, title: str, items: list[str]) -> None:
    with column:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(title)
        for item in items:
            st.markdown(f'<div class="item-card">{item}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


st.set_page_config(
    page_title="FitCheck AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "analysis" not in st.session_state:
    st.session_state.analysis = None

with st.sidebar:
    st.markdown("## FitCheck AI")
    st.caption("Intelligent Resume Optimization & Job Matching using RAG")
    st.divider()
    st.session_state.theme = st.toggle("Dark mode", value=st.session_state.theme == "Dark")
    st.session_state.theme = "Dark" if st.session_state.theme else "Light"
    st.markdown("### Navigation")
    st.markdown("Upload Resume")
    st.markdown("Job Description")
    st.markdown("Output Dashboard")
    st.divider()
    try:
        health = requests.get(f"{API_BASE_URL}/health", timeout=3).json()
        st.success(f"API online · {health['analysis_provider']}")
    except requests.RequestException:
        st.error("API offline")

st.markdown(css(st.session_state.theme), unsafe_allow_html=True)

st.markdown(
    """
    <div class="topbar">
      <div>
        <h1 class="brand-title">FitCheck AI</h1>
        <div class="brand-subtitle">RAG-powered resume scoring, skill gap analysis, and interview prep.</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

input_left, input_right = st.columns([0.95, 1.35], gap="large")

with input_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader("PDF or DOCX", type=["pdf", "docx"], label_visibility="collapsed")
    st.caption("Your resume is parsed, chunked, embedded, and searched against the role requirements.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(" ")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🕘 Previous Analysis")
    try:
        history = requests.get(f"{API_BASE_URL}/history", timeout=5).json()
    except requests.RequestException:
        history = []
    if history:
        for item in history[:5]:
            st.markdown(
                f"""<div class="item-card"><b>{item["fit_score"]}%</b> · {item["resume_filename"]}<br>
                <span class="muted">{item["created_at"][:19].replace("T", " ")}</span></div>""",
                unsafe_allow_html=True,
            )
    else:
        st.caption("No saved analyses yet.")
    st.markdown("</div>", unsafe_allow_html=True)

with input_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💼 Enter Job Description")
    job_description = st.text_area(
        "Paste the complete role description",
        height=230,
        placeholder="Paste responsibilities, qualifications, required skills, and nice-to-have skills...",
        label_visibility="collapsed",
    )
    analyze_clicked = st.button("Analyze Resume", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if analyze_clicked:
    if not resume_file:
        st.warning("Upload a PDF or DOCX resume first.")
    elif not job_description.strip():
        st.warning("Paste a job description before analysis.")
    else:
        progress = st.progress(0, text="Analyzing your resume...")
        try:
            files = {"resume": (resume_file.name, resume_file.getvalue(), resume_file.type)}
            data = {"job_description": job_description}
            for value in [18, 42, 68]:
                progress.progress(value, text="Analyzing your resume...")
            response = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data, timeout=120)
            response.raise_for_status()
            st.session_state.analysis = response.json()
            progress.progress(100, text="Analysis complete")
        except requests.HTTPError as exc:
            detail = exc.response.json().get("detail", str(exc)) if exc.response is not None else str(exc)
            st.error(detail)
        except requests.RequestException as exc:
            st.error(f"Could not reach backend: {exc}")
        finally:
            progress.empty()

analysis = st.session_state.analysis
if analysis:
    result = analysis
    matches = analysis.get("keyword_matches", {})
    matched_count = sum(1 for present in matches.values() if present)
    missing_count = sum(1 for present in matches.values() if not present)

    st.markdown("## Output Dashboard")
    score_col, chart_col, keywords_col = st.columns([0.85, 1.25, 1], gap="large")

    with score_col:
        score = int(result["fit_score"])
        st.markdown(
            f"""
            <div class="card" style="text-align:center; --score:{score}%;">
                <h3>🔥 Fit Score</h3>
                <div class="score-wrap">
                    <div class="score-inner"><div><div class="score-number">{score}%</div><div class="muted">Role Match</div></div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with chart_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Skill Match Chart")
        chart_df = pd.DataFrame(
            [{"Status": "Matched", "Skills": matched_count}, {"Status": "Missing", "Skills": missing_count}]
        )
        theme_dark = st.session_state.theme == "Dark"
        fig = px.bar(
            chart_df,
            x="Status",
            y="Skills",
            color="Status",
            color_discrete_map={"Matched": "#22c55e", "Missing": "#ef4444"},
            text="Skills",
        )
        fig.update_layout(
            height=285,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e5edf9" if theme_dark else "#0f172a",
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10),
        )
        fig.update_yaxes(gridcolor="rgba(148,163,184,.18)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with keywords_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔎 Keyword Coverage")
        if matches:
            st.markdown(
                '<div class="pill-grid">'
                + "".join(
                    f'<span class="pill {"good" if present else "missing"}">{keyword}</span>'
                    for keyword, present in list(matches.items())[:18]
                )
                + "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.caption("No explicit skill keywords detected.")
        st.markdown("</div>", unsafe_allow_html=True)

    lower_left, lower_mid, lower_right = st.columns(3, gap="large")
    render_list(lower_left, "❌ Missing Skills", result["missing_skills"], "missing")
    render_list(lower_mid, "✅ Strengths", result["strengths"], "good")
    render_list(lower_right, "⚠ Weak Areas", result["weak_areas"], "")

    suggestions_col, questions_col = st.columns(2, gap="large")
    render_cards(suggestions_col, "💡 Suggestions", result["suggestions"])
    render_cards(questions_col, "🎯 Interview Questions", result["interview_questions"])

    with st.expander("Retrieved Resume Context"):
        for index, chunk in enumerate(analysis.get("relevant_chunks", []), start=1):
            st.markdown(f"**Chunk {index}**")
            st.write(chunk[:1200])

    try:
        report_response = requests.get(f"{API_BASE_URL}/report/{analysis['analysis_id']}", timeout=30)
        report_response.raise_for_status()
        st.download_button(
            "Download PDF Report",
            data=BytesIO(report_response.content),
            file_name=f"fitcheck-{analysis['analysis_id']}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except requests.RequestException:
        st.info("PDF report will be available after the backend report service responds.")
