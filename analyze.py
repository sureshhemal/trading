#!/usr/bin/env python3
"""
MA50 + Breakout Stock Analyzer

Analyzes a stock symbol using the MA50 + Breakout system for daily (1D) charts.
Follows the workflow from stock-check.md, entry-exit-plan.md, and risk-check.md.

Usage:
    python analyze.py SYMBOL [--capital AMOUNT]
    
Example:
    python analyze.py SAMP.N0000 --capital 100000
"""

import sys
import argparse
from typing import Dict, List, Optional, Tuple
from data.cse_client import fetch_for_symbol, ma50_from_closes

# Trading system parameters
STOP_LOSS_BUFFER = 0.99  # Place stop 1% below swing low for safety margin
TARGET_MULTIPLIER = 2    # 2R (risk-to-reward ratio) target
RISK_PER_TRADE = 0.01    # Risk 1% of capital per trade


def calculate_ma50_slope(closes: List[float], ma50_window: int = 50) -> Optional[bool]:
    """
    Determine if MA50 is sloping upward.
    
    Returns:
        True if MA50 is trending up, False if down/flat, None if insufficient data
    """
    if len(closes) < ma50_window + 10:  # Need extra data to calculate slope
        return None
    
    # Calculate MA50 for last 10 days to determine slope
    ma50_values = []
    for i in range(10):
        idx = -(10 - i)
        window_closes = closes[idx - ma50_window:idx] if idx != 0 else closes[-ma50_window:]
        if len(window_closes) >= ma50_window:
            ma50_values.append(sum(window_closes) / ma50_window)
    
    if len(ma50_values) < 2:
        return None
    
    # Check if generally trending up (compare recent vs older MA50)
    recent_avg = sum(ma50_values[-3:]) / 3
    older_avg = sum(ma50_values[:3]) / 3
    
    return recent_avg > older_avg


def find_resistance_level(highs: List[float], lookback_days: int = 60) -> Optional[float]:
    """
    Find resistance level from recent highs (last 1-3 months).
    
    Returns:
        Resistance price level or None if cannot determine
    """
    if len(highs) < lookback_days:
        lookback_days = len(highs)
    
    if lookback_days < 20:  # Need at least 20 days
        return None
    
    recent_highs = highs[-lookback_days:]
    
    # Find significant resistance: recent peak that price tested multiple times
    max_high = max(recent_highs)
    
    # Look for levels near the max that were tested 2+ times
    tolerance = max_high * 0.02  # 2% tolerance
    
    # Count touches near the max high
    touches = sum(1 for h in recent_highs if abs(h - max_high) <= tolerance)
    
    if touches >= 2:
        return max_high
    
    return None


def find_swing_low(lows: List[float], current_price: float, lookback: int = 20) -> Optional[float]:
    """
    Find recent swing low below current price.
    
    Returns:
        Swing low price or None if cannot determine
    """
    if len(lows) < lookback:
        lookback = len(lows)
    
    if lookback < 5:
        return None
    
    recent_lows = lows[-lookback:]
    
    # Find the lowest low in recent period that's below current price
    valid_lows = [low for low in recent_lows if low < current_price]
    
    if not valid_lows:
        return None
    
    return min(valid_lows)


def check_breakout_volume(volumes: List[float], breakout_idx: int = -1) -> bool:
    """
    Check if breakout candle has higher volume than recent days.
    
    Args:
        volumes: List of volume data
        breakout_idx: Index of breakout candle (default -1 for most recent)
    
    Returns:
        True if breakout volume is higher than recent average
    """
    if len(volumes) < 10:
        return False
    
    breakout_volume = volumes[breakout_idx]
    
    # Compare with average of previous 5-10 days
    if breakout_idx == -1:
        recent_volumes = volumes[-10:-1]
    else:
        recent_volumes = volumes[max(0, breakout_idx-10):breakout_idx]
    
    if not recent_volumes:
        return False
    
    avg_volume = sum(recent_volumes) / len(recent_volumes)
    
    return breakout_volume > avg_volume


