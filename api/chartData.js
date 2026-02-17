const CSE_BASE = "https://www.cse.lk/api/";

async function csePost(endpoint, data) {
  const body = new URLSearchParams(data).toString();
  const res = await fetch(CSE_BASE + endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!res.ok) throw new Error(`CSE ${endpoint}: ${res.status}`);
  return res.json();
}

async function fetchChartData(symbol) {
  const summary = await csePost("companyInfoSummery", { symbol });
  const info = summary.reqSymbolInfo || {};
  const stockId = info.id;
  if (stockId == null) return { data: [] };
  const chart = await csePost("companyChartDataByStock", { stockId, period: "5" });
  const raw = chart.chartData || [];
  const rows = raw.map((r) => ({
    close: r.p,
    high: r.h,
    low: r.l,
    volume: r.q,
  }));
  return { data: rows };
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("end", () => resolve(Buffer.concat(chunks).toString()));
    req.on("error", reject);
  });
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const body = await parseBody(req);
    const params = new URLSearchParams(body);
    const symbol = params.get("symbol");
    if (!symbol) {
      return res.status(200).json({ data: [], error: "missing symbol" });
    }
    const out = await fetchChartData(symbol);
    return res.status(200).json(out);
  } catch (e) {
    return res.status(502).json({ error: String(e.message || e) });
  }
}
