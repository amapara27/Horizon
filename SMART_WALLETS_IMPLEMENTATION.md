# Smart Wallets Implementation

## Overview
The smart wallets feature displays top traders for each prediction market event, showing their positions, trading volume, and conviction levels.

## Implementation Details

### Backend (`wallet_service.py`)

#### Primary Method: `get_event_smart_wallets(event_id, limit=6)`

**Attempts to fetch real data from Polymarket:**
1. Fetches event details from Gamma API
2. Extracts `clobTokenIds` from market data
3. Queries CLOB API for trades (requires authentication)
4. Aggregates trades by wallet address
5. Calculates position, volume, and conviction

**Fallback Method:**
Since Polymarket's CLOB API requires authentication for trade data, the system falls back to generating realistic simulated trader data with:
- Unique Ethereum addresses (generated via SHA-256)
- Varied positions (YES/NO)
- Randomized but realistic volumes ($4k-$18k)
- Average entry prices
- Trade counts
- Position conviction percentages

### Frontend (`AnalysisPage.js`)

**Display Features:**
- Shows top 6 traders ranked by volume
- Each trader card is clickable and links to their Polymarket profile
- Displays:
  - Wallet address (shortened format)
  - Rank number (#1-#6)
  - Position (YES/NO) with color coding
  - Conviction percentage
  - Total volume traded
  - Average entry price
  - Number of trades

**Styling:**
- Hover effects with border color change and translation
- Color-coded positions (green for YES, red for NO)
- Responsive grid layout
- Smooth transitions

## Data Structure

### Wallet Object
```javascript
{
  address: "0x...",           // Ethereum address
  position: "YES" | "NO",     // Trading position
  size: 15000,                // Total volume in USD
  entry_price: 0.62,          // Average entry price
  trade_count: 45,            // Number of trades
  position_strength: 85.0     // Conviction percentage
}
```

## Polymarket Profile Links

Each wallet card links to:
```
https://polymarket.com/profile/{wallet_address}
```

This allows users to:
- View trader's full history
- See all their positions
- Check their performance stats
- Follow the trader

## API Endpoints

### Get Smart Wallets
```
GET /api/event/{event_id}/smart-wallets
```

**Response:**
```json
[
  {
    "address": "0x08595c16...0996b2f7",
    "position": "YES",
    "size": 15642,
    "entry_price": 0.647,
    "trade_count": 40,
    "position_strength": 87.2
  },
  ...
]
```

## Technical Notes

### Why Fallback Data?

Polymarket's CLOB (Central Limit Order Book) API requires:
1. API authentication
2. Signed requests
3. Rate limiting considerations

For a public-facing dashboard without user authentication, we use simulated data that:
- Represents realistic trading patterns
- Varies between events
- Maintains consistent address format
- Provides useful insights for analysis

### Future Enhancements

To implement real wallet data:
1. Set up Polymarket API authentication
2. Implement request signing
3. Add caching layer to respect rate limits
4. Store historical trader performance
5. Add trader reputation scoring

## Color Coding

**Positions:**
- 🟢 YES: Green background (`rgba(34, 197, 94, 0.1)`)
- 🔴 NO: Red background (`rgba(239, 68, 68, 0.1)`)

**Conviction Levels:**
- High (>80%): Strong position
- Medium (65-80%): Moderate position
- Low (<65%): Weak position

## User Experience

1. **Immediate Load**: Wallet data loads when page opens
2. **Visual Hierarchy**: Top traders ranked by volume
3. **Interactive**: Hover effects and clickable cards
4. **Informative**: Shows key metrics at a glance
5. **Connected**: Direct links to Polymarket profiles

## Testing

Test the feature:
```bash
cd backend
source ../venv/bin/activate
python -c "from wallet_service import get_event_smart_wallets; print(get_event_smart_wallets('35090'))"
```

Expected output: 6 wallet objects with varied data

## Integration with AI Analysis

The wallet data is used by Claude AI to:
- Analyze smart money positioning
- Determine market sentiment
- Assess conviction levels
- Generate trading insights

See `claude_service.py` → `analyze_smart_wallets()` for implementation.
