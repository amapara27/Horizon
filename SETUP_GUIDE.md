# Setup Guide - Horizon Dashboard

## Quick Start

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Activate virtual environment**:
```bash
source ../venv/bin/activate
```

3. **Install dependencies** (if not already installed):
```bash
pip install -r requirements.txt
```

4. **Start the backend server**:
```bash
./start.sh
```

Or manually:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Open a new terminal** and navigate to frontend directory:
```bash
cd frontend
```

2. **Install dependencies** (if not already installed):
```bash
npm install
```

3. **Start the development server**:
```bash
npm start
```

The frontend will open at `http://localhost:3000`

## Features

### Dashboard (Home Page)
- View Tech Events, Trending Events, and Sports Events
- Click on any event to view detailed analysis

### Analysis Page
- **Three-column layout**:
  - Left: Market data (placeholder)
  - Center: Event details with prices and volume
  - Right: Smart wallet positions
  
- **AI Sentiment Analysis** (bottom section):
  - Event Analysis: AI analyzes market fundamentals
  - Smart Wallet Analysis: AI analyzes smart money positioning
  - Combined Sentiment: Weighted final score with confidence level

## API Endpoints

### Dashboard Endpoints
- `GET /api/tech-events` - Get tech-related events
- `GET /api/trending-events` - Get trending events by volume
- `GET /api/sports-events` - Get sports events

### Analysis Endpoints
- `GET /api/event/{event_id}` - Get event details
- `GET /api/event/{event_id}/smart-wallets` - Get smart wallet positions
- `GET /api/event/{event_id}/sentiment` - Get event sentiment analysis
- `GET /api/event/{event_id}/wallet-sentiment` - Get wallet sentiment analysis
- `GET /api/event/{event_id}/combined-sentiment` - Get combined sentiment

## Environment Variables

Make sure `backend/.env` contains:
```
CLAUDE_API_KEY=your-claude-api-key-here
NEWS_API_KEY=your-news-api-key-here
```

## Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use

### Frontend shows "Failed to fetch"
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify backend URL in frontend code is correct

### Claude AI not working
- Check your `CLAUDE_API_KEY` in `.env`
- Verify anthropic package is installed: `pip list | grep anthropic`
- The app will still work without Claude, but sentiment analysis won't be available

## Dependencies

### Backend
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Requests 2.31.0
- Python-dotenv 1.0.0
- Anthropic 0.18.1
- httpx 0.27.0

### Frontend
- React
- React Router DOM
- Standard React dependencies

## Notes

- Smart wallet data is currently mocked due to Polymarket API limitations
- Sentiment analysis takes 10-20 seconds to complete
- The combined sentiment weighs event analysis at 60% and wallet analysis at 40%
