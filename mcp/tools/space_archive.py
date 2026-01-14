import requests
from bs4 import BeautifulSoup

def scrape_space_archive(year: int, keyword: str | None = None, limit: int = 20):

    url = f"https://www.space.com/news/archive/{year}"

    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as e:
        print(f"Erreur lors du chargement des archives Space.com : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    items = soup.select("li.archive-item")

    for item in items:
        title_tag = item.find("a")
        date_tag = item.find("time")

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = "https://www.space.com" + title_tag.get("href", "")
        date = date_tag.get_text(strip=True) if date_tag else "Unknown date"

        articles.append({
            "title": title,
            "date": date,
            "url": link,
            "source": "Space.com"
        })

    # Filtrage par mot clé
    if keyword:
        keyword = keyword.lower()
        articles = [
            a for a in articles
            if keyword in a["title"].lower()
        ]

    return articles[:limit]
