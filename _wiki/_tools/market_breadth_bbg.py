"""Constituent breadth from the licensed local Bloomberg Desktop API."""
import argparse
import datetime as dt
import json
import hashlib
import math
import time
from pathlib import Path

import blpapi

DATA = Path(__file__).resolve().parents[1] / '_data' / 'market_breadth'
DATA.mkdir(parents=True, exist_ok=True)

def plain(el):
    if el.isArray():
        return [plain(el.getValueAsElement(i)) if el.isComplexType() else scalar(el.getValue(i)) for i in range(el.numValues())]
    if el.isComplexType():
        return {str(el.getElement(i).name()): plain(el.getElement(i)) for i in range(el.numElements())}
    return None if el.isNull() else scalar(el.getValue())

def scalar(v):
    if isinstance(v, blpapi.Element): return plain(v)
    return v.isoformat() if isinstance(v, (dt.date, dt.datetime, dt.time)) else str(v) if isinstance(v, blpapi.Name) else v

class Client:
    def __init__(self):
        op = blpapi.SessionOptions()
        op.setServerHost('localhost'); op.setServerPort(8194)
        op.setConnectTimeout(4000)
        self.session = blpapi.Session(op)
        if not self.session.start(): raise RuntimeError('Local Bloomberg unavailable')

    def request(self, service, kind, values=None, overrides=None):
        if not self.session.openService(service): raise RuntimeError(service)
        req = self.session.getService(service).createRequest(kind)
        for key, value in (values or {}).items():
            if isinstance(value, list):
                for v in value: req.append(key, v)
            else: req.set(key, value)
        for key, value in (overrides or {}).items():
            ov = req.getElement('overrides').appendElement()
            ov.setElement('fieldId', key); ov.setElement('value', str(value))
        self.session.sendRequest(req)
        result = []; start = time.monotonic()
        while time.monotonic() - start < 90:
            event = self.session.nextEvent(1000)
            for message in event:
                if event.eventType() in (blpapi.Event.RESPONSE, blpapi.Event.PARTIAL_RESPONSE):
                    item = plain(message.asElement())
                    if 'responseError' in item: raise RuntimeError(str(item['responseError']))
                    result.append(item)
                elif event.eventType() == blpapi.Event.REQUEST_STATUS:
                    raise RuntimeError(str(message))
            if event.eventType() == blpapi.Event.RESPONSE: return result
        raise TimeoutError(kind)

    def ref(self, securities, fields, overrides=None):
        return self.request('//blp/refdata', 'ReferenceDataRequest', {'securities':securities,'fields':fields}, overrides)

    def hist(self, securities, fields, start, end):
        return self.request('//blp/refdata', 'HistoricalDataRequest', {'securities':securities,'fields':fields,'startDate':start,'endDate':end,'periodicitySelection':'DAILY','adjustmentSplit':True,'adjustmentNormal':False,'adjustmentAbnormal':False,'adjustmentFollowDPDF':False,'nonTradingDayFillOption':'ACTIVE_DAYS_ONLY'})

    def close(self): self.session.stop()

