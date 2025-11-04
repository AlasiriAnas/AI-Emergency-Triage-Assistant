# backend/app/routes/chat.py
from typing import List, Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.core.deps import get_current_user
from app.models.user import User
from app.services.groq_chat_service import chat_with_ai

router = APIRouter(prefix="/chat", tags=["Conversational AI"])

UIRole = Literal["patient", "ai"]

class ChatTurn(BaseModel):
    role: UIRole = Field(..., description="patient or ai")
    content: str = Field(..., min_length=1)

class ChatRequest(BaseModel):
    history: List[ChatTurn] = Field(default_factory=list)

class ChatResponse(BaseModel):
    user: str
    reply: str

@router.post("/", response_model=ChatResponse)
async def chat(payload: ChatRequest, current_user: User = Depends(get_current_user)):
    has_patient_msg = any(t.role == "patient" and t.content.strip() for t in payload.history)
    if not has_patient_msg:
        raise HTTPException(status_code=400, detail="No patient message found in history.")

    try:
        history_dicts = [t.model_dump() for t in payload.history]
        reply = await chat_with_ai(history_dicts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat service error: {e}")

    return ChatResponse(user=current_user.email, reply=reply)
