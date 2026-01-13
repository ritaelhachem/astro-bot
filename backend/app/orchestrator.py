# from app.ollama_client import chat, SYSTEM_PROMPT
# from app.memory import get_history, append_message

# def handle_message(message: str, conversation_id: str) -> str:
#     append_message(conversation_id, "user", message)

#     history = get_history(conversation_id)
#     messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history[-12:]

#     try:
#         reply = chat(messages)
#     except Exception as e:
#         print("Ollama error:", e)
#         reply = (
#             "Erreur: je n’arrive pas à joindre Ollama. "
#             "Vérifie que le service tourne et que le modèle est installé."
#         )

#     append_message(conversation_id, "assistant", reply)

#     return reply

import json
import requests
from app.ollama_client import chat, SYSTEM_PROMPT
from app.memory import get_history, append_message

MCP_BASE_URL = "http://127.0.0.1:8001"

TOOLS_DESC = """
Tu as accès aux tools suivants via MCP (à utiliser si nécessaire) :

1) scrape(url: string)
- But: récupérer les derniers titres d'articles d'une page web (scraping HTML).
- Quand l'utiliser: quand l'utilisateur demande des "news", "actus", "dernières actualités", "tendances" ou une info récente.
- Endpoint: POST /tools/scrape  body: {"url":"..."}

2) summarize(text: string)
- But: produire un résumé court d'un texte.
- Quand l'utiliser: quand tu as un texte long (scrapé) à résumer.
- Endpoint: POST /tools/summarize  body: {"text":"..."}

3) search(text: string, keyword: string)
- But: compter la présence d'un mot-clé dans un texte.
- Quand l'utiliser: pour repérer rapidement si un sujet est présent dans un contenu scrapé.
- Endpoint: POST /tools/search  body: {"text":"...", "keyword":"..."}

4) calculate(expression: string)
- But: faire un calcul simple.
- Quand l'utiliser: conversions/estimations utiles en astronomie (unités, proportions), pas pour faire un bot de maths.
- Endpoint: POST /tools/calculate  body: {"expression":"..."}
""".strip()

AGENT_RULES = """
RÈGLES:
- Tu réponds en français.
- Tu es spécialisé en astronomie (science). Si la question est hors astronomie et ne nécessite pas d'outil utile au contexte,
  tu réponds exactement : « Je ne peux pas répondre à cette question car elle n’est pas liée à l’astronomie. »
- Si la question demande des actualités récentes, tu dois utiliser scrape (avec une URL) puis éventuellement summarize.
- Format obligatoire de sortie (JSON uniquement, sans texte autour) :

A) Réponse directe :
{"action":"final","answer":"..."}

B) Appel tool :
{"action":"tool","tool_name":"scrape|summarize|search|calculate","args":{...}}

Ne renvoie jamais autre chose que ce JSON.
""".strip()

def call_mcp(tool_name: str, args: dict) -> dict:
    endpoint_map = {
        "scrape": "/tools/scrape",
        "summarize": "/tools/summarize",
        "search": "/tools/search",
        "calculate": "/tools/calculate",
    }
    if tool_name not in endpoint_map:
        raise ValueError(f"Unknown tool: {tool_name}")

    url = MCP_BASE_URL + endpoint_map[tool_name]
    r = requests.post(url, json=args, timeout=25)
    r.raise_for_status()
    return r.json()

def safe_json(text: str) -> dict:
    text = (text or "").strip()
    if text.startswith("{") and text.endswith("}"):
        return json.loads(text)

    # fallback: extraire le premier bloc {...}
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start:end+1])

    raise ValueError("No JSON found")

def handle_message(message: str, conversation_id: str) -> str:
    append_message(conversation_id, "user", message)
    history = get_history(conversation_id)

    # 1) Demander au LLM s'il doit appeler un tool
    decision_messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + TOOLS_DESC + "\n\n" + AGENT_RULES}
    ] + history[-12:]

    decision_raw = chat(decision_messages)

    try:
        decision = safe_json(decision_raw)
    except Exception:
        # fallback simple par mots-clés si le modèle ne respecte pas le JSON
        lowered = message.lower()
        if any(k in lowered for k in ["news", "actu", "actualités", "tendance", "dernières"]):
            decision = {"action": "tool", "tool_name": "scrape", "args": {"url": "https://www.nasa.gov/rss/dyn/breaking_news.rss"}}
        else:
            decision = {"action": "final", "answer": "Je ne peux pas traiter cette demande pour le moment."}

    if decision.get("action") == "final":
        reply = decision.get("answer", "")
        append_message(conversation_id, "assistant", reply)
        return reply

    # 2) Appel tool demandé
    if decision.get("action") == "tool":
        tool_name = decision.get("tool_name")
        args = decision.get("args", {}) or {}

        try:
            tool_result = call_mcp(tool_name, args)
        except Exception as e:
            reply = f"Erreur tool MCP ({tool_name}): {e}"
            append_message(conversation_id, "assistant", reply)
            return reply

        # 3) Redonner le résultat au LLM pour rédiger la réponse finale
        final_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question utilisateur: {message}"},
            {"role": "user", "content": f"Résultat du tool {tool_name} (JSON):\n{json.dumps(tool_result, ensure_ascii=False)}"},
            {"role": "user", "content": "Rédige une réponse finale claire en français. Si c'est hors astronomie, refuse avec la phrase imposée."}
        ]

        reply = chat(final_messages)
        append_message(conversation_id, "assistant", reply)
        return reply

    # 4) Cas non prévu
    reply = "Je ne peux pas répondre pour le moment."
    append_message(conversation_id, "assistant", reply)
    return reply