def save(name, value):
    (DATA / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def probe(client):
    out = {}
    for term in ['all time high', 'historical high', 'maximum price']:
        try:
            out[term] = client.request('//blp/apiflds', 'FieldSearchRequest', {'searchSpec':term,'returnFieldDocumentation':True})
            print(term, json.dumps(out[term])[:18000], flush=True)
        except Exception as exc: print(term, str(exc), flush=True)
    save('field_search.json', out)
    membership = client.ref(['CCMP Index','SPX Index','RTY Index'], ['INDX_MEMBERS','INDX_MWEIGHT_HIST'])
    save('members_probe.json', membership)
    for message in membership:
        for sec in message.get('securityData',[]):
            print(sec['security'], {k:len(v) if isinstance(v,list) else v for k,v in sec.get('fieldData',{}).items()}, sec.get('fieldExceptions'), sec.get('securityError'), flush=True)
    hist = client.hist(['SPX Index','CCMP Index','RTY Index','AAPL US Equity'],['PX_LAST','PX_HIGH'],'20260901','20260929')
    save('history_probe.json',hist)
    print('history',json.dumps(hist)[-2200:],flush=True)

def probe2(client):
    fields = client.request('//blp/apiflds','FieldInfoRequest',{'id':['PX386','DS004','PX392','PX395','DY262','PX393','PX391','BE997','PY204','DS276','BE998','INDX_MWEIGHT_HIST'],'returnFieldDocumentation':True})
    save('field_info.json', fields)
    for m in fields:
        for item in m.get('fieldData',[]): print(json.dumps(item), flush=True)
    test = client.ref(['AAPL US Equity','NVDA US Equity','F US Equity','GE US Equity'],['INTERVAL_HIGH','ALL_TIME_HIGH_PERCENT','PX_LAST'],{'START_DATE_OVERRIDE':'19000101','END_DATE_OVERRIDE':'20260908','MARKET_DATA_OVERRIDE':'PX_HIGH'})
    save('high_probe.json',test)
    print(json.dumps(test),flush=True)

def probe3(client):
    securities=['AAPL US Equity','NVDA US Equity','F US Equity','GE US Equity']
    out=client.hist(securities,['PX_HIGH'],'19000101','20260908')
    save('full_high_validation.json',out)
    for m in out:
        sec=m.get('securityData',{}); points=[x for x in sec.get('fieldData',[]) if x.get('PX_HIGH')]
        print(sec.get('security'),len(points),max(points,key=lambda x:x['PX_HIGH']) if points else sec,flush=True)
    hist=client.hist(['AAPL US Equity'],['ALL_TIME_HIGH_PERCENT'],'20260901','20260929')
    save('ath_field_history_probe.json',hist); print(json.dumps(hist),flush=True)
    members=client.ref(['CCMP Index','SPX Index','RTY Index'],['INDX_MWEIGHT_HIST'],{'END_DATE_OVERRIDE':'20260929'})
    save('members_20260929.json',members)
    print('members',[{s['security']:{k:[len(v),v[:2]] for k,v in s['fieldData'].items()}} for m in members for s in m['securityData']],flush=True)

def ref_rows(messages):
    return {s['security']:s for m in messages for s in m.get('securityData',[])}

def fetch(client):
    asof=dt.date.today().strftime('%Y%m%d')
    indices=['CCMP Index','SPX Index','RTY Index']
    idx=client.hist(indices,['PX_LAST'],(dt.date.today()-dt.timedelta(days=45)).strftime('%Y%m%d'),asof)
    idxrows={m['securityData']['security']:m['securityData']['fieldData'] for m in idx}
    dates=sorted(set.intersection(*[{x['date'] for x in rows if x.get('PX_LAST')} for rows in idxrows.values()]))[-16:]
    if len(dates)!=16: raise RuntimeError('Need baseline plus 15 completed sessions')
    end=dates[-1].replace('-',''); baseline=dates[0].replace('-','')
    run=DATA/end; run.mkdir(exist_ok=True)
    def cached(name,callback):
        path=run/name
        if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
        value=callback(); path.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8'); return value
    members=cached('members.json',lambda:client.ref(indices,['INDX_MWEIGHT_HIST'],{'END_DATE_OVERRIDE':end}))
    def security(raw):
        symbol,exchange=raw.rsplit(' ',1)
        if not exchange.startswith('U'): raise ValueError('Unexpected non-US constituent: '+raw)
        return symbol+' US Equity'
    universes={k:sorted({security(x['Index Member']) for x in s['fieldData']['INDX_MWEIGHT_HIST']}) for k,s in ref_rows(members).items()}
    tickers=sorted(set().union(*map(set,universes.values())))
    print('WINDOW',dates,'UNIVERSES',{k:len(v) for k,v in universes.items()},'UNIQUE',len(tickers),flush=True)
    references={}; histories={}
    for i in range(0,len(tickers),150):
        batch=tickers[i:i+150]; tag=hashlib.sha256('|'.join(batch).encode()).hexdigest()[:10]
        ref=cached(f'ref_{i:04}_{tag}.json',lambda:client.ref(batch,['INTERVAL_HIGH','NAME','ALL_TIME_HIGH_PERCENT','PX_LAST'],{'START_DATE_OVERRIDE':'19000101','END_DATE_OVERRIDE':baseline,'MARKET_DATA_OVERRIDE':'PX_HIGH'}))
        references.update(ref_rows(ref))
        hist=cached(f'hist_{i:04}_{tag}.json',lambda:client.hist(batch,['PX_LAST','PX_HIGH'],baseline,end))
        histories.update({m['securityData']['security']:m['securityData'] for m in hist if 'securityData' in m})
        print(f'Fetched {min(i+150,len(tickers))}/{len(tickers)}',flush=True)
    payload={'source':'Bloomberg Desktop API','retrieved_at':dt.datetime.now(dt.timezone.utc).isoformat(),'dates':dates,'baseline':dates[0],'asof':dates[-1],'universes':universes,'index_history':idxrows,'references':references,'histories':histories}
    (run/'raw.json').write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
    print('SAVED',run/'raw.json',flush=True)

if __name__ == '__main__':
    client = Client()
    try:
        if '--fetch' in __import__('sys').argv: fetch(client)
        elif '--probe3' in __import__('sys').argv: probe3(client)
        elif '--probe2' in __import__('sys').argv: probe2(client)
        else: probe(client)
    finally: client.close()
