# backend/app/services/groq_chat_service.py
from typing import List, Dict, Literal
from groq import Groq
from anyio import to_thread

from app.core.config import settings

# Groq model (fast, good quality). You can switch to a larger model later if needed.
GROQ_MODEL = "llama-3.1-8b-instant"

# System prompt tuned for emergency-triage style, concise questions, and memory of context.
SYSTEM_PROMPT = (
    "You are an emergency triage assistant. Your goals:\n"
    "1) Ask focused, minimal questions to quickly assess severity.\n"
    "2) Keep messages short (1–3 sentences) and easy to answer.\n"
    "3) Remember chat context; do NOT repeat previous questions.\n"
    "4) If signs suggest life-threatening issues (e.g., crushing chest pain, severe SOB, stroke signs), "
    "   advise immediate attention from a clinician.\n"
    "5) Do not give a diagnosis; collect details for triage.\n"
    "When possible, ask at most one follow-up question at a time."
)

# Type aliases for clarity
Role = Literal["user", "assistant"]


def _convert_history_to_openai_messages(history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Convert UI history to OpenAI-style messages.
    UI history is a list of dicts: { 'role': 'patient' | 'ai', 'content': '...' }
    We convert:
      - 'patient' -> role 'user'
      - 'ai'      -> role 'assistant'
    """
    messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history:
        role = turn.get("role", "patient")
        content = (turn.get("content") or "").strip()
        if not content:
            continue

        if role == "patient":
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "assistant", "content": content})

    return messages


def _chat_sync(history: List[Dict[str, str]]) -> str:
    """
    Synchronous call to Groq. Wrapped by to_thread.run_sync when called from async endpoints.
    """
    if not settings.GROQ_API_KEY:
        # Fail loudly if the key is missing
        raise RuntimeError("GROQ_API_KEY is not configured.")

    client = Groq(api_key=settings.GROQ_API_KEY)
    messages = _convert_history_to_openai_messages(history)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=300,
    )

    # Groq SDK returns objects; message content is a string
    return (response.choices[0].message.content or "").strip()


async def chat_with_ai(history: List[Dict[str, str]]) -> str:
    """
    Async wrapper that runs sync Groq client safely in a thread.
    """
    return await to_thread.run_sync(_chat_sync, history)
