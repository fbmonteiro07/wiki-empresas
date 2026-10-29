"""Reproducible sentiment decision lab. Python standard library; offline build.

Inputs are read-only. Outputs only _data/sentiment_research, _dashboards and _meta.
No fitted weights, retrospective selection, or automatic trading recommendations.
"""
from __future__ import annotations

import argparse
import bisect
import datetime as dt
import hashlib
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
import sentiment_relative_backtest as relative_lab
import sentiment_indicator_ranking as ranking_lab
import sentiment_pair_backtest as pair_lab

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / '_data'
OUT = DATA / 'sentiment_research'
VERSION = '2.5'
COSTS = [0, 10, 25, 50]
TECH = ['rsi14', 'momentum21', 'momentum63', 'distance50']
EARN = ['eps28', 'sales28']
SOCIAL = ['tone7', 'tone_change']
CORE = TECH + EARN + SOCIAL + ['attention']
LABELS = {'momentum': 'Momentum only', 'rsi': 'RSI only', 'technical': 'Technicals',
          'earnings': 'Fixed-FY revisions', 'social': 'X sentiment', 'attention': 'Attention only',
          'te': 'Technicals + revisions', 'tes': 'Technicals + revisions + X',
          'tess': '+ sell-side tone', 'tesx': '+ curated X', 'equal': 'Matched equal weight', 'qqq': 'QQQ'}
MODEL_KEYS = ['momentum','rsi','technical','earnings','social','attention','te','tes']


def mean(xs):
    return statistics.fmean(xs) if xs else None


def ranks(values):
    """Midranks on [0,1]; ties do not depend on ticker ordering."""
    a = sorted(values.items(), key=lambda x: x[1])
    out = {}
    i = 0
    while i < len(a):
        j = i + 1
        while j < len(a) and a[j][1] == a[i][1]:
            j += 1
        r = ((i + j - 1) / 2) / (len(a) - 1) if len(a) > 1 else .5
        for k, _ in a[i:j]:
            out[k] = r
        i = j
    return out


def corr(x, y):
    if len(x) < 3:
        return None
    mx, my = mean(x), mean(y)
    den = math.sqrt(sum((a-mx)**2 for a in x) * sum((b-my)**2 for b in y))
    return sum((a-mx)*(b-my) for a,b in zip(x,y)) / den if den else None


def spearman(scores, returns):
    keys = sorted(set(scores) & set(returns))
    a, b = ranks({k:scores[k] for k in keys}), ranks({k:returns[k] for k in keys})
    return corr([a[k] for k in keys], [b[k] for k in keys])


def rsi(prices, n=14):
    result = [None] * len(prices)
    if len(prices) <= n:
        return result
    up = mean([max(prices[i]-prices[i-1],0) for i in range(1,n+1)])
    down = mean([max(prices[i-1]-prices[i],0) for i in range(1,n+1)])
    for i in range(n, len(prices)):
        if i > n:
            change = prices[i]-prices[i-1]
            up = ((n-1)*up+max(change,0))/n
            down = ((n-1)*down+max(-change,0))/n
        result[i] = 50. if up == down == 0 else 100. if down == 0 else 100-100/(1+up/down)
    return result


def symmetric_change(now, old):
    if now is None or old is None:
        return None
    den = abs(now) + abs(old)
    return 2*(now-old)/den if den else 0.


def shifted(date, days):
    return (dt.date.fromisoformat(date)+dt.timedelta(days=days)).isoformat()


class Series:
    def __init__(self, data):
        self.data = {d:float(v) for d,v in data.items() if isinstance(v,(int,float)) and math.isfinite(v)}
        self.dates = sorted(self.data)

    def at(self, date, max_age=10):
        i = bisect.bisect_right(self.dates,date)-1
        if i < 0 or (dt.date.fromisoformat(date)-dt.date.fromisoformat(self.dates[i])).days > max_age:
            return None
        return self.data[self.dates[i]]

    def window(self, date, days):
        lo = bisect.bisect_right(self.dates,shifted(date,-days))
        hi = bisect.bisect_right(self.dates,date)
        return [(d,self.data[d]) for d in self.dates[lo:hi]]


