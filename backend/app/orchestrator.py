from app.ollama_client import chat, SYSTEM_PROMPT
from app.memory import get_history, append_message

def handle_message(message: str, conversation_id: str) -> str:
    append_message(conversation_id, "user", message)

    history = get_history(conversation_id)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history[-12:]

    try:
        reply = chat(messages)
    except Exception as e:
        print("Ollama error:", e)
        reply = (
            "Erreur: je n’arrive pas à joindre Ollama. "
            "Vérifie que le service tourne et que le modèle est installé."
        )

    append_message(conversation_id, "assistant", reply)

    return reply
