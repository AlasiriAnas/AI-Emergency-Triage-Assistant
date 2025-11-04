from fastapi import APIRouter, Body, Depends
from app.services.ai_chat_service import analyze_patient_input
from app.core.database import SessionLocal
from app.models.triage_record import TriageRecord
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/triage", tags=["Triage"])

@router.post("/")
def process_triage(payload: dict = Body(...), current_user: User = Depends(get_current_user)):
    """
    Receives patient symptoms, runs AI scoring, saves to DB with user link, returns severity.
    """
    patient_id = payload.get("patient_id", "")
    symptoms = payload.get("symptoms", "")

    ai_result = analyze_patient_input(symptoms)

    severity_label = ai_result["severity"]["label"]
    priority = ai_result["severity"]["priority"]
    detected_symptoms = ", ".join(ai_result["detected_symptoms"])

    db = SessionLocal()
    record = TriageRecord(
        user_id=current_user.id,   # ✅ link triage to logged-in patient
        patient_id=patient_id,
        symptoms=symptoms,
        detected_symptoms=detected_symptoms,
        severity_label=severity_label,
        priority=priority
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()

    return {
        "status": "saved",
        "patient": current_user.email,   # optional clarity
        "received": payload,
        "ai_analysis": ai_result
    }
