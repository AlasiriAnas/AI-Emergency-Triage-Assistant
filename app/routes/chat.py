from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.deps import get_current_user
from app.services.groq_chat_service import chat_with_ai

router = APIRouter(prefix="/chat", tags=["Conversational AI"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(payload: ChatRequest, user = Depends(get_current_user)):
    reply = await chat_with_ai(payload.message)

    return {
        "user": user.email,
        "message": payload.message,
        "reply": reply
    }
