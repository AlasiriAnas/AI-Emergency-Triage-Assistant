from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.ai_chat_service import analyze_patient_input

router = APIRouter(prefix="/triage", tags=["Triage"])

# ------------------- Pydantic Models -------------------

class TriageRequest(BaseModel):
    patient_id: Optional[str] = Field(None, example="P12345")
    symptoms: str = Field(..., example="I feel chest pain and shortness of breath")

class SeverityResponse(BaseModel):
    priority: int
    label: str
    reasoning: str

class AIAnalysis(BaseModel):
    detected_symptoms: List[str]
    severity: SeverityResponse

class TriageResponse(BaseModel):
    received: TriageRequest
    ai_analysis: AIAnalysis


# ------------------- Route -------------------

@router.post("/", response_model=TriageResponse)
def process_triage(payload: TriageRequest):
    """
    Receives patient symptom input and returns AI-based analysis + severity score.
    """
    ai_result = analyze_patient_input(payload.symptoms)
    return {
        "received": payload,
        "ai_analysis": ai_result
    }