class Inputs:
    def __init__(self, max_est_age=35):
        self.sources = {}
        self.max_est_age = max_est_age
        self.companies = self.load('estimates.json')['companies']
        self.prices = self.load('technicals/prices.json')
        self.bbg = self.load('sentiment/bbg_long.json')
        self.own = self.load('sentiment/tweet_daily.json')
        self.ss = self.load('sentiment/sellside_daily.json')
        self.desk = self.load('sentiment/desk_ledger.json')
        self.est = {y:self.load(f'sentiment_research/estimates_{y}.json') for y in [2024,2025,2026]}
        self.ret = self.load('sentiment_research/returns.json')
        self.instruments = self.load('sentiment_research/instruments.json')['securities']
        self.protocol = self.load('sentiment_research/protocol.json')
        meta = self.load('index_meta.json')
        self.peer_graph = self.load('graph.json')
        self.groups = {}
        for section in meta['sections']:
            for entry in section['entries']:
                self.groups.setdefault(entry['ticker'], section['title'].replace('\ufffd','/'))
        self.names = sorted(t for t in self.companies if t in self.ret['series'] and t in self.prices['names'])
        self.usd = [t for t in self.names if self.companies[t]['bbg'].endswith(' US Equity') and
                    self.instruments.get(self.companies[t]['bbg'],{}).get('CRNCY') == 'USD']
        self.px, self.tri, self.indicators = {}, {}, {}
        for t,s in self.ret['series'].items():
            self.px[t] = Series(s.get('PX_LAST',{}))
            self.tri[t] = Series(s.get('TOT_RETURN_INDEX_GROSS_DVDS',{}))
            dates = self.px[t].dates
            close = [self.px[t].data[d] for d in dates]
            rr = rsi(close)
            self.indicators[t] = {}
            for i,d in enumerate(dates):
                if i < 63 or close[i] <= 0:
                    continue
                self.indicators[t][d] = {'rsi14':rr[i], 'momentum21':close[i]/close[i-21]-1,
                    'momentum63':close[i]/close[i-63]-1, 'distance50':close[i]/mean(close[i-49:i+1])-1,
                    'distance200':close[i]/mean(close[i-199:i+1])-1 if i>=199 else None,
                    'px':close[i]}
        self.calendar = self.tri['_QQQ'].dates
        self.common_end = min(self.bbg['asof'],self.ret['asof'],self.prices['asof'])
        self.vendor = {t:{f:Series(s) for f,s in v.items()} for t,v in self.bbg['series'].items()}
        self.estimates = {y:{t:{f:Series(s) for f,s in v.items()} for t,v in obj['series'].items()} for y,obj in self.est.items()}
        self.cache = {}

    def load(self, relative):
        path = DATA / relative
        raw = path.read_bytes()
        obj = json.loads(raw)
        self.sources[relative] = {'path':'../_data/'+relative, 'sha256':hashlib.sha256(raw).hexdigest(),
            'asof': obj.get('asof') or obj.get('meta',{}).get('built'), 'tag':'HARD' if relative.startswith(('technicals','sentiment_research/returns','sentiment/bbg')) else 'PARTIAL'}
        return obj

    def social(self,t,date):
        s = self.vendor.get(t,{})
        counts = s.get('TWITTER_PUBLICATION_COUNT',Series({}))
        tones = s.get('TWITTER_SENTIMENT_DAILY_AVG',Series({}))
        now = counts.window(date,7)
        prev = counts.window(shifted(date,-7),28)
        def tone(rows):
            valid = [(v,tones.data[d]) for d,v in rows if v>0 and d in tones.data]
            n = sum(v for v,_ in valid)
            return sum(v*x for v,x in valid)/n if n>=5 and len(valid)>=3 else None
        a,b = tone(now),tone(prev)
        att = math.log1p(mean([v for _,v in now]))-math.log1p(mean([v for _,v in prev])) if len(now)>=4 and len(prev)>=14 else None
        return {'tone7':a,'tone_change':a-b if a is not None and b is not None else None,
                'attention':att,'mentions7':sum(v for _,v in now) if len(now)>=4 else None,
                'vendor_days7':len(now),'vendor_days28':len(prev)}

    def rows(self, signal):
        if signal in self.cache:
            return self.cache[signal]
        ci = bisect.bisect_left(self.calendar,signal)-1
        if ci < 0:
            return {}
        cut = self.calendar[ci]
        year = int(signal[:4])
        result = {}
        for t in self.names:
            dates = self.px[t].dates
            i = bisect.bisect_right(dates,cut)-1
            if i<0 or shifted(dates[i],5)<cut:
                continue
            r = dict(self.indicators[t].get(dates[i],{}))
            if not r:
                continue
            r.update(self.social(t,cut))
            r.update({'ticker':t,'signal':signal,'cutoff':cut,'price_date':dates[i], 'eps28':None,'sales28':None,
                      'target_fy':year+1,'ss_tone':None,'curated_tone':None,'short_interest':None})
            for f,key in [('BEST_EPS','eps28'),('BEST_SALES','sales28')]:
                seq = self.estimates.get(year,{}).get(t,{}).get(f,Series({}))
                now,old = seq.at(cut,self.max_est_age),seq.at(shifted(cut,-28),self.max_est_age)
                r[key] = symmetric_change(now,old) if f=='BEST_EPS' else now/old-1 if now is not None and old is not None and old>0 else None
                r['eps_now' if f=='BEST_EPS' else 'sales_now'] = now
                r['eps_old' if f=='BEST_EPS' else 'sales_old'] = old
                ix=bisect.bisect_right(seq.dates,cut)-1
                r['eps_observed' if f=='BEST_EPS' else 'sales_observed']=seq.dates[ix] if now is not None and ix>=0 else None
                ix=bisect.bisect_right(seq.dates,shifted(cut,-28))-1
                r['eps_old_observed' if f=='BEST_EPS' else 'sales_old_observed']=seq.dates[ix] if old is not None and ix>=0 else None
            ss = [v for d,v in self.ss.get('tickers',{}).get(t,{}).items() if shifted(cut,-28)<d<=cut]
            n = sum(v.get('tone_n',0) for v in ss)
            r['ss_tone'] = sum(v.get('tone_w',0) for v in ss)/n if n>=3 else None
            r['ss_notes28'] = sum(v.get('n',0) for v in ss) if cut>=self.ss.get('since','2026-01-30') else None
            own = [v for d,v in self.own.get('tickers',{}).get(t,{}).items() if shifted(cut,-28)<d<=cut]
            bull,bear = sum(v.get('bull',0) for v in own),sum(v.get('bear',0) for v in own)
            r['curated_tone'] = (bull-bear)/(bull+bear) if bull+bear>=5 and len(own)>=3 else None
            r['curated_mentions28'] = sum(v.get('tone_n',0) for v in own) if cut>=self.own['start'] else None
            si = self.vendor.get(t,{}).get('SI_PERCENT_EQUITY_FLOAT',Series({}))
            # Display only: publication-time alignment is not certified for this field.
            r['short_interest'] = si.at(cut,40)
            p = self.prices['names'].get(t,{})
            vi = bisect.bisect_right(p.get('d',[]),cut)
            volumes = [v for v in p.get('v',[])[max(0,vi-20):vi] if v is not None and v>0]
            r['volume_ratio'] = volumes[-1]/mean(volumes[:-1]) if len(volumes)==20 and mean(volumes[:-1]) else None
            result[t] = r
        self.cache[signal] = result
        return result


