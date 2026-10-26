"""Reproducible arithmetic; USD billions unless explicitly noted. Stdlib only."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = 'Anthropic supplied S-1 dated 2026-10-26; filing-readable.txt'
qrev = [.376, .787, 1.382, 2.040, 4.731, 11.555]
qcompute = [.944, 1.390, 2.047, 2.945, 3.387, 5.558]
qop = [-.935, -1.200, -3.089, -2.836, -1.667, .974]
qadj = [-.830, -1.019, -1.284, -1.721, -.617, 2.235]
qnames = ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
quarterly = [dict(period=n, revenue=r, compute=c, gaap_operating_income=o,
                  adjusted_operating_income=a, gaap_operating_margin=o/r,
                  adjusted_operating_margin=a/r, revenue_per_compute_dollar=r/c,
                  sequential_growth=None if i==0 else r/qrev[i-1]-1,
                  input_tag='HARD', source=SOURCE+' lines 7401-7417, 7516-7524')
             for i,(n,r,c,o,a) in enumerate(zip(qnames,qrev,qcompute,qop,qadj))]
annual = []
for n,r,cor,rd,sm,ga,legal in [('2024',.386,.752,2.275,.163,.176,0),
                            ('2025',4.585,2.773,6.338,.911,1.123,1.5),
                            ('H1 2025',1.163,1.019,1.850,.239,.190,0),
                            ('H1 2026',16.286,2.380,9.741,3.808,1.050,0)]:
    annual.append(dict(period=n,revenue=r,cost_of_revenue=cor,gross_profit=r-cor,
        derived_gross_margin=1-cor/r,rd=rd,sales_marketing=sm,ga=ga,
        operating_income=r-cor-rd-sm-ga-legal,input_tag='HARD',
        source=SOURCE+' lines 15842-15862; margins DERIVED'))

# PARTIAL: original reporting, not the blank Q3 fields of the attachment.
q3_reported = 16.8
q3_source = ('Reuters Breakingviews / Karen Kwok, 2026-10-15, updated 10-16; '
 'https://www.breakingviews.com/40925ca4af2b/columns/breaking-view/anthropics-2-trln-dream-faces-deflation-trap-2026-10-15/')
scenarios=[]
for g in [-.1,0,.2,.4]:
    q4=q3_reported*(1+g)
    scenarios.append(dict(q4_sequential_growth_ESTIMATE=g,q4_revenue=q4,
        fy2026_revenue=16.286+q3_reported+q4,
        q4_average_quarter_annualized=q4*4,
        warning='Conditional sensitivity, not guidance or a probability-weighted forecast; annualized quarter is not defined Run-Rate Revenue.'))

# Anchor: observed Q2 adjusted non-compute expense. No guessed cost conversion.
q2_adjusted_noncompute = 10.581 - 5.558 - 1.261
noncompute_ratio = q2_adjusted_noncompute/11.555
margin_sensitivity=[dict(compute_share_ESTIMATE=c,
    adjusted_operating_margin=1-c-noncompute_ratio,
    adjusted_operating_income_per_100bn_revenue=100*(1-c-noncompute_ratio))
    for c in [.48,.50,.60,.70]]
q1_adjusted_noncompute_actual = 6.398-3.387-.924-.126
q1_predicted = noncompute_ratio*4.731
q1_error=q1_predicted/q1_adjusted_noncompute_actual-1
q1_noncompute_ratio=q1_adjusted_noncompute_actual/4.731
for row in margin_sensitivity:
    row['adjusted_margin_at_Q1_noncompute_ratio_ESTIMATE']=1-row['compute_share_ESTIMATE']-q1_noncompute_ratio

checks = {
 'quarter_revenue_sums_to_H1':abs(sum(qrev[-2:])-16.286)<1e-9,
 'quarter_op_sums_to_H1':abs(sum(qop[-2:])+.693)<1e-9,
 'functional_expenses_sum_to_natural_expenses_H1':abs(2.380+9.741+3.808+1.050-16.979)<1e-9,
 'adjusted_op_bridge_H1':abs(-.693+2.185+.126-1.618)<1e-9,
 'adjusted_net_bridge_H1':abs(-80.748+72.388+8.720+2.185+.126-2.671)<1e-9,
 'cashflow_reconciles_H1':abs(-80.748+2.185+.097+72.388+.126+8.720-.007-4.982+2.094+2.679-.003+1.380-3.929)<1e-9,
 'Q2_adj_cost_calibration_is_definition_not_validation':True,
 'Q1_cost_holdout_actual':q1_adjusted_noncompute_actual,
 'Q1_cost_holdout_predicted':q1_predicted,
 'Q1_cost_holdout_error':q1_error,
 'Q1_cost_holdout_within_25pct':abs(q1_error)<=.25,
 'Q1_cost_holdout_margin_error_pp':(q1_adjusted_noncompute_actual-q1_predicted)/4.731*100,
 'Q1_cost_holdout_interpretation':'AMBER: material 8.9pp margin error despite cost error below 25%; not forward validation.',
 'Q3_independent_rounded_scale_check':dict(headcount_approx=5300,revenue_per_employee_gt_millions=6.6,
    implied_Q3_rough_scale=5300*6.6/1000-2.040-16.286,
    reported_Q3_PARTIAL=q3_reported,
    caveat='Rounded headcount and a lower-bound productivity metric; scale consistency only, not exact validation.'),
 'full_forward_cashflow_validation':'UNAVAILABLE: September cash and annual obligation schedule blank; no annual cash runway claimed.',
 'current_commitments_rollforward':'UNAVAILABLE: do not sum June obligations, later amendments and counterparty face values into a current total.',
 'forecasts_externally_validated':False,
}
other={
 'H1_revenue_growth':16.286/1.163-1,
 'Q3_reported_sequential_growth':16.8/11.555-1,
 'H1_compute_share':8.945/16.286,
 'H1_gross_profit':16.286-2.380,
 'H1_after_cost_of_revenue_and_functional_SM_margin':(16.286-2.380-3.808)/16.286,
 'H1_rd_share':9.741/16.286,
 'H1_functional_SM_share':3.808/16.286,
 'H1_GA_share':1.050/16.286,
 'H1_consumption_share':13.064/16.286,
 'H1_subscription_share':3.222/16.286,
 'H1_international_share':4.523/16.286,
 'H1_net_working_capital_source':-4.982+2.094+2.679-.003+1.380,
 'H1_CFO_before_WC':3.929-(-4.982+2.094+2.679-.003+1.380),
 'H1_CFO_less_cash_capex':3.929-.482,
 'H1_CFO_less_cash_capex_finance_principal':3.929-.482-.004,
 'H1_net_investment_purchases':18.972-2.610,
 'H1_non_security_investing_cash_use':17.181-(18.972-2.610),
 'H1_liquid_assets':112.389+19.262,
 'June_purchase_and_uncommenced_lease_subtotal':265.6+321.4,
 'June_identified_obligations_including_commenced_undiscounted_leases':265.6+321.4+1.601+.523,
 'SpaceX_full_capacity_annualized_payment':3.1*12,
 'RPO_expected_next_12months':10.8*.75,
 'Q2_GAAP_compute_share_break_even_holding_other_cost_share':1-(10.581-5.558)/11.555,
 'Q2_adjusted_compute_share_break_even_holding_other_cost_share':1-noncompute_ratio,
 'H1_sbc_fraction_of_personnel':2.185/3.152,
 'June_RSU_unrecognized_annual_equivalent_sensitivity':23.7/2.1,
}
valuation = [dict(equity_value_ESTIMATE=v,fy2026_mid_scenario_multiple=v/scenarios[2]['fy2026_revenue'],
    Q3_reported_quarter_annualized_multiple=v/(16.8*4)) for v in [1500,2000]]
out=dict(as_of='2026-10-26',units='USD billions unless noted',quarterly=quarterly,
    functional_financials=annual,q3_reported_PARTIAL=dict(value=q3_reported,source=q3_source),
    scenarios=scenarios,cost_calibration=dict(anchor_q2_adjusted_noncompute=q2_adjusted_noncompute,
    ratio=noncompute_ratio,tag='DERIVED FROM HARD; future ratio held constant is ESTIMATE'),
    margin_sensitivity=margin_sensitivity,other=other,valuation_sensitivity=valuation,guardrails=checks)
ROOT.joinpath('calculations.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
