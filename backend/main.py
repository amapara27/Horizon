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
    analyze_smart_wallets,
    generate_combined_sentiment
)
from wallet_service import get_event_smart_wallets

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

@app.get("/api/event/{event_id}/smart-wallets")
def get_event_wallets(event_id: str):
    """Get smart wallet positions for a specific event"""
    wallets = get_event_smart_wallets(event_id)
    return wallets

@app.get("/api/event/{event_id}/sentiment")
def get_event_sentiment(event_id: str):
    """Get AI sentiment analysis for event"""
    try:
        # Fetch event data
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        event_data = response.json()
        
        # Analyze sentiment
        sentiment = analyze_event_sentiment(event_data)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

@app.get("/api/event/{event_id}/wallet-sentiment")
def get_wallet_sentiment(event_id: str):
    """Get AI analysis of smart wallet activity"""
    try:
        # Fetch event and wallet data
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        event_data = response.json()
        
        wallets = get_event_smart_wallets(event_id)
        
        # Analyze wallet sentiment
        sentiment = analyze_smart_wallets(wallets, event_data)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing wallets: {str(e)}")

@app.get("/api/event/{event_id}/combined-sentiment")
def get_combined_sentiment(event_id: str):
    """Get combined AI sentiment analysis"""
    try:
        # Fetch event data
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        event_data = response.json()
        
        # Get both analyses
        event_sentiment = analyze_event_sentiment(event_data)
        
        wallets = get_event_smart_wallets(event_id)
        wallet_sentiment = analyze_smart_wallets(wallets, event_data)
        
        # Generate combined sentiment
        combined = generate_combined_sentiment(event_sentiment, wallet_sentiment, event_data)
        return combined
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating combined sentiment: {str(e)}")