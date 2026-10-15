# AI-Based Resume Screening and Candidate Ranking System

A student project prototype that compares resumes with a job description using NLP-style text features and a transparent skill dictionary.

## Features in v0.1
- Upload multiple PDF, DOCX, or TXT resumes.
- Paste or upload one job description.
- Extract text from PDFs and Word documents.
- Rank resumes with TF-IDF and cosine similarity.
- Detect skills from a small built-in dictionary.
- Show matched skills, skills not detected, and component scores.
- Export the result table to CSV.

## Scoring method
The prototype currently uses:

`Overall score = 0.70 × TF-IDF similarity + 0.30 × job-skill coverage`

These weights are an initial heuristic for demonstrating the pipeline. They are **not validated hiring criteria**. A proper evaluation should use a documented, representative, consented or synthetic dataset and metrics appropriate to the task. Scores must not be treated as a decision about a person's worth or hiring suitability.

## Run from VS Code without typing commands
1. Open this project folder in VS Code.
2. In Anaconda Navigator, use the Environments interface to create a Python environment (Python 3.11 is a conservative compatibility choice).
3. Install the packages listed in `requirements.txt` using a GUI package manager where available. If a package is unavailable there, you may need a package-installation interface that supports pip.
4. Open `app/streamlit_app.py` and run it with a Streamlit-capable IDE extension or configured run profile. Streamlit apps normally need to be launched with `streamlit run app/streamlit_app.py`; this README intentionally does not require using Terminal if your IDE provides a GUI runner.
5. Upload synthetic test resumes and a sample job description.

GUI tools differ by setup, and a normal Python “Run” button may not launch Streamlit correctly.

## Project structure
- `app/streamlit_app.py` — web interface
- `src/resume_parser.py` — PDF/DOCX/TXT extraction
- `src/matcher.py` — skill detection and ranking logic
- `tests/test_matcher.py` — starter unit tests
- `data/sample_job_descriptions/` — synthetic job description
- `data/sample_resumes/` — synthetic sample resumes

## Known limitations
- Scanned PDFs need OCR, which is not included yet.
- Skill dictionary is small and may miss relevant skills or detect terms without understanding context.
- TF-IDF is based on word overlap and does not fully understand meaning.
- Work experience and education are not independently verified or scored.
- Results may reflect wording and formatting differences.
- This tool is decision support only; a human must review results.

## Responsible use
- Do not upload real resumes without appropriate permission and safeguards.
- Do not use protected characteristics, photos, names, age, gender, religion, disability, caste, or proxies as scoring features.
- Do not use a score as the sole basis for rejecting or hiring a candidate.
- Explain the limitations to reviewers and provide an accessible alternative review process.

## Roadmap
1. Add semantic matching with sentence embeddings and compare against TF-IDF.
2. Expand and document the skill taxonomy.
3. Add stronger validation, edge-case tests, and evaluation metrics.
4. Add architecture, workflow, and use-case diagrams.
5. Add screenshots and project report/bibliography with sources actually consulted.
