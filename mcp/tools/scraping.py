import requests
from bs4 import BeautifulSoup

def scrape_latest_news(url: str):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    # On prend les premiers titres <h2> de la page
    for item in soup.find_all("h2")[:5]:
        title_text = item.get_text(strip=True)
        if title_text:
            articles.append({
                "title": title_text,
            })

    return {"articles": articles}
