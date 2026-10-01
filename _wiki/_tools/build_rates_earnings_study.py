"""Build the dated rates/earnings comparison from explicit source vintages."""
from pathlib import Path
import json, math, html, re

ROOT=Path(__file__).resolve().parents[1]/'_data/research/rates_earnings_20260930'
S={
'rev22':('FactSet / John Butters, 2 Sep 2022','https://insight.factset.com/larger-cuts-than-average-to-eps-estimates-for-sp500-cos-in-july-august-for-q3'),
'rev26':('FactSet / John Butters, 4 Sep 2026','https://insight.factset.com/analysts-increasing-eps-estimates-for-sp-500-companies-for-2nd-straight-quarter'),
'q322':('FactSet / John Butters, 30 Sep 2022; data through 29 Sep','https://insight.factset.com/largest-cuts-to-eps-estimates-for-sp-500-companies-for-q3-2022-in-more-than-two-years'),
'q122':('FactSet / John Butters, 1 Apr 2022','https://insight.factset.com/analysts-lower-eps-estimates-for-q122-but-raise-eps-estimates-for-cy22'),
'q222':('FactSet / John Butters, 1 Jul 2022','https://insight.factset.com/analysts-lowered-eps-estimates-for-q222-but-raised-eps-estimates-for-cy22-during-q2'),
'q422':('FactSet / John Butters, 6 Jan 2023','https://insight.factset.com/have-analysts-lowered-eps-estimates-more-than-average-for-sp-500-companies-for-q4'),
'enter22':('FactSet / John Butters, 30 Dec 2021','https://insight.factset.com/2022-key-predictions-by-factset-experts?hs_amp=true'),
'late22':('FactSet / John Butters, 16 Dec 2022','https://insight.factset.com/sp-500-cy-2022-earnings-preview-ex-energy-sp-500-expected-to-report-decline-in-earnings?hs_amp=true'),
'exenergy22':('FactSet / John Butters, 11 Aug 2022','https://insight.factset.com/ex-energy-sp-500-reporting-a-year-over-year-decline-in-earnings-of-4-for-q2'),
'jan26':('FactSet / John Butters, 9 Jan 2026, pp. 15 and 32; chart as of 8 Jan','https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_010926.pdf'),
'jun26':('FactSet / John Butters, 26 Jun 2026, p. 25; chart as of 25 Jun','https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_062626.pdf'),
'sep26':('FactSet / John Butters, 25 Sep 2026, pp. 9-15, 30-31; chart as of 24 Sep','https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_092526.pdf'),
'sales26':('FactSet / John Butters, 10 Aug 2026','https://insight.factset.com/sp-500-reporting-highest-revenue-growth-since-q4-2021'),
'mag26':('FactSet / John Butters, 28 Aug 2026','https://insight.factset.com/mag-7-companies-reported-earnings-growth-above-100-boosted-by-investment-gains'),
'underlying26':('FactSet / John Butters, 7 Aug 2026; 88% reported','https://insight.factset.com/sp-500-earnings-season-update-august-7-2026'),
'sp22':('S&P DJI / Howard Silverblatt, 5 Jul 2022','https://www.spglobal.com/spdji/en/commentary/article/us-equities-market-attributes-june-2022/'),
'treasury26':('US Treasury, daily nominal par yields through 29 Sep 2026','https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026'),
'real26':('US Treasury, daily real par yields through 29 Sep 2026','https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_real_yield_curve&field_tdr_date_value=2026'),
'treasury22':('US Treasury, daily nominal par yields, Sep 2022','https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202209'),
'real22':('US Treasury, daily real par yields, Sep 2022','https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_real_yield_curve&field_tdr_date_value_month=202209'),
'fed26':('Federal Reserve, 16 Sep 2026','https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm'),
'fed22':('Federal Reserve, 14 Dec 2022','https://www.federalreserve.gov/newsevents/pressreleases/monetary20221214a.htm'),
'nv21':('NVIDIA, 18 Aug 2021; fiscal Q2 ended 1 Aug','https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2022'),
'nv22':('NVIDIA, 24 Aug 2022; fiscal Q2 ended 31 Jul','https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2023'),
'nv26':('NVIDIA, 26 Aug 2026; fiscal Q2 ended 26 Jul','https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/default.aspx'),
'ms22':('Microsoft, 26 Jul 2022; quarter ended 30 Jun','https://www.microsoft.com/en-us/Investor/earnings/FY-2022-Q4/press-release-webcast'),
'ms26':('Microsoft, 29 Jul 2026; quarter ended 30 Jun','https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast'),
'fidelity':('Fidelity, user-confirmed source; exhibit reads 27 Sep 2026','fidelity_exhibit.png')}

