"""Funding coverage, USD bn; stdlib only. No invented maturity schedule."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
I={
 "asof":"2026-11-01",
 "source_filing":"Anthropic S-1 filed 2026-10-26; historical balances June 30",
 "source_model":"FUNDA model 2026-10-26; public post 2026-10-27; archived PDF pp.14-15,25-26",
 "cash":{"value":112.389,"tag":"HARD","source":"S-1 F-6"},
 "short_term_investments":{"value":19.262,"tag":"HARD","source":"S-1 F-6"},
 "restricted_cash_excluded":{"value":2.529,"tag":"HARD","source":"S-1 F-6"},
 "raise":{"value":100,"tag":"ESTIMATE","source":"User assumption: additional NET proceeds by Dec-2026"},
 "reserve":{"value":5,"tag":"ESTIMATE","source":"Conservative cash reserve anchored to $5bn liquidity covenant; not a legal covenant calculation"},
 "purchase_commitments":{"value":265.6,"tag":"HARD","source":"S-1 F-59; June stock"},
 "uncommenced_leases":{"value":321.4,"tag":"HARD","source":"S-1 F-37; undiscounted, some conditional"},
 "commenced_leases":{"value":2.124,"tag":"HARD","source":"S-1 F-37: 1.601 operating + 0.523 finance"},
 "q2_revenue":{"value":11.555,"tag":"HARD","source":"S-1 p.158"},
 "q2_opex":{"value":10.581,"tag":"HARD","source":"S-1 p.158"},
 "q2_compute":{"value":5.558,"tag":"HARD","source":"S-1 p.158"},
 "q2_sbc":{"value":1.261,"tag":"HARD","source":"S-1 pp.160-161"},
 "q1_revenue":{"value":4.731,"tag":"HARD","source":"S-1 p.158"},
 "q1_opex":{"value":6.398,"tag":"HARD","source":"S-1 p.158"},
 "q1_compute":{"value":3.387,"tag":"HARD","source":"S-1 p.158"},
 "q1_sbc":{"value":0.924,"tag":"HARD","source":"S-1 pp.160-161"},
 "q1_noncash_charity":{"value":0.126,"tag":"HARD","source":"S-1 p.161"},
 "funda_ipo":{"value":60,"tag":"ESTIMATE","source":"FUNDA pp.12,14-15; funda assumption"},
 "years":[2026,2027,2028,2029,2030],
 "funda_revenue":{"value":[52.8,118.3,197.9,304.4,438.4],"tag":"ESTIMATE","source":"FUNDA p.14; annual revenue, not exit ARR"},
 "funda_fcf":{"value":[4.0,-22.7,-19.4,35.0,103.1],"tag":"ESTIMATE","source":"FUNDA p.14, FCF AFTER finance-lease principal"},
 "funda_cash":{"value":[192.2,169.5,150.1,185.1,288.3],"tag":"ESTIMATE","source":"FUNDA p.14; includes IPO60; excludes revolver and notes; cash + STI"},
 "downside_cash_2030":{"value":16,"tag":"PARTIAL","source":"FUNDA p.15 chart, approximate forecast endpoint; Dec27 run-rate ~109, then +30/+25/+20%"},
 "stall_cash_2030":{"value":-176,"tag":"PARTIAL","source":"FUNDA p.15 chart, approximate forecast endpoint; run-rate ~83 flat, not zero revenue"},
 "spacex_month":{"value":3.1,"tag":"HARD","source":"S-1 p.172, approximate fees at full capacity expected Dec26"},
 "spacex_ceiling":{"value":120.5,"tag":"HARD","source":"S-1 p.172, UP TO, terms into 2029; cancellable"},
 "spcx_q3":{"value":14.575,"tag":"HARD","source":"SpaceX 10-Q filed 2026-10-22"},
 "spcx_b_share":{"value":0.345,"tag":"HARD","source":"SpaceX 10-Q concentration table; B unnamed"}
}
v=lambda k:I[k]["value"]
liq=v("cash")+v("short_term_investments")
res=liq+v("raise")
stock=v("purchase_commitments")+v("uncommenced_leases")
delta=v("raise")-v("funda_ipo")
cash=[c+delta for c in v("funda_cash")]
cost2=(v("q2_opex")-v("q2_compute")-v("q2_sbc"))/v("q2_revenue")
cost1=(v("q1_opex")-v("q1_compute")-v("q1_sbc")-v("q1_noncash_charity"))/v("q1_revenue")
burn=-(v("funda_fcf")[1]+v("funda_fcf")[2])
R={
 "static_liquidity":{"June":liq,"plus_raise_before_H2_cash_changes":res,"less_reserve":res-v("reserve"),"H2_cash_bridge":"UNKNOWN; static comparison only, not a December actual"},
 "stock_coverage":{"June_subtotal":stock,"including_commenced_leases":stock+v("commenced_leases"),"raise_pct":100*v("raise")/stock,"cash_plus_raise_pct":100*res/stock,"less_reserve_pct":100*(res-v("reserve"))/stock},
 "funda_rebased":{"delta":delta,"years":I["years"],"revenue":v("funda_revenue"),"cash":cash,"fcf_after_lease_principal":v("funda_fcf"),"trough_year_end":min(cash),"trough_year":I["years"][cash.index(min(cash))],"trough_headroom":min(cash)-v("reserve"),"peak_2027_28_burn":burn,"raise_over_burn":v("raise")/burn,"downside_end2030_approx":v("downside_cash_2030")+delta,"stall_end2030_approx":v("stall_cash_2030")+delta,"stall_funding_to_reserve":v("reserve")-v("stall_cash_2030")-delta},
 "sensitivities":{"extra_burn_10":[c-10*max(0,y-2026) for c,y in zip(cash,I["years"])],"extra_burn_25":[c-25*max(0,y-2026) for c,y in zip(cash,I["years"])],"downside_end2030_extra10":v("downside_cash_2030")+delta-40,"downside_end2030_extra15":v("downside_cash_2030")+delta-60,"downside_annual_extra_burn_to_reserve":(v("downside_cash_2030")+delta-v("reserve"))/4},
 "guardrails":{"Q2_noncompute_ratio":cost2,"Q1_noncompute_ratio":cost1,"independent_period_drift_pct":100*(cost1/cost2-1),"constant_stability":"RED: Q1 differs >25%; forward ratio is not externally validated","cash_rollforward_rounding_residuals":[round(v("funda_cash")[i]-v("funda_cash")[i-1]-v("funda_fcf")[i],6) for i in range(1,5)],"maturities":"AMBER: updated contractual annual payment table blank","growth":"AMBER: funda-hardcoded ARR, not guide or independently validated forecast","cash_basis":"GREEN: finance-lease principal included; noncash lease additions not cash","liquidity":"GREEN: restricted cash and conditional facilities excluded","customer_identity":"AMBER: filings do not identify Customer B"},
 "spacex":{"annualized":v("spacex_month")*12,"quarter":v("spacex_month")*3,"three_month_notice_cost_approx":v("spacex_month")*3,"raise_years_at_full_rate":v("raise")/(v("spacex_month")*12),"customer_b_q3":v("spcx_q3")*v("spcx_b_share"),"full_delivery_quarter_vs_Q3_pct":100*v("spacex_month")*3/v("spcx_q3"),"2027_gross_savings_if_stop_Jul1_or_Apr1":[v("spacex_month")*6,v("spacex_month")*9],"one_full_year_compute_spend_savings_replacement0_50_100pct_before_lost_contribution_and_transition_cost":[v("spacex_month")*12*(1-r) for r in (0,.5,1)],"limitations":"Exit dates are scenarios, not legal earliest dates. Notice cost is service payment, not penalty. Exact tranches and expiry dates unknown. No remaining-contract balance fabricated; no 2030 contractual savings. Savings exclude lost customer contribution and transition costs."}
}
assert abs(liq-131.651)<1e-9
assert abs(stock-587)<1e-9
assert max(map(abs,R["guardrails"]["cash_rollforward_rounding_residuals"]))<=.100001
(OUT/"inputs.json").write_text(json.dumps(I,indent=2),encoding="utf-8")
(OUT/"calculations.json").write_text(json.dumps(R,indent=2),encoding="utf-8")
print(json.dumps(R,indent=2))

