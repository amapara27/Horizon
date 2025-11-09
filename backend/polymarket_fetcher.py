import requests
import json

GAMMA_API = "https://gamma-api.polymarket.com"
SPORTS_TAG_ID = '10'  # Sports category

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

def get_tech_events_service(limit=20):
    """
    Fetches tech-related events using Tech, AI, and Big Tech tags.
    """
    print("--- 💻 Tech Events ---")
    params = {
        'closed': 'false',
        'order': 'volume24hr',
        'ascending': 'false',
        'limit': 100
    }
    
    # Tech tag IDs: Tech (1401), AI (439), Big Tech (101999)
    tech_tag_ids = ['1401', '439', '101999']
    
    try:
        response = requests.get(f"{GAMMA_API}/events", params=params)
        response.raise_for_status()
        all_events = response.json()
        
        # Filter for events with tech tags
        tech_events = []
        for event in all_events:
            event_tags = event.get('tags', [])
            # Check if event has any of the tech tag IDs
            if any(tag.get('id') in tech_tag_ids for tag in event_tags):
                tech_events.append(event)
                formatted = format_event_data(event)
                if formatted:
                    print(formatted)
                
                if len(tech_events) >= limit:
                    break
        
        return tech_events[:limit]
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tech events: {e}\n")
        return []

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


## Fetches sports events
def get_sports_events_service(limit=5):
    """
    Fetches the newest events in the Sports category.
    """
    print("--- '⚽ Sports' Events ---")
    
    params = {
       'closed': 'false',
        'tag_id': SPORTS_TAG_ID,
        'order': 'id',
        'ascending': 'false',
        'limit': limit
    }
    
    try:
        response = requests.get(f"{GAMMA_API}/events", params=params)
        response.raise_for_status()
        events = response.json()
        
        if not events:
            print("  No events found for this tag ID.\n")
            return []

        for event in events:
            formatted = format_event_data(event)
            if formatted:
                print(formatted)
        
        return events

    except requests.exceptions.RequestException as e:
        print(f"Error fetching sports events: {e}\n")
        return []
# --- Main Function to Run Dashboard ---

def get_dashboard_data():
    get_tech_events_service()
    print("---" * 15)
    get_trending_events_service()
    print("---" * 15)
    get_sports_events_service()

if __name__ == "__main__":
    get_dashboard_data()