r"""
or_open_closed.py — opening block for the OpenRouter dashboard: "Open-weight vs
proprietary" share of tokens (100% stacked area) + weekly token traffic (line),
the NVIDIA-slide framing rebuilt on OpenRouter's own weekly feed, weekly cadence.

Data
  * Weekly totals: OpenRouter's calendar-week chart feed (model_chart.json, captured
    by or_fetch.py every Monday) — 53 Monday weeks, top-9 models per week + "Others".
  * Split, EXACT (full feed): our trailing-7-day rank_week.json snapshots (every model,
    not just the top 9). A snapshot taken on Monday d covers [d-7, d-1] = the chart
    week starting d-7; Tuesday snapshots are off by one day (flagged offset_days=1).
    Available from the week of 2026-07-13; one new exact point per Monday refresh.
  * Split, BOUNDED (weeks before the first snapshot): only the nine named models can
    be classified; "Others" (35-55% of tokens) is drawn as an explicit unattributed
    band. The long tail is NOT allocated pro-rata — on the weeks where we can check,
    the tail is far more proprietary than the top 9 (Jul-Sep 2026: tail 44-66% open
    vs top-9 78-100% open), so pro-rata would overstate open share by ~10-15 pp.

Classification (per model, source-side, not hand-typed):
  open-weight   = the model's OpenRouter listing carries a Hugging Face link
                  (hugging_face_id in /api/v1/models, or hf_slug in the catalog)
  proprietary   = listed, no Hugging Face link
  unattributed  = stealth previews (author "stealth" / "openrouter" alpha models —
                  weights status undisclosed while they run) and routers
  fallback for models no longer listed: or_build.LAB author capture + regex overrides.

Writes _wiki/_data/openrouter/open_closed.json (derived; audit trail incl. the
per-model class of every named chart model). render() is fail-soft.

Run standalone:  py "E:\Wiki Felipe empresas\_wiki\_tools\or_open_closed.py"
"""
import datetime as dt
import glob
import html
import json
import math
import re
import sys
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
OR = WIKI / "_data" / "openrouter"
OUT = OR / "open_closed.json"
SOURCE = "https://openrouter.ai/rankings"

UNATTRIBUTED_AUTHORS = {"stealth", "openrouter"}
OPEN_FALLBACK = (r"^openai/gpt-oss", r"^google/gemma", r"^meta-llama/", r"^microsoft/phi",
                 r"^mistralai/(?!.*(medium|codestral|saba|ocr))")
BANDS = ("open", "closed", "unattributed")          # bottom -> top in the stack
LABEL = {"open": "Open-weight", "closed": "Proprietary", "unattributed": "Stealth / unattributed"}


def _strip(s):
    return re.sub(r"-\d{8}$", "", re.sub(r"-\d{4}-\d{2}-\d{2}$", "", s or ""))


