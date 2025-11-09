import requests
import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def extract_keywords(title):
    """
    Extract meaningful keywords from text for news search.
    Simplified to focus on the most important terms - uses OR for broader results.
    """
    # Remove common question words and punctuation
    title = re.sub(r'\?|!|\.', '', title)
    
    # Keywords to remove (too generic)
    stop_words = ['in', 'on', 'at', 'by', 'for', 'to', 'of', 'the', 'a', 'an', 'will', 'does', 'is', 'are', 'this', 'that', 'be', 'and', 'or']
    
    # Split into words and filter
    words = title.split()
    keywords = [w for w in words if w.lower() not in stop_words and len(w) > 2]
    
    # Return the most important keywords - use OR for broader results
    if len(keywords) >= 2:
        return ' OR '.join(f'"{w}"' for w in keywords[:2])  # Only top 2 keywords with OR
    elif len(keywords) == 1:
        return f'"{keywords[0]}"'
    else:
        return f'"{title}"'

def get_event_news(event_title, market_question, outcome_name, max_results=20):
    """
    Fetch news articles related to a specific outcome from the last 30 days.
    Uses event title + outcome name for search query.
    
    Args:
        event_title: The event title (e.g., "What price will Bitcoin hit in November 2024?")
        market_question: The market question (e.g., "Top Searched Person on Google in 2024")
        outcome_name: The specific outcome (e.g., "Pope Leo XIV")
        max_results: Maximum number of articles to return
    
    Returns:
        Dictionary with articles list and query info
    """
    if not NEWS_API_KEY:
        return {"error": "NEWS_API_KEY not configured", "articles": []}
    
    # Calculate date range (last 30 days for maximum results)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    from_date = thirty_days_ago.strftime('%Y-%m-%d')
    
    # Combine event title and outcome name for search query
    # Extract key terms from event title
    clean_title = re.sub(r'[^\w\s]', '', event_title)
    title_words = [w for w in clean_title.split() if len(w) > 3][:3]  # Top 3 words from title
    
    # Clean outcome name
    clean_outcome = re.sub(r'[^\w\s]', '', outcome_name)
    
    # Combine title keywords with outcome
    query_parts = title_words + [clean_outcome]
    query = ' '.join(query_parts).strip()
    
    # If query is too short or generic, don't search
    if len(query) < 3:
        return {
            'articles': [],
            'query_used': query,
            'outcome_name': outcome_name,
            'market_question': market_question
        }
    
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': max_results,
        'from': from_date
    }
    
    print(f"News API query: {query}")
    
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = []
            for article in data.get('articles', []):
                # Filter out removed articles
                if article.get('title') and '[Removed]' not in article.get('title', ''):
                    articles.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'url': article.get('url'),
                        'source': article.get('source', {}).get('name'),
                        'publishedAt': article.get('publishedAt'),
                        'urlToImage': article.get('urlToImage')
                    })
            
            print(f"Found {len(articles)} articles for '{query}'")
            
            return {
                'articles': articles,
                'query_used': query,
                'outcome_name': outcome_name,
                'market_question': market_question
            }
        else:
            print(f"News API error: {data.get('message', 'Unknown error')}")
            return {'error': data.get('message', 'Unknown error'), 'articles': []}
            
    except requests.exceptions.RequestException as e:
        print(f"News API request error: {str(e)}")
        return {'error': str(e), 'articles': []}
