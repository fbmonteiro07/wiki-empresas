"""Reproducible one-off reconciliation, stdlib only. Outputs only to this data folder."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
u = {
    "tam_2030_bn": 173.0, "units_2030_m": 63.0,
    "tsmc_revenue_2025_bn": 3.667, "tsmc_revenue_2030_bn": 44.068,
    "tsmc_wafers_2025_kwpm": 18.0, "tsmc_wafers_2030_kwpm": 122.4,
    "wafer_asp_2025_usd": 17000.0, "wafer_asp_2030_usd": 30000.0,
    "units_2025_m": 23.0, "amd_share_2025": .24, "arm_share_2025": .16,
    "amd_share_2030": .29, "arm_share_2030": .42,
    "amd_wafers_2025_kwpm": 11.8, "arm_wafers_2025_kwpm": 6.1,
    "amd_wafers_2030_kwpm": 56.7, "arm_wafers_2030_kwpm": 65.7,
}

def content(wafers_kwpm, wafer_asp, cpu_units_m):
    return wafers_kwpm * 1000 * 12 * wafer_asp / (cpu_units_m * 1e6)

def scenario(tam=200.0, cpu_asp_factor=1.0, wafer_asp_factor=1.0,
             wafer_intensity_factor=1.0, served_share=None):
    share = u["amd_share_2030"] + u["arm_share_2030"]
    share_factor = 1 if served_share is None else served_share / share
    quantity_factor = tam/u["tam_2030_bn"]/cpu_asp_factor
    scale = quantity_factor * wafer_intensity_factor * share_factor
    return {"tam_bn": tam, "industry_cpu_units_m": u["units_2030_m"]*quantity_factor,
            "served_cpu_units_m": u["units_2030_m"]*quantity_factor*share*share_factor,
            "wafer_demand_kwpm": u["tsmc_wafers_2030_kwpm"]*scale,
            "annual_wafers_m": u["tsmc_wafers_2030_kwpm"]*scale*12/1000,
            "tsmc_revenue_bn": u["tsmc_revenue_2030_bn"]*scale*wafer_asp_factor}

served25 = u["units_2025_m"]*(u["amd_share_2025"]+u["arm_share_2025"])
served30 = u["units_2030_m"]*(u["amd_share_2030"]+u["arm_share_2030"])
intensity25 = u["tsmc_wafers_2025_kwpm"]*12000/(served25*1e6)
intensity30 = u["tsmc_wafers_2030_kwpm"]*12000/(served30*1e6)
by_vendor={}
for vendor in ["amd","arm"]:
    by_vendor[vendor]={}
    for yr in [2025,2030]:
        by_vendor[vendor][str(yr)] = content(u[f"{vendor}_wafers_{yr}_kwpm"],u[f"wafer_asp_{yr}_usd"],u[f"units_{yr}_m"]*u[f"{vendor}_share_{yr}"])

base=scenario()
ms_venice=6804/5.670
ms_vera=6229/5.750
bofa_hybrid=(24.9*by_vendor["amd"]["2030"]+27.8*by_vendor["arm"]["2030"])/1000*200/210.6
checks={
    "arithmetic_revenue_rounding": {"status":"PASS", "difference_pct":(122400*12*30000/(44.068e9)-1)*100, "kind":"identity only; not validation"},
    "independent_vendor_units_bofa_hybrid": {"status":"PASS_ORDER_OF_MAGNITUDE", "revenue_bn":bofa_hybrid,"difference_vs_base_pct":(bofa_hybrid/base["tsmc_revenue_bn"]-1)*100,"limitation":"BofA unit forecast independent; UBS content reused; not actual validation"},
    "independent_ms_venice_content": {"status":"PASS_ORDER_OF_MAGNITUDE", "usd_per_cpu":ms_venice,"difference_vs_ubs_amd_pct":(ms_venice/by_vendor["amd"]["2030"]-1)*100,"limitation":"2027 product forecast vs 2030 average; compute-only scope"},
    "independent_ms_vera_content": {"status":"PASS_ORDER_OF_MAGNITUDE", "usd_per_cpu":ms_vera,"difference_vs_ubs_arm_pct":(ms_vera/by_vendor["arm"]["2030"]-1)*100,"limitation":"Vera is one Arm product, not custom Arm fleet; both forecasts"},
    "observed_cpu_level_and_flow": {"status":"UNVALIDATED", "reason":"No reported CPU-specific revenue / shipments or foundry invoice series to calibrate and back-test"},
    "physical_average_area": {"status":"PARTIAL", "wafer_area_mm2_per_cpu_2030":intensity30*3.141592653589793*150**2, "reason":"Includes edge loss/yield/multi-die effects; no arbitrary yield plugged; not a physical die-size estimate"},
    "stock_flow": {"status":"PASS", "reason":"All revenues and units annual flows; kwpm monthly flow-equivalent requirement, never a cumulative installed base or new capex"},
    "scope": {"status":"PASS", "reason":"Server-only; Intel server wafers excluded; PCs and non-CPU GPUs/memory/packaging excluded; never incremental vs consensus"}
}
for name in ["independent_vendor_units_bofa_hybrid", "independent_ms_venice_content", "independent_ms_vera_content"]:
    check=checks[name]
    deviation=next(v for k,v in check.items() if k.startswith("difference"))
    if abs(deviation)>25: check["status"]="FLAG_OVER_25PCT"

out={"asof":"2026-09-22", "grounding":"PARTIAL: broker-calibrated scenario, not reported actual calibration", "input_tags":{"ubs":"HARD sourced broker estimates; all point inputs", "target_tam":"ESTIMATE: user scenario, $200bn", "holding_mix_intensity_asp":"ESTIMATE: explicit extension of UBS 2030 scenario", "bernstein":"PARTIAL: sourced ranges / approximate estimates", "bofa_and_ms":"HARD sourced independent forecasts; compatibility only"}, "ubs":u,
     "derived":{"industry_cpu_asp_2030_usd":173000/63,"tsmc_content_2025_usd":3667/served25,"tsmc_content_2030_usd":44068/served30,"served_units_2025_m":served25,"served_units_2030_m":served30,"wafer_intensity_ratio_2030_vs_2025":intensity30/intensity25,"vendor_content_usd":by_vendor,"revenue_increment_vs_2025_bn":base["tsmc_revenue_bn"]-3.667,"server_revenue_share_of_tam_2030":44.068/173,"cross_broker_scope_vintage_gap_2025_bn":[15-3.667,16-3.667]},
     "base":base,"scenarios":{"2025_wafer_intensity_with_2030_wafer_price":scenario(wafer_intensity_factor=intensity25/intensity30),"all_tam_uplift_from_cpu_price":scenario(cpu_asp_factor=200/173),"cpu_asp_plus20pct":scenario(cpu_asp_factor=1.2),"wafer_asp_minus20pct":scenario(wafer_asp_factor=.8),"wafer_asp_plus20pct":scenario(wafer_asp_factor=1.2),"tsmc_served_share_61pct":scenario(served_share=.61)},"checks":checks}
(HERE/"results.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
