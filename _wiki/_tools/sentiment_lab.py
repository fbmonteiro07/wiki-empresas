# -*- coding: utf-8 -*-
"""Sentiment lab — can anything in the sentiment data set be made LEADING?

Hypothesis battery on the Bloomberg weekly panel (99 names, Jan-2024 → today, universe-relative returns):
  H1  How hot is too hot?  Attention / tone / BULL deciles → forward 1/2/4/8/12-week relative return.
  H2  Hot after a rally vs hot after a drop: extremes conditioned on the same week's return.
  H3  Hot × short interest: crowded long (hot, low SI) vs squeeze (hot, high SI).
  H4  Streaks: how many consecutive weeks in the top attention quintile before the fade?
  H5  Sentiment the price does not explain: tone residual after the same-week return.
  H6  Divergence: sentiment improving while price falls (and the reverse).
  H7  Acceleration: the blow-off signature (this week's attention jump minus last week's).
  H8  Aggregate timing: whole-universe attention vs the universe's own forward return.
  H9  Twitter vs news disagreement.
  H10 Short-interest CHANGE (4w) as a signal; SI change × attention.
  OOS Anything that works on 2024–2025 is re-checked on 2026 only.

Writes _wiki/_data/sentiment/lab.json and prints the battery. Read-only on pages.
"""
import sys, json, math, datetime as dt
from pathlib import Path
from collections import defaultdict
import importlib.util

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bs", HERE / "build_sentiment.py"); bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)
DATA = bs.DATA; TODAY = bs.TODAY
HZ = {"1w": 7, "2w": 14, "4w": 28, "8w": 56, "12w": 84}

