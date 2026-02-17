# Stock Check (MA50 + Breakout)

**User's only input: stock symbol.** Paste the ticker; the AI uses daily (1D) chart data to run the check and fill entry, stop, target, and position size. If the AI cannot get data, it will ask for the missing values (e.g. entry price, swing low, capital for position size).

---

**My input:**
- Symbol: SYMBOL

---

## Run the check

Using daily chart data for SYMBOL:

### 1) Is price above MA50?
YES / NO

### 2) Is MA50 sloping upward?
YES / NO

### 3) Is price near a clear resistance level?
YES / NO

### 4) Did a candle CLOSE above resistance?
YES / NO

### 5) Was breakout volume bigger than recent days?
YES / NO

### 6) Recent swing low price:
_________ (derive from chart, or ask user if needed)

### 7) Stop loss price (below swing low):
_________

### 8) Entry price (e.g. breakout level):
_________

### 9) Risk per share:
Entry − Stop Loss = _________

### 10) User's total capital:
_________ (ask only when calculating position size, or use placeholder)

### 11) 1% risk amount:
Capital × 0.01 = _________

### 12) Position size:
1% risk ÷ risk per share = ______ shares

### 13) Profit target (2R):
Entry + (2 × risk per share) = _________

---

## Result

- **If ALL conditions 1–5 are YES** → Valid trade. Use the stop loss, position size, and target above.
- **If any condition is NO** → Skip this trade.

---

*User: Replace SYMBOL with your ticker, then paste into the AI. You only provide the symbol.*
