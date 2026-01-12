def summarize(text: str):
    sentences = text.split(".")
    summary = ". ".join(sentences[:2]).strip()

    return {
        "summary": summary if summary else "Résumé impossible (texte trop court)."
    }
