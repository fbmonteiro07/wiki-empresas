"""Compute and audit the Bloomberg constituent drawdown panel; stdlib only."""
import csv
import datetime as dt
import json
import math
from pathlib import Path
from market_breadth_bbg import Client, DATA

LABELS={'CCMP Index':'Nasdaq Composite','SPX Index':'S&P 500 (SPY)','RTY Index':'Russell 2000'}
THRESHOLDS=[10,20,30,50]

def positive(x): return isinstance(x,(int,float)) and math.isfinite(x) and x>0

def build():
    run=sorted(p.parent for p in DATA.glob('*/raw.json'))[-1]
    raw=json.loads((run/'raw.json').read_text(encoding='utf-8'))
    dates=raw['dates']; baseline=dates[0]; histories=raw['histories']; refs=raw['references']
    missing=[t for t,h in histories.items() if not any(x['date']==baseline and positive(x.get('PX_LAST')) for x in h.get('fieldData',[]))]
    recovery_path=run/'baseline_backfill.json'
    if recovery_path.exists(): recovery=json.loads(recovery_path.read_text(encoding='utf-8'))
    else:
        recovery=[]; client=Client()
        try:
            for i in range(0,len(missing),150):
                recovery.extend(client.hist(missing[i:i+150],['PX_LAST','PX_HIGH'],(dt.date.fromisoformat(baseline)-dt.timedelta(days=60)).strftime('%Y%m%d'),baseline.replace('-','')))
        finally: client.close()
        recovery_path.write_text(json.dumps(recovery),encoding='utf-8')
    backfills={m['securityData']['security']:m['securityData'].get('fieldData',[]) for m in recovery if 'securityData' in m}
    excluded={}; stocks={}; audit_compare=[]; audit_mismatches=[]
    for ticker,h in histories.items():
        ref=refs.get(ticker,{}).get('fieldData',{}); peak=ref.get('INTERVAL_HIGH')
        if not positive(peak): excluded[ticker]='No pre-window historical high (new listing or unavailable)'; continue
        rows={x['date']:x for x in backfills.get(ticker,[])}
        rows.update({x['date']:x for x in h.get('fieldData',[])})
        prior=[x for d,x in sorted(rows.items()) if d<=baseline and positive(x.get('PX_LAST'))]
        if not prior: excluded[ticker]='No valid closing price on/before baseline'; continue
        last=prior[-1]['PX_LAST']; last_date=prior[-1]['date']
        series=[]; invalid=False
        for d in dates:
            row=rows.get(d,{})
            if positive(row.get('PX_HIGH')): peak=max(peak,row['PX_HIGH'])
            if positive(row.get('PX_LAST')): last=row['PX_LAST']; last_date=d
            if last>peak*(1+1e-5): invalid=True
            series.append({'date':d,'close':last,'ath':peak,'drawdown_pct':100*(1-last/peak),'price_date':last_date,'carried':last_date!=d})
        if invalid: excluded[ticker]='Close exceeds reconstructed historical high; basis requires review'; continue
        stocks[ticker]={'name':ref.get('NAME',ticker),'series':series}
        final=series[-1]
        # Independent Bloomberg snapshot field uses 1960-present highs; compare
        # only where reference price equals this panel's closing-price endpoint.
        if positive(ref.get('PX_LAST')) and abs(ref['PX_LAST']-final['close'])<1e-6 and isinstance(ref.get('ALL_TIME_HIGH_PERCENT'),(int,float)):
            gap=abs(final['drawdown_pct']+ref['ALL_TIME_HIGH_PERCENT'])
            check={'ticker':ticker,'gap_pp':gap,'computed':final['drawdown_pct'],'bbg':-ref['ALL_TIME_HIGH_PERCENT']}
            audit_compare.append(check)
            if gap>0.02: audit_mismatches.append(check)
    summary={'source':raw['source'],'retrieved_at':raw['retrieved_at'],'asof':raw['asof'],'baseline':baseline,'dates':dates,'thresholds':THRESHOLDS,'basis':'Closing price / running intraday historical high; split-adjusted, cash dividends unadjusted','membership':'September 29, 2026 constituent snapshot held fixed over the period; share classes counted separately','missing_observations':'Last valid close carried forward. No baseline high/close -> excluded from every date.','indices':[]}
    constituents=[]
    for index,universe in raw['universes'].items():
        eligible=[t for t in universe if t in stocks]; n=len(eligible)
        points=[]
        for i,d in enumerate(dates):
            counts=[sum(stocks[t]['series'][i]['drawdown_pct']>=threshold-1e-9 for t in eligible) for threshold in THRESHOLDS]
            assert counts==sorted(counts,reverse=True) and 0<=counts[-1]<=counts[0]<=n
            points.append({'date':d,'counts':counts,'pct':[round(100*c/n,6) for c in counts],'carried':sum(stocks[t]['series'][i]['carried'] for t in eligible)})
        ip={x['date']:x['PX_LAST'] for x in raw['index_history'][index] if positive(x.get('PX_LAST'))}
        item={'ticker':index,'label':LABELS[index],'universe':len(universe),'covered':n,'coverage_pct':100*n/len(universe),'excluded':[{'ticker':t,'reason':excluded.get(t,'No response')} for t in universe if t not in stocks],'points':points,'delta_counts':[points[-1]['counts'][i]-points[0]['counts'][i] for i in range(4)],'delta_pp':[points[-1]['pct'][i]-points[0]['pct'][i] for i in range(4)],'index_return_pct':100*(ip[dates[-1]]/ip[dates[0]]-1)}
        summary['indices'].append(item)
        for ticker in universe:
            if ticker not in stocks: continue
            for row in stocks[ticker]['series']:
                constituents.append({'index':index,'ticker':ticker,'name':stocks[ticker]['name'],**row,'source':'Bloomberg Desktop API','retrieved_at':raw['retrieved_at']})
    audit={'reference_validation_compared':len(audit_compare),'reference_mismatch_tolerance_pp':0.02,'reference_mismatches':audit_mismatches,'unique_eligible':len(stocks),'unique_excluded':excluded,'nesting':'PASS','denominator_constant':'PASS','future_highs':'Baseline through Sep 8, then cumulative max of observed highs through each date','source_field_errors':{t:r.get('fieldExceptions') for t,r in refs.items() if r.get('securityError')},'latest_carried':[{'index':x['label'],'count':x['points'][-1]['carried']} for x in summary['indices']]}
    (run/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (run/'validation.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    with (run/'constituent_drawdowns.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(constituents[0])); writer.writeheader(); writer.writerows(constituents)
    with (run/'breadth_daily.csv').open('w',newline='',encoding='utf-8-sig') as f:
        fields=['index','date','threshold_pct','count','covered','universe','percentage','carried_prices','source']
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for index in summary['indices']:
            for p in index['points']:
                for i,t in enumerate(THRESHOLDS): writer.writerow(dict(index=index['label'],date=p['date'],threshold_pct=t,count=p['counts'][i],covered=index['covered'],universe=index['universe'],percentage=p['pct'][i],carried_prices=p['carried'],source=raw['source']))
    print(json.dumps({'indices':[{k:v for k,v in x.items() if k!='points'} for x in summary['indices']],'latest':[{x['label']:x['points'][-1]} for x in summary['indices']],'audit':audit},indent=2))

if __name__=='__main__': build()
