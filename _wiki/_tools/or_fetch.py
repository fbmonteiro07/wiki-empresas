r"""
or_fetch.py — pull OpenRouter's PUBLIC (unauthenticated) endpoints and cache the
raw JSON under _wiki/_data/openrouter/raw/<YYYY-MM-DD>/.

Pure stdlib. The machine sits behind a TLS proxy that breaks cert verification
(same reason pip fails), so we use an unverified SSL context. Every endpoint hit
here is public read-only data (the same JSON that powers openrouter.ai/rankings).

Endpoints captured:
  models     GET /api/v1/models                          per-token pricing, modality, context
  catalog    GET /api/frontend/v1/catalog/models         author/name/modality per permaslug
  providers  GET /api/frontend/v1/all-providers          provider metadata
  rank_week  GET /api/frontend/v1/rankings/models?view=week    trailing-7d tokens per model
  rank_month GET /api/frontend/v1/rankings/models?view=month   trailing-30d tokens per model
  apps       GET /api/frontend/v1/rankings/apps?view=week       trailing day/week/month per app

Run:  py "E:\Wiki Felipe empresas\_wiki\_tools\or_fetch.py"
"""
import json
import ssl
import sys
import time
import urllib.request
import urllib.error
import datetime as dt
from pathlib import Path

DATA = Path("E:/Wiki Felipe empresas/_wiki/_data")
OR = DATA / "openrouter"
CTX = ssl._create_unverified_context()
UA = {"User-Agent": "Mozilla/5.0 (wiki-openrouter-fetch)"}

BASE = "https://openrouter.ai"
FE = BASE + "/api/frontend/v1"

ENDPOINTS = {
    "models":     BASE + "/api/v1/models",
    "catalog":    FE + "/catalog/models",
    "providers":  FE + "/all-providers",
    "rank_week":  FE + "/rankings/models?view=week",
    "rank_month": FE + "/rankings/models?view=month",
    "apps":       FE + "/rankings/apps?view=week",
}

# Per-provider price watchlist (documented public API: /api/v1/models/{slug}/endpoints).
# First three prove "first-party = same price on every venue"; the rest map the
# neocloud market (Together/Fireworks/DeepInfra/...) for open-weight models.
ENDPOINT_MODELS = [
    "anthropic/claude-opus-4.8",
    "anthropic/claude-sonnet-5",
    "openai/gpt-5.6-sol",
    "deepseek/deepseek-v3.2",
    "deepseek/deepseek-v4-flash",
    "deepseek/deepseek-v4-pro",
    "qwen/qwen3-next-80b-a3b-instruct",
    "meta-llama/llama-4-maverick",
    "z-ai/glm-5.2",
    "minimax/minimax-m3",
    "moonshotai/kimi-k2.5",
    "mistralai/mistral-large-2512",
]


def get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def main():
    today = dt.date.today().isoformat()
    outdir = OR / "raw" / today
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = {"fetched_at": dt.datetime.now().isoformat(timespec="seconds"), "date": today, "endpoints": {}}
    for name, url in ENDPOINTS.items():
        try:
            data = get(url)
            (outdir / (name + ".json")).write_text(json.dumps(data), encoding="utf-8")
            rows = data.get("data") if isinstance(data, dict) else data
            n = len(rows) if hasattr(rows, "__len__") else "?"
            manifest["endpoints"][name] = {"url": url, "ok": True, "n": n}
            print("  OK  %-11s %s rows" % (name, n))
        except Exception as e:
            manifest["endpoints"][name] = {"url": url, "ok": False, "error": "%s: %s" % (type(e).__name__, e)}
            print("  ERR %-11s %s" % (name, e), file=sys.stderr)
    # per-provider endpoint prices for the watchlist (fail-soft per slug)
    eps = {}
    for slug in ENDPOINT_MODELS:
        try:
            eps[slug] = get(BASE + "/api/v1/models/" + slug + "/endpoints").get("data", {})
        except Exception as e:
            manifest["endpoints"].setdefault("model_endpoints_errors", {})[slug] = str(e)
    (outdir / "endpoints.json").write_text(json.dumps(eps), encoding="utf-8")
    manifest["endpoints"]["model_endpoints"] = {"ok": True, "n": len(eps)}
    print("  OK  %-11s %s models" % ("endpoints", len(eps)))
    (outdir / "_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    # pointer to the newest good snapshot
    (OR / "latest.txt").write_text(today, encoding="utf-8")
    print("wrote", outdir)


if __name__ == "__main__":
    main()
