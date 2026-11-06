"""Read stacked-bar values straight from a PDF's vector charts (no data labels needed).

    py pdf_chart_bars.py <file.pdf> v <page> [<page> ...]        vertical bars (one chart per "0" y-axis tick)
    py pdf_chart_bars.py <file.pdf> h <page>[:ymin] [...]          horizontal bars (charts split by row gaps; ymin skips content above)

Needs PyMuPDF (fitz) from the user site-packages: run with `py`, not `py -I`. Output: per chart, the fitted
units-per-point, the tick values used, and each bar's value per fill colour (map colours to series from the
legend / page image). First used on Bernstein 2026-11-06 (BERN_262934), validated against its % exhibits.
Vertical charts: bars grouped by x, value scale fitted on the y-axis tick labels.
Horizontal charts: bars grouped by y (rows), scale fitted on the x-axis tick labels; row label = words left of the bars."""
import collections
import json
import sys

import fitz

sys.stdout.reconfigure(encoding="utf-8")
d = fitz.open(sys.argv[1]) if __name__ == "__main__" else None
SKIP = {(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)}


def num(s):
    t = s.replace(",", "").replace("%", "")
    try:
        return float(t)
    except ValueError:
        return None


def fit(pairs):
    """least squares value = a + b*coord"""
    n = len(pairs)
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    sxx = sum((p[0] - mx) ** 2 for p in pairs)
    b = sum((p[0] - mx) * (p[1] - my) for p in pairs) / sxx
    return my - b * mx, b


def rects(pg):
    out = []
    for x in pg.get_drawings():
        f = x.get("fill")
        if not f:
            continue
        col = tuple(round(c, 3) for c in f)
        if col in SKIP:
            continue
        for it in x["items"]:
            if it[0] == "re" and it[1].width > 0.05 and it[1].height > 0.05:
                out.append((col, it[1]))
    return out


def legend_filter(rs):
    # legend swatches are small squares (~4x4); bars are thin in one direction but long in the other
    return [(c, r) for c, r in rs if not (abs(r.width - r.height) < 0.6 and r.width < 6)]


def vertical(pno):
    pg = d[pno - 1]
    rs = legend_filter(rects(pg))
    words = pg.get_text("words")
    # one chart per "0" y-axis tick: each rect belongs to the nearest zero-baseline at or below it
    zeros = sorted((w[1] + w[3]) / 2 for w in words if w[4] in ("0",) and w[2] < 120)
    charts = collections.defaultdict(lambda: collections.defaultdict(list))
    for c, r in rs:
        base = next((z for z in zeros if z >= r.y1 - 3), None)
        if base is None:
            continue
        charts[base][round(r.x0)].append((c, r))
    res = []
    for base, byx in sorted(charts.items()):
        bs = sorted(byx.items())
        top = min(r.y0 for _, segs in bs for _, r in segs)
        xmin = min(x for x, _ in bs)
        ticks = [(((w[1] + w[3]) / 2), num(w[4])) for w in words if num(w[4]) is not None and w[2] < xmin and top - 25 < (w[1] + w[3]) / 2 < base + 6]
        a, b = fit(ticks)
        rows = []
        for x, segs in sorted(bs):
            vals = collections.defaultdict(float)
            for c, r in segs:
                vals[c] += -b * (r.y1 - r.y0)          # height in value units (b < 0)
            rows.append({"x": x, **{str(k): round(v, 1) for k, v in vals.items()}})
        res.append({"baseline": base, "ticks": ticks, "unit_per_pt": round(-b, 3), "bars": rows})
    return res


def horizontal(pno, ymin=0.0):
    pg = d[pno - 1]
    rs = [(c, r) for c, r in legend_filter(rects(pg)) if r.y0 > ymin]
    words = pg.get_text("words")
    byy = collections.defaultdict(list)
    for c, r in rs:
        byy[round((r.y0 + r.y1) / 2)].append((c, r))
    # cluster rows into charts by shared left edge
    rows = []
    for y, segs in byy.items():
        left = min(r.x0 for _, r in segs)
        rows.append((y, left, segs))
    # split into charts where consecutive rows are > 60pt apart (row pitch inside a chart is ~20-55pt)
    rows.sort()
    groups, cur = [], []
    for y, left, segs in rows:
        if cur and y - cur[-1][0] > 60:
            groups.append(cur)
            cur = []
        cur.append((y, left, segs))
    if cur:
        groups.append(cur)
    charts = {(min(l for _, l, _ in g), g[0][0]): [(y, s) for y, _, s in g] for g in groups}
    res = []
    for (left, _), rs_ in charts.items():
        ys = [y for y, _ in rs_]
        bottom = max(ys)
        ticks = [((w[0] + w[2]) / 2, num(w[4])) for w in words if num(w[4]) is not None and bottom + 2 < (w[1] + w[3]) / 2 < bottom + 30 and w[0] > left - 15]
        if len(ticks) < 2:
            res.append({"left": left, "error": "no ticks", "n": len(rs_)})
            continue
        a, b = fit(ticks)
        out = []
        for y, segs in sorted(rs_):
            label = " ".join(w[4] for w in words if abs((w[1] + w[3]) / 2 - y) < 4 and w[2] < left - 1)
            vals = collections.defaultdict(float)
            for c, r in segs:
                vals[c] += b * (r.x1 - r.x0)
            out.append({"label": label, **{str(k): round(v, 2) for k, v in vals.items()}})
        res.append({"left": left, "unit_per_pt": round(b, 4), "ticks": ticks, "rows": out})
    return res


if __name__ == "__main__":
    mode = sys.argv[2]
    for p in sys.argv[3:]:
        pp, _, ym = p.partition(":")
        r = vertical(int(pp)) if mode == "v" else horizontal(int(pp), float(ym or 0))
        print(f"===== page {p}")
        for ch in r:
            print("-- chart", {k: v for k, v in ch.items() if k not in ("bars", "rows", "ticks")}, "ticks", [t[1] for t in ch.get("ticks", [])])
            for b in ch.get("bars", ch.get("rows", [])):
                print("   ", b)
