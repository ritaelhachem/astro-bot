import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:3b"

SYSTEM_PROMPT = (
    "Tu es un assistant d’astronomie pédagogique. "
    "Réponds toujours en français, de façon claire et structurée."
)

def chat(messages: list[dict]) -> str:
    """
    messages: [{"role":"system|user|assistant", "content":"..."}]
    retourne: texte réponse
    """
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["message"]["content"]
