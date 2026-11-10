r"""
Per-company view of the Aterio US data-center census: which wiki companies appear in it, in what role,
how many MW at each stage, when they activate and how likely Aterio thinks each project is to happen.

Reads   the newest Aterio export (P:\Felipe Monteiro\Aterio, same folder logic as build_aterio_dashboard.py):
          data-centers/inventory/data_center_inventory_<date>.csv
          power-generation/behind-the-meter-inventory/behind_the_meter_power_generation_inventory_<date>.csv
        _data/dc_projects/aterio/xchk.json        (which Aterio campuses the Capstone DC registry carries)
Writes  _data/aterio/company_exposure.json        (per ticker x role + market totals)
        _data/aterio/company_blocks/<TICKER>.md   (the markdown section for each company page)

        _data/aterio/theme_house_view.md          (the house-view section of themes/aterio-dc-census.md)

Feature script: it NEVER writes wiki pages. The page sections between the markers
`<!-- aterio-census:begin ... -->` / `<!-- aterio-census:end -->` are pasted from company_blocks/ by an
agent edit (with a Changelog line) when a new export lands. The theme page's house-view section
(`<!-- aterio-house-view:begin ... -->` / `:end -->`) is pasted from theme_house_view.md the same way.

Bases: MW = SELECTED_POWER_CAPACITY_MW = facility power per building (published, else Aterio's estimate).
Behind-the-meter rows are generation nameplate, a different basis: never add them to data-center MW.
Likelihood = Aterio's PROJECT_EXECUTION_LIKELIHOOD (High / Medium / Low; Aterio @ GS call 2026-10-20: High >80%
materialise, Medium ~50-60%, Low <40%). Active buildings carry no tier.

House view (Capstone treatment, rules in _data/aterio/treatment.json): every role also carries the GW IT-eq
that survive the house rules in 2026-30, through the shared loader aterio_core.py (same load, same masks, same
measured facility/IT ratio as the house view, the hyperscaler dashboard and the registry cross-check). As on the
hyperscaler dashboard, a hyperscaler self-build counts as naming its own tenant for rule 4. The US total and the
state table of the theme section come from _data/aterio/capstone_view.json (aterio_capstone_view.py): run that first.

    py build_aterio_company.py [--src <Aterio folder>]
"""
import argparse, json, os, re, sys
from collections import defaultdict

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import aterio_core as core  # noqa: E402
from build_aterio_dashboard import clean, split_list  # noqa: E402

WIKI = os.path.dirname(HERE)
OUT_DIR = os.path.join(WIKI, "_data", "aterio")
BLOCKS = os.path.join(OUT_DIR, "company_blocks")
THEME_MD = os.path.join(OUT_DIR, "theme_house_view.md")
VIEW = os.path.join(OUT_DIR, "capstone_view.json")
XCHK = os.path.join(WIKI, "_data", "dc_projects", "aterio", "xchk.json")
YEARS = [2026, 2027, 2028, 2029, 2030]
TIERS = ["High", "Medium", "Low"]
HB = ["online", "building", "delayed", "planned"]      # house-view buckets (planned = announced / land bank kept by the rules)

