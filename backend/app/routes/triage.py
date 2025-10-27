from fastapi import APIRouter, Body
from app.services.ai_chat_service import analyze_patient_input

router = APIRouter(prefix="/triage", tags=["Triage"])

@router.post("/")
def process_triage(payload: dict = Body(...)):
    """
    Receives patient symptom input and returns AI-based analysis + severity score.
    """
    user_input = payload.get("symptoms", "")
    ai_result = analyze_patient_input(user_input)

    return {
        "received": payload,
        "ai_analysis": ai_result
    }
