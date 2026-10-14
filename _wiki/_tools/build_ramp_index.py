r"""Ramp AI Index -> _data/ramp-ai-index/{series,model_share}.json (+ latest.txt).

TWO monthly alt-data series off the same Ramp panel (US corporate-card / bill-pay base):

  A. SPEND  (spend_per_employee.csv -> series.json)
     Median monthly AI-tool spend per employee, three cohorts (all, top 10%, top 1%),
     Aug-2023 ->. We hold the PRIMARY series; the wiki previously carried only
     second-hand citations (Goldman 2026-08-14, MS via SPCX) -- see themes/tokenmaxxing.md.

  B. MODEL MIX (model_share.csv -> model_share.json)
     Per-named-model share of usage, Jan-2025 ->. Shares sum to 100 each month across
     the models Ramp names. Derived cuts: provider share, the Anthropic capability
     ladder (Haiku<Sonnet<Opus<Fable, ordering per _wiki/ANTHROPIC.md), vintage
     turnover (share held by models first seen <=3 / 4-12 / >12 months ago), HHI,
     and per-model launch curves (share by months since first appearance).

     !! BASIS TRAPS, both unresolved without Ramp's methodology note:
        - The panel names only Anthropic / OpenAI / xAI / Cursor. GOOGLE (Gemini),
          Meta, Mistral and DeepSeek appear NOWHERE, so this is share of the covered
          set, NOT of enterprise LLM usage. Do not read it as market share.
        - What the share is weighted BY (spend? calls? tokens? firms?) is not stated.
          It is NOT the same basis as Ramp's vendor-adoption cut (~41% of firms use
          Anthropic vs ~39.5% OpenAI, Jun-2026, on ANTHROPIC.md) -- that one counts
          firms and overlaps; this one sums to 100.

Refresh: drop the newer CSV export over the matching file in `_data/ramp-ai-index/`
(same header) and re-run. Prints paste-ready markdown blocks for the theme pages.

    py "E:\Wiki Felipe empresas\_wiki\_tools\build_ramp_index.py"

Writes only under _wiki/_data (feature-script rule). stdlib only.
"""
import csv, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
DIR = os.path.join(WIKI, "_data", "ramp-ai-index")
CSV = os.path.join(DIR, "spend_per_employee.csv")
MSCSV = os.path.join(DIR, "model_share.csv")
RAW = os.path.join(DIR, "raw")
VINT = os.path.join(DIR, "vintages")


def _meta():
    p = os.path.join(DIR, "fetch_meta.json")
    if os.path.exists(p):
        return json.load(io.open(p, encoding="utf-8"))
    return {}


META = _meta()
PROVENANCE = (("Pulled by fetch_ramp_index.py from %s on %s (inline Next.js flight payload; "
               "legacy CSVs regenerated from raw/). Earlier vintages: CSVs supplied by Felipe "
               "2026-08-20 (spend) and 2026-09-02 (model share), archived under vintages/."
               % (META.get("url"), META.get("fetched_at")))
              if META else
              "CSVs supplied by Felipe 2026-08-20 (spend) and 2026-09-02 (model share).")

COHORTS = [
    ("median_monthly_spend_per_employee_usd", "median", "All companies (median)"),
    ("top_10_percent_median_spend_per_employee_usd", "top10", "Top 10% cohort"),
    ("top_1_percent_median_spend_per_employee_usd", "top1", "Top 1% cohort"),
]
MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


def label(ym):
    y, m = ym.split("-")[:2]
    return "%s-%s" % (MON[int(m) - 1], y[2:])


def compound(levels, i, w):
    """Trailing compound growth over w months, %/mo. None until enough history."""
    if i < w or levels[i - w] <= 0:
        return None
    return ((levels[i] / levels[i - w]) ** (1.0 / w) - 1) * 100


# ============================================================ B. model mix
# Anthropic's own capability ladder, cheapest/smallest first. Fable placed ABOVE Opus
# per _wiki/ANTHROPIC.md ("Fable 5 -- the new top tier above Opus, released June 2026").
# This ordering is the WIKI's read of the ladder, not a Ramp field.
ANTH_LADDER = ["Haiku", "Sonnet", "Opus", "Fable"]