def _loadj(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def load_hf_index(wiki=WIKI):
    """slug -> has Hugging Face link. Every captured models.json + the newest catalog."""
    idx = {}
    raw = wiki / "_data" / "openrouter" / "raw"
    for p in sorted(glob.glob(str(raw / "*" / "models.json"))):
        try:
            data = _loadj(p)["data"]
        except Exception:
            continue
        for m in data:
            flag = bool(m.get("hugging_face_id"))
            for k in (m.get("canonical_slug"), m.get("id"), _strip(m.get("canonical_slug"))):
                if k:
                    idx[k] = idx.get(k, False) or flag
    for p in sorted(glob.glob(str(raw / "*" / "catalog.json")))[-1:]:
        try:
            data = _loadj(p)["data"]
        except Exception:
            continue
        for c in data:
            flag = bool(c.get("hf_slug"))
            for k in (c.get("permaslug"), c.get("slug"), _strip(c.get("permaslug"))):
                if k:
                    idx[k] = idx.get(k, False) or flag
    return idx


def _lab_map():
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from or_build import LAB
        return LAB
    except Exception:
        return {}


def classify(key, hf, lab=None):
    base = key.split(":")[0]
    author = base.split("/")[0].lower()
    if author in UNATTRIBUTED_AUTHORS:
        return "unattributed"
    for k in (base, _strip(base)):
        if k in hf:
            return "open" if hf[k] else "closed"
    for pat in OPEN_FALLBACK:
        if re.match(pat, base):
            return "open"
    cap = (lab or {}).get(author)
    if cap:
        return "closed" if cap[1] == "first-party" else "open"
    return "unattributed"


def build(wiki=WIKI, write=True):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from openrouter_cover import load_chart
    chart, path = load_chart(wiki)
    stamp = dt.datetime.fromtimestamp(chart["cachedAt"] / 1000, dt.timezone.utc)
    hf = load_hf_index(wiki)
    lab = _lab_map()
    named_class = {}
    weeks = []
    for row in chart["data"]:
        start = dt.date.fromisoformat(row["x"])
        if start + dt.timedelta(days=7) > stamp.date():
            continue                                   # week in progress -> excluded
        named = {b: 0.0 for b in BANDS}
        for k, v in row["ys"].items():
            if k == "Others":
                continue
            c = classify(k, hf, lab)
            named_class[k] = c
            named[c] += v
        others = float(row["ys"].get("Others", 0))
        total = float(sum(row["ys"].values()))
        weeks.append({"x": row["x"], "total": total,
                      "top9": {"open": named["open"], "closed": named["closed"],
                               "unattributed": named["unattributed"] + others, "stealth": named["unattributed"], "others": others}})
    # exact overlay from full-feed trailing-7-day snapshots
    snaps = []
    for p in sorted(glob.glob(str(wiki / "_data" / "openrouter" / "raw" / "*" / "rank_week.json"))):
        try:
            d = dt.date.fromisoformat(Path(p).parent.name)
            data = _loadj(p)["data"]
        except Exception:
            continue
        agg = {b: 0.0 for b in BANDS}
        for r in data:
            var = r.get("variant")
            key = r["model_permaslug"] + ((":" + var) if var and var != "standard" else "")
            t = float(r.get("total_prompt_tokens") or 0) + float(r.get("total_completion_tokens") or 0)
            agg[classify(key, hf, lab)] += t
        tot = sum(agg.values())
        if tot > 0:
            snaps.append((d, d - dt.timedelta(days=7), agg, tot))
    for w in weeks:
        start = dt.date.fromisoformat(w["x"])
        best = None
        for d, wstart, agg, tot in snaps:
            off = (wstart - start).days
            if abs(off) <= 1 and (best is None or abs(off) < abs(best[0]) or (abs(off) == abs(best[0]) and d > best[1])):
                best = (off, d, agg, tot)
        if best:
            off, d, agg, tot = best
            w["full"] = {b: agg[b] / tot for b in BANDS}
            w["full_tokens"] = tot
            w["snapshot"] = d.isoformat()
            w["offset_days"] = off
    for w in weeks:
        if "full" in w:
            w["share"] = dict(w["full"]); w["basis"] = "full"
        else:
            w["share"] = {b: w["top9"][b] / w["total"] if w["total"] else 0.0 for b in BANDS}; w["basis"] = "top9"
    full_weeks = [w for w in weeks if w["basis"] == "full"]
    latest_full = None
    if full_weeks:
        lf = full_weeks[-1]
        latest_full = {"x": lf["x"], "snapshot": lf["snapshot"], "offset_days": lf["offset_days"], "total": lf["total"], **lf["share"]}
    first = weeks[0] if weeks else None
    last = weeks[-1] if weeks else None
    base_i = max(0, len(weeks) - 53)
    base = weeks[base_i] if weeks else None
    out = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "source": SOURCE, "chart_file": str(path.relative_to(wiki)).replace("\\", "/"),
        "chart_asof": stamp.strftime("%Y-%m-%d %H:%M UTC"),
        "method": {
            "totals": "OpenRouter calendar-week chart feed (top-9 models + Others); complete weeks only",
            "split_full": "trailing-7-day rank_week snapshots (every model); Monday snapshot d covers chart week d-7; offset_days flags Tuesday captures",
            "split_top9": "weeks before the first snapshot: only the nine named models are classified; Others drawn as unattributed, never allocated pro-rata",
            "classification": "open-weight = Hugging Face link on the OpenRouter listing (hugging_face_id / hf_slug); proprietary = listed without one; unattributed = stealth previews (stealth/*, openrouter/*-alpha) and routers; unlisted models fall back to or_build.LAB author capture + gpt-oss/gemma/llama/phi/mistral overrides",
        },
        "weeks": weeks,
        "latest_full": latest_full,
        "first_week": {"x": first["x"], "total": first["total"], **first["share"], "basis": first["basis"]} if first else None,
        "last_week": {"x": last["x"], "total": last["total"], "basis": last["basis"]} if last else None,
        "traffic_multiple": {"vs_week": base["x"], "x": (last["total"] / base["total"]) if base and base["total"] else None} if base and last else None,
        "named_model_class": dict(sorted(named_class.items())),
        "n_weeks": len(weeks), "n_full_weeks": len(full_weeks),
    }
    if write:
        OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


# ---------------------------------------------------------------- rendering
def _fmt_t(v):
    return ("%.0fT" if v >= 1e13 else "%.1fT") % (v / 1e12)


def _pct(v, dp=None):
    p = v * 100
    if dp is None:
        dp = 0 if p >= 10 else 1
    return ("%." + str(dp) + "f%%") % p


