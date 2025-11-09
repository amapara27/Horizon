from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---
# 1. IMPORT YOUR SERVICE FUNCTIONS
# ---
# (You named your file 'polymarket_fetcher.py' in the last error)
# (I named the functions with '_service' in my example)
from polymarket_fetcher import (
    get_tech_events_service,
    get_trending_events_service,
    get_sports_events_service
)

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
    import requests
    try:
        response = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error fetching event: {str(e)}")