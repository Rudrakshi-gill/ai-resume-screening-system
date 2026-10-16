"""Resume ranking using TF-IDF similarity and normalized skill coverage."""

import re
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
@st.cache_resource
def load_semantic_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2",
        device="cpu",
    )

# Canonical skill names and their common variations.
# Variations are mapped to one consistent skill name.
SKILL_SYNONYMS = {
    "python": ["python", "python3", "python programming"],
    "java": ["java", "java programming"],
    "c++": ["c++", "cpp"],
    "c": ["c language", "programming in c"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "natural language processing": [
        "natural language processing",
        "nlp",
    ],
    "computer vision": ["computer vision", "cv"],
    "generative ai": ["generative ai", "genai", "generative artificial intelligence"],
    "large language models": [
        "large language models",
        "large language model",
        "llms",
        "llm",
    ],
    "neural networks": ["neural networks", "neural network"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "data visualisation"],
    "sql": ["sql", "structured query language"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo db"],
    "excel": ["excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "git": ["git", "version control"],
    "github": ["github", "git hub"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "google cloud": ["google cloud", "gcp"],
    "rest api": ["rest api", "restful api", "rest apis"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "streamlit": ["streamlit"],
    "django": ["django"],
    "html": ["html"],
    "css": ["css"],
    "react": ["react", "reactjs", "react.js"],
    "linux": ["linux"],
    "spacy": ["spacy", "spaCy"],
    "transformers": ["transformers", "hugging face transformers"],
    "sentence transformers": ["sentence transformers", "sentence-transformers"],
    "statistics": ["statistics", "statistical analysis"],
    "communication": ["communication", "communication skills"],
    "project management": ["project management"],
    "problem solving": ["problem solving", "problem-solving"],
}


def normalize(text: str) -> str:
    """Normalize text for consistent matching."""
    text = (text or "").lower()
    return re.sub(r"\s+", " ", text).strip()


def contains_phrase(text: str, phrase: str) -> bool:
    """Check for a phrase without matching it inside unrelated words."""
    pattern = (
        r"(?<![a-z0-9+#])"
        + re.escape(phrase.lower())
        + r"(?![a-z0-9+#])"
    )
    return bool(re.search(pattern, text))


def extract_skills(text: str) -> list[str]:
    """Return canonical skill names found in the text."""
    normalized = normalize(text)
    found = []

    for canonical_name, variations in SKILL_SYNONYMS.items():
        if any(
            contains_phrase(normalized, variation)
            for variation in variations
        ):
            found.append(canonical_name)

    return sorted(set(found))


def rank_resumes(
    resumes: list[dict],
    job_description: str,
) -> list[dict]:
    """Rank resumes using TF-IDF, semantic similarity, and skill coverage."""

    if not resumes:
        return []

    jd = (job_description or "").strip()

    if not jd:
        raise ValueError("Job description cannot be empty.")

    resume_texts = [
        item.get("text", "") or ""
        for item in resumes
    ]

    # 1. TF-IDF similarity
    texts = [jd] + resume_texts

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    matrix = vectorizer.fit_transform(texts)

    tfidf_scores = cosine_similarity(
        matrix[0:1],
        matrix[1:],
    ).flatten()

    # 2. Semantic similarity
    # The model downloads its files on first use if they are not cached.
    model = load_semantic_model()

    embeddings = model.encode(
        [jd] + resume_texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    semantic_scores = embeddings[1:] @ embeddings[0]

    # Convert cosine similarity from [-1, 1] to [0, 1].
    semantic_scores = [
        max(0.0, min(1.0, (float(value) + 1.0) / 2.0))
        for value in semantic_scores
    ]

    # 3. Skill coverage
    jd_skills = set(extract_skills(jd))
    results = []

    for resume, tfidf, semantic in zip(
        resumes,
        tfidf_scores,
        semantic_scores,
    ):
        resume_skills = set(
            extract_skills(resume.get("text", "") or "")
        )

        if jd_skills:
            matched = sorted(jd_skills & resume_skills)
            missing = sorted(jd_skills - resume_skills)
            coverage = len(matched) / len(jd_skills)
        else:
            matched = []
            missing = []
            coverage = 0.0

        # Experimental weights: evaluate these using labelled examples.
        score = (
            0.35 * float(tfidf)
            + 0.35 * float(semantic)
            + 0.30 * coverage
        )

        results.append({
            "filename": resume.get(
                "filename",
                "Unnamed resume",
            ),
            "score": max(0.0, min(1.0, score)),
            "similarity": float(tfidf),
            "semantic_similarity": float(semantic),
            "skill_coverage": float(coverage),
            "matched_skills": matched,
            "missing_skills": missing,
        })

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True,
    )