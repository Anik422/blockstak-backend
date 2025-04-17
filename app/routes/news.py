from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from slugify import slugify
import requests


from app.auth import get_current_user
from app.database import get_db
from app.models import News, Source
from app import config
from app.routes import headlines


router = APIRouter(prefix="/news", tags=["News"])  # Main router for news
router.include_router(headlines.router)  # Include the headlines router


@router.get("/", summary="Fetch all news with pagination")
def get_news(page: int = 1, page_size: int = 10, user: str = Depends(get_current_user)):
    """
    Fetch all news with pagination.
    """
    url = f"https://newsapi.org/v2/everything?q=latest&page={page}&pageSize={page_size}&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching news",
        )
    news_data = response.json()
    return {
        "status": "success",
        "news": news_data.get("articles", []),
        "totalResults": news_data.get("totalResults", 0),
    }


@router.post("/save-latest")
def save_latest_news(
    db: Session = Depends(get_db), user: str = Depends(get_current_user)
):
    """
    Fetch and save the latest news articles from the News API.
    """
    url = (
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={config.NEWS_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch news from API",
        )

    articles = response.json().get("articles", [])

    save_titles = []
    already_saved = []
    for item in articles:
        source_data = item.get("source", {})
        if source_data != {} and source_data.get("name"):
            source_id = source_data.get("id") or slugify(source_data["name"])
            source_name = source_data.get("name")

            # Check if source already exists
            source = db.query(Source).filter(Source.id == source_id).first()
            if not source:
                source = Source(id=source_id, name=source_name)
                db.add(source)

            # Check if news article already exists
            # Use slugify to create a unique slug for the news article
            slug = slugify(item["title"])
            new = db.query(News).filter(News.slug == slug).first()
            if not new:
                # Create a new news article
                news_item = News(
                    title=item["title"],
                    description=item.get("description"),
                    url=item["url"],
                    published_at=datetime.fromisoformat(
                        item["publishedAt"].replace("Z", "+00:00")
                    ),
                    author=item.get("author"),
                    url_to_image=item.get("urlToImage"),
                    content=item.get("content"),
                    source_id=source.id,
                    slug=slug,
                )
                db.add(news_item)
                save_titles.append(item["title"])
            else:
                already_saved.append(item["title"])
            if len(save_titles) >= 3:
                break
    db.commit()
    return {
        "status": "success",
        "message": f"Saved {len(save_titles)} news articles",
        "already_saved": already_saved,
        "saved_titles": save_titles,
    }
