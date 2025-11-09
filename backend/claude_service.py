import os
from dotenv import load_dotenv
import json

load_dotenv()

# Try to import Anthropic, but make it optional
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
    CLAUDE_AVAILABLE = True
except Exception as e:
    print(f"Warning: Claude AI not available: {e}")
    client = None
    CLAUDE_AVAILABLE = False

def analyze_event_sentiment(event_data):
    """
    Analyzes a specific event and returns a sentiment score.
    Returns a percentage between -100 (very bearish) and +100 (very bullish).
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "sentiment_score": 0, 
            "reasoning": "Claude AI is not available. Please check your API key and dependencies."
        }
    
    if not event_data:
        return {"sentiment_score": 0, "reasoning": "No event data to analyze"}
    
    event_info = f"""
Event: {event_data.get('title', 'N/A')}
Description: {event_data.get('description', 'N/A')}
Volume: ${event_data.get('volumeNum', 0):,.0f}
24h Volume: ${event_data.get('volume24hr', 0):,.0f}
Liquidity: ${event_data.get('liquidityNum', 0):,.0f}
"""
    
    # Add market prices
    markets = event_data.get('markets', [])
    if markets:
        market = markets[0]
        prices = json.loads(market.get('outcomePrices', '[0, 0]'))
        outcomes = json.loads(market.get('outcomes', '["Yes", "No"]'))
        event_info += f"\nCurrent Prices:\n"
        for i, outcome in enumerate(outcomes):
            event_info += f"  {outcome}: {float(prices[i])*100:.1f}¢\n"
    
    prompt = f"""Analyze this prediction market event and provide a sentiment score.

{event_info}

Based on the event details, market activity, and current prices, provide a sentiment score from -100 (very bearish/unlikely) to +100 (very bullish/likely).

Consider:
- Market volume and liquidity (higher = more confidence)
- Price trends and positioning
- Event likelihood and market efficiency

Respond in JSON format with:
- sentiment_score: integer from -100 to +100
- reasoning: 2-3 sentence explanation of your analysis"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        result = json.loads(response_text)
        return result
    except Exception as e:
        return {"sentiment_score": 0, "reasoning": f"Error analyzing sentiment: {str(e)}"}


def analyze_smart_wallets(wallet_data, event_data):
    """
    Analyzes smart wallet activity for a specific event.
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "sentiment_score": 0, 
            "reasoning": "Claude AI is not available. Please check your API key and dependencies."
        }
    
    if not wallet_data or len(wallet_data) == 0:
        return {"sentiment_score": 0, "reasoning": "No wallet data available for analysis"}
    
    prompt = f"""Analyze smart wallet trading activity for this prediction market event:

Event: {event_data.get('title', 'N/A')}

Smart Wallet Activity:
{json.dumps(wallet_data, indent=2)}

Based on the wallet positions, trading patterns, and win rates, provide a sentiment score from -100 (very bearish) to +100 (very bullish).

Consider:
- Position directions and sizes
- Wallet win rates and profitability
- Trading conviction (larger positions = more confidence)

Respond in JSON format with:
- sentiment_score: integer from -100 to +100
- reasoning: 2-3 sentence explanation"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        result = json.loads(response_text)
        return result
    except Exception as e:
        return {"sentiment_score": 0, "reasoning": f"Error analyzing wallets: {str(e)}"}


def generate_combined_sentiment(event_sentiment, wallet_sentiment, event_data):
    """
    Generates a final combined sentiment score.
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "sentiment_score": 0,
            "reasoning": "Claude AI is not available. Please check your API key and dependencies.",
            "confidence": "low"
        }
    
    prompt = f"""Synthesize these analyses into a final sentiment score for this prediction market:

Event: {event_data.get('title', 'N/A')}

Event Analysis:
{json.dumps(event_sentiment, indent=2)}

Smart Wallet Analysis:
{json.dumps(wallet_sentiment, indent=2)}

Provide a final weighted sentiment score from -100 (very bearish) to +100 (very bullish).
Weight event fundamentals (60%) and smart wallet activity (40%).

Respond in JSON format with:
- sentiment_score: integer from -100 to +100
- reasoning: 2-3 sentence comprehensive assessment
- confidence: string (low/medium/high)"""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        result = json.loads(response_text)
        return result
    except Exception as e:
        return {
            "sentiment_score": 0,
            "reasoning": f"Error generating combined sentiment: {str(e)}",
            "confidence": "low"
        }
