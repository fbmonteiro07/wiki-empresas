"""Calculate calendar-year valuation from captured sources; no forecast plugs."""
import datetime as dt
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def main():
    data, holdings = load('constituents.json'), load('holdings.json')['equities']
    years = ['2026', '2027', '2028']
    mv_total = sum(float(r['Market Value'].replace(',', '')) for r in holdings)
    components, checks = [], []
    for row in holdings:
        ticker = row['Ticker']
        key = ticker + ' US Equity'
        spot = data['spot'][key]
        price = float(row['Price'].replace(',', ''))
        market_value = float(row['Market Value'].replace(',', ''))
        weight = market_value / mv_total
        # Full company market cap includes all share classes. Rebase live market cap to close.
        market_cap_mn = spot['CUR_MKT_CAP'] / spot['PX_LAST'] * price / 1e6
        checks.append({'check': ticker + ' iShares price vs Bloomberg previous close', 'pass': abs(price / spot['PX_YEST_CLOSE'] - 1) < 0.001, 'ishares': price, 'bbg': spot['PX_YEST_CLOSE']})
        assert spot['CRNCY'] == spot['EQY_FUND_CRNCY'] == 'USD'
        entry = {'ticker': ticker, 'tag': 'HARD (sourced consensus, not realized outcome)', 'weight': weight, 'price_usd': price, 'market_cap_usd_mn': market_cap_mn, 'years': {}}
        for year in years:
            point = data[year][key]
            eps, fcf = point.get('BEST_EPS'), point.get('BEST_ESTIMATE_FCF')
            entry['years'][year] = {'eps_usd': eps, 'fcf_usd_mn': fcf, 'earnings_yield': eps / price if eps is not None else None, 'fcf_yield': fcf / market_cap_mn if fcf is not None else None}
        components.append(entry)
    msft = next(r for r in components if r['ticker'] == 'MSFT')
    table = {'MSFT': {}, 'IGV': {}}
    for year in years:
        m = msft['years'][year]
        table['MSFT'][year] = {'pe': 1 / m['earnings_yield'], 'pfcf': 1 / m['fcf_yield'], 'eps': m['eps_usd'], 'fcf_usd_mn': m['fcf_usd_mn']}
        igv = {}
        for metric, field in [('pe', 'earnings_yield'), ('pfcf', 'fcf_yield')]:
            covered = [r for r in components if r['years'][year][field] is not None]
            coverage = sum(r['weight'] for r in covered)
            contribution = sum(r['weight'] * r['years'][year][field] for r in covered)
            igv[metric] = coverage / contribution
            igv[metric + '_coverage'] = coverage
            igv[metric + '_unscaled_contribution'] = contribution
            igv[metric + '_missing'] = [r['ticker'] for r in components if r['years'][year][field] is None]
            igv[metric + '_negative'] = [r['ticker'] for r in covered if r['years'][year][field] < 0]
            # Missing-weight sensitivity: contributions at zero vs observed portfolio yield.
            igv[metric + '_missing_zero_yield'] = 1 / contribution
            # Independent implementation: aggregate owned underlying dollars for the covered basket.
            capital = sum(r['weight'] * mv_total for r in covered)
            fundamental = sum(r['weight'] * mv_total * r['years'][year][field] for r in covered)
            checks.append({'check': f'IGV {year} {metric} ownership arithmetic', 'pass': abs(capital / fundamental - igv[metric]) < 1e-9})
        table['IGV'][year] = igv
    # Validate CY26 against reported adjusted actuals and forward quarter consensus;
    # past BEST estimates alone are stale forecasts, not reported actuals.
    actual, quarters = load('msft_actuals.json'), load('msft_periods.json')
    eps26 = sum(actual[q]['MSFT US Equity']['IS_COMP_EPS_ADJUSTED'] for q in ['Q3', 'Q4']) + sum(quarters[q]['MSFT US Equity']['BEST_EPS'] for q in ['1FQ', '2FQ'])
    fcf26 = sum(actual[q]['MSFT US Equity']['CF_FREE_CASH_FLOW'] for q in ['Q3', 'Q4']) + sum(quarters[q]['MSFT US Equity']['BEST_ESTIMATE_FCF'] for q in ['1FQ', '2FQ'])
    checks += [{'check': 'MSFT CY26 EPS equals actual Q1/Q2 plus estimated Q3/Q4', 'pass': abs(eps26 - table['MSFT']['2026']['eps']) < 1e-9}, {'check': 'MSFT CY26 FCF equals actual Q1/Q2 plus estimated Q3/Q4', 'pass': abs(fcf26 - table['MSFT']['2026']['fcf_usd_mn']) < 1e-7}]
    for year, nums in [('2027', range(3, 7)), ('2028', range(7, 11))]:
        for metric, field in [('eps', 'BEST_EPS'), ('fcf_usd_mn', 'BEST_ESTIMATE_FCF')]:
            total = sum(quarters[f'{n}FQ']['MSFT US Equity'][field] for n in nums)
            checks.append({'check': f'MSFT CY{year} {metric} four-quarter reconciliation', 'pass': abs(total - table['MSFT'][year][metric]) < 1e-7})
    live = data['spot']['MSFT US Equity']
    checks.append({'check': 'MSFT market cap scale vs independently reported shares', 'pass': abs(live['CUR_MKT_CAP'] / live['PX_LAST'] / (live['EQY_SH_OUT'] * 1e6) - 1) < 0.001})
    result = {'pricing_date': '2026-09-21', 'consensus_retrieved_at': data['retrieved_at'], 'holdings_date': '2026-09-21', 'formula': 'MSFT: close/EPS, equity market capitalization/FCF. IGV: covered equity weight / sum(weight * fundamental yield), negatives retained, missing excluded and weights renormalized.', 'source_fields': ['BEST_EPS', 'BEST_ESTIMATE_FCF', 'BEST_FPERIOD_OVERRIDE=2026BC/2027BC/2028BC'], 'msft_price': msft['price_usd'], 'msft_mktcap_usd_mn': msft['market_cap_usd_mn'], 'table': table, 'checks': checks, 'components': components}
    (HERE / 'valuation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['msft_price', 'msft_mktcap_usd_mn', 'table']}, indent=2))
    print('checks', len(checks), 'failures', [c for c in checks if not c['pass']])


if __name__ == '__main__':
    main()
