#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
credit_alerts.py — daily AI credit ALERTS (single-name CDS / bonds / equities / index spreads + the broker tape).

Why: on 2026-10-13 CoreWeave's 5Y CDS went back to its late-July high (~1,000bp, Rothschild & Co TMT Daily 10-14)
and nothing flagged it — the weekly credit monitor tracks four index-level series on Fridays, and its 10-09
e-mail had failed on the Outlook OST limit. This script is the daily layer on top of that monitor.

Two layers, both attributed:
  MARKET   _data/credit_watch.json (fetch_credit_watch.py): per instrument the 1-day and 5-observation change in
           its own unit (bp for spreads, % for equities), the trailing-60-observation sigma, new 60d / 1y highs and
           hand-set level lines (rules in _data/credit_watch_config.json). Spreads alert on widening, equities on
           down moves. The Bloomberg observation date is always printed — never 'today' by assumption.
  MAIL     the Outlook window (credit_mail_collect.ps1): credit terms within N chars of a watched name, grouped by
           company and distinct firm; every excerpt carries sender firm / name / received time.

Writes  _data/credit-monitor/alerts/latest.json        everything the dashboard renders (watch table + alerts)
        _data/credit-monitor/alerts/log.jsonl          one line per run (heartbeat) and per alert
        _data/credit-monitor/alerts/state.json         de-dup memory (per instrument observation date, mail ids)
        _data/credit-monitor/alerts/emails/<stamp>.html the rendered e-mail (dry run or sent)
        _data/credit-monitor/alerts/receipts/<stamp>.json delivery record (Sent Items verified, not 'submitted')
Usage
  py credit_alerts.py                       evaluate retained data, dry run (writes HTML, sends nothing)
  py credit_alerts.py --fetch --mail --send fetch Bloomberg + scan mail + e-mail Felipe if anything fired
  py credit_alerts.py --mail-hours 40       widen the mail window (default: config mail.lookback_hours)
  py credit_alerts.py --force               ignore de-dup and the Outbox-backlog guard
Exit codes: 0 ran (alerts or not) · 3 send not confirmed · 4 skipped (Outbox backlog) · 5 send failed
stdlib + pywin32 (Outlook COM) only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import os
import re
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_wiki" / "_data"
TOOLS = ROOT / "_wiki" / "_tools"
CONFIG = DATA / "credit_watch_config.json"
WATCH = DATA / "credit_watch.json"
ALERTS = DATA / "credit-monitor" / "alerts"
E = html.escape
SEV_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}


