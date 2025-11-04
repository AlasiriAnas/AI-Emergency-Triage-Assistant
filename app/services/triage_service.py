# backend/app/services/triage_service.py
import json
from groq import Groq
from app.core.config import settings
from app.core.database import SessionLocal

client = Groq(api_key=settings.GROQ_API_KEY)

def save_triage_record(user_id, data):
    from app.models.triage_record import TriageRecord
    db = SessionLocal()
    try:
        record = TriageRecord(
            patient_id=user_id,
            symptoms=", ".join(data.get("symptoms", [])),
            duration=data.get("duration", ""),
            severity_label=data.get("severity", "Low"),
            risk_factors=", ".join(data.get("risk_factors", [])),
            ticket=data.get("ticket", ""),
            wait_time=data.get("wait_time", ""),
            status="waiting"
        )
        db.add(record)
        db.commit()
    finally:
        db.close()

async def analyze_triage(messages, user_id: int):
    system_prompt = """
You are an AI triage assistant inside the ER.
Never tell patient to go to ER—they're already there.

Rules:
- Ask max 2–3 short follow-ups
- Then classify severity + ticket
- Respond JSON only
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(messages)}
        ],
        temperature=0.2
    )

    raw = res.choices[0].message.content.strip()
    if "{" in raw:
        raw = raw[raw.index("{"): raw.rindex("}")+1]

    try:
        data = json.loads(raw)
    except:
        return {"final": False}

    # 💡 Multi-turn logic — if model isn't final, keep chatting
    if not data.get("final"):
        return {"final": False}

    severity = data.get("severity", "Low")
    ticket_prefix = {"Critical":"P","High":"A","Medium":"B","Low":"C"}.get(severity,"C")
    ticket = f"{ticket_prefix}{1000+user_id}"
    data["ticket"] = ticket

    wait = {"Critical":"Immediate","High":"5–15 minutes","Medium":"20–40 minutes","Low":"45–90 minutes"}
    data["wait_time"] = wait.get(severity,"45–90 minutes")

    save_triage_record(user_id, data)
    return data
