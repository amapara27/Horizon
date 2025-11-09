import requests
import json

GAMMA_API = "https://gamma-api.polymarket.com"

def calculate_liquidity_score(liquidity):
    """
    Calculate a 0-100 liquidity score based on total liquidity.
    This is a factual metric based on simple thresholds.
    
    Score ranges:
    - 0: No liquidity
    - 10: < $1,000
    - 30: < $10,000
    - 70: < $100,000
    - 95: >= $100,000
    """
    if liquidity == 0:
        return 0
    elif liquidity < 1000:
        return 10
    elif liquidity < 10000:
        return 30
    elif liquidity < 100000:
        return 70
    else:
        return 95

def get_liquidity_level(score):
    """
    Convert liquidity score to a human-readable level.
    """
    if score == 0:
        return "No Liquidity"
    elif score <= 10:
        return "Very Thin"
    elif score <= 30:
        return "Thin"
    elif score <= 70:
        return "Good"
    else:
        return "Excellent"

def get_liquidity_reasoning(liquidity, score):
    """
    Generate reasoning text for the liquidity score.
    """
    if liquidity == 0:
        return "Market has zero liquidity. This is an extremely high-risk, illiquid market."
    elif score <= 10:
        return f"Market has very thin liquidity (${liquidity:,.0f}). High slippage risk."
    elif score <= 30:
        return f"Market has thin liquidity (${liquidity:,.0f}). Moderate slippage risk."
    elif score <= 70:
        return f"Market has good liquidity (${liquidity:,.0f}). Reasonable for trading."
    else:
        return f"Market has excellent liquidity (${liquidity:,.0f}). Low slippage risk."

def get_event_market_depth(event_id):
    """
    Fetches market depth data from Polymarket API and calculates factual liquidity scores.
    This is a pure Python function - NO AI calls.
    
    Returns a list of outcomes with their liquidity metrics.
    """
    try:
        # Get event details
        event_response = requests.get(f"{GAMMA_API}/events/{event_id}", timeout=10)
        if event_response.status_code != 200:
            print(f"Failed to fetch event: {event_response.status_code}")
            return []
        
        event_data = event_response.json()
        markets = event_data.get('markets', [])
        
        if not markets:
            print("No markets found")
            return []
        
        # Collect market depth data
        market_depth_data = []
        
        # Check if multi-outcome event
        is_multi_outcome = len(markets) > 1 and markets[0].get('groupItemTitle')
        
        for market_idx, market in enumerate(markets[:10]):  # Top 10 outcomes
            market_question = market.get('question', f'Market {market_idx + 1}')
            group_item_title = market.get('groupItemTitle', '')
            outcomes = json.loads(market.get('outcomes', '["Yes", "No"]'))
            
            # For multi-outcome events, use groupItemTitle as the outcome name
            if is_multi_outcome:
                outcome_name = group_item_title if group_item_title else market_question
            else:
                outcome_name = outcomes[0] if outcomes else 'Yes'
            
            # Get liquidity from the market
            liquidity = float(market.get('liquidityNum', 0))
            
            # Calculate factual score
            score = calculate_liquidity_score(liquidity)
            level = get_liquidity_level(score)
            reasoning = get_liquidity_reasoning(liquidity, score)
            
            # Get current price
            prices = json.loads(market.get('outcomePrices', '[0, 0]'))
            current_price = float(prices[0]) * 100 if prices else 0
            
            market_depth_data.append({
                'outcome': outcome_name,
                'market_question': market_question,
                'liquidity': round(liquidity, 2),
                'liquidity_score': score,
                'liquidity_level': level,
                'reasoning': reasoning,
                'current_price': round(current_price, 1)
            })
        
        # Sort by liquidity (highest first)
        market_depth_data.sort(key=lambda x: x['liquidity'], reverse=True)
        
        print(f"Found market depth data for {len(market_depth_data)} outcomes")
        return market_depth_data
        
    except Exception as e:
        print(f"Error in get_event_market_depth: {e}")
        import traceback
        traceback.print_exc()
        return []
