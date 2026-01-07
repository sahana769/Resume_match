import os
import streamlit as st
import google.generativeai as genai
from pdf_text_extractor import extract_text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_GEMINI_API")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-lite-latest")

# ---------------- UI ----------------
st.header("SKILL MATCHER: :blue[AI assisted skill matching tool]")

tips = """
📌 Upload your resume in the sidebar (PDF format only)  
📌 Copy and paste the job description  
📌 Submit and see the AI-powered skill matching results
"""
st.write(tips)

# ---------------- Sidebar ----------------
st.sidebar.header('UPLOAD YOUR RESUME HERE', divider='green')
st.sidebar.subheader('PDF format only')

pdf_doc = st.sidebar.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

pdf_text = ""
if pdf_doc:
    pdf_text = extract_text(pdf_doc)
else:
    st.sidebar.info('Please upload a PDF resume')

# ---------------- Job Description ----------------
job_desc = st.text_area(
    "Paste the Job Description here",
    max_chars=2000,
    height=300
)

# ---------------- Prompt ----------------
if pdf_text and job_desc:
    prompt = f"""
    Assuming you are an expert in job skill matching and profile shortlisting.

    Resume:
    {pdf_text}

    Job Description:
    {job_desc}

    Generate the following output:

    • Calculate and show the ATS score. Discuss matching and non-matching keywords (max 2 lines).
    • Calculate and show chances of selection (1 line).
    • Perform SWOT analysis in bullet points.
    • List resume positives that help shortlisting.
    • Suggest improvements for the resume.
    • Prepare TWO revised resumes optimized for this job description.
    • Ensure resumes can be copied to Word and exported as PDF.
    """

    if st.button("Analyze Resume"):
        response = model.generate_content(prompt)
        st.subheader("📊 AI Analysis Result")
        st.write(response.text)
else:
    st.warning("Please upload a resume and paste a job description.")
