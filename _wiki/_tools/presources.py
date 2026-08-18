#!/usr/bin/env python
"""
presources.py - PRE-FLIGHT SOURCE SWEEP.

Run this BEFORE building or updating a model. It enumerates every primary source
on a ticker that already exists (filings, transcripts, decks, ingested reports,
and optionally emails), then diffs that against what your model/notes actually
cite. Anything on disk that you have not cited comes back as an OPEN item.

Exists because three consecutive adversarial audits of the COHR model returned
the same #1 finding: broker notes, 10-Ks, 10-Qs, transcripts and an investor day
sat unread on disk while the model leaned on one broker file and a Substack relay.
That is a checkable condition, so check it mechanically instead of by resolve.

Usage
-----
  py _wiki/_tools/presources.py --ticker COHR
  py _wiki/_tools/presources.py --ticker COHR --cited "Modelos oficiais/Modelo COHR v3.xlsx"
  py _wiki/_tools/presources.py --ticker COHR --cited notes.md --emails scratchpad/outlook21.json
  py _wiki/_tools/presources.py --ticker COHR --cited model.xlsx --gate

--cited   a .md / .txt / .py / .xlsx to scan for references. For .xlsx every cell
          string across every sheet is scanned, so source notes in the workbook count.
--emails  a JSON dump from E:/.claude/scripts/outlook.py (list, or {"emails":[...]}).
--gate    exit 1 if any OPEN primary remains. Use it to block a build.
"""
import argparse, json, os, re, sys, zipfile
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

# Senders that publish research. Used only to grade email hits, never to filter them.
RESEARCH_HINTS = ("jefferies", "jpmorgan", "jpmresearch", "bofa", "morganstanley", "ms.com",
                  "barclays", "ubs", "citi", "bernstein", "redburn", "rothschild",
                  "raymondjames", "wolfe", "bnpparibas", "exane", "needham", "rosenblatt",
                  "gs.com", "goldman", "btgpactual", "susquehanna", "sig.com", "melius",
                  "newstreet", "arete", "bernsteinsg", "22vresearch", "visiblealpha")


def _dt(s):
    for f in ("%Y-%m-%d", "%Y%m%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None


def find_disk(ticker):
    """Everything on disk for this ticker, bucketed."""
    t = ticker.upper()
    out = {"10-K": [], "10-Q": [], "8-K / other filing": [], "transcript": [],
           "deck / investor day": [], "ingested report": [], "wiki page": []}
    tdir = ROOT / t
    if tdir.is_dir():
        for p in tdir.rglob("*"):
            if not p.is_file():
                continue
            n = p.name
            low = n.lower()
            if "10-k" in low:
                out["10-K"].append(p)
            elif "10-q" in low:
                out["10-Q"].append(p)
            elif p.suffix.lower() in (".html", ".htm") and re.search(r"_(8-K|S-\d|DEF)", n, re.I):
                out["8-K / other filing"].append(p)
            elif "transcript" in str(p.parent).lower() or "transcript" in low:
                out["transcript"].append(p)
            elif p.suffix.lower() in (".pdf", ".pptx") or "apresenta" in str(p.parent).lower():
                out["deck / investor day"].append(p)
    rep = ROOT / "relatórios bons"
    if rep.is_dir():
        pat = re.compile(rf"(^|[^A-Za-z]){t}([^A-Za-z]|$)", re.I)
        for p in rep.glob("*"):
            if p.is_file() and pat.search(p.name):
                out["ingested report"].append(p)
    for cand in (ROOT / "_wiki" / f"{t}.md",):
        if cand.exists():
            out["wiki page"].append(cand)
    return {k: sorted(v) for k, v in out.items() if v}


def cited_text(path):
    """Pull all text out of a citation target. .xlsx -> every string cell, every sheet."""
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"--cited not found: {p}")
    if p.suffix.lower() in (".xlsx", ".xlsm"):
        buf = []
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                if name.startswith("xl/") and name.endswith(".xml"):
                    try:
                        buf.append(z.read(name).decode("utf-8", "ignore"))
                    except Exception:
                        pass
        return "\n".join(buf)
    return p.read_text(encoding="utf-8", errors="ignore")


