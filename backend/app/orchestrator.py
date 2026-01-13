from app.ollama_client import chat, SYSTEM_PROMPT
from app.memory import get_history, append_message
from app.mcp_client import scrape_astronomy_news

def needs_news_tool(user_message: str) -> bool:
    """
    Déclenche le tool 'scrape_astronomy_news' si la question semble demander
    des infos récentes/actuelles (news, dernières, cette semaine, etc.).
    """
    msg = user_message.lower()
    triggers = [
        "actu", "actualité", "news", "récent", "récentes", "dernière", "dernières",
        "cette semaine", "aujourd", "dernier", "nouvelle", "nouvelles", "découverte",
        "lancement", "mission", "annonce"
    ]
    return any(t in msg for t in triggers)

def extract_keyword(user_message: str) -> str | None:
    """
    Extraction très simple d'un mot-clé utile pour filtrer les news RSS.
    Si rien trouvé, on renvoie None (le tool renverra un flux global).
    """
    msg = user_message.lower()
    candidates = [
        "mars", "jupiter", "saturne", "uranus", "neptune", "venus", "mercure",
        "soleil", "lune", "comète", "astéroïde", "asteroide", "exoplanète", "exoplanete",
        "télescope", "telescope", "jwst", "hubble", "spacex", "nasa", "esa"
    ]
    for c in candidates:
        if c in msg:
            return c
    return None

def handle_message(message: str, conversation_id: str) -> str:
    append_message(conversation_id, "user", message)
    history = get_history(conversation_id)

    tool_payload_text = None
    if needs_news_tool(message):
        keyword = extract_keyword(message)
        try:
            tool_resp = scrape_astronomy_news(keyword=keyword, limit=8)
            items = tool_resp.get("output", [])

            tool_payload_text = "\n".join(
                f"- [{a.get('source')}] {a.get('title')} ({a.get('date')})\n"
                f"  Lien: {a.get('link')}\n"
                f"  Résumé: {a.get('summary')}"
                for a in items[:8]
            )

        except Exception as e:
            print("MCP error:", e)
            tool_payload_text = None

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history[-12:]

    if tool_payload_text:
        messages.append({
            "role": "system",
            "content": (
                "Données récentes issues d'un tool MCP (actualités astronomiques).\n"
                "Utilise ces données si la question porte sur l'actualité et cite les sources.\n\n"
                f"{tool_payload_text}"
            )
        })

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
