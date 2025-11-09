import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def extract_keywords(title):
    """
    Extract meaningful keywords from event title for better news search.
    """
    # Remove common question words and punctuation
    title = re.sub(r'\?|!|\.', '', title)
    
    # Keywords to remove (too generic)
    stop_words = ['in', 'on', 'at', 'by', 'for', 'to', 'of', 'the', 'a', 'an', 'will', 'does', 'is', 'are', 'this', 'that']
    
    # Common topic mappings for better results
    topic_keywords = {
        'fed': ['Federal Reserve', 'interest rates', 'Jerome Powell', 'FOMC'],
        'trump': ['Donald Trump', 'Trump administration'],
        'bitcoin': ['Bitcoin', 'cryptocurrency', 'crypto'],
        'ai': ['artificial intelligence', 'AI technology'],
        'election': ['election', 'voting', 'polls'],
        'ukraine': ['Ukraine', 'Russia Ukraine'],
        'israel': ['Israel', 'Gaza', 'Middle East'],
        'china': ['China', 'Xi Jinping'],
        'elon': ['Elon Musk', 'Tesla', 'SpaceX'],
        'meta': ['Meta', 'Facebook', 'Mark Zuckerberg'],
        'google': ['Google', 'Alphabet'],
        'apple': ['Apple', 'iPhone'],
        'nfl': ['NFL', 'football'],
        'nba': ['NBA', 'basketball'],
        'rates': ['interest rates', 'Federal Reserve'],
        'decision': ['Federal Reserve', 'FOMC', 'interest rates']
    }
    
    # Check if any topic keywords match
    title_lower = title.lower()
    for key, expansions in topic_keywords.items():
        if key in title_lower:
            return ' OR '.join(f'"{exp}"' for exp in expansions)
    
    # Split into words and filter
    words = title.split()
    keywords = [w for w in words if w.lower() not in stop_words and len(w) > 2]
    
    # If we have good keywords, use them
    if len(keywords) >= 2:
        return ' AND '.join(keywords[:3])
    elif len(keywords) == 1:
        return keywords[0]
    else:
        return title

def get_event_news(event_title, max_results=10):
    """
    Fetch news articles related to an event title.
    """
    if not NEWS_API_KEY:
        return {"error": "NEWS_API_KEY not configured"}
    
    # Extract better search query
    query = extract_keywords(event_title)
    
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': max_results
    }
    
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
            return {'articles': articles}
        else:
            return {'error': data.get('message', 'Unknown error')}
            
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
