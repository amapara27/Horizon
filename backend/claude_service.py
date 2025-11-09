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


def analyze_news_sentiment(news_articles, event_data):
    """
    Analyzes news articles related to an event and returns a sentiment score.
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "sentiment_score": 0, 
            "reasoning": "Claude AI is not available. Please check your API key and dependencies."
        }
    
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
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        result = json.loads(response_text)
        return result
    except Exception as e:
        return {"sentiment_score": 0, "reasoning": f"Error analyzing news sentiment: {str(e)}"}


def analyze_smart_wallets(wallet_data, event_data):
    """
    Analyzes smart wallet activity for a specific event based on their historical performance.
    Evaluates the quality of traders investing in this event.
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "sentiment_score": 0, 
            "reasoning": "Claude AI is not available. Please check your API key and dependencies."
        }
    
    if not wallet_data or len(wallet_data) == 0:
        return {"sentiment_score": 0, "reasoning": "No wallet data available for analysis"}
    
    # Format wallet data with historical performance
    wallet_summary = []
    for wallet in wallet_data:
        summary = {
            "position": wallet.get('position'),
            "size": wallet.get('size'),
            "historical_win_rate": wallet.get('win_rate', 'N/A'),
            "total_historical_trades": wallet.get('historical_trades', 'N/A'),
            "total_profit": wallet.get('total_profit', 'N/A'),
            "markets_traded": wallet.get('markets_traded', 'N/A')
        }
        wallet_summary.append(summary)
    
    prompt = f"""Analyze the quality of traders investing in this prediction market event:

Event: {event_data.get('title', 'N/A')}

Top Traders and Their Historical Performance:
{json.dumps(wallet_summary, indent=2)}

Evaluate the QUALITY of these traders based on their historical performance:
- Win rates (higher = better traders)
- Total trades (more experience = more reliable)
- Profitability (consistent profits = skilled traders)
- Market diversity (more markets = well-rounded)

Provide a sentiment score from -100 to +100 based on:
- If GOOD traders (high win rates, profitable) are investing → HIGHER score
- If POOR traders (low win rates, unprofitable) are investing → LOWER score
- Consider the DIRECTION they're betting (YES/NO) and their conviction

The score reflects: "Are skilled, successful traders confident in this outcome?"

Respond in JSON format with:
- sentiment_score: integer from -100 to +100
- reasoning: 2-3 sentence explanation focusing on trader quality
- trader_quality: string (excellent/good/average/poor)"""

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
        return {"sentiment_score": 0, "reasoning": f"Error analyzing wallets: {str(e)}", "trader_quality": "unknown"}


def generate_combined_sentiment(news_sentiment, wallet_sentiment, event_data):
    """
    Generates a final combined sentiment score from news and wallet analysis.
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "sentiment_score": 0,
            "reasoning": "Claude AI is not available. Please check your API key and dependencies.",
            "confidence": "low"
        }
    
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
