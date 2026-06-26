#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_snapshot.py — inject a compact "Consensus snapshot" box + EPS-revision line
into the top of every company page (right after the _Wiki byline), between
idempotent <!-- SNAPSHOT:START --> / <!-- SNAPSHOT:END --> markers.

Source of truth:
  _data/estimates.json  (BBG consensus — 81 names)
  _data/house.json      (Capstone official model — 8 names: overlaid where present)

Metrics (per user spec): Revenue, Gross profit (=Rev x GM%), Gross margin,
EBITDA, EPS, Capex, OCF (no forward BBG consensus -> EBITDA shown as proxy).

Re-runnable: replaces the block between markers if it already exists.
"""
import sys, os, re, json, glob

sys.stdout.reconfigure(encoding="utf-8")
WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(WIKI)

START = "<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->"
END = "<!-- SNAPSHOT:END -->"

CCY = {"USD": "$", "EUR": "€", "JPY": "¥", "TWD": "NT$", "KRW": "₩"}
BLOCKS = "▁▂▃▄▅▆▇█"  # ▁▂▃▄▅▆▇█


def money(v, sym):
    if v is None:
        return "—"
    a = abs(v)
    if a >= 1000:  # millions -> bn
        return f"{sym}{v/1000:.1f}bn"
    return f"{sym}{v:.0f}m"


def pct(v):
    return "—" if v is None else f"{v:.1f}%"


def eps_fmt(v, sym):
    return "—" if v is None else f"{sym}{v:.2f}"


def sparkline(vals):
    vals = [x for x in vals if x is not None]
    if len(vals) < 2:
        return ""
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return BLOCKS[0] * len(vals)
    return "".join(BLOCKS[int((x - lo) / (hi - lo) * (len(BLOCKS) - 1))] for x in vals)


def make_svg(rev):
    """Inline SVG bar chart of the EPS-estimate trend (6m/3m/1m/now) for FY1 & FY2.
    Colors match the wiki's light theme (index.html palette). Self-contained."""
    panels = []
    for fy, label in (("fy1", "FY1"), ("fy2", "FY2")):
        d = (rev or {}).get("eps", {}).get(fy)
        if not d or d.get("now") is None:
            continue
        now = d["now"]
        def ago(w):
            p = d.get(w)
            return None if p is None else now / (1 + p / 100.0)
        panels.append((label, d, [ago("6m"), ago("3m"), ago("1m"), now]))
    if not panels:
        return ""
    pw, gap, bh, top, bw, bgap = 150, 26, 44, 14, 20, 8
    W = len(panels) * pw + (len(panels) - 1) * gap
    H = top + bh + 30
    labs = ["6m", "3m", "1m", "now"]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Roboto,sans-serif">']
    for pi, (label, d, series) in enumerate(panels):
        ox = pi * (pw + gap)
        mx = max(v for v in series if v is not None)
        p.append(f'<text x="{ox}" y="10" font-size="11" font-weight="600" fill="#33405c">{label} EPS revision</text>')
        n = len(series)
        for i, v in enumerate(series):
            x = ox + i * (bw + bgap)
            if v is not None:
                h = max(3.0, v / mx * bh)
                color = "#1c7d3f" if i == n - 1 else "#1c5fd6"
                p.append(f'<rect x="{x}" y="{top+bh-h:.1f}" width="{bw}" height="{h:.1f}" rx="2" fill="{color}"/>')
            p.append(f'<text x="{x+bw/2:.0f}" y="{top+bh+11}" font-size="9" text-anchor="middle" fill="#8492ad">{labs[i]}</text>')
        bits = []
        for w in ("3m", "6m"):
            if d.get(w) is not None:
                bits.append(f"+{d[w]:.1f}% {w}" if d[w] >= 0 else f"{d[w]:.1f}% {w}")
        p.append(f'<text x="{ox}" y="{top+bh+26}" font-size="10" fill="#1c7d3f">{" · ".join(bits)}</text>')
    p.append("</svg>")
    return "".join(p)


def revision_line(rev):
    """EPS revision: direction/magnitude of estimate changes (basis-agnostic).
    Reconstructs the estimate 6m/3m/1m ago from 'now' + % change to draw the trend.
    Shows sparkline + 3m/6m % only (absolute level lives in the EPS row)."""
    out = []
    for fy in ("fy1", "fy2"):
        d = (rev or {}).get("eps", {}).get(fy)
        if not d or d.get("now") is None:
            continue
        now = d["now"]
        def ago(w):
            p = d.get(w)
            return None if p is None else now / (1 + p / 100.0)
        spark = sparkline([ago("6m"), ago("3m"), ago("1m"), now])
        bits = []
        for w in ("3m", "6m"):
            if d.get(w) is not None:
                bits.append((f"+{d[w]:.1f}% {w}" if d[w] >= 0 else f"{d[w]:.1f}% {w}"))
        tag = "FY1" if fy == "fy1" else "FY2"
        chg = (" " + " · ".join(bits)) if bits else " (flat)"
        out.append(f"{tag} {spark}{chg}")
    return " · ".join(out)


