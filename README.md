# Horizon - Polymarket Dashboard

A modern, real-time dashboard for tracking Polymarket prediction markets. Built with React and FastAPI.

## Features

- 🚀 **Newest Events** - Track the latest prediction markets
- 🔥 **Trending Events** - See what's hot by 24-hour volume
- 🪙 **Crypto Events** - Monitor crypto-related markets
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

4. Create a `.env` file (optional - currently no API keys required for Polymarket):
```bash
cp .env.example .env
```

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

- `GET /api/new-events` - Fetch newest events
- `GET /api/trending-events` - Fetch trending events by volume
- `GET /api/crypto-events` - Fetch crypto-related events

## Project Structure

```
horizon/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── polymarket_fetcher.py   # Polymarket API integration
│   └── .env.example            # Environment variables template
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── HomePage.js     # Main dashboard component
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── App.js
│   │   ├── App.css             # Styling
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
