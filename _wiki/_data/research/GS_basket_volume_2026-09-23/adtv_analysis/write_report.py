"""Render the sourced arithmetic and explicitly conditional basket scenario."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.loads((HERE / 'analysis.json').read_text(encoding='utf-8'))
stocks = d['stocks']
plnt = stocks['PLNT US Equity']
lines = [
    '# Basket liquidity and PLNT',
    '',
    'Bloomberg Desktop API, retrieved September 23, 2026. Stock observations refer to September 22, 2026.',
    '',
    'The previously extracted index volume equals the sum of the constituents’ volumes on their listed exchanges. It does not identify Goldman basket order flow, direction, client notional or dealer hedge executions. The basket turnover field likewise aggregates underlying trading. Neither is a valid observed basket trade notional.',
    '',
    '## Inputs and scope',
    '',
    '- **HARD:** constituent weights from Bloomberg `INDX_MWEIGHT`, reference snapshot on September 23 before US trading. These are snapshot weights, not verified execution-time weights.',
    '- **HARD:** constituent prices, shares traded and dollar turnover from Bloomberg historical `PX_LAST`, `PX_VOLUME` and `TURNOVER`, using US composite tickers. Equity TURNOVER is USD; the index field is USD thousands and is not used in the participation calculation.',
    '- **DERIVED from HARD:** dollar ADTV is mean daily TURNOVER over the 20 sessions from August 24 through September 21, excluding the September 22 event day. Share ADV is separately calculated from shares traded over the same sessions.',
    '- **ESTIMATE / illustrative scenario:** USD100,000,000 one-way basket order, 100% executed in constituent equities in proportion to the September 23 snapshot weights, compared with the liquidity baseline preceding September 22. The notional, full cash pass-through and applicability of snapshot weights are scenario assumptions. This does not reconstruct September 22 basket execution. A swap transaction need not result in the same immediate cash hedging.',
    '- Top ten means the ten largest basket weights. PLNT is shown separately even when outside the top ten.',
    '',
    '## PLNT: observed trading and hypothetical allocation',
    '',
    f"Close: ${plnt['price']:.2f}, versus ${plnt['previous_price']:.2f} on September 21. Derived close-to-close return: {plnt['close_return_pct']:.2f}%.",
    '',
    f"Observed share volume: {plnt['volume_shares']:,.0f}; preceding 20-session share ADV: {plnt['adv20_shares']:,.2f}; volume / ADV = {plnt['volume_vs_adv20_pct']:.2f}%.",
    '',
    f"Observed dollar turnover: ${plnt['turnover_usd']:,.0f}; preceding 20-session dollar ADTV: ${plnt['adtv20_usd']:,.2f}; turnover / ADTV = {plnt['turnover_vs_adtv20_pct']:.2f}%.",
    '',
    'These observed ratios describe all trading in PLNT and do not isolate basket-related trading.',
    '',
]
for basket, b in d['baskets'].items():
    p = b['PLNT']
    lines += [
        f"**{basket}:** PLNT weight {p['weight_pct']:.6f}% (rank {p['rank_by_weight']}).",
        '',
        f"1. Hypothetical PLNT allocation = $100,000,000 × {p['weight_pct'] / 100:.8f} = ${p['scenario_leg_usd']:,.0f}.",
        f"2. Dollar participation = ${p['scenario_leg_usd']:,.0f} / ${plnt['adtv20_usd']:,.2f} × 100 = {p['scenario_pct_adtv20']:.4f}% of dollar ADTV.",
        f"3. Basket order corresponding to 10% of PLNT dollar ADTV = 0.10 × ${plnt['adtv20_usd']:,.2f} / {p['weight_pct'] / 100:.8f} = ${p['scenario_basket_usd_for_10pct_adtv']:,.0f}.",
        '',
    ]

for basket, b in d['baskets'].items():
    lines += [f'## {basket}: top ten weights', '',
              'USD100m scenario is hypothetical. Dollar ADTV is consolidated US turnover; both percentage columns below use that same dollar denominator.', '',
              '| Stock | Weight (HARD) | Dollar ADTV20 (USD m, derived) | Observed Sep 22 turnover / ADTV | Hypothetical USD100m basket leg / ADTV |',
              '|---|---:|---:|---:|---:|']
    for r in b['top10_by_weight']:
        s = stocks[r['ticker']]
        lines.append(f"| {r['ticker'].split()[0]} | {r['weight_pct']:.3f}% | {s['adtv20_usd']/1_000_000:.2f} | {s['turnover_vs_adtv20_pct']:.1f}% | {r['scenario_pct_adtv20']:.2f}% |")
    lines.append('')

lines += [
    '## Price impact, sensitivity and checks', '',
    'No calibrated PLNT price-impact coefficient or actual signed basket order was supplied or observed. A causal price impact, expected PLNT closing price or portion of its observed decline attributable to these baskets is therefore unavailable. A percentage of ADTV is not a percentage price move.', '',
    'The participation equation has no fitted constant: allocation = basket notional × weight; participation = allocation / dollar ADTV. Doubling the hypothetical notional doubles participation. Changing the actual cash-hedged fraction scales the result proportionally. There is no claim of linearity between participation and price impact.', '',
    'Guards: both basket weight sums are within rounding of 100%; all constituent baselines have 20 prior trading sessions; currencies and consolidated volume bases match; historical turnover divided by volume produces a price consistent with the independently returned close. These checks validate the data and arithmetic, not a causal trading model.', '',
    'Pre-trade impact also depends on execution timing, volatility, spread, order size and participation. Source: [NYSE, Choey Li, October 17, 2023](https://www.nyse.com/data-insights/closing-auction-immediate-market-impact-price-drift-and-transaction-cost-of-trading-part-2).', '',
    'Raw Bloomberg source capture: [weights](../reference.json), [constituent history](constituents_history.json), [reference checks](constituents_reference.json), [original index-volume reconciliation](../verification.json). Calculation inputs and outputs: [analysis.json](analysis.json).', '',
    'Independent skeptic review: see [audit verdict](audit_verdict.md).',
]
(HERE / 'Basket_ADTV_and_PLNT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(HERE / 'Basket_ADTV_and_PLNT.md')