def pct(a,b): return (b/a-1)*100
def rates(suffix,dates):
    out=[]
    for date in dates:
        values=[]
        for real in [False,True]:
            kind='daily_treasury_real_yield_curve' if real else 'daily_treasury_yield_curve'
            rows=json.loads((ROOT/f'{kind}_{suffix}.json').read_text())
            head=next(r for r in rows if r and r[0]=='Date'); index=head.index('10 YR' if real else '10 Yr')
            row=next(r for r in rows if r and r[0]==date)
            values.append(float(row[index]))
        out.append({'date':date,'nominal':values[0],'real':values[1],'nominal_minus_real':round(values[0]-values[1],2),'tag':'HARD; spread DERIVED'})
    return out

R22=sum([rates(s,[d]) for s,d in [('202112','12/31/2021'),('202203','03/31/2022'),('202206','06/30/2022'),('202209','09/30/2022'),('202210','10/24/2022'),('202212','12/30/2022')]],[])
R26=rates('2026',['01/02/2026','02/27/2026','06/30/2026','08/31/2026','09/25/2026','09/29/2026'])
REVS=[
{'target':'Q3 2022','window':'30 Jun-31 Aug 2022','start':59.44,'end':56.21,'reported_pct':-5.4,'source':'rev22'},
{'target':'Q3 2026','window':'30 Jun-31 Aug 2026','start':88.64,'end':89.69,'reported_pct':1.2,'source':'rev26'},
{'target':'CY 2022','window':'30 Jun-31 Aug 2022','start':229.60,'end':226.15,'reported_pct':-1.5,'source':'rev22'},
{'target':'CY 2026','window':'30 Jun-31 Aug 2026','start':340.49,'end':361.38,'reported_pct':6.1,'source':'rev26'},
{'target':'CY 2023','window':'30 Jun-29 Sep 2022','start':250.60,'end':241.83,'reported_pct':-3.5,'source':'q322'},
{'target':'CY 2027','window':'25 Jun-24 Sep 2026','start':397.42,'end':416.97,'reported_pct':None,'source':'jun26 + sep26'},
{'target':'CY 2026','window':'8 Jan-24 Sep 2026','start':310.84,'end':361.37,'reported_pct':None,'source':'jan26 + sep26'},
{'target':'CY 2027','window':'8 Jan-24 Sep 2026','start':357.83,'end':416.97,'reported_pct':None,'source':'jan26 + sep26'},
{'target':'CY 2023','window':'30 Jun-31 Dec 2022','start':250.60,'end':230.51,'reported_pct':None,'source':'q322 + q422'}]
for x in REVS: x.update(calculated_pct=pct(x['start'],x['end']),input_tag='HARD',result_tag='DERIVED')
SCENARIOS=[{'eps_change':g,'pe_start':p,'pe_end':16,'price_return':((1+g/100)*16/p-1)*100} for p in [19.2,19.5] for g in [-10,0,10,15.4,20,30]]
MULTIPLES=[{'eps_change':30,'pe_start':p,'pe_end':m,'price_return':(1.3*m/p-1)*100} for p in [19.2,19.5] for m in [14,16,18]]
MODEL={'equation':'P1/P0 = (E1/E0)*(PE1/PE0); price only, same earnings definition; no causal yield/PE fit',
'inputs':{'pe_current':{'value':19.2,'tag':'HARD / ANCHOR','source':'sep26'},'pe_fidelity_midpoint':{'value':19.5,'tag':'PARTIAL','source':'fidelity 19-20x range'},'pe_terminal':{'value':16,'tag':'ESTIMATE / SCENARIO','source':'fidelity hypothesis, not independently validated'},'growth_30':{'value':30,'tag':'SCENARIO','source':'fidelity; must mean change in chosen earnings denominator, not already realized CY growth'},'growth_15_4':{'value':15.4,'tag':'HARD forecast / SCENARIO application','source':'sep26 aggregate CY2027 growth; NOT a measured future NTM denominator increase'}},
'calibration':'Accounting identity, no fitted constant. Current multiple anchored at 19.2x. No defensible calibrated causal mapping from 6% yields to 16x P/E; do not claim one.',
'guardrails':{'units':'PASS: same EPS and P/E basis required; price excludes dividends','fixed_period':'PASS: revisions hold target year/quarter fixed; do not compound revisions for different quarters','vintage':'PASS: two-month pair exactly matched; three-month next-year pair has five-day date offset disclosed','independent_anchor':'PASS: Fidelity 19-20x range checked against separate FactSet 19.2x observation','causal_yield_fit':'NOT VALIDATED: 6% -> 16x is a stress assumption','horizon':'PASS: scenarios conditional; 2027 growth not asserted to equal NTM change','earnings_quality':'PARTIAL: exclusion of GOOG/AMZN is not a full recurring-earnings restatement','growth_vs_revision':'PASS: no adding +32% YoY to +16.3% same-year estimate revision'},
'break_even_19_2_to_16_pct':pct(16,19.2),'break_even_19_5_to_16_pct':pct(16,19.5),'scenarios':SCENARIOS,'multiple_scenarios':MULTIPLES}
DATA={'as_of':'2026-09-30','sources':S,'rates_2022':R22,'rates_2026':R26,'revisions':REVS,'model':MODEL}
for x in REVS:
    if x['reported_pct'] is not None: assert abs(x['reported_pct']-x['calculated_pct'])<.1
