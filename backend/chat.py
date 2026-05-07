from fastapi import APIRouter
from transformers import pipeline

router = APIRouter()

# Load free AI model
chatbot = pipeline(
   "text2text-generation",
    model="google/flan-t5-base"
)

@router.post("/chat/")
def chat_ai(data: dict):

    try:
        message = data.get("message", "")

        if not message:
            return {
                "reply": "Please enter a message"
            }

        prompt = f"""
        You are an AI Career Coach.

        User: {message}

        AI:
        """

        result = chatbot(
            prompt,
            max_length=120,
            num_return_sequences=1
        )

        reply = result[0]["generated_text"]

        return {
            "reply": reply
        }

    except Exception as e:

        return {
            "reply": f"Error: {str(e)}"
        }