def is_cited(path, blob):
    """A source counts as cited if its filename, its stem, or its date appears."""
    stem = Path(path).stem
    if stem and stem in blob:
        return True
    if Path(path).name in blob:
        return True
    m = re.search(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})", stem)
    if m:
        iso = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        if iso in blob:
            return True
    # transcripts are often cited as "Q4FY26" or "FQ4 FY26"
    q = re.search(r"(F?Q\d\s?FY\d{2})", stem, re.I)
    if q and q.group(1).replace(" ", "") in blob.replace(" ", ""):
        return True
    return False


def load_emails(path, ticker, days):
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"--emails not found: {p}")
    data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    if isinstance(data, dict):
        for k in ("emails", "messages", "items", "data"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
    if not isinstance(data, list):
        return []
    t = ticker.upper()
    name_map = {"COHR": "coherent", "LITE": "lumentum", "AAOI": "applied optoelectronics",
                "NVDA": "nvidia", "AVGO": "broadcom", "MU": "micron", "ASML": "asml"}
    pat = re.compile(rf"(^|[^A-Za-z]){t}([^A-Za-z]|$)|{name_map.get(t, t)}", re.I)
    cut = datetime.now() - timedelta(days=days)
    hits = []
    for e in data:
        if not isinstance(e, dict):
            continue
        subj = str(e.get("subject") or e.get("Subject") or "")
        if not pat.search(subj):
            continue
        raw = str(e.get("received") or e.get("receivedDateTime") or e.get("date") or "")
        d = None
        for f in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                d = datetime.strptime(raw[:19], f)
                break
            except ValueError:
                pass
        if d and d < cut:
            continue
        sender = str(e.get("sender") or e.get("from") or e.get("sender_email") or "")
        hits.append({"date": d.strftime("%Y-%m-%d") if d else "?", "subject": subj[:96],
                     "sender": sender[:52],
                     "research": any(h in sender.lower() for h in RESEARCH_HINTS)})
    return sorted(hits, key=lambda x: x["date"], reverse=True)


def main():
    ap = argparse.ArgumentParser(description="Pre-flight source sweep before a model build.")
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--cited", help="model or notes file to scan for references")
    ap.add_argument("--emails", help="JSON dump from outlook.py")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--gate", action="store_true", help="exit 1 if OPEN primaries remain")
    a = ap.parse_args()

    t = a.ticker.upper()
    print("=" * 84)
    print(f"  PRE-FLIGHT SOURCE SWEEP  -  {t}   ({datetime.now():%Y-%m-%d %H:%M})")
    print("=" * 84)

    blob = cited_text(a.cited) if a.cited else ""
    if a.cited:
        print(f"  citations scanned from: {a.cited}\n")
    else:
        print("  no --cited given: listing what exists, not what is missing\n")

    disk = find_disk(t)
    open_items, total = [], 0
    for bucket, paths in disk.items():
        print(f"  {bucket.upper()}  ({len(paths)})")
        for p in paths:
            total += 1
            rel = p.relative_to(ROOT)
            if not a.cited:
                print(f"      {rel}")
                continue
            ok = is_cited(p, blob)
            if not ok:
                open_items.append(rel)
            print(f"    {'OK  ' if ok else 'OPEN'} {rel}")
        print()

    if a.emails:
        hits = load_emails(a.emails, t, a.days)
        res = [h for h in hits if h["research"]]
        print(f"  EMAILS on {t}, last {a.days}d  ({len(hits)} hits, {len(res)} from research senders)")
        for h in hits[:40]:
            mark = "*" if h["research"] else " "
            cited = ""
            if a.cited:
                cited = "  OK" if (h["subject"][:40] in blob) else "  OPEN"
            print(f"    {mark} {h['date']}  {h['sender']:<52} {h['subject']}{cited}")
        if len(hits) > 40:
            print(f"      ... {len(hits)-40} more")
        print("      (* = sender matches a research house)\n")

    print("=" * 84)
    if a.cited:
        print(f"  {total} primary sources on disk · {len(open_items)} NOT cited")
        if open_items:
            print("\n  OPEN - read or explicitly decline these before the build:")
            for r in open_items:
                print(f"      {r}")
            print("\n  Declining is fine. Doing it silently is what the audits kept finding.")
        else:
            print("  Every primary source on disk is referenced. Good.")
    else:
        print(f"  {total} primary sources on disk. Re-run with --cited to see what is unused.")
    print("=" * 84)

    if a.gate and a.cited and open_items:
        sys.exit(1)


if __name__ == "__main__":
    main()
