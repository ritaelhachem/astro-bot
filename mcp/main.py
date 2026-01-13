from fastapi import FastAPI
from pydantic import BaseModel

# Import des tools
from tools.scraping import scrape_latest_news
from tools.calculate import calculate
from tools.summarize import summarize
from tools.search import search_keyword
from tools.scrape_rss import scrape_astronomy_news
from tools.astronomy_image_search import astronomy_image_search
from tools.celestial_position import celestial_position




app = FastAPI(title="MCP Server")

# -----------------------------
# MODELES DE REQUÊTES
# -----------------------------

class ScrapeRequest(BaseModel):
    url: str

class CalculateRequest(BaseModel):
    expression: str

class SummarizeRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    text: str
    keyword: str

class AstronomyNewsRequest(BaseModel):
    keyword: str | None = None
    limit: int = 20

class AstronomyImageRequest(BaseModel):
    keyword: str
    limit: int = 10

class CelestialPositionRequest(BaseModel):
    object_name: str




# -----------------------------
# ROUTES DES TOOLS
# -----------------------------

@app.post("/tools/scrape")
def scrape_tool(request: ScrapeRequest):
    data = scrape_latest_news(request.url)
    return {
        "tool": "scrape",
        "input": request.url,
        "output": data
    }

@app.post("/tools/calculate")
def calculate_tool(request: CalculateRequest):
    data = calculate(request.expression)
    return {
        "tool": "calculate",
        "input": request.expression,
        "output": data
    }

@app.post("/tools/summarize")
def summarize_tool(request: SummarizeRequest):
    data = summarize(request.text)
    return {
        "tool": "summarize",
        "input": request.text,
        "output": data
    }

@app.post("/tools/search")
def search_tool(request: SearchRequest):
    data = search_keyword(request.text, request.keyword)
    return {
        "tool": "search",
        "input": {"text": request.text, "keyword": request.keyword},
        "output": data
    }

@app.post("/tools/scrape_astronomy_news")
def scrape_astronomy_news_tool(request: AstronomyNewsRequest):
    data = scrape_astronomy_news(keyword=request.keyword, limit=request.limit)
    return {
        "tool": "scrape_astronomy_news",
        "input": {"keyword": request.keyword, "limit": request.limit},
        "output": data
    }

@app.post("/tools/astronomy_image_search")
def astronomy_image_search_tool(request: AstronomyImageRequest):
    data = astronomy_image_search(keyword=request.keyword, limit=request.limit)
    return {
        "tool": "astronomy_image_search",
        "input": {"keyword": request.keyword, "limit": request.limit},
        "output": data
    }

@app.post("/tools/celestial_position")
def celestial_position_tool(request: CelestialPositionRequest):
    data = celestial_position(request.object_name)
    return {
        "tool": "celestial_position",
        "input": {"object_name": request.object_name},
        "output": data
    }
