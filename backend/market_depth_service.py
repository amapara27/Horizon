import requests
import json
from collections import defaultdict

GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"

def get_event_market_depth(event_id, limit=6):
    """
    Fetches aggregated market depth data from Polymarket's order books.
    Returns market liquidity metrics including order book depth, unique makers, and spreads.
    """
    try:
        # Get event details
        event_response = requests.get(f"{GAMMA_API}/events/{event_id}", timeout=10)
        if event_response.status_code != 200:
            print(f"Failed to fetch event: {event_response.status_code}")
            return []
        
        event_data = event_response.json()
        markets = event_data.get('markets', [])
        
        if not markets:
            print("No markets found")
            return []
        
        # Collect aggregated market depth data
        market_depth_data = []
        
        for market_idx, market in enumerate(markets[:3]):  # Check first 3 markets
            clob_token_ids = market.get('clobTokenIds', [])
            if isinstance(clob_token_ids, str):
                clob_token_ids = json.loads(clob_token_ids)
            
            if not clob_token_ids:
                continue
            
            market_question = market.get('question', f'Market {market_idx + 1}')
            group_item_title = market.get('groupItemTitle', '')
            outcomes = json.loads(market.get('outcomes', '["Yes", "No"]'))
            
            # For multi-outcome events, use groupItemTitle as the market identifier
            display_market = group_item_title if group_item_title else market_question
            
            # For each outcome (YES and NO typically)
            for outcome_idx, token_id in enumerate(clob_token_ids[:2]):
                try:
                    book_url = f"{CLOB_API}/book"
                    params = {'token_id': token_id}
                    book_response = requests.get(book_url, params=params, timeout=10)
                    
                    if book_response.status_code == 200:
                        book_data = book_response.json()
                        bids = book_data.get('bids', [])
                        asks = book_data.get('asks', [])
                        
                        # Debug: print first order structure
                        if bids and outcome_idx == 0:
                            print(f"Sample bid order keys: {bids[0].keys() if bids else 'no bids'}")
                        
                        # Calculate aggregated metrics
                        total_bid_volume = sum(float(order.get('size', 0)) for order in bids)
                        total_ask_volume = sum(float(order.get('size', 0)) for order in asks)
                        total_bid_liquidity = sum(float(order.get('size', 0)) * float(order.get('price', 0)) for order in bids)
                        total_ask_liquidity = sum(float(order.get('size', 0)) * float(order.get('price', 0)) for order in asks)
                        
                        # Count unique makers - try different field names
                        bid_makers_set = set()
                        for order in bids:
                            maker = order.get('maker_address') or order.get('maker') or order.get('owner')
                            if maker:
                                bid_makers_set.add(maker)
                        
                        ask_makers_set = set()
                        for order in asks:
                            maker = order.get('maker_address') or order.get('maker') or order.get('owner')
                            if maker:
                                ask_makers_set.add(maker)
                        
                        unique_bid_makers = len(bid_makers_set)
                        unique_ask_makers = len(ask_makers_set)
                        
                        # Calculate depth at different price levels
                        bid_depth_5pct = sum(float(order.get('size', 0)) for order in bids[:5]) if len(bids) >= 5 else total_bid_volume
                        ask_depth_5pct = sum(float(order.get('size', 0)) for order in asks[:5]) if len(asks) >= 5 else total_ask_volume
                        
                        # Best bid/ask
                        best_bid = float(bids[0].get('price', 0)) if bids else 0
                        best_ask = float(asks[0].get('price', 0)) if asks else 0
                        spread = (best_ask - best_bid) if (best_bid and best_ask) else 0
                        
                        outcome_name = outcomes[outcome_idx] if outcome_idx < len(outcomes) else f'Outcome {outcome_idx + 1}'
                        
                        market_depth_data.append({
                            'market': display_market,
                            'outcome': outcome_name,
                            'total_bid_volume': round(total_bid_volume, 2),
                            'total_ask_volume': round(total_ask_volume, 2),
                            'total_liquidity': round(total_bid_liquidity + total_ask_liquidity, 2),
                            'unique_makers': unique_bid_makers + unique_ask_makers,
                            'bid_makers': unique_bid_makers,
                            'ask_makers': unique_ask_makers,
                            'top_5_bid_depth': round(bid_depth_5pct, 2),
                            'top_5_ask_depth': round(ask_depth_5pct, 2),
                            'best_bid': round(best_bid, 3),
                            'best_ask': round(best_ask, 3),
                            'spread': round(spread, 4),
                            'total_orders': len(bids) + len(asks),
                            'bid_orders': len(bids),
                            'ask_orders': len(asks)
                        })
                        
                        print(f"Market depth for {outcome_name}: {unique_bid_makers + unique_ask_makers} makers, ${round(total_bid_liquidity + total_ask_liquidity, 2)} liquidity")
                
                except Exception as e:
                    print(f"Error fetching book for token {token_id}: {e}")
                    continue
        
        if not market_depth_data:
            print("No market depth data found")
            return []
        
        # Sort by liquidity and return top entries
        market_depth_data.sort(key=lambda x: x['total_liquidity'], reverse=True)
        
        print(f"Found market depth data for {len(market_depth_data)} outcomes")
        return market_depth_data[:limit]
        
    except Exception as e:
        print(f"Error in get_event_smart_wallets: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_market_statistics(event_id):
    """
    This would provide additional market statistics like historical volume trends.
    Currently not implemented as it requires historical data access.
    """
    return {
        "event_id": event_id,
        "note": "Historical market statistics require additional data sources"
    }
