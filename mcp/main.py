from fastapi import FastAPI
from pydantic import BaseModel

# Import des tools
from tools.scrape_rss import scrape_astronomy_news
from tools.astronomy_image_search import astronomy_image_search
from tools.celestial_position import celestial_position
from tools.astronomy_archive import search_astronomy_archive
from tools.space_archive import scrape_space_archive






app = FastAPI(title="MCP Server")


class AstronomyNewsRequest(BaseModel):
    keyword: str | None = None
    limit: int = 20

class AstronomyImageRequest(BaseModel):
    keyword: str
    limit: int = 10

class CelestialPositionRequest(BaseModel):
    object_name: str

class AstronomyArchiveRequest(BaseModel):
    year: int
    keyword: str | None = None
    limit: int = 20

class SpaceArchiveRequest(BaseModel):
    year: int
    keyword: str | None = None
    limit: int = 20





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

@app.post("/tools/search_astronomy_archive")
def search_astronomy_archive_tool(request: AstronomyArchiveRequest):
    data = search_astronomy_archive(
        year=request.year,
        keyword=request.keyword,
        limit=request.limit
    )
    return {
        "tool": "search_astronomy_archive",
        "input": {
            "year": request.year,
            "keyword": request.keyword,
            "limit": request.limit
        },
        "output": data
    }

@app.post("/tools/scrape_space_archive")
def scrape_space_archive_tool(request: SpaceArchiveRequest):
    data = scrape_space_archive(
        year=request.year,
        keyword=request.keyword,
        limit=request.limit
    )
    return {
        "tool": "scrape_space_archive",
        "input": {
            "year": request.year,
            "keyword": request.keyword,
            "limit": request.limit
        },
        "output": data
    }
