from app.ollama_client import chat, SYSTEM_PROMPT

def handle_message(message: str, conversation_id: str, memory_store: dict) -> str:
    # Récupérer l'historique (mémoire en RAM)
    history = memory_store.get(conversation_id, [])
    history.append({"role": "user", "content": message})

    # Construire les messages pour Ollama
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history[-12:]

    try:
        reply = chat(messages)
    except Exception:
        reply = "Erreur: je n’arrive pas à joindre Ollama. Vérifie que le service tourne et que le modèle est installé."

    # Sauvegarder la réponse dans l'historique
    history.append({"role": "assistant", "content": reply})
    memory_store[conversation_id] = history

    return reply