def analyze_stock(
    symbol: str,
    current_price: Optional[float] = None,
    ma50_value: Optional[float] = None,
    ma50_uptrend: Optional[bool] = None,
    resistance_level: Optional[float] = None,
    breakout_confirmed: Optional[bool] = None,
    swing_low: Optional[float] = None,
    capital: float = 100000
) -> Dict:
    """
    Main analysis function following the MA50 + Breakout workflow.
    
    Args:
        symbol: Stock symbol (e.g., SAMP.N0000)
        current_price: Current/last traded price (if known)
        ma50_value: MA50 value (if known)
        ma50_uptrend: Whether MA50 is sloping upward (if known)
        resistance_level: Resistance level (if known)
        breakout_confirmed: Whether breakout with volume is confirmed
        swing_low: Recent swing low price (if known)
        capital: Total trading capital for position sizing
    
    Returns:
        Dictionary with analysis results
    """
    result = {
        'symbol': symbol,
        'setup_valid': False,
        'conditions': {},
        'prices': {},
        'position': {},
        'verdict': '',
        'reason': ''
    }
    
    # Try to fetch data from API if parameters not provided
    data_from_api = False
    closes, highs, lows, volumes = [], [], [], []
    
    if any(x is None for x in [current_price, ma50_value, resistance_level]):
        try:
            print(f"Attempting to fetch data for {symbol} from CSE API...")
            api_data = fetch_for_symbol(symbol)
            # Parse API data (structure depends on actual CSE response)
            # This is a placeholder - actual implementation depends on API response format
            if api_data and 'company' in api_data:
                company_info = api_data.get('company', {}).get('reqSymbolInfo', {})
                if 'lastTradedPrice' in company_info and current_price is None:
                    current_price = float(company_info['lastTradedPrice'])
                    data_from_api = True
            
            # If chart data available, extract OHLCV
            if api_data and 'chart' in api_data and api_data['chart']:
                # Parse chart data (format depends on API)
                # This is placeholder logic
                pass
                
        except Exception as e:
            print(f"Could not fetch data from API: {e}")
    
    # If still missing data, ask user
    if current_price is None:
        try:
            current_price = float(input(f"Enter current price for {symbol}: "))
        except (ValueError, EOFError):
            result['verdict'] = 'SKIP'
            result['reason'] = 'Missing current price data'
            return result
    
    if ma50_value is None:
        try:
            ma50_value = float(input(f"Enter MA50 value for {symbol}: "))
        except (ValueError, EOFError):
            result['verdict'] = 'SKIP'
            result['reason'] = 'Missing MA50 data'
            return result
    
    if resistance_level is None:
        try:
            resistance_level = float(input(f"Enter recent resistance level for {symbol} (from last 1-3 months): "))
        except (ValueError, EOFError):
            result['verdict'] = 'SKIP'
            result['reason'] = 'Missing resistance level'
            return result
    
    if breakout_confirmed is None:
        try:
            answer = input(f"Did the last candle close above {resistance_level} with higher volume than recent days? (yes/no): ").strip().lower()
            breakout_confirmed = answer in ['yes', 'y']
        except EOFError:
            result['verdict'] = 'SKIP'
            result['reason'] = 'Missing breakout confirmation'
            return result
    
    if swing_low is None:
        try:
            swing_low = float(input(f"Enter recent swing low price (below current price {current_price}): "))
        except (ValueError, EOFError):
            result['verdict'] = 'SKIP'
            result['reason'] = 'Missing swing low data'
            return result
    
    # Store prices
    result['prices']['current'] = current_price
    result['prices']['ma50'] = ma50_value
    result['prices']['resistance'] = resistance_level
    result['prices']['swing_low'] = swing_low
    
    # === STOCK CHECK: 5 CONDITIONS ===
    print("\n" + "="*60)
    print("STOCK CHECK - MA50 + Breakout System (Daily Charts)")
    print("="*60)
    
    # 1. Is price above MA50?
    condition1 = current_price > ma50_value
    result['conditions']['price_above_ma50'] = condition1
    print(f"\n1. Is price above MA50?")
    print(f"   Current Price: {current_price:.2f}")
    print(f"   MA50: {ma50_value:.2f}")
    result_text = f"   Result: YES ✓" if condition1 else f"   Result: NO ✗"
    print(result_text)
    
    # 2. Is MA50 sloping upward?
    # If we have historical data, calculate; otherwise use provided value or ask user
    if ma50_uptrend is not None:
        condition2 = ma50_uptrend
    elif closes and len(closes) >= 60:
        condition2 = calculate_ma50_slope(closes)
    else:
        try:
            answer = input("\n2. Is MA50 sloping upward? (yes/no): ").strip().lower()
            condition2 = answer in ['yes', 'y']
        except EOFError:
            condition2 = False
    
    result['conditions']['ma50_uptrend'] = condition2
    print(f"\n2. Is MA50 sloping upward?")
    print(f"   Result: {'YES ✓' if condition2 else 'NO ✗'}")
    
    # 3. Is there a clear resistance level?
    condition3 = resistance_level is not None and resistance_level > 0
    result['conditions']['clear_resistance'] = condition3
    print(f"\n3. Is there a clear resistance level (last 1-3 months)?")
    print(f"   Resistance: {resistance_level:.2f}")
    print(f"   Result: {'YES ✓' if condition3 else 'NO ✗'}")
    
    # 4. Did candle close above resistance?
    condition4 = current_price > resistance_level
    result['conditions']['breakout_close'] = condition4
    print(f"\n4. Did a candle CLOSE above resistance?")
    print(f"   Current Price: {current_price:.2f}")
    print(f"   Resistance: {resistance_level:.2f}")
    print(f"   Result: {'YES ✓' if condition4 else 'NO ✗'}")
    
    # 5. Higher volume on breakout?
    condition5 = breakout_confirmed
    result['conditions']['volume_confirmation'] = condition5
    print(f"\n5. Was breakout volume higher than recent days?")
    print(f"   Result: {'YES ✓' if condition5 else 'NO ✗'}")
    
    # Check if all conditions met
    all_conditions = [condition1, condition2, condition3, condition4, condition5]
    setup_valid = all(all_conditions)
    result['setup_valid'] = setup_valid
    
    print("\n" + "="*60)
    if not setup_valid:
        failed_conditions = []
        if not condition1:
            failed_conditions.append("Price not above MA50")
        if not condition2:
            failed_conditions.append("MA50 not sloping up")
        if not condition3:
            failed_conditions.append("No clear resistance")
        if not condition4:
            failed_conditions.append("No breakout above resistance")
        if not condition5:
            failed_conditions.append("No volume confirmation")
        
        result['verdict'] = 'SKIP'
        result['reason'] = f"Failed conditions: {', '.join(failed_conditions)}"
        print(f"\nVERDICT: SKIP THIS TRADE")
        print(f"Reason: {result['reason']}")
        print("="*60)
        return result
    
    # === ENTRY, STOP, TARGET ===
    print("\nAll conditions met! Calculating entry, stop, and target...")
    print("="*60)
    
    # Entry price (breakout level or current price)
    entry_price = max(current_price, resistance_level)
    result['prices']['entry'] = entry_price
    
    # Stop loss (slightly below swing low for safety margin)
    stop_loss = swing_low * STOP_LOSS_BUFFER
    result['prices']['stop'] = stop_loss
    
    # Risk per share
    risk_per_share = entry_price - stop_loss
    result['prices']['risk_per_share'] = risk_per_share
    
    # Target (2R - twice the risk per share)
    target_price = entry_price + (TARGET_MULTIPLIER * risk_per_share)
    result['prices']['target'] = target_price
    
    print(f"\nENTRY, STOP, TARGET:")
    print(f"  Entry Price:     {entry_price:.2f} (breakout level)")
    print(f"  Swing Low:       {swing_low:.2f}")
    print(f"  Stop Loss:       {stop_loss:.2f} (slightly below swing low)")
    print(f"  Risk per Share:  {risk_per_share:.2f} (Entry - Stop)")
    print(f"  Target (2R):     {target_price:.2f} (Entry + 2 × Risk)")
    
    # === RISK CHECK & POSITION SIZING ===
    print("\n" + "="*60)
    print("RISK CHECK & POSITION SIZING")
    print("="*60)
    
    # 1% risk amount
    risk_amount = capital * RISK_PER_TRADE
    result['position']['capital'] = capital
    result['position']['risk_amount'] = risk_amount
    
    # Position size in shares
    position_size = int(risk_amount / risk_per_share)  # Round down
    result['position']['shares'] = position_size
    
    # Total position value
    position_value = position_size * entry_price
    result['position']['value'] = position_value
    
    # Actual risk (accounting for rounding)
    actual_risk = position_size * risk_per_share
    result['position']['actual_risk'] = actual_risk
    
    print(f"\nCapital:              {capital:,.2f}")
    print(f"Risk per Trade (1%):  {risk_amount:,.2f}")
    print(f"Risk per Share:       {risk_per_share:.2f}")
    print(f"Position Size:        {position_size:,} shares")
    print(f"Position Value:       {position_value:,.2f} ({(position_value/capital)*100:.1f}% of capital)")
    print(f"Actual Risk:          {actual_risk:,.2f} ({(actual_risk/capital)*100:.2f}% of capital)")
    
    # === FINAL VERDICT ===
    print("\n" + "="*60)
    print("FINAL VERDICT")
    print("="*60)
    
    result['verdict'] = 'VALID TRADE'
    result['reason'] = 'All conditions met'
    
    print(f"\n✓ VALID TRADE")
    print(f"\nTrade Summary:")
    print(f"  Symbol:        {symbol}")
    print(f"  Entry:         {entry_price:.2f}")
    print(f"  Stop Loss:     {stop_loss:.2f}")
    print(f"  Target (2R):   {target_price:.2f}")
    print(f"  Position Size: {position_size:,} shares")
    print(f"  Risk/Share:    {risk_per_share:.2f}")
    print(f"  Max Risk:      {actual_risk:,.2f} ({(actual_risk/capital)*100:.2f}% of capital)")
    print(f"  Potential Profit: {position_size * 2 * risk_per_share:,.2f} (2R)")
    
    print("\nPre-Trade Checklist:")
    print("  ✓ Price above MA50")
    print("  ✓ MA50 trending up")
    print("  ✓ Breakout with strong volume")
    print("  ✓ Stop loss placed")
    print("  ✓ Risk ≤ 1% capital")
    print("  ✓ Target at least 2R")
    
    print("\n" + "="*60)
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Analyze a stock using MA50 + Breakout system (daily charts)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python analyze.py SAMP.N0000
  python analyze.py SAMP.N0000 --capital 100000
  python analyze.py AAPL --capital 50000