def scores(rows, eligible):
    fields = CORE+['ss_tone','curated_tone']
    pr = {f:ranks({t:rows[t][f] for t in eligible if rows[t].get(f) is not None}) for f in fields}
    out = {}
    for t in eligible:
        def pillar(fs):
            return mean([pr[f][t] for f in fs]) if all(t in pr[f] for f in fs) else None
        a,b,c = pillar(TECH),pillar(EARN),pillar(SOCIAL)
        r = {'technical':a,'earnings':b,'social':c,'attention':pr['attention'].get(t),
             'momentum':pr['momentum63'].get(t),'rsi':pr['rsi14'].get(t), 'ss':pr['ss_tone'].get(t), 'curated':pr['curated_tone'].get(t)}
        r['te'] = mean([a,b]) if a is not None and b is not None else None
        r['tes'] = mean([a,b,c]) if all(x is not None for x in [a,b,c]) else None
        r['tess'] = mean([a,b,c,r['ss']]) if all(x is not None for x in [a,b,c,r['ss']]) else None
        r['tesx'] = mean([a,b,c,r['curated']]) if all(x is not None for x in [a,b,c,r['curated']]) else None
        out[t] = r
    return out


def bootstrap(values, horizon, draws=1200):
    if len(values)<8:
        return None
    block = 4 if horizon==5 else 2
    rng = random.Random(428+len(values)+horizon)
    means = []
    n = len(values)
    for _ in range(draws):
        sample = []
        while len(sample)<n:
            start=rng.randrange(n)
            sample.extend(values[(start+j)%n] for j in range(block))
        means.append(mean(sample[:n]))
    means.sort()
    return [means[int(.025*draws)],means[int(.975*draws)]]


def select_events(inputs,year,horizon,cohort,lag_extra=0):
    cal = inputs.calendar
    signal_i = next(i for i,d in enumerate(cal) if d>=f'{year}-01-01' and dt.date.fromisoformat(d).weekday()==4)
    events, skipped = [],[]
    required = CORE + (['ss_tone'] if cohort=='sellside' else ['curated_tone'] if cohort=='curated' else [])
    while signal_i+1+horizon<len(cal):
        signal = cal[signal_i]
        if signal>min(inputs.common_end,f'{year}-12-31'):
            break
        entry_i,exit_i=signal_i+1,signal_i+1+horizon
        if cal[exit_i]>min(inputs.ret['asof'],f'{year}-12-31'):
            break
        rows = inputs.rows(cal[signal_i-lag_extra])
        eligible = sorted(t for t in inputs.usd if t in rows and all(rows[t].get(f) is not None for f in required))
        # Eligibility and rankings are frozen BEFORE observing any future price.
        score = scores(rows,eligible)
        if len(eligible)<30:
            skipped.append({'date':signal,'reason':'fewer than 30 complete signal observations','n':len(eligible)})
        else:
            missing=[t for t in eligible if any(d not in inputs.tri[t].data for d in cal[entry_i:exit_i+1])]
            if missing:
                skipped.append({'date':signal,'reason':'missing outcome: whole matched event excluded','tickers':missing})
            else:
                returns={t:inputs.tri[t].data[cal[exit_i]]/inputs.tri[t].data[cal[entry_i]]-1 for t in eligible}
                events.append({'signal':signal,'cutoff':cal[signal_i-lag_extra-1],'entry':cal[entry_i],'exit':cal[exit_i],
                    'entry_i':entry_i,'exit_i':exit_i,'eligible':eligible,'scores':score,'returns':returns})
        signal_i+=horizon
    return events,skipped


def turnover(target, previous):
    return sum(abs(target.get(t,0)-previous.get(t,0)) for t in set(target)|set(previous))


def execution_scale(target, previous, cost):
    """Self-financing fees: x + c * sum(abs(x*w_target - w_pre)) = 1.

    x is post-fee wealth / pre-fee wealth. Traded notional is measured against
    pre-fee wealth. Unlike unscaled target L1, this also handles initial funding.
    """
    if cost==0:
        return 1.,turnover(target,previous)
    lo,hi=0.,1.
    for _ in range(55):
        x=(lo+hi)/2
        traded=sum(abs(x*target.get(t,0)-previous.get(t,0)) for t in set(target)|set(previous))
        if x+cost*traded>1:
            hi=x
        else:
            lo=x
    x=(lo+hi)/2
    traded=sum(abs(x*target.get(t,0)-previous.get(t,0)) for t in set(target)|set(previous))
    return x,traded


