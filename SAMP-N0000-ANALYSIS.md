# Stock Analysis Summary for SAMP.N0000

This document demonstrates the MA50 + Breakout stock analysis for **SAMP.N0000** using the automated analyzer.

## Analysis Workflow

The `analyze.py` script implements the complete workflow as specified in the problem statement:

### 1. Get the Setup
- Checks if price is above MA50
- Verifies MA50 is sloping upward
- Identifies clear resistance level (from last 1-3 months)
- Confirms candle closed above resistance with higher volume

### 2. Entry, Stop, Target Calculation
- Entry price: Breakout level (resistance) or current price if already broken out
- Stop loss: Slightly below swing low (1% buffer)
- Risk per share: Entry - Stop
- Target: Entry + (2 × Risk per share) for 2R target

### 3. Stock Check (5 Conditions)
All five conditions must be YES:
- [ ] Price above MA50
- [ ] MA50 sloping upward
- [ ] Clear resistance level identified
- [ ] Candle closed above resistance
- [ ] Breakout volume higher than recent days

If ANY condition is NO → **SKIP THIS TRADE**

### 4. Risk Check & Position Sizing
- Risk per trade: 1% of capital
- Position size: (1% risk) ÷ (risk per share)
- Validates stop loss and 2R target

### 5. Final Verdict
Returns either:
- **VALID TRADE** with complete details (entry, stop, target, position size)
- **SKIP** with specific reason(s)

## How to Analyze SAMP.N0000

### Option 1: With All Data (Recommended)

```bash
python analyze.py SAMP.N0000 \
  --current-price 45.50 \
  --ma50 42.00 \
  --ma50-uptrend yes \
  --resistance 44.00 \
  --swing-low 40.00 \
  --breakout yes \
  --capital 100000
```

### Option 2: Interactive Mode

```bash
python analyze.py SAMP.N0000 --capital 100000
```

The script will prompt for any missing data:
- Current price
- MA50 value
- MA50 uptrend status
- Resistance level
- Breakout confirmation
- Recent swing low

### Option 3: Fetch from CSE API (if accessible)

```bash
python analyze.py SAMP.N0000 --capital 100000
```

If the CSE API is accessible, it will automatically fetch available data and only prompt for what's missing.

## Example Output

For a valid trade setup:

```
============================================================
STOCK CHECK - MA50 + Breakout System (Daily Charts)
============================================================

1. Is price above MA50?
   Current Price: 45.50
   MA50: 42.00
   Result: YES ✓

2. Is MA50 sloping upward?
   Result: YES ✓

3. Is there a clear resistance level (last 1-3 months)?
   Resistance: 44.00
   Result: YES ✓

4. Did a candle CLOSE above resistance?
   Current Price: 45.50
   Resistance: 44.00
   Result: YES ✓

5. Was breakout volume higher than recent days?
   Result: YES ✓

============================================================

All conditions met! Calculating entry, stop, and target...

============================================================
ENTRY, STOP, TARGET:
  Entry Price:     45.50 (breakout level)
  Swing Low:       40.00
  Stop Loss:       39.60 (slightly below swing low)
  Risk per Share:  5.90 (Entry - Stop)
  Target (2R):     57.30 (Entry + 2 × Risk)

============================================================
RISK CHECK & POSITION SIZING
============================================================

Capital:              100,000.00
Risk per Trade (1%):  1,000.00
Risk per Share:       5.90
Position Size:        169 shares
Position Value:       7,689.50 (7.7% of capital)
Actual Risk:          997.10 (1.00% of capital)

============================================================
FINAL VERDICT
============================================================

✓ VALID TRADE

Trade Summary:
  Symbol:        SAMP.N0000
  Entry:         45.50
  Stop Loss:     39.60
  Target (2R):   57.30
  Position Size: 169 shares
  Risk/Share:    5.90
  Max Risk:      997.10 (1.00% of capital)
  Potential Profit: 1,994.20 (2R)

Pre-Trade Checklist:
  ✓ Price above MA50
  ✓ MA50 trending up
  ✓ Breakout with strong volume
  ✓ Stop loss placed
  ✓ Risk ≤ 1% capital
  ✓ Target at least 2R

============================================================
```

## Trading Rules Applied

The analyzer strictly follows these rules from the trading guides:

1. **Timeframe**: Daily charts (1D) only
2. **Risk Management**: 1% of capital per trade maximum
3. **Target**: 2R (twice the risk) minimum
4. **Stop Loss**: Always placed below recent swing low
5. **Entry Criteria**: All 5 conditions must be met
6. **Position Sizing**: Calculated to maintain 1% risk regardless of stock price

## Next Steps

After receiving a "VALID TRADE" verdict:

1. **Review the numbers** - Confirm entry, stop, and target make sense
2. **Check your capital** - Ensure you have enough to buy the calculated position size
3. **Set orders**:
   - Entry order at the specified entry price
   - Stop loss order at the specified stop price
   - Target (limit) order at the specified target price
4. **Monitor the trade** - Follow your plan, don't move stops or targets based on emotion
5. **Journal the trade** - Record your reasoning and outcome for learning

## Important Notes

- **Never trade without a stop loss**
- **Never risk more than 1% per trade**
- **Don't chase spikes** - wait for proper setups
- **Skip bad setups** - patience is key
- **Always verify data** from official sources before trading with real money

## Data Requirements

To use this analyzer effectively for SAMP.N0000, you need:

1. **Current/Last traded price** - From CSE or your broker
2. **50-day moving average (MA50)** - Calculate from daily closing prices
3. **MA50 trend** - Is it sloping up over the last 10 days?
4. **Resistance level** - Identify from chart (last 1-3 months)
5. **Breakout confirmation** - Did last candle close above resistance with high volume?
6. **Recent swing low** - Lowest point in recent price action (for stop placement)
7. **Your trading capital** - Total amount you're willing to allocate

All calculations (entry, stop, target, position size) are derived from these inputs following the MA50 + Breakout system rules.
