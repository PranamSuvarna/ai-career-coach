import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("Training started...")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "career_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

df = pd.read_csv(DATA_PATH)

X = df["text"]
y = df["label"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

with open(MODEL_PATH, "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Model trained and saved!")