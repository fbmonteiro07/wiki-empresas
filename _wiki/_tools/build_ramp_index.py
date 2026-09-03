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
        "provenance": ("CSV supplied by Felipe 2026-09-02 (ramp-ai-index-model-share.csv). "
                       "Ramp's methodology note is NOT verified -- see caveats."),
        "caveats": [
            "COVERAGE: the panel names only Anthropic, OpenAI, xAI and Cursor. Google/Gemini, "
            "Meta, Mistral and DeepSeek appear in NO month. This is share of the covered set, "
            "not share of enterprise LLM usage, and it is not a market share.",
            "BASIS: what the share is weighted by (spend, API calls, tokens, or firms) is not "
            "stated in the export. Every row is model_type='Named model', which implies Ramp "
            "also holds a non-named bucket that this export excludes.",
            "NOT the same cut as Ramp's vendor-adoption number (~41% of US firms use Anthropic "
            "vs ~39.5% OpenAI, Jun-2026, on ANTHROPIC.md): that counts FIRMS and overlaps "
            "across vendors; this sums to 100. The two are reconcilable only as penetration "
            "vs intensity -- they are not alternative estimates of one quantity.",
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
        "provenance": ("CSV supplied by Felipe 2026-08-20 "
                       "(ramp-ai-index-spend-per-employee.csv). Ramp's own methodology note "
                       "is NOT yet verified -- cohort definitions below are read off the "
                       "column headers."),
        "caveats": [
            "Cohort definitions inferred from column names: 'top 10%' / 'top 1%' read as the "
            "MEDIAN spend per employee WITHIN that cohort. Unconfirmed against Ramp's docs.",
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


if __name__ == "__main__":
    main()