# ticker -> how it appears in the census. op_tick = PROVIDER_TICKER_NAME; the rest are regexes matched against
# single items of the comma-separated list fields. op_name also catches unlisted / private operators.
SPEC = {
    "AMZN": dict(op_tick="AMZN", tenant=r"^Amazon\b", btm_cust=r"^Amazon\b"),
    "MSFT": dict(op_tick="MSFT", tenant=r"^Microsoft$", btm_cust=r"^Microsoft$"),
    "GOOG": dict(op_tick="GOOG", tenant=r"^Google$", fin=r"^Google$", btm_cust=r"^Google$"),
    "META": dict(op_tick="META", tenant=r"^(Facebook|Meta)$", btm_cust=r"^(Facebook|Meta)$"),
    "ORCL": dict(op_tick="ORCL", op_name=r"\bOracle\b", tenant=r"^Oracle$"),
    "AAPL": dict(op_tick="AAPL"),
    "OPENAI": dict(op_name=r"\bOpenAI\b", tenant=r"^OpenAI$", btm_cust=r"^OpenAI$"),
    "ANTHROPIC": dict(tenant=r"^Anthropic$", btm_cust=r"^Anthropic$"),
    "SPCX": dict(op_name=r"\bxAI\b|\bX\.AI\b|SpaceX", tenant=r"^xAI$", btm_dev=r"^xAI$", btm_cust=r"^xAI$"),
    "CRWV": dict(op_tick="CRWV", op_name=r"CoreWeave", tenant=r"^CoreWeave$"),
    "NBIS": dict(op_tick="NBIS", op_name=r"Nebius", tenant=r"^Nebius$"),
    "NSCALE": dict(op_name=r"Nscale", tenant=r"^Nscale$", btm_dev=r"^Nscale$", btm_cust=r"^Nscale$"),
    "IREN": dict(op_tick="IREN", op_name=r"^Iren\b|^IREN\b"),
    "CEREBRAS": dict(op_name=r"Cerebras", tenant=r"^Cerebras$"),
    "TSLA": dict(op_tick="TSLA", op_name=r"^Tesla\b", btm_eq=r"^Tesla$"),
    "NVDA": dict(tenant=r"^NVIDIA$", backer=r"^(Nvidia|NVIDIA)$", fin=r"^NVIDIA$"),
    "AMD": dict(tenant=r"^AMD$", fin=r"^AMD$"),
    "JPM": dict(op_tick="JPM", fin=r"JPMorgan"),
    "GS": dict(fin=r"^Goldman Sachs"),
    "BX": dict(backer=r"Blackstone", fin=r"Blackstone"),
    "KKR": dict(backer=r"\bKKR\b", fin=r"\bKKR\b"),
    "BLK": dict(backer=r"BlackRock|Global Infrastructure Partners", fin=r"BlackRock"),
    "OWL": dict(backer=r"Blue Owl", fin=r"Blue Owl"),
    "APO": dict(backer=r"\bApollo\b", fin=r"\bApollo\b"),
    "GEV": dict(partner=r"GE Vernova", btm_eq=r"GE Vernova"),
    "BE": dict(partner=r"Bloom Energy", btm_eq=r"Bloom Energy"),
    "TLN": dict(partner=r"^Talen", util_tick="TLN", btm_dev=r"^Talen"),
    "VST": dict(partner=r"Luminant|Vistra", btm_dev=r"Luminant|Vistra"),
    "CEG": dict(partner=r"Constellation", btm_dev=r"Constellation"),
    "WMB": dict(partner=r"^Williams\b", btm_dev=r"^Williams\b"),
    "ETN": dict(partner=r"^Eaton\b", btm_eq=r"^Eaton\b"),
    "PWR": dict(partner=r"Quanta", btm_eq=r"Quanta"),
    "VRT": dict(partner=r"Vertiv", btm_eq=r"Vertiv"),
}
ROLE_LABEL = {
    "operator": "Operator / self-build",
    "tenant": "Named end user (someone else's building)",
    "backer": "Owner / backer of the developer",
    "fin": "Project financing",
    "partner": "Power, equipment or construction partner",
    "utility": "Serving utility",
}
BTM_LABEL = {"btm_dev": "developer", "btm_eq": "equipment / construction", "btm_cust": "customer"}


def items(v) -> list[str]:
    return [x for x in split_list(v) if x]


def any_match(v, rx) -> bool:
    return bool(rx) and any(re.search(rx, x, re.I) for x in items(v))


def lk_mix(d: pd.DataFrame) -> str:
    """Likelihood of a set of non-active buildings, MW-weighted: 'High', or 'High 70% · Medium 30%'."""
    s = d[d["like"].isin(TIERS)].groupby("like")["MW"].sum()
    if s.sum() <= 0:
        n = d["like"].isin(TIERS).sum()
        return "/".join(sorted(set(d.loc[d["like"].isin(TIERS), "like"]))) if n else "–"
    s = (s / s.sum() * 100).round()
    order = [t for t in TIERS if t in s.index and s[t] > 0]
    return order[0] if len(order) == 1 else " · ".join(f"{t} {s[t]:.0f}%" for t in order)


