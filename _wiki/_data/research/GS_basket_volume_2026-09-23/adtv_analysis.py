"""Read-only Bloomberg constituent liquidity and explicit basket-notional scenarios."""
import datetime as dt
import json
from pathlib import Path
import statistics
import sys

import blpapi

from pull_basket_volume import collect, HERE

OUT = HERE / 'adtv_analysis'
OUT.mkdir(exist_ok=True)
ASOF = '2026-09-22'


def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def capture(session, request, name):
    result = {'source': 'Bloomberg Desktop API', 'retrieved_at': dt.datetime.now().astimezone().isoformat(),
              'request': str(request), 'messages': collect(session, request)}
    write(name, result)
    return result


def security_rows(data):
    out = {}
    for message in data['messages']:
        securities = message['data'].get('securityData', [])
        if isinstance(securities, dict):
            securities = [securities]
        for security in securities:
            if security.get('securityError'):
                raise ValueError(security['securityError'])
            out[security['security']] = security
    return out


def main():
    ref = security_rows(json.loads((HERE / 'reference.json').read_text(encoding='utf-8')))
    weights = {ticker: row['fieldData']['INDX_MWEIGHT'] for ticker, row in ref.items()}
    tickers = sorted({m['Member Ticker and Exchange Code'].split()[0] + ' US Equity' for members in weights.values() for m in members})
    if sys.argv[1] == 'pull':
        options = blpapi.SessionOptions()
        options.setServerHost('localhost')
        options.setServerPort(8194)
        options.setConnectTimeout(5000)
        session = blpapi.Session(options)
        if not session.start():
            raise RuntimeError('Bloomberg unavailable')
        try:
            if not session.openService('//blp/refdata'):
                raise RuntimeError('Bloomberg refdata unavailable')
            service = session.getService('//blp/refdata')
            request = service.createRequest('HistoricalDataRequest')
            for ticker in tickers:
                request.append('securities', ticker)
            for field in ['PX_LAST', 'PX_VOLUME', 'TURNOVER']:
                request.append('fields', field)
            request.set('startDate', '20260801')
            request.set('endDate', '20260922')
            request.set('periodicitySelection', 'DAILY')
            data = capture(session, request, 'constituents_history.json')
            print('History securities:', len(security_rows(data)))
            request = service.createRequest('ReferenceDataRequest')
            for ticker in tickers:
                request.append('securities', ticker)
            for field in ['NAME', 'CRNCY', 'PX_LAST', 'PX_VOLUME', 'LAST_UPDATE_DT', 'VOLUME_AVG_20D', 'CUR_MKT_CAP']:
                request.append('fields', field)
            data = capture(session, request, 'constituents_reference.json')
            print('Reference securities:', len(security_rows(data)))
        finally:
            session.stop()
        return

    data = json.loads((OUT / 'constituents_history.json').read_text(encoding='utf-8'))
    hist = security_rows(data)
    spot = security_rows(json.loads((OUT / 'constituents_reference.json').read_text(encoding='utf-8')))
    output = {'asof': ASOF, 'retrieved_at': data['retrieved_at'], 'scenario_notional_usd': 100_000_000,
              'scenario_notional_tag': 'ESTIMATE: illustrative input, not a claimed observed basket trade',
              'weights_tag': 'HARD: Bloomberg INDX_MWEIGHT reference snapshot retrieved 2026-09-23',
              'prices_volumes_turnover_tag': 'HARD: Bloomberg US composite historical data',
              'ADTV_basis': 'Arithmetic mean of US composite daily TURNOVER over 20 completed trading sessions strictly before 2026-09-22; raw equity turnover in USD',
              'calibration': 'No impact coefficient or causal price-impact estimate. ADTV participation is an arithmetic identity conditional on scenario notional and holdings.',
              'stocks': {}, 'baskets': {}}
    for ticker in tickers:
        rows = hist[ticker]['fieldData']
        current = next(r for r in rows if r['date'] == ASOF)
        prior = [r for r in rows if r['date'] < ASOF and r.get('PX_VOLUME', 0) > 0 and r.get('TURNOVER', 0) > 0][-20:]
        if len(prior) != 20:
            raise ValueError(f'{ticker}: {len(prior)} valid preceding sessions')
        if spot[ticker]['fieldData']['CRNCY'] != 'USD':
            raise ValueError('Currency mismatch')
        adv_shares = statistics.mean(r['PX_VOLUME'] for r in prior)
        adv_usd = statistics.mean(r['TURNOVER'] for r in prior)
        # Separately returned prices provide a non-circular check of TURNOVER units.
        implied_vwap = current['TURNOVER'] / current['PX_VOLUME']
        if not 0.5 < implied_vwap / current['PX_LAST'] < 1.5:
            raise ValueError(f'Turnover unit mismatch for {ticker}')
        previous = prior[-1]
        output['stocks'][ticker] = {
            'name': spot[ticker]['fieldData']['NAME'],
            'price': current['PX_LAST'], 'previous_price': previous['PX_LAST'],
            'close_return_pct': (current['PX_LAST'] / previous['PX_LAST'] - 1) * 100,
            'volume_shares': current['PX_VOLUME'], 'turnover_usd': current['TURNOVER'],
            'adv20_shares': adv_shares, 'adtv20_usd': adv_usd,
            'volume_vs_adv20_pct': current['PX_VOLUME'] / adv_shares * 100,
            'turnover_vs_adtv20_pct': current['TURNOVER'] / adv_usd * 100,
            'baseline_start': prior[0]['date'], 'baseline_end': prior[-1]['date'], 'baseline_sessions': len(prior),
            'implied_vwap': implied_vwap, 'turnover_units_check': 'PASS',
            'spot_bbg_average20_shares': spot[ticker]['fieldData']['VOLUME_AVG_20D']}
    for basket, members in weights.items():
        ranked = sorted(members, key=lambda r: r['Percentage Weight'], reverse=True)
        total_weight = sum(m['Percentage Weight'] for m in members)
        if abs(total_weight - 100) > 0.01:
            raise ValueError(f'Weights not 100: {basket} {total_weight}')
        results = []
        for rank, member in enumerate(ranked, 1):
            ticker = member['Member Ticker and Exchange Code'].split()[0] + ' US Equity'
            stock = output['stocks'][ticker]
            weight_pct = member['Percentage Weight']
            leg_usd = output['scenario_notional_usd'] * weight_pct / 100
            results.append({'rank_by_weight': rank, 'ticker': ticker, 'weight_pct': weight_pct,
                            'scenario_leg_usd': leg_usd, 'scenario_leg_shares_at_close': leg_usd / stock['price'],
                            'scenario_pct_adtv20': leg_usd / stock['adtv20_usd'] * 100,
                            'scenario_basket_usd_for_10pct_adtv': 0.10 * stock['adtv20_usd'] / (weight_pct / 100)})
        output['baskets'][basket] = {'weight_sum_pct': total_weight, 'top10_by_weight': results[:10],
                                     'PLNT': next(r for r in results if r['ticker'] == 'PLNT US Equity')}
    output['guardrails'] = {'weight_sums': 'PASS', 'baseline_sessions_20': 'PASS', 'US_composite_basis': 'PASS',
                             'turnover_implied_vwap_vs_separate_close': 'PASS', 'actual_basket_flow': 'UNAVAILABLE',
                             'causal_price_impact_calibration': 'UNAVAILABLE'}
    write('analysis.json', output)
    print(json.dumps({'PLNT': output['stocks']['PLNT US Equity'], 'baskets': output['baskets']}, indent=2))


if __name__ == '__main__':
    main()