The script will attempt to fetch data from the CSE API.
If data is not available, you will be prompted to enter:
  - Current price
  - MA50 value
  - Recent resistance level
  - Breakout confirmation (yes/no)
  - Recent swing low price
        '''
    )
    
    parser.add_argument('symbol', help='Stock symbol (e.g., SAMP.N0000, AAPL)')
    parser.add_argument('--capital', type=float, default=100000,
                        help='Total trading capital (default: 100000)')
    parser.add_argument('--current-price', type=float, help='Current price (optional)')
    parser.add_argument('--ma50', type=float, help='MA50 value (optional)')
    parser.add_argument('--ma50-uptrend', choices=['yes', 'no'], help='MA50 sloping upward (optional)')
    parser.add_argument('--resistance', type=float, help='Resistance level (optional)')
    parser.add_argument('--swing-low', type=float, help='Recent swing low (optional)')
    parser.add_argument('--breakout', choices=['yes', 'no'], help='Breakout confirmed (optional)')
    
    args = parser.parse_args()
    
    # Convert yes/no to boolean if provided
    breakout_confirmed = None
    if args.breakout:
        breakout_confirmed = args.breakout == 'yes'
    
    ma50_uptrend = None
    if args.ma50_uptrend:
        ma50_uptrend = args.ma50_uptrend == 'yes'
    
    # Run analysis
    result = analyze_stock(
        symbol=args.symbol,
        current_price=args.current_price,
        ma50_value=args.ma50,
        ma50_uptrend=ma50_uptrend,
        resistance_level=args.resistance,
        breakout_confirmed=breakout_confirmed,
        swing_low=args.swing_low,
        capital=args.capital
    )
    
    # Exit with appropriate code
    sys.exit(0 if result['verdict'] == 'VALID TRADE' else 1)


if __name__ == '__main__':
    main()
