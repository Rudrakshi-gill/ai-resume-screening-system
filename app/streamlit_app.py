import sys
from pathlib import Path

import pandas as pd
import streamlit as st
SKILL_SYNONYMS = {
    "python": [
        "python3",
        "python programming",
    ],
    "java": [
        "java programming",
        "core java",
    ],
    "c++": [
        "cpp",
        "c plus plus",
    ],
    "c": [
        "c programming",
        "c language",
    ],
    "javascript": [
        "js",
        "javascript programming",
    ],
    "typescript": [
        "ts",
        "typescript programming",
    ],
    "machine learning": [
        "ml",
        "machine-learning",
    ],
    "deep learning": [
        "dl",
        "deep-learning",
    ],
    "artificial intelligence": [
        "ai",
        "artificial intelligence",
    ],
    "natural language processing": [
        "nlp",
        "natural-language processing",
    ],
    "computer vision": [
        "cv",
        "computer-vision",
    ],
    "generative ai": [
        "genai",
        "generative artificial intelligence",
    ],
    "large language models": [
        "llm",
        "llms",
        "large language model",
    ],
    "neural networks": [
        "neural network",
        "artificial neural networks",
        "ann",
    ],
    "scikit-learn": [
        "sklearn",
        "scikit learn",
    ],
    "tensorflow": [
        "tensorflow framework",
        "tf",
    ],
    "pytorch": [
        "pytorch framework",
        "torch",
    ],
    "pandas": [
        "pandas library",
        "python pandas",
    ],
    "numpy": [
        "numpy library",
        "numerical python",
    ],
    "matplotlib": [
        "matplotlib library",
        "pyplot",
    ],
    "data analysis": [
        "data analytics",
    ],
    "data visualization": [
        "data visualisation",
        "visualizing data",
    ],
    "sql": [
        "structured query language",
        "sql queries",
    ],
    "mysql": [
        "mysql database",
    ],
    "postgresql": [
        "postgres",
        "postgresql database",
    ],
    "mongodb": [
        "mongo database",
    ],
    "microsoft excel": [
        "ms excel",
        "excel",
    ],
    "power bi": [
        "powerbi",
        "microsoft power bi",
    ],
    "tableau": [
        "tableau software",
    ],
    "git": [
        "git version control",
        "version control with git",
    ],
    "github": [
        "github repository",
        "git hub",
    ],
    "docker": [
        "docker containers",
        "containerization with docker",
    ],
    "kubernetes": [
        "k8s",
        "kubernetes orchestration",
    ],
    "amazon web services": [
        "aws",
        "amazon cloud services",
    ],
    "microsoft azure": [
        "azure",
        "azure cloud",
    ],
    "google cloud platform": [
        "gcp",
        "google cloud",
    ],
    "rest api": [
        "restful api",
        "rest apis",
    ],
    "fastapi": [
        "fast api",
        "fastapi framework",
    ],
    "flask": [
        "flask framework",
        "python flask",
    ],
    "streamlit": [
        "streamlit framework",
        "python streamlit",
    ],
}

# --------------------------------------------------
# Project setup
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.resume_parser import extract_text
from src.matcher import rank_resumes, extract_skills


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="TalentLens | Resume Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Pastel light theme
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* ==========================================
       GLOBAL COLOURS
       ========================================== */

    :root {
        --background: #F7F5FC;
        --surface: #FFFFFF;
        --lavender: #EDE7F7;
        --lavender-dark: #D8CBEA;
        --blue-soft: #E9F0FA;
        --sage-soft: #E7F0E8;
        --text: #454356;
        --muted: #777489;
        --border: #E5DFEE;
        --accent: #A99ACB;
    }

    .stApp {
        background-color: var(--background) !important;
        color: var(--text) !important;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp label {
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background-color: #F7F5FC !important;
    }

    [data-testid="stToolbar"] {
        background-color: transparent !important;
    }

    /* ==========================================
       SIDEBAR
       ========================================== */

    section[data-testid="stSidebar"] {
        background-color: #F0ECF8 !important;
        border-right: 1px solid #E4DDEE;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #F0ECF8 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] strong {
        color: #504B63;
    }

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #77738A !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #DDD5E9 !important;
    }

    /* Sidebar brand */

    .brand-mark {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }

    .brand-icon {
        font-size: 29px;
        color: #9C8ABD !important;
    }

    .brand-name {
        font-size: 20px;
        font-weight: 750;
        color: #49445F !important;
    }

    .brand-sub {
        font-size: 13px;
        color: #77738A !important;
        margin-top: 3px;
    }

    /* Sidebar progress bars */

   /* Sidebar scoring bars — pastel lavender */

