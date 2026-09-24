"""GPU rental benchmarks: local Bloomberg Desktop API and public SemiAnalysis.

py _wiki/_tools/gpu_pricing.py              # collect; retain last good data on failure
py _wiki/_tools/build_gpu_pricing.py        # render cached data, no network

No pip dependencies: stdlib plus the workstation's installed Bloomberg SDK.
Only the public SemiAnalysis endpoint is used; no institutional credentials.
"""
import datetime as dt
import json
import math
import socket
import ssl
import time
import urllib.request
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / '_data' / 'gpu-pricing'
PUBLIC_URL = 'https://gpu-index.semianalysis.com/api/public-data'
SA_URL = 'https://gpu-index.semianalysis.com/'
SD_URL = 'https://www.silicondata.com/products/silicon-index'
INSTRUMENTS = [
    ('SDH100RT Index', 'H100', 'Silicon Data', 'Standardized non-hyperscale rental'),
    ('SDA100RT Index', 'A100', 'Silicon Data', 'Standardized non-hyperscale rental'),
    ('SDB200RT Index', 'B200', 'Silicon Data', 'Standardized non-hyperscale rental'),
    ('SAH100SC Index', 'H100', 'SemiAnalysis', 'Spot-contract composite'),
]


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def read(path, fallback=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else fallback


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    tmp.replace(path)


def positive(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError('Invalid price: ' + repr(value))
    return value


def source_date(value):
    text = str(value)
    try:
        date = dt.date.fromisoformat(text[:10])
    except ValueError:
        date = parsedate_to_datetime(text).astimezone(dt.timezone.utc).date()
    if date > dt.datetime.now(dt.timezone.utc).date():
        raise ValueError('Future observation: ' + text)
    return date.isoformat()


def normalize_public(payload, fetched_at):
    if payload.get('status') != 'ok' or not payload.get('index'):
        raise ValueError('SemiAnalysis public index is empty or invalid')
    series = []
    for gpu in ('H100', 'A100', 'B200'):
        points = {}
        for row in payload['index']:
            value = row.get(gpu.lower())
            if value is not None:
                date = source_date(row['date'])
                if date in points and points[date] != value:
                    raise ValueError('Multiple different prices per day; public API schema needs review')
                points[date] = positive(value)
        if not points:
            raise ValueError('Missing public ' + gpu + ' index')
        series.append({'id': 'sa-public-' + gpu.lower(), 'gpu': gpu, 'publisher': 'SemiAnalysis',
                       'channel': 'Public API', 'basis': 'Spot-contract composite',
                       'unit': 'USD / GPU-hour', 'source_url': SA_URL, 'fetched_at': fetched_at,
                       'points': sorted([date, value] for date, value in points.items())})
    contracts = []
    for item in payload.get('contract', []):
        if item.get('sku') != 'H100':
            continue
        for row in item.get('data', []):
            record = {'period': row['period'], 'date': source_date(row['period_start']),
                      'one_year': None, 'on_demand': None,
                      'sold_out': row['period'] in item.get('soldOutPeriods', {}).get('onDemand', [])}
            for key, target in [('1y', 'one_year'), ('onDemand', 'on_demand')]:
                values = row.get(key)
                if values is not None:
                    if len(values) != 2 or positive(values[0]) > positive(values[1]):
                        raise ValueError('Invalid contract range: ' + repr(values))
                    record[target] = values
            contracts.append(record)
    if not contracts or not any(row['one_year'] for row in contracts):
        raise ValueError('SemiAnalysis public H100 contract ranges are missing')
    return {'fetched_at': fetched_at, 'source_url': PUBLIC_URL, 'series': series,
            'contracts': sorted(contracts, key=lambda row: row['date'])}


def fetch_public(folder):
    # Keep certificate and hostname checks; accommodate the workstation TLS proxy.
    context = ssl.create_default_context()
    context.verify_flags &= ~getattr(ssl, 'VERIFY_X509_STRICT', 0)
    req = urllib.request.Request(PUBLIC_URL, headers={'User-Agent': 'Capstone-GPU-pricing/1.0'})
    with urllib.request.urlopen(req, context=context, timeout=35) as response:
        payload = json.load(response)
    write(folder / 'semianalysis-public.json', payload)
    return normalize_public(payload, now())


def request_bbg(session, request, blpapi):
    session.sendRequest(request)
    deadline = time.monotonic() + 45
    results = []
    while time.monotonic() < deadline:
        event = session.nextEvent(1000)
        if event.eventType() in (blpapi.Event.RESPONSE, blpapi.Event.PARTIAL_RESPONSE):
            for message in event:
                results.append(message.toPy())
            if event.eventType() == blpapi.Event.RESPONSE:
                return results
        elif event.eventType() == blpapi.Event.REQUEST_STATUS:
            raise RuntimeError('Bloomberg request failed: ' + '; '.join(str(m) for m in event))
    raise TimeoutError('Bloomberg response timed out after 45 seconds')


def normalize_bbg(history, references, fetched_at):
    errors, series, ref = [], [], {}
    for message in references:
        if 'responseError' in message:
            errors.append(str(message['responseError']))
        for row in message.get('securityData', []):
            ref[row['security']] = row
    rows_by_ticker = {}
    for message in history:
        if 'responseError' in message:
            errors.append(str(message['responseError']))
        row = message.get('securityData', {})
        if row.get('security'):
            rows_by_ticker.setdefault(row['security'], []).append(row)
    for ticker, gpu, publisher, basis in INSTRUMENTS:
        rows, points = rows_by_ticker.get(ticker, []), {}
        try:
            for row in rows:
                if row.get('securityError') or row.get('fieldExceptions'):
                    raise ValueError(str(row.get('securityError') or row['fieldExceptions']))
                for obs in row.get('fieldData', []):
                    if obs.get('PX_LAST') is not None:
                        points[source_date(obs['date'])] = positive(obs['PX_LAST'])
            if not points:
                raise ValueError('No PX_LAST history returned')
            fields = ref.get(ticker, {}).get('fieldData', {})
            if fields.get('CRNCY') not in (None, 'USD'):
                raise ValueError('Unexpected currency: ' + str(fields['CRNCY']))
            item = {'id': ticker.split()[0], 'ticker': ticker, 'gpu': gpu, 'publisher': publisher,
                    'channel': 'Bloomberg Desktop API', 'basis': basis, 'unit': 'USD / GPU-hour',
                    'field': 'PX_LAST', 'name': fields.get('NAME', ticker),
                    'source_url': SD_URL if publisher == 'Silicon Data' else SA_URL,
                    'fetched_at': fetched_at, 'points': sorted([d, v] for d, v in points.items())}
            if fields.get('PX_LAST') is not None and fields.get('LAST_UPDATE_DT'):
                item['quote'] = [source_date(fields['LAST_UPDATE_DT']), positive(fields['PX_LAST'])]
            series.append(item)
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(ticker + ': ' + str(exc))
    return series, errors


def fetch_bbg(folder):
    with socket.create_connection(('127.0.0.1', 8194), timeout=2):
        pass
    import blpapi  # Existing licensed SDK, no installation or remote-server fallback.
    opts = blpapi.SessionOptions()
    opts.setServerHost('localhost'); opts.setServerPort(8194); opts.setConnectTimeout(4000)
    session = blpapi.Session(opts)
    try:
        if not session.start() or not session.openService('//blp/refdata'):
            raise ConnectionError('Bloomberg Desktop API is unavailable')
        service = session.getService('//blp/refdata')
        req = service.createRequest('HistoricalDataRequest')
        for ticker, *_ in INSTRUMENTS:
            req.append('securities', ticker)
        req.append('fields', 'PX_LAST')
        req.set('startDate', '20230101'); req.set('endDate', dt.date.today().strftime('%Y%m%d'))
        req.set('periodicitySelection', 'DAILY')
        history = request_bbg(session, req, blpapi)
        req = service.createRequest('ReferenceDataRequest')
        for ticker, *_ in INSTRUMENTS:
            req.append('securities', ticker)
        for field in ('NAME', 'PX_LAST', 'LAST_UPDATE_DT', 'CRNCY'):
            req.append('fields', field)
        references = request_bbg(session, req, blpapi)
        # Convert SDK date objects for reproducible raw JSON snapshots.
        history = json.loads(json.dumps(history, default=str))
        references = json.loads(json.dumps(references, default=str))
        write(folder / 'bbg-history.json', history)
        write(folder / 'bbg-reference.json', references)
        return normalize_bbg(history, references, now())
    finally:
        session.stop()


def merge_series(previous, fresh):
    merged = {row['id']: row for row in previous}
    for row in fresh:
        old = merged.get(row['id'])
        if old and old['points'][-1][0] > row['points'][-1][0]:
            raise ValueError('New snapshot regressed for ' + row['id'])
        if old:
            points = dict(old['points']); points.update(dict(row['points']))
            row = {**row, 'points': sorted([d, v] for d, v in points.items())}
        merged[row['id']] = row
    return list(merged.values())


def refresh():
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder = ROOT / 'raw' / stamp
    errors = []
    bbg = read(ROOT / 'bloomberg.json', {'series': []})
    try:
        fresh, issues = fetch_bbg(folder)
        errors.extend(issues)
        if fresh:
            write(ROOT / 'bloomberg.json', {'fetched_at': now(), 'series': merge_series(bbg['series'], fresh)})
    except Exception as exc:
        errors.append('Bloomberg: ' + str(exc))
    try:
        public = fetch_public(folder)
        old = read(ROOT / 'semianalysis.json', {'series': [], 'contracts': []})
        public['series'] = merge_series(old['series'], public['series'])
        if old['contracts'] and public['contracts'][-1]['date'] < old['contracts'][-1]['date']:
            raise ValueError('Public contract history regressed; previous snapshot retained')
        write(ROOT / 'semianalysis.json', public)
    except Exception as exc:
        errors.append('SemiAnalysis public: ' + str(exc))
    write(ROOT / 'status.json', {'attempted_at': now(), 'errors': errors,
                               'raw_snapshot': str(folder.relative_to(ROOT))})
    for name in ('bloomberg', 'semianalysis'):
        for row in read(ROOT / (name + '.json'), {'series': []})['series']:
            print(row['id'], len(row['points']), 'observations; latest', row['points'][-1])
    for error in errors:
        print('RETAINED LAST GOOD DATA:', error)
    return errors


if __name__ == '__main__':
    raise SystemExit(1 if refresh() else 0)