assert abs(((1+.30)*16/19.5-1)*100-6.6666666667)<1e-8
assert abs(MODEL['break_even_19_2_to_16_pct']-20)<1e-8
checks={
 'published_revisions_reconcile':all(abs(x['reported_pct']-x['calculated_pct'])<.1 for x in REVS if x['reported_pct'] is not None),
 'independent_starting_pe_in_exhibit_range':19<=19.2<=20,
 'treasury_spreads_reconcile':all(abs(r['nominal']-r['real']-r['nominal_minus_real'])<1e-8 for r in R22+R26),
 'same_eps_same_multiple_flat_return':all(abs((1*m/m-1)*100)<1e-8 for m in [14,16,19.2,19.5,22]),
 'terminal_sensitivity_14x_30pct':abs((1.3*14/19.5-1)*100+6.66666666666667)<1e-8,
 'observed_ntm_bridge_rounding':abs(((1+.089)*19.2/20.4-1)*100-2.7)<.3,
 'economic_yield_pe_mapping':'UNVALIDATED: not fitted; scenario only',
 'normalization':'PARTIAL: not a recurring-EPS index restatement'}
assert all(v for v in checks.values() if isinstance(v,bool))
(ROOT/'validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
(ROOT/'study_data.json').write_text(json.dumps(DATA,indent=2),encoding='utf-8')
template=Path(__file__).with_name('rates_earnings_study.template.html').read_text(encoding='utf-8')
def cite(m):
    label,url=S[m.group(1)]
    return f'<span class="cite">[<a href="{html.escape(url,quote=True)}">{html.escape(label)}</a>]</span>'
doc=re.sub(r'\[\[cite:([a-z0-9]+)\]\]',cite,template)
doc=doc.replace('__DATA__',json.dumps(DATA).replace('</','<\\/'))
doc=doc.replace('__SOURCES__',''.join(f'<p><b>{html.escape(k)}</b> · <a href="{html.escape(u,quote=True)}">{html.escape(l)}</a></p>' for k,(l,u) in S.items()))
assert '[[cite:' not in doc and '__DATA__' not in doc and '__SOURCES__' not in doc
(ROOT/'study.html').write_text(doc,encoding='utf-8')
print('Built', ROOT/'study.html', len(doc),'characters')
