# CSE MA50 Breakout Scanner

Run the [scanner](cse-scanner.html) via `python3 serve-scanner.py` then open **http://127.0.0.1:8765/** — and follow the system rules below.

---

# CSE MA50 Breakout System — Transcript

*Source: User conversation (CSE MA50 Breakout system).*

---

## CORE STRATEGY

**Goal:**  
Trade trend-following breakouts on CSE stocks using MA50 + volume + risk control.

**Timeframe:**  
Daily (1D) only.

---

## SYSTEM RULES

### 1) TREND FILTER

- Price > MA50  
- MA50 sloping upward  

If false → **SKIP** stock.

---

### 2) RESISTANCE

- Find clear resistance from previous highs.  
- Use last 2–3 months data.  
- **DO NOT** include today’s candle in resistance calc.

---

### 3) BREAKOUT TRIGGER

Valid breakout when:

- **Close > resistance** (body close, not wick).  
- Breakout must be **recent** (last 1–3 candles).

---

### 4) VOLUME CONFIRMATION

- Breakout candle volume **>** average volume (last 20 days).  
- **Exclude today** from average calculation.

---

### 5) AVOID EXTENDED MOVES

Do not buy if price is too far above MA50.

**Rule:**  
(Price − MA50) / MA50 ≤ ~10–15%

Prevents chasing spikes.

---

### 6) ENTRY

- **Entry** = breakout close (or next day open).

---

### 7) STOP LOSS

- **Stop** = below recent swing low (last ~15 days).  
- Add small buffer.  
- Stop protects capital.

---

### 8) RISK PER SHARE

**Risk/share** = Entry − Stop

---

### 9) POSITION SIZING

- Max risk per trade = **1% of capital**.  

**Position size:**  
(1% capital) / risk per share

---

### 10) PROFIT TARGET

**Target** = Entry + 2 × risk per share **(2R)**

---

## SCANNER LOGIC

**BUY** when:

- Price > MA50  
- MA50 rising  
- Fresh breakout  
- Volume spike  
- Not extended  

**WATCH** when:

- Trend ok  
- Near resistance  
- No breakout yet  

**SKIP** when:

- Below MA50  
- No trend  
- Overextended  
- No volume  

---

## IMPORTANT NOTES

- **Score** column = ranking only.  
- **Decision** column = action.  

- Never chase vertical candles.  
- Never trade without stop loss.  
- Patience > frequency.  

- Expect **1–2 good trades per week**, not daily.  

- Trading = **probability**, not prediction.
