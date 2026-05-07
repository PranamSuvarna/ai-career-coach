def generate_roadmap(career):
    roadmap = {
        "Data Scientist": [
            "Learn Python",
            "Learn Pandas & NumPy",
            "Study Machine Learning",
            "Work on projects",
            "Learn Deep Learning"
        ],
        "Web Developer": [
            "Learn HTML, CSS",
            "Learn JavaScript",
            "Learn React",
            "Build projects",
            "Learn backend (Node/FastAPI)"
        ],
        "Software Engineer": [
            "Learn DSA",
            "Learn System Design",
            "Practice coding",
            "Build projects",
            "Prepare for interviews"
        ]
    }

    return roadmap.get(career, ["Explore basics", "Build projects"])