r"""
Orchestrator — rebuild all six wiki feature artifacts in dependency order, then
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
    ("build_search_index.py", []),  # incremental — unchanged files skipped
    ("build_graph.py", []),         # needs catalysts + search index + book + assumptions
]

HUB = [
    ("Edge tracker", "edge.html", "House vs Street divergences (the alpha) — programmatic + curated."),
    ("Read-through map", "readthrough.html", "Supply-chain & substitutes: who reads through to whom."),
    ("Catalyst loop", "catalysts.html", "Upcoming calendar + passed catalysts awaiting a post-mortem."),
    ("Catalyst timeline", "gantt.html", "Forward Gantt — every catalyst on one time axis (bar width = date precision)."),
    ("What changed", "diff.html", "Recent page changelog + ingest deltas (rating/PT moves starred)."),
    ("Coverage audit", "coverage.html", "Source material on disk that the page never read (decks, calls, latest filings)."),
    ("Canonical assumptions", "assumptions.html", "One number per debate — every cross-page figure, all variants, scope traps flagged."),
    ("Knowledge graph", "graph.html", "Interactive map of the whole repo — tickers, themes, debates, brokers, supply chain."),
    ("Book exposure", "book.html", "Positions × unresolved debates × catalysts — where the book is most exposed."),
    ("Hyperscaler capex", "hyperscaler-capex/Capex_Cloud.html", "Consensus vs actual vs house cloud capex (existing)."),
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
