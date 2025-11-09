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

def analyze_news_sentiment(news_articles, outcome_name, market_question):
    """
    Analyzes news articles for a specific outcome and returns a sentiment score.
    
    CRITICAL RULE: If no relevant news is found, return score of 0 with reasoning
    "No relevant news found." Do NOT invent negative sentiment from lack of news.
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "score": 0,
            "reasoning": "AI analysis unavailable. Please add a valid CLAUDE_API_KEY to backend/.env file."
        }
    
    # Check if we have articles
    if not news_articles or len(news_articles) == 0:
        return {
            "score": 0,
            "reasoning": "No relevant news found in the last 30 days for this outcome."
        }
    
    # Format news articles for Claude
    news_text = "\n\n".join([
        f"Title: {article.get('title', 'N/A')}\nDescription: {article.get('description', 'N/A')}\nSource: {article.get('source', 'N/A')}"
        for article in news_articles[:10]  # Limit to 10 articles
    ])
    
    prompt = f"""Analyze these news articles for the specific outcome: "{outcome_name}" in the market: "{market_question}"

News Articles (last 30 days):
{news_text}

CRITICAL RULES:
1. If the news articles are NOT specifically about "{outcome_name}", return a score of 0 and reasoning "No relevant news found."
2. Do NOT invent negative sentiment from a lack of news. Absence of news = score of 0, not negative.
3. Only return a non-zero score if the news is clearly relevant to this specific outcome.

Analyze the news:
1. Are these articles specifically about "{outcome_name}"? If not, score = 0.
2. If yes, what is the sentiment? Positive news = positive score, negative news = negative score.
3. How strong is the signal? Strong = higher magnitude, weak = lower magnitude.

Sentiment Score Guidelines:
- 0: No relevant news found
- +70 to +100: Very positive news strongly supporting this outcome
- +30 to +69: Moderately positive news
- +1 to +29: Slightly positive news
- -1 to -29: Slightly negative news
- -30 to -69: Moderately negative news
- -70 to -100: Very negative news contradicting this outcome

Respond with ONLY valid JSON (no markdown):
{{
  "score": <integer from -100 to +100>,
  "reasoning": "<2-3 sentences explaining the news sentiment or stating 'No relevant news found.'>"
}}"""

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
        return {"score": 0, "reasoning": f"Error analyzing news: {str(e)}"}


def generate_final_summary(outcome_name, news_analysis, depth_analysis):
    """
    Generates a concise bullet-point summary synthesizing news and liquidity data.
    This is the new "Overall Analysis" - AI as summarizer, not predictor.
    
    Args:
        outcome_name: The outcome being analyzed
        news_analysis: Dict with 'score' and 'reasoning' from news sentiment
        depth_analysis: Dict with 'liquidity_score', 'liquidity_level', 'reasoning' from market depth
    
    Returns:
        Dict with 'summary' text (bullet points on new lines)
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "summary": "• AI analysis unavailable. Please configure CLAUDE_API_KEY."
        }
    
    prompt = f"""Synthesize a concise bullet-point summary for this prediction market outcome.

Outcome: "{outcome_name}"

News Sentiment Analysis:
- Score: {news_analysis.get('score', 0)} (range: -100 to +100, where 0 = no news)
- Reasoning: {news_analysis.get('reasoning', 'No analysis available')}

Market Liquidity Analysis:
- Score: {depth_analysis.get('liquidity_score', 0)} (range: 0-100, factual metric)
- Level: {depth_analysis.get('liquidity_level', 'Unknown')}
- Reasoning: {depth_analysis.get('reasoning', 'No analysis available')}

Write a concise summary with 3-4 bullet points, each on a new line:
• Signal: State if positive, negative, or neutral
• News: Summarize news sentiment in one short phrase
• Liquidity: State liquidity level and trading risk
• Recommendation: One sentence on market attractiveness

Example format:
• Signal: Neutral - no clear direction
• News: No relevant coverage found in last 30 days
• Liquidity: Zero liquidity - extremely high risk
• Recommendation: Avoid trading; price is meaningless

IMPORTANT: Put each bullet on its own line (use \\n between bullets, not blank lines).

Respond with ONLY valid JSON (no markdown):
{{
  "summary": "<your bullet points here, each starting with • on a new line>"
}}"""

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
        return {"summary": f"• Error generating summary: {str(e)}"}
