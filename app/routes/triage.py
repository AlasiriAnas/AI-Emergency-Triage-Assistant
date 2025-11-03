from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.routes.auth import get_current_user
from app.services.triage_service import analyze_triage_conversation

router = APIRouter(prefix="/triage", tags=["Triage"])

# ----- Request & Response Models -----

class TriageRequest(BaseModel):
    messages: List[str]

class TriageSummary(BaseModel):
    symptoms: List[str]
    duration: str
    severity: str
    riskFactors: List[str]

class TriageResponse(BaseModel):
    summary: TriageSummary


# ----- Endpoints -----

@router.post("/summary", response_model=TriageResponse)
async def generate_summary(payload: TriageRequest, user=Depends(get_current_user)):
    """
    Takes patient chat history (text messages only)
    and returns triage classification via Groq AI.
    """

    try:
        data = analyze_triage_conversation(payload.messages)

        return {
            "summary": {
                "symptoms": data.get("symptoms", []),
                "duration": data.get("duration", ""),
                "severity": data.get("severity", "Low"),
                "riskFactors": data.get("risk_factors", [])
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage analysis failed: {str(e)}")


# Optional placeholder if you later add manual triage logging
@router.get("/ping")
async def ping_check(user=Depends(get_current_user)):
    return {"status": "Triage API alive"}
