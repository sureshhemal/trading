# Stock Trading Guide

1. **Choose a stock** → Follow [HOW-TO-CHOOSE-A-STOCK.md](./HOW-TO-CHOOSE-A-STOCK.md).
2. **You have a stock** → Use the prompts in the `prompts/` folder to decide what to do next (research, entry/exit, risk).
3. **Automated analysis** → Use `analyze.py` to run the full MA50 + Breakout analysis workflow.

## Quick Start: Analyze a Stock

To analyze a stock using the MA50 + Breakout system:

```bash
python analyze.py SYMBOL [--capital AMOUNT] [options]
```

### Example Analysis: SAMP.N0000

See [SAMP-N0000-ANALYSIS.md](./SAMP-N0000-ANALYSIS.md) for a complete walkthrough of analyzing SAMP.N0000.

### Example with all data provided:
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

### Example with interactive prompts:
If you don't provide all parameters, the script will prompt you for missing data:
```bash
python analyze.py SAMP.N0000 --capital 100000
```

The script will output:
- **Valid trade** with entry, stop, target, position size, and risk details
- **Skip** with specific reasons if any condition fails

For more examples, see [EXAMPLES.md](./EXAMPLES.md).

## Prompts

Once you have a ticker, open the right prompt in `prompts/` and paste your stock + context. The prompts will tell you what to do next.

## CSE (Colombo Stock Exchange) data

For CSE symbols, this repo can fetch data from the [unofficial CSE API](https://github.com/GH0STH4CKER/Colombo-Stock-Exchange-CSE-API-Documentation). See [CSE-API.md](./CSE-API.md) and run `python data/cse_client.py SYMBOL` to grab company info and chart data for the MA50 + Breakout checks.
