#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
build_credit_live.py — "AI CREDIT LIVE": the official workbook (AI_Credit_Live.xlsx, Daniel Grozdea) as a
Bloomberg-terminal-style visual page, plus an Outlook-safe e-mail edition.

Felipe 2026-10-16: "Deixe esse dashboard bem visual estilo bbg e me mande por email".

Reads  _data/credit_workbook.json           (credit_workbook.py --import / --refresh)
Writes _dashboards/credit-live.html         self-contained (inline SVG, no libraries)
       _data/credit-monitor/exports/<date>-credit-live-email.html   the e-mail body (table-based, inline styles)
Usage  py build_credit_live.py              build only
       py build_credit_live.py --send       build + e-mail Felipe (Outlook COM, page attached, Sent Items verified)

Palette (validated with the dataviz skill's validate_palette.py on a black surface, 2026-10-16): data marks
IG cyan #17a0c4 · HY amber #c48300 · widening red #d94444 · tightening blue #3a80d6 (CVD ΔE ≥ 18). The chrome amber
#ffb000 is used for headings / labels only (text tokens, never a series). Bases as in the workbook: price in
points of par, yield = YTM %, spread = OAS bp, CDS = CDS_FLAT_SPREAD bp, Barclays 15-Sep levels are YTW.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html as H
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_wiki" / "_data"
DASH = ROOT / "_wiki" / "_dashboards"
OUT = DASH / "credit-live.html"
EXPORTS = DATA / "credit-monitor" / "exports"
LAN = "http://ds-cap-33:8080/wiki/_dashboards/credit-live.html"
LAN_MONITOR = "http://ds-cap-33:8080/wiki/_dashboards/credit-monitor.html"
TO = "felipe.monteiro@capstone.com.br"

E = H.escape
IG, HY, RED, BLUE = "#17a0c4", "#c48300", "#d94444", "#3a80d6"
AMBER, INK, INK2, MUT, LINE, PANEL = "#ffb000", "#e6e9ee", "#b9c0cb", "#7d8794", "#232a35", "#0b0e13"


def n(v, dec=2, suf=""):
    return "—" if v is None else f"{v:,.{dec}f}{suf}"


def sg(v, dec=0, suf=""):
    return "—" if v is None else f"{v:+,.{dec}f}{suf}"


def ycol(y):
    return RED if (y or 0) >= 10 else AMBER if (y or 0) >= 8 else INK


# ----------------------------------------------------------------------------- SVG helpers
def hbars(rows, vmax, w=560, bar=14, gap=6, ml=118, mr=70, line=None, line_label="", fmt=lambda v: f"{v:.2f}%", color=lambda r: IG, sub=lambda r: ""):
    """Horizontal bar ladder: rows = [(label, value, row)], one axis, rounded data-ends, selective labels (values at bar ends)."""
    h = 16 + len(rows) * (bar + gap) + 18
    iw = w - ml - mr
    X = lambda v: ml + max(0.0, v) / vmax * iw
    s = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="bar ladder">']
    for t in range(0, int(vmax) + 1, max(1, int(vmax // 5) or 1)):
        s.append(f'<line class="grid" x1="{X(t):.1f}" x2="{X(t):.1f}" y1="12" y2="{h - 18}"/><text class="ax" x="{X(t):.1f}" y="{h - 5}" text-anchor="middle">{t}</text>')
    if line is not None and line <= vmax:
        s.append(f'<line class="thr" x1="{X(line):.1f}" x2="{X(line):.1f}" y1="8" y2="{h - 18}"/><text class="thr-t" x="{X(line) + 3:.1f}" y="10">{E(line_label)}</text>')
    y = 16
    for label, v, r in rows:
        c = color(r)
        s.append(f'<g class="hit" data-tip="{E(sub(r))}"><rect x="{ml}" y="{y}" width="{max(0.0, X(v) - ml):.1f}" height="{bar}" rx="3" fill="{c}" opacity=".9"/>'
                 f'<text class="lbl" x="{ml - 6}" y="{y + bar - 3}" text-anchor="end">{E(label)}</text>'
                 f'<text class="val" x="{X(v) + 5:.1f}" y="{y + bar - 3}">{E(fmt(v))}</text></g>')
        y += bar + gap
    s.append("</svg>")
    return "".join(s)


def dbars(rows, w=560, bar=14, gap=6, ml=118, mr=60, fmt=lambda v: f"{v:+.0f} bp", sub=lambda r: ""):
    """Diverging horizontal bars around zero: positive = widening (red), negative = tightening (blue)."""
    vals = [abs(v) for _, v, _ in rows] or [1]
    vmax = max(vals) * 1.08
    h = 16 + len(rows) * (bar + gap) + 18
    iw = w - ml - mr
    x0 = ml + iw / 2
    X = lambda v: x0 + v / vmax * iw / 2
    s = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="diverging bars">']
    step = max(25, int(round(vmax / 4 / 25.0)) * 25)
    t = -step * 4
    while t <= step * 4:
        if abs(t) <= vmax:
            s.append(f'<line class="grid" x1="{X(t):.1f}" x2="{X(t):.1f}" y1="12" y2="{h - 18}"/><text class="ax" x="{X(t):.1f}" y="{h - 5}" text-anchor="middle">{t:+d}</text>')
        t += step
    s.append(f'<line class="axis" x1="{x0:.1f}" x2="{x0:.1f}" y1="10" y2="{h - 16}"/>')
    y = 16
    for label, v, r in rows:
        c = RED if v >= 0 else BLUE
        x1, x2 = (x0, X(v)) if v >= 0 else (X(v), x0)
        s.append(f'<g class="hit" data-tip="{E(sub(r))}"><rect x="{x1:.1f}" y="{y}" width="{max(0.5, x2 - x1):.1f}" height="{bar}" rx="3" fill="{c}" opacity=".9"/>'
                 f'<text class="lbl" x="{ml - 6}" y="{y + bar - 3}" text-anchor="end">{E(label)}</text>'
                 f'<text class="val" x="{(x2 + 5) if v >= 0 else (x1 - 5):.1f}" y="{y + bar - 3}"{"" if v >= 0 else " text-anchor=\"end\""}>{E(fmt(v))}</text></g>')
        y += bar + gap
    s.append("</svg>")
    return "".join(s)


def dumbbell(rows, w=560, rh=20, ml=118, mr=24):
    """rows = [(label, a, b, r)] — a = project-bond OAS (amber), b = tenant comp OAS (cyan); connector = pickup."""
    vmax = max([max(a, b) for _, a, b, _ in rows] or [1]) * 1.06
    h = 16 + len(rows) * rh + 18
    iw = w - ml - mr
    X = lambda v: ml + v / vmax * iw
    s = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="OAS vs tenant comparable">']
    step = max(100, int(round(vmax / 5 / 100.0)) * 100)
    for t in range(0, int(vmax) + 1, step):
        s.append(f'<line class="grid" x1="{X(t):.1f}" x2="{X(t):.1f}" y1="12" y2="{h - 18}"/><text class="ax" x="{X(t):.1f}" y="{h - 5}" text-anchor="middle">{t}</text>')
    y = 16
    for label, a, b, r in rows:
        cy = y + rh / 2
        s.append(f'<g class="hit" data-tip="{E(r)}"><line x1="{X(min(a, b)):.1f}" x2="{X(max(a, b)):.1f}" y1="{cy:.1f}" y2="{cy:.1f}" stroke="{MUT}" stroke-width="2"/>'
                 f'<circle cx="{X(b):.1f}" cy="{cy:.1f}" r="4.5" fill="{IG}" stroke="{PANEL}" stroke-width="2"/>'
                 f'<circle cx="{X(a):.1f}" cy="{cy:.1f}" r="4.5" fill="{HY}" stroke="{PANEL}" stroke-width="2"/>'
                 f'<text class="lbl" x="{ml - 6}" y="{cy + 4:.1f}" text-anchor="end">{E(label)}</text>'
                 f'<text class="val" x="{X(max(a, b)) + 8:.1f}" y="{cy + 4:.1f}">{a - b:+.0f}</text></g>')
        y += rh
    s.append("</svg>")
    return "".join(s)


def curve(points, w=560, h=200, ml=46, mr=16, mt=16, mb=28, unit=" bp"):
    """One series line (CRWV CDS term structure)."""
    if not points:
        return '<p class="mut">no data</p>'
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    lo, hi = min(ys) * 0.96, max(ys) * 1.04
    iw, ih = w - ml - mr, h - mt - mb
    X = lambda x: ml + (x - xs[0]) / (xs[-1] - xs[0] or 1) * iw
    Y = lambda v: mt + (hi - v) / (hi - lo or 1) * ih
    s = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="term structure">']
    for i in range(5):
        v = lo + (hi - lo) * i / 4
        s.append(f'<line class="grid" x1="{ml}" x2="{w - mr}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text class="ax" x="{ml - 6}" y="{Y(v) + 4:.1f}" text-anchor="end">{v:,.0f}</text>')
    d = " ".join(f"{'M' if i == 0 else 'L'}{X(x):.1f},{Y(v):.1f}" for i, (x, v) in enumerate(points))
    s.append(f'<path d="{d}" fill="none" stroke="{HY}" stroke-width="2" stroke-linejoin="round"/>')
    for x, v in points:
        s.append(f'<g class="hit" data-tip="{x}Y: {v:,.0f}{unit}"><circle cx="{X(x):.1f}" cy="{Y(v):.1f}" r="4.5" fill="{HY}" stroke="{PANEL}" stroke-width="2"/>'
                 f'<text class="ax" x="{X(x):.1f}" y="{h - 8}" text-anchor="middle">{x}Y</text></g>')
    s.append(f'<text class="val" x="{X(xs[-1]) - 4:.1f}" y="{Y(ys[-1]) - 10:.1f}" text-anchor="end">{ys[-1]:,.0f}{unit}</text>')
    s.append("</svg>")
    return "".join(s)


def paired_bars(rows, w=560, h=220, ml=46, mr=10, mt=14, mb=34):
    """rows = [(label, now, then)] grouped bars: now (amber) vs MS desk 24-Aug (cyan). One axis."""
    vmax = max([max(a, b or 0) for _, a, b in rows] or [1]) * 1.12
    iw, ih = w - ml - mr, h - mt - mb
    gw = iw / max(1, len(rows))
    bw = min(18, gw * 0.32)
    Y = lambda v: mt + (vmax - v) / vmax * ih
    s = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="5Y CDS now vs MS desk 24-Aug">']
    for i in range(5):
        v = vmax * i / 4
        s.append(f'<line class="grid" x1="{ml}" x2="{w - mr}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text class="ax" x="{ml - 6}" y="{Y(v) + 4:.1f}" text-anchor="end">{v:,.0f}</text>')
    for i, (label, a, b) in enumerate(rows):
        cx = ml + gw * (i + 0.5)
        tip = f"{label}: {a:,.0f} bp now · MS desk 24-Aug {b:,.0f} bp · {a - b:+.0f}" if b is not None else f"{label}: {a:,.0f} bp"
        s.append(f'<g class="hit" data-tip="{E(tip)}">')
        if b is not None:
            s.append(f'<rect x="{cx - bw - 1:.1f}" y="{Y(b):.1f}" width="{bw:.1f}" height="{max(0.5, Y(0) - Y(b)):.1f}" rx="3" fill="{IG}" opacity=".9"/>')
        s.append(f'<rect x="{cx + 1:.1f}" y="{Y(a):.1f}" width="{bw:.1f}" height="{max(0.5, Y(0) - Y(a)):.1f}" rx="3" fill="{HY}" opacity=".9"/>'
                 f'<text class="ax" x="{cx:.1f}" y="{h - 16}" text-anchor="middle">{E(label)}</text>'
                 f'<text class="val" x="{cx + 1 + bw / 2:.1f}" y="{Y(a) - 4:.1f}" text-anchor="middle">{a:,.0f}</text></g>')
    s.append("</svg>")
    return "".join(s)


# ----------------------------------------------------------------------------- page
def build(wb):
    T = wb["totals"]
    proj = [b for b in wb["bonds"] if b["section"] in ("IG", "HY")]
    comps = [b for b in wb["bonds"] if b["section"] == "Parent"]
    sec_color = lambda b: IG if b["section"] == "IG" else HY
    asof = wb.get("values_asof") or "—"
    stamp = (wb.get("refreshed_at") or wb.get("imported_at") or "")[:16].replace("T", " ")
    rf = wb.get("refresh") or {}
    hot = sorted((b for b in proj if (b.get("yld") or 0) >= 10), key=lambda b: -b["yld"])
    crwv = {c["name"].split()[-1]: c for c in wb["cds"] if c["name"].startswith("CRWV")}
    crwv_pts = [(int(k[:-1]), c["spread_bp"]) for k, c in crwv.items() if c.get("spread_bp") is not None]
    crwv_pts.sort()
    five = [c for c in wb["cds"] if c["name"].endswith("5Y") and not c["name"].startswith("CRWV") and c.get("spread_bp") is not None]

    # ticker strip
    strip = [("IG w-avg px", n(T["IG"]["wavg_price"]), f'{T["IG"]["n"]} bonds · ${T["IG"]["face_mn"] / 1000:.1f}bn face'),
             ("HY w-avg px", n(T["HY"]["wavg_price"]), f'{T["HY"]["n"]} bonds · ${T["HY"]["face_mn"] / 1000:.1f}bn face'),
             ("Principal below par", f'${(T["IG"]["par_mn"] + T["HY"]["par_mn"]) / 1000:,.2f}bn', f'IG {T["IG"]["par_mn"] / 1000:,.2f} · HY {T["HY"]["par_mn"] / 1000:,.2f}'),
             ("Since 15-Sep", f'${(T["IG"]["since_sep_mn"] + T["HY"]["since_sep_mn"]) / 1000:,.2f}bn', "value change vs Barclays 15-Sep prices"),
             ("≥ 10% yield", f"{len(hot)} / {len(proj)}", "; ".join(f"{b['ticker']} {b['yld']:.1f}" for b in hot[:4]) or "none"),
             ("CRWV 5Y CDS", f'{n(crwv.get("5Y", {}).get("spread_bp"), 0)} bp', f'flat spread · Δ vs snapshot {sg(crwv.get("5Y", {}).get("d_snapshot_bp"))}'),
             ("CRWV 9¾ 2031", f'{n(next((b["yld"] for b in comps if b["ticker"] == "CRWV"), None))}%', f'px {n(next((b["px"] for b in comps if b["ticker"] == "CRWV"), None))} · OAS {n(next((b["oas_bp"] for b in comps if b["ticker"] == "CRWV"), None), 0)} bp'),
             ("ORCL 4.95 2031", f'{n(next((b["yld"] for b in comps if b["ticker"] == "ORCL"), None))}%', f'px {n(next((b["px"] for b in comps if b["ticker"] == "ORCL"), None))} · OAS {n(next((b["oas_bp"] for b in comps if b["ticker"] == "ORCL"), None), 0)} bp')]
    strip_html = "".join(f'<div class="kpi"><div class="kl">{E(k)}</div><div class="kv">{E(v)}</div><div class="kd">{E(d)}</div></div>' for k, v, d in strip)

    # charts
    ladder = hbars([(b["ticker"], b["yld"], b) for b in sorted(proj, key=lambda b: -(b["yld"] or 0)) if b.get("yld") is not None],
                   vmax=max(b["yld"] for b in proj if b.get("yld")) * 1.12, line=10, line_label="10% line", color=sec_color,
                   sub=lambda b: f"{b['name']} · tenant {b['tenant']} · {b['rating']} · px {n(b['px'], 3)} · OAS {n(b['oas_bp'], 0)} bp")
    dsep = dbars([(b["ticker"], b["dyld_since_sep_bp"], b) for b in sorted(proj, key=lambda b: -(b["dyld_since_sep_bp"] or 0)) if b.get("dyld_since_sep_bp") is not None],
                 sub=lambda b: f"{b['ticker']}: {n((b.get('barclays') or {}).get('ytw_0915'))}% YTW on 15-Sep → {n(b['yld'])}% YTM now · value since 15-Sep ${n(b['since_sep_mn'], 0)}mn")
    pk = dumbbell([(b["ticker"], b["oas_bp"], b["comp_oas_bp"], f"{b['ticker']} OAS {n(b['oas_bp'], 0)} vs {b['comp_name']} {n(b['comp_oas_bp'], 0)} · pickup {sg(b['pickup_bp'])} bp (15-Sep {sg(b['pickup_sep_bp'])})")
                   for b in sorted(proj, key=lambda b: -(b["pickup_bp"] or 0)) if b.get("oas_bp") is not None and b.get("comp_oas_bp") is not None])
    par = dbars([(b["ticker"], b["par_mn"], b) for b in sorted(proj, key=lambda b: (b["par_mn"] or 0)) if b.get("par_mn") is not None],
                fmt=lambda v: f"{v:+,.0f}", sub=lambda b: f"{b['ticker']}: px {n(b['px'], 3)} on ${n(b['amt_mn'], 0)}mn → {n(b['par_pct'] * 100, 1)}% of face")
    cds_curve = curve(crwv_pts)
    cds_bars = paired_bars([(c["name"].split()[0], c["spread_bp"], c.get("ms_desk_0824_bp")) for c in five])

    # equity heat tiles
    tiles = []
    for e in sorted(wb["equities"], key=lambda e: (e.get("chg_pct_1d") or 0)):
        c = e.get("chg_pct_1d")
        a = min(1.0, abs(c or 0) / 12)
        bg = f"color-mix(in srgb, {RED if (c or 0) < 0 else BLUE} {int(12 + a * 55)}%, {PANEL})"
        rv = e.get("relvol") or 0
        tiles.append(f'<div class="eq" style="background:{bg}" data-tip="{E(e.get("why") or "")} · {E(e["bbg"])} · vol {n(e.get("volume"), 0)} vs 30d avg {n(e.get("vol_avg_30d"), 0)}">'
                     f'<div class="eqn">{E(e["name"])}</div><div class="eqv">{sg(c, 1, "%")}</div><div class="eqd">{n(e.get("px"))} · {n(rv, 1, "x")} vol{" ▲" if rv >= 1.5 else ""}</div></div>')

    # monitor table
    trs = []
    for sec, lab in (("IG", "INVESTMENT GRADE · HPC DATA CENTER BUILDERS"), ("HY", "HIGH YIELD · HPC DATA CENTER BUILDERS"), ("Parent", "TENANT / PARENT COMPARABLES")):
        bs = [b for b in wb["bonds"] if b["section"] == sec]
        trs.append(f'<tr class="cat"><td colspan="13">{lab}</td></tr>')
        for b in bs:
            yc = ycol(b.get("yld"))
            d15 = b.get("dyld_since_sep_bp")
            dc = RED if (d15 or 0) >= 25 else BLUE if (d15 or 0) <= -25 else INK2
            pkv = b.get("pickup_bp")
            trs.append(f'<tr><td><b>{E(b["ticker"])}</b> <span class="src">{E((b["name"] or "")[:52])}</span></td><td>{E(b.get("tenant") or "")}</td>'
                       f'<td class="r">{n(b.get("mw"), 0)}</td><td class="src">{E(b.get("rating") or "")}</td><td class="r">{n(b.get("amt_mn"), 0)}</td>'
                       f'<td class="r">{n(b.get("px"), 3)}</td><td class="r" style="color:{RED if (b.get("chg_pct_1d") or 0) < 0 else BLUE}">{sg(b.get("chg_pct_1d"), 2, "%")}</td>'
                       f'<td class="r" style="color:{yc}"><b>{n(b.get("yld"), 2)}</b></td><td class="r">{n(b.get("oas_bp"), 0)}</td>'
                       f'<td class="r" style="color:{dc}">{sg(d15)}</td><td class="r" style="color:{BLUE if (pkv or 0) < 0 else INK}">{sg(pkv)} <span class="src">{E(b.get("comp_name") or "")}</span></td>'
                       f'<td class="r">{n(b.get("par_mn"), 0)}</td><td>{E(b.get("barclays_rec") or "")}</td></tr>')
        if sec in ("IG", "HY"):
            t = T[sec]
            trs.append(f'<tr class="tot"><td>{sec} TOTAL</td><td colspan="3"></td><td class="r">{n(t["face_mn"], 0)}</td><td class="r">{n(t["wavg_price"], 3)}</td><td colspan="5"></td><td class="r">{n(t["par_mn"], 0)}</td><td></td></tr>')
    monitor = ("<table><thead><tr><th>BOND</th><th>TENANT</th><th class='r'>MW</th><th>RTG</th><th class='r'>AMT $MN</th><th class='r'>PX</th><th class='r'>1D</th>"
               "<th class='r'>YTM %</th><th class='r'>OAS</th><th class='r'>Δ15-SEP</th><th class='r'>PICKUP vs COMP</th><th class='r'>vs PAR $MN</th><th>BARC</th></tr></thead>"
               f"<tbody>{''.join(trs)}</tbody></table>")

    # other instruments
    ors, grp = [], None
    for o in wb["other"]:
        if o["group"] != grp:
            grp = o["group"]; ors.append(f'<tr class="cat"><td colspan="8">{E(grp.upper())}</td></tr>')
        yc = ycol(o.get("yld")) if o["kind"] == "bond" else INK2
        ors.append(f'<tr><td><b>{E(o["name"])}</b> <span class="src">{E(o["kind"])}</span></td><td class="r">{n(o.get("amt_mn"), 0)}</td><td class="r">{n(o.get("px"), 3)}</td>'
                   f'<td class="r" style="color:{RED if (o.get("chg_pct_1d") or 0) < 0 else BLUE}">{sg(o.get("chg_pct_1d"), 2, "%")}</td><td class="r" style="color:{yc}">{n(o.get("yld"), 2)}</td>'
                   f'<td class="r" style="color:{RED if (o.get("dyld_vs_snapshot_bp") or 0) >= 25 else INK2}">{sg(o.get("dyld_vs_snapshot_bp"))}</td><td class="r">{n(o.get("par_mn"), 0)}</td><td class="src">{E(o.get("rating_sp") or "")}</td></tr>')
    other = ("<table><thead><tr><th>INSTRUMENT</th><th class='r'>AMT $MN</th><th class='r'>PX</th><th class='r'>1D</th><th class='r'>YTM %</th><th class='r'>Δ vs SNAP</th><th class='r'>vs PAR $MN</th><th>S&amp;P</th></tr></thead>"
             f"<tbody>{''.join(ors)}</tbody></table>")
    cds_tbl = ("<table><thead><tr><th>CDS</th><th class='r'>FLAT bp</th><th class='r'>Δ SNAP</th><th class='r'>MS 24-AUG</th><th class='r'>Δ MS</th></tr></thead><tbody>"
               + "".join(f'<tr><td>{E(c["name"])}</td><td class="r"><b>{n(c.get("spread_bp"), 0)}</b></td><td class="r" style="color:{RED if (c.get("d_snapshot_bp") or 0) > 0 else INK2}">{sg(c.get("d_snapshot_bp"))}</td><td class="r">{n(c.get("ms_desk_0824_bp"), 0)}</td><td class="r" style="color:{RED if (c.get("d_vs_ms_bp") or 0) > 0 else INK2}">{sg(c.get("d_vs_ms_bp"))}</td></tr>' for c in wb["cds"]) + "</tbody></table>")

    css = f"""
:root{{color-scheme:dark}}
*{{box-sizing:border-box;margin:0}}
body{{background:#000;color:{INK};font:13px/1.45 Consolas,"IBM Plex Mono","Cascadia Mono",Menlo,monospace;padding:0 0 60px}}
.top{{background:#000;border-bottom:2px solid {AMBER};padding:10px 18px;display:flex;flex-wrap:wrap;gap:10px 24px;align-items:baseline}}
.top h1{{color:{AMBER};font-size:20px;letter-spacing:.14em;font-weight:700}}
.top .st{{color:{INK2};font-size:12px}} .top .st b{{color:{INK}}} .top a{{color:{IG};text-decoration:none}}
.strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:{LINE};border-bottom:1px solid {LINE}}}
.kpi{{background:{PANEL};padding:8px 12px}} .kl{{color:{AMBER};font-size:10.5px;letter-spacing:.12em;text-transform:uppercase}} .kv{{font-size:22px;font-weight:700;margin-top:2px;font-variant-numeric:tabular-nums}} .kd{{color:{MUT};font-size:11px;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.wrap{{padding:14px 18px;display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:14px}}
.panel{{background:{PANEL};border:1px solid {LINE};padding:10px 12px 8px;min-width:0}} .panel.wide{{grid-column:1/-1}}
.ph{{display:flex;justify-content:space-between;gap:12px;align-items:baseline;border-bottom:1px solid {LINE};padding-bottom:6px;margin-bottom:8px}}
.ph h2{{color:{AMBER};font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:700}} .ph .n{{color:{MUT};font-size:11px}}
.legend{{display:flex;gap:16px;flex-wrap:wrap;color:{INK2};font-size:11px;margin:4px 0 2px}} .sw{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}}
svg{{width:100%;height:auto;display:block}} .grid{{stroke:{LINE};stroke-width:1}} .axis{{stroke:{MUT};stroke-width:1}} .ax{{fill:{MUT};font-size:10px}} .lbl{{fill:{INK2};font-size:10.5px}} .val{{fill:{INK};font-size:10.5px;font-weight:700}}
.thr{{stroke:{RED};stroke-width:1}} .thr-t{{fill:{RED};font-size:10px}}
.hit{{cursor:default}} .hit:hover rect,.hit:hover circle{{filter:brightness(1.25)}}
table{{border-collapse:collapse;width:100%;font-size:12px;font-variant-numeric:tabular-nums}} th{{color:{AMBER};font-size:10.5px;letter-spacing:.08em;text-align:left;padding:5px 7px;border-bottom:1px solid {AMBER};font-weight:700}}
td{{padding:4px 7px;border-bottom:1px solid #141922;vertical-align:top;white-space:nowrap}} .r{{text-align:right}} th.r{{text-align:right}}
tr.cat td{{color:{IG};font-size:10.5px;letter-spacing:.1em;padding-top:9px;border-bottom:1px solid {LINE}}} tr.tot td{{color:{AMBER};font-weight:700;border-top:1px solid {LINE}}}
.src{{color:{MUT};font-size:10.5px}} .mut{{color:{MUT}}} .tscroll{{overflow-x:auto}}
.eqgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:6px}} .eq{{border:1px solid {LINE};padding:7px 8px;border-radius:3px}} .eqn{{font-size:11px;color:{INK2};white-space:nowrap;overflow:hidden;text-overflow:ellipsis}} .eqv{{font-size:18px;font-weight:700;font-variant-numeric:tabular-nums}} .eqd{{font-size:10.5px;color:{MUT}}}
details summary{{cursor:pointer;color:{IG};font-size:11.5px;margin-top:6px}}
#tip{{position:fixed;pointer-events:none;background:#141922;border:1px solid {AMBER};color:{INK};padding:5px 8px;font-size:11px;max-width:420px;display:none;z-index:9}}
footer{{padding:12px 18px;color:{MUT};font-size:11px;border-top:1px solid {LINE}}}
@media (max-width:640px){{.wrap{{grid-template-columns:1fr;padding:10px}} .panel.wide{{grid-column:auto}}}}
"""
    js = """
const tip=document.createElement('div');tip.id='tip';document.body.appendChild(tip);
document.querySelectorAll('[data-tip]').forEach(el=>{el.addEventListener('mousemove',ev=>{tip.textContent=el.dataset.tip;tip.style.display='block';const r=tip.getBoundingClientRect();tip.style.left=Math.min(ev.clientX+14,innerWidth-r.width-10)+'px';tip.style.top=Math.max(6,ev.clientY-r.height-10)+'px';});el.addEventListener('mouseleave',()=>tip.style.display='none');});
"""
    leg_sec = f'<div class="legend"><span><i class="sw" style="background:{IG}"></i>IG builders</span><span><i class="sw" style="background:{HY}"></i>HY builders</span><span><i class="sw" style="background:{RED};width:18px;height:2px;vertical-align:3px"></i>10% line (MS: HY DC deals get pulled near ~10%)</span></div>'
    leg_div = f'<div class="legend"><span><i class="sw" style="background:{RED}"></i>wider / lower value</span><span><i class="sw" style="background:{BLUE}"></i>tighter / higher value</span></div>'
    leg_pk = f'<div class="legend"><span><i class="sw" style="background:{HY};border-radius:50%"></i>project bond OAS</span><span><i class="sw" style="background:{IG};border-radius:50%"></i>tenant / parent comp OAS</span><span>label = pickup (bond − comp), bp</span></div>'
    leg_cds = f'<div class="legend"><span><i class="sw" style="background:{HY}"></i>now (CDS_FLAT_SPREAD)</span><span><i class="sw" style="background:{IG}"></i>MS Credit Trading desk, 24-Aug-2026</span></div>'
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Credit Live</title><meta name="description" content="Data-center project bonds, comps, CDS and the equity tape from the official AI_Credit_Live workbook, terminal view."><style>{css}</style></head><body>
<header class="top"><h1>AI CREDIT LIVE</h1><span class="st">OFFICIAL WORKBOOK · <b>AI_Credit_Live.xlsx</b> · Daniel Grozdea · Barclays IG/HY DC comp-sheet layout 16-Sep-2026</span>
<span class="st">VALUES <b>{E(asof)}</b> {E(stamp)} · {E(wb.get("values_source_key", ""))} · refresh <b>{E(rf.get("status", "—"))}</b>{(" · " + E(rf.get("detail", ""))) if rf.get("detail") else ""}</span>
<span class="st"><a href="credit-monitor.html">← credit monitor</a> · <a href="index.html">hub</a> · <a href="../_data/credit-monitor/workbook/AI_Credit_Live.xlsx">xlsx</a></span></header>
<div class="strip">{strip_html}</div>
<main class="wrap">
<section class="panel"><div class="ph"><h2>Yield ladder — project bonds, YTM %</h2><span class="n">{len(proj)} bonds · sorted</span></div>{leg_sec}{ladder}</section>
<section class="panel"><div class="ph"><h2>Δ yield since Barclays 15-Sep, bp</h2><span class="n">YTW 15-Sep → YTM now (approx.)</span></div>{leg_div}{dsep}</section>
<section class="panel"><div class="ph"><h2>OAS pickup vs tenant comparable, bp</h2><span class="n">negative = project bond tighter than the tenant's own bond</span></div>{leg_pk}{pk}</section>
<section class="panel"><div class="ph"><h2>Principal vs par, $mn per issue</h2><span class="n">(px − 100)/100 × amount outstanding</span></div>{leg_div}{par}</section>
<section class="panel"><div class="ph"><h2>CoreWeave CDS term structure, bp</h2><span class="n">CDS_FLAT_SPREAD · 1Y–10Y</span></div>{cds_curve}</section>
<section class="panel"><div class="ph"><h2>5Y CDS — now vs MS desk marks 24-Aug</h2><span class="n">hyperscalers · vendors · ORCL · SPCX</span></div>{leg_cds}{cds_bars}</section>
<section class="panel wide"><div class="ph"><h2>Equity tape — issuers &amp; tenants, 1d %</h2><span class="n">tile intensity = size of the move · ▲ = volume ≥ 1.5× 30-day average</span></div><div class="eqgrid">{''.join(tiles)}</div></section>
<section class="panel wide"><div class="ph"><h2>Monitor — project bonds &amp; comps</h2><span class="n">YTM red ≥ 10% · amber ≥ 8% · Δ15-Sep red ≥ +25bp · pickup blue = negative</span></div><div class="tscroll">{monitor}</div></section>
<section class="panel wide"><div class="ph"><h2>Other instruments — vendor &amp; hyperscaler notes, neocloud converts / HY / loans, comparator bonds</h2><span class="n">{len(wb["other"])} instruments · snapshot ref {E(wb.get("snapshot_ref") or "—")}</span></div><div class="tscroll">{other}</div></section>
<section class="panel"><div class="ph"><h2>CDS table</h2><span class="n">flat spreads, bp</span></div><div class="tscroll">{cds_tbl}</div></section>
<section class="panel"><div class="ph"><h2>Reading this page</h2></div><p class="mut" style="font-size:11.5px;line-height:1.6">Price in points of par · yield = Bloomberg YLD_YTM_MID · spread = OAS_SPREAD_MID · CDS = CDS_FLAT_SPREAD (not the issuer board's PX_LAST series on the credit monitor) · Barclays 15-Sep and 3-Aug levels are YTW, so changes since then are approximate · converts and loans are measured against par for comparability only · composite quotes refresh about every 15 s and are not trades · equity relative volume = today / 30-day average. Values are re-pulled through the local Bloomberg terminal by the credit-alerts lane (09:30 / 18:30 São Paulo) and the Friday brief; the workbook itself is live when opened in Excel with the Bloomberg add-in. Every line of the deal dossiers (SEC filings, indentures, releases) is in the credit monitor's workbook section.</p></section>
</main>
<footer>Capstone · internal research · built {dt.datetime.now().isoformat(timespec="minutes")} from <code>_data/credit_workbook.json</code> (source: {E(wb.get("source", ""))}) · page: <code>_tools/build_credit_live.py</code></footer>
<script>{js}</script></body></html>"""
    return page


# ----------------------------------------------------------------------------- e-mail edition (Outlook Word renderer: tables + inline styles only)
def email_html(wb, date):
    T = wb["totals"]
    proj = [b for b in wb["bonds"] if b["section"] in ("IG", "HY")]
    hot = sorted((b for b in proj if (b.get("yld") or 0) >= 10), key=lambda b: -b["yld"])
    crwv = {c["name"].split()[-1]: c for c in wb["cds"] if c["name"].startswith("CRWV")}
    F = "font-family:Consolas,Courier New,monospace;"  # no quotes: the string sits inside single-quoted style attributes
    TD = F + "font-size:12px;color:#e6e9ee;padding:4px 7px;border-bottom:1px solid #1b2129;white-space:nowrap"
    TDR = TD + ";text-align:right"
    TH = F + "font-size:10.5px;color:#ffb000;padding:5px 7px;border-bottom:1px solid #ffb000;text-align:left;letter-spacing:1px"
    THR = TH + ";text-align:right"
    CAT = F + "font-size:10.5px;color:#17a0c4;padding:9px 7px 3px;letter-spacing:1px"
    H2 = F + "font-size:12.5px;color:#ffb000;letter-spacing:2px;margin:18px 0 6px"

    def kpi(k, v, d):
        return (f"<td bgcolor='#0b0e13' style='{F}padding:8px 12px;border:1px solid #232a35;vertical-align:top'><div style='font-size:10px;color:#ffb000;letter-spacing:1px'>{E(k)}</div>"
                f"<div style='font-size:20px;font-weight:bold;color:#e6e9ee'>{E(v)}</div><div style='font-size:10.5px;color:#7d8794'>{E(d)}</div></td>")
    kpis = [("IG W-AVG PX", n(T["IG"]["wavg_price"]), f'{T["IG"]["n"]} bonds · ${T["IG"]["face_mn"] / 1000:.1f}bn'),
            ("HY W-AVG PX", n(T["HY"]["wavg_price"]), f'{T["HY"]["n"]} bonds · ${T["HY"]["face_mn"] / 1000:.1f}bn'),
            ("BELOW PAR", f'${(T["IG"]["par_mn"] + T["HY"]["par_mn"]) / 1000:,.2f}bn', f'since 15-Sep ${(T["IG"]["since_sep_mn"] + T["HY"]["since_sep_mn"]) / 1000:,.2f}bn'),
            ("≥ 10% YIELD", f"{len(hot)} / {len(proj)}", "; ".join(f"{b['ticker']} {b['yld']:.1f}" for b in hot[:3]) or "none"),
            ("CRWV 5Y CDS", f'{n(crwv.get("5Y", {}).get("spread_bp"), 0)} bp', f'1Y {n(crwv.get("1Y", {}).get("spread_bp"), 0)} · 10Y {n(crwv.get("10Y", {}).get("spread_bp"), 0)}')]
    parts = [f"<table width='100%' cellpadding='0' cellspacing='0' bgcolor='#000000' style='background:#000000'><tr><td bgcolor='#000000' style='padding:14px;{F}'>",
             f"<table width='100%' cellpadding='0' cellspacing='0' bgcolor='#000000'><tr><td style='{F}font-size:19px;color:#ffb000;letter-spacing:3px;font-weight:bold;border-bottom:2px solid #ffb000;padding-bottom:6px'>AI CREDIT LIVE</td>"
             f"<td align='right' style='{F}font-size:11px;color:#b9c0cb;border-bottom:2px solid #ffb000;padding-bottom:6px'>official workbook AI_Credit_Live.xlsx (Daniel Grozdea) · values {E(wb.get('values_asof') or '')} {E((wb.get('refreshed_at') or '')[11:16])} · {E(wb.get('values_source_key', ''))}</td></tr></table>",
             "<table width='100%' cellpadding='0' cellspacing='4' style='margin-top:8px'><tr>" + "".join(kpi(*k) for k in kpis) + "</tr></table>"]
    # monitor
    rows = []
    for sec, lab in (("IG", "INVESTMENT GRADE · HPC DC BUILDERS"), ("HY", "HIGH YIELD · HPC DC BUILDERS"), ("Parent", "TENANT / PARENT COMPARABLES")):
        rows.append(f"<tr><td colspan='9' style='{CAT}'>{lab}</td></tr>")
        for b in [b for b in wb["bonds"] if b["section"] == sec]:
            yc = ycol(b.get("yld")); d15 = b.get("dyld_since_sep_bp")
            dc = RED if (d15 or 0) >= 25 else BLUE if (d15 or 0) <= -25 else "#b9c0cb"
            rows.append(f"<tr><td style='{TD}'><b>{E(b['ticker'])}</b> <font color='#7d8794' style='font-size:10.5px'>{E((b.get('tenant') or '')[:28])}</font></td>"
                        f"<td style='{TDR}'>{n(b.get('amt_mn'), 0)}</td><td style='{TDR}'>{n(b.get('px'), 2)}</td>"
                        f"<td style='{TDR}'><font color='{RED if (b.get('chg_pct_1d') or 0) < 0 else BLUE}'>{sg(b.get('chg_pct_1d'), 2, '%')}</font></td>"
                        f"<td style='{TDR}'><font color='{yc}'><b>{n(b.get('yld'), 2)}</b></font></td><td style='{TDR}'>{n(b.get('oas_bp'), 0)}</td>"
                        f"<td style='{TDR}'><font color='{dc}'>{sg(d15)}</font></td><td style='{TDR}'><font color='{BLUE if (b.get('pickup_bp') or 0) < 0 else '#e6e9ee'}'>{sg(b.get('pickup_bp'))}</font></td>"
                        f"<td style='{TDR}'>{n(b.get('par_mn'), 0)}</td></tr>")
        if sec in ("IG", "HY"):
            t = T[sec]
            rows.append(f"<tr><td style='{TD};color:#ffb000;border-top:1px solid #232a35'><b>{sec} TOTAL</b></td><td style='{TDR};color:#ffb000;border-top:1px solid #232a35'><b>{n(t['face_mn'], 0)}</b></td>"
                        f"<td style='{TDR};color:#ffb000;border-top:1px solid #232a35'><b>{n(t['wavg_price'], 2)}</b></td><td colspan='5' style='{TD};border-top:1px solid #232a35'></td><td style='{TDR};color:#ffb000;border-top:1px solid #232a35'><b>{n(t['par_mn'], 0)}</b></td></tr>")
    parts.append(f"<div style='{H2}'>MONITOR — PROJECT BONDS &amp; COMPS <font color='#7d8794' style='letter-spacing:0;font-size:10.5px'>(YTM red ≥ 10% · amber ≥ 8% · Δ15-Sep red ≥ +25bp · pickup blue = tighter than the tenant's own bond)</font></div>")
    parts.append(f"<table width='100%' cellpadding='0' cellspacing='0' bgcolor='#0b0e13'><tr><th style='{TH}'>BOND · TENANT</th><th style='{THR}'>AMT $MN</th><th style='{THR}'>PX</th><th style='{THR}'>1D</th><th style='{THR}'>YTM %</th><th style='{THR}'>OAS</th><th style='{THR}'>Δ15-SEP</th><th style='{THR}'>PICKUP</th><th style='{THR}'>vs PAR $MN</th></tr>{''.join(rows)}</table>")
    # CDS + equities side by side
    cds = "".join(f"<tr><td style='{TD}'>{E(c['name'])}</td><td style='{TDR}'><b>{n(c.get('spread_bp'), 0)}</b></td><td style='{TDR}'><font color='{RED if (c.get('d_snapshot_bp') or 0) > 0 else '#b9c0cb'}'>{sg(c.get('d_snapshot_bp'))}</font></td><td style='{TDR}'>{n(c.get('ms_desk_0824_bp'), 0)}</td><td style='{TDR}'><font color='{RED if (c.get('d_vs_ms_bp') or 0) > 0 else '#b9c0cb'}'>{sg(c.get('d_vs_ms_bp'))}</font></td></tr>" for c in wb["cds"])
    eqs = "".join(f"<tr><td style='{TD}'>{E(e['name'])}</td><td style='{TDR}'>{n(e.get('px'))}</td><td style='{TDR}'><font color='{RED if (e.get('chg_pct_1d') or 0) < 0 else BLUE}'><b>{sg(e.get('chg_pct_1d'), 1, '%')}</b></font></td><td style='{TDR}'><font color='{AMBER if (e.get('relvol') or 0) >= 1.5 else '#b9c0cb'}'>{n(e.get('relvol'), 1, 'x')}</font></td></tr>" for e in sorted(wb["equities"], key=lambda e: (e.get("chg_pct_1d") or 0)))
    parts.append("<table width='100%' cellpadding='0' cellspacing='0'><tr><td width='55%' valign='top' style='padding-right:10px'>"
                 f"<div style='{H2}'>CDS FLAT SPREADS, bp</div><table width='100%' cellpadding='0' cellspacing='0' bgcolor='#0b0e13'><tr><th style='{TH}'>CDS</th><th style='{THR}'>NOW</th><th style='{THR}'>Δ SNAP</th><th style='{THR}'>MS 24-AUG</th><th style='{THR}'>Δ MS</th></tr>{cds}</table></td>"
                 f"<td width='45%' valign='top'><div style='{H2}'>EQUITY TAPE, 1D</div><table width='100%' cellpadding='0' cellspacing='0' bgcolor='#0b0e13'><tr><th style='{TH}'>EQUITY</th><th style='{THR}'>PX</th><th style='{THR}'>1D</th><th style='{THR}'>REL VOL</th></tr>{eqs}</table></td></tr></table>")
    # CRWV + neocloud debt
    cv = [o for o in wb["other"] if o["name"].startswith(("CRWV", "NBIS", "SOFTBK", "SPCX")) or o["group"].startswith("Neocloud")]
    seen, cvr = set(), []
    for o in cv:
        if o["name"] in seen:
            continue
        seen.add(o["name"])
        cvr.append(f"<tr><td style='{TD}'>{E(o['name'])} <font color='#7d8794' style='font-size:10.5px'>{E(o['kind'])}</font></td><td style='{TDR}'>{n(o.get('amt_mn'), 0)}</td><td style='{TDR}'>{n(o.get('px'), 2)}</td><td style='{TDR}'><font color='{RED if (o.get('chg_pct_1d') or 0) < 0 else BLUE}'>{sg(o.get('chg_pct_1d'), 2, '%')}</font></td><td style='{TDR}'><font color='{ycol(o.get('yld')) if o['kind'] == 'bond' else '#b9c0cb'}'>{n(o.get('yld'), 2)}</font></td><td style='{TDR}'><font color='{RED if (o.get('dyld_vs_snapshot_bp') or 0) >= 25 else '#b9c0cb'}'>{sg(o.get('dyld_vs_snapshot_bp'))}</font></td></tr>")
    parts.append(f"<div style='{H2}'>NEOCLOUD / MINER DEBT &amp; CONVERTS, SPACEX, SOFTBANK</div><table width='100%' cellpadding='0' cellspacing='0' bgcolor='#0b0e13'><tr><th style='{TH}'>INSTRUMENT</th><th style='{THR}'>AMT $MN</th><th style='{THR}'>PX</th><th style='{THR}'>1D</th><th style='{THR}'>YTM %</th><th style='{THR}'>Δ vs SNAP</th></tr>{''.join(cvr)}</table>")
    parts.append(f"<div style='{F}font-size:11px;color:#7d8794;margin-top:16px;border-top:1px solid #232a35;padding-top:8px'>Charts (yield ladder, Δ since 15-Sep, OAS pickup dumbbells, principal vs par, CRWV CDS curve, 5Y CDS vs MS desk) are in the attached page and live at <a href='{LAN}' style='color:#17a0c4'>{LAN}</a> · research, alerts and dossiers: <a href='{LAN_MONITOR}' style='color:#17a0c4'>credit monitor</a>.<br>"
                 "Bases: price pts of par · yield YLD_YTM_MID % · spread OAS_SPREAD_MID bp · CDS CDS_FLAT_SPREAD bp (not the issuer board's PX_LAST) · Barclays 15-Sep levels are YTW (changes approximate) · converts/loans vs par for comparability only · composite quotes, not trades. "
                 "Source: AI_Credit_Live.xlsx, Daniel Grozdea (Capstone); layout Barclays IG/HY Data Center Comp Sheets 16-Sep-2026; MS Credit Trading desk CDS 24-Aug-2026. Capstone internal research.</div></td></tr></table>")
    return "".join(parts)


def send(body_html, subject, attachment: Path):
    import win32com.client
    app = win32com.client.Dispatch("Outlook.Application")
    ns = app.GetNamespace("MAPI")
    mail = app.CreateItem(0)
    mail.To = TO
    mail.Subject = subject
    mail.HTMLBody = body_html
    mail.Attachments.Add(str(attachment))
    mail.Send()
    sent = ns.GetDefaultFolder(5).Items
    sent.Sort("[CreationTime]", True)
    for _ in range(12):
        time.sleep(10)
        it, k = sent.GetFirst(), 0
        while it is not None and k < 60:
            if str(getattr(it, "Subject", "")) == subject:
                return {"status": "sent", "entry_id": it.EntryID, "sent_on": str(it.SentOn)[:19]}
            it = sent.GetNext(); k += 1
    return {"status": "queued_or_unknown"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--send", action="store_true", help="e-mail Felipe (Outlook COM): terminal-style body + the page attached")
    a = ap.parse_args()
    wb = json.loads((DATA / "credit_workbook.json").read_text(encoding="utf-8"))
    page = build(wb)
    OUT.write_text(page, encoding="utf-8")
    print(f"credit live -> {OUT}  ({OUT.stat().st_size // 1024} KB)")
    date = dt.date.today().isoformat()
    EXPORTS.mkdir(parents=True, exist_ok=True)
    body = email_html(wb, date)
    bpath = EXPORTS / f"{date}-credit-live-email.html"
    bpath.write_text(body, encoding="utf-8")
    apath = EXPORTS / f"{date}-credit-live.html"
    apath.write_text(page, encoding="utf-8")
    print(f"e-mail body -> {bpath}")
    if a.send:
        subject = f"AI Credit Live | {date} | terminal view — official workbook AI_Credit_Live.xlsx"
        rec = send(body, subject, apath)
        rec.update(subject=subject, to=TO, body=str(bpath), attachment=str(apath), at=dt.datetime.now().isoformat(timespec="seconds"))
        (EXPORTS / f"{date}-credit-live-receipt.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
        print(json.dumps(rec, indent=1))
        return 0 if rec["status"] == "sent" else 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
