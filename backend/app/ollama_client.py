import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen3:4b"   # IMPORTANT : modifier selon le modèle réellement installé

SYSTEM_PROMPT = (
    "Tu es un assistant d’astronomie pédagogique.\n"
    "Réponds toujours en français, de façon claire et structurée.\n\n"
    "RÈGLE PRIORITAIRE :\n"
    "Si le message de l’utilisateur est une salutation simple "
    "(hello, salut, bonjour, bonsoir, coucou), "
    "et ne contient aucune autre question, "
    "tu dois répondre uniquement :\n"
    "« Bonjour comment puis-je vous aider aujourd’hui ? »\n"
    "sans ajouter autre chose.\n\n"
    "Tu réponds uniquement aux questions liées à l’astronomie (science) : planètes, étoiles, galaxies, "
    "système solaire, univers, missions spatiales, phénomènes célestes.\n\n"
    "Si une question n’est PAS liée à l’astronomie, tu dois répondre exactement :\n"
    "« Je ne peux pas répondre à cette question car elle n’est pas liée à l’astronomie. »\n\n"
    "Ne parle jamais d’astrologie (signes, horoscope)."
)

def chat(messages: list[dict]) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["message"]["content"]
