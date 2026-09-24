"""Capture raw, read-only Bloomberg basket data and field documentation."""
import datetime as dt
import json
from pathlib import Path
import sys
import time

import blpapi

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / '_tools'))
from probe_revenue_ebit_history import simplify

SECURITIES = ['GSXUSWCH Index', 'GSCBSWC2 Index']
FIELDS = ['NAME', 'SECURITY_TYP', 'SECURITY_DES', 'CRNCY', 'PX_LAST',
          'LAST_UPDATE_DT', 'PX_VOLUME', 'VOLUME', 'TURNOVER',
          'VOLUME_AVG_20D', 'VOLUME_AVG_30D', 'INDX_VOLUME', 'INDX_MWEIGHT']


def collect(session, request, timeout=60):
    session.sendRequest(request)
    messages = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        event = session.nextEvent(1000)
        for message in event:
            messages.append({'type': str(message.messageType()), 'data': simplify(message.asElement())})
        if event.eventType() == blpapi.Event.RESPONSE:
            return messages
        if event.eventType() == blpapi.Event.REQUEST_STATUS:
            raise RuntimeError(json.dumps(messages, default=str))
    raise TimeoutError('Bloomberg request timed out')


def save(name, request, messages):
    data = {'source': 'Bloomberg Desktop API, localhost:8194',
            'retrieved_at': dt.datetime.now().astimezone().isoformat(),
            'request': str(request), 'messages': messages}
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return data


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'reference'
    options = blpapi.SessionOptions()
    options.setServerHost('localhost')
    options.setServerPort(8194)
    options.setConnectTimeout(5000)
    session = blpapi.Session(options)
    if not session.start():
        raise RuntimeError('Bloomberg Desktop API unavailable')
    try:
        service_name = '//blp/apiflds' if mode in ('metadata', 'search') else '//blp/refdata'
        if not session.openService(service_name):
            raise RuntimeError('Cannot open ' + service_name)
        service = session.getService(service_name)
        if mode == 'metadata':
            request = service.createRequest('FieldInfoRequest')
            for field in FIELDS:
                request.append('id', field)
            request.set('returnFieldDocumentation', True)
        elif mode == 'search':
            request = service.createRequest('FieldSearchRequest')
            request.set('searchSpec', sys.argv[2])
            request.set('returnFieldDocumentation', True)
        elif mode in ('constituents', 'constituents_primary'):
            source = json.loads((HERE / 'reference.json').read_text(encoding='utf-8'))
            tickers = set()
            for message in source['messages']:
                for security in message['data'].get('securityData', []):
                    for member in security.get('fieldData', {}).get('INDX_MWEIGHT', []):
                        ticker = member['Member Ticker and Exchange Code']
                        tickers.add(ticker + ' Equity' if mode == 'constituents_primary' else ticker.split()[0] + ' US Equity')
            request = service.createRequest('ReferenceDataRequest')
            for ticker in sorted(tickers):
                request.append('securities', ticker)
            for field in ['NAME', 'PX_VOLUME', 'TURNOVER', 'LAST_UPDATE_DT']:
                request.append('fields', field)
        elif mode == 'history':
            request = service.createRequest('HistoricalDataRequest')
            for security in SECURITIES:
                request.append('securities', security)
            for field in ['PX_LAST', 'PX_VOLUME', 'VOLUME', 'TURNOVER']:
                request.append('fields', field)
            request.set('startDate', '20250923')
            request.set('endDate', '20260923')
            request.set('periodicitySelection', 'DAILY')
        else:
            request = service.createRequest('ReferenceDataRequest')
            for security in SECURITIES:
                request.append('securities', security)
            for field in FIELDS:
                request.append('fields', field)
        suffix = '_' + sys.argv[2].replace(' ', '_') if mode == 'search' else ''
        data = save(mode + suffix + '.json', request, collect(session, request))
        if mode in ('history', 'constituents', 'constituents_primary'):
            for message in data['messages']:
                securities = message['data'].get('securityData', [])
                if isinstance(securities, dict):
                    rows = securities.get('fieldData', [])
                    volume_rows = [row for row in rows if row.get('PX_VOLUME') is not None]
                    print(securities['security'], 'rows', len(rows), 'with volume', len(volume_rows), 'first', volume_rows[:1], 'last', volume_rows[-1:])
                elif securities:
                    print('Constituent records saved:', len(securities))
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    finally:
        session.stop()


if __name__ == '__main__':
    main()
