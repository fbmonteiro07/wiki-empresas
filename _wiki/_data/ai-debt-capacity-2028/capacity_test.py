"""2028 debt underwriting diagnostics, USD billions, as of 2026-10-16.

This deliberately does NOT turn debt-stock limits into annual financed capex.
Run with stdlib Python. The existing house valuation model is never modified.
"""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
est = json.loads((ROOT / '_wiki/_data/estimates.json').read_text(encoding='utf-8'))
forecast = est['companies']

def annual(ticker, period):
    p = forecast[ticker]['periods'][period]
    return {k: p[k] / 1000 for k in ('rev', 'ebit', 'ebitda', 'capex')}

def blend(a, b, weight):
    return {k: a[k] * weight + b[k] * (1-weight) for k in a}

rows = []
for ticker in ('MSFT', 'AMZN', 'GOOG', 'META', 'ORCL', 'SPCX', 'CRWV', 'NBIS', 'AKAM'):
    if ticker == 'MSFT':
        f = blend(annual(ticker, '2FY'), annual(ticker, '3FY'), .5)
        basis = 'CY2028 approximation: 1/2 FY2028 + 1/2 FY2029; no quarterly seasonality'
    elif ticker == 'ORCL':
        f = blend(annual(ticker, '2FY'), annual(ticker, '3FY'), 5/12)
        basis = 'CY2028 approximation: 5/12 FY2028 + 7/12 FY2029; no quarterly seasonality'
    else:
        f = annual(ticker, '3FY')
        basis = 'CY2028 = FY2028'
    rows.append(dict(ticker=ticker, **f, basis=basis, tag='PARTIAL',
                     source='Bloomberg consensus cache, 2026-10-16; adjusted earnings basis',
                     net_new_debt_capacity_2028=None,
                     reason='Opening debt, eligible cash flows and future loan amortization not fully reconciled'))

# These rating anchors are NOT lending covenants, and BBG EBITDA is NOT
# necessarily S&P adjusted EBITDA. This is a sensitivity identity, not capacity.
anchors = {'MSFT': 1., 'AMZN': 1.5, 'GOOG': 1., 'META': 1.}
for row in rows:
    if row['ticker'] in anchors:
        row['leverage_anchor'] = anchors[row['ticker']]
        row['closing_adjusted_net_debt_proxy'] = row['ebitda'] * row['leverage_anchor']
proxy = sum(r.get('closing_adjusted_net_debt_proxy', 0) for r in rows)

# CRWV: explicitly repair economic FCFF's noncash SBC deduction.
# Values here use rounded wiki house table, not spurious precision.
# Source: Felipe Monteiro / Capstone official model, 2026-10-14, build script
# lines 181-185, 277-285, and model_out.json. No cash SBC withholding assumed.
sbc26, sbc27, sbc28 = 12.8*.05, 26.7*.03, 44.69*.025
cash_buffer = 5.539  # HARD actual June 2026; holding it flat is ESTIMATE
net_debt26_cash = 45.4 - sbc26*(1+.095/2)
gross_open27 = net_debt26_cash + cash_buffer
gap27 = 29.6 - sbc27
cf27 = 50.9 - gap27
old_rate = .09  # ESTIMATE weighted cash-cost proxy, anchored to house 9% from 2027
net_borrow27 = (gap27 + old_rate*gross_open27)/(1-old_rate/2)
interest27 = net_borrow27-gap27
gross_open28 = gross_open27 + net_borrow27
gap28 = 28.3-sbc28
cf28 = 60.8-gap28
dscr = 1.35  # HARD DDTL5.5 covenant; extension to consolidated cash is ESTIMATE

