from fastapi import APIRouter
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@router.post("/chat/")
def chat_ai(data: dict):

    message = data.get("message", "")
    history = data.get("history", [])

    system_prompt = """
You are an expert AI Career Coach.
Help users with:
- Career guidance
- Skill improvement
- Resume advice
- Interview preparation
Be concise, practical, and structured.
"""

    messages = [{"role": "system", "content": system_prompt}]

    # add last 10 messages
    for msg in history[-10:]:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})

    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}