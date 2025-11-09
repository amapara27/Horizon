# Top 3 Outcomes Analysis UI

## What's New

Added a new UI section that displays individual sentiment analysis for the **top 3 most probable outcomes** in multi-outcome events.

## Features

### For Each Outcome, You'll See:

1. **Rank Badge** - #1, #2, #3 position
2. **Outcome Name & Current Price** - e.g., "Trump 65.0¢"
3. **Three Individual Scores:**
   - 📰 **News Sentiment** (-100 to +100): How news supports this specific outcome
   - 📊 **Market Depth Score** (-100 to +100): Liquidity quality for this outcome
   - 🎯 **Overall Score** (-100 to +100): Combined risk/reward assessment
4. **AI Reasoning** - 2-3 sentences explaining the scores

## Visual Layout

```
┌─────────────────────────────────────────────────────────────────┐
│              🎯 Top 3 Outcomes Analysis                         │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   #1 Outcome    │   #2 Outcome    │   #3 Outcome               │
│   Trump         │   Biden         │   Other                    │
│   65.0¢         │   25.0¢         │   8.0¢                     │
│                 │                 │                            │
│ 📰 News: +75    │ 📰 News: -20    │ 📰 News: -40              │
│ 📊 Depth: +85   │ 📊 Depth: +30   │ 📊 Depth: -15             │
│ 🎯 Overall: +80 │ 🎯 Overall: +5  │ 🎯 Overall: -25           │
│                 │                 │                            │
│ "News strongly  │ "Mixed signals  │ "Very thin liquidity      │
│  favors Trump   │  with moderate  │  makes this risky..."     │
│  with excellent │  liquidity..."  │                           │
│  liquidity..."  │                 │                            │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

## Color Coding

- **#1 Outcome**: Green border/accent (#10b981)
- **#2 Outcome**: Indigo border/accent (#6366f1)
- **#3 Outcome**: Amber border/accent (#f59e0b)

**Score Colors:**
- +50 to +100: Green (strong positive)
- +20 to +49: Lime (moderate positive)
- -19 to +19: Yellow (neutral)
- -20 to -49: Orange (moderate negative)
- -50 to -100: Red (strong negative)

## When It Appears

- **Multi-outcome events only** - automatically detected
- Appears after clicking "Run Analysis"
- Shows above the general sentiment analysis section
- Binary events continue to show only the 3-column layout

## API Endpoint

New endpoint: `GET /api/event/{event_id}/top-outcomes-analysis`

Returns:
```json
{
  "outcomes": [
    {
      "outcome": "Trump",
      "price": 65.0,
      "news_sentiment": 75,
      "market_depth_score": 85,
      "overall_score": 80,
      "reasoning": "News strongly favors this outcome with recent polling data..."
    },
    ...
  ]
}
```

## How to Test

1. Restart your backend server
2. Navigate to a **multi-outcome event** (e.g., election with multiple candidates)
3. Click "Run Analysis"
4. You'll see the new "Top 3 Outcomes Analysis" section appear
5. Each outcome shows its individual scores and reasoning

## Benefits

- **Compare outcomes side-by-side** - see which has best risk/reward
- **Understand each outcome individually** - not just overall market sentiment
- **Make better trading decisions** - know which outcome has best liquidity + news support
- **Visual hierarchy** - quickly identify the most attractive opportunities
