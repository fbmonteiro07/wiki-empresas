# -*- coding: utf-8 -*-
"""Sentiment ranking block for the daily Twitter Morning Wrap e-mail.

Reads the weekly hot/cold x bull/bear panel the sentiment dashboard reads
(_wiki/_data/sentiment/panel_weekly.json, rebuilt nightly by the 18:15 chain via
build_sentiment.py) and emits the "Ranking — week ending ..." table of
_dashboards/sentiment.html as a markdown block the e-mail renderer
(E:/.claude/scripts/send_briefing_email.py) already styles: pipe table, $TICKER pills,
+x% / -x% colouring. No row tints (no emoji flags) — kept clean on purpose.

Scores: HOT and BULL are shown 0–100 = the dashboard's cross-sectional z (clipped ±3)
mapped linearly, so 50 = the week's average, 100 = +3σ. Stance = bull/bear vs the week's
median BULL, exactly the dashboard's quadrant split (hot/cold vs median HOT is implicit:
the top-N cut by HOT is hot by construction; a cold name would be labelled "Cold-…").

Top N names by HOT, compact column set (no forward-return columns). The panel is weekly
(complete weeks ending Friday), so a daily send repeats the same week until the next
Friday close is processed; the band states the week-ending and rebuild dates.

Usage:
    py sentiment_ranking_md.py                      -> prints the block
    py sentiment_ranking_md.py --top 20 --out F     -> also writes it to F
    py sentiment_ranking_md.py --into BRIEFING.md   -> inserts/replaces the block inside an existing
                                                       wrap, at the TOP (right after the header bar);
                                                       --position watch puts it before WHAT TO WATCH NEXT
Exit code 0 on success; 2 when the panel is missing (the caller sends without the block).
"""
import sys, json, math, re, argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "_data" / "sentiment" / "panel_weekly.json"
BAND_PREFIX = "== SENTIMENT RANKING"
CLOSER = "---"                      # renders as a thin rule; also delimits the block for idempotent re-runs

COLS = ["Ticker", "HOT /100", "BULL /100", "Attention Δ", "Mentions /wk", "Bull / bear",
        "EPS rev 4w", "SI %", "SS notes /wk", "SS flow Δ", "Stance"]


def score(z):
    """clipped z in [-3, 3] -> 0..100 (50 = week average)."""
    if z is None:
        return "–"
    return f"{round((max(-3.0, min(3.0, z)) + 3.0) / 6.0 * 100):d}"


def expct(x):
    """log-ratio -> signed % change, as the dashboard shows Attention Δ / SS flow Δ."""
    if x is None:
        return "–"
    return f"{math.exp(x) * 100 - 100:+.0f}%"


def pct1(x):
    return "–" if x is None else f"{x * 100:+.1f}%"


def num(x, d=0):
    return "–" if x is None else f"{x:.{d}f}"


def ticker_cell(t):
    # the renderer's $TICKER pill takes up to 8 chars after the $; longer names go bold
    return f"${t}" if re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,7}", t) else f"**{t}**"


def quadrant(r, med_hot, med_bull):
    if r.get("HOT") is None or r.get("BULL") is None:
        return ""
    return ("hot" if r["HOT"] >= med_hot else "cold") + "-" + ("bull" if r["BULL"] >= med_bull else "bear")


def stance(q):
    return {"hot-bull": "Bull", "hot-bear": "Bear", "cold-bull": "Cold-bull", "cold-bear": "Cold-bear"}.get(q, "–")