def crwv_case(new_rate, principal, opening_book_principal=None):
    # Full refinancing of scheduled principal. Borrowing/repayment midpoint.
    # Only principal from the opening book changes from old_rate to new_rate.
    # Main sensitivities assume2028-originated loans start amortizing in2029.
    a_old = principal if opening_book_principal is None else opening_book_principal
    assert 0 <= a_old <= principal
    n = (gap28+old_rate*gross_open28+(new_rate-old_rate)*a_old/2)/(1-new_rate/2)
    interest = n-gap28
    max_n = 2*(cf28/dscr-principal-old_rate*gross_open28-
               (new_rate-old_rate)*a_old/2)/new_rate
    supported = min(n, max_n) if max_n >= 0 else None
    return dict(new_rate=new_rate, total_2028_principal=principal,
                opening_book_principal=a_old, principal_on_2028_originations=principal-a_old,
                required_net_borrowing=n, required_gross_borrowing=n+principal,
                interest=interest, adjusted_ebit_interest=8.85/interest,
                after_sbc_ebit_interest=(8.85-sbc28)/interest,
                adjusted_ebitda_interest=28.6/interest,
                illustrative_debt_service_coverage=cf28/(interest+principal),
                screen_supported_net=supported,
                capex_deferral_if_cash_generation_unchanged=(n-supported)*(1-new_rate/2) if supported is not None else None,
                flag='FAILS BEFORE NEW DEBT' if max_n < 0 else 'CONDITIONAL SCREEN ONLY')

def pv_annuity(rate, years):
    return (1-(1+rate)**(-years))/rate

nbis = next(r for r in rows if r['ticker']=='NBIS')
nbis_bound = {str(n): nbis['ebitda']/1.15*pv_annuity(.11,n) for n in (3,5)}

