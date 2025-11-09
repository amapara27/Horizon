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
    Analyzes news articles using Claude Sonnet 4 with probability assessment.
    Returns sentiment score, probability, and concise bullet-point reasoning.
    """
    if not CLAUDE_AVAILABLE or not client:
        return {
            "score": 0,
            "probability_assessment": "Unknown",
            "reasoning": "AI analysis unavailable"
        }
    
    if not news_articles or len(news_articles) == 0:
        print(f"No articles for '{outcome_name}'")
        return {
            "score": 0,
            "probability_assessment": "Insufficient data",
            "reasoning": "No relevant news found"
        }
    
    print(f"Analyzing {len(news_articles)} articles for '{outcome_name}'")
    
    news_text = "\n\n".join([
        f"Title: {article.get('title', 'N/A')}\nDescription: {article.get('description', 'N/A')}\nSource: {article.get('source', 'N/A')}"
        for article in news_articles[:10]
    ])
    
    prompt = f"""Analyze news for prediction market outcome.

MARKET: "{market_question}"
OUTCOME: "{outcome_name}"

NEWS:
{news_text}

TASK:
1. Check if news is relevant to "{outcome_name}"
2. If NO → score: 0, probability: "Insufficient data"
3. If YES → Assess probability and score

PROBABILITY LEVELS:
- "Very High" (70-100%): Strong evidence outcome will happen
- "High" (55-70%): Good evidence favoring outcome
- "Moderate" (45-55%): Mixed/unclear
- "Low" (30-45%): Evidence suggests unlikely
- "Very Low" (0-30%): Strong evidence against
- "Insufficient data": No relevant news

SCORE (-100 to +100):
- Positive: News makes outcome MORE likely
- Negative: News makes outcome LESS likely
- Zero: No relevant news

REASONING FORMAT (3 bullets, max 10 words each):
• Relevancy: [Yes/No + why in 5 words]
• Evidence: [Top 1-2 facts only]
• Impact: [Effect on probability in 5 words]

BE EXTREMELY CONCISE. Cut all unnecessary words.

Return ONLY valid JSON:
{{
  "score": <-100 to +100>,
  "probability_assessment": "<Very High|High|Moderate|Low|Very Low|Insufficient data>",
  "reasoning": "• Relevancy: [text]
• Evidence: [text]
• Impact: [text]"
}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        print(f"Response: {response_text[:150]}...")
        
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        result = json.loads(response_text, strict=False)
        print(f"'{outcome_name}': score={result.get('score', 0)}, prob={result.get('probability_assessment', 'Unknown')}")
        return result
    except json.JSONDecodeError as e:
        print(f"JSON error: {str(e)}")
        return {"score": 0, "probability_assessment": "Error", "reasoning": "Error parsing response"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"score": 0, "probability_assessment": "Error", "reasoning": "Error analyzing news"}


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
    
    prompt = f"""Create concise summary for prediction market outcome.

OUTCOME: "{outcome_name}"

NEWS ANALYSIS:
- Score: {news_analysis.get('score', 0)} (-100 to +100)
- Probability: {news_analysis.get('probability_assessment', 'Unknown')}
- Reasoning: {news_analysis.get('reasoning', 'N/A')}

LIQUIDITY:
- Score: {depth_analysis.get('liquidity_score', 0)} (0-100)
- Level: {depth_analysis.get('liquidity_level', 'Unknown')}
- Reasoning: {depth_analysis.get('reasoning', 'N/A')}

Create 4-5 bullets (max 8 words each):
• Probability: [assessment]
• Signal: [positive/negative/neutral + why]
• News: [key finding]
• Liquidity: [level + risk]
• Recommendation: [actionable - use "bet for/against" or "consider/avoid" language]

BE CONCISE. Use active language like "Bet against", "Consider betting for", "Avoid due to low liquidity", etc.

Return ONLY valid JSON:
{{
  "summary": "• Probability: [text]
• Signal: [text]
• News: [text]
• Liquidity: [text]
• Recommendation: [text]"
}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        print(f"Summary response: {response_text[:150]}...")
        
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        result = json.loads(response_text, strict=False)
        return result
    except json.JSONDecodeError as e:
        print(f"JSON error: {str(e)}")
        return {"summary": "• Error: Unable to generate summary"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"summary": "• Error: Unable to generate summary"}
