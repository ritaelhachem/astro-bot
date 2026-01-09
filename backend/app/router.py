from fastapi import APIRouter
from pydantic import BaseModel
from app.orchestrator import handle_message

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

class ChatResponse(BaseModel):
    reply: str
    conversation_id: str

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = handle_message(req.message, req.conversation_id)
    return {"reply": reply, "conversation_id": req.conversation_id}
