import requests
from datetime import datetime

API_URL = "https://api.spaceflightnewsapi.net/v4/articles/"

def search_astronomy_archive(year: int, keyword: str | None = None, limit: int = 20):

    start_date = f"{year}-01-01T00:00:00Z"
    end_date = f"{year}-12-31T23:59:59Z"

    params = {
        "published_at_gte": start_date,
        "published_at_lte": end_date,
        "limit": limit
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Erreur de l'API archives: {e}")
        return []

    data = response.json()
    articles = data.get("results", [])

    if keyword:
        keyword = keyword.lower()
        articles = [
            a for a in articles
            if keyword in a.get("title", "").lower()
            or keyword in a.get("summary", "").lower()
        ]

    results = []
    for a in articles[:limit]:
        results.append({
            "title": a.get("title"),
            "summary": a.get("summary"),
            "url": a.get("url"),
            "image_url": a.get("image_url"),
            "published_at": a.get("published_at"),
            "source": a.get("news_site")
        })

    return results