def portfolio(inputs,events,key,cost_bps):
    cost=cost_bps/10000
    equity=1.
    prior={}
    curve=[]
    periods=[]
    ledger=[]
    total_turn=0.
    for ei,event in enumerate(events):
        names=event['eligible']
        if key=='qqq':
            selected=['_QQQ']
        elif key=='equal':
            selected=names
        else:
            selected=sorted(names,key=lambda t:(-event['scores'][t][key],t))[:max(1,math.ceil(len(names)/5))]
        target={t:1/len(selected) for t in selected}
        gap=ei>0 and events[ei-1]['exit']!=event['entry']
        # A coverage gap is cash, not a free mark-to-market jump.
        if gap and prior:
            equity*=1-cost
            total_turn+=1
            if curve:
                curve[-1][1]=equity
            periods[-1]['net']=(1+periods[-1]['net'])*(1-cost)-1
            prior={}
        fee_scale,trade=execution_scale(target,prior,cost)
        total_turn+=trade
        before=equity
        equity*=fee_scale
        start_equity=equity
        entry=event['entry']
        if not curve:
            curve.append([event['signal'],before])
        if curve and curve[-1][0]==entry:
            curve[-1][1]=equity
        else:
            curve.append([entry,equity])
        for d in inputs.calendar[event['entry_i']+1:event['exit_i']+1]:
            factor=mean([inputs.tri[t].data[d]/inputs.tri[t].data[entry] for t in selected])
            equity=start_equity*factor
            curve.append([d,equity])
        factors={t:inputs.tri[t].data[event['exit']]/inputs.tri[t].data[entry] for t in selected}
        gross=mean(list(factors.values()))
        prior={t:target[t]*factors[t]/gross for t in selected}
        if ei==len(events)-1:
            equity*=1-cost
            total_turn+=1
            curve[-1][1]=equity
        periods.append({'signal':event['signal'],'entry':entry,'exit':event['exit'], 'net':equity/before-1,'gross':gross-1,'turnover':trade})
        if key not in ('equal','qqq'):
            bottom=sorted(names,key=lambda t:(event['scores'][t][key],t))[:len(selected)]
            ledger.append({'signal':event['signal'],'cutoff':event['cutoff'],'entry':entry,'exit':event['exit'],
               'n':len(names),'top':selected,'bottom':bottom,'gross_top':gross-1,
               'gross_bottom':mean([event['returns'][t] for t in bottom]),
               'ic':spearman({t:event['scores'][t][key] for t in names},event['returns'])})
    peak=1.
    dd=0.
    for _,value in curve:
        peak=max(peak,value)
        dd=min(dd,value/peak-1)
    return {'return':equity-1 if periods else None,'drawdown':dd if periods else None,'turnover':total_turn,
            'n':len(periods),'mean_period':mean([p['net'] for p in periods]),
            'curve':curve,'periods':periods,'ledger':ledger,
            'mean_ic':mean([r['ic'] for r in ledger if r['ic'] is not None]),
            'spread':mean([r['gross_top']-r['gross_bottom'] for r in ledger])}


def compare(a,b,horizon):
    diffs=[x['net']-y['net'] for x,y in zip(a['periods'],b['periods'])]
    return {'n':len(diffs),'mean_increment':mean(diffs),'ci':bootstrap(diffs,horizon),
            'positive_periods':sum(v>0 for v in diffs),'cumulative_difference':a['return']-b['return'] if diffs else None}


def run_tests(inputs):
    results={}
    for cohort in ['core','sellside','curated']:
        results[cohort]={}
        for year in [2024,2025,2026]:
            if cohort!='core' and year<2026:
                continue
            results[cohort][str(year)]={}
            for horizon in [5,20]:
                events,skipped=select_events(inputs,year,horizon,cohort)
                keys=MODEL_KEYS if cohort=='core' else ['tes','tess' if cohort=='sellside' else 'tesx']
                bucket={'n':len(events),'first':events[0]['entry'] if events else None,
                        'last':events[-1]['exit'] if events else None,'skipped':skipped,'costs':{},
                        'names_min':min([len(e['eligible']) for e in events],default=0),
                        'names_max':max([len(e['eligible']) for e in events],default=0)}
                for cost in COSTS:
                    models={k:portfolio(inputs,events,k,cost) for k in keys+['equal','qqq']}
                    for key,m in models.items():
                        if m['n']:
                            m['excess_equal']=m['return']-models['equal']['return']
                            m['excess_qqq']=m['return']-models['qqq']['return']
                        else:
                            m['excess_equal']=m['excess_qqq']=None
                        if cost!=10:
                            m.pop('ledger',None)
                    tests={'sentiment':compare(models['tes'],models['te'],horizon),
                           'earnings':compare(models['te'],models['technical'],horizon)} if cohort=='core' else {
                           'addition':compare(models[keys[-1]],models['tes'],horizon)}
                    bucket['costs'][str(cost)]={'models':models,'tests':tests}
                # Store exact eligible returns for auditing top/bottom selections and factor exposures.
                bucket['events']=[{'signal':e['signal'],'cutoff':e['cutoff'],'entry':e['entry'],'exit':e['exit'],
                    'eligible':e['eligible'],'returns':e['returns']} for e in events]
                results[cohort][str(year)][str(horizon)]=bucket
                print(f'{cohort} {year} {horizon}d: {len(events)} complete periods; {len(skipped)} skipped',flush=True)
    # A further one-session lag is a robustness check, not a parameter to optimize.
    events,skipped=select_events(inputs,2026,20,'core',lag_extra=1)
    a,b=portfolio(inputs,events,'tes',10),portfolio(inputs,events,'te',10)
    results['lag_sensitivity']={'test':compare(a,b,20),'n':len(events),'skipped':skipped}
    # Sparse consensus updates can be carried as last known, never back-filled.
    # Report the stricter availability definition as a sensitivity, not a fitted choice.
    inputs.max_est_age=10
    inputs.cache.clear()
    events,skipped=select_events(inputs,2026,20,'core')
    a,b=portfolio(inputs,events,'tes',10),portfolio(inputs,events,'te',10)
    results['freshness_sensitivity']={'test':compare(a,b,20),'n':len(events),'skipped':skipped,'max_estimate_age_days':10}
    inputs.max_est_age=35
    inputs.cache.clear()
    return results


