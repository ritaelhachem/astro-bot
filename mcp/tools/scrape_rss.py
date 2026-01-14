import urllib.request
import xml.etree.ElementTree as ET
import html
import re

SOURCES = {
    "NASA": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "ESA": "https://www.esa.int/rssfeed/Our_Activities/Space_Science",
    "Space.com": "https://www.space.com/feeds/all",
    "UniverseToday": "https://universetoday.com/feed/",
    "Phys.org": "https://phys.org/rss-feed/space-news/"
}

def fetch_rss(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read()

def clean_html(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def parse_rss(xml_data, source):
    root = ET.fromstring(xml_data)
    articles = []

    for item in root.findall(".//item"):
        title = clean_html(item.findtext("title", ""))
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        description = clean_html(item.findtext("description", ""))

        articles.append({
            "title": title,
            "date": pub_date,
            "source": source,
            "link": link,
            "summary": description
        })

    return articles

def scrape_astronomy_news(keyword=None, limit=50):
    print(">>> TOOL RSS CHARGÉ")
    all_articles = []

    for source, url in SOURCES.items():
        print(f"Scraping {source}...")
        try:
            xml_data = fetch_rss(url)
            articles = parse_rss(xml_data, source)
            all_articles.extend(articles)
        except Exception as e:
            print(f"Erreur avec {source}: {e}")

    print(f"Nombre total d'articles trouvés : {len(all_articles)}")

    if keyword:
        keyword = keyword.lower()
        all_articles = [
            a for a in all_articles
            if keyword in a["title"].lower() or keyword in a["summary"].lower()
        ]

    return all_articles[:limit]

