# 📄 ResumeAnalyzer - AI-Powered Resume Screener & ATS Optimizer

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5--Flash--Lite-orange.svg?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)

An elegant, beginner-friendly **Agentic AI** project designed to screen and optimize resumes using an AI-powered pipeline. This application parses PDF resumes, analyzes them against a target job description using the **Google Gemini 2.5 Flash** model, and presents the insights on an interactive dashboard.

LIVE LINK : https://resumeanalyzer-frontend-0ern.onrender.com
---

## 🌟 Key Features

*   **📈 ATS Score Gauge**: Visual indicator showing how well the resume matches standard recruitment system requirements (0-100 scale).
*   **🔍 Keyword & Skill Gap Analysis**: Automatically identifies critical technical or soft skills missing from the resume when matched against a target Job Description.
*   **✅ Strengths & Weaknesses Breakdown**: Generates clear, structured points identifying the strongest aspects of the resume and areas needing attention.
*   **💡 Actionable Improvement Suggestions**: Step-by-step suggestions to help the resume stand out.
*   **✨ AI Bullet Point Rewriter**: An interactive tool to rewrite weak resume bullet points into high-impact, results-oriented metrics (using the Google XYZ formula).

---

## 🛠️ Tech Stack

*   **Frontend**: `Streamlit` (Interactive Python Web Application Framework)
*   **Backend**: `FastAPI` (High-performance API server with automatic documentation)
*   **PDF Extraction**: `PyPDF2` (Parses PDF text streams in-memory)
*   **LLM/AI Model**: `Google Gemini 2.5 Flash Lite` (via the latest `google-genai` SDK)
*   **Environment Management**: `python-dotenv`

---

## 📐 Project Architecture

```mermaid
graph TD
    A[User / PDF Resume & JD] -->|Uploads PDF & submits| B(Streamlit Frontend - app.py)
    B -->|Sends Multipart Form POST Request| C(FastAPI Backend - main.py)
    C -->|Extracts text in-memory| D[PyPDF2 Parser]
    D -->|Plain Text Resume| C
    C -->|Constructs Prompt & Response Schema| E[Google Gemini 2.5 Flash]
    E -->|Structured JSON Response| C
    C -->|Validated JSON Response| B
    B -->|Displays Score, Strengths, Suggestions| F[User Dashboard]
```

---

## 📂 Project Directory Structure

```text
ResumeAnalyzer/
├── backend/
│   └── main.py          # FastAPI server handling API routes and Gemini LLM logic
├── frontend/
│   └── app.py           # Streamlit UI dashboard code
├── .env                 # API Keys & Local System Configurations (gitignore this in production)
├── requirements.txt      # Python dependencies for the entire project
└── README.md            # Detailed project documentation (this file)
```

---

## ⚙️ Installation & Local Setup

Follow these simple steps to run this project locally:

### 1. Clone the repository
```bash
git clone https://github.com/Gargi3012/ResumeAnalyzer.git
cd ResumeAnalyzer
```

### 2. Install Python Packages
Install all required libraries for both the backend and frontend using the single root-level `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
BACKEND_URL=http://localhost:8000
```
> ⚠️ **Note**: A default Gemini key has been configured inside the backend, but it's highly recommended to replace it with your own key.

---

## 🚦 How to Run the Application

You need to run the **Backend** and **Frontend** servers concurrently in separate terminal windows.

### Step 1: Start the Backend (FastAPI)
Run the following command from the root directory:
```bash
uvicorn backend.main:app --reload
```
*   **URL**: `http://localhost:8000`
*   **Interactive Documentation (Swagger UI)**: `http://localhost:8000/docs`

### Step 2: Start the Frontend (Streamlit)
Open a new terminal window, navigate to the root directory, and run:
```bash
streamlit run frontend/app.py
```
*   **URL**: `http://localhost:8501` (Opens automatically in your browser)

---
<img width="866" height="440" alt="Screenshot 2026-06-15 002240" src="https://github.com/user-attachments/assets/653f86d9-6b98-4b90-b1d2-2311b1f897da" />

<img width="584" height="413" alt="Screenshot 2026-06-15 002327" src="https://github.com/user-attachments/assets/3f860e18-ab27-44e4-aa81-593c12194228" />


## 💡 Developer Insights

This project demonstrates several best practices for building modern LLM-powered applications:

1.  **Structured AI Responses (`response_schema`)**: Instead of parsing unreliable text outputs, we use the `google-genai` SDK's structured output mode. By passing a Pydantic class (`AnalysisResult`) to the model config, the Gemini model is forced to output valid JSON matching our exact schema.
2.  **In-Memory PDF Parsing**: Instead of saving uploaded files to disk (which causes storage leak and file-system write issues on cloud platforms), we use `io.BytesIO` along with `PyPDF2` to extract text instantly in-memory.
3.  **Clean Separation of Concerns**: The backend handles CPU-heavy PDF parsing and LLM integration, while the frontend handles only the rendering and presentation layer.