def mean(xs): xs = [x for x in xs if x is not None]; return (sum(xs) / len(xs)) if xs else None
def tstat(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 3: return None
    m = sum(xs) / len(xs); sd = (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5
    return (m / (sd / len(xs) ** 0.5)) if sd else None
def hit(xs): xs = [x for x in xs if x is not None]; return (sum(1 for x in xs if x > 0) / len(xs)) if xs else None
def zs(vals):  # cross-sectional z over dict
    xs = [v for v in vals.values() if v is not None]
    if len(xs) < 8: return {k: None for k in vals}
    m = sum(xs) / len(xs); sd = (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5 or 1.0
    return {k: (None if v is None else max(-3.5, min(3.5, (v - m) / sd))) for k, v in vals.items()}
def median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs: return None
    n = len(xs); return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2
def summ(xs):
    xs = [x for x in xs if x is not None]
    return {"n": len(xs), "mean": mean(xs), "median": median(xs), "hit": hit(xs), "t": tstat(xs)} if xs else {"n": 0, "mean": None, "median": None, "hit": None, "t": None}

def build():
    uni = bs.load_universe()
    bb, tickers, weeks, panel = bs.build_long_panel(uni)
    # ---- extra fields: forward returns at 2/8/12w, same-week return, SI 4w change, attention accel, streaks, aggregate attention
    ew = {}  # equal-weight universe index by date
    dates = sorted({d for t in tickers for d in bb[t]["PX_LAST"]}); lvl = 1.0; prev = None
    for d in dates:
        if prev:
            rets = [bb[t]["PX_LAST"][d] / bb[t]["PX_LAST"][prev] - 1 for t in tickers if d in bb[t]["PX_LAST"] and prev in bb[t]["PX_LAST"]]
            if rets: lvl *= 1 + sum(rets) / len(rets)
        ew[d] = lvl; prev = d
    def px(t, d): return bs.last_on_or_before(bb[t]["PX_LAST"], d)
    def ewv(d):
        k = bs.last_on_or_before(ew, d); return k
    end = TODAY
    for i, f in enumerate(weeks):
        row = panel[f]
        for t in tickers:
            r = row[t]; p0 = px(t, f); e0 = ewv(f)
            for h, dd in HZ.items():
                d1 = bs.shift(f, dd); ok = dt.date.fromisoformat(d1) <= end - dt.timedelta(1)
                p1 = px(t, d1) if ok else None
                r["fwd_" + h] = (p1 / p0 - 1) if (p0 and p1) else None          # raw buy-and-hold; demeaned below
            pm = px(t, bs.shift(f, -7))
            r["same"] = (p0 / pm - 1) if (p0 and pm) else None
        # universe-relative = minus the SAME week's cross-sectional mean of the same-horizon buy-and-hold return.
        # (A daily-rebalanced EW index is the wrong benchmark here: its rebalancing premium made every decile
        #  look negative over 8–12 weeks in the first run.)
        for k in ["fwd_" + h for h in HZ] + ["same"]:
            mu = mean([row[t].get(k) for t in tickers])
            for t in tickers:
                if row[t].get(k) is not None and mu is not None: row[t][k] = row[t][k] - mu
        for t in tickers:
            r = row[t]; si_now = r.get("si"); si_prev = None
            for k in sorted(bb[t].get("SI_PERCENT_EQUITY_FLOAT", {})):
                if k <= bs.shift(f, -28): si_prev = bb[t]["SI_PERCENT_EQUITY_FLOAT"][k]
            r["si_chg"] = (si_now - si_prev) if (si_now is not None and si_prev is not None) else None
            prev_att = panel[weeks[i - 1]][t].get("att") if i else None
            r["att_accel"] = (r["att"] - prev_att) if (r.get("att") is not None and prev_att is not None) else None
            r["tw_news_gap"] = (r["tone"] - r["news_tone"]) if (r.get("tone") is not None and r.get("news_tone") is not None) else None
        # cross-sectional z of the new fields
        for k in ("same", "si_chg", "att_accel", "tw_news_gap"):
            z = zs({t: row[t].get(k) for t in tickers})
            for t in tickers: row[t]["z_" + k] = z[t]
        # tone residual on same-week return (cross-sectional OLS on z's)
        xs = [(row[t]["z_tone"], row[t]["z_same"]) for t in tickers if row[t].get("z_tone") is not None and row[t].get("z_same") is not None]
        if len(xs) >= 10:
            mx = mean([a for a, _ in xs]); my = mean([b for _, b in xs])
            cov = sum((a - mx) * (b - my) for a, b in xs); var = sum((b - my) ** 2 for _, b in xs) or 1.0
            beta = cov / var
            for t in tickers:
                a, b = row[t].get("z_tone"), row[t].get("z_same")
                row[t]["tone_resid"] = (a - beta * b) if (a is not None and b is not None) else None
        else:
            for t in tickers: row[t]["tone_resid"] = None
        # CROWD = z_att − z_si: high = everyone talking, nobody short (crowded long); low = ignored and heavily shorted.
        # SQUEEZE = z_att + z_si: high = everyone talking AND heavily shorted.
        for t in tickers:
            a, b = row[t].get("z_att"), row[t].get("z_si")
            row[t]["CROWD"] = (a - b) if (a is not None and b is not None) else None
            row[t]["SQUEEZE"] = (a + b) if (a is not None and b is not None) else None
        # divergence: tone change z minus same-week return z (positive = sentiment improving faster than price)
        for t in tickers:
            a, b = row[t].get("z_tone_chg"), row[t].get("z_same")
            row[t]["diverg"] = (a - b) if (a is not None and b is not None) else None
        # attention streak: consecutive weeks (incl. this one) with z_att >= 0.84 (top ~20%)
        for t in tickers:
            s = 0; j = i
            while j >= 0 and (panel[weeks[j]][t].get("z_att") or -9) >= 0.84: s += 1; j -= 1
            row[t]["streak"] = s
    # aggregate attention (universe): mean log ratio of total tweet count vs trailing 4w, and universe fwd raw return
    agg = []
    for i, f in enumerate(weeks):
        tot = sum(panel[f][t].get("cnt") or 0 for t in tickers)
        prevs = [sum(panel[weeks[j]][t].get("cnt") or 0 for t in tickers) for j in range(max(0, i - 4), i)]
        if len(prevs) < 2 or not tot: continue
        a = math.log((tot + 0.5) / (sum(prevs) / len(prevs) + 0.5))
        e0 = ewv(f); out = {"w": f, "agg_att": a}
        for h, dd in HZ.items():
            d1 = bs.shift(f, dd); e1 = ewv(d1) if dt.date.fromisoformat(d1) <= end - dt.timedelta(1) else None
            out["ew_" + h] = (e1 / e0 - 1) if (e0 and e1) else None
        agg.append(out)
    return bb, tickers, weeks, panel, agg

# ----------------------------------------------------------------------------- tests
def decile_table(panel, weeks, key, yrs=None):
    """key decile (1 = lowest … 10 = highest) → forward returns by horizon."""
    buckets = defaultdict(lambda: defaultdict(list))
    for f in weeks:
        if yrs and f[:4] not in yrs: continue
        row = panel[f]; ok = [t for t, r in row.items() if r.get(key) is not None]
        if len(ok) < 30: continue
        ok.sort(key=lambda t: row[t][key])
        for i, t in enumerate(ok):
            d = min(10, int(i * 10 / len(ok)) + 1)
            for h in HZ: buckets[d][h].append(row[t].get("fwd_" + h))
    return {d: {h: summ(v) for h, v in hs.items()} for d, hs in sorted(buckets.items())}

def cond(panel, weeks, pred, yrs=None):
    out = defaultdict(list); eps = 0
    for f in weeks:
        if yrs and f[:4] not in yrs: continue
        for t, r in panel[f].items():
            try: ok = pred(r)
            except Exception: ok = False
            if ok:
                eps += 1
                for h in HZ: out[h].append(r.get("fwd_" + h))
    return {h: summ(v) for h, v in out.items()} | {"episodes": eps}

def ic_by_h(panel, weeks, key, yrs=None, ctrl=None):
    """Mean weekly Spearman IC of key vs fwd_h; optional partial on ctrl."""
    res = {}
    for h in HZ:
        ics = []
        for f in weeks:
            if yrs and f[:4] not in yrs: continue
            row = panel[f]; sig = {t: r.get(key) for t, r in row.items()}; fwd = {t: r.get("fwd_" + h) for t, r in row.items()}
            if ctrl:
                ic, n = bs.partial_spearman(sig, fwd, {t: r.get(ctrl) for t, r in row.items()})
            else:
                ic, n = bs.spearman(sig, fwd)
            if ic is not None and n >= 15: ics.append(ic)
        res[h] = {"ic": mean(ics), "t": tstat(ics), "n": len(ics), "hit": hit(ics)} if ics else None
    return res

def fmtp(x, d=2): return "  –  " if x is None else f"{x*100:+.{d}f}%"
def fmtt(x): return "  –" if x is None else f"{x:+.1f}"

def main():
    bb, tickers, weeks, panel, agg = build()
    IS, OOS = {"2024", "2025"}, {"2026"}
    LAB = {"asof": TODAY.isoformat(), "weeks": len(weeks), "span": [weeks[0], weeks[-1]], "horizons": list(HZ)}
    print(f"lab: {len(weeks)} weeks × {len(tickers)} names, {weeks[0]} → {weeks[-1]}. All returns universe-relative.\n")

    # H1 deciles
    print("H1 — decile of the signal (10 = hottest / most bullish) → mean forward relative return")
    LAB["H1"] = {}
    for key in ("z_att", "z_tone", "BULL", "z_news", "z_tone_chg", "HOT", "CROWD", "SQUEEZE", "z_si"):
        dt_ = decile_table(panel, weeks, key); LAB["H1"][key] = dt_
        if 10 not in dt_ or 1 not in dt_: print(f"  {key}: no deciles (missing key?)"); continue
        print(f"  {key:11s}  " + "  ".join(f"{h:>15s}" for h in HZ) + "   mean | median   (n per cell ≈ %d)" % (dt_[10]["1w"]["n"]))
        for d in (1, 2, 5, 9, 10):
            print(f"    D{d:<2d}         " + "  ".join(f"{fmtp(dt_[d][h]['mean'])}|{fmtp(dt_[d][h]['median'])}" for h in HZ))
        print(f"    D10−D1      " + "  ".join(f"{fmtp((dt_[10][h]['mean'] or 0) - (dt_[1][h]['mean'] or 0)):>15s}" for h in HZ))

    # H2 extremes × same-week return
    print("\nH2 — very hot (attention z ≥ 1.5) split by what price did the SAME week")
    LAB["H2"] = {}
    for name, pred in [("hot & up ≥ +3% rel", lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("same") or 0) >= 0.03),
                       ("hot & flat", lambda r: (r.get("z_att") or 0) >= 1.5 and -0.03 < (r.get("same") or 0) < 0.03),
                       ("hot & down ≤ −3% rel", lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("same") or 0) <= -0.03),
                       ("hot & down ≤ −8% rel (capitulation?)", lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("same") or 0) <= -0.08),
                       ("very hot z ≥ 2.5, any", lambda r: (r.get("z_att") or 0) >= 2.5),
                       ("cold z ≤ −1.5, any", lambda r: (r.get("z_att") if r.get("z_att") is not None else 9) <= -1.5),
                       ("euphoria: att z ≥1.5 & tone z ≥1", lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("z_tone") or 0) >= 1.0),
                       ("panic: att z ≥1.5 & tone z ≤ −1", lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("z_tone") if r.get("z_tone") is not None else 9) <= -1.0)]:
        c = cond(panel, weeks, pred); LAB["H2"][name] = c
        print(f"  {name:40s} n={c['episodes']:4d}  " + "  ".join(f"{fmtp(c[h]['mean'])} (hit {c[h]['hit']*100 if c[h]['hit'] is not None else 0:.0f}%, t {fmtt(c[h]['t'])})" for h in ("1w", "4w", "12w")))

    # H3 hot × short interest
    print("\nH3 — hot (attention z ≥ 1) × short-interest tercile")
    LAB["H3"] = {}
    si_terc = {}
    for f in weeks:
        row = panel[f]; v = sorted(r["si"] for r in row.values() if r.get("si") is not None)
        if len(v) >= 30: si_terc[f] = (v[len(v) // 3], v[2 * len(v) // 3])
    def si_bucket(f, r):
        if f not in si_terc or r.get("si") is None: return None
        lo, hi = si_terc[f]; return "lowSI" if r["si"] < lo else ("highSI" if r["si"] >= hi else "midSI")
    for name in ("lowSI", "midSI", "highSI"):
        out = defaultdict(list); eps = 0
        for f in weeks:
            for t, r in panel[f].items():
                if (r.get("z_att") or 0) >= 1.0 and si_bucket(f, r) == name:
                    eps += 1
                    for h in HZ: out[h].append(r.get("fwd_" + h))
        c = {h: summ(v) for h, v in out.items()} | {"episodes": eps}; LAB["H3"]["hot & " + name] = c
        print(f"  hot & {name:7s} n={eps:4d}  " + "  ".join(f"{fmtp(c[h]['mean'])} (t {fmtt(c[h]['t'])})" for h in ("1w", "4w", "12w")))
    # and cold × SI
    for name in ("lowSI", "highSI"):
        out = defaultdict(list); eps = 0
        for f in weeks:
            for t, r in panel[f].items():
                if (r.get("z_att") if r.get("z_att") is not None else 9) <= -1.0 and si_bucket(f, r) == name:
                    eps += 1
                    for h in HZ: out[h].append(r.get("fwd_" + h))
        c = {h: summ(v) for h, v in out.items()} | {"episodes": eps}; LAB["H3"]["cold & " + name] = c
        print(f"  cold & {name:6s} n={eps:4d}  " + "  ".join(f"{fmtp(c[h]['mean'])} (t {fmtt(c[h]['t'])})" for h in ("1w", "4w", "12w")))

    # H4 streaks
    print("\nH4 — consecutive weeks in the top attention quintile (streak length at week t) → forward")
    LAB["H4"] = {}
    for s in (1, 2, 3, 4):
        pred = (lambda r, s=s: r.get("streak") == s) if s < 4 else (lambda r: (r.get("streak") or 0) >= 4)
        c = cond(panel, weeks, pred); LAB["H4"][f"streak{'≥' if s == 4 else '='}{s}"] = c
        print(f"  streak {'≥' if s == 4 else '='}{s}   n={c['episodes']:4d}  " + "  ".join(f"{fmtp(c[h]['mean'])} (t {fmtt(c[h]['t'])})" for h in ("1w", "4w", "12w")))

    # H5 tone residual, H6 divergence, H7 acceleration, H9 gap, H10 si change: IC by horizon, raw and ex-momentum
    print("\nH5/H6/H7/H9/H10 — rank IC by horizon (raw | controlling for past-4w return)")
    LAB["IC"] = {}
    for key, label in (("tone_resid", "H5 tone residual (ex same-week return)"), ("diverg", "H6 divergence: tone-chg z − same-week ret z"),
                       ("att_accel", "H7 attention acceleration"), ("tw_news_gap", "H9 Twitter tone − news tone"), ("z_si_chg", "H10 short-interest 4w change"),
                       ("CROWD", "NEW crowding: attention − short interest"), ("SQUEEZE", "NEW squeeze: attention + short interest"), ("z_si", "ref: short interest level"), ("z_att", "ref: attention"), ("z_tone", "ref: tone"), ("z_same", "ref: same-week return (reversal?)"), ("ret_m4w", "ref: past-4w return (momentum)")):
        raw = ic_by_h(panel, weeks, key); par = ic_by_h(panel, weeks, key, ctrl="ret_m4w"); LAB["IC"][key] = {"raw": raw, "ex_mom": par}
        print(f"  {label:44s} " + "  ".join(f"{h}:{(raw[h] or {}).get('ic', 0) or 0:+.3f}|{(par[h] or {}).get('ic', 0) or 0:+.3f}(t{fmtt((par[h] or {}).get('t'))})" for h in ("1w", "2w", "4w", "8w")))

    # H8 aggregate timing
    print("\nH8 — whole-universe attention (total tweets vs trailing 4w) vs the universe's own forward return")
    LAB["H8"] = {}
    vals = sorted(a["agg_att"] for a in agg); q = [vals[len(vals) // 4], vals[len(vals) // 2], vals[3 * len(vals) // 4]]
    for name, lo, hi in (("Q1 quietest", -9, q[0]), ("Q2", q[0], q[1]), ("Q3", q[1], q[2]), ("Q4 loudest", q[2], 9)):
        sel = [a for a in agg if lo <= a["agg_att"] < hi]; c = {h: summ([a.get("ew_" + h) for a in sel]) for h in HZ}; LAB["H8"][name] = c | {"weeks": len(sel)}
        print(f"  {name:12s} weeks={len(sel):3d}  " + "  ".join(f"{h}:{fmtp(c[h]['mean'])}" for h in ("1w", "4w", "12w")))
    ic_agg = {}
    for h in HZ:
        pairs = [(a["agg_att"], a["ew_" + h]) for a in agg if a.get("ew_" + h) is not None]
        r, n = bs.spearman({i: p[0] for i, p in enumerate(pairs)}, {i: p[1] for i, p in enumerate(pairs)}); ic_agg[h] = {"rho": r, "n": n}
    LAB["H8"]["rho"] = ic_agg; print("  Spearman(agg attention, universe fwd): " + "  ".join(f"{h}:{(ic_agg[h]['rho'] or 0):+.2f}(n={ic_agg[h]['n']})" for h in HZ))

    # OOS: repeat the headline conditionals on 2024-25 vs 2026
    print("\nOOS — the conditionals that looked interesting, fit years vs 2026")
    LAB["OOS"] = {}
    tests = {"hot & up ≥3%": lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("same") or 0) >= 0.03,
             "hot & down ≤−8%": lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("same") or 0) <= -0.08,
             "euphoria": lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("z_tone") or 0) >= 1.0,
             "panic": lambda r: (r.get("z_att") or 0) >= 1.5 and (r.get("z_tone") if r.get("z_tone") is not None else 9) <= -1.0,
             "streak ≥4": lambda r: (r.get("streak") or 0) >= 4,
             "cold z≤−1.5": lambda r: (r.get("z_att") if r.get("z_att") is not None else 9) <= -1.5}
    for name, pred in tests.items():
        a, b = cond(panel, weeks, pred, IS), cond(panel, weeks, pred, OOS); LAB["OOS"][name] = {"2024-25": a, "2026": b}
        print(f"  {name:18s} 24-25: n={a['episodes']:4d} 4w {fmtp(a['4w']['mean'])} (t {fmtt(a['4w']['t'])}) 12w {fmtp(a['12w']['mean'])} (t {fmtt(a['12w']['t'])})   |  2026: n={b['episodes']:4d} 4w {fmtp(b['4w']['mean'])} (t {fmtt(b['4w']['t'])}) 12w {fmtp(b['12w']['mean'])} (t {fmtt(b['12w']['t'])})")
    for key in ("tone_resid", "diverg", "att_accel", "z_si_chg"):
        a, b = ic_by_h(panel, weeks, key, IS, ctrl="ret_m4w"), ic_by_h(panel, weeks, key, OOS, ctrl="ret_m4w"); LAB["OOS"][key] = {"2024-25": a, "2026": b}
        print(f"  {key:18s} ex-mom IC  24-25: " + " ".join(f"{h}:{(a[h] or {}).get('ic', 0) or 0:+.3f}" for h in ("1w", "4w", "8w")) + "   |  2026: " + " ".join(f"{h}:{(b[h] or {}).get('ic', 0) or 0:+.3f}" for h in ("1w", "4w", "8w")))

    print("\nBY YEAR — the interaction cells and the composites, each calendar year separately (4w | 12w mean, t)")
    LAB["BYYEAR"] = {}
    cells = {"hot & lowSI": lambda f, r: (r.get("z_att") or 0) >= 1.0 and si_bucket(f, r) == "lowSI",
             "hot & highSI": lambda f, r: (r.get("z_att") or 0) >= 1.0 and si_bucket(f, r) == "highSI",
             "cold & highSI": lambda f, r: (r.get("z_att") if r.get("z_att") is not None else 9) <= -1.0 and si_bucket(f, r) == "highSI",
             "cold & lowSI": lambda f, r: (r.get("z_att") if r.get("z_att") is not None else 9) <= -1.0 and si_bucket(f, r) == "lowSI",
             "panic (hot & tone≤−1)": lambda f, r: (r.get("z_att") or 0) >= 1.5 and (r.get("z_tone") if r.get("z_tone") is not None else 9) <= -1.0,
             "hot & up ≥3%": lambda f, r: (r.get("z_att") or 0) >= 1.5 and (r.get("same") or 0) >= 0.03,
             "hot & down ≤−3%": lambda f, r: (r.get("z_att") or 0) >= 1.5 and (r.get("same") or 0) <= -0.03}
    for name, pred in cells.items():
        line = f"  {name:22s}"; LAB["BYYEAR"][name] = {}
        for y in ("2024", "2025", "2026"):
            out = defaultdict(list); eps = 0
            for f in weeks:
                if f[:4] != y: continue
                for t, r in panel[f].items():
                    if pred(f, r):
                        eps += 1
                        for h in HZ: out[h].append(r.get("fwd_" + h))
            c = {h: summ(v) for h, v in out.items()} | {"episodes": eps}; LAB["BYYEAR"][name][y] = c
            line += f"  {y}: n={eps:3d} {fmtp(c['4w']['mean'])} (t{fmtt(c['4w']['t'])}) | {fmtp(c['12w']['mean'])} (t{fmtt(c['12w']['t'])})"
        print(line)
    for key in ("BULL", "CROWD", "SQUEEZE", "z_si", "z_tone", "z_att"):
        line = f"  D10−D1 {key:9s}"; LAB["BYYEAR"][key] = {}
        for y in ("2024", "2025", "2026"):
            dt_ = decile_table(panel, weeks, key, {y}); LAB["BYYEAR"][key][y] = dt_
            if 10 in dt_ and 1 in dt_:
                line += f"  {y}: 1w {fmtp((dt_[10]['1w']['mean'] or 0) - (dt_[1]['1w']['mean'] or 0))} 4w {fmtp((dt_[10]['4w']['mean'] or 0) - (dt_[1]['4w']['mean'] or 0))} 12w {fmtp((dt_[10]['12w']['mean'] or 0) - (dt_[1]['12w']['mean'] or 0))}"
        print(line)
        ic = {y: ic_by_h(panel, weeks, key, {y}, ctrl="ret_m4w") for y in ("2024", "2025", "2026")}
        print(f"  ex-mom IC {key:9s}" + "".join(f"  {y}: 1w {(ic[y]['1w'] or {}).get('ic', 0) or 0:+.3f} 4w {(ic[y]['4w'] or {}).get('ic', 0) or 0:+.3f} 12w {(ic[y]['12w'] or {}).get('ic', 0) or 0:+.3f}" for y in ic))
    (DATA / "lab.json").write_text(json.dumps(LAB, ensure_ascii=False), encoding="utf-8")
    print("\nwrote", DATA / "lab.json")

if __name__ == "__main__":
    main()
