from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---
# 1. IMPORT YOUR SERVICE FUNCTIONS
# ---
# (You named your file 'polymarket_fetcher.py' in the last error)
# (I named the functions with '_service' in my example)
from polymarket_fetcher import (
    get_new_events_service,
    get_trending_events_service,
    get_crypto_events_service 
    # Make sure these are the function names in your fetcher file!
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

@app.get("/api/new-events")
def get_new_events():
    # WRONG: return get_new_events()
    # RIGHT: Call the function you imported
    return get_new_events_service()

@app.get("/api/trending-events")
def get_trending_events():
    # WRONG: return get_trending_events()
    # RIGHT: Call the function you imported
    return get_trending_events_service(limit=20)

@app.get("/api/crypto-events")
def get_crypto_events():
    # WRONG: return get_crypto_events()
    # RIGHT: Call the function you imported
    return get_crypto_events_service()