def dc_role(d: pd.DataFrame, reg_keys: set, show_provider: bool) -> dict:
    nonact = d[d["grp"] != "active"]
    win = nonact[nonact["yr"].between(2026, 2030)]
    out = {"n_bld": int(len(d)), "n_campus": int(d["key"].nunique()),
           "mw": {g: round(float(d.loc[d["grp"] == g, "MW"].sum()), 1) for g in ("active", "uc", "delayed", "ann", "wd")},
           "active_2026": round(float(d.loc[(d["grp"] == "active") & (d["yr"] == 2026), "MW"].sum()), 1),
           "win_tier": {t: round(float(win.loc[(win["like"] == t) & (win["grp"] != "wd"), "MW"].sum()), 1) for t in TIERS},
           "no_mw": int((d["MW"] <= 0).sum()),
           "years": {}, "campuses": []}
    # Capstone house view of this role: GW IT-eq kept by the rules (d["house"]), by activation year and bucket, next to
    # what Aterio dates to the window with no filter (d["dated"]); 'it' = facility MW ÷ the measured facility/IT ratio
    h = d[d["house"]]
    gw = lambda s: round(float(s.sum()) / 1000, 2)
    out["house"] = {"it_gw": gw(h["it"]), "by_year": {str(y): gw(h.loc[h["yr"] == y, "it"]) for y in YEARS},
                    "buckets": {b: gw(h.loc[h["bucket"] == b, "it"]) for b in HB},
                    "dated_it_gw": gw(d.loc[d["dated"], "it"]), "n_campus": int(h["key"].nunique())}
    live = nonact[nonact["grp"] != "wd"]
    for label, m in (("Under construction", live["grp"] == "uc"), ("Delayed", live["grp"] == "delayed"),
                     ("Planned · High", (live["grp"] == "ann") & (live["like"] == "High")),
                     ("Planned · Medium", (live["grp"] == "ann") & (live["like"] == "Medium")),
                     ("Planned · Low", (live["grp"] == "ann") & (live["like"] == "Low"))):
        x = live[m]
        row = {str(y): round(float(x.loc[x["yr"] == y, "MW"].sum()), 1) for y in YEARS}
        row["2031+"] = round(float(x.loc[x["yr"] >= 2031, "MW"].sum()), 1)
        row["undated"] = round(float(x.loc[x["yr"].isna(), "MW"].sum()), 1)
        out["years"][label] = row
    cams = []
    for k, c in d.groupby("key"):
        lw = c[(c["grp"].isin(["uc", "delayed", "ann"])) & c["yr"].between(2026, 2030)]
        a26 = c[(c["grp"] == "active") & (c["yr"] == 2026)]
        if lw.empty and a26.empty:
            continue
        cnt = c["grp"].value_counts()
        acts = sorted(x for x in lw["act"] if x)
        cams.append({
            "key": k, "name": clean(c["camp"].iloc[0]), "st": clean(c["STATE_CODE"].iloc[0]), "city": clean(c["CITY_NAME"].iloc[0]),
            "provider": clean(c["PROVIDER_NAME"].iloc[0]) if show_provider else "",
            "users": "; ".join(sorted({u for v in c["END_USER_COMPANIES"].dropna() for u in items(v)})),
            "stages": " · ".join(f"{cnt[g]} {lab}" for g, lab in (("active", "active"), ("uc", "UC"), ("delayed", "delayed"), ("ann", "planned"), ("wd", "withdrawn")) if cnt.get(g, 0)),
            "mw_uc": round(float(lw.loc[lw["grp"] == "uc", "MW"].sum()), 1),
            "mw_dl": round(float(lw.loc[lw["grp"] == "delayed", "MW"].sum()), 1),
            "mw_plan": round(float(lw.loc[lw["grp"] == "ann", "MW"].sum()), 1),
            "mw_a26": round(float(a26["MW"].sum()), 1),
            "like": lk_mix(lw) if not lw.empty else "–",
            "act": f"{acts[0]} → {acts[-1]}" if len(acts) > 1 and acts[0] != acts[-1] else (acts[0] if acts else ""),
            "pub_date": bool(lw["pub"].any()) if not lw.empty else False,
            "registry": k in reg_keys,
        })
    cams.sort(key=lambda x: -(x["mw_uc"] + x["mw_dl"] + x["mw_plan"] + x["mw_a26"]))
    out["n_campus_win"] = len(cams)
    out["campuses"] = cams
    return out


def btm_role(b: pd.DataFrame) -> dict:
    out = {"n_phase": int(len(b)), "n_project": int(b["ATERIO_POWER_GENERATION_PROJECT_UID"].nunique()),
           "mw": {s: round(float(v), 1) for s, v in b.groupby("PHASE_STAGE")["MW"].sum().items()}, "projects": []}
    for k, p in b.groupby("ATERIO_POWER_GENERATION_PROJECT_UID"):
        acts = sorted(x for x in p["act"] if x)
        out["projects"].append({"name": clean(p["PROJECT_NAME"].iloc[0]), "st": clean(p["STATE_CODE"].iloc[0]),
                                "tech": clean(p["ATERIO_PLANT_TECHNOLOGY_TYPE"].dropna().iloc[0]) if p["ATERIO_PLANT_TECHNOLOGY_TYPE"].notna().any() else "",
                                "fuel": clean(p["ATERIO_PLANT_ENERGY_SOURCE"].dropna().iloc[0]) if p["ATERIO_PLANT_ENERGY_SOURCE"].notna().any() else "",
                                "stages": " · ".join(f"{n} {s.lower()}" for s, n in p["PHASE_STAGE"].value_counts().items()),
                                "mw": round(float(p["MW"].sum()), 1),
                                "customers": clean(p["CUSTOMER_COMPANIES"].dropna().iloc[0]) if p["CUSTOMER_COMPANIES"].notna().any() else "",
                                "act": f"{acts[0]} → {acts[-1]}" if len(acts) > 1 and acts[0] != acts[-1] else (acts[0] if acts else "")})
    out["projects"].sort(key=lambda x: -x["mw"])
    return out


