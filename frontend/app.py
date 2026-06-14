import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer & ATS Optimizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Sleek CSS for Premium Styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0f111a;
        color: #ffffff;
    }
    
    /* Header/Title alignment */
    .title-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        border-radius: 12px;
        color: white;
    }
    .title-container h1 {
        margin: 0;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
    }
    .title-container p {
        margin: 10px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Cards styling */
    .card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Score display */
    .score-container {
        text-align: center;
        padding: 1.5rem;
        border-radius: 50%;
        width: 150px;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        border: 8px solid;
    }
    .score-high {
        border-color: #10b981;
        color: #10b981;
    }
    .score-medium {
        border-color: #f59e0b;
        color: #f59e0b;
    }
    .score-low {
        border-color: #ef4444;
        color: #ef4444;
    }
    
    /* Bullet points styling */
    .bullet-suggest {
        background-color: #1e1b4b;
        border-left: 5px solid #6366f1;
        padding: 10px 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="title-container">
    <h1>📄 AI Resume Analyzer</h1>
    <p>Optimize your resume for ATS systems and get AI-powered improvement suggestions instantly</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab_analyze, tab_rewrite = st.tabs(["🔍 Resume Analyzer & ATS Scorer", "✍️ Bullet Point Rewriter"])

# ==================== TAB 1: RESUME ANALYZER ====================
with tab_analyze:
    st.subheader("Evaluate Your Resume")
    
    col_input, col_results = st.columns([1, 2])
    
    with col_input:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("### 📤 Upload PDF Resume")
        uploaded_file = st.file_uploader(
            "Upload your resume in PDF format", 
            type=["pdf"], 
            help="Please select a PDF file. Scanned images are not supported."
        )
        
        st.write("### 🎯 Target Job Description (Optional)")
        job_description = st.text_area(
            "Paste the job description you are targeting to get a keyword match and missing skills analysis.",
            placeholder="Key skills: Python, FastAPI, Docker, AWS...",
            height=200
        )
        
        analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_results:
        if analyze_btn:
            if uploaded_file is None:
                st.error("Please upload a PDF resume first!")
            else:
                with st.spinner("Analyzing resume... This may take a few seconds."):
                    try:
                        # Prepare files for multipart/form-data upload
                        files = {
                            "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
                        }
                        data = {}
                        if job_description.strip():
                            data["job_description"] = job_description
                        
                        # Call FastAPI endpoint
                        response = requests.post(f"{BACKEND_URL}/api/analyze", files=files, data=data)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Retrieve values
                            score = result.get("ats_score", 0)
                            summary = result.get("summary", "")
                            strengths = result.get("strengths", [])
                            weaknesses = result.get("weaknesses", [])
                            missing_skills = result.get("missing_skills", [])
                            suggestions = result.get("suggestions", [])
                            
                            # Render ATS Score
                            st.write("### 📈 ATS Compatibility Score")
                            
                            # Determine score color class
                            score_class = "score-low"
                            if score >= 75:
                                score_class = "score-high"
                            elif score >= 50:
                                score_class = "score-medium"
                                
                            st.markdown(f"""
                            <div class="score-container {score_class}">
                                <div style="font-size: 2.5rem; font-weight: 800;">{score}</div>
                                <div style="font-size: 0.8rem; font-weight: bold; text-transform: uppercase;">SCORE</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"**Score Interpretation:** {score}/100. " + 
                                       ("Excellent! Your resume matches the standard requirements very well." if score >= 75 else 
                                        "Good effort, but there is substantial room for improvement to pass standard ATS screenings." if score >= 50 else 
                                        "Needs urgent attention. Your resume might get filtered out by modern ATS parsers."))
                            
                            # Display Summary
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.write("#### 📝 Professional Summary")
                            st.write(summary)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Display Strengths & Weaknesses side-by-side
                            col_str, col_weak = st.columns(2)
                            with col_str:
                                st.markdown('<div class="card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
                                st.write("#### ✅ Strengths")
                                for s in strengths:
                                    st.write(f"- {s}")
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                            with col_weak:
                                st.markdown('<div class="card" style="border-top: 4px solid #f59e0b;">', unsafe_allow_html=True)
                                st.write("#### ⚠️ Weaknesses & Gaps")
                                for w in weaknesses:
                                    st.write(f"- {w}")
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                            # Missing Skills
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.write("#### 🔍 Missing Skills & Keywords")
                            if missing_skills:
                                cols = st.columns(min(len(missing_skills), 4))
                                for idx, skill in enumerate(missing_skills):
                                    with cols[idx % 4]:
                                        st.info(f"🔴 {skill}")
                            else:
                                st.success("No critical missing skills identified! Great alignment.")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Suggestions
                            st.markdown('<div class="card" style="border-top: 4px solid #6366f1;">', unsafe_allow_html=True)
                            st.write("#### 💡 Actionable Suggestions for Improvement")
                            for sug in suggestions:
                                st.write(f"- {sug}")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                        else:
                            st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error occurred')}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("Could not connect to the backend server. Please make sure the FastAPI backend is running on port 8000.")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")
        else:
            st.info("Upload your resume and click 'Analyze Resume' to view the breakdown here.")

# ==================== TAB 2: BULLET POINT REWRITER ====================
with tab_rewrite:
    st.subheader("Optimize Your Bullet Points")
    st.write("ATS systems love action-oriented bullet points that quantify achievements. Paste a weak or simple bullet point below, and Gemini will rewrite it to showcase your impact.")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    bullet_input = st.text_area(
        "Enter your resume bullet point:",
        placeholder="Example: I was in charge of managing the database and resolving issues."
    )
    
    rewrite_btn = st.button("✨ Rewrite Bullet Point", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if rewrite_btn:
        if not bullet_input.strip():
            st.warning("Please enter a bullet point first!")
        else:
            with st.spinner("Rewriting bullet point..."):
                try:
                    payload = {"bullet_point": bullet_input}
                    response = requests.post(f"{BACKEND_URL}/api/rewrite-bullet", json=payload)
                    
                    if response.status_code == 200:
                        suggestions = response.json().get("suggestions", [])
                        st.write("### 🚀 Suggested Alternatives:")
                        for idx, sug in enumerate(suggestions, 1):
                            st.markdown(f"""
                            <div class="bullet-suggest">
                                <strong>Alternative {idx}:</strong><br/>
                                {sug}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Failed to rewrite bullet point')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend server. Please make sure the FastAPI backend is running on port 8000.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
