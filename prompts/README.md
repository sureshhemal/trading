# Prompts — What to do after you pick a stock

We use the **MA50 + Breakout system** on **daily charts** (see [HOW-TO-CHOOSE-A-STOCK.md](../HOW-TO-CHOOSE-A-STOCK.md)).

---

## Prompt to copy (symbol only)

| File | What to do |
|------|------------|
| **[COPY-THIS-PROMPT.md](./COPY-THIS-PROMPT.md)** | **Copy the entire file** into your AI chat. Replace `SYMBOL` with your ticker (e.g. `LOLC.N0000`, `AAPL`), then send. |
| [analyze-stock.md](./analyze-stock.md) | Same prompt with instructions at the top; copy the block below the first `---`. |

Your only input = stock symbol. The AI returns **Valid trade** (entry, stop, target, position size) or **Skip** (with reason).

---

## Other prompt files

| Prompt | Use when |
|--------|----------|
| **`analyze-stock.md`** | One-shot: paste symbol only. AI runs full workflow (setup → entry/stop/target → stock check → risk check) and returns Valid trade or Skip. |
| **`stock-check.md`** | Run the full checklist from symbol only: 5 conditions, swing low, stop, position size (1%), 2R target. AI fills from chart or asks if needed. |
| **`entry-exit-plan.md`** | Plan entry, stop (below swing low), and 2R target from symbol only. Daily charts. |
| **`risk-check.md`** | Before placing: confirm risk per share, 1% risk, position size. Input: symbol only; AI uses entry/stop from setup or asks. Asks for capital when needed for position size. |

---

## How to use

1. Copy the prompt file you need into your AI chat.
2. Replace `SYMBOL` (or the ticker placeholder) with your stock symbol.
3. The AI does the rest; it will ask for capital or specific numbers only when necessary.

## Data for CSE symbols (Colombo Stock Exchange)

For **CSE symbols** (e.g. `LOLC.N0000`), you can pull real data from the CSE API so the AI has prices and chart data:

- See **[CSE-API.md](../CSE-API.md)** for the API overview and how this repo uses it.
- Run `python data/cse_client.py SYMBOL` to fetch company summary and chart data; paste the output into the chat if the AI cannot call the API itself.
- API source: [Colombo-Stock-Exchange-CSE-API-Documentation](https://github.com/GH0STH4CKER/Colombo-Stock-Exchange-CSE-API-Documentation) (unofficial).
