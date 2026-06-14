import os
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import PyPDF2
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Resume Analyzer API",
    description="Backend API for analyzing resumes and rewriting bullet points using Gemini",
    version="1.0.0"
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini Client
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it in your .env file.")
client = genai.Client(api_key=gemini_key)

# Define schemas for Structured Outputs
class AnalysisResult(BaseModel):
    ats_score: int = Field(description="ATS compatibility score from 0 to 100")
    summary: str = Field(description="Brief professional summary of the resume")
    strengths: list[str] = Field(description="List of key strengths found in the resume")
    weaknesses: list[str] = Field(description="List of weaknesses or areas of improvement")
    missing_skills: list[str] = Field(description="Key skills/keywords missing from the resume (especially relative to job description)")
    suggestions: list[str] = Field(description="Actionable feedback to improve the resume")

class BulletRewriteResult(BaseModel):
    suggestions: list[str] = Field(description="Exactly 3 high-impact rewritten suggestions for the bullet point")

# Helper to extract text from PDF
def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF. The file might be scanned or empty.")
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF file: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Resume Analyzer API is up and running!"}

@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(None)
):
    # Ensure it's a PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Read file bytes and extract text
    file_bytes = await file.read()
    resume_text = extract_text_from_pdf(file_bytes)
    
    # Construct Gemini Prompt
    prompt = f"""
You are an expert ATS (Applicant Tracking System) recruiter and resume analyzer.
Analyze the following resume and compare it against the provided Job Description (if any).

Resume Content:
{resume_text}

Job Description (Optional):
{job_description or "Not Provided"}

Analyze the resume and fill out the response structure. Keep comments professional and constructive.
"""
    
    try:
        # Generate content using Gemini 2.5 Flash Lite
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AnalysisResult,
                temperature=0.2, # Lower temperature for more analytical/consistent scoring
            )
        )
        # The response.text is guaranteed to match the AnalysisResult JSON structure
        return AnalysisResult.model_validate_json(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Gemini API: {str(e)}")

class BulletRewriteRequest(BaseModel):
    bullet_point: str

@app.post("/api/rewrite-bullet", response_model=BulletRewriteResult)
def rewrite_bullet(request: BulletRewriteRequest):
    if not request.bullet_point.strip():
        raise HTTPException(status_code=400, detail="Bullet point cannot be empty.")
        
    prompt = f"""
You are an expert resume writer. Rewrite the following resume bullet point to make it more professional, high-impact, and results-oriented.
Use the Google XYZ formula (Accomplished [X] as measured by [Y], by doing [Z]) or strong action verbs where appropriate.
Provide exactly 3 diverse, high-impact alternative bullet points.

Original Bullet Point:
"{request.bullet_point}"
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=BulletRewriteResult,
                temperature=0.7, # Higher temperature for more creative rewrites
            )
        )
        return BulletRewriteResult.model_validate_json(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Gemini API: {str(e)}")
