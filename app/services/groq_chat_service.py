# backend/app/services/groq_chat_service.py

from typing import List, Dict, Literal
from groq import Groq
from anyio import to_thread
from app.core.config import settings

# Latest Groq model
GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are an emergency triage assistant INSIDE the hospital ER.

The patient is already in the emergency room.
❌ NEVER tell them to go to the ER or call emergency services.
✅ Ask a maximum of one short question per reply.
✅ Keep a warm, calm tone.
✅ Focus only on gathering symptoms, not diagnosing.
✅ Avoid repeating questions already asked.
✅ If severe symptoms are clear, wrap up politely and reassure:
   "Thank you. A clinician will review you shortly."

Your messages must be short and only text (no JSON here).
"""

Role = Literal["user", "assistant"]

def _convert_history_to_openai_messages(history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    asked_questions = set()

    for turn in history:
        role = turn.get("role", "patient")
        content = (turn.get("content") or "").strip()
        if not content:
            continue

        if role == "patient":
            messages.append({"role": "user", "content": content})
        else:
            if content not in asked_questions:
                messages.append({"role": "assistant", "content": content})
                asked_questions.add(content)

    return messages

def _chat_sync(history: List[Dict[str, str]]) -> str:
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    client = Groq(api_key=settings.GROQ_API_KEY)
    messages = _convert_history_to_openai_messages(history)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=200,
    )

    reply = (response.choices[0].message.content or "").strip()

    if reply.lower().startswith("as an ai"):
        reply = reply.split("\n", 1)[-1].strip()

    return reply

async def chat_with_ai(history: List[Dict[str, str]]) -> str:
    return await to_thread.run_sync(_chat_sync, history)
