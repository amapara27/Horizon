from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

from polymarket_fetcher import (
    get_tech_events_service,
    get_trending_events_service,
    get_sports_events_service
)
from claude_service import (
    analyze_event_sentiment,
    analyze_market_depth,
    generate_combined_sentiment,
    analyze_news_sentiment
)
from market_depth_service import get_event_market_depth
from news_service import get_event_news

# --- App Setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/api/tech-events")
def get_tech_events():
    return get_tech_events_service(limit=20)

@app.get("/api/trending-events")
def get_trending_events():
    return get_trending_events_service(limit=20)

@app.get("/api/sports-events")
def get_sports_events():
    return get_sports_events_service(limit=20)

@app.get("/api/event/{event_id}")
def get_event_details(event_id: str):
    try:
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching event: {str(e)}")

@app.get("/api/event/{event_id}/market-depth")
def get_event_market_depth_endpoint(event_id: str):
    """Get aggregated market depth data for a specific event"""
    depth_data = get_event_market_depth(event_id)
    return depth_data

@app.get("/api/event/{event_id}/news")
def get_event_news_endpoint(event_id: str):
    """Get news articles related to a specific event"""
    try:
        # Fetch event data to get the title
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        event_data = response.json()
        
        # Get news based on event title
        news = get_event_news(event_data.get('title', ''), max_results=10)
        return news
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.get("/api/event/{event_id}/news-sentiment")
def get_news_sentiment_endpoint(event_id: str):
    """Get AI sentiment analysis for news articles"""
    try:
        # Fetch event data to get the title
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        event_data = response.json()
        
        # Get news articles
        news = get_event_news(event_data.get('title', ''), max_results=10)
        
        # Analyze news sentiment
        sentiment = analyze_news_sentiment(news.get('articles', []), event_data)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing news sentiment: {str(e)}")

@app.get("/api/event/{event_id}/market-depth-sentiment")
def get_market_depth_sentiment(event_id: str):
    """Get AI analysis of market depth and liquidity"""
    try:
        # Fetch event and market depth data
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        event_data = response.json()
        
        depth_data = get_event_market_depth(event_id)
        
        # Analyze market depth sentiment
        sentiment = analyze_market_depth(depth_data, event_data)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing market depth: {str(e)}")

@app.get("/api/event/{event_id}/combined-sentiment")
def get_combined_sentiment(event_id: str):
    """Get combined AI sentiment analysis"""
    try:
        # Fetch event data
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        event_data = response.json()
        
        # Get news articles
        news = get_event_news(event_data.get('title', ''), max_results=10)
        news_sentiment = analyze_news_sentiment(news.get('articles', []), event_data)
        
        # Get market depth analysis
        depth_data = get_event_market_depth(event_id)
        depth_sentiment = analyze_market_depth(depth_data, event_data)
        
        # Generate combined sentiment
        combined = generate_combined_sentiment(news_sentiment, depth_sentiment, event_data)
        return combined
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating combined sentiment: {str(e)}")