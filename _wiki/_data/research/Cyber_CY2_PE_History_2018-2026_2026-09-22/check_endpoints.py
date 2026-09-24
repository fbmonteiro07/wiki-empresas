import datetime as dt
import json
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, r'E:\bloomberg_api')
from bloomberg import bdh
data = json.loads((HERE / 'history.json').read_text())
out = {}
for year, history in data['history'].items():
    groups = {}
    for ticker, name in data['companies']:
        if ticker == 'SAIL' and year in ['2022', '2023', '2024']:
            continue
        sec = '2542797D US Equity' if ticker == 'SAIL' and int(year) <= 2021 else ticker + ' Equity' if ticker == '4704 JP' else ticker + ' US Equity'
        prices = [r for r in history['records'] if r['ticker'] == sec and r['field'] == 'PX_LAST']
        if prices:
            date = max(r['date'] for r in prices)
            groups.setdefault(date, []).append(sec)
    out[year] = []
    for date, securities in groups.items():
        records = bdh(securities, ['PX_LAST', 'BEST_EPS', 'BEST_PE_RATIO'], date.replace('-', ''), date.replace('-', ''), BEST_FPERIOD_OVERRIDE=history['override'], nonTradingDayFillOption='ALL_CALENDAR_DAYS', nonTradingDayFillMethod='PREVIOUS_VALUE', adjustmentSplit=True, adjustmentNormal=False, adjustmentAbnormal=False).to_dict('records')
        out[year].extend(records)
    (HERE / 'all_endpoint_checks.json').write_text(json.dumps(out, indent=2, default=str))
    print(year, 'checked', len(out[year]), 'source values', flush=True)
