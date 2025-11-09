import requests
import json

GAMMA_API = "https://gamma-api.polymarket.com"
CRYPTO_TAG_ID = '21'

## Formats event data for display
def format_event_data(event):
    """
    A helper function to parse an event and its
    first market into a clean, readable string.
    """
    try:
        market = event['markets'][0]
        title = event.get('title', 'N/A')
        bid = market.get('bestBid', 'N/A')
        ask = market.get('bestAsk', 'N/A')
        
        # Get the first outcome name, e.g., "Yes" or "Up"
        outcomes = json.loads(market.get('outcomes', '[]'))
        outcome_name = outcomes[0] if outcomes else "Outcome 1"

        return f"  - {title}\n    ({outcome_name} Price: ${bid} / ${ask})\n"
        
    except (KeyError, IndexError):
        # Silently skip if the event has no markets
        return None

# Fetches newest events

def get_new_events_service(limit=5):
    """
    Fetches the most recently created active events.
    """
    print("--- 🚀 Newest Events ---")
    params = {
        'closed': 'false',
        'order': 'id',          # 'id' (or 'creation_date') is best for "new"
        'ascending': 'false',   # Newest first
        'limit': limit
    }
    
    try:
        response = requests.get(f"{GAMMA_API}/events", params=params)
        response.raise_for_status()
        events = response.json()
        
        for event in events:
            formatted = format_event_data(event)
            if formatted:
                print(formatted)
        
        return events  # Return the data
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching new events: {e}\n")
        return []  # Return empty list on error

## Fetches trending events by volume
def get_trending_events_service(limit=20):
    """
    Fetches the most active events by 24-hour volume.
    """
    print("--- 🔥 Trending Events (by Volume) ---")
    params = {
        'closed': 'false',
        'order': 'volume24hr', 
        'ascending': 'false',    
        'limit': limit
    }
    
    try:
        response = requests.get(f"{GAMMA_API}/events", params=params)
        response.raise_for_status()
        events = response.json()
        
        for event in events:
            formatted = format_event_data(event)
            if formatted:
                print(formatted)
        
        return events  # Return the data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending events: {e}\n")
        return []  # Return empty list on error


## Fetches crypto events
def get_crypto_events_service(limit=5):
    """
    Fetches the newest events in a specific category (e.g., "Politics").
    """
    print("--- 'Crypto' Events ---")
    
    # I've updated this to use '4' (Politics) which is a valid ID
    params = {
        'closed': 'false',
        'tag_id': CRYPTO_TAG_ID, # Filter by category
        'order': 'id',                  # Get newest in this category
        'ascending': 'false',
        'limit': limit
    }
    
    try:
        response = requests.get(f"{GAMMA_API}/events", params=params)
        response.raise_for_status()
        events = response.json()
        
        if not events:
            print("  No events found for this tag ID.\n")
            return []  # Return empty list

        for event in events:
            formatted = format_event_data(event)
            if formatted:
                print(formatted)
        
        return events  # Return the data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching breaking events: {e}\n")
        return []  # Return empty list on error

# --- Main Function to Run Dashboard ---

def get_dashboard_data():
    get_new_events_service()
    print("---" * 15) # Add a separator
    get_trending_events_service()
    print("---" * 15) # Add a separator
    get_crypto_events_service()

if __name__ == "__main__":
    get_dashboard_data()