def setup(row,score):
    t,e,s,a=[score.get(k) for k in ['technical','earnings','social','attention']]
    if any(x is None for x in [t,e,s,a]):
        return 'Incomplete inputs'
    if e>=.65 and t>=.55 and a<.45:
        return 'Quiet improvement'
    if a>=.75 and s>=.65 and e<.45:
        return 'Narrative ahead of estimates'
    if e<.35 and t<.35 and s<.45:
        return 'Deterioration'
    if s<.35 and e>=.55 and t>=.45:
        return 'Skepticism / improving numbers'
    if e>=.6 and t>=.6 and s>=.6:
        return 'Broad confirmation'
    if row.get('rsi14',50)>=70:
        return 'Strong / extended'
    if row.get('rsi14',50)<=30:
        return 'Weak / oversold'
    return 'Mixed evidence'


def snapshots(inputs):
    eligible_dates=[d for i,d in enumerate(inputs.calendar) if d>='2024-01-01' and d<=inputs.ret['asof'] and i>0 and inputs.calendar[i-1]<=inputs.bbg['asof']]
    latest=eligible_dates[-1]
    dates=sorted(set([d for d in eligible_dates if dt.date.fromisoformat(d).weekday()==4]+[latest]))
    out={}
    for date in dates:
        rows=inputs.rows(date)
        # Display percentiles include all covered listings, clearly separated from the USD backtest.
        sc=scores(rows,list(rows))
        out[date]=[{**r,'scores':sc[t],'setup':setup(r,sc[t])} for t,r in rows.items()]
    return out,latest


def peer_groups(inputs):
    """Current curated competitors, with explicit sector fallback; no inferred edges."""
    direct = {t:{} for t in inputs.names}
    for a,b,reason in inputs.peer_graph.get('competes',[]):
        if a in direct and b in direct and a!=b:
            direct[a][b] = reason
            direct[b][a] = reason
    return {t:{'direct':[{'ticker':p,'reason':why} for p,why in sorted(direct[t].items())],
               'sector':[p for p in inputs.names if p!=t and inputs.groups.get(t) not in (None,'Other')
                         and inputs.groups.get(p)==inputs.groups.get(t)],
               'default_mode':'direct' if direct[t] else 'sector'} for t in inputs.names}


def company_studies(inputs):
    """Single-stock outcomes using the same all-listing ranks as the display.

    Fixed calendar schedules, never selected using the score or future return.
    These are gross descriptive outcomes, not a traded or fitted strategy.
    Retain unavailable outcomes as null so the UI can disclose missing coverage.
    """
    out = {t:{} for t in inputs.usd}
    cal = inputs.calendar
    for year in [2024,2025,2026]:
        first = next(i for i,d in enumerate(cal) if d>=f'{year}-01-01' and dt.date.fromisoformat(d).weekday()==4)
        for horizon in [5,20]:
            for t in out:
                out[t].setdefault(str(year),{})[str(horizon)] = []
            for si in range(first,len(cal)-horizon-1,horizon):
                signal,entry,exit_date = cal[si],cal[si+1],cal[si+1+horizon]
                if signal>min(inputs.common_end,f'{year}-12-31') or exit_date>min(inputs.ret['asof'],f'{year}-12-31'):
                    break
                rows = inputs.rows(signal)
                sc = scores(rows,list(rows))
                q0,q1 = (inputs.tri['_QQQ'].data.get(d) for d in [entry,exit_date])
                for ticker in out:
                    if ticker not in rows:
                        continue
                    a,b = (inputs.tri[ticker].data.get(d) for d in [entry,exit_date])
                    ret = b/a-1 if a is not None and b is not None and a>0 else None
                    out[ticker][str(year)][str(horizon)].append({
                        'signal':signal,'cutoff':cal[si-1],'entry':entry,'exit':exit_date,
                        'scores':sc[ticker],'return':ret,'qqq_return':q1/q0-1,
                        'tri_entry':a,'tri_exit':b,'peers':len(rows)})
    return out


def relative_context(inputs,studies):
    """All covered peers at each fixed outcome-study signal, including non-US peers."""
    result={};cal=inputs.calendar
    for year in [2024,2025,2026]:
        first=next(i for i,d in enumerate(cal) if d>=f'{year}-01-01' and dt.date.fromisoformat(d).weekday()==4)
        for h in [5,20]:
            for si in range(first,len(cal)-h-1,h):
                signal,entry,exit_date=cal[si],cal[si+1],cal[si+1+h]
                if signal>min(inputs.common_end,f'{year}-12-31') or exit_date>min(inputs.ret['asof'],f'{year}-12-31'):
                    break
                if signal not in result:
                    raw=inputs.rows(signal)
                    result[signal]={'scores':scores(raw,list(raw)),'raw':{t:{f:r.get(f) for f in [*ranking_lab.FEATURES,'vendor_days7']} for t,r in raw.items()},'horizons':{}}
                result[signal]['horizons'][str(h)]={'signal':signal,'cutoff':cal[si-1],'entry':entry,'exit':exit_date,
                    'qqq_return':inputs.tri['_QQQ'].data[exit_date]/inputs.tri['_QQQ'].data[entry]-1}
    return result


