r"""
Orchestrator — rebuild the wiki feature artifacts in dependency order, then
the dashboards hub. Safe to run anytime (read-only on pages; writes only to
_meta / _data / _dashboards). Wire into the nightly routine after the ingest.

    py "E:/Wiki Felipe empresas/_wiki/_tools/refresh_features.py"
    py "E:/Wiki Felipe empresas/_wiki/_tools/refresh_features.py --run-estimates"  # also fetch missing BBG
"""
import sys, subprocess, html
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _wlib import DASH, TODAY
sys.stdout.reconfigure(encoding="utf-8")

TOOLS = Path(__file__).parent
RUN_EST = "--run-estimates" in sys.argv

# (script, extra args) — extract_house feeds build_edge, so order matters.
STEPS = [
    ("build_index.py", []),         # 00_INDEX.md from _data/index_meta.json (before search index)
    ("extract_house.py", []),
    ("build_edge.py", []),
    ("remediate.py", ["--run-estimates"] if RUN_EST else []),
    ("build_readthrough.py", []),
    ("build_diff.py", []),
    ("build_catalysts.py", []),
    ("build_gantt.py", []),
    ("build_coverage.py", []),
    ("build_assumptions.py", []),
    ("build_book.py", []),          # needs build_catalysts + extract_house first
    ("build_mgmt_comms.py", []),    # reads each page's commentary-evolution table
    ("build_cyber_kpis.py", []),    # cyber KPI ledger (_data/cyber_kpis.json + estimates.json) -> cyber-kpis.html
    ("gpu_pricing.py", []),        # Bloomberg + public SemiAnalysis; retain cache on source failure
    ("build_gpu_pricing.py", []),  # render retained or refreshed observations
    ("build_openrouter_dash.py", []),  # keep the embedded GPU tab in sync
    ("build_search_index.py", []),  # incremental — unchanged files skipped
    ("build_graph.py", []),         # needs catalysts + search index + book + assumptions
    ("build_analyst.py", []),       # belief ledger + ranked, attributed proactive signal queue
    ("build_sentiment.py", ["--no-bbg"]),   # hot/cold × bull/bear indicator — tweets re-scanned, BBG history from cache (terminal-only refresh: run without --no-bbg)
]

