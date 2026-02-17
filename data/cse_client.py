"""
Colombo Stock Exchange (CSE) API client for the MA50 + Breakout system.

Uses the unofficial CSE API documented at:
https://github.com/GH0STH4CKER/Colombo-Stock-Exchange-CSE-API-Documentation

Data is for daily (1D) charts. Verify with official CSE sources.
"""

import requests
from typing import Any, Dict, List, Optional

BASE_URL = "https://www.cse.lk/api/"


def _post(endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """POST to a CSE API endpoint. Returns JSON or raises."""
    url = BASE_URL.rstrip("/") + "/" + endpoint.lstrip("/")
    payload = data or {}
    resp = requests.post(url, data=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def get_company_summary(symbol: str) -> Dict[str, Any]:
    """
    Get detailed info for a single stock by symbol.

    Example: get_company_summary("LOLC.N0000")
    Returns: reqSymbolInfo (name, lastTradedPrice, change, changePercentage, marketCap), etc.
    """
    return _post("companyInfoSummery", {"symbol": symbol})


def get_chart_data(symbol: str, period: int = 1, chart_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Get chart data for a stock. period=1 typically means daily.

    Args:
        symbol: CSE symbol (e.g. LOLC.N0000)
        period: 1 = daily (adjust if API uses different convention)
        chart_id: optional, if required by API
    """
    data: Dict[str, Any] = {"symbol": symbol, "period": period}
    if chart_id is not None:
        data["chartId"] = chart_id
    return _post("chartData", data)


def get_today_prices() -> Dict[str, Any]:
    """Today's share price data for all securities."""
    return _post("todaySharePrice")


def get_market_summary() -> Dict[str, Any]:
    """Market summary data."""
    return _post("marketSummery")


def fetch_for_symbol(symbol: str) -> Dict[str, Any]:
    """
    Fetch all data needed for the MA50 + Breakout checklist for one symbol.

    Returns a dict with:
      - company: result of companyInfoSummery (name, lastTradedPrice, etc.)
      - chart: result of chartData if available (CSE may require chartId; see CSE-API.md)
    """
    company = get_company_summary(symbol)
    chart = {}
    try:
        chart = get_chart_data(symbol)
    except requests.HTTPError:
        pass  # chartData may require chartId or different params; company data is still useful
    return {"symbol": symbol, "company": company, "chart": chart}


def ma50_from_closes(closes: List[float]) -> Optional[float]:
    """
    Compute 50-period simple moving average from a list of closing prices (oldest first).

    Returns None if fewer than 50 points.
    """
    if len(closes) < 50:
        return None
    return sum(closes[-50:]) / 50


if __name__ == "__main__":
    import sys
    import json

    symbol = sys.argv[1] if len(sys.argv) > 1 else "LOLC.N0000"
    try:
        out = fetch_for_symbol(symbol)
        print(json.dumps(out, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