def relative_guardrails(inputs,studies,context):
    bad=[];matches=0;slots=0;seen=0
    ix={d:i for i,d in enumerate(inputs.calendar)}
    for h in ['5','20']:
        prior=None
        for date,pack in sorted(context.items()):
            e=pack['horizons'].get(h)
            if not e:
                continue
            slots+=len(inputs.usd)
            if not(e['cutoff']<date<e['entry']<e['exit']) or ix[e['exit']]-ix[e['entry']]!=int(h) or (prior and prior>e['entry']):
                bad.append(date+'/'+h)
            prior=e['exit']
    for t,ys in studies.items():
        for hs in ys.values():
            for h,es in hs.items():
                for e in es:
                    seen+=1
                    if e['scores']!=context[e['signal']]['scores'].get(t):
                        bad.append(t+'/'+e['signal']+'/score')
                    else:
                        matches+=1
    return {'name':'Relative-context event alignment','status':'FAIL' if bad else 'PASS',
            'detail':f'{matches} company event scores match their exact-date peer context; 5/20-session windows and non-overlap verified. {slots-seen} unavailable company rows remain placeholders in the {slots}-slot master schedule.',
            'type':'Internal schedule and score check','bad':bad}


def evidence(inputs):
    result=defaultdict(list)
    for o in inputs.desk.get('observations',[]):
        t=o.get('ticker')
        if t not in inputs.names:
            continue
        result[t].append({k:o.get(k) for k in ['date','firm','author','role','kind','tone','position','summary','excerpt','subject','source_id','review_date']})
    for t in result:
        result[t]=sorted(result[t],key=lambda x:x.get('date') or '',reverse=True)
    for t in inputs.names:
        for date,v in sorted(inputs.own.get('tickers',{}).get(t,{}).items(),reverse=True):
            for post in v.get('top',[])[:1]:
                result[t].append({'date':date,'firm':'Curated X','author':post.get('h'), 'role':'Selected account',
                    'kind':'Curated X','summary':post.get('t'),'tone':post.get('s'),
                    'source_id':None,'note':'Archived excerpt; post URL and historical engagement snapshot not supplied.'})
    return {t:sorted(v,key=lambda x:x.get('date') or '',reverse=True) for t,v in result.items()}


def guardrails(inputs,results):
    checks=[]
    diffs=[]
    for t in inputs.names:
        cached=inputs.prices['names'][t]
        pairs=[(d,p) for d,p in zip(cached['d'],cached['c']) if d in inputs.px[t].data and p>0][-10:]
        diffs.extend((abs(inputs.px[t].data[d]/p-1),t,d) for d,p in pairs)
    worst=sorted(diffs,reverse=True)[:5]
    checks.append({'name':'Independent cache price reconciliation','status':'PASS' if worst and worst[0][0]<.001 else 'FAIL',
        'detail':f'{len(diffs)} same-security/date observations, fresh Bloomberg PX_LAST versus existing OHLCV cache; tolerance 0.1%.',
        'worst':worst,'type':'Independent extraction cross-check; same underlying vendor'})
    bad=[]
    for cohort in ['core','sellside','curated']:
        for year,hs in results[cohort].items():
            for h,b in hs.items():
                if any(not(e['cutoff']<e['signal']<e['entry']<e['exit']) for e in b['events']):
                    bad.append(f'{cohort}/{year}/{h}')
    checks.append({'name':'Information cutoff before execution','status':'FAIL' if bad else 'PASS',
                   'detail':'Every event: source-date cutoff < signal session < next-close entry < exit.','type':'Internal timing check','bad':bad})
    discrepancies=[]
    for cohort in ['core','sellside','curated']:
        for year,hs in results[cohort].items():
            for h,b in hs.items():
                for cost,pack in b['costs'].items():
                    for key,m in pack['models'].items():
                        if m['n']:
                            product=math.prod(1+p['net'] for p in m['periods'])-1
                            if abs(product-m['return'])>1e-9:
                                discrepancies.append(f'{cohort}/{year}/{h}/{cost}/{key}')
    checks.append({'name':'Cash and return reconciliation','status':'FAIL' if discrepancies else 'PASS',
                   'detail':'Compounded holding-period returns reconcile to the marked portfolio, including gaps and liquidation costs.',
                   'type':'Internal accounting check','bad':discrepancies})
    missing=sum(sum(s['reason'].startswith('missing outcome') for s in b['skipped']) for c in ['core','sellside','curated'] for hs in results[c].values() for b in hs.values())
    checks.append({'name':'Missing realized prices','status':'FAIL' if missing else 'PASS',
                   'detail':f'{missing} whole matched events excluded after a missing outcome. No replacement stock or shortened return was inserted.',
                   'type':'Coverage check'})
    checks.append({'name':'Listing currency and exchange','status':'PASS' if all(inputs.instruments[inputs.companies[t]['bbg']]['CRNCY']=='USD' and inputs.companies[t]['bbg'].endswith(' US Equity') for t in inputs.usd) else 'FAIL',
                   'detail':f'{len(inputs.usd)} US listings verified with Bloomberg CRNCY. Financial-reporting currency is never used for portfolio eligibility.',
                   'type':'Independent reference-data check'})
    checks.append({'name':'Original point-in-time vintages','status':'PARTIAL',
        'detail':'Fixed fiscal targets prevent horizon roll. Vendor corrections, original release times and original consensus constituent vintages are not certified.', 'type':'Data limitation'})
    checks.append({'name':'Historical universe membership','status':'PARTIAL',
        'detail':'Current wiki watchlist projected backward; includes selection and survivorship bias. This is not a broad investable-universe test.','type':'Data limitation'})
    checks.append({'name':'Genuine out-of-sample evidence','status':'PARTIAL',
        'detail':'Rules frozen before this run, but 2026 has been studied previously. All reported history is retrospective; no live validation yet.','type':'Research limitation'})
    checks.append({'name':'Independent skeptic review','status':'PENDING','detail':'Required before delivery.','type':'Review'})
    review_path=OUT/'audit_review.json'
    if review_path.exists():
        review=json.loads(review_path.read_text(encoding='utf-8'))
        if review.get('fingerprint')==review_fingerprint(inputs):
            checks[-1].update({'status':review.get('status','PARTIAL'),'detail':review.get('summary',''),'review':review})
        else:
            checks[-1].update({'status':'PENDING','detail':'A prior review exists, but model, template, protocol or source hashes changed. This build needs a fresh review.'})
    return checks


