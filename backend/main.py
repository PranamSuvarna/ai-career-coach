from fastapi import FastAPI

from routes.analyze import router as analyze_router
from routes.chat import router as chat_router
from routes.resume import router as resume_router

app = FastAPI()

# Routes
app.include_router(analyze_router)
app.include_router(chat_router)
app.include_router(resume_router)

# Home Route
@app.get("/")
def home():

    return {
        "message": "AI Career Coach Backend Running"
    }