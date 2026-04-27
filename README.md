# 🚀 FitCheck AI

**Intelligent Resume Optimization & Job Matching System using RAG, Agentic AI, DevOps, and Data Analytics**

---

## 📌 Project Overview

FitCheck AI is an AI-powered system that analyzes a candidate’s resume against a job description and provides actionable insights such as fit score, skill gaps, and improvement suggestions.

The goal of this project is to help candidates optimize their resumes, understand job requirements better, and improve their chances of getting selected.

---

## 🎯 Key Features

* 🔥 **Fit Score Calculation** – Measures how well a resume matches a job description
* ❌ **Skill Gap Analysis** – Identifies missing skills required for the role
* ✅ **Strength & Weakness Detection** – Highlights strong and weak areas
* 💡 **Smart Suggestions** – Provides actionable recommendations
* 🎯 **Interview Preparation** – Generates expected interview questions
* 📊 **Interactive Dashboard** – Visual representation of analysis

---

## 🧠 Technologies Used

* **Programming Language:** Python
* **Backend:** FastAPI
* **Frontend:** Streamlit
* **AI/ML:** RAG (Retrieval-Augmented Generation), NLP
* **Vector Database:** FAISS
* **DevOps:** Docker, CI/CD (conceptual)
* **Visualization:** Streamlit Dashboard

---

## ⚙️ System Architecture

```
Resume → Text Processing → Chunking → Embedding → Vector DB (FAISS)
       → Retrieval (RAG) → AI Analysis → Dashboard Output
```

---

## 🤖 Agentic AI Workflow

```
Input (Resume + JD)
      ↓
Retrieve Relevant Data
      ↓
Analyze & Compare
      ↓
Generate Insights (Fit Score, Gaps, Suggestions)
```

---

## 🔁 DevOps Pipeline (Conceptual)

```
Code → GitHub → CI/CD → Docker → Deployment
```

---

## 📊 Output Dashboard

The system provides:

* Fit Score Visualization
* Skill Match Chart
* Keyword Coverage
* Missing Skills
* Strengths & Weak Areas

👉 *(Add your dashboard screenshot here)*

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository

```
git clone https://github.com/suryansh2306/fitcheck-ai.git
cd fitcheck-ai
```

### 2️⃣ Create Virtual Environment

```
python -m venv .venv
.\.venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run Backend

```
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 5️⃣ Run Frontend

```
streamlit run frontend/app.py
```

---

## 📈 Results & Benefits

* Faster resume evaluation
* Better alignment with job roles
* Reduced manual effort
* Clear and actionable insights

---

## 🔮 Future Scope

* Integration with job portals
* ATS compatibility scoring
* Resume auto-generation
* Advanced AI model integration

---

## 👨‍💻 Author

**Suryansh**
Medicaps University
Enrollment No: EN22CS3011003

---

## ⭐ Acknowledgment

This project is developed as a final year B.Tech major project focusing on practical applications of AI in recruitment and career optimization.

---
