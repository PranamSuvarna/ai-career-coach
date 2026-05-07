from fastapi import APIRouter, UploadFile, File
import pdfplumber

from services.skill_extractor import (
    extract_skills,
    calculate_resume_score,
    missing_skills
)

router = APIRouter()

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text

# ---------------- RESUME ANALYSIS ----------------
@router.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):

    try:

        # Extract text
        text = extract_text_from_pdf(file.file)

        # Extract skills
        result = extract_skills(text)

        skills = result["all_skills"]

        # Resume score
        score = calculate_resume_score(skills)

        # Missing skills
        missing = missing_skills(
            skills,
            "data scientist"
        )

        # Career prediction
        if "machine learning" in skills:
            career = "Data Scientist"

        elif "react" in skills:
            career = "Frontend Developer"

        elif "fastapi" in skills:
            career = "Backend Developer"

        else:
            career = "Software Engineer"

        return {

            "career": career,

            "confidence": score,

            "skills": skills,

            "roadmap": [
                "Build Projects",
                "Learn Advanced Concepts",
                "Practice Interview Questions",
                "Deploy Applications"
            ],

            "advice": {
                "strengths": skills,

                "weaknesses": missing,

                "recommendations": [
                    f"Learn {skill}" for skill in missing
                ]
            }
        }

    except Exception as e:

        return {
            "error": str(e)
        }