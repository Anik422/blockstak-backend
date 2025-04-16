from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import requests


from app.auth import get_current_user
from app import config
from app.database import get_db
from app.models import News, Source
from app import config


router = APIRouter(prefix="/news", tags=["news"])


@router.get("/", summary="Fetch all news with pagination")
def get_news(page: int = 1, page_size: int = 10, user: str = Depends(get_current_user)):
    url = f"https://newsapi.org/v2/everything?q=latest&page={page}&pageSize={page_size}&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching news")
    news_data = response.json()
    return {"news": news_data.get("articles", []), "totalResults": news_data.get("totalResults", 0)}


@router.post("/save-latest")
def save_latest_news(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch news from API")
    
    articles = response.json().get("articles", [])[:3]
    
    save_titles = []
    for item in articles:
        source_data = item.get("source", {})
        source_id = source_data.get("id") or f"unknown-{item['title'][:10]}"
        source_name = source_data.get("name") or "Unknown Source"
        
        # Check if source already exists
        source = db.query(Source).filter(Source.id == source_id).first()
        if not source:
            print(f"Creating new source: {source_name}")
            source = Source(id=source_id, name=source_name)
            db.add(source)
        
        # Create News
        news_item = News(
            title=item["title"],
            description=item.get("description"),
            url=item["url"],
            published_at=datetime.fromisoformat(item["publishedAt"].replace("Z", "+00:00")),
            author=item.get("author"),
            url_to_image=item.get("urlToImage"),
            content=item.get("content"),
            source_id=source.id
        )
        db.add(news_item)
        save_titles.append(item["title"])
    db.commit()
    return {"message": "Latest news saved successfully", "titles": save_titles}
    