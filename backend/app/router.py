from fastapi import APIRouter
from pydantic import BaseModel
from app.orchestrator import handle_message

router = APIRouter()

# Mémoire globale (RAM)
MEMORY_STORE: dict[str, list[dict]] = {}

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

@router.post("/chat")
def chat(req: ChatRequest):
    reply = handle_message(
        req.message,
        req.conversation_id,
        MEMORY_STORE
    )

    return {
        "reply": reply,
        "conversation_id": req.conversation_id
    }
