"""Historical Bloomberg calendar-year +2 P/E, preserving source vintage."""
import datetime as dt
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, r'E:\bloomberg_api')
from bloomberg import bdh, bdp

COMPANIES = [
    ('RPD', 'Rapid7'), ('CHKP', 'Check Point'), ('TENB', 'Tenable'),
    ('4704 JP', 'Trend Micro'), ('QLYS', 'Qualys'), ('S', 'SentinelOne'),
    ('ZS', 'Zscaler'), ('SAIL', 'SailPoint'), ('VRNS', 'Varonis'),
    ('OKTA', 'Okta'), ('FTNT', 'Fortinet'), ('RBRK', 'Rubrik'),
    ('NET', 'Cloudflare'), ('PANW', 'Palo Alto Networks'), ('CRWD', 'CrowdStrike'),
]


def security(ticker):
    return ticker + ' Equity' if ticker == '4704 JP' else ticker + ' US Equity'


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, default=str), encoding='utf-8')


def main():
    securities = [security(t) for t, _ in COMPANIES] + ['2542797D US Equity']
    identities = bdp(securities, ['NAME', 'ID_BB_GLOBAL', 'ID_CUSIP', 'EQY_INIT_PO_DT', 'EQY_FISCAL_YR_END', 'CRNCY', 'EQY_FUND_CRNCY']).to_dict('records')
    save('identities.json', identities)
    print('Identities saved', flush=True)
    data = {'retrieved_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'companies': COMPANIES, 'history': {}}
    for year in range(2018, 2027):
        end = dt.date(year, 12, 31) if year < 2026 else dt.date(2026, 9, 21)
        start = end - dt.timedelta(days=14)
        override = str(year + 2) + 'BC'
        records = bdh(securities, ['PX_LAST', 'BEST_PE_RATIO', 'BEST_EPS'], start.strftime('%Y%m%d'), end.strftime('%Y%m%d'), BEST_FPERIOD_OVERRIDE=override, adjustmentSplit=True, adjustmentNormal=False, adjustmentAbnormal=False).to_dict('records')
        data['history'][str(year)] = {'cutoff': end.isoformat(), 'target_calendar_year': year + 2, 'override': override, 'records': records}
        save('history.json', data)
        print(year, '-> CY', year + 2, 'records', len(records), flush=True)
    print('Complete', flush=True)


if __name__ == '__main__':
    main()
