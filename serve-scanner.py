#!/usr/bin/env python3
"""
Local server for CSE Scanner — avoids CORS and fetches daily chart data.
CSE chartData returns []; we use companyInfoSummery (symbol -> id) then
companyChartDataByStock (stockId, period=5) for daily bars and normalize to
{ data: [{ close, high, low, volume }, ...] }.
Run: python3 serve-scanner.py
Then open: http://127.0.0.1:8765/
"""
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
import json
import os

PORT = 8765
CSE_BASE = "https://www.cse.lk/api/"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(SCRIPT_DIR, "cse-scanner.html")


def cse_post(endpoint, data):
    req = urllib.request.Request(
        CSE_BASE + endpoint,
        data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def fetch_chart_data(symbol):
    """Resolve symbol -> stockId, fetch daily chart (period=5), return { data: [...] }."""
    summary = cse_post("companyInfoSummery", {"symbol": symbol})
    info = summary.get("reqSymbolInfo") or {}
    stock_id = info.get("id")
    if stock_id is None:
        return {"data": []}
    chart = cse_post("companyChartDataByStock", {"stockId": stock_id, "period": "5"})
    raw = chart.get("chartData") or []
    # CSE: h=high, l=low, p=close, q=volume. Scanner expects close, high, low, volume.
    rows = [
        {"close": r.get("p"), "high": r.get("h"), "low": r.get("l"), "volume": r.get("q")}
        for r in raw
    ]
    return {"data": rows}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print("[%s] %s" % (self.log_date_time_string(), format % args))

    def do_GET(self):
        if self.path in ("/", "/index.html", "/cse-scanner.html"):
            self.serve_html()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/api/chartData":
            self.proxy_chart()
        else:
            self.send_error(404)

    def serve_html(self):
        try:
            with open(HTML_PATH, "rb") as f:
                data = f.read()
        except FileNotFoundError:
            self.send_error(404, "cse-scanner.html not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def proxy_chart(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        try:
            params = parse_qs(body.decode(), keep_blank_values=True)
            symbol = (params.get("symbol") or [None])[0]
            if not symbol:
                out = {"data": [], "error": "missing symbol"}
            else:
                out = fetch_chart_data(symbol)
        except urllib.error.HTTPError as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e.code)}).encode())
            return
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
        resp_body = json.dumps(out).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(resp_body))
        self.end_headers()
        self.wfile.write(resp_body)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle each request in a new thread so Promise.all() fetches run in parallel."""
    pass


def main():
    server = ThreadedHTTPServer(("127.0.0.1", PORT), Handler)
    print("CSE Scanner server: http://127.0.0.1:%s/" % PORT)
    print("Open that URL in your browser to avoid CORS.")
    server.serve_forever()


if __name__ == "__main__":
    main()