def load(src: str):
    """Inventory through the shared loader (aterio_core: US rows, every field, key / yr / act / grp / like) + the BTM
    inventory. Adds the house view per building: 'house' = kept by rules 2-4, 'dated' = everything Aterio dates to
    the window, 'bucket' = switched on / building / delayed / planned, 'it' = facility MW ÷ the measured ratio."""
    rules = core.rules()
    inv, asof = core.find_inventory(src)
    a = core.load(inv, cols=None, self_tenant=True)
    k = core.ratio(a, rules)["k"]
    m = core.masks(a, rules)
    a["MW"], a["camp"] = a["mw"], a["campus"]
    a["it"] = a["mw"] / k
    a["house"], a["dated"] = m["keep"], m["raw"]
    st = a["DATA_CENTER_STAGE"]
    a["bucket"] = np.select([m["act"], m["bld"] & (st == "Construction"), m["bld"] & (st == "Delayed"), m["ann"]], HB, "")
    a["pub"] = a["ESTIMATED_ACTIVATION_DATE_PUBLIC_SOURCE"].notna()
    bp, _ = core.find_btm(src)
    b = pd.read_csv(bp, low_memory=False)
    b = b[b["FLG_BTM_PROJECT"] == "Y"].copy()
    b["MW"] = pd.to_numeric(b["TOT_PHASE_NAMEPLATE_POWER_MW"], errors="coerce").fillna(0.0)
    b["act"] = pd.to_datetime(b["PHASE_SELECTED_ACTIVATION_DATE"], errors="coerce").dt.strftime("%Y-%m").fillna("")
    return a, b, inv, bp, asof, k, rules


def market(a: pd.DataFrame) -> dict:
    live = a[a["grp"].isin(["uc", "delayed", "ann"])]
    win = live[live["yr"].between(2026, 2030)]
    yrs = {}
    for label, m in (("Under construction", win["grp"] == "uc"), ("Delayed", win["grp"] == "delayed"),
                     ("Planned · High", (win["grp"] == "ann") & (win["like"] == "High")),
                     ("Planned · Medium", (win["grp"] == "ann") & (win["like"] == "Medium")),
                     ("Planned · Low", (win["grp"] == "ann") & (win["like"] == "Low"))):
        yrs[label] = {str(y): round(float(win.loc[m & (win["yr"] == y), "MW"].sum()), 1) for y in YEARS}
    st = win.groupby("STATE_CODE").apply(lambda d: pd.Series({
        "uc": d.loc[d["grp"] == "uc", "MW"].sum(), "high": d.loc[(d["grp"] == "ann") & (d["like"] == "High"), "MW"].sum(),
        "med": d.loc[(d["grp"] == "ann") & (d["like"] == "Medium"), "MW"].sum(), "low": d.loc[(d["grp"] == "ann") & (d["like"] == "Low"), "MW"].sum(),
        "dl": d.loc[d["grp"] == "delayed", "MW"].sum()}), include_groups=False)
    st["tot"] = st.sum(axis=1)
    st = st.sort_values("tot", ascending=False).head(12).round(0)
    return {"mw": {g: round(float(a.loc[a["grp"] == g, "MW"].sum()), 1) for g in ("active", "uc", "delayed", "ann", "wd")},
            "win_tier": {t: round(float(win.loc[win["like"] == t, "MW"].sum()), 1) for t in TIERS},
            "win_stage": {g: round(float(win.loc[win["grp"] == g, "MW"].sum()), 1) for g in ("uc", "delayed", "ann")},
            "years": yrs, "states": {k: {c: float(v) for c, v in r.items()} for k, r in st.iterrows()},
            "pub_share_win": round(float(win.loc[win["pub"], "MW"].sum() / max(1.0, win["MW"].sum())), 3)}


def fmt(mw: float) -> str:
    return f"{mw:,.0f}" if mw else "–"


def gwf(mw: float) -> str:
    return f"{mw / 1000:,.1f} GW" if mw >= 50 else (f"{mw:,.0f} MW" if mw else "0")