def build(top=20):
    if not PANEL.is_file():
        raise FileNotFoundError(PANEL)
    p = json.loads(PANEL.read_text(encoding="utf-8"))
    weeks = p["weeks"]; last = weeks[-1]; row = p["panel"][last]
    # same medians as _sentiment_dash.render(): upper median of the latest complete week
    hs = sorted(r["HOT"] for r in row.values() if r.get("HOT") is not None)
    bs = sorted(r["BULL"] for r in row.values() if r.get("BULL") is not None)
    med_hot = hs[len(hs) // 2] if hs else 0; med_bull = bs[len(bs) // 2] if bs else 0
    rows = [dict(r, t=t) for t, r in row.items() if r.get("HOT") is not None or r.get("BULL") is not None]
    rows.sort(key=lambda r: (r.get("HOT") is None, -(r.get("HOT") or 0)))
    n_all = len(rows); rows = rows[:top]

    lines = [f"{BAND_PREFIX} — top {len(rows)} of {n_all} by HOT, week ending {last} ==", ""]
    lines.append(
        "HOT = attention vs the name's own trailing 4 weeks · BULL = bull/bear balance of the discussion · "
        "both scored 0–100 within the week (50 = week average) · Mentions = curated + wire handles · "
        f"SS = sell-side e-mail flow · panel rebuilt {p.get('asof', '?')}, rolls after each Friday close · "
        "full table, quadrant map and backtests: `_wiki/_dashboards/sentiment.html`")
    lines.append("")
    lines.append("| " + " | ".join(COLS) + " |")
    lines.append("|" + "|".join("---" for _ in COLS) + "|")
    for r in rows:
        q = quadrant(r, med_hot, med_bull)
        mentions = (r.get("m_cur") or 0) + (r.get("m_wire") or 0)
        cells = [ticker_cell(r["t"]), score(r.get("HOT")), score(r.get("BULL")), expct(r.get("att")),
                 num(mentions), f"{r.get('bull', 0)} / {r.get('bear', 0)}", pct1(r.get("eps_rev")),
                 ("–" if r.get("si") is None else f"{r['si']:.1f}%"), num(r.get("ss_n")), expct(r.get("ss_att")), stance(q)]
        lines.append("| " + " | ".join(cells) + " |")
    hr = [r["t"] for r in rows if quadrant(r, med_hot, med_bull) == "hot-bear"]
    lines.append("")
    lines.append(f"Hot-bear this week: {', '.join(hr) if hr else 'none'} — the only quadrant with a positive forward edge "
                 f"in the backtest; read the list as attention, not as a call.")
    lines.append("")
    lines.append(CLOSER)
    return "\n".join(lines)


def _is_section_header(lines, i):
    s = lines[i].strip(); nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
    return s.startswith("== ") or re.fullmatch(r"={10,}", s) is not None or \
        (bool(s) and s == s.upper() and re.search(r"[A-Z]", s) is not None and re.fullmatch(r"[-=]{3,}", nxt) is not None)


def _strip_existing(lines):
    """Drop a previously inserted block: band line .. closer (inclusive), or up to the next section header
    for a block written by an older version without the closer."""
    out, i, n = [], 0, len(lines)
    while i < n:
        if lines[i].startswith(BAND_PREFIX):
            while out and not out[-1].strip():          # the spacer line we add before the band
                out.pop()
            i += 1
            while i < n:
                if lines[i].strip() == CLOSER:
                    i += 1; break
                if _is_section_header(lines, i):
                    break
                i += 1
            while i < n and not lines[i].strip():      # and the spacer after it
                i += 1
            continue
        out.append(lines[i]); i += 1
    return out


def _top_anchor(lines):
    """Line index right after the opening header bar (==== / title / ====), else after the Subject line."""
    bars = [i for i, ln in enumerate(lines[:12]) if re.fullmatch(r"={10,}", ln.strip())]
    if len(bars) >= 2:
        return bars[1] + 1
    for i, ln in enumerate(lines[:3]):
        if ln.lower().startswith("subject:"):
            return i + 1
    return 0


def _watch_anchor(lines):
    for i, ln in enumerate(lines):                       # before WHAT TO WATCH NEXT banner
        if ln.strip().upper().startswith("WHAT TO WATCH NEXT") and i + 1 < len(lines) and re.fullmatch(r"[-=]{3,}", lines[i + 1].strip()):
            return i
    bars = [i for i, ln in enumerate(lines) if re.fullmatch(r"={10,}", ln.strip())]
    if len(bars) >= 2 and bars[-1] - bars[-2] <= 6:      # before the closing bar
        return bars[-2]
    return len(lines)


def insert_into(path, block, position="top"):
    text = Path(path).read_text(encoding="utf-8")
    lines = _strip_existing(text.replace("\r\n", "\n").split("\n"))
    pos = _top_anchor(lines) if position == "top" else _watch_anchor(lines)
    new = lines[:pos] + [""] + block.split("\n") + [""] + lines[pos:]
    Path(path).write_text("\n".join(new), encoding="utf-8")
    return pos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--out", help="write the block to this file")
    ap.add_argument("--into", help="insert/replace the block inside this markdown file")
    ap.add_argument("--position", choices=["top", "watch"], default="top",
                    help="top = right after the header bar (default); watch = before WHAT TO WATCH NEXT")
    a = ap.parse_args()
    try:
        block = build(a.top)
    except FileNotFoundError as e:
        print(f"sentiment ranking: panel missing ({e}) — nothing inserted"); sys.exit(2)
    if a.out:
        Path(a.out).write_text(block, encoding="utf-8"); print(f"wrote {a.out}")
    if a.into:
        pos = insert_into(a.into, block, a.position)
        print(f"inserted sentiment ranking block into {a.into} at line {pos + 1} ({a.position})")
    if not a.out and not a.into:
        print(block)


if __name__ == "__main__":
    main()
