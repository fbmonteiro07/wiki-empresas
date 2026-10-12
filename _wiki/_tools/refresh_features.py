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
    # ("build_edge.py", []),        # DISABLED 2026-10-02 (Felipe): wiki-edge routine retired; edge.md/edge.html frozen at 2026-10-01
    ("remediate.py", ["--run-estimates"] if RUN_EST else []),
    ("build_readthrough.py", []),
    ("build_diff.py", []),
    ("build_catalysts.py", []),
    ("build_coverage.py", []),
    ("build_assumptions.py", []),
    ("build_mgmt_comms.py", []),    # reads each page's commentary-evolution table
    ("gpu_pricing.py", []),        # Bloomberg + public SemiAnalysis; retain cache on source failure
    ("build_gpu_pricing.py", []),  # render retained or refreshed observations
    ("build_openrouter_dash.py", []),  # keep the embedded GPU tab in sync
    ("build_search_index.py", []),  # incremental — unchanged files skipped
    ("build_graph.py", ["--no-html"]),  # graph_full.json only (graph_query hook + build_analyst); graph.html retired 2026-10-12
    ("build_analyst.py", []),       # belief ledger + ranked, attributed proactive signal queue
    ("build_sentiment.py", ["--no-bbg"]),   # hot/cold × bull/bear indicator — tweets re-scanned, BBG history from cache (terminal-only refresh: run without --no-bbg)
    ("build_sentiment_monitor.py", []),  # daily sentiment monitor: CNN F&G (live, cached), movers, windows, map, daily note
    ("build_dashboards_hub.py", []),  # hub from the hand-edited registry _data/dashboards.json (cadence sections, dates, stale flags)
]


def main():
    print(f"=== refresh_features {TODAY.isoformat()} ===")
    for script, extra in STEPS:
        print(f"\n--- {script} {' '.join(extra)} ---")
        r = subprocess.run([sys.executable, str(TOOLS / script), *extra], capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode != 0:
            sys.stderr.write(r.stderr[-1200:])
            print(f"[WARN] {script} exited {r.returncode}")
    print("done.")


if __name__ == "__main__":
    main()
