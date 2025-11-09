import os
from dotenv import load_dotenv
import json

load_dotenv()

# Try to import Anthropic, but make it optional
try:
    from anthropic import Anthropic
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        print("Warning: CLAUDE_API_KEY not found in environment")
        client = None
        CLAUDE_AVAILABLE = False
    else:
        client = Anthropic(api_key=api_key)
        CLAUDE_AVAILABLE = True
        print("Claude AI client initialized successfully")
except Exception as e:
    print(f"Warning: Claude AI not available: {e}")
    client = None
    CLAUDE_AVAILABLE = False

def get_unavailable_response(include_trader_quality=False):
    """Returns a standard response when Claude AI is unavailable"""
    response = {
        "sentiment_score": 0,
        "reasoning": "AI analysis unavailable. Please add a valid CLAUDE_API_KEY to backend/.env file. Get your API key at: https://console.anthropic.com/"
    }
    if include_trader_quality:
        response["trader_quality"] = "unknown"
    return response

def analyze_event_sentiment(event_data):
    """
    Analyzes a specific event and returns a sentiment score.
    For multi-outcome events, analyzes the overall market dynamics.
    """
    if not CLAUDE_AVAILABLE or not client:
        return get_unavailable_response()
    
    if not event_data:
        return {"sentiment_score": 0, "reasoning": "No event data to analyze"}
    
    event_info = f"""
Event: {event_data.get('title', 'N/A')}
Description: {event_data.get('description', 'N/A')}
Volume: ${event_data.get('volumeNum', 0):,.0f}
24h Volume: ${event_data.get('volume24hr', 0):,.0f}
Liquidity: ${event_data.get('liquidityNum', 0):,.0f}
"""
    
    # Add market prices - handle both binary and multi-outcome events
    markets = event_data.get('markets', [])
    is_multi_outcome = len(markets) > 1 and markets[0].get('groupItemTitle')
    
    if is_multi_outcome:
        event_info += f"\nMulti-Outcome Market - Top Outcomes:\n"
        for market in markets[:5]:  # Show top 5
            prices = json.loads(market.get('outcomePrices', '[0, 0]'))
            title = market.get('groupItemTitle', market.get('question', 'Unknown'))
            event_info += f"  {title}: {float(prices[0])*100:.1f}¢\n"
    elif markets:
        market = markets[0]
        prices = json.loads(market.get('outcomePrices', '[0, 0]'))
        outcomes = json.loads(market.get('outcomes', '["Yes", "No"]'))
        event_info += f"\nBinary Market Prices:\n"
        for i, outcome in enumerate(outcomes):
            event_info += f"  {outcome}: {float(prices[i])*100:.1f}¢\n"
    
    if is_multi_outcome:
        prompt = f"""Analyze this multi-outcome prediction market and assess market confidence.

{event_info}

For multi-outcome markets, provide a sentiment score from -100 to +100 based on:
- Market clarity: Is there a clear favorite or is it uncertain? (clear favorite = higher score)
- Market efficiency: Do prices reflect reasonable probabilities? (efficient = higher score)
- Volume and liquidity: Higher activity suggests more confidence (higher = positive score)

Respond in JSON format with:
- sentiment_score: integer from -100 to +100 (reflects market confidence and clarity)
- reasoning: 2-3 sentence explanation of market dynamics"""
    else:
        prompt = f"""Analyze this binary prediction market event and provide a sentiment score.

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
            model="claude-3-haiku-20240307",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        result = json.loads(response_text)
        return result
    except Exception as e:
        return {"sentiment_score": 0, "reasoning": f"Error analyzing sentiment: {str(e)}"}


def analyze_news_sentiment(news_articles, event_data):
    """
    Analyzes news articles related to an event and returns a sentiment score.
    """
    if not CLAUDE_AVAILABLE or not client:
        return get_unavailable_response()
    
    if not news_articles or len(news_articles) == 0:
        return {"sentiment_score": 0, "reasoning": "No news articles available for analysis"}
    
    # Format news articles for Claude
    news_text = "\n\n".join([
        f"Title: {article.get('title', 'N/A')}\nDescription: {article.get('description', 'N/A')}\nSource: {article.get('source', 'N/A')}"
        for article in news_articles[:10]  # Limit to 10 articles
    ])
    
    prompt = f"""Analyze these news articles related to the prediction market event: "{event_data.get('title', 'N/A')}"

News Articles:
{news_text}

Based on the news sentiment, tone, and implications, provide a sentiment score from -100 (very bearish/negative) to +100 (very bullish/positive).