def review_fingerprint(inputs):
    document={'sources':{k:v['sha256'] for k,v in inputs.sources.items()},
              'model':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'template':hashlib.sha256((BASE/'_tools/sentiment_research.template.html').read_bytes()).hexdigest(),
              'company_ui':{ext:hashlib.sha256((BASE/f'_tools/sentiment_company_ui.{ext}').read_bytes()).hexdigest() for ext in ['js','css']},
              'relative_test':{name:hashlib.sha256((BASE/f'_tools/{name}').read_bytes()).hexdigest() for name in ['sentiment_relative_backtest.py','sentiment_relative_ui.js']},
              'indicator_ranking':{name:hashlib.sha256((BASE/f'_tools/{name}').read_bytes()).hexdigest() for name in ['sentiment_indicator_ranking.py','sentiment_ranking_ui.js']},
              'pair_test':{name:hashlib.sha256((BASE/f'_tools/{name}').read_bytes()).hexdigest() for name in ['sentiment_pair_backtest.py','sentiment_pair_ui.js']},
              'fetcher':hashlib.sha256((BASE/'_tools/fetch_sentiment_research.py').read_bytes()).hexdigest()}
    return hashlib.sha256(json.dumps(document,sort_keys=True).encode()).hexdigest()


def make_verdict(results,checks):
    primary=results['core']['2026']['20']['costs']['10']['tests']['sentiment']
    year_tests={y:results['core'][y]['20']['costs']['10']['tests']['sentiment'] for y in ['2024','2025','2026']}
    positive=all((v['mean_increment'] or -1)>0 for v in year_tests.values())
    lower=primary['ci'][0] if primary['ci'] else None
    failure=any(c['status']=='FAIL' for c in checks)
    passed=lower is not None and lower>0 and positive and not failure
    return {'label':'Research sample invalid — repair data before interpreting performance.' if failure else 'Provisional signal; paper-test only' if passed else 'Keep the research cockpit. Do not adopt the sentiment trade signal.',
        'alpha_case':'PROVISIONAL' if passed else 'NOT ESTABLISHED',
        'reason':'A numerical or outcome-coverage guardrail failed. Published performance is diagnostic only and cannot support an adoption decision.' if failure else 'The primary test meets the statistical screen, but historical universe and data-vintage limitations still prevent an investment-grade claim.' if passed else
                 'The incremental sentiment test does not clear the predeclared evidence threshold. Monitoring value is separate from demonstrated predictive value.',
        'primary':primary,'by_year':year_tests,'consistent_year_signs':positive,
        'actions':['Keep sourced comments, technical context and fixed-FY revisions together for research.',
                   'Avoid a paid expansion of social collection until prospective incremental value is demonstrated.',
                   'Freeze the design and collect true as-received observations before any live signal decision.']}


def compact(obj):
    if isinstance(obj,float):
        return round(obj,7) if math.isfinite(obj) else None
    if isinstance(obj,dict):
        return {k:compact(v) for k,v in obj.items()}
    if isinstance(obj,list):
        return [compact(v) for v in obj]
    return obj