result = {
    'asof': '2026-10-16', 'units': 'USD billions unless ratio/rate',
    'status': 'PARTIAL UNDERWRITING DIAGNOSTIC; no validated ecosystem funded total',
    'withdrawn_claim': 'USD1.25tn financeable in 2028 derived from78.8% funding mix',
    'companies': rows,
    'big_four': {
        'closing_adjusted_net_debt_proxy': proxy,
        'formula': 'Maximum increase in adjusted net debt = proxy - opening2028 adjusted net debt. Net new financial borrowing additionally equals this headroom + change in qualifying cash - change in other agency debt adjustments. Reconcile agency EBITDA, leases and guarantees first.',
        'anchor_source': 'JPM / Erica Speer, hyperscaler equity-credit call 2026-07-20; Alphabet1x corroborated by S&P2026-02-09',
        'sensitivity_opening_adjusted_net_debt': {str(d): proxy-d for d in (400,600,800,1000)},
        'tag': 'PARTIAL; does not establish annual issuance absorption or borrowers willingness'
    },
    'crwv': {
        'source': 'Capstone / Felipe Monteiro official model2026-10-14; CRWV10-Q2026-08-12; DDTL5.5 SEC8-K2026-08-10',
        'sbc_addbacks': {'2026':sbc26,'2027':sbc27,'2028':sbc28},
        'opening2027_gross_debt_estimate':gross_open27,
        '2027_net_borrowing_estimate':net_borrow27,
        '2027_cash_interest_estimate':interest27,
        '2027_max_principal_under_same_screen':cf27/dscr-interest27,
        'opening2028_gross_debt_estimate':gross_open28,
        '2028_capex':60.8, '2028_preinterest_cash_gap':gap28,
        '2028_preinterest_cash_generation_proxy':cf28,
        'known2028_principal_on_June2026_debt_only':4.416,
        'old_debt_cash_rate_estimate':old_rate,
        'cases':[crwv_case(r,a) for r in (.09,.11,.14) for a in (10,15,16,17,20)],
        'max_principal_to_fund_full_plan': {
            str(r):(cf28/dscr*(1-r/2)-old_rate*gross_open28-r*gap28/2)/(1-old_rate/2)
            for r in (.09,.11,.14)
        },
        'limitations': [
            'Cash bridge assumes SBC is noncash, no offsetting buybacks/withholding; keeps house cash taxes unchanged, no interest tax shield.',
            'Opening2027 is a repaired house estimate, not committed financing;2027 must itself pass the path test.',
            'Cash-generation proxy includes working-capital/customer-prepayment inflows. It is NOT verified covenant CFADS.',
            '1.35x is DDTL5.5-specific, not a consolidated covenant or demonstrated origination threshold.',
            'Principal10/15/16/17/20bn are sensitivity inputs, not forecasts; actual future loan schedules are unavailable.',
            'Main cases assume all principal comes from the opening2028book, including2026-27originations;2028new loans start amortizing in2029. The function allows separate old-book and total principal inputs.',
            'Fixed/hedged debt retains a separate9% weighted-rate estimate; only new/refinanced debt bears the scenario rate.',
            'Capex reductions hold2028 operating cash constant; cuts that reduce commissioning/revenue would require a second operating-model iteration.',
            'No unrestricted funds released from pledged SPVs or incremental collateral/DSRA availability are assumed proven.'
        ]
    },
    'nbis': {
        'illustrative_total_amortizing_loan_stock':nbis_bound,
        'assumptions':'ESTIMATE:11% rate, annual end-year level debt service,100% of2028EBITDA unencumbered cash maintained3/5years;1.15x is actual July2026 facility covenant floor.',
        'warning':'Not2028newborrowing. Adjust for existing claims, revenue already collected as customer prepayments, contractual refunds if any, cash tax/capex/reserves, and pledged cash flows. Deferred revenue is not automatically a future cash refund. Secured collateral cannot be pledged twice.'
    },
    'amortization_evidence': {
        'META':{'2028':1.5,'source':'June2026 10-Q','tag':'HARD on outstanding stock only'},
        'SPCX':{'2028':2.867,'source':'June2026 10-Q debt table; includes other financings, not just2031+notes','tag':'HARD on outstanding stock only'},
        'ORCL':{'FY2028':10.145,'source':'May2026 10-K; not calendar2028','tag':'PARTIAL calendar bridge'},
        'AMZN':{'CY2028_principal_plus_interest':17.087,'source':'June2026 10-Q commitments; includes interest','tag':'HARD; not principal-only'},
        'MSFT':{'FY2028':0,'FY2029':2.001,'source':'June2026 10-K; do not equate FY2028zero with CY2028zero','tag':'PARTIAL calendar bridge'},
        'GOOG':{'CY2028_at_Dec2025':2.676,'source':'2025 10-K; must add later2026issuances and FX','tag':'PARTIAL stale principal floor'},
        'IREN':{'FY2028_at_June2026':.269927,'source':'FY2026 10-K; excludes later2.4bn30-month Mackenzie facility','tag':'PARTIAL calendar/new draws'},
        'NSCALE':{'CY2028_at_June2026':.0529,'conditional_convert_face_due_June2028':3.1,'source':'S-1 September18; automatically converts at IPO; NVIDIA1bn may issue directly as shares','tag':'PARTIAL contingent issuance/conversion; excludes laterfacilities'},
        'CIFR':{'CY2028':.296291,'source':'June2026 10-Q','tag':'HARD outstanding stock only'},
        'WULF':{'CY2028':.297290,'source':'June2026 10-Q','tag':'HARD outstanding stock only'}
    },
    'global_financeable_2028':None,
    'global_capex_cut_2028':None,
    'unassessed_names':['Lambda','Crusoe','Fluidstack','private projects','sovereign and regional clouds','APLD project-by-project borrowing base'],
    'guardrails':[
        'PASS: USD millions converted once to billions; calendar-year normalization explicit.',
        'PASS: gross borrowing minus principal equals net borrowing in every CRWV case.',
        'PASS: cash and economic FCFF separated; original house model preserved.',
        'BLOCK: cannot sum corporate stock ceiling, project loanstock and annual financing need.',
        'BLOCK: no company allocation of top-down1.25tn exists; residual is unassessed, not zero funding or capexcut.',
        'BLOCK: future amortization, contract cash waterfalls, guarantees/leases and2026-27 financing not fully reconciled.'
    ]
}
assert all(abs(c['required_gross_borrowing']-c['total_2028_principal']-c['required_net_borrowing'])<1e-9 for c in result['crwv']['cases'])
assert nbis_bound['5']>nbis_bound['3']
assert result['global_financeable_2028'] is None
(HERE/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'big_four_proxy':proxy,'crwv':{k:v for k,v in result['crwv'].items() if k not in ('limitations','cases')},'base_cases':[c for c in result['crwv']['cases'] if c['new_rate'] in (.11,.14) and c['total_2028_principal'] in (15,16)],'nbis':nbis_bound},indent=2))
