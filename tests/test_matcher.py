import pytest
from src.matcher import extract_skills, rank_resumes


def test_extracts_known_skills_case_insensitively():
    assert extract_skills("PYTHON, SQL and machine learning") == [
        "machine learning", "python", "sql"
    ]


def test_ranks_relevant_resume_higher():
    jd = "Python developer with SQL and machine learning experience"
    resumes = [
        {"filename": "general.txt", "text": "I enjoy teamwork and office administration."},
        {"filename": "relevant.txt", "text": "Python SQL machine learning pandas projects."},
    ]
    ranked = rank_resumes(resumes, jd)
    assert ranked[0]["filename"] == "relevant.txt"
    assert 0 <= ranked[0]["score"] <= 1


def test_empty_resume_list_returns_empty():
    assert rank_resumes([], "Python developer") == []


def test_empty_job_description_rejected():
    with pytest.raises(ValueError):
        rank_resumes([{"filename": "a.txt", "text": "Python"}], " ")
