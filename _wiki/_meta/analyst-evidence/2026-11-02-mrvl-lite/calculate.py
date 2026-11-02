"""MRVL/LITE fixed-ratio diagnostic. USD millions; shares millions. Stdlib only."""
import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parent
ip=root/'inputs.json'
if not ip.exists():
 e=json.loads((root.parents[2]/'_data/estimates.json').read_text(encoding='utf-8'))
 i={'asof':'2026-11-02','consensus_asof':e['asof'],
 'sources':{'terms':'Marvell/Lumentum joint release 2026-11-02, marvell-announcement.html',
 'consensus':'BBG estimates.json snapshot 2026-10-30, CY2027 and next fiscal quarter',
 'actual':'Lumentum Q1 FY27 release 2026-11-02, lumentum-q1fy27.html',
 'slides':'Transaction presentation 2026-11-02, pages 20-21'},
 'terms':{'exchange_ratio':4.5,'mrvl_ownership':.67,'lite_ownership':.33,'announced_lite_ev_m':115000,'announced_lite_per_share':1132,'premium':.239,'reference_date':'2026-10-28','close':'H1 CY2028','tag':'HARD announced terms, not closed'},
 'consensus':{t:{'px':e['companies'][t]['px'],**e['companies'][t]['periods']['CY2027']} for t in ['MRVL','LITE']},
 'consensus_tag':'HARD quoted source vintage; forecasts, not realized results',
 'lite_next_q':e['companies']['LITE']['periods']['2FQ'],
 'lite_actual':{'rev':1262.6,'eps':4.57,'ni':461.1,'shares':101.0,'tax':.165,'q2_rev_range':[1575,1625],'q2_eps_range':[5.9,6.2],'tag':'HARD company release, Q1 actual and Q2 guidance'},
 'synergies':{'announced_annual_run_rate_lower_bound':1000,'tag':'HARD management target, primarily COGS; timing unspecified'},
 'scenario_savings':[0,500,1000],'scenario_tag':'ESTIMATE conditional annual realized savings, not a year-one ramp forecast',
 'synergy_tax_tag':'PARTIAL: use sourced LITE FY27 non-GAAP 16.5% tax as proxy; not combined-company guidance',
 'deck':{'mrev':12600,'lrev':5100,'mgm':.58,'lgm':.53,'mopm':.37,'lopm':.42,'pf_gm':.57,'pf_opm':.39,'tag':'HARD rounded annualized-quarter slide inputs, NOT calendar-year forecasts'}}
 ip.write_text(json.dumps(i,indent=2),encoding='utf-8')
i=json.loads(ip.read_text());m,l=i['consensus']['MRVL'],i['consensus']['LITE'];r=i['terms']['exchange_ratio'];tax=i['lite_actual']['tax']
sm=m['ni']/m['eps'];sl=l['ni']/l['eps'];new=r*sl;total=sm+new;ni=m['ni']+l['ni'];base=ni/total;gap=sl*(r*m['eps']-l['eps'])
d=i['deck'];rev=d['mrev']+d['lrev'];gm=(d['mrev']*d['mgm']+d['lrev']*d['lgm'])/rev;opm=(d['mrev']*d['mopm']+d['lrev']*d['lopm'])/rev
rows=[]
for s in i['scenario_savings']:
 eps=(ni+s*(1-tax))/total
 rows.append({'pretax_savings_m':s,'aftertax_savings_m':s*(1-tax),'pf_eps':eps,'accretion_pct':100*(eps/m['eps']-1)})
