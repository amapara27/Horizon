# Horizon - Polymarket Analysis Dashboard

An AI-powered prediction market analysis platform that combines real-time Polymarket data with news sentiment analysis to help traders make informed decisions.

## What It Does

Horizon analyzes Polymarket prediction markets by:

1. **Fetching Live Market Data** - Pulls real-time prices, liquidity, and order book depth from Polymarket
2. **Gathering Relevant News** - Searches for recent news articles related to each market outcome using NewsAPI
3. **AI Sentiment Analysis** - Uses Claude AI to analyze news sentiment and assess how it might impact market outcomes
4. **Liquidity Scoring** - Evaluates market depth and liquidity to identify tradeable opportunities
5. **Comprehensive Summaries** - Generates AI-powered summaries combining market data, news sentiment, and liquidity analysis

## Features

- 📊 **Deep Market Analysis** - Detailed breakdown of top 3 outcomes per market with liquidity scores
- 📰 **News Integration** - Real-time news articles with AI sentiment analysis for each outcome
- 🤖 **Claude AI Insights** - Smart summaries that combine market metrics with news sentiment
- 💧 **Liquidity Analysis** - Order book depth analysis to identify liquid vs illiquid markets
- 🔥 **Multiple Categories** - Browse Tech, Trending, and Sports prediction markets
- 🎨 **Modern UI** - Clean, responsive design with smooth animations
- ⚡ **Real-time Data** - Live updates from Polymarket's Gamma API

## Tech Stack

**Frontend:**
- React
- Modern CSS with gradient backgrounds and glass-morphism effects
- Responsive design

**Backend:**
- FastAPI (Python)
- Polymarket Gamma API integration
- Claude AI (Anthropic) for sentiment analysis
- NewsAPI for real-time news gathering
- CORS enabled for local development

## Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```bash
ANTHROPIC_API_KEY=your_claude_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

Get your API keys:
- Claude API: https://console.anthropic.com/
- NewsAPI: https://newsapi.org/

5. Start the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## API Endpoints

- `GET /api/tech-events` - Fetch tech-related prediction markets
- `GET /api/trending-events` - Fetch trending events by 24hr volume
- `GET /api/sports-events` - Fetch sports-related markets
- `GET /api/event/{event_id}` - Get detailed event information
- `GET /api/event/{event_id}/analysis` - Get comprehensive AI analysis including:
  - Market depth and liquidity scores
  - News sentiment analysis
  - AI-generated trading insights

## Project Structure

```
horizon/
├── backend/
│   ├── main.py                    # FastAPI application & API endpoints
│   ├── polymarket_fetcher.py      # Polymarket API integration
│   ├── market_depth_service.py    # Liquidity analysis & scoring
│   ├── news_service.py            # NewsAPI integration
│   ├── claude_service.py          # Claude AI sentiment analysis
│   └── .env                       # API keys (not in repo)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.js        # Market browser
│   │   │   └── AnalysisPage.js    # Detailed analysis view
│   │   ├── services/
│   │   │   └── api.js             # API client
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## Development

### Running Both Servers

You'll need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## Contributing

Feel free to open issues or submit pull requests!

## License

MIT