def anth_family(model):
    for f in ANTH_LADDER:
        if model.startswith(f):
            return f
    return None


def build_model_share():
    """model_share.csv -> model_share.json. Returns the dict (None if no CSV on disk)."""
    if not os.path.exists(MSCSV):
        return None
    with io.open(MSCSV, newline="", encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if r.get("date_month")]
    dates = sorted(set(r["date_month"][:7] for r in rows))
    idx = dict((m, i) for i, m in enumerate(dates))
    n = len(dates)

    # per-model series, aligned to `dates`, 0 where the model is absent that month
    # NB: presence is tracked separately from value -- Ramp lists some models (the Grok
    # variants) with a share that rounds to 0.0000, and they are still on the panel.
    ser, prov_of, seen = {}, {}, {}
    for r in rows:
        m = r["model"]
        ser.setdefault(m, [0.0] * n)[idx[r["date_month"][:7]]] = float(r["model_share_pct"])
        seen.setdefault(m, set()).add(idx[r["date_month"][:7]])
        prov_of[m] = r["provider"]

    # integrity: Ramp's shares should close to 100 every month
    totals = [round(sum(s[i] for s in ser.values()), 4) for i in range(n)]
    off = [(dates[i], totals[i]) for i in range(n) if abs(totals[i] - 100) > 0.01]

    providers = sorted(set(prov_of.values()))
    prov_series = dict((p, [round(sum(ser[m][i] for m in ser if prov_of[m] == p), 4)
                            for i in range(n)]) for p in providers)

    models = []
    for m, s in ser.items():
        live = sorted(seen[m])
        first, last = live[0], live[-1]
        peak = max(range(n), key=lambda i: s[i])
        models.append({
            "model": m, "provider": prov_of[m],
            "family": anth_family(m) if prov_of[m] == "Anthropic" else None,
            "series": [round(v, 4) for v in s],
            "first": dates[first], "first_i": first, "last": dates[last],
            "censored": first == 0,           # already live at panel start -> true age unknown
            "debut_share": round(s[first], 4),
            "peak": round(s[peak], 4), "peak_month": dates[peak],
            "months_to_peak": peak - first,
            "latest": round(s[-1], 4),
        })
    models.sort(key=lambda d: (-d["peak"], d["model"]))

    # Anthropic ladder, as % of ALL named models and as % of Anthropic
    ladder_all, ladder_rel = {}, {}
    for fam in ANTH_LADDER:
        v = [round(sum(ser[m][i] for m in ser if prov_of[m] == "Anthropic"
                       and anth_family(m) == fam), 4) for i in range(n)]
        ladder_all[fam] = v
        ladder_rel[fam] = [round(100 * v[i] / prov_series["Anthropic"][i], 4)
                           if prov_series["Anthropic"][i] else None for i in range(n)]

    # vintage turnover. AGE IS MEASURED FROM FIRST APPEARANCE IN THE PANEL, so every
    # model live in month 0 is left-censored: the >12m bucket cannot fill until the
    # panel itself is 12 months old (i.e. it is only honest from dates[12] onward).
    vint = {"le3": [], "m4_12": [], "gt12": []}
    for i in range(n):
        b = {"le3": 0.0, "m4_12": 0.0, "gt12": 0.0}
        for m, s in ser.items():
            if i not in seen[m]:
                continue
            age = i - min(seen[m])
            b["le3" if age <= 3 else "m4_12" if age <= 12 else "gt12"] += s[i]
        for k in b:
            vint[k].append(round(b[k], 4))

    conc = []
    for i in range(n):
        live = sorted(((s[i], m) for m, s in ser.items() if i in seen[m]), reverse=True)
        conc.append({
            "n_models": len(live),
            "hhi": round(sum(v * v for v, _ in live) / 100, 2),   # 0-100 scale (shares in %)
            "top1": live[0][1], "top1_share": round(live[0][0], 4),
            "top3_share": round(sum(v for v, _ in live[:3]), 4),
        })

    out = {
        "source": "Ramp AI Index",
        "series_name": "share of named-model usage, % (sums to 100 each month)",
        "provenance": PROVENANCE,
        "caveats": [
            "COVERAGE: the panel names only Anthropic, OpenAI, xAI and Cursor. Google/Gemini, "
            "Meta, Mistral and DeepSeek appear in NO month. This is share of the covered set, "
            "not share of enterprise LLM usage, and it is not a market share.",
            "BASIS: what the share is weighted by (spend, API calls, tokens, or firms) is not "
            "stated on the page. The overall breakdown carries only named models; the curated "
            "segment cuts add an 'other provider' bucket per vendor.",
            "NOT the same cut as Ramp's vendor-adoption series (share of US firms paying each "
            "vendor, now primary in panel.json / dashboard section B): that counts FIRMS and "
            "overlaps across vendors; this sums to 100. The two are reconcilable only as "
            "penetration vs intensity -- they are not alternative estimates of one quantity.",
            "VINTAGE IS LEFT-CENSORED: model age is measured from first appearance in the "
            "panel (Jan-2025), not from true release. Models live in the first month are older "
            "than they read, so the >12-month bucket is only meaningful from "
            + dates[min(12, n - 1)] + ".",
            "Anthropic's Haiku<Sonnet<Opus<Fable ordering is the wiki's read (ANTHROPIC.md), "
            "not a Ramp field. Ramp supplies no tier, price or token weighting.",
            "Latest month can restate, and a model's debut month is a partial month of "
            "availability -- a debut share understates a launch's run-rate.",
        ],
        "months": n, "first": dates[0], "latest": dates[-1], "dates": dates,
        "monthly_total_check": {"totals": totals, "months_off_100": off},
        "providers": prov_series,
        "anthropic_ladder_pct_all": ladder_all,
        "anthropic_ladder_pct_anthropic": ladder_rel,
        "vintage_pct": vint,
        "vintage_censored_through": dates[min(11, n - 1)],
        "concentration": conc,
        "models": models,
    }
    with io.open(os.path.join(DIR, "model_share.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=True))

    print("\n\nmodel_share.json written: %d months, %s -> %s, %d models, %d providers"
          % (n, dates[0], dates[-1], len(models), len(providers)))
    if off:
        print("  !! months whose shares do NOT sum to 100: %s" % off)
    else:
        print("  shares sum to 100.00 +/- 0.01 in all %d months" % n)
    print("\n| Month | %s | models | HHI | Top model |" % " | ".join(providers))
    print("|---" * (len(providers) + 4) + "|")
    for i in range(n):
        print("| %s | %s | %d | %.1f | %s %.1f%% |"
              % (label(dates[i]), " | ".join("%.1f%%" % prov_series[p][i] for p in providers),
                 conc[i]["n_models"], conc[i]["hhi"], conc[i]["top1"], conc[i]["top1_share"]))
    print("\nAnthropic ladder, %% of ALL named models: " + " / ".join(ANTH_LADDER))
    for i in range(n):
        print("  %s  %s" % (label(dates[i]),
                            "  ".join("%5.1f" % ladder_all[f][i] for f in ANTH_LADDER)))
    return out


# ============================================================ C. restatement audit
def build_restatement():
    """Diff every archived csv vintage against the current one -> restatement.json.
    Ramp re-cuts history silently; this keeps the old numbers quotable with their vintage."""
    if not os.path.isdir(VINT):
        return None
    out = {"spend_per_employee": [], "model_share": []}

    def read(path):
        with io.open(path, newline="", encoding="utf-8-sig") as f:
            return [r for r in csv.DictReader(f) if r.get("date_month")]

    cur_sp = dict((r["date_month"][:7], r) for r in read(CSV))
    cur_ms = {}
    for r in read(MSCSV):
        cur_ms[(r["date_month"][:7], r["provider"], r["model"])] = float(r["model_share_pct"])
    for fn in sorted(os.listdir(VINT)):
        path = os.path.join(VINT, fn)
        if fn.startswith("spend_per_employee."):
            rows = []
            for r in read(path):
                m = r["date_month"][:7]
                c = cur_sp.get(m)
                rec = {"month": m}
                for key, slug, _ in COHORTS:
                    old = float(r[key])
                    new = float(c[key]) if c else None
                    rec[slug] = {"old": old, "new": new,
                                 "pct": round((new / old - 1) * 100, 2) if (c and old) else None}
                rows.append(rec)
            med = [x["median"]["pct"] for x in rows if x["median"]["pct"] is not None]
            out["spend_per_employee"].append({
                "vintage": fn, "months": len(rows), "dropped_months": [x["month"] for x in rows if not cur_sp.get(x["month"])],
                "median_revision_pct_range": [min(med), max(med)] if med else None,
                "latest_common": rows[-1] if rows else None, "rows": rows})
        elif fn.startswith("model_share."):
            diffs, n = [], 0
            for r in read(path):
                k = (r["date_month"][:7], r["provider"], r["model"])
                if k in cur_ms:
                    n += 1
                    d = cur_ms[k] - float(r["model_share_pct"])
                    if abs(d) >= 0.5:
                        diffs.append({"month": k[0], "model": k[2], "old": float(r["model_share_pct"]),
                                      "new": cur_ms[k], "pp": round(d, 2)})
            out["model_share"].append({"vintage": fn, "rows_compared": n,
                                       "moves_ge_0.5pp": sorted(diffs, key=lambda x: -abs(x["pp"]))})
    with io.open(os.path.join(DIR, "restatement.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(out, indent=1))
    for v in out["spend_per_employee"]:
        print("\nrestatement vs %s: median revised %s%% .. %s%% across %d months; dropped %s"
              % (v["vintage"], v["median_revision_pct_range"][0], v["median_revision_pct_range"][1],
                 v["months"], v["dropped_months"]))
    for v in out["model_share"]:
        print("restatement vs %s: %d rows compared, %d moves >= 0.5pp (largest %s)"
              % (v["vintage"], v["rows_compared"], len(v["moves_ge_0.5pp"]),
                 v["moves_ge_0.5pp"][0] if v["moves_ge_0.5pp"] else "-"))
    return out


# ============================================================ D. the wider panel
def _raw(name):
    p = os.path.join(RAW, name + ".json")
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else None


def _pivot(rows, key, dates, val="adoption_rate_pct", date="date_month"):
    """rows -> {category: [value per date]} (None where absent)."""
    idx = dict((d, i) for i, d in enumerate(dates))
    out = {}
    for r in rows:
        k = r[key]
        out.setdefault(k, [None] * len(dates))
        i = idx.get(r[date][:7])
        if i is not None:
            out[k][i] = r[val]
    return out


def build_panel():
    """raw/*.json -> panel.json: adoption (overall / Census / vendor / size / sector),
    AI share of business spend, spend-per-employee extras + curated cuts, model share by
    segment, and the Token Spend Management sample (weekly volume & spend by maker,
    blended $/M tokens). Nothing here is derived beyond pivots, sums and ratios."""
    if _raw("adoptionOverall") is None:
        print("\n(no raw/ datasets on disk -- run fetch_ramp_index.py; panel.json skipped)")
        return None
    P = {"source": "Ramp AI Index", "provenance": PROVENANCE, "fetched_at": META.get("fetched_at")}

    # ---- adoption
    ao = sorted(_raw("adoptionOverall"), key=lambda r: r["date_month"])
    AD = [r["date_month"][:7] for r in ao]
    census = _pivot(_raw("adoptionUsEstimate"), "question_version", AD)
    cen_all = [None] * len(AD)
    cen_ver = [None] * len(AD)
    for r in _raw("adoptionUsEstimate"):
        if r["date_month"][:7] in AD and r["adoption_rate_pct"] is not None:
            i = AD.index(r["date_month"][:7])
            cen_all[i] = r["adoption_rate_pct"]
            cen_ver[i] = r["question_version"]
    vendor = _pivot(_raw("adoptionVendor"), "vendor", AD)
    cross = None
    for i in range(len(AD)):
        a, o = vendor.get("Anthropic", [None])[i], vendor.get("OpenAI", [None])[i]
        if a is not None and o is not None and a > o and cross is None:
            cross = AD[i]
    P["adoption"] = {
        "dates": AD,
        "overall": [r["adoption_rate_pct"] for r in ao],
        "overall_mom_pp": [r["mom_change_pp"] for r in ao],
        "overall_yoy_pp": [r["yoy_change_pp"] for r in ao],
        "census": cen_all, "census_question_version": cen_ver,
        "census_wording_change": "2025-11",
        "vendor": vendor, "vendor_crossover_anthropic_gt_openai": cross,
        "size": _pivot(_raw("adoptionSize"), "business_size", AD),
        "sector": _pivot(_raw("adoptionIndustry"), "naics_sector", AD),
        "definition": ("share of businesses with an observed payment for an AI product or "
                       "service in the month (card + invoice/ACH); Census = Business Trends and "
                       "Outlook Survey, question re-worded Nov-2025"),
    }
    st = _raw("adoptionState")
    last = max(r["date_month"] for r in st)
    P["adoption"]["state_latest"] = sorted(
        [{"state": r["state_code"], "pct": r["adoption_rate_pct"], "n_firms": r["n_firms"]}
         for r in st if r["date_month"] == last], key=lambda x: -x["pct"])

    # ---- AI share of business spend (TPV)
    ss = _raw("spendShareData")
    ov = sorted(ss["overall"], key=lambda r: r["my_date"])
    SD = [r["my_date"][:7] for r in ov]
    sec = _pivot(ss["sector"], "naics_sector", SD, val="ai_share_of_tpv", date="my_date")
    P["spend_share"] = {
        "dates": SD, "overall_pct": [round(100 * r["ai_share_of_tpv"], 3) for r in ov],
        "sector_pct": dict((k, [None if v is None else round(100 * v, 3) for v in s]) for k, s in sec.items()),
        "definition": "AI spend as a share of total payment volume (TPV) on Ramp, %",
    }

    # ---- spend per employee: the extra percentiles + curated cuts
    spe = sorted(_raw("spendPerEmployee"), key=lambda r: r["date_month"])
    PD = [r["date_month"][:7] for r in spe]
    P["spend_extra"] = {
        "dates": PD,
        "median": [r["median_pepm"] for r in spe],
        "p90": [r["p90_pepm"] for r in spe], "p99": [r["p99_pepm"] for r in spe],
        "top10_median": [r["top_10_percent_median_pepm"] for r in spe],
        "top1_median": [r["top_1_percent_median_pepm"] for r in spe],
        "winsorized_weighted": [r["p99_winsorized_weighted_pepm"] for r in spe],
        "note": ("p90/p99 = the 90th/99th percentile company; top10/top1 = median INSIDE "
                 "that cohort; winsorized_weighted = spend-weighted mean with the top 1% capped"),
    }
    cur = _raw("spendPerEmployeeCurated")
    P["spend_curated"] = {}
    for dim in sorted(set(r["dimension_type"] for r in cur)):
        rows = [r for r in cur if r["dimension_type"] == dim]
        labels = sorted(set((r["display_order"], r["dimension_label"]) for r in rows))
        P["spend_curated"][dim] = {
            "labels": [l for _, l in labels],
            "median": _pivot(rows, "dimension_label", PD, val="median_pepm"),
            "weighted": _pivot(rows, "dimension_label", PD, val="p99_winsorized_weighted_pepm"),
        }

    # ---- model share by segment (provider roll-up; named + 'other provider' buckets)
    msc = _raw("modelShareCurated")
    MD = sorted(set(r["date_month"][:7] for r in msc))
    P["model_share_curated"] = {"dates": MD, "dims": {}}
    for dim in sorted(set(r["dimension_type"] for r in msc)):
        rows = [r for r in msc if r["dimension_type"] == dim]
        labels = [l for _, l in sorted(set((r["display_order"], r["dimension_label"]) for r in rows))]
        prov = {}
        for r in rows:
            k = (r["dimension_label"], r["ai_provider"])
            prov.setdefault(k, [0.0] * len(MD))
            prov[k][MD.index(r["date_month"][:7])] += 100.0 * r["model_share"]
        P["model_share_curated"]["dims"][dim] = {
            "labels": labels,
            "provider_pct": dict(("%s|%s" % k, [round(v, 2) for v in s]) for k, s in prov.items()),
        }

    # ---- tokens (Token Spend Management sample)
    tv = _raw("tokenVolumes")
    WK = sorted(set(r["period_end"] for r in tv))
    vol, spd = {}, {}
    for r in tv:
        tgt = vol if r["metric_key"] == "token_volume" else spd
        tgt.setdefault(r["model_maker"], [0.0] * len(WK))
        tgt[r["model_maker"]][WK.index(r["period_end"])] += r["metric_value"]
    makers = sorted(vol, key=lambda m: -vol[m][-1])
    # monthly roll-up on complete months only (a month is complete when its last
    # calendar day <= the last period_end on file)
    import calendar
    MM = sorted(set(w[:7] for w in WK))
    last_day = WK[-1]
    MM = [m for m in MM if "%s-%02d" % (m, calendar.monthrange(int(m[:4]), int(m[5:7]))[1]) <= last_day]
    mvol, mspd = {}, {}
    for mk in vol:
        mvol[mk] = [sum(vol[mk][i] for i, w in enumerate(WK) if w[:7] == m) for m in MM]
        mspd[mk] = [sum(spd.get(mk, [0.0] * len(WK))[i] for i, w in enumerate(WK) if w[:7] == m) for m in MM]
    tp = _raw("tokenPrices")
    PDATES = sorted(set(r["usage_date"] for r in tp))
    PW = [d for d in PDATES if d in set(WK)] or PDATES[::7]
    prices = {}
    for r in tp:
        if r["usage_date"] not in PW:
            continue
        key = "%s|%s" % (r["model_maker"], r["token_type"])
        prices.setdefault(key, [None] * len(PW))
        prices[key][PW.index(r["usage_date"])] = round(1e6 * r["token_cost_usd_7d"] / r["token_count_7d"], 4) if r["token_count_7d"] else None
    P["tokens"] = {
        "weeks": WK, "makers": makers,
        "volume_by_maker": dict((m, [round(v) for v in vol[m]]) for m in vol),
        "spend_by_maker": dict((m, [round(v, 2) for v in spd.get(m, [0.0] * len(WK))]) for m in vol),
        "months_complete": MM,
        "monthly_volume_by_maker": dict((m, [round(v) for v in mvol[m]]) for m in mvol),
        "monthly_spend_by_maker": dict((m, [round(v, 2) for v in mspd[m]]) for m in mspd),
        "price_dates": PW, "price_usd_per_m": prices,
        "price_note": "token_cost_usd_7d / token_count_7d x 1e6 -- blended $ per million tokens, trailing 7 days, sampled on week-end dates",
        "definition": ("Ramp Token Spend Management product sample: usage + billing imported from "
                       "connected AI providers. Ramp: a SAMPLE of its businesses, 'not representative "
                       "of Ramp's total AI spend volume, though results are directionally similar'."),
        "model_count": len(set(r["series_key"] for r in tv)),
    }

    with io.open(os.path.join(DIR, "panel.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(P, indent=0, ensure_ascii=True))
    print("\npanel.json written: adoption %s -> %s (%d months), spend share %s, tokens %d weeks to %s (%d makers, %d model series)"
          % (AD[0], AD[-1], len(AD), SD[-1], len(WK), WK[-1], len(makers), P["tokens"]["model_count"]))
    print("  adoption %s: Ramp %.2f%% vs Census %s%% | vendor: %s | Anthropic > OpenAI since %s"
          % (AD[-1], P["adoption"]["overall"][-1], cen_all[-1],
             ", ".join("%s %.2f" % (k, v[-1]) for k, v in sorted(vendor.items(), key=lambda kv: -(kv[1][-1] or 0))), cross))
    tot = sum(vol[m][-1] for m in vol)
    print("  tokens week to %s: %s" % (WK[-1], ", ".join("%s %.1f%%" % (m, 100 * vol[m][-1] / tot) for m in makers[:6])))
    for key in ("anthropic|all_tokens", "openai|all_tokens"):
        if key in prices:
            print("  blended $/M %s: first %s -> latest %s" % (key, prices[key][0], prices[key][-1]))
    return P


# ============================================================ driver
def main():
    with io.open(CSV, newline="", encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if r.get("date_month")]
    dates = [r["date_month"][:7] for r in rows]
    n = len(dates)

    # regimes: rolling 12-month windows from the first observation, remainder last
    eras = []
    a = 1
    while a < n:
        b = min(a + 12, n)
        eras.append({"a": a, "b": b, "months": b - a,
                     "label": "%s - %s" % (label(dates[a]), label(dates[b - 1]))})
        a = b

    out = {
        "source": "Ramp AI Index",
        "series_name": "median monthly AI spend per employee, USD",
        "provenance": PROVENANCE,
        "caveats": [
            "Cohort definitions per Ramp's published note: 'Spend per Employee' = monthly "
            "observed AI spending / employee count for businesses in the reported cohort; "
            "'top 10%' / 'top 1%' are the MEDIAN within that cohort.",
            "RESTATED: Ramp re-cut the whole history in the Oct-2026 vintage (every month moved; "
            "see restatement.json). Quote the vintage with the number.",
            "Cohorts are re-cut every month, so a cohort's MoM step is part re-ranking and "
            "part same-company growth. This is why top-1% monthly sigma is ~3x the median's.",
            "Per-employee is a ratio: headcount moves the denominator.",
            "Latest month can restate. 2026-07 top-10% prints exactly 650.00 -- a round number "
            "to the cent in a two-decimal series reads as rounded or preliminary.",
            "Panel = Ramp's US corporate-card / bill-pay customer base, not total enterprise "
            "AI spend, and not a public-market revenue proxy.",
        ],
        "months": n, "first": dates[0], "latest": dates[-1],
        "dates": dates, "eras": eras, "cohorts": {},
    }

    for key, slug, name in COHORTS:
        lv = [float(r[key]) for r in rows]
        mom = [None] + [(lv[i] / lv[i - 1] - 1) * 100 for i in range(1, n)]
        r4 = lambda x: None if x is None else round(x, 4)
        out["cohorts"][slug] = {
            "name": name, "column": key,
            "level": [round(v, 2) for v in lv],
            "mom_pct": [r4(v) for v in mom],
            "compound_3m_pct": [r4(compound(lv, i, 3)) for i in range(n)],
            "compound_12m_pct": [r4(compound(lv, i, 12)) for i in range(n)],
            "yoy_pct": [r4(None if i < 12 else (lv[i] / lv[i - 12] - 1) * 100) for i in range(n)],
            "index_first_100": [round(v / lv[0] * 100, 1) for v in lv],
            "full_period": {
                "first": round(lv[0], 2), "last": round(lv[-1], 2),
                "multiple": round(lv[-1] / lv[0], 3),
                "compound_pct_mo": r4(compound(lv, n - 1, n - 1)),
                "down_months": sum(1 for v in mom[1:] if v < 0),
                "stdev_pp": r4((sum((v - sum(mom[1:]) / (n - 1)) ** 2 for v in mom[1:]) / (n - 1)) ** 0.5),
            },
            "eras": [{"label": e["label"], "months": e["months"],
                      "compound_pct_mo": r4(compound(lv, e["b"] - 1, e["b"] - e["a"])),
                      "multiple": round(lv[e["b"] - 1] / lv[e["a"] - 1], 3),
                      "down_months": sum(1 for v in mom[e["a"]:e["b"]] if v < 0)}
                     for e in eras],
        }

    with io.open(os.path.join(DIR, "series.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=True))
    with io.open(os.path.join(DIR, "latest.txt"), "w", encoding="utf-8") as f:
        f.write(dates[-1] + "\n")

    # paste-ready block for the theme pages
    print("series.json written: %d months, %s -> %s\n" % (n, dates[0], dates[-1]))
    print("| Cohort | %s | %s | 3-yr multiple | Compound | Last 12m | Down months |"
          % (label(dates[0]), label(dates[-1])))
    print("|---|---|---|---|---|---|---|")
    for _, slug, name in COHORTS:
        c = out["cohorts"][slug]; fp = c["full_period"]
        print("| %s | $%s | $%s | %.2fx | %+.2f%%/mo | %+.2f%%/mo | %d/%d |"
              % (name, format(fp["first"], ",.2f"), format(fp["last"], ",.2f"), fp["multiple"],
                 fp["compound_pct_mo"], c["compound_12m_pct"][-1], fp["down_months"], n - 1))
    print("\nRegime compound rates (%/mo):")
    for e in eras:
        print("  %-19s %s" % (e["label"], "  ".join(
            "%s %+6.2f" % (s, out["cohorts"][s]["eras"][eras.index(e)]["compound_pct_mo"])
            for _, s, _ in COHORTS)))

    build_model_share()
    build_restatement()
    build_panel()


if __name__ == "__main__":
    main()
