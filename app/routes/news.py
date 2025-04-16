from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
import requests
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