def _dfmt(x):
    d = dt.date.fromisoformat(x)
    return d.strftime("%b ") + str(d.day) + d.strftime(", %Y")


def _nice_step(maximum):
    raw = maximum / 4
    power = 10 ** math.floor(math.log10(max(raw, 1)))
    return next(n * power for n in (1, 2, 2.5, 4, 5, 8, 10) if n * power >= raw)


def _month_ticks(weeks, pw):
    """Month-start ticks, thinned so labels never collide (≥40 viewBox px apart).

    A partial first month (series starts on the 29th) hands its year label to the
    first full month; January always carries the year; the stride keeps January.
    """
    n = len(weeks)
    starts, prev = [], None
    for i, w in enumerate(weeks):
        d = dt.date.fromisoformat(w["x"])
        if (d.year, d.month) != prev:
            starts.append([i, d])
            prev = (d.year, d.month)
    if len(starts) >= 2 and starts[1][0] - starts[0][0] < 3:
        starts = starts[1:]
    if not starts:
        return []
    pitch = pw / max(n - 1, 1)
    stride = max(1, math.ceil(40 / max(pitch * 4.35, 1e-9)))
    jan = next((k for k, (i, d) in enumerate(starts) if d.month == 1), 0)
    keep = [(k, i, d) for k, (i, d) in enumerate(starts) if (k - jan) % stride == 0]
    if keep and keep[0][0] != 0 and (starts[0][0] - 0) >= 0 and (keep[0][1] - starts[0][0]) * pitch >= 40:
        keep.insert(0, (0, starts[0][0], starts[0][1]))
    out, first = [], True
    for k, i, d in keep:
        out.append((i, d.strftime("%b") + (d.strftime(" '%y") if (first or d.month == 1) else "")))
        first = False
    return out