def J(p: Path, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


# ----------------------------------------------------------------------------- market layer
def clean_points(points, asof_iso=None):
    out = {}
    for d, v in points or []:
        try:
            dt.date.fromisoformat(d)
            v = float(v)
        except (TypeError, ValueError):
            continue
        if math.isfinite(v) and (asof_iso is None or d <= asof_iso):
            out[d] = v
    return sorted(out.items())


def change_value(unit, group, a, b):
    """b - a in the alert unit: bp for spreads/yields, % for equities."""
    if group == "equity":
        return (b / a - 1.0) * 100.0 if a else None
    if unit == "%":
        return (b - a) * 100.0
    return b - a


def series_stats(series, window=60, asof_iso=None):
    pts = clean_points(series.get("points"), asof_iso)
    unit, group = series.get("unit", ""), series.get("group", "")
    alert_unit = "%" if group == "equity" else "bp"
    st = {"id": series["id"], "label": series["label"], "group": group, "company": series.get("company"),
          "ticker": series.get("ticker"), "unit": unit, "alert_unit": alert_unit, "status": series.get("status"),
          "config_status": series.get("config_status"), "source": series.get("source"), "error": series.get("error"),
          "n": len(pts), "last": None, "last_date": None, "prev_date": None, "d1": None, "d5": None, "sigma": None,
          "z1": None, "z5": None, "high_60d": False, "high_1y": False, "line_cross": None, "level_line": series.get("rules", {}).get("level_line")}
    if len(pts) < 2:
        return st
    dates, vals = [p[0] for p in pts], [p[1] for p in pts]
    st.update(last=vals[-1], last_date=dates[-1], prev=vals[-2], prev_date=dates[-2])
    st["d1"] = change_value(unit, group, vals[-2], vals[-1])
    if len(vals) >= 6:
        st["d5"] = change_value(unit, group, vals[-6], vals[-1])
        st["d5_from"] = dates[-6]
    # sigma of the trailing `window` one-observation changes, excluding the last one
    chg = [change_value(unit, group, vals[i - 1], vals[i]) for i in range(1, len(vals) - 1)]
    chg = [c for c in chg if c is not None][-window:]
    floor = {"cds": 3.0, "bond": 3.0, "index": 1.0, "equity": 1.0}.get(group, 1.0)
    if len(chg) >= 10:
        sd = statistics.pstdev(chg)
        st["sigma"] = max(sd, floor)
        st["sigma_n"] = len(chg)
        st["z1"] = st["d1"] / st["sigma"] if st["d1"] is not None else None
        if st["d5"] is not None:
            st["z5"] = st["d5"] / (st["sigma"] * math.sqrt(5))
    hist60 = vals[-61:-1] if len(vals) > 1 else []
    hist1y = vals[-253:-1]
    if group != "equity":
        st["high_60d"] = bool(hist60) and vals[-1] > max(hist60) and len(hist60) >= 20
        st["high_1y"] = bool(hist1y) and vals[-1] > max(hist1y) and len(hist1y) >= 120
        line = st["level_line"]
        if line is not None:
            st["line_cross"] = "up" if vals[-2] < line <= vals[-1] else ("above" if vals[-1] >= line else None)
    else:
        lows = vals[-61:-1]
        st["low_60d"] = bool(lows) and vals[-1] < min(lows) and len(lows) >= 20
    return st


def evaluate(st, rules):
    """Return (severity, reasons[]) — spreads/yields on widening, equities on down moves."""
    reasons, score = [], 0
    if st["d1"] is None:
        return "none", []
    sign = -1.0 if st["group"] == "equity" else 1.0
    d1 = st["d1"] * sign
    d5 = (st["d5"] or 0.0) * sign
    z1 = (st["z1"] or 0.0) * sign
    z5 = (st["z5"] or 0.0) * sign
    abs1, zmin, abs5 = rules.get("d1_abs"), rules.get("d1_z"), rules.get("d5_abs")
    big1 = abs1 is not None and d1 >= abs1
    zbig = zmin is not None and st["z1"] is not None and z1 >= zmin
    big5 = abs5 is not None and d5 >= abs5
    u = st["alert_unit"]
    equity = st["group"] == "equity"
    z5min = rules.get("d5_z", 2.0)
    zbig5 = st["z5"] is None or z5 >= z5min
    if big1 and zbig:
        score = 3; reasons.append(f"1d {d1 * sign:+.0f}{u} = {z1:.1f}σ (≥{abs1}{u} and ≥{zmin}σ)")
    elif big1 or zbig:
        # spreads: an absolute move is news on its own; equities: price vol is only a proxy, so abs OR z alone is logged, not mailed
        score = max(score, 1 if equity else 2); reasons.append(f"1d {d1 * sign:+.0f}{u}" + (f" = {z1:.1f}σ" if st["z1"] is not None else ""))
    if big5:
        score = max(score, 2 if (zbig5 or not equity) else 1)
        if zbig5 and st["z5"] is not None and z5 >= max(z5min, 2.5) and not equity:
            score = 3
        reasons.append(f"5-obs {d5 * sign:+.0f}{u} since {st.get('d5_from')}" + (f" ({z5:.1f}σ)" if st["z5"] else ""))
    if rules.get("high_1y") and st.get("high_1y"):
        score = max(score, 3); reasons.append("new 1-year high")
    elif rules.get("high_60d") and st.get("high_60d"):
        score = max(score, 2); reasons.append("new 60-day high")
    if st.get("line_cross") == "up":
        score = 3; reasons.append(f"crossed the {st['level_line']}{st['unit'] if st['unit'] != '%' else '%'} line")
    if st["group"] == "equity" and st.get("low_60d") and score:
        reasons.append("new 60-day low")
    return {0: "none", 1: "low", 2: "medium", 3: "high"}[score], reasons


def market_layer(cfg, watch, asof_iso=None):
    rows, alerts = [], []
    window = int(cfg.get("sigma_window", 60))
    rules_by_id = {i["id"]: i.get("rules", {}) for i in cfg["instruments"]}
    for s in watch.get("series", []):
        st = series_stats(s, window, asof_iso)
        sev, reasons = evaluate(st, rules_by_id.get(s["id"], {})) if st["last"] is not None else ("none", [])
        st["severity"], st["reasons"] = sev, reasons
        rows.append(st)
        if sev != "none":
            u = st["alert_unit"]
            level = fmt_level(st)
            headline = f"{st['label']} {st['d1']:+.0f}{u} → {level} ({st['last_date']})" if st["group"] != "equity" else \
                       f"{st['label']} {st['d1']:+.1f}% → {level} ({st['last_date']})"
            alerts.append({"kind": "market", "id": st["id"], "company": st["company"], "group": st["group"], "severity": sev,
                           "headline": headline, "reasons": reasons, "last": st["last"], "last_date": st["last_date"],
                           "d1": st["d1"], "d5": st["d5"], "z1": st["z1"], "sigma": st["sigma"], "alert_unit": u,
                           "ticker": st["ticker"], "source": st.get("source"), "data_status": st["status"]})
    return rows, alerts


# ----------------------------------------------------------------------------- mail layer
def collect_mail(hours, out_dir: Path):
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(TOOLS / "credit_mail_collect.ps1"),
           "-SinceUtc", since, "-OutputDirectory", str(out_dir)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    cov = J(out_dir / "mail-coverage.json", {}) or {}
    cov["since_utc"] = cov.get("since_utc", since)
    cov["collector_exit"] = res.returncode
    if res.returncode:
        cov["error"] = (res.stderr or res.stdout)[-800:]
    return J(out_dir / "mail.json", []) or [], cov


def excerpt_key(excerpt: str) -> str:
    import hashlib
    return hashlib.sha1(re.sub(r"[^a-z0-9]+", " ", excerpt.lower())[:200].encode()).hexdigest()[:16]


def mail_hits(cfg_mail, mails, state_ids, seen_excerpts=None):
    """Each credit-term occurrence is attributed to the NEAREST watched name within proximity_chars (so 'GOOGL +1%'
    two sentences after a CoreWeave CDS line is not a GOOGL hit). Subject hits need name -> credit term within
    subject_adjacent_chars. One hit per (message, company); identical excerpts across messages collapse."""
    credit = re.compile(cfg_mail["credit_terms"], re.I)
    names = {k: re.compile(v, re.I) for k, v in cfg_mail["name_groups"].items()}
    ignore = re.compile(cfg_mail.get("ignore_subjects", "$^"), re.I)
    prox = int(cfg_mail.get("proximity_chars", 260))
    prox_by = {k: int(v) for k, v in (cfg_mail.get("proximity_override") or {}).items()}
    adj = int(cfg_mail.get("subject_adjacent_chars", 25))
    seen_excerpts = set(seen_excerpts or ())
    hits = []
    for m in mails:
        subj = m.get("subject") or ""
        if ignore.search(subj) or m.get("id") in state_ids:
            continue
        text = (subj + "\n" + (m.get("body") or "")).replace("\r", "")
        text = re.sub(r"<https?://[^>]*>|https?://\S+|\S{60,}", " ", text)      # tracking links / encoded junk never carry evidence
        cpos = [x.start() for x in credit.finditer(text)]
        if not cpos:
            continue
        npos = [(nm.start(), comp) for comp, rx in names.items() for nm in rx.finditer(text)]
        if not npos:
            continue
        best = {}                                   # company -> (score, excerpt)
        for c in cpos:
            near = [(abs(c - p_), p_, comp) for p_, comp in npos if abs(c - p_) <= prox_by.get(comp, prox)]
            if not near:
                continue
            dist, p_, comp = min(near)
            lo, hi = max(0, min(c, p_) - 120), min(len(text), max(c, p_) + 180)
            excerpt = re.sub(r"\s+", " ", text[lo:hi]).strip()
            cand = (1, excerpt)
            if comp not in best or cand[0] > best[comp][0]:
                best[comp] = cand
        for comp, rx in names.items():               # subject: name followed by a credit term within adj chars
            if any(credit.search(subj, nm.end(), nm.end() + adj) for nm in rx.finditer(subj)):
                best[comp] = (2, best.get(comp, (0, re.sub(r"\s+", " ", subj).strip()))[1])
        for comp, (score, excerpt) in best.items():
            k = excerpt_key(excerpt)
            if k in seen_excerpts:                   # boilerplate repeated across days (a desk's standing risk list)
                continue
            seen_excerpts.add(k)
            hits.append({"company": comp, "id": m.get("id"), "subject": subj, "sender": m.get("sender"),
                         "sender_name": m.get("sender_name"), "date": m.get("date"), "in_subject": score == 2,
                         "excerpt": excerpt[:320], "excerpt_key": k})
    return hits


def firm_of(sender: str, sender_name: str) -> str:
    dom = (sender or "").split("@")[-1].lower()
    known = {"gs.com": "Goldman Sachs", "jefferies.com": "Jefferies", "rothschildandco.com": "Rothschild & Co", "redburn.com": "Rothschild & Co Redburn",
             "jpmorgan.com": "J.P. Morgan", "jpmresearchmail.com": "J.P. Morgan", "morganstanley.com": "Morgan Stanley", "ubs.com": "UBS",
             "bofa.com": "BofA", "baml.com": "BofA", "barclays.com": "Barclays", "citi.com": "Citi", "db.com": "Deutsche Bank",
             "bernstein.com": "Bernstein", "bernsteinsg.com": "Bernstein", "evercoreisi.com": "Evercore ISI", "wolferesearch.com": "Wolfe",
             "sig.com": "Susquehanna", "cantor.com": "Cantor", "btgpactual.com": "BTG Pactual", "xpi.com.br": "XP", "itau.com.br": "Itaú",
             "vitalknowledge.net": "Vital Knowledge", "tmtbreakout@substack.com": "TMT Breakout", "damnang2@substack.com": "DAMNANG", "substack.com": "Substack", "semianalysis.com": "SemiAnalysis", "capstone.com.br": "Capstone (internal)",
             "22vresearch.com": "22V Research", "hedgeye.com": "Hedgeye", "theinformation.com": "The Information", "ft.com": "FT", "bloomberg.net": "Bloomberg"}
    addr = (sender or "").lower()
    for k, v in known.items():
        if "@" in k and addr == k:
            return v
    for k, v in known.items():
        if "@" not in k and dom.endswith(k):
            return v
    return sender_name or dom


def narrative_layer(cfg_mail, hits):
    groups = {}
    for h in hits:
        h["firm"] = firm_of(h["sender"], h["sender_name"])
        groups.setdefault(h["company"], []).append(h)
    out = []
    minf = cfg_mail.get("min_firms", {})
    for comp, hs in groups.items():
        firms = sorted({h["firm"] for h in hs})
        need = int(minf.get(comp, minf.get("default", 1)))
        subject_level = any(h["in_subject"] for h in hs)
        if len(firms) < need and not subject_level:
            continue
        sev = "high" if (subject_level and len(firms) >= 2) or len(firms) >= 3 else "medium"
        hs.sort(key=lambda h: (not h["in_subject"], h["date"] or ""))
        out.append({"kind": "mail", "company": comp, "severity": sev, "n_msgs": len(hs), "firms": firms,
                    "headline": f"{comp}: {len(firms)} source{'s' if len(firms) != 1 else ''} on credit ({', '.join(firms[:4])}{'…' if len(firms) > 4 else ''})",
                    "items": [{k: h[k] for k in ("firm", "sender_name", "sender", "date", "subject", "excerpt", "in_subject", "id")} for h in hs[:6]]})
    out.sort(key=lambda a: (-SEV_RANK[a["severity"]], -a["n_msgs"]))
    return out


# ----------------------------------------------------------------------------- rendering
def fmt_level(st):
    if st["last"] is None:
        return "—"
    if st["group"] == "equity":
        return f"{st['last']:,.2f}"
    if st["unit"] == "bp":
        return f"{st['last']:,.0f} bp"
    if st["unit"] == "%":
        return f"{st['last'] * 100:,.0f} bp" if st["group"] == "index" else f"{st['last']:.2f}%"
    return f"{st['last']:,.2f}"


def fmt_chg(v, unit, dec=0):
    return "—" if v is None else (f"{v:+.{dec}f}%" if unit == "%" else f"{v:+.{dec}f} bp")


def render_email(date, market_alerts, narrative, rows, bbg_status, cov, cfg):
    lan = cfg["delivery"].get("lan_dashboard", "")
    TH = "text-align:left;font-size:10.5px;color:#66788a;text-transform:uppercase;letter-spacing:.4px;padding:5px 6px;border-bottom:1px solid #dfe6ee"
    TD = "padding:6px 6px;border-bottom:1px solid #eef2f6;vertical-align:top;font-size:12.5px"
    TDR = TD + ";text-align:right;white-space:nowrap"
    color = {"high": "#d03b3b", "medium": "#ec835a", "low": "#fab219", "none": "#898781"}
    top = (market_alerts + narrative)
    top.sort(key=lambda a: -SEV_RANK[a["severity"]])
    head = top[0]["headline"] if top else "no alert"
    parts = [f"<div style='font-family:Segoe UI,Arial,sans-serif;max-width:860px;color:#0b0b0b'>",
             f"<div style='background:#192b40;color:#fff;padding:14px 18px;border-radius:8px'><div style='font-size:18px;font-weight:700'>AI Credit ALERT | {E(date)}</div>"
             f"<div style='font-size:13px;opacity:.9;margin-top:4px'>{E(head)}</div></div>"]
    if market_alerts:
        parts.append("<h3 style='margin:18px 0 6px;font-size:15px'>Market triggers (Bloomberg, completed observations)</h3>")
        parts.append(f"<table style='border-collapse:collapse;width:100%'><tr><th style='{TH}'>Instrument</th><th style='{TH}'>Level</th><th style='{TH}'>1d</th><th style='{TH}'>5-obs</th><th style='{TH}'>σ</th><th style='{TH}'>Why</th><th style='{TH}'>Source</th></tr>")
        for a in market_alerts:
            st = next(r for r in rows if r["id"] == a["id"])
            ztxt = "—" if a["z1"] is None else f"{a['z1']:+.1f}σ"
            parts.append(f"<tr><td style='{TD}'><b style='color:{color[a['severity']]}'>{E(a['severity'].upper())}</b> {E(a['headline'].split(' → ')[0])}</td>"
                         f"<td style='{TDR}'>{E(fmt_level(st))}<br><small>{E(a['last_date'])}</small></td>"
                         f"<td style='{TDR}'>{E(fmt_chg(a['d1'], a['alert_unit'], 1 if a['group'] == 'equity' else 0))}</td>"
                         f"<td style='{TDR}'>{E(fmt_chg(a['d5'], a['alert_unit'], 1 if a['group'] == 'equity' else 0))}</td>"
                         f"<td style='{TDR}'>{ztxt}</td>"
                         f"<td style='{TD}'>{E('; '.join(a['reasons']))}</td><td style='{TD}'><small>{E(a.get('source') or a.get('ticker') or '')}" + (" · <b>stale data</b>" if a.get("data_status") == "stale" else "") + "</small></td></tr>")
        parts.append("</table>")
    if narrative:
        parts.append("<h3 style='margin:18px 0 6px;font-size:15px'>Broker / desk tape (Outlook window)</h3>")
        for n in narrative:
            parts.append(f"<div style='margin:8px 0 4px'><b style='color:{color[n['severity']]}'>{E(n['severity'].upper())}</b> <b>{E(n['headline'])}</b> · {n['n_msgs']} message{'s' if n['n_msgs'] != 1 else ''}</div><ul style='margin:0 0 8px 18px;padding:0'>")
            for it in n["items"]:
                who = f"{it['firm']} · {it['sender_name']}" if it["sender_name"] and it["sender_name"] != it["firm"] else it["firm"]
                parts.append(f"<li style='font-size:12.5px;margin:3px 0'><b>{E(who)}</b> <small>{E((it['date'] or '')[:16].replace('T', ' '))} UTC · {E(it['subject'][:110])}</small><br>“{E(it['excerpt'])}”</li>")
            parts.append("</ul>")
    if not market_alerts and not narrative:
        parts.append("<p>No trigger fired on this run.</p>")
    # watch table — always, so the reader sees what IS covered and what is not
    parts.append("<h3 style='margin:18px 0 6px;font-size:15px'>Watch list state</h3>")
    parts.append(f"<table style='border-collapse:collapse;width:100%'><tr><th style='{TH}'>Instrument</th><th style='{TH}'>Level</th><th style='{TH}'>1d</th><th style='{TH}'>5-obs</th><th style='{TH}'>z</th><th style='{TH}'>Obs date</th><th style='{TH}'>Status</th></tr>")
    for st in rows:
        status = st["status"] or "none"
        note = {"ok": "fresh", "stale": "kept previous", "none": "no history"}.get(status, status)
        if st.get("config_status") in ("unverified", "needs_isin"):
            note += f" · ticker {st['config_status']}"
        zrow = "—" if st["z1"] is None else f"{st['z1']:+.1f}"
        parts.append(f"<tr><td style='{TD}'>{E(st['label'])}<br><small>{E(st.get('ticker') or '—')}</small></td><td style='{TDR}'>{E(fmt_level(st))}</td>"
                     f"<td style='{TDR}'>{E(fmt_chg(st['d1'], st['alert_unit'], 1 if st['group'] == 'equity' else 0))}</td>"
                     f"<td style='{TDR}'>{E(fmt_chg(st['d5'], st['alert_unit'], 1 if st['group'] == 'equity' else 0))}</td>"
                     f"<td style='{TDR}'>{zrow}</td><td style='{TDR}'>{E(st['last_date'] or '—')}</td><td style='{TD}'><small>{E(note)}</small></td></tr>")
    parts.append("</table>")
    foot = [f"Bloomberg Desktop API: <b>{E(bbg_status.get('state', 'unknown'))}</b>" + (f" — {E(bbg_status.get('detail', '')[:160])}" if bbg_status.get("state") not in ("ok", None) else "")]
    if cov:
        foot.append(f"Mail window: {E(str(cov.get('since_utc', '?'))[:16])} → {E(str(cov.get('until_utc', '?'))[:16])} UTC · {cov.get('collected', 0)} messages · Outlook lag {cov.get('inbox_lag_hours', '?')} h" + (f" · <b>collector error</b>: {E(str(cov.get('error'))[:160])}" if cov.get("error") else ""))
    foot.append(f"Rules and tickers: <code>_data/credit_watch_config.json</code> · dashboard: <a href='{E(lan)}'>{E(lan)}</a> · weekly research brief: Fridays 09:00.")
    foot.append("Capstone internal research. Desk and specialist-sales voices carry no ratings or price targets. Spreads in bp, bond yields in %, equities in % — never netted across units.")
    parts.append("<div style='margin-top:18px;padding-top:10px;border-top:1px solid #dfe6ee;font-size:11.5px;color:#52514e'>" + "<br>".join(foot) + "</div></div>")
    return "\n".join(parts), head


# ----------------------------------------------------------------------------- Outlook delivery (Sent Items verified)
def outlook_ns():
    import win32com.client
    return win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")


def find_subject(folder, prefix, limit=400):
    items = folder.Items
    items.Sort("[CreationTime]", True)
    out, it, n = [], items.GetFirst(), 0
    while it is not None and n < limit:
        try:
            if str(getattr(it, "Subject", "")).startswith(prefix):
                out.append({"subject": it.Subject, "created": str(it.CreationTime)[:19]})
        except Exception:  # noqa: BLE001
            pass
        it = items.GetNext(); n += 1
    return out


def send_alert(body_html, subject, to, prefix, force=False):
    ns = outlook_ns()
    outbox = ns.GetDefaultFolder(4)
    backlog = find_subject(outbox, prefix, 400)
    if backlog and not force:
        return {"status": "skipped_outbox_backlog", "outbox_backlog": backlog[:5], "outbox_count": outbox.Items.Count}
    try:
        import win32com.client
        app = win32com.client.Dispatch("Outlook.Application")
        mail = app.CreateItem(0)
        mail.To = to
        mail.Subject = subject
        mail.HTMLBody = body_html
        mail.Send()
    except Exception as exc:  # noqa: BLE001 — OST-full / COM errors land here
        return {"status": "failed_not_sent", "error": f"{type(exc).__name__}: {exc}"[:400]}
    status = "unknown"
    for _ in range(9):
        time.sleep(10)
        if find_subject(ns.GetDefaultFolder(5), subject, 150):
            status = "sent"; break
        if find_subject(outbox, subject, 400):
            status = "queued"
    return {"status": status, "outbox_count": outbox.Items.Count}


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fetch", action="store_true", help="run fetch_credit_watch.py first")
    ap.add_argument("--mail", action="store_true", help="scan the Outlook window (credit_mail_collect.ps1)")
    ap.add_argument("--mail-hours", type=float, default=None)
    ap.add_argument("--mail-json", help="use an existing mail.json instead of collecting (tests / replays)")
    ap.add_argument("--send", action="store_true", help="e-mail Felipe when something fired")
    ap.add_argument("--force", action="store_true", help="ignore de-dup and the Outbox-backlog guard")
    ap.add_argument("--date", default=None, help="label / asof date YYYY-MM-DD (default today)")
    ap.add_argument("--asof", default=None, help="evaluate market data as of this observation date (tests)")
    a = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    date = a.date or dt.date.today().isoformat()
    stamp = dt.datetime.now().strftime("%Y-%m-%dT%H%M")
    ALERTS.mkdir(parents=True, exist_ok=True)
    (ALERTS / "emails").mkdir(exist_ok=True); (ALERTS / "receipts").mkdir(exist_ok=True)
    state = J(ALERTS / "state.json", {"market": {}, "mail_ids": {}}) or {"market": {}, "mail_ids": {}}

    if a.fetch:
        res = subprocess.run([sys.executable, str(TOOLS / "fetch_credit_watch.py")], cwd=ROOT, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=900, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        print(res.stdout.strip()[-2000:])
        if res.returncode and res.stderr:
            print(res.stderr.strip()[-800:], file=sys.stderr)
    watch = J(WATCH, {"series": [], "bbg_status": {"state": "never-fetched", "detail": "run fetch_credit_watch.py"}}) or {}
    bbg_status = watch.get("bbg_status", {"state": "unknown"})
    rows, market_alerts = market_layer(cfg, watch, a.asof)

    # de-dup market alerts on the observation date (one alert per instrument per observation; higher severity re-fires)
    fresh_market = []
    for m in market_alerts:
        prev = state["market"].get(m["id"], {})
        if not a.force and prev.get("last_date") == m["last_date"] and SEV_RANK[prev.get("severity", "none")] >= SEV_RANK[m["severity"]]:
            m["suppressed"] = "already alerted for this observation"
            continue
        fresh_market.append(m)

    narrative, cov, hits = [], {}, []
    if a.mail or a.mail_json:
        mails = []
        if a.mail_json:
            mails = J(Path(a.mail_json), []) or []
            cov = {"since_utc": "replay", "collected": len(mails)}
        else:
            out_dir = Path(tempfile.gettempdir()) / "credit-alerts" / stamp
            out_dir.mkdir(parents=True, exist_ok=True)
            try:
                mails, cov = collect_mail(a.mail_hours or float(cfg["mail"].get("lookback_hours", 30)), out_dir)
            except Exception as exc:  # noqa: BLE001
                cov = {"error": f"{type(exc).__name__}: {exc}"[:300], "collected": 0}
        cutoff_ids = set() if a.force else set(state["mail_ids"].keys())
        seen_x = set() if a.force else set(state.get("mail_excerpts", {}).keys())
        hits = mail_hits(cfg["mail"], mails, cutoff_ids, seen_x)
        narrative = narrative_layer(cfg["mail"], hits)

    min_sev = SEV_RANK[cfg["delivery"].get("min_severity_to_mail", "medium")]
    firing = [m for m in fresh_market if SEV_RANK[m["severity"]] >= min_sev] + [n for n in narrative if SEV_RANK[n["severity"]] >= min_sev]
    body, head = render_email(date, fresh_market, narrative, rows, bbg_status, cov, cfg)
    html_path = ALERTS / "emails" / f"{stamp}.html"
    html_path.write_text(body, encoding="utf-8")

    latest = {"generated_at": dt.datetime.now().isoformat(timespec="seconds"), "date": date, "bbg_status": bbg_status,
              "watch_fetched_at": watch.get("fetched_at"), "rows": rows, "market_alerts": market_alerts, "narrative": narrative,
              "mail_coverage": cov, "fired": bool(firing), "headline": head if firing else None, "email_html": str(html_path)}
    (ALERTS / "latest.json").write_text(json.dumps(latest, ensure_ascii=False, indent=1), encoding="utf-8")

    summary = {"date": date, "stamp": stamp, "fired": bool(firing), "headline": head if firing else None,
               "market_alerts": [{"id": m["id"], "severity": m["severity"], "headline": m["headline"]} for m in fresh_market],
               "narrative": [{"company": n["company"], "severity": n["severity"], "firms": n["firms"], "n_msgs": n["n_msgs"]} for n in narrative],
               "suppressed": [m["id"] for m in market_alerts if m.get("suppressed")], "bbg_status": bbg_status.get("state"),
               "bbg_detail": (bbg_status.get("detail") or "")[:200], "mail_collected": cov.get("collected"), "mail_error": cov.get("error"),
               "watch_series": len(rows), "watch_fresh": sum(1 for r in rows if r["status"] == "ok"), "email_html": str(html_path), "send": None}

    with (ALERTS / "log.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"run": stamp, "date": date, "fired": bool(firing), "headline": head if firing else None,
                             "market": summary["market_alerts"], "narrative": summary["narrative"], "bbg": bbg_status.get("state"),
                             "mail_collected": cov.get("collected")}, ensure_ascii=False) + "\n")

    if firing and a.send:
        subject = f"{cfg['delivery']['subject_prefix']} {date} | {head}"[:240]
        rec = send_alert(body, subject, cfg["delivery"]["to"], cfg["delivery"]["subject_prefix"], a.force)
        rec.update(subject=subject, to=cfg["delivery"]["to"], attempted_at=dt.datetime.now().isoformat(timespec="seconds"), body=str(html_path))
        (ALERTS / "receipts" / f"{stamp}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        summary["send"] = rec["status"]
        if rec["status"] in ("sent", "queued"):
            for m in fresh_market:
                state["market"][m["id"]] = {"last_date": m["last_date"], "severity": m["severity"], "alerted_at": stamp}
            for h in hits:
                state["mail_ids"][h["id"]] = date
                state.setdefault("mail_excerpts", {})[h["excerpt_key"]] = date
    elif firing:
        summary["send"] = "dry-run"
    # forget mail ids older than 14 days, persist state
    keep = (dt.date.fromisoformat(date) - dt.timedelta(days=14)).isoformat()
    state["mail_ids"] = {k: v for k, v in state["mail_ids"].items() if v >= keep}
    state["mail_excerpts"] = {k: v for k, v in state.get("mail_excerpts", {}).items() if v >= keep}
    (ALERTS / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if summary["send"] in ("sent", "queued", "dry-run", None):
        return 0
    return {"skipped_outbox_backlog": 4, "failed_not_sent": 5}.get(summary["send"], 3)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
