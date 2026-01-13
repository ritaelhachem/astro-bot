import requests

NASA_IMAGE_API = "https://images-api.nasa.gov/search"

def astronomy_image_search(keyword: str, limit: int = 10):
    """
    Recherche des images astronomiques via l'API NASA.
    Retourne une liste d'images avec titre, description et URL.
    """

    params = {
        "q": keyword,
        "media_type": "image"
    }

    try:
        response = requests.get(NASA_IMAGE_API, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Erreur API NASA: {e}")
        return []

    data = response.json()

    items = data.get("collection", {}).get("items", [])
    results = []

    for item in items[:limit]:
        metadata = item.get("data", [{}])[0]
        links = item.get("links", [{}])

        results.append({
            "title": metadata.get("title", "No title"),
            "description": metadata.get("description", "No description"),
            "date_created": metadata.get("date_created", ""),
            "image_url": links[0].get("href", "") if links else "",
            "source": "NASA Image API"
        })

    return results
