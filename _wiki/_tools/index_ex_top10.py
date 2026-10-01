"""Audit distance from ATH for indices and published ex-largest-company variants."""
import json
import datetime as dt
from pathlib import Path
from market_breadth_bbg import Client, ref_rows

DATA=Path(__file__).resolve().parents[1]/'_data'/'market_breadth'/'ex_top10_20260929'
DATA.mkdir(exist_ok=True)

def cache(name,call):
    file=DATA/name
    if file.exists(): return json.loads(file.read_text(encoding='utf-8'))
    value=call();file.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8');return value

def probe(client):
    for name,fields,overrides in [('start_weights',['INDX_MWEIGHT_HIST'],{'END_DATE_OVERRIDE':'20260908'}),('current_weights',['INDX_MWEIGHT','INDX_MWEIGHT_HIST'],{})]:
        out=cache(name+'.json',lambda:client.ref(['SPX Index','NDX Index','RTY Index'],fields,overrides))
        for sec,row in ref_rows(out).items():
            print(name,sec,{k:{'n':len(v),'sample':v[:3]} if isinstance(v,list) else v for k,v in row.get('fieldData',{}).items()},row.get('fieldExceptions'),flush=True)
    fields=cache('weight_fields.json',lambda:client.request('//blp/apiflds','FieldSearchRequest',{'searchSpec':'index member weight','returnFieldDocumentation':True}))
    print('field candidates',[(f['id'],f.get('fieldInfo',{}).get('mnemonic'),f.get('fieldInfo',{}).get('description')) for m in fields for f in m.get('fieldData',[])][:40],flush=True)

def probe_more(client):
    out=cache('alternate_weights.json',lambda:client.ref(['SPX Index','NDX Index','RTY Index'],['INDEX_MEMBERS_WEIGHTS','INDX_MWEIGHT_PX','INDX_MWEIGHT_PX2','INDX_MWEIGHT_PX3']))
    for sec,row in ref_rows(out).items():
        print(sec,{k:{'n':len(v),'sample':v[:2]} if isinstance(v,list) else v for k,v in row.get('fieldData',{}).items()},row.get('fieldExceptions'),flush=True)
    out=cache('etf_fields.json',lambda:client.request('//blp/apiflds','FieldSearchRequest',{'searchSpec':'fund holdings weight','returnFieldDocumentation':True}))
    print('ETF FIELDS',[(f['id'],f.get('fieldInfo',{}).get('mnemonic'),f.get('fieldInfo',{}).get('description')) for m in out for f in m.get('fieldData',[])][:30],flush=True)
    for query in ['S&P 500 ex','Nasdaq 100 ex','Russell 2000 equal']:
        try:
            out=cache('instruments_'+query.replace(' ','_').replace('/','_')+'.json',lambda:client.request('//blp/instruments','instrumentListRequest',{'query':query,'yellowKeyFilter':'YK_FILTER_INDX','languageOverride':'LANG_OVERRIDE_NONE','maxResults':25}))
            print(query,out,flush=True)
        except Exception as e:print(type(e).__name__,e.args,flush=True)

def raw_weight(client):
    import blpapi
    client.session.openService('//blp/refdata')
    req=client.session.getService('//blp/refdata').createRequest('ReferenceDataRequest')
    req.append('securities','NDX Index');req.append('fields','INDX_MWEIGHT')
    client.session.sendRequest(req)
    while True:
        ev=client.session.nextEvent(1000)
        for m in ev:
            if ev.eventType() in (blpapi.Event.RESPONSE,blpapi.Event.PARTIAL_RESPONSE):
                (DATA/'raw_weight_message.txt').write_text(str(m),encoding='utf-8')
                print(str(m)[:3000],flush=True)
        if ev.eventType()==blpapi.Event.RESPONSE:break

