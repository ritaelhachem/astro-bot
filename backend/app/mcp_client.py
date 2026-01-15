import requests

MCP_URL = "http://127.0.0.1:9000"

def scrape_astronomy_news(keyword: str | None = None, limit: int = 10) -> dict:
   
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



def get_celestial_position(object_name: str, location: str, iso_time: str | None = None) -> dict:
   
    payload = {
        "object_name": object_name,
        "location": location,
        "iso_time": iso_time
    }

    response = requests.post(
        f"{MCP_URL}/tools/position",
        json=payload,
        timeout=25
    )
    response.raise_for_status()
    return response.json()
