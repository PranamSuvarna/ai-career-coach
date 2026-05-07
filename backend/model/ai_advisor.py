def generate_advice(skills, career):
    advice = {}

    # 🔹 Skill gaps
    required_skills = {
        "Data Scientist": ["python", "machine learning", "pandas", "numpy"],
        "Web Developer": ["html", "css", "javascript", "react"],
        "Software Engineer": ["python", "dsa", "system design"]
    }

    missing = []
    for skill in required_skills.get(career, []):
        if skill not in skills:
            missing.append(skill)

    advice["missing_skills"] = missing

    # 🔹 Strengths
    advice["strengths"] = list(skills.keys()) if isinstance(skills, dict) else skills

    # 🔹 Suggestions
    advice["suggestions"] = [
        f"Improve {skill}" for skill in missing
    ]

    return advice