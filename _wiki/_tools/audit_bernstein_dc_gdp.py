"""Reproduce rounded Exhibit 6 labels and audit Aterio costs; stdlib only.
Not a reconstruction of Bernstein's undisclosed valuation model or GDP impact.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_data/aterio/gdp-audit-2026-11-09'
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = Path(r'P:\Felipe Monteiro\Aterio\data-centers\inventory\data_center_inventory_20260831.csv')
# HARD as printed, rounded labels only; not independently verified economic data.
STATES = 'WY NM IA NV TX OH GA OK WI AZ PA AL NE SC MI MD OR AR IL KS TN ID CO NY CA MN FL'.split()
TOTALS = [100,33,32,30,28,21,19,19,16,14,12,11,9,8,8,7,6,6,6,4,4,3,1,1,0,0,0]
LABOR = [36,12,12,11,10,8,7,7,6,5,4,4,3,3,3,2,2,2,2,2,1,1,None,None,None,None,None]
REST = [63,21,20,19,18,13,12,12,10,9,8,7,6,5,5,4,4,4,4,3,2,2,None,None,None,None,None]
# HARD: BEA via FRED, annual nominal 2025 GDP, September 30 2026 release.
# This denominator is an explicit reconstruction choice, NOT Bernstein's known vintage.
GDP_BN = {'WY':52.4912,'NM':152.1200,'IA':271.9372,'TX':2932.3436,'OH':976.8717,'GA':936.0867}
rows = [r for r in csv.DictReader(SOURCE.open(encoding='utf-8-sig')) if r['COUNTRY_CODE']=='US']
campuses = defaultdict(list)
for r in rows:
    campuses[r['ATERIO_DATA_CENTER_CAMPUS_UID'] or r['ATERIO_DATA_CENTER_UID']].append(r)
def number(r, key):
    return float(r[key] or 0)
audit = []
for state in sorted({r['STATE_CODE'] for r in rows}):
    uc = [r for r in rows if r['STATE_CODE']==state and r['DATA_CENTER_STAGE']=='Construction']
    keys = {r['ATERIO_DATA_CENTER_CAMPUS_UID'] or r['ATERIO_DATA_CENTER_UID'] for r in uc}
    groups = [campuses[k] for k in keys]
    values = [[number(r,'TOT_PROJECT_COST') for r in g if r['TOT_PROJECT_COST']] for g in groups]
    audit.append(dict(state=state,construction_buildings=len(uc),construction_facility_mw=sum(number(r,'SELECTED_POWER_CAPACITY_MW') for r in uc),
        qualifying_campuses=len(groups),campuses_with_cost=sum(bool(v) for v in values),
        conflicting_cost_campuses=sum(len(set(v))>1 for v in values),
        cross_state_campus_ids=sum(len({r['STATE_CODE'] for r in g})>1 for g in groups),
        naive_construction_row_cost_bn=sum(number(r,'TOT_PROJECT_COST') for r in uc)/1e9,
        known_full_campus_budget_bn=sum(max(v) if v else 0 for v in values)/1e9))
labels = []
for st, total, labor, rest in zip(STATES,TOTALS,LABOR,REST):
    d=dict(state=st,total_pct_printed=total,labor_pct_printed=labor,rest_pct_printed=rest)
    if st in GDP_BN:
        a=next(x for x in audit if x['state']==st)
        d.update(gdp_2025_bn=GDP_BN[st],gdp_source=f'https://fred.stlouisfed.org/series/{st}NGSP',
                 implied_budget_bn=total/100*GDP_BN[st],
                 implied_million_usd_per_construction_facility_mw=total/100*GDP_BN[st]*1000/a['construction_facility_mw'])
    labels.append(d)
focus = []
tx_cost = next(d['implied_million_usd_per_construction_facility_mw'] for d in labels if d['state']=='TX')
campus_detail = []
for state in ['TX','OH','GA']:
    a = next(x for x in audit if x['state']==state)
    d = next(x for x in labels if x['state']==state)
    calibrated_ratio = a['construction_facility_mw'] * tx_cost / 1000 / GDP_BN[state] * 100
    error = calibrated_ratio/d['total_pct_printed']-1
    focus.append(dict(state=state,bernstein_total_pct=d['total_pct_printed'],bernstein_labor_pct=d['labor_pct_printed'],
        gdp_2025_bn=GDP_BN[state],implied_budget_bn=d['implied_budget_bn'],
        implied_budget_rounding_low_bn=(d['total_pct_printed']-.5)/100*GDP_BN[state],
        implied_budget_rounding_high_bn=(d['total_pct_printed']+.5)/100*GDP_BN[state],
        construction_facility_gw=a['construction_facility_mw']/1000,
        implied_usdm_per_facility_mw=d['implied_million_usd_per_construction_facility_mw'],
        naive_cost_bn=a['naive_construction_row_cost_bn'],known_campus_budget_bn=a['known_full_campus_budget_bn'],
        known_campus_budget_over_gdp_pct=a['known_full_campus_budget_bn']/GDP_BN[state]*100,
        campuses_with_cost=a['campuses_with_cost'],qualifying_campuses=a['qualifying_campuses'],
        tx_calibrated_ratio_pct=calibrated_ratio,tx_calibrated_relative_error_pct=error*100,
        cross_state_fit='CALIBRATION ONLY' if state=='TX' else ('POINT ESTIMATE >25%; rounding-sensitive' if abs(error)>.25 else 'WITHIN 25%; weak holdout, not economic validation')))
    for key, group in campuses.items():
        uc=[r for r in group if r['STATE_CODE']==state and r['DATA_CENTER_STAGE']=='Construction']
        if not uc: continue
        costs=sorted({number(r,'TOT_PROJECT_COST')/1e9 for r in group if r['TOT_PROJECT_COST']})
        campus_detail.append(dict(state=state,campus_id=key,name=uc[0]['DATA_CENTER_CAMPUS_NAME'] or uc[0]['DATA_CENTER_BUILDING_NAME'],
            construction_buildings=len(uc),all_campus_buildings=len(group),
            construction_facility_mw=sum(number(r,'SELECTED_POWER_CAPACITY_MW') for r in uc),
            all_campus_facility_mw=sum(number(r,'SELECTED_POWER_CAPACITY_MW') for r in group),
            recorded_campus_cost_values_bn=costs,cost_source_urls=sorted({r['CAPEX_URL'] for r in group if r['CAPEX_URL']})))
(OUT/'tx-oh-ga-campus-detail.json').write_text(json.dumps(campus_detail,indent=2),encoding='utf-8')
payload=dict(source='Bernstein / Chad Dillard, Exhibit 6, 2026-11-04; user confirmed Bernstein',
    aterio_source=str(SOURCE),aterio_vintage='2026-08-31',gdp_basis='2025 annual nominal GDP, BEA via FRED, release 2026-09-30; Bernstein denominator unknown',
    labor_calibration={'tag':'PARTIAL / derived','formula':'36 / (36 + 63), from rounded Wyoming components','fraction':36/99,'headline_8pct_times_fraction':8*36/99},
    labels=labels,audit=audit,tx_oh_ga=focus,
    guardrails={'label_arithmetic':'PARTIAL: independently rounded components do not always add to printed totals; a printed zero does not establish zero activity',
    'deduplication':'PARTIAL: campus ID, building ID fallback; max conflicting cost retained. Cross-state campus IDs flagged; state totals are diagnostic and must not be summed without resolving allocation',
    'cost_coverage':'FAIL for full valuation: missing budgets, whole-campus vs construction-phase mismatch',
    'vintage':'FAIL for exact replication: August Aterio export vs November exhibit, GDP vintage unknown',
    'annual_flow':'FAIL for GDP impact: total project budget is not annual local value added',
    'headline_aggregation':'UNRESOLVED: 8% aggregation weights and geographic universe not disclosed in exhibit',
    'labor_validation':'UNRESOLVED: calibration to chart is not independent validation of labor share',
    'skeptic':'PARTIAL replication; independent TX/OH/GA raw-data and arithmetic check passed. Georgia threshold is rounding-sensitive. See skeptic-tx-oh-ga.txt; project URLs were exported, not externally verified.'})
(OUT/'audit.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
def table(data):
    heads=list(data[0]); return '<table><thead><tr>'+''.join('<th>'+escape(h.replace('_',' '))+'</th>' for h in heads)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(str(r.get(h,'')))+'</td>' for h in heads)+'</tr>' for r in data)+'</tbody></table>'
bars=''.join(f'<div class="row"><b>{r["state"]}</b><div><span style="width:{r["total_pct_printed"]}%"></span></div><strong>{r["total_pct_printed"]}%</strong></div>' for r in labels)
examples=[{'state':d['state'],'GDP_2025_bn':d['gdp_2025_bn'],'printed_ratio_pct':d['total_pct_printed'],'implied_project_budget_bn':round(d['implied_budget_bn'],2),'implied_USDm_per_MW':round(d['implied_million_usd_per_construction_facility_mw'],2)} for d in labels if 'gdp_2025_bn' in d]
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Bernstein data-center / GDP audit</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:0 24px;color:#182b43;background:#fafbfc}h1{font-size:30px}p,li{line-height:1.6}.row{display:grid;grid-template-columns:35px 1fr 55px;gap:12px;margin:7px 0;align-items:center}.row span{display:block;background:#294d7e;height:15px}.row>div{background:#edf0f5}table{border-collapse:collapse;width:100%;font-size:13px}td,th{padding:9px;border-bottom:1px solid #ccd5df;text-align:right}th{background:#edf0f5}section{overflow-x:auto;margin:24px 0}.note{padding:18px;background:#fff0d1}a{color:#175f9a}</style>
<h1>Can Bernstein's data-center / GDP calculation be recreated?</h1><p>Audit date: 9 November 2026 · Bernstein / Chad Dillard, Exhibit 6, 4 November 2026. Source confirmed by user. Exhibit credits Aterio, Haver Analytics and Bernstein analysis.</p>
<p class="note"><b>PARTIAL reconstruction.</b> Printed chart values can be recreated. The underlying numerator, labor assumption and headline aggregation cannot yet be independently validated. Total budgets divided by annual GDP measure project scale, not annual GDP contribution or the contraction from a freeze.</p>
<h2>Recreated total bars: project value / state GDP</h2><p>HARD as transcribed from the exhibit, rounded to whole percentages; not independently verified. Labor/rest labels are preserved in the data below. A printed 0% does not establish zero activity.</p>'''+bars+'''
<h2>The arithmetic</h2><p>State ratio = project value assigned to construction / nominal state GDP. Labor ratio = state ratio × assumed labor fraction. Wyoming's printed components imply 36 / (36 + 63) = 36.36% labor; 8% × 36.36% = 2.91%, which rounds to 3%. This is a PARTIAL calibration to rounded labels, not proof of Bernstein's exact assumption, nor an independent labor-cost check.</p>
<p>The examples below use HARD 2025 nominal BEA GDP figures (FRED release 30 September 2026). Selecting this GDP period is our explicit assumption: Haver's series, vintage and reference period used by Bernstein are unknown. Implied budgets are derived, not observed. Implied $/MW also uses the older August Aterio construction facility-MW denominator; it is a mismatch diagnostic, not a cost estimate.</p>'''+table(examples)+'''
<h2>Why the GDP interpretation fails</h2><ul><li>Projects span multiple years. A freeze affects spending that would otherwise occur during the period, not the entire original budget.</li><li>State GDP measures local value added. Imported or out-of-state equipment cannot all be assigned to the host state's production. Land transactions are not new production.</li><li>Labor cost is not automatically local value added: distinguish compensation, contractor invoices, off-site fabrication and local work.</li><li>Deduplicate campus costs and separate active, construction and future phases. Missing costs cannot be treated as zero.</li><li>To calculate aggregate exposure use sum of eligible budgets / sum of GDP for the same geography, not an unweighted mean of state percentages. The exhibit alone does not identify how 8% was aggregated.</li></ul>
<p>A proper annual impact estimate needs the baseline annual spending schedule, the spending actually displaced by a freeze, local value-added content, and any redeployment/offsets. No GDP-loss number is estimated here. Sensitivity is linear in budgets and labor share and inverse in GDP; doubling the spending horizon halves a simple annualized exposure proxy, but does not establish GDP impact.</p>
<h2>Aterio raw-cost audit, 31 August 2026</h2><p>HARD source fields with derived aggregations. US only; construction stage exactly. Qualifying campus = at least one building under construction. The known budget counts each qualifying campus once, using the largest recorded cost when values conflict. It includes whole-campus phases and omits missing budgets, so it is neither complete construction cost nor a lower bound on current construction spending. Naive total sums cost on construction rows and is shown only to expose repetition.</p><section>'''+table(audit)+'''</section><h2>Printed labels</h2><section>'''+table([{k:d[k] for k in ['state','total_pct_printed','labor_pct_printed','rest_pct_printed']} for d in labels])+'''</section><h2>Validation status</h2>'''+table([{'check':k,'status':v} for k,v in payload['guardrails'].items()])+'''
<h2>Sources</h2><ul><li>Bernstein / Chad Dillard, 4 November 2026, Exhibit 6, supplied screenshot. Full report methodology unavailable.</li><li>Aterio licensed census, 31 August 2026, local inventory CSV; campus-level cost definition also documented in the wiki Aterio theme.</li><li><a href="https://fred.stlouisfed.org/series/WYNGSP">BEA/FRED Wyoming</a> · <a href="https://fred.stlouisfed.org/series/NMNGSP">New Mexico</a> · <a href="https://fred.stlouisfed.org/series/IANGSP">Iowa</a> · <a href="https://fred.stlouisfed.org/series/TXNGSP">Texas</a></li><li><a href="https://www.bea.gov/help/glossary?title=GDP&amp;title_1=All">BEA GDP definitions</a></li></ul><p>Reproduction data: <a href="../_data/aterio/gdp-audit-2026-11-09/audit.json">audit.json</a>. Generator: _wiki/_tools/audit_bernstein_dc_gdp.py.</p></html>'''
focus_rows=[{'State':f['state'],'Bernstein total %':f['bernstein_total_pct'],'Labor %':f['bernstein_labor_pct'],
    'GDP $bn':round(f['gdp_2025_bn'],1),'Implied budget $bn':round(f['implied_budget_bn'],1),
    'Construction facility GW':round(f['construction_facility_gw'],3),'Implied $m/MW':round(f['implied_usdm_per_facility_mw'],2),
    'Known campus budgets $bn':round(f['known_campus_budget_bn'],2),
    'Cost coverage campuses':str(f['campuses_with_cost'])+'/'+str(f['qualifying_campuses'])} for f in focus]
fit_rows=[{'State':f['state'],'Ratio at TX implied $/MW':round(f['tx_calibrated_ratio_pct'],2),'Relative error %':round(f['tx_calibrated_relative_error_pct'],2),'Check':f['cross_state_fit']} for f in focus]
focus_html='<h2 id="tx-oh-ga">Texas, Ohio and Georgia — detailed check</h2><p>Added 9 November 2026. HARD inputs: Bernstein printed bars (4 November), Aterio source fields (31 August), BEA/FRED 2025 GDP (30 September release). DERIVED: all implied budgets, $/MW and aggregate costs. PARTIAL: period alignment and cross-state calibration. No assumed missing-campus budgets are filled.</p><section>'+table(focus_rows)+'</section><p>Arithmetic: implied budget = printed ratio / 100 × GDP. Implied $m/MW = implied budget $bn × 1,000 / construction facility MW. Known campus budgets are incomplete and include non-construction phases; their GDP ratios are not corrected estimates of the Bernstein bars. No cross-state campus IDs occur in these three subsets.</p><p>Diagnostic: calibrate a single cost per facility MW on Texas, then test Ohio and Georgia without refitting. This tests whether one common cost explains the exhibit with our older inventory, not whether that cost is real.</p>'+table(fit_rows)+'<p>Georgia breaches the 25% relative-error guardrail at printed midpoints; that threshold classification is sensitive to whole-percentage rounding. The mismatch itself remains: a common Texas-calibrated cost cannot reproduce all three bars on this inventory and GDP basis. Different data vintages, valuation assumptions or capacity scopes may explain the difference; the test cannot identify which. Changing the valuation constant by 10% moves this proxy by 10%; whole-percentage chart rounding creates ±0.5 percentage-point uncertainty before any vintage mismatch.</p><p>Full campus drill-down with source links, cost conflicts and missing budgets: <a href="../_data/aterio/gdp-audit-2026-11-09/tx-oh-ga-campus-detail.json">TX / OH / GA project records</a>. GDP sources: <a href="https://fred.stlouisfed.org/series/TXNGSP">Texas</a>, <a href="https://fred.stlouisfed.org/series/OHNGSP">Ohio</a>, <a href="https://fred.stlouisfed.org/series/GANGSP">Georgia</a>.</p>'
html=html.replace('<h2>Recreated total bars:',focus_html+'<h2>Recreated total bars:')
(ROOT/'_dashboards/bernstein-dc-gdp-audit.html').write_text(html,encoding='utf-8')
print(json.dumps(focus,indent=2))
print(json.dumps({'examples':examples,'labor_pct':36/99*100,'headline_labor_pct':8*36/99,'output':str(ROOT/'_dashboards/bernstein-dc-gdp-audit.html')},indent=2))
