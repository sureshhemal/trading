# Usage Examples for analyze.py

The `analyze.py` script implements the MA50 + Breakout system workflow as described in the trading guides.

## Basic Usage

### Example 1: SAMP.N0000 - Valid Trade Scenario

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

**Output:**
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

### Example 2: SAMP.N0000 - Failed Trade (Price Below MA50)

```bash
python analyze.py SAMP.N0000 \
  --current-price 40.00 \
  --ma50 42.00 \
  --ma50-uptrend yes \
  --resistance 44.00 \
  --swing-low 38.00 \
  --breakout no \
  --capital 100000
```

**Output:**
```
============================================================
STOCK CHECK - MA50 + Breakout System (Daily Charts)
============================================================

1. Is price above MA50?
   Current Price: 40.00
   MA50: 42.00
   Result: NO ✗

2. Is MA50 sloping upward?
   Result: YES ✓

3. Is there a clear resistance level (last 1-3 months)?
   Resistance: 44.00
   Result: YES ✓

4. Did a candle CLOSE above resistance?
   Current Price: 40.00
   Resistance: 44.00
   Result: NO ✗

5. Was breakout volume higher than recent days?
   Result: NO ✗

============================================================

VERDICT: SKIP THIS TRADE
Reason: Failed conditions: Price not above MA50, No breakout above resistance, No volume confirmation
============================================================
```

### Example 3: Interactive Mode

If you don't have all the data, run with just the symbol:

```bash
python analyze.py SAMP.N0000 --capital 100000
```

The script will prompt you for each missing value:
```
Attempting to fetch data for SAMP.N0000 from CSE API...
Could not fetch data from API: ...
Enter current price for SAMP.N0000: 45.50
Enter MA50 value for SAMP.N0000: 42.00
Enter recent resistance level for SAMP.N0000 (from last 1-3 months): 44.00
Did the last candle close above 44.00 with higher volume than recent days? (yes/no): yes
Enter recent swing low price (below current price 45.50): 40.00

2. Is MA50 sloping upward? (yes/no): yes
```

## Command-Line Options

```
usage: analyze.py [-h] [--capital CAPITAL] [--current-price CURRENT_PRICE]
                  [--ma50 MA50] [--ma50-uptrend {yes,no}]
                  [--resistance RESISTANCE] [--swing-low SWING_LOW]
                  [--breakout {yes,no}]
                  symbol

positional arguments:
  symbol                Stock symbol (e.g., SAMP.N0000, AAPL)

options:
  -h, --help            show this help message and exit
  --capital CAPITAL     Total trading capital (default: 100000)
  --current-price CURRENT_PRICE
                        Current price (optional)
  --ma50 MA50           MA50 value (optional)
  --ma50-uptrend {yes,no}
                        MA50 sloping upward (optional)
  --resistance RESISTANCE
                        Resistance level (optional)
  --swing-low SWING_LOW
                        Recent swing low (optional)
  --breakout {yes,no}   Breakout confirmed (optional)
```

## Workflow

The script follows the exact workflow described in the problem statement:

1. **Get the setup** — Checks if price is above MA50, MA50 is sloping up, there's clear resistance, and breakout occurred with higher volume.

2. **Entry, stop, target** — Identifies entry price (breakout level), recent swing low, stop loss (slightly below swing low), and calculates risk per share and 2R target.

3. **Stock check** — Evaluates all 5 entry conditions (YES/NO). If any is NO, outputs "Skip this trade" and stops.

4. **Risk check** — Calculates 1% risk amount, position size in shares, and confirms stop loss and 2R target are set.

5. **Result** — Gives clear verdict: **Valid trade** (with all details) or **Skip** (with reason).

## Data Sources

The script attempts to fetch data from the CSE API (for CSE symbols like SAMP.N0000). If the API is not accessible or you're analyzing non-CSE stocks, you can:

1. Provide all data via command-line options (see Example 1)
2. Let the script prompt you interactively (see Example 3)
3. Provide partial data and be prompted for the rest

## Exit Codes

- `0` - Valid trade found
- `1` - Trade should be skipped (conditions not met or missing data)
