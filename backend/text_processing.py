import re


SKILL_VOCABULARY = [
    "python", "java", "javascript", "typescript", "sql", "nosql", "postgresql",
    "mysql", "mongodb", "redis", "aws", "azure", "gcp", "docker", "kubernetes",
    "terraform", "linux", "fastapi", "django", "flask", "react", "streamlit",
    "node", "spark", "airflow", "kafka", "machine learning", "deep learning",
    "nlp", "rag", "llm", "openai", "langchain", "vector database", "faiss",
    "chromadb", "pandas", "numpy", "scikit-learn", "pytorch", "tensorflow",
    "mlops", "ci/cd", "git", "rest api", "microservices", "data engineering",
    "etl", "analytics", "leadership", "communication", "agile", "scrum",
]


def preprocess_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    if not text:
        return []
    words = text.split()
    chunks: list[str] = []
    step = max(chunk_size - overlap, 1)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + chunk_size])
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(words):
            break
    return chunks


def extract_keywords(text: str) -> list[str]:
    lowered = text.lower()
    found = [skill for skill in SKILL_VOCABULARY if re.search(rf"\b{re.escape(skill)}\b", lowered)]
    extra_terms = re.findall(r"\b[A-Z][A-Za-z0-9+#./-]{2,}\b", text)
    normalized = [term.lower() for term in extra_terms if len(term) <= 24]
    return sorted(set(found + normalized))


def keyword_match_map(job_description: str, resume_text: str) -> dict[str, bool]:
    resume_lower = resume_text.lower()
    return {keyword: keyword.lower() in resume_lower for keyword in extract_keywords(job_description)}