Consider:
- Overall tone of the news (positive, negative, neutral)
- Likelihood of the event occurring based on news
- Market-moving information in the articles
- Credibility and recency of sources

Respond in JSON format with:
- sentiment_score: integer from -100 to +100
- reasoning: 2-3 sentence explanation of your analysis"""

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        result = json.loads(response_text)
        return result
    except Exception as e:
        return {"sentiment_score": 0, "reasoning": f"Error analyzing news sentiment: {str(e)}"}


def analyze_smart_wallets(market_depth_data, event_data):
    """
    Analyzes market depth and liquidity distribution for a specific event.
    Evaluates market health and trader participation.
    """
    if not CLAUDE_AVAILABLE or not client:
        return get_unavailable_response(include_trader_quality=True)
    
    if not market_depth_data or len(market_depth_data) == 0:
        return {"sentiment_score": 0, "reasoning": "No market depth data available for analysis", "trader_quality": "unknown"}
    
    # Format market depth data
    depth_summary = []
    for depth in market_depth_data:
        summary = {
            "outcome": depth.get('outcome'),
            "total_liquidity": depth.get('total_liquidity'),
            "unique_makers": depth.get('unique_makers'),
            "bid_volume": depth.get('total_bid_volume'),
            "ask_volume": depth.get('total_ask_volume'),
            "spread": depth.get('spread'),
            "total_orders": depth.get('total_orders')
        }
        depth_summary.append(summary)
    
    # Check if multi-outcome
    markets = event_data.get('markets', [])
    is_multi_outcome = len(markets) > 1 and markets[0].get('groupItemTitle')
    
    if is_multi_outcome:
        prompt = f"""Analyze the market depth and liquidity for this multi-outcome prediction market:

Event: {event_data.get('title', 'N/A')}

Market Depth by Outcome:
{json.dumps(depth_summary, indent=2)}

Evaluate market health based on:
- Liquidity distribution: Is liquidity concentrated or spread across outcomes?
- Maker participation: More unique makers = healthier market
- Order book balance: Balanced bid/ask volumes = efficient market
- Spread tightness: Tighter spreads = more liquid market

Provide a sentiment score from -100 to +100 based on:
- High liquidity + many makers + tight spreads = POSITIVE (healthy market)
- Low liquidity + few makers + wide spreads = NEGATIVE (thin market)
- Balanced distribution across outcomes = MORE POSITIVE

Respond in JSON format with:
- sentiment_score: integer from -100 to +100
- reasoning: 2-3 sentence explanation of market health
- trader_quality: string (excellent/good/average/poor) based on participation"""
    else:
        prompt = f"""Analyze the market depth and liquidity for this prediction market:

Event: {event_data.get('title', 'N/A')}

Market Depth:
{json.dumps(depth_summary, indent=2)}

Evaluate market health based on:
- Total liquidity: Higher = more trader confidence
- Maker participation: More unique makers = diverse opinions and healthy market
- Order book balance: Balanced bid/ask = efficient price discovery
- Spread: Tighter spread = more liquid and efficient market

Provide a sentiment score from -100 to +100 based on:
- High liquidity + many makers + tight spreads = POSITIVE (confident market)
- Low liquidity + few makers + wide spreads = NEGATIVE (uncertain market)
- Imbalanced order book = directional signal

Respond in JSON format with:
- sentiment_score: integer from -100 to +100
- reasoning: 2-3 sentence explanation of market quality
- trader_quality: string (excellent/good/average/poor) based on participation"""

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        result = json.loads(response_text)
        return result
    except Exception as e:
        return {"sentiment_score": 0, "reasoning": f"Error analyzing wallets: {str(e)}", "trader_quality": "unknown"}


def generate_combined_sentiment(news_sentiment, wallet_sentiment, event_data):
    """
    Generates a final combined sentiment score from news and wallet analysis.
    """
    if not CLAUDE_AVAILABLE or not client:
        response = get_unavailable_response()
        response["confidence"] = "low"
        return response
    
    prompt = f"""Synthesize these analyses into a final sentiment score for this prediction market:

Event: {event_data.get('title', 'N/A')}

News Sentiment Analysis:
{json.dumps(news_sentiment, indent=2)}

Smart Wallet Analysis:
{json.dumps(wallet_sentiment, indent=2)}

Provide a final weighted sentiment score from -100 (very bearish) to +100 (very bullish).
Weight news sentiment (50%) and smart wallet activity (50%) equally.

Respond in JSON format with:
- sentiment_score: integer from -100 to +100
- reasoning: 2-3 sentence comprehensive assessment
- confidence: string (low/medium/high)"""

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
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
