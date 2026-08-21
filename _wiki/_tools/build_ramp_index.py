#!/usr/bin/env python
"""Ramp AI Index -> _data/ramp-ai-index/series.json (+ latest.txt).

Monthly alt-data indicator: median monthly AI-tool spend per employee across Ramp's
corporate card / bill-pay customer base, for three cohorts (all companies, top 10%,
top 1%). We hold the PRIMARY series; the wiki previously carried only second-hand
citations of it (Goldman 2026-08-14, MS via SPCX) -- see themes/tokenmaxxing.md.

Refresh: drop the newer CSV export over `_data/ramp-ai-index/spend_per_employee.csv`
(same header) and re-run. Prints a paste-ready markdown block for the theme pages.

    py "E:\\Wiki Felipe empresas\\_wiki\\_tools\\build_ramp_index.py"

Writes only under _wiki/_data (feature-script rule). stdlib only.
"""
import csv, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
DIR = os.path.join(WIKI, "_data", "ramp-ai-index")
CSV = os.path.join(DIR, "spend_per_employee.csv")

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


if __name__ == "__main__":
    main()
