from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def analyze_triage_conversation(messages: list[str]):
    prompt = f"""
You are an emergency triage AI. Goal: rapidly assess severity, NOT ask endless questions.

Rules:

1. ALWAYS remember the full conversation context
2. Ask a MAX of 1–2 short questions at a time
3. Stop once enough data is collected — then output severity
4. Focus on life-threat symptoms:
   - Chest pain
   - Breathing difficulty
   - Stroke symptoms
   - Severe trauma
   - Confusion / altered consciousness
   - Persistent vomiting / dehydration
   - Very high fever
5. Use plain language, short questions.
6. Respond empathetically.

At decision time output JSON:
{
  "severity": "Low | Medium | High | Critical",
  "reasons": [ "...", "..." ],
  "next_step": "Immediate care | Urgent nurse | Standard wait | Home care advice"
}

If you're mid-assessment, continue asking useful questions.
If enough info is known — output the JSON without asking more.

"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content

    import json
    try:
        data = json.loads(content)
    except:
        raise ValueError("AI returned invalid JSON: " + str(content))

    return data
