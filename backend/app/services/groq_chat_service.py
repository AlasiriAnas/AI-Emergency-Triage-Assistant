from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

async def chat_with_ai(message: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a medical triage assistant. "
                    "Ask structured medical questions to assess symptoms. "
                    "Never provide medical diagnosis or treatment. "
                    "If serious symptoms appear, respond: "
                    "'This may be an emergency — please seek medical care immediately.' "
                    "Goal: guide and collect medical context safely."
                ),
            },
            {"role": "user", "content": message},
        ],
        max_tokens=300,
        temperature=0.7,
    )

    # ✅ Correct way to return content
    return response.choices[0].message.content