def g2(x: float) -> str:
    """GW for the house-view tables: 1 decimal from 10 GW, 2 below, – for zero."""
    return "–" if not x or abs(x) < 0.005 else (f"{x:,.1f}" if x >= 10 else f"{x:,.2f}")


def house_lines(roles: dict, k: float, rules: dict) -> list[str]:
    """The house-view part of a company section: GW IT-eq kept by the Capstone rules, per role."""
    y0, y1 = rules["window"]
    hi = " / ".join(rules["include"]["announced_likelihood"])
    head = f"**Capstone house view, {y0}-{y1 % 100} (GW IT-eq)**"
    rows = [(r, x["house"]) for r, x in roles.items() if x["house"]["it_gw"] or x["house"]["dated_it_gw"]]
    if not rows:
        return [f"{head}: nothing in the window for this company's roles ({core.rules_line(rules, k)}).", ""]
    L = [f"{head}: {core.rules_line(rules, k)}. This is the figure to quote; the other tables in this section stay on Aterio's own "
         f"basis (facility MW, every likelihood tier).", "",
         f"| Role in the census | House view | " + " | ".join(str(y) for y in YEARS)
         + f" | Switched on · building · delayed · planned {hi} | Aterio's dating, no filter |",
         "|---|---|" + "---|" * len(YEARS) + "---|---|"]
    for r, h in rows:
        L.append(f"| {ROLE_LABEL[r]} | **{g2(h['it_gw'])}** | " + " | ".join(g2(h["by_year"][str(y)]) for y in YEARS)
                 + " | " + " · ".join(g2(h["buckets"][b]) for b in HB) + f" | {g2(h['dated_it_gw'])} |")
    L += ["", "_GW IT-eq, same rules and code as the US house view on the reference page (`_tools/aterio_core.py`, rules in "
              "`_data/aterio/treatment.json`). A building counts for every company with a role on it, so never add rows across roles or pages._", ""]
    return L


