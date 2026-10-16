# TalentLens — Resume Intelligence

TalentLens is a student-built Streamlit prototype for comparing multiple resumes with a job description. It extracts text from PDF, DOCX, and TXT files, identifies skills using a synonym-aware dictionary, calculates text and semantic similarity, and exports a ranked results table.

> **Decision-support prototype only.** Scores are experimental text-relevance signals, not validated hiring criteria. A human reviewer must assess candidates fairly; never use this score as the sole basis for a hiring or rejection decision.

## Features

- Upload one job description as text or PDF/DOCX/TXT.
- Upload multiple candidate resumes in PDF, DOCX, or TXT format.
- Extract resume text and report files that could not be read.
- Rank resumes using TF-IDF similarity, sentence-embedding semantic similarity, and detected-skill coverage.
- Display matched skills, skills not detected, component scores, and overall ranking.
- Export results as CSV.
- Pastel lavender-grey interface and light Streamlit theme.

## Scoring method

The current experimental score is:

`Overall score = 0.35 × TF-IDF similarity + 0.35 × semantic similarity + 0.30 × job-skill coverage`

The three components are combined as a transparent heuristic. The weights have not been scientifically validated. Evaluate and tune them only with a documented, representative, consented or synthetic dataset and appropriate evaluation metrics. Similarity does not verify the truth of a resume or measure a person's ability, personality, culture fit, or future performance.

## Project structure

- `app/streamlit_app.py` — Streamlit interface and results display
- `src/resume_parser.py` — PDF/DOCX/TXT text extraction
- `src/matcher.py` — skill extraction, TF-IDF, semantic similarity, and ranking
- `tests/test_matcher.py` — starter unit tests
- `.streamlit/config.toml` — light lavender-grey theme
- `requirements.txt` — Python dependencies
- `run_app.py` — configured Streamlit launcher

## Setup and launch

1. Create a Python environment. Python 3.11 is a conservative compatibility choice for the dependencies.
2. Install the packages in `requirements.txt` using your preferred Python package manager.
3. Open the project folder in VS Code.
4. Launch the app using the project's `run_app.py` runner or a configured Streamlit IDE runner. The standard Streamlit command is `streamlit run app/streamlit_app.py`.
5. On first use, `sentence-transformers` downloads the `all-MiniLM-L6-v2` model if it is not already cached. The model is configured to run on CPU for compatibility.
6. Add a job description and upload synthetic or consented resumes.

## Known limitations

- Scanned/image-only PDFs may not contain extractable text; OCR is not included.
- The built-in skill dictionary is limited and may miss relevant skills or match context incorrectly.
- TF-IDF relies on word overlap; semantic similarity may still misinterpret context.
- Resume claims, employment history, qualifications, and experience are not verified.
- Results can be affected by document formatting and wording.

## Responsible use and privacy

- Do not upload real resumes without appropriate permission and safeguards.
- Do not score or rank using protected characteristics or proxies, including age, gender, caste, religion, disability, photographs, or names.
- Do not use the score as the sole basis for hiring or rejection.
- Keep a human reviewer in control and provide candidates with a fair, accessible process.
- Do not commit private resumes, exported result CSVs, model caches, credentials, or secrets to GitHub.
