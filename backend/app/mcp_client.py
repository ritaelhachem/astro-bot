import requests

MCP_URL = "http://127.0.0.1:9000"

def scrape_astronomy_news(keyword: str | None = None, limit: int = 10) -> dict:
    """
    Appelle le tool MCP /tools/scrape_astronomy_news pour récupérer des actualités astronomiques récentes

    :param keyword: mot-clé optionnel (ex: "mars", "jupiter", etc...)
    :param limit: nombre max d'articles à récupérer
    :return: JSON retourné par le MCP
    """
    payload = {
        "keyword": keyword,
        "limit": limit
    }

    response = requests.post(
        f"{MCP_URL}/tools/scrape_astronomy_news",
        json=payload,
        timeout=20
    )

    response.raise_for_status()
    return response.json()

def search_astronomy_archive(year: int, keyword: str | None = None, limit: int = 10) -> dict:
    """
    Appelle le tool MCP /tools/search_astronomy_archive pour récupérer des articles d'archives (par année).
    """
    payload = {
        "year": year,
        "keyword": keyword,
        "limit": limit
    }

    response = requests.post(
        f"{MCP_URL}/tools/search_astronomy_archive",
        json=payload,
        timeout=20
    )

    response.raise_for_status()
    return response.json()