def theme_section(out: dict, k: float, rules: dict) -> str:
    """The house-view section of themes/aterio-dc-census.md: US total from capstone_view.json + one row per company."""
    v = json.load(open(VIEW, encoding="utf-8"))
    if v["asof"] != out["asof"] or v["fac_it"] != k:
        sys.exit(f"capstone_view.json is from another export or ratio ({v['asof']}, ÷{v['fac_it']}): run aterio_capstone_view.py first")
    asof, (y0, y1) = out["asof"], rules["window"]
    us, raw, rm, fi = v["us"], v["raw"], v["removed"], v["sens"]["fac_it"]
    yrs = [str(y) for y in range(y0, y1 + 1)]
    hi = " / ".join(rules["include"]["announced_likelihood"])
    lo_band = min(fi["total_weighted"], fi["total_weighted_excl_eq1"], us["it"])
    L = [f"## Capstone house view (house rules of {rules.get('decided', '')})",
         f"<!-- aterio-house-view:begin asof={asof} · generated by _tools/build_aterio_company.py into _data/aterio/theme_house_view.md; "
         f"refresh = rerun aterio_capstone_view.py then the script, and paste the new section between these markers (agent edit + Changelog line), never by script -->",
         f"_Aterio data-center census as of {asof}, Capstone treatment. Rules: `_data/aterio/treatment.json` (decided by Felipe, {rules.get('decided', '')}); "
         f"one shared loader applies them everywhere: `_tools/aterio_core.py`. The rest of this page stays on Aterio's own basis (facility MW, every "
         f"likelihood tier); this section is the figure to quote as the house view. Dashboards: [house view and vintages](../_dashboards/dc-delay-risk.html#aterio-deck) · "
         f"[hyperscalers and company lookup](../_dashboards/aterio-hyperscalers.html)._", "",
         f"**{us['it']:.1f} GW IT-eq is due to switch on in the US in {y0}-{y1 % 100}** ({us['fac']:.1f} GW facility; {v['n_buildings']:,} buildings on "
         f"{v['n_campuses']:,} campuses), against {raw['it']:.1f} GW IT-eq that Aterio dates to the same window with no filter.", "",
         f"- **Rule 1, basis:** IT-eq = facility MW ÷ {k:g}, Aterio's own facility/IT median on the {fi['n']:,} buildings that carry both fields "
         f"({fi['n_eq1']} of them at exactly 1.000). The MW-weighted ratio (÷{fi['weighted']:.2f}) gives {fi['total_weighted']:.0f} GW and the ratio without the "
         f"1.000 rows (÷{fi['weighted_excl_eq1']:.2f}) gives {fi['total_weighted_excl_eq1']:.0f} GW: quote {lo_band:.0f}-{us['it']:.0f} GW as the band.",
         f"- **Rule 2, universe:** what switched on since Jan-{y0}, plus buildings under construction or delayed, plus planned buildings rated {hi}.",
         "- **Rule 3, dates:** Aterio's activation date as published, with no Capstone haircut on top.",
         "- **Rule 4, exclusion:** a campus rated Low whose buildings name no end user is dropped in every stage.",
         "- **Registry:** Capstone's public-source registry ([dc-delay-risk](../_dashboards/dc-delay-risk.html)) stays independent; Aterio is the cross-check, not the base.", "",
         f"| GW IT-eq | " + " | ".join(yrs) + f" | {y0}-{y1 % 100} |", "|---|" + "---|" * (len(yrs) + 1)]
    g1 = lambda x: "–" if abs(x) < 0.05 else f"{x:,.1f}"          # US-level tables: one decimal throughout
    mon = pd.Timestamp(asof).strftime("%b")
    for lab, b in ((f"Switched on (Jan-{mon} {asof[:4]})", "online"), ("Under construction", "building"), ("Delayed", "delayed"), (f"Planned · {hi}", "announced")):
        L.append(f"| {lab} | " + " | ".join(g1(us["by_year"][y][b]) for y in yrs) + f" | {g1(us['buckets'][b])} |")
    L.append("| **House view** | " + " | ".join(f"**{us['by_year'][y]['total']:.1f}**" for y in yrs) + f" | **{us['it']:.1f}** |")
    L.append("| Aterio's dating, no filter | " + " | ".join(f"{raw['by_year'][y]['total']:.1f}" for y in yrs) + f" | {raw['it']:.1f} |")
    cut = " · ".join(f"planned {lk} {g:.1f}" for lk, g in sorted(rm["announced_by_likelihood"].items(), key=lambda kv: -kv[1]))
    L += ["", f"**What the rules take out of the window (GW IT-eq):** {cut} · Low-likelihood campuses with no tenant {rm['low_no_tenant_built']:.1f} "
              f"(under construction, delayed or switched on). Outside the window and not counted: {rm['after_window']:.1f} GW dated after {y1} and "
              f"{rm['undated_pipeline']:.1f} GW with no date.", "",
          f"**Largest states, house view (GW IT-eq, {y0}-{y1 % 100})**", "",
          f"| State | House view | Switched on | Under constr. + delayed | Planned · {hi} | Aterio's dating, no filter |", "|---|---|---|---|---|---|"]
    for s in v["states"][:12]:
        L.append(f"| {s['st']} | **{s['it']:.1f}** | {g1(s['online'])} | {g1(s['building'])} | {g1(s['announced'])} | {s['raw_it']:.1f} |")
    cols = [r for r in ROLE_LABEL if any(r in rec["roles"] and (rec["roles"][r]["house"]["it_gw"] or rec["roles"][r]["house"]["dated_it_gw"]) for rec in out["tickers"].values())]
    short = {"operator": "Operator / self-build", "tenant": "Named end user", "backer": "Backer", "fin": "Project financing",
             "partner": "Power / equipment partner", "utility": "Serving utility"}
    L += ["", f"**House view by company (GW IT-eq, {y0}-{y1 % 100})** — same rules and code; a hyperscaler self-build counts as naming its own tenant for "
              f"rule 4 (as on the hyperscaler dashboard), which adds under 0.1 GW to the US total. A building counts for every company with a role on it, "
              f"so never add rows or columns. Blank = the company has no such role in the census; – = it has the role but nothing survives the rules.", "",
          "| Ticker | " + " | ".join(short[c] for c in cols) + " |", "|---|" + "---|" * len(cols)]
    for t, rec in out["tickers"].items():
        cells = [g2(rec["roles"][c]["house"]["it_gw"]) if c in rec["roles"] else "" for c in cols]
        if any(x not in ("", "–") for x in cells):
            L.append(f"| [{t}](../{t}.md) | " + " | ".join(cells) + " |")
    L.append("<!-- aterio-house-view:end -->")
    return "\n".join(L) + "\n"


