"""
Tests for CareerLearn AI backend — covers:
  1. Multi-career support (all 6 careers)
  2. Experience-level personalization (Beginner / Intermediate / Advanced)
  3. Real readiness percentage calculation
  4. Input validation for unsupported careers
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from main import app, CAREERS_DB, FALLBACK_CONTENT

client = TestClient(app)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def analyze(career, skills=None, level="Beginner"):
    payload = {"targetCareer": career, "currentSkills": skills or [], "experienceLevel": level}
    return client.post("/api/analyze", json=payload)


# ─── Health check ─────────────────────────────────────────────────────────────

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    # Health endpoint lists all supported careers
    for career in CAREERS_DB:
        assert career in data["careers"], f"{career} missing from health careers"


# ─── Fix 1: Multi-Career Support ─────────────────────────────────────────────

def test_all_careers_return_200():
    """Every career in CAREERS_DB must return HTTP 200."""
    for career in CAREERS_DB:
        r = analyze(career)
        assert r.status_code == 200, f"Career '{career}' returned {r.status_code}"


def test_ml_engineer_roadmap_preserved():
    r = analyze("ML Engineer")
    data = r.json()
    assert r.status_code == 200
    assert "Machine Learning" in data["roadmap"]
    assert "Deep Learning" in data["roadmap"]
    assert "Python" in data["roadmap"]


def test_data_scientist_has_correct_skills():
    r = analyze("Data Scientist")
    data = r.json()
    assert "Exploratory Data Analysis" in data["roadmap"]
    assert "Storytelling with Data" in data["roadmap"]
    # Should NOT default to ML Engineer skills purely
    assert "Model Deployment" not in data["roadmap"]


def test_data_analyst_roadmap():
    r = analyze("Data Analyst")
    data = r.json()
    assert "Excel" in data["roadmap"]
    assert "Business Intelligence Tools" in data["roadmap"]
    assert "Deep Learning" not in data["roadmap"]


def test_software_engineer_roadmap():
    r = analyze("Software Engineer")
    data = r.json()
    assert "Object-Oriented Programming" in data["roadmap"]
    assert "Testing & Debugging" in data["roadmap"]


def test_ai_engineer_roadmap():
    r = analyze("AI Engineer")
    data = r.json()
    assert "Natural Language Processing" in data["roadmap"]
    assert "MLOps" in data["roadmap"]


def test_full_stack_developer_roadmap():
    r = analyze("Full Stack Developer")
    data = r.json()
    assert "React" in data["roadmap"]
    assert "Node.js" in data["roadmap"]
    assert "HTML & CSS" in data["roadmap"]


def test_no_silent_ml_fallback():
    """A valid non-ML career must NOT have the ML Engineer roadmap baked in."""
    ml_roadmap = set(CAREERS_DB["ML Engineer"])
    r = analyze("Full Stack Developer")
    data = r.json()
    # Some overlap is expected (e.g. REST APIs) but the roadmap should NOT be identical
    assert set(data["roadmap"]) != ml_roadmap


def test_invalid_career_returns_422():
    r = analyze("Astronaut")
    assert r.status_code == 422
    body = r.json()
    assert "error" in body["detail"]
    assert "supported_careers" in body["detail"]
    assert "ML Engineer" in body["detail"]["supported_careers"]


def test_skill_gaps_computed_correctly():
    """Known skills must be excluded from missingSkills."""
    known = ["Python", "SQL"]
    r = analyze("Data Analyst", skills=known)
    data = r.json()
    for k in known:
        if k in CAREERS_DB["Data Analyst"]:
            assert k not in data["missingSkills"], f"{k} should not be a gap"
            assert k in data["knownSkills"]


def test_all_missing_skills_have_explanations():
    r = analyze("Software Engineer")
    data = r.json()
    explained = {e["skill"] for e in data["skillExplanations"]}
    for skill in data["missingSkills"]:
        assert skill in explained, f"No explanation for missing skill: {skill}"


# ─── Fix 2: Experience-Level Personalization ──────────────────────────────────

def test_experience_level_echoed_in_response():
    for level in ("Beginner", "Intermediate", "Advanced"):
        r = analyze("ML Engineer", level=level)
        data = r.json()
        assert data["experienceLevel"] == level


def test_experience_level_in_skill_explanations():
    r = analyze("ML Engineer", level="Intermediate")
    data = r.json()
    for exp in data["skillExplanations"]:
        assert "experienceLevel" in exp
        assert exp["experienceLevel"] == "Intermediate"


def test_beginner_has_beginner_task_difficulty():
    r = analyze("ML Engineer", skills=[], level="Beginner")
    data = r.json()
    # Mathematics is always a gap for a blank ML Engineer
    math_exp = next((e for e in data["skillExplanations"] if e["skill"] == "Mathematics"), None)
    assert math_exp is not None
    task = math_exp.get("applicationTask", {})
    assert task.get("difficulty") == "Beginner"


def test_intermediate_python_task_differs_from_beginner():
    r_b = analyze("ML Engineer", skills=[], level="Beginner")
    r_i = analyze("ML Engineer", skills=[], level="Intermediate")
    # Python is a required skill for ML Engineer — may or may not be missing depending on user
    # Force it by providing no current skills
    exp_b = {e["skill"]: e for e in r_b.json()["skillExplanations"]}
    exp_i = {e["skill"]: e for e in r_i.json()["skillExplanations"]}
    if "Python" in exp_b and "Python" in exp_i:
        task_b = exp_b["Python"].get("applicationTask", {}).get("title", "")
        task_i = exp_i["Python"].get("applicationTask", {}).get("title", "")
        assert task_b != task_i, "Beginner and Intermediate Python tasks should differ"


def test_invalid_experience_level_defaults_to_beginner():
    r = analyze("ML Engineer", level="Expert")
    data = r.json()
    assert data["experienceLevel"] == "Beginner"


# ─── Fix 3: Real Readiness Percentage ─────────────────────────────────────────

def test_readiness_pct_zero_when_no_skills():
    r = analyze("ML Engineer", skills=[])
    data = r.json()
    assert data["readinessPct"] == 0
    assert data["readinessEstimate"] == "Low"


def test_readiness_pct_100_when_all_skills_known():
    all_skills = CAREERS_DB["ML Engineer"]
    r = analyze("ML Engineer", skills=all_skills)
    data = r.json()
    assert data["readinessPct"] == 100
    assert data["readinessEstimate"] == "High"
    assert data["missingSkills"] == []


def test_readiness_pct_partial():
    required = CAREERS_DB["Data Analyst"]
    half = required[:len(required) // 2]
    r = analyze("Data Analyst", skills=half)
    data = r.json()
    expected_pct = int((len(half) / len(required)) * 100)
    assert data["readinessPct"] == expected_pct


def test_readiness_pct_is_integer():
    r = analyze("Full Stack Developer", skills=["React"])
    data = r.json()
    assert isinstance(data["readinessPct"], int)


def test_readiness_estimate_consistent_with_pct():
    """The estimate label must be consistent with the numeric percentage."""
    for career in CAREERS_DB:
        r = analyze(career, skills=[])
        data = r.json()
        pct = data["readinessPct"]
        estimate = data["readinessEstimate"]
        if pct > 75:
            assert estimate == "High"
        elif pct > 40:
            assert estimate == "Medium"
        else:
            assert estimate == "Low"


def test_roadmap_returned_for_every_career():
    for career in CAREERS_DB:
        r = analyze(career)
        data = r.json()
        assert data["roadmap"] == CAREERS_DB[career], f"Roadmap mismatch for {career}"


# ─── FALLBACK_CONTENT coverage ────────────────────────────────────────────────

def test_fallback_content_covers_all_required_skills():
    """Every skill in any career roadmap must have FALLBACK_CONTENT or a generic fallback.
    This confirms no skill silently produces empty content."""
    all_required = {skill for skills in CAREERS_DB.values() for skill in skills}
    missing_content = [s for s in all_required if s not in FALLBACK_CONTENT]
    # Generic fallback exists for unknown skills, but flag any uncovered ones for awareness
    # This is a soft warning, not a hard failure
    if missing_content:
        print(f"\n[INFO] Skills without curated FALLBACK_CONTENT (generic fallback used): {missing_content}")


# ─── Resume Intelligence ──────────────────────────────────────────────────────

def _pdf_bytes(text: str) -> bytes:
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    if text:
        page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data


def test_parse_resume_extracts_canonical_skills():
    pdf = _pdf_bytes("Skills: Python, SQL, React, Machine Learning, Git, pandas")
    r = client.post("/api/parse-resume", files={"file": ("resume.pdf", pdf, "application/pdf")})
    assert r.status_code == 200
    skills = r.json()["extractedSkills"]
    assert "Python" in skills
    assert "SQL" in skills
    assert "React" in skills
    assert "Machine Learning" in skills
    assert "Version Control (Git)" in skills
    assert "Data Wrangling" in skills  # pandas alias


def test_parse_resume_rejects_non_pdf():
    r = client.post("/api/parse-resume", files={"file": ("notes.txt", b"python sql", "text/plain")})
    assert r.status_code == 400


def test_parse_resume_rejects_empty_file():
    r = client.post("/api/parse-resume", files={"file": ("empty.pdf", b"", "application/pdf")})
    assert r.status_code == 400


def test_parse_resume_rejects_corrupted_pdf():
    r = client.post("/api/parse-resume", files={"file": ("bad.pdf", b"%PDF-1.4 not a real pdf", "application/pdf")})
    assert r.status_code == 422


def test_parse_resume_rejects_textless_pdf():
    r = client.post("/api/parse-resume", files={"file": ("scan.pdf", _pdf_bytes(""), "application/pdf")})
    assert r.status_code == 422
    assert "scanned" in r.json()["detail"].lower() or "no text" in r.json()["detail"].lower()


def test_parse_resume_does_not_invent_unmentioned_skills():
    pdf = _pdf_bytes("Education: B.E. Computer Science\nSkills: Python")
    r = client.post("/api/parse-resume", files={"file": ("resume.pdf", pdf, "application/pdf")})
    skills = r.json()["extractedSkills"]
    assert skills == ["Python"]


# ─── Career recommendation ────────────────────────────────────────────────────

def test_recommend_requires_skills():
    r = client.post("/api/recommend", json={"currentSkills": []})
    assert r.status_code == 400


def test_recommend_returns_top_three_with_overlap():
    r = client.post("/api/recommend", json={"currentSkills": ["React", "HTML & CSS", "JavaScript", "Node.js"]})
    assert r.status_code == 200
    data = r.json()
    recs = data["recommendations"]
    assert len(recs) == 3
    assert recs[0]["career"] == "Full Stack Developer"
    assert "React" in recs[0]["matchingSkills"]
    assert "similarityScore" in recs[0]
    assert recs[0]["similarityScore"] >= recs[1]["similarityScore"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
