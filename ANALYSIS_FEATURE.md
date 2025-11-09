# Analysis Page Feature

## Overview
The Analysis page provides AI-powered sentiment analysis for individual prediction market events using Claude AI.

## Layout

### Three-Column Top Section
1. **Left Column**: Market data section (placeholder for future features)
2. **Center Column**: Event details with prices, volume, and liquidity
3. **Right Column**: Smart wallet positions showing how top traders are positioned

### Bottom AI Analysis Section
Three subsections providing sentiment scores:
1. **Event Analysis**: Claude analyzes the event fundamentals, volume, and market conditions
2. **Smart Wallet Analysis**: Claude analyzes how smart money is positioned
3. **Combined Sentiment**: Weighted combination (60% event, 40% wallets) with confidence level

## Sentiment Scoring
- Scores range from **-100 (very bearish)** to **+100 (very bullish)**
- Color-coded for easy interpretation:
  - Green (>50): Very Bullish
  - Light Green (20-50): Bullish
  - Yellow (-20 to 20): Neutral
  - Orange (-50 to -20): Bearish
  - Red (<-50): Very Bearish

## How to Use

1. Click on any event from the dashboard
2. View the event details and smart wallet positions
3. Click "Run Analysis" to get AI sentiment scores
4. Review the three sentiment analyses:
   - Event fundamentals
   - Smart wallet positioning
   - Combined final score

## API Endpoints

- `GET /api/event/{event_id}` - Get event details
- `GET /api/event/{event_id}/smart-wallets` - Get smart wallet positions
- `GET /api/event/{event_id}/sentiment` - Get event sentiment analysis
- `GET /api/event/{event_id}/wallet-sentiment` - Get wallet sentiment analysis
- `GET /api/event/{event_id}/combined-sentiment` - Get combined sentiment

## Technical Details

- **AI Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- **Backend**: FastAPI with Anthropic SDK
- **Frontend**: React with inline styling
- **Smart Wallets**: Currently uses mock data (Polymarket API limitations)

## Setup

1. Install backend dependencies:
```bash
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
```

2. Ensure `.env` has your Claude API key:
```
CLAUDE_API_KEY=your-api-key-here
```

3. Start the backend:
```bash
uvicorn main:app --reload
```

4. Start the frontend:
```bash
cd frontend
npm start
```

## Notes

- Analysis takes 10-20 seconds as Claude processes the data
- Smart wallet data is currently mocked due to Polymarket API limitations
- The combined sentiment weighs event analysis at 60% and wallet analysis at 40%
