import requests
import json
from fastapi import HTTPException # Import HTTPException

# --- Configuration ---
GAMMA_API = "https://gamma-api.polymarket.com"
CRYPTO_TAG_ID = '21'

# --- Main Helper Function ---
def fetch_from_polymarket(endpoint: str, params: dict):
    """
    A helper to fetch data from Polymarket and raise FastAPI errors.
    """
    try:
        response = requests.get(f"{GAMMA_API}{endpoint}", params=params)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        # If the Polymarket API fails, forward the error
        status_code = e.response.status_code if e.response else 500
        raise HTTPException(status_code=status_code, detail=f"Error from Polymarket API: {e}")
    except Exception as e:
        # For any other unexpected error
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# --- Service Functions (Now they return data) ---

def get_new_events_service(limit=5):
    """
    Fetches the most recently created active events.
    """
    params = {
        'closed': 'false',
        'order': 'id',
        'ascending': 'false',
        'limit': limit
    }
    # We return the data instead of printing
    events = fetch_from_polymarket('/events', params)
    return events

def get_trending_events_service(limit=20):
    """
    Fetches the most active events by 24-hour volume.
    """
    params = {
        'closed': 'false',
        'order': 'volume24hr', 
        'ascending': 'false',    
        'limit': limit
    }
    # We return the data instead of printing
    events = fetch_from_polymarket('/events', params)
    return events


def get_crypto_events_service(limit=5): # Renamed for clarity
    """
    Fetches the newest events in the 'Crypto' category.
    """
    params = {
        'closed': 'false',
        'tag_id': CRYPTO_TAG_ID, # Filter by category
        'order': 'id',           # Get newest in this category
        'ascending': 'false',
        'limit': limit
    }
    # We return the data instead of printing
    events = fetch_from_polymarket('/events', params)
    return events