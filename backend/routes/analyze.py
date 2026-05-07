from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# -----------------------
# Request model
# -----------------------
class InputText(BaseModel):
    text: str


# -----------------------
# Skill DB
# -----------------------
SKILL_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "data science", "pandas", "numpy", "sql", "flask",
    "django", "streamlit", "tensorflow", "pytorch",
    "html", "css", "javascript"
]


# -----------------------
# Extract skills
# -----------------------
def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILL_DB if skill in text]


# -----------------------
# Career prediction
# -----------------------
def predict_career(skills):
    if "machine learning" in skills:
        return "AI/ML Engineer", 90
    if "data science" in skills:
        return "Data Scientist", 88
    if "flask" in skills:
        return "Backend Developer", 85
    if "html" in skills:
        return "Frontend Developer", 80
    return "Software Developer", 70


# -----------------------
# API ROUTE
# -----------------------
@router.post("/analyze")
def analyze(input: InputText):
    skills = extract_skills(input.text)
    career, confidence = predict_career(skills)

    return {
        "career": career,
        "confidence": confidence,
        "skills": skills,
        "roadmap": ["Keep learning", "Build projects", "Practice DSA"],
        "advice": f"Focus on {career} projects and consistency."
    }