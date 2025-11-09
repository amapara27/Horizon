# Quick Start Guide

## Prerequisites
- Python 3.x with virtual environment
- Node.js and npm
- Claude API key
- News API key

## Setup (First Time Only)

### 1. Environment Variables
Create/verify `backend/.env`:
```bash
CLAUDE_API_KEY=your-claude-api-key-here
NEWS_API_KEY=your-news-api-key-here
```

### 2. Install Backend Dependencies
```bash
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

## Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
source ../venv/bin/activate
uvicorn main:app --reload
```

Backend will run on: `http://127.0.0.1:8000`

### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```

Frontend will open at: `http://localhost:3000`

## Using the Application

### Dashboard
1. View three columns of events (Tech, Trending, Sports)
2. Click any event to view detailed analysis

### Analysis Page

**Top Section (3 columns):**
- **Left**: Related news articles (clickable)
- **Center**: Event details, prices, volume
- **Right**: Smart wallet positions

**Bottom Section (AI Analysis):**
1. Click "Run Analysis" button
2. Wait 10-20 seconds for Claude to process
3. View three sentiment scores:
   - **Left**: News sentiment (-100 to +100)
   - **Middle**: Overall sentiment (combined)
   - **Right**: Wallet sentiment (-100 to +100)

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Reinstall dependencies
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
```

### Frontend shows "Failed to fetch"
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS is enabled in backend

### Claude AI not working
- Check `CLAUDE_API_KEY` in `.env`
- Verify anthropic package: `pip list | grep anthropic`
- Check backend terminal for error messages

### News not loading
- Check `NEWS_API_KEY` in `.env`
- Verify News API rate limits (100/day free tier)
- Check backend terminal for API errors

## API Endpoints Reference

### Dashboard
- `GET /api/tech-events`
- `GET /api/trending-events`
- `GET /api/sports-events`

### Analysis
- `GET /api/event/{id}` - Event details
- `GET /api/event/{id}/news` - News articles
- `GET /api/event/{id}/smart-wallets` - Wallet positions
- `GET /api/event/{id}/news-sentiment` - News AI analysis
- `GET /api/event/{id}/wallet-sentiment` - Wallet AI analysis
- `GET /api/event/{id}/combined-sentiment` - Combined AI analysis

## File Structure

```
Horizon-1/
├── backend/
│   ├── main.py                 # FastAPI app & endpoints
│   ├── claude_service.py       # Claude AI integration
│   ├── news_service.py         # News API integration
│   ├── wallet_service.py       # Smart wallet data
│   ├── polymarket_fetcher.py   # Polymarket API
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # API keys (create this)
│   └── start.sh               # Backend startup script
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.js    # Dashboard
│   │   │   └── AnalysisPage.js # Analysis page
│   │   ├── App.js             # Main app
│   │   └── App.css            # Styles
│   └── package.json           # Node dependencies
└── venv/                      # Python virtual environment
```

## Tips

- **Analysis Speed**: Claude takes 10-20 seconds, be patient
- **News Quality**: More specific event titles = better news results
- **Rate Limits**: News API free tier = 100 requests/day
- **Mock Data**: Smart wallets currently use mock data
- **Sentiment Scores**: -100 (bearish) to +100 (bullish)

## Support

Check these files for more details:
- `FINAL_IMPLEMENTATION.md` - Complete feature documentation
- `SETUP_GUIDE.md` - Detailed setup instructions
- `FIXES_APPLIED.md` - Bug fixes and solutions