def build_block(ticker, est_co, house_co):
    sym = CCY.get(est_co.get("ccy", "USD"), "$")
    ccy = est_co.get("ccy", "USD")
    cols = ("CY2026", "CY2027")

    # numeric values per column, with a source flag ("bbg"/"house") for rev/gm/eps
    # rev/gm in BBG units (rev = millions); house rev = $bn -> convert to millions for parity
    vals = {c: {} for c in cols}
    src = {c: {} for c in cols}
    for c in cols:
        p = est_co["periods"].get(c, {})
        for k in ("rev", "gm", "ebitda", "eps", "capex"):
            vals[c][k] = p.get(k)
            src[c][k] = "bbg"

    # ---- Capstone official-model overlay (8 names) ----
    is_house = bool(house_co)
    if is_house:
        yrs = house_co.get("years", {})
        usd_ok = ccy == "USD"  # house revenue is $bn; only overlay rev when page ccy is USD too
        for c in cols:
            y = yrs.get(c[-4:], {})  # "CY2026" -> "2026"
            if usd_ok and y.get("rev") is not None:
                vals[c]["rev"] = y["rev"] * 1000.0  # $bn -> $m
                src[c]["rev"] = "house"
            if y.get("gm") is not None:
                vals[c]["gm"] = y["gm"]
                src[c]["gm"] = "house"
            if y.get("eps") is not None:
                vals[c]["eps"] = y["eps"]
                src[c]["eps"] = "house"

    def cell(c, key, fmt):
        v = vals[c].get(key)
        s = fmt(v)
        return f"**{s}**" if (src[c].get(key) == "house" and v is not None) else s

    def gp_cell(c):  # gross profit = displayed revenue x displayed gross margin
        r, g = vals[c].get("rev"), vals[c].get("gm")
        return money(r * g / 100.0, sym) if (r is not None and g is not None) else "—"

    rows = [
        ("Revenue",       [cell(c, "rev",   lambda v: money(v, sym)) for c in cols]),
        ("Gross profit",  [gp_cell(c) for c in cols]),
        ("Gross margin",  [cell(c, "gm",    pct) for c in cols]),
        ("EBITDA",        [cell(c, "ebitda", lambda v: money(v, sym)) for c in cols]),
        ("EPS",           [cell(c, "eps",   lambda v: eps_fmt(v, sym)) for c in cols]),
        ("Capex",         [cell(c, "capex", lambda v: money(v, sym)) for c in cols]),
        ("OCF (≈EBITDA)", [cell(c, "ebitda", lambda v: money(v, sym)) for c in cols]),
    ]

    asof = est_co.get("revisions", {}).get("asof", "")
    if is_house:
        heading = f"### \U0001F4CA Snapshot — Capstone official model + BBG · asof {asof} · {ccy}"
        legend = "\n_**Bold** = Capstone official model; plain = BBG consensus._"
    else:
        heading = f"### \U0001F4CA Consensus snapshot — BBG · asof {asof} · {ccy}"
        legend = ""

    lines = [START, heading, "", "| Metric | CY2026E | CY2027E |", "|---|--:|--:|"]
    for lbl, (c26, c27) in rows:
        lines.append(f"| {lbl} | {c26} | {c27} |")
    lines.append("")
    if SVG_MODE:
        svg = make_svg(est_co.get("revisions"))
        if svg:
            lines.append(svg)
            lines.append("")  # blank line so the markdown parser treats the SVG as a block
    else:
        rl = revision_line(est_co.get("revisions"))
        if rl:
            lines.append(f"**EPS revision** (BBG est. trend) — {rl}")
            lines.append("")
    note = "_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._"
    lines.append(note + legend)
    lines.append(END)
    return "\n".join(lines)


def inject(md_path, block):
    txt = open(md_path, encoding="utf-8").read()
    if START in txt and END in txt:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), block, txt, count=1, flags=re.S)
        open(md_path, "w", encoding="utf-8", newline="\n").write(new)
        return "updated"
    lines = txt.splitlines()
    ins = None
    for i, l in enumerate(lines):
        if l.startswith("_Wiki"):
            ins = i + 1
            break
    if ins is None:  # fallback: after H1
        for i, l in enumerate(lines):
            if l.startswith("# "):
                ins = i + 1
                break
    if ins is None:
        return "no-anchor"
    lines[ins:ins] = ["", block]
    open(md_path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    return "inserted"


SVG_MODE = True  # default: inline SVG chart for EPS revision; pass --text for the unicode sparkline fallback


def main():
    global SVG_MODE
    args = [a for a in sys.argv[1:]]
    if "--svg" in args:
        args.remove("--svg")
    if "--text" in args:
        SVG_MODE = False
        args.remove("--text")
    est = json.load(open("_data/estimates.json", encoding="utf-8"))["companies"]
    house = json.load(open("_data/house.json", encoding="utf-8"))["companies"]
    only = set(a.upper().replace(".MD", "") for a in args)
    files = sorted(f for f in glob.glob("*.md") if not f.startswith("_") and f != "00_INDEX.md")
    done = skipped = 0
    for f in files:
        tk = f[:-3]
        if only and tk not in only:
            continue
        if tk not in est:
            skipped += 1
            continue
        block = build_block(tk, est[tk], house.get(tk))
        status = inject(f, block)
        done += 1
        print(f"{status:9} {tk}")
    print(f"\n{done} injected, {skipped} skipped (no BBG consensus).")


if __name__ == "__main__":
    main()
