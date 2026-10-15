"""Baseline resume ranking using TF-IDF similarity and transparent skill coverage."""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A starter dictionary, not a comprehensive taxonomy. Extend it for your project domain.
SKILLS = [
    "python", "java", "c++", "sql", "mysql", "postgresql", "mongodb",
    "machine learning", "deep learning", "natural language processing", "nlp",
    "data analysis", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "streamlit", "flask", "django", "html", "css", "javascript", "react",
    "git", "github", "docker", "aws", "azure", "linux", "excel",
    "communication", "project management", "statistics", "data visualization",
    "power bi", "tableau", "problem solving", "computer vision", "spacy",
    "transformers", "sentence transformers", "rest api", "fastapi"
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def extract_skills(text: str) -> list[str]:
    normalized = normalize(text)
    found = []
    for skill in SKILLS:
        # Boundaries avoid matching short skills inside unrelated words.
        pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"
        if re.search(pattern, normalized):
            found.append(skill)
    return sorted(set(found))


def rank_resumes(resumes: list[dict], job_description: str) -> list[dict]:
    """Return ranked resume dictionaries with scores from 0 to 1."""
    if not resumes:
        return []
    jd = (job_description or "").strip()
    if not jd:
        raise ValueError("Job description cannot be empty.")

    texts = [jd] + [item.get("text", "") or "" for item in resumes]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(texts)
    similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    jd_skills = set(extract_skills(jd))
    results = []
    for resume, similarity in zip(resumes, similarities):
        resume_skills = set(extract_skills(resume.get("text", "")))
        if jd_skills:
            matched = sorted(jd_skills & resume_skills)
            missing = sorted(jd_skills - resume_skills)
            coverage = len(matched) / len(jd_skills)
        else:
            matched, missing, coverage = [], [], 0.0

        # Initial heuristic weights. Validate and tune using a labelled evaluation set.
        score = (0.70 * float(similarity)) + (0.30 * coverage)
        results.append({
            "filename": resume.get("filename", "Unnamed resume"),
            "score": max(0.0, min(1.0, score)),
            "similarity": float(similarity),
            "skill_coverage": float(coverage),
            "matched_skills": matched,
            "missing_skills": missing,
        })
    return sorted(results, key=lambda item: item["score"], reverse=True)
