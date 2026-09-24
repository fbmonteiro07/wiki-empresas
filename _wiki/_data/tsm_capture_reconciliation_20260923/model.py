"""Reconstruct the user's undated exhibit; no company estimate is updated.

Stdlib only. Rounded exhibit values constrain a family of models, not a unique
economic explanation. All cost shares below are inferred, not observed invoices.
"""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import json

D = Decimal
EXHIBIT = {
    "NVDA": ["5.2", "4.4", "4.6", "4.7", "4.7"],
    "AVGO": ["10.3", "8.8", "9.2", "9.4", "9.4"],
    "AMD": ["10.3", "8.8", "9.2", "9.4", "9.4"],
    "MRVL": ["10.3", "8.8", "9.2", "9.4", "9.4"],
    "MediaTek": ["21.9", "18.8", "19.6", "20.0", "20.0"],
    "Alchip": ["21.9", "18.8", "19.6", "20.0", "20.0"],
}
GM = {"NVDA": D("0.80"), "AVGO": D("0.60"), "AMD": D("0.60"),
      "MRVL": D("0.60"), "MediaTek": D("0.15"), "Alchip": D("0.15")}
# Representative points inside the joint rounding intervals, not precise estimates.
SHARES = list(map(D, ["0.258", "0.221", "0.231", "0.235", "0.235"]))

def rounded_percent(x):
    return str((x * 100).quantize(D("0.1"), rounding=ROUND_HALF_UP))

def run():
    output = {k: [rounded_percent(s * (1 - GM[k])) for s in SHARES] for k in GM}
    intervals = []
    for j in range(5):
        lower = max((D(EXHIBIT[k][j]) - D("0.05")) / 100 / (1-GM[k]) for k in GM)
        upper = min((D(EXHIBIT[k][j]) + D("0.05")) / 100 / (1-GM[k]) for k in GM)
        intervals.append({"lower_inclusive_pct": float(lower*100),
                          "upper_exclusive_pct": float(upper*100),
                          "selected_pct": float(SHARES[j]*100),
                          "inside": lower <= SHARES[j] < upper})
    # Exact shared-cost-share explanation of rounded columns imposes this GM bound.
    # Use the fourth column's highest group and NVDA interval conservatively.
    nvda_min_gm = 1-(D("4.75")/D("19.95"))
    sensitivity = {"NVDA_75pct_GM": float(SHARES[-1]*D("0.25")*100),
                   "AVGO_AMD_MRVL_50pct_GM": float(SHARES[-1]*D("0.50")*100),
                   "MediaTek_30pct_GM": float(SHARES[-1]*D("0.70")*100),
                   "MediaTek_40pct_GM": float(SHARES[-1]*D("0.60")*100),
                   "MediaTek_50pct_GM": float(SHARES[-1]*D("0.50")*100)}
    alternative_fits = []
    for a in map(D, ["0.78", "0.82"]):
        scale = (1-a)/D("0.20")
        alt_gm = {k: 1-(1-g)*scale for k,g in GM.items()}
        alt_shares = [s/scale for s in SHARES]
        alt_out = {k:[rounded_percent(s*(1-alt_gm[k])) for s in alt_shares] for k in GM}
        alternative_fits.append({"gm_pct":{k:float(g*100) for k,g in alt_gm.items()},
                                 "matches_all": alt_out == EXHIBIT})
    result = {
        "asof": "2026-09-23", "exhibit_source_and_column_dates": "unconfirmed",
        "formula": "capture = TSMC invoice / customer product revenue = (TSMC invoice / product COGS) * (1 - product gross margin)",
        "inputs": {
            "exhibit": {"tag":"ANCHOR", "meaning":"exact transcription of user exhibit; not verified actuals", "values_pct":EXHIBIT},
            "nvda_80pct_gm": {"tag":"PARTIAL", "source":"Unnamed expert, Capstone Notion transcript, 2026-09-09; approximate product illustration, not audited corporate GM"},
            "avgo_60pct_gm": {"tag":"PARTIAL", "source":"Same expert explicitly says 80% to 60%; transcript's earlier 16% is internally inconsistent"},
            "amd_mrvl_60pct_gm": {"tag":"ESTIMATE", "meaning":"assumed solely to reproduce shared rows; no product-specific validation"},
            "mediatek_alchip_15pct_gm": {"tag":"ESTIMATE", "meaning":"inferred conditional on NVDA 80%, a shared cost share, and observed ratios"},
            "tsmc_cogs_shares": {"tag":"ESTIMATE", "meaning":"inverse-fitted representative rounding-compatible values; same-column fit is not independent validation", "values_pct":[float(x*100) for x in SHARES]},
        },
        "reconstructed_pct":output,
        "rounding_intervals": intervals,
        "all_30_cells_match":output == EXHIBIT,
        "alternative_fits":alternative_fits,
        "sensitivity_last_column_pct":sensitivity,
        "cost_share_sensitivity_last_column_pct": {
            label: {k: float(SHARES[-1]*scale*(1-g)*100) for k,g in GM.items()}
            for label,scale in [("minus_10pct_relative",D("0.9")),("plus_10pct_relative",D("1.1"))]
        },
        "shared_share_nvda_min_gm_pct_conservative_rounding_bound":float(nvda_min_gm*100),
        "guardrails": {
            "arithmetic":"GREEN: all 30 rounded cells match",
            "physical_bounds":"GREEN within model: all margins and invoice/COGS shares between zero and one",
            "identification":"AMBER: multiple parameter families fit exactly; original formula unproven",
            "independent_margin_check":"AMBER: Sep 9 expert supports approximate NVDA/AVGO illustrative margins; Aug 3 Fubon discussion contemplates much higher MediaTek margins, on unconfirmed comparable scope",
            "independent_invoice_level":"UNVALIDATED: no matched product, generation, invoice scope or observed TSMC share of COGS",
            "flow_and_timing":"UNVALIDATED: columns are unlabeled; cannot map procurement timing to recognized customer revenue",
            "basis":"UNVALIDATED: wafer-only vs packaging and gross vs net HBM accounting unknown; must use matched product revenue, not automatically corporate sales",
        },
    }
    (Path(__file__).parent/"results.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    run()
