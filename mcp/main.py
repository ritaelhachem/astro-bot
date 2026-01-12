from fastapi import FastAPI
from pydantic import BaseModel

# Import des tools
from tools.scraping import scrape_latest_news
from tools.calculate import calculate
from tools.summarize import summarize
from tools.search import search_keyword

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
