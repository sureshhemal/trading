# Stock Trading Guide

1. **Choose a stock** → Follow [HOW-TO-CHOOSE-A-STOCK.md](./HOW-TO-CHOOSE-A-STOCK.md).
2. **You have a stock** → Use the prompts in the `prompts/` folder to decide what to do next (research, entry/exit, risk).

## Prompts

Once you have a ticker, open the right prompt in `prompts/` and paste your stock + context. The prompts will tell you what to do next.

## CSE (Colombo Stock Exchange) data

For CSE symbols, this repo can fetch data from the [unofficial CSE API](https://github.com/GH0STH4CKER/Colombo-Stock-Exchange-CSE-API-Documentation). See [CSE-API.md](./CSE-API.md) and run `python data/cse_client.py SYMBOL` to grab company info and chart data for the MA50 + Breakout checks.
