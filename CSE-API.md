# Using CSE API for stock data

This project can use the **Colombo Stock Exchange (CSE)** public API to fetch data when you use a CSE symbol. That way the prompts (e.g. [analyze-stock](prompts/analyze-stock.md)) can work with real prices and chart data.

## API source

Unofficial documentation and examples:

- **Repo:** [Colombo-Stock-Exchange-CSE-API-Documentation](https://github.com/GH0STH4CKER/Colombo-Stock-Exchange-CSE-API-Documentation)
- **Base URL:** `https://www.cse.lk/api/`
- **Method:** POST for all listed endpoints

Use responsibly and verify data with [official CSE](https://www.cse.lk/) sources. The API is reverse‑engineered and may change.

## Endpoints we use

| Endpoint               | Purpose for this project                          |
|------------------------|----------------------------------------------------|
| `companyInfoSummery`   | Name, last price, change, market cap by symbol    |
| `chartData`            | Historical chart (for MA50, resistance, volume)    |
| `todaySharePrice`      | Today’s prices (optional)                         |
| `marketSummery`        | Market summary (optional)                         |

## CSE symbol format

Symbols are like `LOLC.N0000` (company code + suffix). Use the exact symbol from CSE.

## How to fetch data in this repo

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the CSE client for one symbol**
   ```bash
   python data/cse_client.py LOLC.N0000
   ```
   This prints JSON with `company` (summary) and `chart` (chart data). You can pass this to the AI along with the symbol when using the prompts.

3. **Use in prompts**
   - In [prompts/analyze-stock.md](prompts/analyze-stock.md) (and other prompts), give the **symbol** only.
   - If the AI has access to this script or to the CSE API, it can pull data for that symbol.
   - Alternatively, run `python data/cse_client.py SYMBOL` yourself and paste the output into the chat so the AI can read price, chart, and derive MA50/stop/target.

## Client API (Python)

```python
from data.cse_client import get_company_summary, get_chart_data, fetch_for_symbol, ma50_from_closes

# One symbol, all we need for the checklist
data = fetch_for_symbol("LOLC.N0000")
# data["company"]  -> companyInfoSummery response
# data["chart"]    -> chartData response (structure depends on CSE response)

# Or only summary
summary = get_company_summary("LOLC.N0000")
last_price = summary["reqSymbolInfo"]["lastTradedPrice"]
```

If `chartData` returns a list of daily closes (or OHLCV), you can compute MA50 with `ma50_from_closes(list_of_closes)`.

## Disclaimer

- The CSE API is **unofficial**. Endpoints and response formats may change.
- Always confirm important figures with official CSE sources before trading.
- This setup is for education and personal use.
