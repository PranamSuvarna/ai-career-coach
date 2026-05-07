import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

def analyze_text(text):
    try:
        with open(MODEL_PATH, "rb") as f:
            model, vectorizer = pickle.load(f)

        X = vectorizer.transform([text])
        prediction = model.predict(X)[0]
        confidence = max(model.predict_proba(X)[0])

        return {
            "career": prediction,
            "confidence": round(confidence * 100, 2)
        }

    except Exception as e:
        return {"error": str(e)}