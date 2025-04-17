from fastapi import APIRouter, Depends, HTTPException, Query, status
import requests


from app.auth import get_current_user
from app import config


router = APIRouter(prefix="/headlines", tags=["Headlines"])  # Main router for headlines


@router.get("/country/{country_code}", summary="Fetch top headlines by country")
def get_top_headlines_by_country(
    country_code: str, user: str = Depends(get_current_user)
):
    """
    Fetch top headlines from the News API by country code.
    """
    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={config.NEWS_API_KEY}"
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


@router.get("/source/{source_id}", summary="Fetch top headlines by source")
def get_top_headlines_by_source(source_id: str, user: str = Depends(get_current_user)):
    """
    Fetch top headlines from the News API by source ID.
    """
    url = f"https://newsapi.org/v2/top-headlines?sources={source_id}&apiKey={config.NEWS_API_KEY}"
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


@router.get("/headlines/filter", summary="Fetch headlines by country and/or source")
def filter_headlines(
    country: str = Query(None, description="Country code like 'us', 'gb', 'bd'"),
    source: str = Query(None, description="Source ID like 'bbc-news'"),
    user: str = Depends(get_current_user),
):
    """
    Fetch top headlines filtered by optional country code and/or source ID.
    """
    url = "https://newsapi.org/v2/top-headlines?"
    if source:
        url += f"sources={source}&"
    if country:
        url += f"country={country}&"
    url += f"apiKey={config.NEWS_API_KEY}"

    response = requests.get(url)
    news_data = response.json()
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=news_data.get("message", "Error fetching news"),
        )

    return {
        "status": "success",
        "news": news_data.get("articles", []),
        "totalResults": news_data.get("totalResults", 0),
    }