def block(t: str, rec: dict, asof: str, k: float, rules: dict) -> str:
    L = [f"## DC construction pipeline — Aterio census ({asof})",
         f"<!-- aterio-census:begin asof={asof} · generated by _tools/build_aterio_company.py into _data/aterio/company_blocks/{t}.md; "
         f"refresh = rerun the script and paste the new block between these markers (agent edit + Changelog line), never by script -->",
         f"_Source: Aterio US data-center census, licensed export as of {asof} (internal use; `P:\\Felipe Monteiro\\Aterio`). "
         f"Reference page: [US DC construction pipeline — Aterio census](themes/aterio-dc-census.md) · explorer: [aterio-dc.html](_dashboards/aterio-dc.html). "
         f"MW = facility power per building (published, else Aterio's estimate); IT-eq ≈ facility ÷ {k:g}. "
         f"Likelihood = Aterio's execution tier: High = power negotiated, land secured, financing lined up or capex committed on earnings calls "
         f"(>80% materialise); Medium ~50-60%; Low = announced with no power or financing signal (<40%); a high tier does not mean the date holds "
         f"(Aterio team on a Goldman Sachs call, 2026-10-20). Activation dates are mostly Aterio's own estimates. Roles come from Aterio's fields "
         f"(operator, end users, backers, financing, partners) and are not checked one by one. "
         f"\"In registry\" = the campus is in Capstone's DC delay-risk registry ([dc-delay-risk](_dashboards/dc-delay-risk.html))._", ""]
    roles = rec["roles"]
    if roles:
        L += ["| Role in the census | Buildings | Active | Under construction | Delayed | Planned (all dates) | Withdrawn / cancelled | 2026-30 not yet active: High · Medium · Low |",
              "|---|---|---|---|---|---|---|---|"]
        for r, x in roles.items():
            m, wt = x["mw"], x["win_tier"]
            L.append(f"| {ROLE_LABEL[r]} | {x['n_bld']} on {x['n_campus']} campuses | {fmt(m['active'])} | {fmt(m['uc'])} | {fmt(m['delayed'])} | {fmt(m['ann'])} | {fmt(m['wd'])} | "
                     f"{fmt(wt['High'])} · {fmt(wt['Medium'])} · {fmt(wt['Low'])} |")
        L += ["", "_MW, facility basis. A building can count under several companies (operator, tenant, financier), so never add these rows across pages._", ""]
        L += house_lines(roles, k, rules)
        main =max(roles, key=lambda r: sum(roles[r]["mw"][g] for g in ("uc", "delayed", "ann")) + roles[r]["mw"]["active"])
        x = roles[main]
        yrs = x["years"]
        if any(sum(v.values()) for v in yrs.values()):
            L += [f"**When it switches on — {ROLE_LABEL[main].lower()}** (MW facility, by Aterio activation year; not yet active only)", "",
                  "| | 2026 | 2027 | 2028 | 2029 | 2030 | 2031+ | undated |", "|---|---|---|---|---|---|---|---|"]
            for lab, row in yrs.items():
                if sum(row.values()):
                    L.append(f"| {lab} | " + " | ".join(fmt(row[k]) for k in [str(y) for y in YEARS] + ["2031+", "undated"]) + " |")
            if x["active_2026"]:
                L.append(f"\n_Already switched on in 2026: {fmt(x['active_2026'])} MW._")
            L.append("")
        for r, x in roles.items():
            cams = x["campuses"][:10 if r == main else 6]
            if not cams:
                continue
            prov = r != "operator"
            more = f" (top {len(cams)} of {x['n_campus_win']})" if x["n_campus_win"] > len(cams) else ""
            L += [f"**Campuses with 2026-30 activity — {ROLE_LABEL[r].lower()}**{more}", "",
                  "| Campus | State | " + ("Operator | " if prov else "") + "Buildings | Under constr. MW | Delayed MW | Planned MW | Likelihood (not yet active) | Activation | In registry |",
                  "|---|---|" + ("---|" if prov else "") + "---|---|---|---|---|---|---|"]
            for c in cams:
                nm = c["name"] + (f" ({c['city']})" if c["city"] and c["city"].lower() not in c["name"].lower() else "")
                act = c["act"] + ("" if c["pub_date"] or not c["act"] else " (Aterio est.)")
                if c["mw_a26"] and not (c["mw_uc"] or c["mw_dl"] or c["mw_plan"]):
                    act = f"switched on 2026 ({fmt(c['mw_a26'])} MW)"
                L.append(f"| {nm} | {c['st']} | " + (f"{c['provider']} | " if prov else "") + f"{c['stages']} | {fmt(c['mw_uc'])} | {fmt(c['mw_dl'])} | {fmt(c['mw_plan'])} | {c['like']} | {act} | {'✓' if c['registry'] else '–'} |")
            L.append("")
        if any(x["no_mw"] for x in roles.values()):
            L.append(f"_Buildings with no MW in the census: {sum(x['no_mw'] for x in roles.values())} (counted in buildings, not in MW)._")
            L.append("")
    for r, x in rec["btm"].items():
        st = " · ".join(f"{s.lower()} {fmt(v)}" for s, v in sorted(x["mw"].items(), key=lambda kv: -kv[1]) if v)
        L += [f"**Behind-the-meter power for data centers — {BTM_LABEL[r]}** (Aterio BTM inventory: {x['n_phase']} phases on {x['n_project']} projects; "
              f"MW = generation **nameplate**, a different basis from the data-center MW above — never add them): {st}.", ""]
        if x["projects"]:
            L += ["| Project | State | Technology | Phases | Nameplate MW | Customers | Activation |", "|---|---|---|---|---|---|---|"]
            for p in x["projects"][:6]:
                L.append(f"| {p['name']} | {p['st']} | {p['tech'] or p['fuel']} | {p['stages']} | {fmt(p['mw'])} | {p['customers'] or '–'} | {p['act'] or '–'} |")
            L.append("")
    L.append("<!-- aterio-census:end -->")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    args = ap.parse_args()
    src = core.find_src(args.src)
    a, b, inv, bp, asof, k, rules = load(src)
    reg_keys = set()
    if os.path.exists(XCHK):
        x = json.load(open(XCHK, encoding="utf-8"))
        reg_keys = {kk for g in x.get("groups", []) for kk in g["at"]["keys"]}
    out = {"asof": asof, "inventory": os.path.basename(inv), "btm_inventory": os.path.basename(bp), "fac_it": k,
           "house_rules": {"decided": rules.get("decided"), "window": rules["window"], "line": core.rules_line(rules, k),
                           "self_tenant_tickers": list(core.SELF_TENANT_TICKERS)},
           "built": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"), "market": market(a), "tickers": {}}
    os.makedirs(BLOCKS, exist_ok=True)
    for t, s in SPEC.items():
        roles, btm = {}, {}
        op = pd.Series(False, index=a.index)
        if s.get("op_tick"):
            op |= a["PROVIDER_TICKER_NAME"].fillna("").str.upper().isin([s["op_tick"], {"GOOG": "GOOGL"}.get(s["op_tick"], s["op_tick"])])
        if s.get("op_name"):
            op |= a["PROVIDER_NAME"].fillna("").str.contains(s["op_name"], case=False, regex=True)
        masks = {"operator": op}
        if s.get("tenant"):
            masks["tenant"] = a["END_USER_COMPANIES"].map(lambda v: any_match(v, s["tenant"])) & ~op
        if s.get("backer"):
            masks["backer"] = a["PROVIDER_BACKED_BY"].map(lambda v: any_match(v, s["backer"]))
        if s.get("fin"):
            masks["fin"] = a["PROJECT_FINANCING_COMPANIES"].map(lambda v: any_match(v, s["fin"]))
        if s.get("partner"):
            masks["partner"] = a["CONSTRUCTION_EQUIPMENT_PROVIDER_COMPANIES"].map(lambda v: any_match(v, s["partner"]))
        if s.get("util_tick"):
            masks["utility"] = a["UTILITY_TICKER_NAME"].fillna("") == s["util_tick"]
        for r, m in masks.items():
            if m.any():
                roles[r] = dc_role(a[m], reg_keys, show_provider=(r != "operator"))
        for r, col in (("btm_dev", "DEVELOPER_COMPANIES"), ("btm_eq", "CONSTRUCTION_EQUIPMENT_PROVIDER_COMPANIES"), ("btm_cust", "CUSTOMER_COMPANIES")):
            if s.get(r):
                m = b[col].map(lambda v: any_match(v, s[r]))
                if m.any():
                    btm[r] = btm_role(b[m])
        if not roles and not btm:
            continue
        rec = {"roles": roles, "btm": btm}
        out["tickers"][t] = rec
        with open(os.path.join(BLOCKS, f"{t}.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(block(t, rec, asof, k, rules))
    with open(os.path.join(OUT_DIR, "company_exposure.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    with open(THEME_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(theme_section(out, k, rules))
    for t, rec in out["tickers"].items():
        bits = [f"{r} {rec['roles'][r]['n_bld']}b uc {rec['roles'][r]['mw']['uc']:.0f} plan {rec['roles'][r]['mw']['ann']:.0f} house {rec['roles'][r]['house']['it_gw']:.2f}" for r in rec["roles"]]
        bits += [f"{r} {rec['btm'][r]['n_phase']}ph" for r in rec["btm"]]
        print(f"{t:10} " + " | ".join(bits))
    print(f"{len(out['tickers'])} tickers · Aterio {asof} → {OUT_DIR}")


if __name__ == "__main__":
    main()
