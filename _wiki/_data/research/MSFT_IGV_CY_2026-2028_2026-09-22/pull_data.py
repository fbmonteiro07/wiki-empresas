"""Read-only Bloomberg Desktop API and iShares source capture for requested valuation."""
import csv
import datetime as dt
import io
import json
from pathlib import Path
import sys
import urllib.request

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / '_tools'))
from probe_revenue_ebit_history import Client, simplify
import blpapi


def save(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def metadata(c, names):
    if not c.session.openService('//blp/apiflds'):
        raise RuntimeError('Field metadata service unavailable')
    req = c.session.getService('//blp/apiflds').createRequest('FieldInfoRequest')
    for name in names:
        req.append('id', name)
    req.set('returnFieldDocumentation', True)
    c.session.sendRequest(req)
    out = []
    while True:
        ev = c.session.nextEvent(10000)
        for msg in ev:
            out.append(simplify(msg.asElement()))
        if ev.eventType() == blpapi.Event.RESPONSE:
            return out


def main():
    mode = sys.argv[1]
    if mode == 'holdings':
        url = 'https://www.ishares.com/us/products/239771/ishares-expanded-tech-software-sector-etf/latest-holdings.csv'
        raw = urllib.request.urlopen(url, timeout=40).read().decode('utf-8-sig')
        (HERE / 'ishares_holdings_2026-09-21.csv').write_text(raw, encoding='utf-8')
        lines = raw.splitlines()
        start = next(i for i, line in enumerate(lines) if line.startswith('Ticker,'))
        rows = list(csv.DictReader(io.StringIO('\n'.join(lines[start:]))))
        rows = [r for r in rows if r.get('Asset Class') == 'Equity']
        save('holdings.json', {'source': url, 'header': lines[:start], 'retrieved_at': dt.datetime.now().isoformat(), 'equities': rows})
        print('equity holdings', len(rows), 'weight', sum(float(r['Weight (%)']) for r in rows))
        return
    c = Client()
    try:
        if mode == 'metadata':
            names = ['BEST_FPERIOD_OVERRIDE', 'BEST_ESTIMATE_FCF', 'BEST_EPS', 'BEST_PE_RATIO', 'CUR_MKT_CAP', 'BEST_ESTIMATE_FCF_NUMEST', 'FUND_HOLDINGS', 'INDX_MEMBERS_WEIGHTS']
            data = metadata(c, names)
            save('field_metadata.json', data)
            print(json.dumps(data, indent=2))
        elif mode == 'msft_periods':
            fields = ['BEST_EPS', 'BEST_EPS_GAAP', 'BEST_ESTIMATE_FCF', 'BEST_CAPEX', 'BEST_NET_INCOME', 'BEST_ESTIMATE_FCF_NUMEST', 'BEST_PERIOD_END_DATE']
            periods = ['2026FY', '2027FY', '2028FY', '2029FY', '2026Q3', '2026Q4'] + [f'{k}FQ' for k in range(1, 11)]
            data = {p: c.ref(['MSFT US Equity'], fields, {'BEST_FPERIOD_OVERRIDE': p}) for p in periods}
            save('msft_periods.json', data)
            print(json.dumps(data, indent=2))
        elif mode == 'constituents':
            holds = json.loads((HERE / 'holdings.json').read_text(encoding='utf-8'))
            securities = [r['Ticker'] + ' US Equity' for r in holds['equities']]
            data = {'retrieved_at': dt.datetime.now().isoformat(), 'spot': c.ref(securities, ['NAME', 'PX_LAST', 'PX_YEST_CLOSE', 'CUR_MKT_CAP', 'EQY_SH_OUT', 'CRNCY', 'EQY_FUND_CRNCY', 'EQY_FISCAL_YR_END', 'LAST_UPDATE_DT'])}
            fields = ['BEST_EPS', 'BEST_EPS_GAAP', 'BEST_PE_RATIO', 'BEST_ESTIMATE_FCF', 'BEST_CAPEX', 'BEST_NET_INCOME', 'BEST_ESTIMATE_FCF_NUMEST']
            for y in [2026, 2027, 2028]:
                data[str(y)] = c.ref(securities, fields, {'BEST_FPERIOD_OVERRIDE': f'{y}BC', 'EQY_FUND_CRNCY': 'USD'})
                print('received', y, len(data[str(y)]), flush=True)
                save('constituents.json', data)
        elif mode == 'etf_holdings':
            data = c.ref(['IGV US Equity', 'SPNASEUT Index'], ['FUND_HOLDINGS', 'INDX_MEMBERS_WEIGHTS', 'FUND_TOTAL_ASSETS', 'FUND_NET_ASSET_VAL', 'FUND_SHARES_OUTSTANDING'])
            save('bbg_holdings.json', data)
            print(json.dumps(data, indent=2)[:3000])
    finally:
        c.close()


if __name__ == '__main__':
    main()
