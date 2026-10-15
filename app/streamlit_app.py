import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.resume_parser import extract_text
from src.matcher import rank_resumes, extract_skills

st.set_page_config(page_title="AI Resume Screening", page_icon="📄", layout="wide")

st.title("AI-Based Resume Screening & Candidate Ranking")
st.caption("A decision-support prototype using NLP and machine learning — not an automated hiring decision.")

with st.sidebar:
    st.header("How scoring works")
    st.write("**70%** TF-IDF text similarity")
    st.write("**30%** job-skill coverage")
    st.caption("These are initial, configurable prototype weights, not scientifically validated hiring criteria.")
    st.divider()
    st.write("Privacy: use synthetic or consented resumes. Uploaded files are processed in this app session and are not intentionally saved to a database.")

st.subheader("1. Add the job description")
jd_upload = st.file_uploader("Optional: upload a job description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], key="jd")
jd_text = ""
if jd_upload:
    try:
        jd_text = extract_text(jd_upload.name, jd_upload.getvalue())
    except Exception as exc:
        st.error(f"Could not read the job description: {exc}")

jd_text = st.text_area(
    "Paste or edit the job description",
    value=jd_text,
    height=220,
    placeholder="Example: We are seeking a Python developer with SQL, machine learning, NLP, Git, and communication skills..."
)

st.subheader("2. Upload candidate resumes")
resume_files = st.file_uploader(
    "Choose one or more PDF, DOCX, or TXT resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    key="resumes",
)

if st.button("Analyze and rank candidates", type="primary", use_container_width=True):
    if not jd_text.strip():
        st.warning("Please paste or upload a job description first.")
    elif not resume_files:
        st.warning("Please upload at least one resume.")
    else:
        parsed = []
        errors = []
        for uploaded in resume_files:
            try:
                text = extract_text(uploaded.name, uploaded.getvalue())
                if text.strip():
                    parsed.append({"filename": uploaded.name, "text": text})
                else:
                    errors.append(f"{uploaded.name}: no readable text found (scanned PDFs may need OCR).")
            except Exception as exc:
                errors.append(f"{uploaded.name}: {exc}")

        if errors:
            for error in errors:
                st.warning(error)

        if parsed:
            results = rank_resumes(parsed, jd_text)
            st.subheader("3. Candidate ranking")
            st.info("Scores indicate textual relevance to this job description. They should be reviewed by a human and must not be used as the sole basis for hiring.")
            display = pd.DataFrame([
                {
                    "Rank": i + 1,
                    "Candidate file": item["filename"],
                    "Overall match (%)": round(item["score"] * 100, 1),
                    "Text similarity (%)": round(item["similarity"] * 100, 1),
                    "Skill coverage (%)": round(item["skill_coverage"] * 100, 1),
                    "Matched skills": ", ".join(item["matched_skills"]) or "None detected",
                    "Skills not detected": ", ".join(item["missing_skills"]) or "None",
                }
                for i, item in enumerate(results)
            ])
            st.dataframe(display, use_container_width=True, hide_index=True)
            st.download_button(
                "Download results as CSV",
                data=display.to_csv(index=False).encode("utf-8"),
                file_name="resume_screening_results.csv",
                mime="text/csv",
            )
            with st.expander("View detected job-description skills"):
                st.write(", ".join(extract_skills(jd_text)) or "No skills from the built-in dictionary were detected.")
            with st.expander("Important limitations"):
                st.markdown(
                    "- TF-IDF measures word overlap and may miss equivalent meanings.\n"
                    "- Skill detection uses a small editable dictionary; it can miss skills or detect context incorrectly.\n"
                    "- Scores do not assess actual ability, culture fit, personality, or future performance.\n"
                    "- Do not use protected characteristics or proxies to rank people.\n"
                    "- Keep a human reviewer in control and provide candidates a fair, accessible process."
                )

st.divider()
st.caption("Prototype v0.1 • Built with Python, Streamlit, scikit-learn, PyMuPDF, and python-docx.")
