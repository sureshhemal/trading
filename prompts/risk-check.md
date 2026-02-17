# Risk Check (Before Placing the Trade)

**User's only input: stock symbol.** The AI uses daily chart data to get entry and stop (from the MA50 + breakout setup, or from the prior entry-exit plan). For position size, the AI asks for the user's capital only when needed, or uses a placeholder (e.g. 100,000) and shows the formula so the user can plug in their number.

We risk **1% of capital per trade** and always use a stop loss.

---

**My input:**
- Symbol: SYMBOL

---

## 1) Entry and stop (from setup)

- Entry price: _________ (from chart / breakout level)
- Stop loss price: _________ (below recent swing low)

(If you cannot get these from data, ask the user.)

---

## 2) Risk per share

**Formula:** Entry − Stop loss = Risk per share

_________ − _________ = _________

---

## 3) 1% risk amount

**Formula:** Capital × 0.01 = 1% risk in currency

Ask for the user's total capital only when needed for this step, or use a placeholder and show: _________ × 0.01 = _________

---

## 4) Position size (shares)

**Formula:** 1% risk ÷ Risk per share = Number of shares

_________ ÷ _________ = ______ shares

(Round down to whole shares if needed.)

---

## 5) Pre-trade checklist

- [ ] Stop loss is placed (slightly below recent swing low)
- [ ] Risk per trade ≤ 1% of capital
- [ ] Position size matches the formula above
- [ ] Profit target is at least 2R (Entry + 2 × Risk per share)

All checked → okay to place the trade within your plan.  
Any unchecked → fix before placing.

---

## Golden rules (reminder)

- Never trade without a stop loss
- Never risk more than 1% per trade
- Don't chase spikes; skip bad setups

---

*User: Replace SYMBOL with your ticker, then paste into the AI. You only provide the symbol.*