o={'price_oct30':{'mrvl':m['px'],'lite':l['px'],'exchange_value':r*m['px'],'premium_pct':100*(r*m['px']/l['px']-1),'mrvl_parity':l['px']/r,'note':'Historical marks; not current quotes or a live merger-arbitrage spread'},
'ownership':{'new_shares_pct_existing_announced':100*.33/.67,'note':'Issuance differs from EPS dilution'},
'calibration':{'mrvl_shares_m':sm,'lite_shares_m':sl,'new_mrvl_shares_proxy_m':new,'combined_shares_proxy_m':total,'tag':'PARTIAL: NI/EPS quotients of consensus forecasts; not exact deal share counts'},
'cy2027_preclose_diagnostic':{'mrvl_eps':m['eps'],'lite_eps':l['eps'],'base_pf_eps':base,'base_dilution_pct':100*(base/m['eps']-1),'lite_eps_breakeven_no_synergies':r*m['eps'],'lite_eps_uplift_needed_pct':100*(r*m['eps']/l['eps']-1),'aftertax_gap_m':gap,'pretax_savings_breakeven_m':gap/(1-tax),'scenarios':rows,'tax_sensitivity':[{'tax':t,'pretax_breakeven_m':gap/(1-t)} for t in [.10,.165,.25]],'eps_per_100m_pretax_savings':100*(1-tax)/total,'announced_ownership_shortcut_eps':.67*m['eps']+.33*l['eps']/r,'note':'Common CY2027 BEFORE closing. Not a forecast of year one after H1 CY2028 close. Excludes integration costs, purchase accounting, intercompany elimination, revised earnings, revenue synergies; all-stock financing.'},
'margin_diagnostic':{'annualized_rev_m':rev,'calculated_gm':gm,'calculated_opm':opm,'company_pf_gm':d['pf_gm'],'company_pf_opm':d['pf_opm'],'cogs_savings_to_restore_mrvl_gm_m':d['lrev']*(d['mgm']-d['lgm']),'one_bn_savings_percent_sales':100*1000/rev,'note':'Rounded slide figures; no assumption all synergies go to COGS'},
'new_lite_guide_vs_oct30_consensus':{'eps_midpoint':sum(i['lite_actual']['q2_eps_range'])/2,'old_eps':i['lite_next_q']['eps'],'eps_upside_pct':100*((sum(i['lite_actual']['q2_eps_range'])/2)/i['lite_next_q']['eps']-1),'rev_midpoint':sum(i['lite_actual']['q2_rev_range'])/2,'old_rev':i['lite_next_q']['rev'],'rev_upside_pct':100*((sum(i['lite_actual']['q2_rev_range'])/2)/i['lite_next_q']['rev']-1),'note':'December 2026 quarter only. Do not extrapolate quarterly surprise to annual EPS'},
'guardrails':{'share_stock':{'status':('PARTIAL' if abs(sl/i['lite_actual']['shares']-1)<=.25 else 'FAIL'),'lite_proxy_vs_company_actual_pct':100*(sl/i['lite_actual']['shares']-1),'note':'Recent reported shares provide a scale check only: timing and construction differ from CY27 NI/EPS forecast proxies; exact deal issuance is not validated'},'ownership':{'status':('PARTIAL' if abs(new/total-.33)<=.01 else 'FAIL'),'lite_ownership_proxy':new/total,'announced':.33,'difference_pp':100*(new/total-.33),'note':'Approximate deal fully diluted ownership vs forecast weighted-average shares'},'basis':{'status':'PASS','note':'Annual NI / share stock = annual EPS; annual cost-savings flows. EV not confused with basic equity value'},'timing':{'status':'PARTIAL','note':'CY27 diagnostic cannot verify year-one-post-close guidance. No 2028/29 closing-year bridge or synergy ramp'},'rounding':{'status':('PARTIAL' if max(abs(gm-d['pf_gm']),abs(opm-d['pf_opm']))<=.01 else 'FAIL'),'gm_difference_pp':100*(gm-d['pf_gm']),'opm_difference_pp':100*(opm-d['pf_opm']),'note':'Rounded slide inputs; quote company PF57/39 separately'}}}
(root/'calculations.json').write_text(json.dumps(o,indent=2),encoding='utf-8')
print(json.dumps(o,indent=2))
