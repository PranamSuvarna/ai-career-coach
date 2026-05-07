# backend/services/skill_extractor.py

import re
import spacy
from collections import Counter

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ---------------- MASTER SKILL DATABASE ----------------
SKILLS_DB = {

    # Programming
    "python", "java", "c", "c++", "javascript", "typescript",
    "go", "rust", "php", "ruby", "swift", "kotlin",

    # Data Science
    "machine learning", "deep learning", "data science",
    "artificial intelligence", "nlp", "computer vision",
    "pandas", "numpy", "matplotlib", "seaborn",
    "scikit-learn", "tensorflow", "keras", "pytorch",
    "xgboost", "lightgbm",

    # Web
    "html", "css", "react", "nextjs", "nodejs",
    "fastapi", "flask", "django", "streamlit",

    # Database
    "sql", "mysql", "postgresql", "mongodb",
    "firebase", "sqlite",

    # Cloud
    "aws", "azure", "gcp", "docker", "kubernetes",

    # Tools
    "git", "github", "linux", "power bi", "tableau",

    # Soft Skills
    "communication", "leadership", "problem solving",
    "teamwork", "critical thinking"
}

# ---------------- CLEAN TEXT ----------------
def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text

# ---------------- EXTRACT SKILLS ----------------
def extract_skills(text):

    text = clean_text(text)

    doc = nlp(text)

    found_skills = []

    # -------- Match Exact Skills --------
    for skill in SKILLS_DB:

        if skill in text:
            found_skills.append(skill)

    # -------- NER + NOUN PHRASES --------
    noun_phrases = [chunk.text.lower() for chunk in doc.noun_chunks]

    for phrase in noun_phrases:

        if phrase in SKILLS_DB:
            found_skills.append(phrase)

    # -------- Remove Duplicates --------
    found_skills = list(set(found_skills))

    # -------- Skill Frequency --------
    skill_counts = Counter(found_skills)

    # -------- Categorize Skills --------
    categorized_skills = categorize_skills(found_skills)

    return {
        "all_skills": found_skills,
        "skill_frequency": dict(skill_counts),
        "categorized_skills": categorized_skills
    }

# ---------------- SKILL CATEGORIES ----------------
def categorize_skills(skills):

    categories = {
        "Programming": [],
        "Data Science": [],
        "Web Development": [],
        "Database": [],
        "Cloud & DevOps": [],
        "Tools": [],
        "Soft Skills": []
    }

    for skill in skills:

        # Programming
        if skill in [
            "python", "java", "c", "c++",
            "javascript", "typescript",
            "go", "rust", "php", "ruby",
            "swift", "kotlin"
        ]:
            categories["Programming"].append(skill)

        # Data Science
        elif skill in [
            "machine learning", "deep learning",
            "data science", "artificial intelligence",
            "nlp", "computer vision",
            "pandas", "numpy", "matplotlib",
            "seaborn", "tensorflow",
            "keras", "pytorch",
            "scikit-learn"
        ]:
            categories["Data Science"].append(skill)

        # Web
        elif skill in [
            "html", "css", "react",
            "nextjs", "nodejs",
            "fastapi", "flask",
            "django", "streamlit"
        ]:
            categories["Web Development"].append(skill)

        # Database
        elif skill in [
            "sql", "mysql",
            "postgresql", "mongodb",
            "firebase", "sqlite"
        ]:
            categories["Database"].append(skill)

        # Cloud
        elif skill in [
            "aws", "azure",
            "gcp", "docker",
            "kubernetes"
        ]:
            categories["Cloud & DevOps"].append(skill)

        # Tools
        elif skill in [
            "git", "github",
            "linux", "power bi",
            "tableau"
        ]:
            categories["Tools"].append(skill)

        # Soft Skills
        elif skill in [
            "communication",
            "leadership",
            "problem solving",
            "teamwork",
            "critical thinking"
        ]:
            categories["Soft Skills"].append(skill)

    return categories

# ---------------- RESUME SCORE ----------------
def calculate_resume_score(skills):

    total_possible_skills = len(SKILLS_DB)

    detected_skills = len(skills)

    score = int(
        (detected_skills / total_possible_skills) * 100
    )

    if score > 100:
        score = 100

    return score

# ---------------- MISSING SKILLS ----------------
def missing_skills(skills, target_role="data scientist"):

    role_skills = {

        "data scientist": [
            "python",
            "machine learning",
            "pandas",
            "numpy",
            "sql",
            "tensorflow",
            "deep learning"
        ],

        "frontend developer": [
            "html",
            "css",
            "javascript",
            "react",
            "typescript"
        ],

        "backend developer": [
            "python",
            "fastapi",
            "flask",
            "sql",
            "docker"
        ]
    }

    required = role_skills.get(
        target_role.lower(),
        []
    )

    missing = []

    for skill in required:

        if skill not in skills:
            missing.append(skill)

    return missing

# ---------------- TEST ----------------
if __name__ == "__main__":

    sample_text = """
    I am a Data Science student skilled in Python,
    Machine Learning, Deep Learning, SQL,
    FastAPI, Streamlit and TensorFlow.
    """

    result = extract_skills(sample_text)

    print("\\n===== EXTRACTED SKILLS =====")
    print(result)

    score = calculate_resume_score(
        result["all_skills"]
    )

    print("\\nResume Score:", score)

    missing = missing_skills(
        result["all_skills"],
        "data scientist"
    )

    print("\\nMissing Skills:", missing)