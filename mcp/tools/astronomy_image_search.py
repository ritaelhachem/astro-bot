import requests

NASA_IMAGE_API = "https://images-api.nasa.gov/search"

# Mots-clésà privilégier
SCIENCE_KEYWORDS = [
    "planet", "surface", "galaxy", "nebula", "supernova", "star",
    "astronomy", "spacecraft", "mission", "rover", "telescope",
    "observatory", "cosmos", "solar", "lunar", "orbit", "nasa"
]

# Mots-clés à exclure pour éviter les results non pertinents
BANNED_KEYWORDS = [
    "poster", "kids", "child", "children", "drawing", "illustration",
    "art", "cartoon", "logo", "education", "school", "toy", "fun",
    "comic", "animation", "sketch"
]

def is_scientific(item):
    """Détermine si une image est scientifique en analysant ses métadonnées."""
    title = item.get("title", "").lower()
    desc = item.get("description", "").lower()

    # si un mot interdit apparaît on rejette
    for bad in BANNED_KEYWORDS:
        if bad in title or bad in desc:
            return False

    # si un mot scientifique apparaît on garde
    for good in SCIENCE_KEYWORDS:
        if good in title or good in desc:
            return True

    # Sinon : on rejette
    return False


def astronomy_image_search(keyword: str, limit: int = 10):

    params = {
        "q": keyword,
        "media_type": "image"
    }

    try:
        response = requests.get(NASA_IMAGE_API, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Erreur API NASA: {e}")
        return []

    data = response.json()
    items = data.get("collection", {}).get("items", [])

    results = []

    for item in items:
        metadata = item.get("data", [{}])[0]
        links = item.get("links", [{}])

        # Filtrage scientifique
        if not is_scientific(metadata):
            continue

        results.append({
            "title": metadata.get("title", "No title"),
            "description": metadata.get("description", "No description"),
            "date_created": metadata.get("date_created", ""),
            "image_url": links[0].get("href", "") if links else "",
            "source": "NASA Image API (filtered)"
        })

        if len(results) >= limit:
            break

    return results
