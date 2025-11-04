# backend/app/routes/triage.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.deps import get_current_user
from app.services.triage_service import analyze_triage

router = APIRouter(prefix="/triage", tags=["Triage"])

class TriageRequest(BaseModel):
    messages: List[str]

@router.post("/process")
async def triage_process(req: TriageRequest, user = Depends(get_current_user)):
    try:
        result = await analyze_triage(req.messages, user.id)

        if not result.get("final"):
            return {"continue": True}  # not done

        return {
            "ticket": {
                "number": result["ticket"],
                "estimatedWait": result["wait_time"]
            },
            "summary": {
                "symptoms": result.get("symptoms", []),
                "duration": result.get("duration", ""),
                "severity": result.get("severity", ""),
                "risk_factors": result.get("risk_factors", [])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage failed: {e}")