section[data-testid="stSidebar"] [data-testid="stProgress"] {
    accent-color: #B9A8D8 !important;
}

section[data-testid="stSidebar"] [data-testid="stProgress"] div {
    border-radius: 10px !important;
}

/* Progress bar background */
section[data-testid="stSidebar"] [data-testid="stProgress"] > div {
    background: #E7E1F0 !important;
}

/* Progress bar fill — override red accents */
section[data-testid="stSidebar"] [data-testid="stProgressBar"],
section[data-testid="stSidebar"] [data-testid="stProgress"] div[role="progressbar"] > div,
section[data-testid="stSidebar"] [data-testid="stProgress"] > div > div {
    background: #B9A8D8 !important;
    background-color: #B9A8D8 !important;
}

    /* ==========================================
       HERO BANNER
       ========================================== */

    .hero {
        background: linear-gradient(
            125deg,
            #EEE8F8 0%,
            #EAF0FA 55%,
            #EDF3EE 100%
        );
        border: 1px solid #E4DDED;
        border-radius: 22px;
        padding: 32px;
        margin: 8px 0 30px 0;
    }

    .eyebrow {
        color: #817594 !important;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero h1 {
        color: #454158 !important;
        font-size: clamp(32px, 4vw, 47px);
        font-weight: 800;
        letter-spacing: -1.2px;
        line-height: 1.2;
        margin: 0 0 15px 0;
    }

    .hero p {
        color: #68657B !important;
        font-size: 16px;
        line-height: 1.8;
        max-width: 850px;
        margin-bottom: 0;
    }

    /* ==========================================
       SECTION HEADINGS
       ========================================== */

    .section-head {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #4A465E;
        font-size: 22px;
        font-weight: 750;
        margin: 20px 0 8px 0;
    }

    .step-tag {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 31px;
        height: 31px;
        border-radius: 10px;
        background: #E7DFF4;
        color: #786795;
        font-size: 14px;
        font-weight: 750;
    }

    .section-sub {
        color: #777489;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 18px;
    }

    /* ==========================================
       PANELS AND CARDS
       ========================================== */

    .panel {
        background: #FFFFFF;
        border: 1px solid #E5DFEE;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .metric {
        background: linear-gradient(145deg, #FFFFFF, #FAF8FD);
        border: 1px solid #E7E1F0;
        border-radius: 16px;
        padding: 19px;
        min-height: 125px;
    }

    .metric-label {
        color: #777389;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-value {
        color: #625777;
        font-size: 28px;
        font-weight: 800;
        margin: 9px 0;
    }

    .metric-note {
        color: #89869A;
        font-size: 12px;
        line-height: 1.6;
    }

    /* ==========================================
       TEXT INPUTS
       ========================================== */

    .stTextInput input,
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #454356 !important;
        -webkit-text-fill-color: #454356 !important;
        caret-color: #454356 !important;
        border: 1px solid #DDD6E9 !important;
        border-radius: 11px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #9691A5 !important;
        -webkit-text-fill-color: #9691A5 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #B9A9D7 !important;
        box-shadow: 0 0 0 2px #EDE7F7 !important;
    }

    /* Select boxes */

    .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #454356 !important;
        border-radius: 10px !important;
    }

    .stSelectbox div[data-baseweb="select"] * {
        color: #454356 !important;
    }

    /* ==========================================
       FILE UPLOADER
       ========================================== */

    div[data-testid="stFileUploader"] {
        background-color: #F5F1FB !important;
        border: 1px solid #E4DCEE !important;
        border-radius: 14px !important;
        padding: 12px !important;
    }

    div[data-testid="stFileUploader"] section {
        background-color: #FCFAFF !important;
        border: 2px dashed #CFC3E3 !important;
        border-radius: 12px !important;
    }

    div[data-testid="stFileUploader"] section,
    div[data-testid="stFileUploader"] section span,
    div[data-testid="stFileUploader"] section small,
    div[data-testid="stFileUploader"] section p {
        color: #625B75 !important;
        -webkit-text-fill-color: #625B75 !important;
    }

    /* Browse files button */

    div[data-testid="stFileUploader"] button {
        background-color: #E5DDF2 !important;
        border: 1px solid #D4C7E8 !important;
        border-radius: 9px !important;
        box-shadow: none !important;
    }

    div[data-testid="stFileUploader"] button,
    div[data-testid="stFileUploader"] button * {
        color: #594D72 !important;
        -webkit-text-fill-color: #594D72 !important;
    }

    div[data-testid="stFileUploader"] button:hover {
        background-color: #DCD1ED !important;
        border-color: #C8B9E2 !important;
    }

    /* Uploaded resume file cards */

    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E1DAEB !important;
        border-radius: 10px !important;
    }

    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
        color: #494558 !important;
        -webkit-text-fill-color: #494558 !important;
    }
    /* Force uploaded-file icon to muted purple-grey */
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] svg,
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] svg path {
        color: #969 !important;
        fill: #969 !important;
        stroke: #969 !important;
}


}
    /* ==========================================
       GENERAL BUTTONS
       ========================================== */

    .stButton > button,
    .stDownloadButton > button {
        background-color: #E2D9F0 !important;
        color: #55496D !important;
        border: 1px solid #D3C6E7 !important;
        border-radius: 11px !important;
        padding: 0.7rem 1rem !important;
        font-weight: 650 !important;
        box-shadow: none !important;
        transition: background-color 0.2s ease;
    }

    .stButton > button *,
    .stDownloadButton > button * {
        color: #55496D !important;
        -webkit-text-fill-color: #55496D !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #D8CDEB !important;
        border-color: #C8B9E1 !important;
    }

    .stButton > button:focus,
    .stDownloadButton > button:focus {
        box-shadow: 0 0 0 2px #EEE8F8 !important;
    }

    /* ==========================================
       EXPANDERS
       ========================================== */

    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5DFEE !important;
        border-radius: 12px !important;
        overflow: hidden;
    }

    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] details > summary {
        background-color: #FFFFFF !important;
        color: #494558 !important;
    }

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary svg {
        color: #494558 !important;
        fill: #77708D !important;
    }

    div[data-testid="stExpander"] summary:hover,
    div[data-testid="stExpander"] summary:hover p {
        background-color: #F8F5FC !important;
        color: #494558 !important;
    }

    div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background-color: #FFFFFF !important;
        color: #494558 !important;
    }

    div[data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
    div[data-testid="stExpander"] [data-testid="stExpanderDetails"] span,
    div[data-testid="stExpander"] [data-testid="stExpanderDetails"] label {
        color: #494558;
    }

    /* ==========================================
       CANDIDATE CARDS
       ========================================== */

    .candidate-card {
        background-color: #FFFFFF;
        border: 1px solid #E5DFEE;
        border-radius: 15px;
        padding: 18px;
        margin: 12px 0;
    }

    .rank-pill {
        display: inline-block;
        background: #EDE6F7;
        color: #786795 !important;
        border-radius: 7px;
        padding: 5px 9px;
        font-size: 11px;
        font-weight: 800;
    }

    .candidate-name {
        color: #494558 !important;
        font-size: 16px;
        font-weight: 750;
        overflow-wrap: anywhere;
    }

    .score-big {
        color: #8A78AC !important;
        font-size: 28px;
        font-weight: 800;
        text-align: right;
    }

    .score-caption {
        color: #89869A !important;
        font-size: 12px;
        text-align: right;
    }

    /* ==========================================
       SKILL LABELS
       ========================================== */

    .skill-chip,
    .missing-chip {
        display: inline-block;
        border-radius: 7px;
        padding: 5px 9px;
        margin: 4px 5px 4px 0;
        font-size: 12px;
        font-weight: 600;
    }

    .skill-chip {
        background: #E6F0E7;
        color: #4F7357 !important;
    }

    .missing-chip {
        background: #F8EEDC;
        color: #896B42 !important;
    }

    /* ==========================================
       RESULTS TABLE
       ========================================== */

    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5DFEE !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    div[data-testid="stDataFrame"] canvas {
        background-color: #FFFFFF !important;
    }

    /* ==========================================
       PROGRESS BARS
       ========================================== */

    div[data-testid="stProgress"] > div {
        background-color: #EAE4F2 !important;
        border-radius: 10px !important;
    }

    div[data-testid="stProgress"] [data-testid="stProgressBar"] {
        background-color: #B7A7D5 !important;
        border-radius: 10px !important;
    }

    /* ==========================================
       LINKS, DIVIDERS AND FOOTER
       ========================================== */

    .stApp a {
        color: #8170A6 !important;
    }

    hr {
        border-color: #E4DDED !important;
    }

    .footer {
        color: #89859A;
        font-size: 12px;
        line-height: 1.8;
        text-align: center;
        padding: 28px 0 12px 0;
    }

    /* Keep the main content comfortable on smaller screens */

    @media (max-width: 768px) {
        .hero {
            padding: 22px;
            border-radius: 16px;
        }

        .hero h1 {
            font-size: 32px;
        }

        .section-head {
            font-size: 19px;
        }
    }
    /* Change the PDF icon background without altering its symbol */
    div[data-testid="stFileChip"] > div:first-child {
        background-color: #969 !important;
}
     
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="brand-mark">
            <div class="brand-icon">✦</div>
            <div>
                <div class="brand-name">TalentLens</div>
                <div class="brand-sub">Resume intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Workspace")
    st.markdown("**01** · Screen candidates")
    st.markdown("**02** · Review match signals")
    st.markdown("**03** · Export results")

    st.divider()

    st.markdown("### Scoring model")
    st.markdown("**70%** · Text similarity")
    st.progress(0.70)

    st.markdown("**30%** · Skill coverage")
    st.progress(0.30)

    st.caption(
        "Prototype weights are heuristic and have not been scientifically validated."
    )

    st.divider()

    st.markdown("### Responsible use")
    st.caption(
        "Use synthetic or consented resumes. Scores support human review; "
        "they must not be the sole basis for hiring decisions."
    )


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">AI-powered recruitment workspace</div>
        <h1>Find relevant talent, faster.</h1>
        <p>
            Compare resumes against a role description with transparent
            text-similarity and skill-coverage signals. Review every result
            with human judgment.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Job description input
# --------------------------------------------------

st.markdown(
    '<div class="section-head">'
    '<span class="step-tag">1</span>Define the role</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-sub">'
    'Upload a job description or paste the role requirements below.'
    '</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1.45], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("**Job description file**")

    jd_upload = st.file_uploader(
        "PDF, DOCX or TXT",
        type=["pdf", "docx", "txt"],
        key="jd",
    )

    st.caption(
        "Tip: include responsibilities, required skills and experience "
        "in the role description."
    )

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    uploaded_jd_text = ""

    if jd_upload:
        try:
            uploaded_jd_text = extract_text(
                jd_upload.name,
                jd_upload.getvalue(),
            )
        except Exception as exc:
            st.error(f"Could not read the job description: {exc}")

    jd_text = st.text_area(
        "Role requirements",
        value=uploaded_jd_text,
        height=160,
        placeholder=(
            "Example: Seeking a Python developer with SQL, machine learning, "
            "NLP, Git and communication skills..."
        ),
        help="You can edit the extracted text before screening.",
    )


# --------------------------------------------------
# Candidate resume input
# --------------------------------------------------

st.markdown(
    '<div class="section-head" style="margin-top:20px">'
    '<span class="step-tag">2</span>Add candidate resumes</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-sub">'
    'Upload multiple resumes together. Supported formats: PDF, DOCX and TXT.'
    '</div>',
    unsafe_allow_html=True,
)

resume_files = st.file_uploader(
    "Drop candidate files here or browse your Mac",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    key="resumes",
)

if resume_files:
    st.caption(
        f"{len(resume_files)} resume file(s) ready for screening."
    )


# --------------------------------------------------
# Analyze and rank candidates
# --------------------------------------------------

analyze = st.button(
    "✦  Analyze and rank candidates",
    type="primary",
    use_container_width=True,
)

if analyze:
    if not jd_text.strip():
        st.warning("Add a job description before screening candidates.")

    elif not resume_files:
        st.warning("Upload at least one candidate resume to continue.")

    else:
        parsed = []
        errors = []

        progress = st.progress(
            0,
            text="Preparing candidate files…",
        )

        for index, uploaded in enumerate(resume_files):
            try:
                text = extract_text(
                    uploaded.name,
                    uploaded.getvalue(),
                )

                if text.strip():
                    parsed.append(
                        {
                            "filename": uploaded.name,
                            "text": text,
                        }
                    )
                else:
                    errors.append(
                        f"{uploaded.name}: no readable text found. "
                        "Scanned PDFs may require OCR."
                    )

            except Exception as exc:
                errors.append(f"{uploaded.name}: {exc}")

            progress.progress(
                (index + 1) / len(resume_files),
                text=(
                    f"Reading resume {index + 1} "
                    f"of {len(resume_files)}…"
                ),
            )

        progress.empty()

        for error in errors:
            st.warning(error)

        if parsed:
            try:
                st.session_state["screening_results"] = rank_resumes(
                    parsed,
                    jd_text,
                )

                st.session_state["screening_jd_skills"] = extract_skills(
                    jd_text,
                )

                st.session_state["screening_jd_text"] = jd_text
                st.session_state["screening_errors"] = errors

            except Exception as exc:
                st.error(f"Could not rank these resumes: {exc}")


# --------------------------------------------------
# Results
# --------------------------------------------------

results = st.session_state.get("screening_results", [])

if results:
    st.divider()

    st.markdown(
        '<div class="section-head">'
        '<span class="step-tag">3</span>Screening overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">'
        'A ranked view of textual relevance. Review the underlying signals '
        'before drawing conclusions.'
        '</div>',
        unsafe_allow_html=True,
    )

    top = results[0]
    jd_skills = st.session_state.get("screening_jd_skills", [])

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    metrics = [
        (
            "Resumes screened",
            str(len(results)),
            "Files with readable text",
        ),
        (
            "Top match score",
            f"{top['score'] * 100:.1f}%",
            "Highest heuristic score",
        ),
        (
            "Skills identified",
            str(len(jd_skills)),
            "From built-in skill dictionary",
        ),
        (
            "Needs review",
            str(len(results)),
            "Human review recommended",
        ),
    ]

    for col, (label, value, note) in zip(
        [c1, c2, c3, c4],
        metrics,
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-head" style="margin-top:28px">'
        'Candidate leaderboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">'
        'Candidates are ordered by the combined prototype score, not by a '
        'validated measure of job performance.'
        '</div>',
        unsafe_allow_html=True,
    )

    for i, item in enumerate(results):
        score = round(item["score"] * 100, 1)

        with st.container():
            st.markdown(
                '<div class="candidate-card">',
                unsafe_allow_html=True,
            )

            top_left, top_right = st.columns([4, 1])

            with top_left:
                st.markdown(
                    f'<div><span class="rank-pill">RANK #{i + 1}</span>'
                    f' &nbsp; <span class="candidate-name">'
                    f'{item["filename"]}</span></div>',
                    unsafe_allow_html=True,
                )

                st.progress(
                    max(0.0, min(1.0, float(item["score"])))
                )

            with top_right:
                st.markdown(
                    f'<div class="score-big">{score:.1f}%</div>'
                    '<div class="score-caption">overall match</div>',
                    unsafe_allow_html=True,
                )

            a, b = st.columns(2)

            with a:
                st.caption(
                    f"Text similarity · {item['similarity'] * 100:.1f}%"
                )

            with b:
                st.caption(
                    f"Skill coverage · "
                    f"{item['skill_coverage'] * 100:.1f}%"
                )

            with st.expander("Review matching signals"):
                st.markdown("**Matched skills**")

                if item["matched_skills"]:
                    matched_html = "".join(
                        f'<span class="skill-chip">✓ {skill}</span>'
                        for skill in item["matched_skills"]
                    )

                    st.markdown(
                        matched_html,
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption(
                        "No listed job-description skills were detected "
                        "in this resume."
                    )

                st.markdown("**Skills not detected**")

                if item["missing_skills"]:
                    missing_html = "".join(
                        f'<span class="missing-chip">+ {skill}</span>'
                        for skill in item["missing_skills"]
                    )

                    st.markdown(
                        missing_html,
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption(
                        "All skills from the built-in dictionary detected "
                        "in the job description were found in this resume."
                    )

            st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------
    # Results table and CSV export
    # ----------------------------------------------

    display = pd.DataFrame(
        [
            {
                "Rank": i + 1,
                "Candidate file": item["filename"],
                "Overall match (%)": round(item["score"] * 100, 1),
                "Text similarity (%)": round(
                    item["similarity"] * 100,
                    1,
                ),
                "Skill coverage (%)": round(
                    item["skill_coverage"] * 100,
                    1,
                ),
                "Matched skills": (
                    ", ".join(item["matched_skills"]) or "None detected"
                ),
                "Skills not detected": (
                    ", ".join(item["missing_skills"]) or "None"
                ),
            }
            for i, item in enumerate(results)
        ]
    )

    export_col, _ = st.columns([1, 2])

    with export_col:
        st.download_button(
            "↓  Export ranking as CSV",
            data=display.to_csv(index=False).encode("utf-8"),
            file_name="resume_screening_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with st.expander("View full results table"):
        st.dataframe(
            display,

            use_container_width=True,
            hide_index=True,
            height=400,
        )
        

    with st.expander("Detected job-description skills"):
        st.write(
            ", ".join(jd_skills)
            or "No skills from the built-in dictionary were detected."
        )

    with st.expander("Methodology and limitations"):
        st.markdown(
            "- Combined score = 35% TF-IDF cosine similarity + 35% "
"semantic similarity using NLP embeddings + 30% skill coverage.\n"
"- TF-IDF measures word overlap and may miss synonyms or "
"equivalent experience.\n"
"- Semantic similarity helps identify related meanings, but may "
"still misinterpret context or overlook important differences.\n"
"- Skill detection uses a built-in dictionary of skills and synonyms; "
"it may miss relevant skills or interpret context incorrectly.\n"
"- Scores do not measure actual ability, personality, culture "
"fit or future performance.\n"
"- Do not use protected characteristics or proxies to rank "
"people. Keep a human reviewer in control and offer candidates "
"a fair, accessible process."
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        TALENTLENS · Academic prototype v0.2 · Python · Streamlit · scikit-learn
        <br>
        Candidate scores are decision-support signals only, not hiring
        recommendations.
    </div>
    """,
    unsafe_allow_html=True,
)