HUB = [
    ('Specialist sales - all companies', 'attention-sentiment/specialist-sales.html', '106-company coverage ledger, contextual desk views, expectations and reported positioning; source disagreements and dated evidence. Dark, offline dashboard.'),
    ('Attention & sentiment', 'attention-sentiment/index.html', 'Price versus discussion, a 106-name stock radar, five rising/falling names, source breadth and specialist-sales evidence. Dark dashboards; retained snapshots.'),
    ('Fear & Greed - extreme entries', 'attention-sentiment/cnn-next-week.html', 'SPY/QQQ performance over the next five trading sessions after new entries into fear or greed zones. Event-focused, with sample sizes and uncertainty.'),
    ('Narratives & specialist sales', 'attention-sentiment/narrative-diffusion.html', 'META/Muse case study: product aliases, author diffusion and source-timed specialist-sales observations.'),
    ("Estudos · OpenRouter + Vercel", "openrouter.html", "Opens with open-weight vs proprietary share of tokens and weekly token traffic (NVIDIA-slide framing, weekly). Then gateway token share, requests, reported versus estimated spend, and weekly changes. Friday summary at 09:00 Brasília."),
    ("GPU rental pricing", "gpu-pricing.html", "H100, A100 and B200: Bloomberg rental benchmarks, SemiAnalysis public spot-contract indices and H100 one-year survey ranges, with dated source data."),
    ("AI gateways — weekly brief", "gateway-weekly.html", "Latest weekly summary covering OpenRouter and Vercel, with dated observations and source-specific methodology."),
    ("Analyst Inbox", "analyst-inbox.html", "Ranked daily ideas, model challenges, narrative shifts, catalysts and read-throughs — each with attribution, action and falsifier."),
    ("AI credit & funding monitor", "credit-monitor.html", "AI issuance, neocloud spreads, counterparty tiering, appetite scoreboard — manual refresh: fetch_funding.py + build_funding_monitor.py."),
    ("Edge tracker", "edge.html", "House vs Street divergences (the alpha) — programmatic + curated."),
    ("Read-through map", "readthrough.html", "Supply-chain & substitutes: who reads through to whom."),
    ("Catalyst loop", "catalysts.html", "Upcoming calendar + passed catalysts awaiting a post-mortem."),
    ("Catalyst timeline", "gantt.html", "Forward Gantt — every catalyst on one time axis (bar width = date precision)."),
    ("What changed", "diff.html", "Recent page changelog + ingest deltas (rating/PT moves starred)."),
    ("Coverage audit", "coverage.html", "Source material on disk that the page never read (decks, calls, latest filings)."),
    ("Canonical assumptions", "assumptions.html", "One number per debate — every cross-page figure, all variants, scope traps flagged."),
    ("Knowledge graph", "graph.html", "Interactive map of the whole repo — tickers, themes, debates, brokers, supply chain."),
    ("Book exposure", "book.html", "Positions × unresolved debates × catalysts — where the book is most exposed."),
    ("Sentiment — hot/cold × bull/bear", "sentiment.html", "Hot/cold × bull/bear per name: own tweet corpus + Bloomberg Twitter/news sentiment (2024→) + sell-side e-mail flow (Outlook) × EPS revisions, rating drift, short interest — weekly ranking, quadrant map, 1w/15d/4w rank-IC backtests and a 1,000-print earnings event-window study (build_sentiment.py)."),
    ("Management communication", "mgmt-communication.html", "MSFT · AMZN · GOOG · META · NVDA · TSM · ASML · AVGO — how the discourse moved quarter by quarter, the capex-message vs tape cross-section, and who will and won't put a number on it."),
    ("Cyber KPI ledger", "cyber-kpis.html", "PANW · CRWD · OKTA — the non-GAAP KPIs Bloomberg does not carry (net new ARR, NGS ARR, cRPO, NRR, Flex, module attach): sourced ledger, cross-company small multiples on a calendar axis, next-print guide vs consensus vs the buy-side bar (hand-curated _data/cyber_kpis.json)."),
    ("Ramp AI Index", "ramp-ai-index.html", "Enterprise alt-data, two series off one panel: model mix (who gets used — provider share, the Anthropic capability ladder, vintage turnover, launch curves) and AI spend per employee. Manual refresh: drop the new CSV in _data/ramp-ai-index/, then build_ramp_index.py + build_ramp_dash.py. ⚠ no Google/Gemini rows in the panel — not a market share."),
    ("Hyperscaler capex", "hyperscaler-capex/Capex_Cloud.html", "Consensus vs actual vs house cloud capex (existing)."),
    ("GW per player", "gw-per-player.html", "Highest GW estimate per player, all sources cited, SemiAnalysis highlighted (hand-curated 2026-07-01)."),
    ("Token fabric", "token-fabric.html", "Token supply vs demand 2026-2030 — calibrated tok/s/MW, per-user watts, malinvestment dial (hand-curated 2026-07-02)."),
    ("The Light Path — OCS · CPO · scale-up/out", "ocs-cpo-lab.html", "Interactive 3D explainer: how an optical circuit switch re-routes light with MEMS mirrors (vs an electrical switch), how optics move from pluggable to NPO to CPO (power, pJ/bit, DSP, laser, service), where copper, pluggables, NPO, CPO and OCS sit in scale-up vs scale-out (with the NVL72 → NVL576 rack-to-rack walkthrough), and a 'Who sits where' map of every company the wiki places in each layer — every number attributed (hand-built 2026-09-27/28)."),
    ("The Wafer Path — TSMC logic · DRAM · HBM", "wafer-lab.html", "Interactive 3D explainer with a step-by-step walkthrough per tab (the drawing builds itself stage by stage, camera follows, each step attributed): how TSMC builds a leading-edge logic wafer (FinFET to GAA to backside power, the EUV/DUV patterning loop, tools and capex per fab), how the memory makers build a DRAM wafer (1T1C cell, 6F² to 4F² VCT to 3D DRAM, where the few EUV layers sit, capacity by maker) and what turns DRAM dies into an HBM stack (TSVs, base die at TSMC, MR-MUF vs TC-NCF vs hybrid bonding, height ceiling, yield compounding, wafer trade ratio) — every number attributed (hand-built 2026-09-28)."),
    ("Memória — superciclo", "memoria-capstone.html", "Superciclo de memória (DRAM · NAND · HBM): KPIs, S/D por segmento, capacidade e conversão HBM, valuation e builds editáveis, dark mode (hand-built 2026-07-08)."),
    ("Memory exports tracker", "memory-exports-tracker.html", "Weekly Monday routine (E:\korea-memory-monitor): Korea customs 10-day preliminaries and HS10 detail (DRAM, flash, multichip, SSD, destinations), MOTIE fixed DDR5/NAND prices, BOK export price indices, Japan flash exports (Kioxia/SanDisk) and the quarter read vs the Street; full monthly report in memory-exports-report.html."),
    ("Revenue das clouds", "rcloud.html", "AWS · Azure · GCP: resultado, RPO (split OpenAI/Anthropic), projeções Capstone vs consenso vs bogey, exposição aos labs, EBIT e capex/FCF — réplica do rcloud.html da Fernanda (sync_rcloud.py)."),
]


def build_hub():
    cards = []
    for title, href, desc in HUB:
        if (DASH / href).exists():
            cards.append(f"<a class='card' href='{href}'><h3>{title}</h3><p>{html.escape(desc)}</p></a>")
    body = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Wiki dashboards</title>
<style>
body{{margin:0;font:15px/1.55 -apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#1a1f29;background:#f5f6f8}}
header{{background:#0f1729;color:#fff;padding:20px 28px}}header h1{{margin:0;font-size:20px}}
header a{{color:#7fb0ff;text-decoration:none}}header p{{margin:4px 0 0;color:#8492ad;font-size:13px}}
main{{max-width:980px;margin:0 auto;padding:24px 28px;display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.card{{display:block;background:#fff;border:1px solid #e3e7ee;border-radius:10px;padding:16px 18px;text-decoration:none;color:inherit;transition:.12s}}
.card:hover{{border-color:#4f8cff;box-shadow:0 2px 10px #0f172914}}
.card h3{{margin:0 0 6px;color:#0f1729;font-size:16px}}.card p{{margin:0;color:#6b7280;font-size:13px}}
</style></head><body>
<header><h1>📊 Wiki dashboards</h1><p>Generated {TODAY.isoformat()} · <a href="../index.html">← back to the company wiki</a></p></header>
<main>{''.join(cards)}</main></body></html>"""
    (DASH / "index.html").write_text(body, encoding="utf-8")


def main():
    print(f"=== refresh_features {TODAY.isoformat()} ===")
    for script, extra in STEPS:
        print(f"\n--- {script} {' '.join(extra)} ---")
        r = subprocess.run([sys.executable, str(TOOLS / script), *extra], capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode != 0:
            sys.stderr.write(r.stderr[-1200:])
            print(f"[WARN] {script} exited {r.returncode}")
    build_hub()
    print(f"\nhub -> {DASH/'index.html'}")
    print("done.")


if __name__ == "__main__":
    main()
