from fastapi import FastAPI
from pydantic import BaseModel
from tools.scrape_rss import scrape_astronomy_news
from tools.astronomy_archive import search_astronomy_archive
from tools.position import celestial_position


app = FastAPI(title="MCP Server")


class AstronomyNewsRequest(BaseModel):
    keyword: str | None = None
    limit: int = 20

class AstronomyArchiveRequest(BaseModel):
    year: int
    keyword: str | None = None
    limit: int = 20

class PositionRequest(BaseModel):
    object_name: str
    location: str
    iso_time: str | None = None


@app.post("/tools/scrape_astronomy_news")
def scrape_astronomy_news_tool(request: AstronomyNewsRequest):
    data = scrape_astronomy_news(keyword=request.keyword, limit=request.limit)
    return {
        "tool": "scrape_astronomy_news",
        "input": {"keyword": request.keyword, "limit": request.limit},
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

@app.post("/tools/position")
def position_tool(req: PositionRequest):
    data = celestial_position(
        object_name=req.object_name,
        location=req.location,
        iso_time=req.iso_time
    )
    return {
        "tool": "position",
        "input": req.model_dump(),
        "output": data
    }