def _share_svg(weeks, first_full):
    W, H = 540, 300
    PL, PR, PT, PB = 40, 126, 24, 30
    pw, ph = W - PL - PR, H - PT - PB
    n = len(weeks)
    xs = [PL + pw * (i / (n - 1) if n > 1 else 0) for i in range(n)]

    def y(v):
        return PT + ph * (1 - v)
    cum = []
    for w in weeks:
        s = w["share"]; c = {"open": s["open"], "closed": s["open"] + s["closed"]}
        c["unattributed"] = min(1.0, c["closed"] + s["unattributed"])
        cum.append(c)
    out = ['<svg class="oc-plot" viewBox="0 0 %d %d" data-x0="%d" data-xw="%d" data-py0="%d" data-ph="%d" tabindex="0" role="img" aria-label="Share of OpenRouter tokens by weight availability, weekly">' % (W, H, PL, pw, PT, ph),
           '<defs><pattern id="oc-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<rect width="6" height="6" class="oc-hatch-a"/><rect width="2.5" height="6" class="oc-hatch-b"/></pattern></defs>']
    for t in (0, .25, .5, .75, 1):
        out.append('<line class="oc-grid" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/>' % (PL, PL + pw, y(t), y(t)))
        out.append('<text class="oc-ax" x="%d" y="%.1f" text-anchor="end">%d%%</text>' % (PL - 6, y(t) + 4, t * 100))
    lower = [0.0] * n
    fills = {"open": "oc-f-open", "closed": "oc-f-closed", "unattributed": "oc-f-unattr"}
    for b in BANDS:
        upper = [cum[i][b] for i in range(n)]
        d = "M" + " L".join("%.1f %.1f" % (xs[i], y(lower[i])) for i in range(n))
        d += " L" + " L".join("%.1f %.1f" % (xs[i], y(upper[i])) for i in range(n - 1, -1, -1)) + " Z"
        out.append('<path class="%s" d="%s"/>' % (fills[b], d))
        if b == "unattributed":
            out.append('<path class="oc-f-unattr-tex" d="%s"/>' % d)
        lower = upper
    for b in ("open", "closed"):                      # 2px surface gap between fills
        out.append('<path class="oc-gap" d="M%s"/>' % " L".join("%.1f %.1f" % (xs[i], y(cum[i][b])) for i in range(n)))
    if first_full is not None and 0 < first_full < n:
        fx = xs[first_full]
        out.append('<line class="oc-divider" x1="%.1f" x2="%.1f" y1="%d" y2="%d"/>' % (fx, fx, PT - 6, PT + ph))
        out.append('<text class="oc-note" x="%.1f" y="%d">full feed, every model \u2192</text>' % (fx + 4, PT - 8))
        out.append('<text class="oc-note" x="%.1f" y="%d" text-anchor="end">\u2190 top-9 named + long tail</text>' % (fx - 4, PT - 8))
    for i, lab in _month_ticks(weeks, pw):
        out.append('<text class="oc-ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (xs[i], H - 9, html.escape(lab)))
    # right-end direct labels (text tokens + swatch), collision-nudged
    last = weeks[-1]["share"]; c = cum[-1]
    mids = [("open", y(c["open"] / 2)), ("closed", y((c["open"] + c["closed"]) / 2)), ("unattributed", y((c["closed"] + c["unattributed"]) / 2))]
    mids.sort(key=lambda t: t[1])
    for k in range(1, len(mids)):
        if mids[k][1] - mids[k - 1][1] < 15:
            mids[k] = (mids[k][0], mids[k - 1][1] + 15)
    short = {"open": "Open-weight", "closed": "Proprietary", "unattributed": "Unattributed"}
    for b, yy in mids:
        out.append('<rect class="oc-sw %s" x="%d" y="%.1f" width="8" height="8" rx="2"/>' % (fills[b], PL + pw + 8, yy - 4))
        out.append('<text class="oc-lab" x="%d" y="%.1f"><tspan class="oc-lab-v">%s</tspan> %s</text>' % (PL + pw + 20, yy + 4, _pct(last[b]), short[b]))
    out.append('<line class="oc-cross" x1="0" x2="0" y1="%d" y2="%d" hidden/>' % (PT, PT + ph))
    out.append('</svg>')
    return "".join(out)


def _traffic_svg(weeks):
    W, H = 540, 300
    PL, PR, PT, PB = 46, 22, 24, 30
    pw, ph = W - PL - PR, H - PT - PB
    n = len(weeks)
    xs = [PL + pw * (i / (n - 1) if n > 1 else 0) for i in range(n)]
    vals = [w["total"] for w in weeks]
    mx = max(vals) if vals else 1
    step = _nice_step(mx)
    top = math.ceil(mx / step) * step
    top = top if mx / top < .93 else top + step

    def y(v):
        return PT + ph * (1 - v / top)
    out = ['<svg class="oc-plot" viewBox="0 0 %d %d" data-x0="%d" data-xw="%d" data-py0="%d" data-ph="%d" data-top="%.0f" tabindex="0" role="img" aria-label="OpenRouter weekly token traffic, trillions">' % (W, H, PL, pw, PT, ph, top)]
    t = 0.0
    while t <= top + 1e-9:
        out.append('<line class="oc-grid" x1="%d" x2="%d" y1="%.1f" y2="%.1f"/>' % (PL, PL + pw, y(t), y(t)))
        out.append('<text class="oc-ax" x="%d" y="%.1f" text-anchor="end">%s</text>' % (PL - 6, y(t) + 4, ("%g" % (t / 1e12)) + "T"))
        t += step
    line = " L".join("%.1f %.1f" % (xs[i], y(vals[i])) for i in range(n))
    out.append('<path class="oc-wash" d="M%s L%.1f %.1f L%.1f %.1f Z"/>' % (line, xs[-1], y(0), xs[0], y(0)))
    out.append('<path class="oc-line" d="M%s"/>' % line)
    for i, lab in _month_ticks(weeks, pw):
        out.append('<text class="oc-ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (xs[i], H - 9, html.escape(lab)))
    picks = sorted(set([0, n - 1] + [i for i in range(0, n, 13)] + [vals.index(mx)]))
    prev_x = -1e9
    for i in picks:
        if xs[i] - prev_x < 34 and i != n - 1:
            continue
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        out.append('<circle class="oc-dot" cx="%.1f" cy="%.1f" r="4"/>' % (xs[i], y(vals[i])))
        out.append('<text class="oc-lab" x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (xs[i] + (4 if i == 0 else 0), y(vals[i]) - 9, anchor, _fmt_t(vals[i])))
        prev_x = xs[i]
    out.append('<line class="oc-cross" x1="0" x2="0" y1="%d" y2="%d" hidden/>' % (PT, PT + ph))
    out.append('<circle class="oc-hover-dot" cx="0" cy="0" r="4" hidden/>')
    out.append('</svg>')
    return "".join(out)


CSS = r"""
.oc{background:var(--plane);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;scroll-margin-top:52px}
.oc *{box-sizing:border-box}
.oc-inner{max-width:1080px;margin:0 auto;padding:24px 26px 10px}
.oc h1{font-size:22px;margin:0 0 6px;letter-spacing:-.3px}
.oc .oc-kicker{color:var(--muted);font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;margin:0 0 4px}
.oc .oc-sub{color:var(--ink2);font-size:14px;margin:0 0 4px;max-width:960px}
.oc .oc-sub b{color:var(--ink)}
.oc-tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:16px 0 14px}
.oc-tile{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:12px 14px}
.oc-tile .l{color:var(--muted);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;display:flex;align-items:center;gap:6px}
.oc-tile .v{font-size:26px;font-weight:700;line-height:1.15;margin:3px 0 2px;font-variant-numeric:tabular-nums}
.oc-tile .s{color:var(--ink2);font-size:12px}
.oc-grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:820px){.oc-grid2{grid-template-columns:1fr}.oc-inner{padding:18px 16px 8px}}
.oc-card{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:14px 16px 10px;min-width:0}
.oc-card h3{font-size:14.5px;margin:0 0 2px}
.oc-card .oc-h3sub{color:var(--muted);font-size:12px;margin:0 0 6px}
.oc-canvas{position:relative}
.oc-plot{display:block;width:100%;height:auto;overflow:visible;outline:none;cursor:crosshair}
.oc-plot:focus-visible{outline:2px solid var(--s1);outline-offset:4px;border-radius:4px}
.oc-plot text{font:11.5px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;fill:var(--ink2);font-variant-numeric:tabular-nums;pointer-events:none}
.oc-plot .oc-ax{fill:var(--muted)}
.oc-plot .oc-lab{fill:var(--ink2);font-size:12px}
.oc-plot .oc-lab-v{fill:var(--ink);font-weight:700}
.oc-plot .oc-note{fill:var(--muted);font-size:10.5px}
.oc-grid{stroke:var(--grid);stroke-width:1}
.oc-f-open{fill:var(--s2)}.oc-f-closed{fill:var(--s1)}.oc-f-unattr{fill:var(--base)}
.oc-f-unattr-tex{fill:url(#oc-hatch)}
.oc-hatch-a{fill:transparent}.oc-hatch-b{fill:rgba(0,0,0,.14)}
:root[data-theme=dark] .oc-hatch-b{fill:rgba(255,255,255,.14)}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .oc-hatch-b{fill:rgba(255,255,255,.14)}}
.oc-gap{fill:none;stroke:var(--surf);stroke-width:2;stroke-linejoin:round}
.oc-divider{stroke:var(--ink2);stroke-width:1;stroke-dasharray:3 3}
.oc-line{fill:none;stroke:var(--s1);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.oc-wash{fill:var(--s1);opacity:.10}
.oc-dot{fill:var(--s1);stroke:var(--surf);stroke-width:2}
.oc-hover-dot{fill:var(--s1);stroke:var(--surf);stroke-width:2}
.oc-cross{stroke:var(--ink2);stroke-width:1;opacity:.6;pointer-events:none}
.oc-plot [hidden]{display:none}
.oc-legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--ink2);margin:6px 0 0}
.oc-legend span{display:inline-flex;align-items:center;gap:6px}
.oc-legend i{width:12px;height:12px;border-radius:3px;display:inline-block}
.oc-legend i.tex{background-image:repeating-linear-gradient(45deg,rgba(0,0,0,.14) 0 2px,transparent 2px 6px)}
.oc-tip{position:absolute;z-index:40;top:8px;left:0;min-width:236px;max-width:calc(100% - 12px);background:var(--surf);color:var(--ink);border:1px solid var(--border);box-shadow:0 8px 28px rgba(0,0,0,.18);border-radius:8px;padding:10px 12px;pointer-events:none;font-size:12px;line-height:1.55}
.oc-tip strong{display:block;font-size:12.5px;margin-bottom:5px}
.oc-tip .r{display:flex;align-items:center;gap:7px}
.oc-tip .r i{width:12px;height:3px;border-radius:2px;flex:none}
.oc-tip .r b{font-variant-numeric:tabular-nums;min-width:46px}
.oc-tip .r span{color:var(--ink2)}
.oc-tip .t{border-top:1px solid var(--grid);margin-top:6px;padding-top:5px;color:var(--ink2)}
.oc-tip .t b{color:var(--ink);font-variant-numeric:tabular-nums}
.oc-tip small{display:block;color:var(--muted);font-size:10.5px;margin-top:4px}
.oc-note-p{color:var(--ink2);font-size:12.5px;margin:12px 0 0}
.oc-note-p code{background:var(--grid);padding:1px 5px;border-radius:4px;font-size:11.5px}
.oc details{margin:10px 0 0;font-size:12.5px}
.oc summary{cursor:pointer;color:var(--ink2);font-weight:600}
.oc-table{width:100%;border-collapse:collapse;margin:8px 0 0;font-size:12px}
.oc-table th,.oc-table td{border-bottom:1px solid var(--grid);padding:4px 8px;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.oc-table th:first-child,.oc-table td:first-child{text-align:left}
.oc-table th{color:var(--ink2);font-weight:700}
.oc-credit{color:var(--muted);font-size:11px;margin:8px 0 0}
.oc-credit a{color:inherit}
"""

JS = r"""
(()=>{
const root=document.getElementById('open-vs-closed');if(!root)return;
const D=JSON.parse(root.querySelector('.oc-data').textContent),W=D.weeks,n=W.length;if(!n)return;
const cards=[...root.querySelectorAll('.oc-canvas')];
const fmtT=v=>(v/1e12).toLocaleString('en-US',{maximumFractionDigits:v>=1e13?0:1})+'T';
const pct=v=>{const p=v*100;return p.toFixed(p>=10?0:1)+'%';};
const dateOf=x=>new Date(x+'T00:00:00Z').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});
const NAMES={open:'Open-weight',closed:'Proprietary',unattributed:'Stealth / unattributed'};
const COL={open:'var(--s2)',closed:'var(--s1)',unattributed:'var(--base)'};
function xOf(svg,i){return +svg.dataset.x0+(+svg.dataset.xw)*(n>1?i/(n-1):0);}
function idxAt(svg,ev){const pt=svg.createSVGPoint();pt.x=ev.clientX;pt.y=ev.clientY;const p=pt.matrixTransform(svg.getScreenCTM().inverse());const f=(p.x-(+svg.dataset.x0))/(+svg.dataset.xw);return Math.max(0,Math.min(n-1,Math.round(f*(n-1))));}
function place(card,svg,i){
 const tip=card.querySelector('.oc-tip');const x=xOf(svg,i);const box=svg.getBoundingClientRect();const frame=card.getBoundingClientRect();
 const px=box.left-frame.left+x*box.width/svg.viewBox.baseVal.width;const tw=tip.offsetWidth;
 tip.style.left=Math.max(0,Math.min(frame.width-tw,px>frame.width/2?px-tw-14:px+14))+'px';
}
function show(i){
 const w=W[i],prev=i>0?W[i-1]:null;
 cards.forEach(card=>{
  const svg=card.querySelector('svg'),tip=card.querySelector('.oc-tip');
  const x=xOf(svg,i);const cross=svg.querySelector('.oc-cross');cross.setAttribute('x1',x);cross.setAttribute('x2',x);cross.removeAttribute('hidden');
  const hd=svg.querySelector('.oc-hover-dot');
  if(hd){const top=+svg.dataset.top,py0=+svg.dataset.py0,ph=+svg.dataset.ph;hd.setAttribute('cx',x);hd.setAttribute('cy',py0+ph*(1-w.total/top));hd.removeAttribute('hidden');}
  tip.replaceChildren();
  const h=document.createElement('strong');h.textContent='Week of '+dateOf(w.x);tip.append(h);
  if(card.dataset.kind==='share'){
   for(const b of ['open','closed','unattributed']){
    const r=document.createElement('div');r.className='r';const k=document.createElement('i');k.style.background=COL[b];
    const v=document.createElement('b');v.textContent=pct(w.share[b]);const s=document.createElement('span');s.textContent=NAMES[b];
    r.append(k,v,s);tip.append(r);
   }
   const t=document.createElement('div');t.className='t';
   if(w.basis==='full'){t.textContent='Full feed, every model · snapshot '+w.snapshot+(w.offset_days?' (window shifted '+Math.abs(w.offset_days)+' day)':'');}
   else{t.textContent='Top-9 named models only · '+pct(w.top9.others/w.total)+' long tail unattributed'+(w.top9.stealth?' (+'+pct(w.top9.stealth/w.total)+' stealth)':'');}
   tip.append(t);
  }else{
   const r=document.createElement('div');r.className='r';const k=document.createElement('i');k.style.background='var(--s1)';
   const v=document.createElement('b');v.textContent=fmtT(w.total);const s=document.createElement('span');s.textContent='tokens in the week';r.append(k,v,s);tip.append(r);
   const t=document.createElement('div');t.className='t';
   if(prev&&prev.total>0){const d=(w.total/prev.total-1)*100;t.textContent='Week over week: '+(d>=0?'+':'')+d.toFixed(1)+'%';}else{t.textContent='First week of the series';}
   tip.append(t);
   const s2=document.createElement('small');s2.textContent='Complete calendar weeks (Mon–Sun, UTC); observed, not estimated.';tip.append(s2);
  }
  tip.hidden=false;place(card,svg,i);
 });
}
function hide(){cards.forEach(card=>{card.querySelector('.oc-tip').hidden=true;card.querySelectorAll('.oc-cross,.oc-hover-dot').forEach(e=>e.setAttribute('hidden',''));});}
let cur=n-1;
cards.forEach(card=>{
 const svg=card.querySelector('svg');
 svg.addEventListener('pointermove',ev=>{cur=idxAt(svg,ev);show(cur);});
 svg.addEventListener('pointerleave',hide);
 svg.addEventListener('focus',()=>show(cur));svg.addEventListener('blur',hide);
 svg.addEventListener('keydown',ev=>{if(ev.key==='Escape'){hide();return;}if(ev.key==='ArrowLeft'||ev.key==='ArrowRight'){ev.preventDefault();cur=Math.max(0,Math.min(n-1,cur+(ev.key==='ArrowRight'?1:-1)));show(cur);}});
});
})();
"""


def _section(data):
    weeks = data["weeks"]
    if not weeks:
        raise ValueError("no complete weeks")
    lf = data.get("latest_full")
    first = data["first_week"]; last = data["last_week"]; mult = data.get("traffic_multiple") or {}
    first_full = next((i for i, w in enumerate(weeks) if w["basis"] == "full"), None)
    first_full_x = _dfmt(weeks[first_full]["x"]) if first_full is not None else "n/a"
    if lf:
        head = ('Open-weight models carry <b>%s</b> of OpenRouter tokens (full feed, week of %s); proprietary models <b>%s</b>, stealth previews <b>%s</b>. '
                % (_pct(lf["open"]), _dfmt(lf["x"]), _pct(lf["closed"]), _pct(lf["unattributed"])))
    else:
        head = 'No full-feed snapshot matches a complete chart week yet; the split below is bounded by the nine named models. '
    f9 = first["closed"] + first["open"]
    head2 = ('A year earlier (week of %s) the nine largest models were <b>%s proprietary</b> \u2014 %s of all tokens vs %s open-weight, with the long tail (%s) unattributed.'
             % (_dfmt(first["x"]), _pct(first["closed"] / f9 if f9 else 0), _pct(first["closed"]), _pct(first["open"]), _pct(first["unattributed"])))
    traffic = ('Weekly token traffic: <b>%s</b> in the week of %s \u2014 <b>%.0f\u00d7</b> the week of %s.'
               % (_fmt_t(last["total"]), _dfmt(last["x"]), mult.get("x") or 0, _dfmt(mult.get("vs_week", first["x"]))))
    wow = None
    if len(weeks) > 1 and weeks[-2]["total"]:
        wow = weeks[-1]["total"] / weeks[-2]["total"] - 1
    tiles = []
    if lf:
        tiles.append('<div class="oc-tile"><div class="l"><i style="width:10px;height:10px;border-radius:3px;background:var(--s2);display:inline-block"></i>Open-weight share</div><div class="v">%s</div><div class="s">of tokens \u00b7 week of %s \u00b7 full feed</div></div>' % (_pct(lf["open"]), _dfmt(lf["x"])))
        tiles.append('<div class="oc-tile"><div class="l"><i style="width:10px;height:10px;border-radius:3px;background:var(--s1);display:inline-block"></i>Proprietary share</div><div class="v">%s</div><div class="s">+ %s stealth / unattributed</div></div>' % (_pct(lf["closed"]), _pct(lf["unattributed"])))
    tiles.append('<div class="oc-tile"><div class="l">Tokens / week</div><div class="v">%s</div><div class="s">week of %s%s</div></div>' % (_fmt_t(last["total"]), _dfmt(last["x"]), (" \u00b7 %+.0f%% WoW" % (wow * 100)) if wow is not None else ""))
    tiles.append('<div class="oc-tile"><div class="l">vs a year ago</div><div class="v">%.0f\u00d7</div><div class="s">%s \u2192 %s</div></div>' % (mult.get("x") or 0, _fmt_t(weeks[max(0, len(weeks) - 53)]["total"]), _fmt_t(last["total"])))
    trs = "".join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        w["x"], _fmt_t(w["total"]), _pct(w["share"]["open"], 1), _pct(w["share"]["closed"], 1), _pct(w["share"]["unattributed"], 1),
        ("full feed \u00b7 " + w["snapshot"] + (" (\u00b1%dd)" % abs(w["offset_days"]) if w["offset_days"] else "")) if w["basis"] == "full" else "top-9 + long tail") for w in reversed(weeks))
    embed = {"weeks": weeks}
    n_full = data["n_full_weeks"]
    return (
        '<style>' + CSS + '</style>'
        '<section class="oc" id="open-vs-closed" aria-labelledby="oc-title"><div class="oc-inner">'
        '<p class="oc-kicker">OpenRouter \u00b7 weekly \u00b7 open-weight vs proprietary</p>'
        '<h1 id="oc-title">Open models take the token volume \u2014 on OpenRouter, ' + (_pct(lf["open"]) if lf else "most") + ' of tokens now run on open weights</h1>'
        '<p class="oc-sub">' + head + head2 + '</p>'
        '<p class="oc-sub">' + traffic + '</p>'
        '<div class="oc-tiles">' + "".join(tiles) + '</div>'
        '<div class="oc-grid2">'
        '<div class="oc-card"><h3>Share of tokens \u2014 open-weight vs proprietary</h3><p class="oc-h3sub">Weekly, % of all OpenRouter tokens \u00b7 exact (every model) from the week of ' + first_full_x + '; earlier weeks: top-9 models classified, long tail shown as unattributed</p>'
        '<div class="oc-canvas" data-kind="share">' + _share_svg(weeks, first_full) + '<div class="oc-tip" role="tooltip" hidden></div></div>'
        '<div class="oc-legend"><span><i style="background:var(--s2)"></i>Open-weight (Hugging Face link on the listing)</span><span><i style="background:var(--s1)"></i>Proprietary (API only)</span><span><i class="tex" style="background-color:var(--base)"></i>Stealth previews \u00b7 long tail before full feed</span></div></div>'
        '<div class="oc-card"><h3>Weekly token traffic</h3><p class="oc-h3sub">Trillions of tokens per calendar week (Mon\u2013Sun, UTC) \u00b7 complete weeks only \u00b7 all models incl. free tiers</p>'
        '<div class="oc-canvas" data-kind="traffic">' + _traffic_svg(weeks) + '<div class="oc-tip" role="tooltip" hidden></div></div></div>'
        '</div>'
        '<p class="oc-note-p"><b>How to read it.</b> Same framing as NVIDIA\'s "Open Models Enable New Builders" slide (Source: OpenRouter, monthly), rebuilt weekly from the feed itself. '
        '<b>Classification is source-side, per model:</b> open-weight = the model\'s OpenRouter listing carries a Hugging Face link; proprietary = listed without one; stealth previews (<code>stealth/*</code>, <code>openrouter/*-alpha</code>) stay unattributed while their author is undisclosed. '
        '<b>Two bases:</b> from the week of ' + first_full_x + ' the split uses our trailing-7-day capture of <i>every</i> model (' + str(n_full) + ' weeks, one more each Monday); before that OpenRouter\'s public history names only the nine largest models per week, so the long tail (35\u201355% of tokens) is drawn as unattributed rather than allocated \u2014 on the weeks we can check, the tail is far more proprietary than the top 9. '
        'OpenRouter is a developer/API slice (no first-party enterprise API, no consumer subscriptions) and counts free-tier tokens; weekly totals are OpenRouter\'s own, complete weeks only. '
        '<b>Reconciling to NVIDIA\'s ~75% (from ~40% a year ago):</b> NVIDIA\'s cut is monthly and its rule is not published; ours gives ' + (_pct(lf["open"]) + ' plus the ' + _pct(lf["unattributed"]) + ' stealth band (' + _pct(lf["open"] + lf["unattributed"]) + ' if every stealth preview turns out open)' if lf else 'a bounded range') + ', and it counts the API-only variants of open families (Qwen Plus, GLM Turbo, MiMo Pro) as proprietary. Treat the level as definition-dependent; the direction and the traffic multiple are not.</p>'
        '<details><summary>Table view \u2014 every week</summary><div style="overflow-x:auto"><table class="oc-table"><thead><tr><th>Week of</th><th>Tokens</th><th>Open-weight</th><th>Proprietary</th><th>Unattributed</th><th>Basis</th></tr></thead><tbody>' + trs + '</tbody></table></div></details>'
        '<p class="oc-credit">Source: <a href="' + SOURCE + '" target="_blank" rel="noopener">OpenRouter</a> weekly chart feed as of ' + html.escape(data["chart_asof"]) + ' (CC BY 4.0) + Capstone trailing-7-day captures \u00b7 generated ' + html.escape(data["generated"][:16].replace("T", " ")) + ' \u00b7 data: <code>_data/openrouter/open_closed.json</code></p>'
        '</div><script type="application/json" class="oc-data">' + json.dumps(embed, ensure_ascii=True).replace("<", "\\u003c") + '</script></section><script>' + JS + '</script>')


def render(wiki=WIKI):
    try:
        data = build(wiki)
        return _section(data)
    except Exception as exc:                     # fail-soft: never take the Monday chain down
        print("or_open_closed: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return '<section id="open-vs-closed"><h1>Open-weight vs proprietary</h1><p>Temporarily unavailable (%s).</p></section>' % html.escape(str(exc))


if __name__ == "__main__":
    d = build()
    lf = d.get("latest_full") or {}
    print("weeks %d (full %d) | latest full week %s: open %.1f%% | closed %.1f%% | unattributed %.1f%% | traffic %s (%.0fx vs %s)" % (
        d["n_weeks"], d["n_full_weeks"], lf.get("x"), lf.get("open", 0) * 100, lf.get("closed", 0) * 100, lf.get("unattributed", 0) * 100,
        _fmt_t(d["last_week"]["total"]), (d.get("traffic_multiple") or {}).get("x") or 0, (d.get("traffic_multiple") or {}).get("vs_week")))
    print("wrote", OUT)