def ath_check(client):
    result=cache('benchmark_ath.json',lambda:client.ref(['SPX Index','QQQ US Equity','NDX Index','RTY Index'],['NAME','PX_LAST','INTERVAL_HIGH','ALL_TIME_HIGH_PERCENT'],{'START_DATE_OVERRIDE':'19000101','END_DATE_OVERRIDE':'20260929','MARKET_DATA_OVERRIDE':'PX_HIGH'}))
    print(json.dumps(result,indent=2),flush=True)
    for query in ['ex top 10','ex ten','Nasdaq ex top','Russell 2000 ex']:
        out=cache('search_'+query.replace(' ','_')+'.json',lambda:client.request('//blp/instruments','instrumentListRequest',{'query':query,'yellowKeyFilter':'YK_FILTER_INDX','languageOverride':'LANG_OVERRIDE_NONE','maxResults':25}))
        print(query,json.dumps(out),flush=True)

def published_ex(client):
    secs=['SPXX Index','NDX70P Index']
    out=cache('published_ex_reference.json',lambda:client.ref(secs,['NAME','LONG_COMP_NAME','INDX_SOURCE','INDX_MEMBERS','PX_LAST','INTERVAL_HIGH'],{'START_DATE_OVERRIDE':'19000101','END_DATE_OVERRIDE':'20260929','MARKET_DATA_OVERRIDE':'PX_HIGH'}))
    for s,row in ref_rows(out).items():
        print(s,{k:len(v) if isinstance(v,list) else v for k,v in row['fieldData'].items()},row.get('fieldExceptions'),flush=True)
    out=cache('published_ex_full_history.json',lambda:client.hist(secs,['PX_LAST','PX_HIGH'],'19000101','20260929'))
    for m in out:
        s=m.get('securityData',{});rows=s.get('fieldData',[])
        print(s.get('security'),'FIRST',rows[:1],'LAST',rows[-1:],'MAX CLOSE',max(rows,key=lambda x:x.get('PX_LAST',0)) if rows else None,'MAX HIGH',max(rows,key=lambda x:x.get('PX_HIGH',0)) if rows else None,flush=True)

def final_check(client):
    for query in ['Nasdaq ex','Russell 2000 excluding']:
        out=cache('final_search_'+query.replace(' ','_')+'.json',lambda:client.request('//blp/instruments','instrumentListRequest',{'query':query,'yellowKeyFilter':'YK_FILTER_INDX','languageOverride':'LANG_OVERRIDE_NONE','maxResults':100}))
        print(query,[r for m in out for r in m.get('results',[]) if any(w in r['description'].lower() for w in ['excl',' ex ','ex-'])],flush=True)
    out=cache('benchmarks_full_history.json',lambda:client.hist(['SPX Index','QQQ US Equity','RTY Index'],['PX_LAST','PX_HIGH'],'19000101','20260929'))
    refs=ref_rows(cache('benchmark_ath.json',lambda:None))
    refs.update(ref_rows(cache('published_ex_reference.json',lambda:None)))
    out+=cache('published_ex_full_history.json',lambda:None)
    summary=[]
    for m in out:
        s=m.get('securityData',{});rows=s.get('fieldData',[])
        if not rows: continue
        highs=[r for r in rows if isinstance(r.get('PX_HIGH'),(int,float)) and r['PX_HIGH']>0]
        maxhigh=max(highs,key=lambda r:r['PX_HIGH']);last=rows[-1]
        ref=refs[s['security']]['fieldData']
        assert abs(maxhigh['PX_HIGH']/ref['INTERVAL_HIGH']-1)<1e-5
        assert abs(last['PX_LAST']/ref['PX_LAST']-1)<1e-5
        summary.append({'ticker':s['security'],'source':'Bloomberg Desktop API','asof':last['date'],'first_available':rows[0]['date'],'close':last['PX_LAST'],'ath':maxhigh['PX_HIGH'],'ath_date':maxhigh['date'],'drawdown_pct':100*(last['PX_LAST']/maxhigh['PX_HIGH']-1),'reference_reconciliation':'PASS'})
    print(json.dumps(summary,indent=2),flush=True)
    (DATA/'verified_drawdowns.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')

if __name__=='__main__':
    c=Client()
    try:
        if '--final' in __import__('sys').argv:final_check(c)
        elif '--published' in __import__('sys').argv:published_ex(c)
        elif '--ath' in __import__('sys').argv:ath_check(c)
        elif '--raw' in __import__('sys').argv:raw_weight(c)
        elif '--more' in __import__('sys').argv:probe_more(c)
        else:probe(c)
    finally:c.close()
