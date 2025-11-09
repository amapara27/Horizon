from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

from polymarket_fetcher import (
    get_tech_events_service,
    get_trending_events_service,
    get_sports_events_service
)
from claude_service import (
    analyze_news_sentiment,
    generate_final_summary
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

@app.get("/api/event/{event_id}/analysis")
def get_event_analysis(event_id: str):
    """
    Primary analysis endpoint that orchestrates all data gathering and AI analysis.
    
    Returns:
        {
            "event_data": {...},
            "outcomes": [
                {
                    "outcome_name": "...",
                    "current_price": 45.2,
                    "liquidity": {...},
                    "news": {...},
                    "final_summary": "..."
                },
                ...
            ]
        }
    """
    try:
        # 1. Get event data
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        event_data = response.json()
        
        # 2. Get market depth (factual liquidity scores)
        depth_data = get_event_market_depth(event_id)
        
        if not depth_data:
            raise HTTPException(status_code=404, detail="No market data found for this event")
        
        # 3. Loop through top 3 outcomes
        outcomes_analysis = []
        event_title = event_data.get('title', '')
        
        for depth in depth_data[:3]:  # Top 3 by liquidity
            outcome_name = depth['outcome']
            market_question = depth['market_question']
            
            print(f"Analyzing outcome: {outcome_name}")
            
            # a. Get news for this specific outcome
            news_data = get_event_news(event_title, market_question, outcome_name, max_results=10)
            
            # b. Analyze news sentiment
            news_sentiment = analyze_news_sentiment(
                news_data.get('articles', []),
                outcome_name,
                market_question
            )
            
            # c. Generate final summary
            final_summary = generate_final_summary(
                outcome_name,
                news_sentiment,
                depth
            )
            
            # Bundle everything together
            outcomes_analysis.append({
                "outcome_name": outcome_name,
                "current_price": depth['current_price'],
                "liquidity": {
                    "amount": depth['liquidity'],
                    "score": depth['liquidity_score'],
                    "level": depth['liquidity_level'],
                    "reasoning": depth['reasoning']
                },
                "news": {
                    "score": news_sentiment.get('score', 0),
                    "reasoning": news_sentiment.get('reasoning', 'No analysis available'),
                    "articles_count": len(news_data.get('articles', [])),
                    "articles": news_data.get('articles', [])[:5],  # Include top 5 articles
                    "query_used": news_data.get('query_used', '')
                },
                "final_summary": final_summary.get('summary', 'No summary available')
            })
        
        return {
            "event_data": {
                "id": event_data.get('id'),
                "slug": event_data.get('slug', ''),
                "title": event_data.get('title'),
                "description": event_data.get('description'),
                "volume": event_data.get('volumeNum', 0),
                "liquidity": event_data.get('liquidityNum', 0)
            },
            "outcomes": outcomes_analysis
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching event data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing event: {str(e)}")