def build():
    inputs=Inputs()
    results=run_tests(inputs)
    snaps,latest=snapshots(inputs)
    stock_studies=company_studies(inputs)
    context=relative_context(inputs,stock_studies)
    checks=guardrails(inputs,results)
    checks.insert(-1,relative_guardrails(inputs,stock_studies,context))
    verdict=make_verdict(results,checks)
    payload={'meta':{'version':VERSION,'built':dt.datetime.now(dt.timezone.utc).isoformat(),'signal_asof':latest,'review_fingerprint':review_fingerprint(inputs),
             'social_asof':inputs.bbg['asof'],'price_asof':inputs.ret['asof'],'source':'Bloomberg + existing Capstone source archives',
             'universe_count':len(inputs.names),'usd_count':len(inputs.usd),'sources':inputs.sources,
             'coverage':{'curated_start':inputs.own['start'],'sellside_start':inputs.ss.get('since','2026-01-30'),
                         'desk':inputs.desk.get('meta',{}),'fixed_fy':'2025Y / 2026Y / 2027Y'}},
             'protocol':inputs.protocol,'labels':LABELS,'results':results,'snapshots':snaps,'evidence':evidence(inputs),
             'company_studies':stock_studies,
             'relative_context':context,
             'peer_groups':peer_groups(inputs),
             'names':{t:{'name':inputs.companies[t].get('name',t),'sector':inputs.groups.get(t,'Other'),
                        'ccy':inputs.instruments.get(inputs.companies[t]['bbg'],{}).get('CRNCY'),
                        'fund_ccy':inputs.companies[t].get('ccy'),'backtest_listing':t in inputs.usd,
                        'bbg':inputs.companies[t]['bbg']} for t in inputs.names},
             'checks':checks,'verdict':verdict}
    payload=compact(payload)
    print('Relative-context outcomes and date-cluster checks...',flush=True)
    payload['relative_summary']=compact(relative_lab.research_summary(payload))
    payload['indicator_rankings']=compact(ranking_lab.ranking_summary(payload))
    payload['pair_tests']=compact(pair_lab.research(payload))
    OUT.mkdir(exist_ok=True)
    serialized=json.dumps(payload,ensure_ascii=False,separators=(',',':'),allow_nan=False)
    (OUT/'dashboard.json').write_text(serialized,encoding='utf-8')
    (OUT/'pair_frozen_rules.json').write_text(json.dumps({'selection_hash':payload['pair_tests']['selection_hash'],'train':'2024–2025','selected_retrospectively_on':payload['meta']['built'],'protocol':inputs.protocol['pair_chronological_test'],'source_manifest':inputs.sources,'selections':payload['pair_tests']['selections']},ensure_ascii=False,indent=2),encoding='utf-8')
    template=(BASE/'_tools/sentiment_research.template.html').read_text(encoding='utf-8')
    template=template.replace('__COMPANY_UI_JS__',(BASE/'_tools/sentiment_company_ui.js').read_text(encoding='utf-8'))
    template=template.replace('__RELATIVE_UI_JS__',(BASE/'_tools/sentiment_relative_ui.js').read_text(encoding='utf-8'))
    template=template.replace('__RANKING_UI_JS__',(BASE/'_tools/sentiment_ranking_ui.js').read_text(encoding='utf-8'))
    template=template.replace('__PAIR_UI_JS__',(BASE/'_tools/sentiment_pair_ui.js').read_text(encoding='utf-8'))
    template=template.replace('__COMPANY_UI_CSS__',(BASE/'_tools/sentiment_company_ui.css').read_text(encoding='utf-8'))
    safe=serialized.replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    (BASE/'_dashboards/sentiment-research.html').write_text(template.replace('__PAYLOAD__',safe),encoding='utf-8')
    def pp(x):
        return 'n/a' if x is None else f'{x*100:+.2f} pp'
    lines=['# Sentiment decision lab — research verdict', '',f'Built {payload["meta"]["built"]}. Bloomberg total returns through {inputs.ret["asof"]}; social through {inputs.bbg["asof"]}.',
           '', '## Decision', '',verdict['label'], '',verdict['reason'], '',
           '## Primary comparison', '', 'Technical + fixed-FY revisions + X versus Technical + fixed-FY revisions. 20-session holds, same eligible stocks and dates, next-close execution, 10 bps per one-way traded notional.', '',
           '| Year | Completed periods | Mean incremental return per hold | Paired 95% interval | Cumulative difference |',
           '|---|---:|---:|---|---:|']
    for y,v in verdict['by_year'].items():
        ci=' / '.join(pp(x) for x in v['ci']) if v['ci'] else 'insufficient periods'
        lines.append(f'| {y} | {v["n"]} | {pp(v["mean_increment"])} | {ci} | {pp(v["cumulative_difference"])} |')
    lines+=['','## Grounding and limits','','HARD: retrieved prices and vendor observations. PARTIAL: original data vintages, parsed text, current watchlist history. ESTIMATE: fixed research weights, windows and transaction-cost scenarios. No weight was fitted. Costs are scenarios, not a claim about achievable execution. No expected future return is estimated.',
            '', 'Signals use only source dates before the signal session. Fixed target fiscal year equals signal calendar year + 1, used for both estimate observations; target differs in time-to-maturity across fiscal calendars. EPS uses symmetric change to handle zero/negative earnings.',
            '', 'Cumulative differences are percentage-point differences between compounded long-only portfolios. Holding-period confidence intervals refer to paired mean differences, not cumulative alpha. No multiple-testing adjustment. Current watchlist selection and hindsight prevent out-of-sample claims.', '',
            '## Guardrails','']
    lines += [f'- {c["status"]} — {c["name"]}: {c["detail"]}' for c in checks]
    lines += ['', '## Reproduce', '', '`py -B _wiki/_tools/build_sentiment_research.py` (offline cached inputs).',
              '', '`py -B _wiki/_tools/fetch_sentiment_research.py --asof YYYY-MM-DD` refreshes only this experiment’s Bloomberg inputs.',
              '', 'Source input hashes, complete matched event ledgers, scenario results and protocol: `_data/sentiment_research/`. Existing hub layouts and source company pages are unchanged.']
    (BASE/'_meta/sentiment-research-verdict.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'verdict':verdict,'checks':checks,'html_bytes':len(serialized)},ensure_ascii=False),flush=True)
    return payload


if __name__=='__main__':
    build()
