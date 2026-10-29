"""Fetch licensed Bloomberg inputs for the sentiment research dashboard.

Uses the repository's existing Bloomberg bridge. Never changes source wiki pages
or existing sentiment caches. --offline is the build script's default behavior.
"""
import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / '_data' / 'sentiment_research'


def write(name, obj):
    OUT.mkdir(exist_ok=True)
    path = OUT / name
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, separators=(',', ':'), allow_nan=False), encoding='utf-8')
    tmp.replace(path)


def fetch(asof):
    from market_breadth_bbg import Client
    companies = json.loads((BASE / '_data/estimates.json').read_text(encoding='utf-8'))['companies']
    technicals = json.loads((BASE / '_data/technicals/prices.json').read_text(encoding='utf-8'))['names']
    names = {t: v['bbg'] for t, v in companies.items() if t in technicals and v.get('bbg')}
    inv = {v: t for t, v in names.items()}
    inv.update({'QQQ US Equity': '_QQQ', 'SPY US Equity': '_SPY'})
    client = Client()
    manifest = {'asof': asof, 'fetched_at': dt.datetime.now(dt.timezone.utc).isoformat(),
                'source': 'Bloomberg Desktop API; locally entitled', 'requests': [], 'exceptions': []}
    try:
        docs = client.request('//blp/apiflds', 'FieldInfoRequest',
                              {'id': ['BEST_FPERIOD_OVERRIDE', 'BEST_EPS', 'BEST_SALES', 'TOT_RETURN_INDEX_GROSS_DVDS'],
                               'returnFieldDocumentation': True})
        write('field_documentation.json', docs)
        for year in [2024, 2025, 2026]:
            target = year + 1
            fields = ['BEST_EPS', 'BEST_SALES']
            series = {}
            securities = list(names.values())
            start = f'{year-1}1101'
            end = min(f'{year}1231', asof.replace('-', ''))
            override = f'{target}Y'
            for i in range(0, len(securities), 20):
                messages = client.request('//blp/refdata', 'HistoricalDataRequest',
                    {'securities': securities[i:i+20], 'fields': fields, 'startDate': start,
                     'endDate': end, 'periodicitySelection': 'DAILY', 'nonTradingDayFillOption': 'ACTIVE_DAYS_ONLY'},
                    {'BEST_FPERIOD_OVERRIDE': override})
                for message in messages:
                    s = message.get('securityData', {})
                    t = inv.get(s.get('security'))
                    if not t:
                        continue
                    series[t] = {field: {} for field in fields}
                    for row in s.get('fieldData', []):
                        for field in fields:
                            if isinstance(row.get(field), (float, int)):
                                series[t][field][row['date']] = row[field]
                    if s.get('fieldExceptions') or s.get('securityError'):
                        manifest['exceptions'].append({'ticker': t, 'override': override,
                            'field': s.get('fieldExceptions'), 'security': s.get('securityError')})
                print(f'Fixed FY {target}: {min(i+20,len(securities))}/{len(securities)}', flush=True)
            write(f'estimates_{year}.json', {'asof': asof, 'signal_year': year, 'target_fiscal_year': target,
                  'override': override, 'source': 'Bloomberg BEST_EPS / BEST_SALES historical, fixed fiscal year',
                  'point_in_time_caveat': 'Historical vendor series retrieved today; original publication vintages and subsequent vendor corrections are not independently certified.',
                  'series': series})
            manifest['requests'].append({'type': 'fixed_fiscal_estimates', 'start': start, 'end': end, 'override': override})
        securities = list(inv)
        series = {}
        fields = ['TOT_RETURN_INDEX_GROSS_DVDS', 'PX_LAST']
        for i in range(0, len(securities), 20):
            messages = client.hist(securities[i:i+20], fields, '20231001', asof.replace('-', ''))
            for message in messages:
                s = message.get('securityData', {})
                t = inv.get(s.get('security'))
                if not t:
                    continue
                series[t] = {f: {} for f in fields}
                for row in s.get('fieldData', []):
                    for field in fields:
                        if isinstance(row.get(field), (float, int)):
                            series[t][field][row['date']] = row[field]
                if s.get('fieldExceptions') or s.get('securityError'):
                    manifest['exceptions'].append({'ticker': t, 'field': s.get('fieldExceptions'), 'security': s.get('securityError')})
            print(f'Total return: {min(i+20,len(securities))}/{len(securities)}', flush=True)
        write('returns.json', {'asof': asof, 'source': 'Bloomberg TOT_RETURN_INDEX_GROSS_DVDS / PX_LAST', 'series': series})
        instruments = {}
        securities = list(names.values())
        for i in range(0,len(securities),30):
            for message in client.ref(securities[i:i+30], ['CRNCY','EQY_FUND_CRNCY']):
                for s in message.get('securityData',[]):
                    instruments[s['security']] = s.get('fieldData',{})
        write('instruments.json', {'asof': manifest['fetched_at'][:10],
              'source':'Bloomberg reference CRNCY / EQY_FUND_CRNCY','securities':instruments})
        # Independent current reference snapshots are retained as a semantic / end-point check.
        anchors = client.ref(['AAPL US Equity', 'MSFT US Equity', 'NVDA US Equity'], ['BEST_EPS','BEST_SALES'], {'BEST_FPERIOD_OVERRIDE':'2027Y'})
        write('reference_anchors.json', {'asof': manifest['fetched_at'][:10], 'history_asof':asof,
              'fetched_at': manifest['fetched_at'], 'override':'2027Y', 'messages': anchors})
        manifest['sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.json') if p.name not in ('manifest.json','dashboard.json','protocol.json')}
        write('manifest.json', manifest)
    finally:
        client.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--asof', required=True, help='Last completed market session, YYYY-MM-DD')
    a = ap.parse_args()
    fetch(a.asof)
