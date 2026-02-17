# Entry & Exit Plan (MA50 + Breakout)

**User's only input: stock symbol.** Paste the ticker; the AI uses daily (1D) chart data to identify entry (breakout level), swing low, stop, and 2R target. If the AI cannot get data, it will ask for the specific values needed.

We use **daily charts (1D)** only; decisions after market close.

---

**My input:**
- Symbol: SYMBOL

---

## Entry

Enter only when **all** are true (derive from daily chart for SYMBOL):

1. Price **above MA50**
2. MA50 **sloping upward**
3. Price near a **clear resistance level** (use last 1–3 months of data)
4. A candle **closes above resistance**
5. Breakout candle has **higher volume than recent days**

If any is missing → no trade. Wait for the next setup.

**Entry price:** _________ (e.g. breakout level — from chart or ask if needed)

---

## Exit — Stop loss

- Find the **recent swing low** (below current price) from the chart.
- Place stop **slightly below** that swing low.

- Swing low price: _________
- Stop loss price: _________

If price hits stop → exit without hesitation.

---

## Exit — Profit target (2R)

- **Risk per share** = Entry − Stop loss = _________
- **Target** = Entry + (2 × Risk per share) = _________

---

## Summary

|        | Price  |
|--------|--------|
| Entry  | _______ |
| Stop   | _______ |
| Target | _______ |
| Risk/share | _______ |

---

*User: Replace SYMBOL with your ticker, then paste into the AI. You only provide the symbol.*
