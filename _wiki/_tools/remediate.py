r"""
FEATURE 2 — Close the lint loop (auto-remediation).

lint_wiki.py only *flags* staleness. This turns those flags into an actionable
worklist and (optionally) executes the parts that are scriptable:

  - BBG estimates missing  -> can be fetched now via the existing fetch_estimates.py
                              (it MERGES into estimates.json, so a subset is safe).
  - No transcript on disk  -> emits ready-to-paste transcript-fetcher agent tasks
                              (agent work, not scriptable here).

Default run = DRY (recompute + write worklist, execute nothing). Pass
--run-estimates to actually call BBG (Terminal must be logged in).

    py "E:/Wiki Felipe empresas/_wiki/_tools/remediate.py"                 # dry: write worklist
    py "E:/Wiki Felipe empresas/_wiki/_tools/remediate.py --run-estimates" # also fetch missing BBG

Writes _meta/worklist.json + _meta/worklist.md. Read-only on pages.
"""
import sys, json, re, subprocess
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import WIKI, META, company_pages, read, load_estimates, DATE_RE, TODAY
sys.stdout.reconfigure(encoding="utf-8")

SEC = WIKI.parent                    # E:\Wiki Felipe empresas  (per-ticker archive folders)
FETCH = r"E:\.claude\scripts\fetch_estimates.py"
RUN_EST = "--run-estimates" in sys.argv


def is_private(txt):
    t = txt.lower()
    return "no public financials" in t or "private company" in t


def compute():
    est = load_estimates().get("companies", {})
    bbg_missing, no_tx, private = [], [], []
    for tk, pf in company_pages():
        txt = read(pf)
        priv = is_private(txt)
        c = est.get(tk)
        if not priv and (c is None or "error" in (c or {})):
            bbg_missing.append(tk)
        tdir = SEC / tk / "transcripts"
        has_tx = tdir.is_dir() and any(DATE_RE.search(f.name) for f in tdir.glob("*.md"))
        if not priv and not has_tx:
            no_tx.append(tk)
        if priv:
            private.append(tk)
    return bbg_missing, no_tx, private


def main():
    bbg_missing, no_tx, private = compute()

    worklist = {
        "asof": TODAY.isoformat(),
        "bbg_missing": bbg_missing,
        "no_transcript": no_tx,
        "private_skipped": private,
        "actions": {
            "fetch_estimates_cmd": f'py "{FETCH}" ' + " ".join(bbg_missing) if bbg_missing else None,
            "transcript_tasks": [
                {"agent": "transcript-fetcher",
                 "prompt": f"Get the latest earnings call transcript for {tk} and save it to "
                           f"E:\\Wiki Felipe empresas\\{tk}\\transcripts\\ as "
                           f"{tk}_<quarter>_<YYYY-MM-DD>.md"}
                for tk in no_tx
            ],
        },
    }
    META.mkdir(parents=True, exist_ok=True)
    (META / "worklist.json").write_text(json.dumps(worklist, ensure_ascii=False, indent=1), encoding="utf-8")

    md = [f"# Wiki remediation worklist\n",
          f"_Generated {TODAY.isoformat()} · closes the loop on `lint_wiki.py` / staleness.md. "
          f"Rebuild: `py _wiki/_tools/remediate.py`._\n",
          f"## 🔴 BBG estimates missing ({len(bbg_missing)}) — scriptable\n"]
    if bbg_missing:
        md.append("Run (BBG Terminal must be logged in) — `fetch_estimates.py` merges, so this is safe:\n")
        md.append("```\n" + worklist["actions"]["fetch_estimates_cmd"] + "\n```\n")
        md.append("Or auto: `py _wiki/_tools/remediate.py --run-estimates`\n")
        md.append(", ".join(bbg_missing) + "\n")
    else:
        md.append("_none_\n")
    md.append(f"## 🟡 No transcript on disk ({len(no_tx)}) — needs the transcript-fetcher agent\n")
    if no_tx:
        md.append("Spawn one `transcript-fetcher` task per name (paste into Claude Code):\n")
        for tk in no_tx:
            md.append(f"- **{tk}** — \"get the latest {tk} earnings transcript -> "
                      f"`E:\\Wiki Felipe empresas\\{tk}\\transcripts\\`\"")
        md.append("")
    else:
        md.append("_none_\n")
    md.append(f"## ⚪ Private — intentionally skipped ({len(private)})\n")
    md.append(", ".join(private) + "\n" if private else "_none_\n")
    (META / "worklist.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"worklist: {len(bbg_missing)} BBG-missing, {len(no_tx)} no-transcript, "
          f"{len(private)} private -> {META/'worklist.md'}")

    if RUN_EST and bbg_missing:
        print(f"\n[--run-estimates] calling fetch_estimates.py for {len(bbg_missing)} names...")
        r = subprocess.run([sys.executable, FETCH, *bbg_missing], capture_output=True, text=True)
        sys.stdout.write(r.stdout[-2000:])
        if r.returncode != 0:
            sys.stderr.write(r.stderr[-1500:])
            print("\n[fetch failed — likely BBG Terminal not logged in. Worklist still written.]")
        else:
            print("\n[fetch done — re-run build_edge.py / build_wiki_html.py to refresh derived views.]")
    elif RUN_EST:
        print("[--run-estimates] nothing to fetch.")


if __name__ == "__main__":
    main()
