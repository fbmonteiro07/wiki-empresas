"""Descriptive relative-context tests. Fixed rules; no optimization or forecasts."""
import bisect
import datetime as dt
import math
import statistics

KEYS = ['tes','te','technical','earnings','social','ss','tess','curated','tesx','attention']


def valid(x):
    return isinstance(x,(int,float)) and math.isfinite(x)


def avg(a):
    return statistics.fmean(a) if a else None


def percentile(value, values, minimum=1):
    a=[x for x in values if valid(x)]
    if not valid(value) or len(a)<minimum:
        return None,len(a)
    return (sum(x<value-1e-10 for x in a)+.5*sum(abs(x-value)<=1e-10 for x in a))/len(a),len(a)


def band(p):
    return None if p is None else 0 if p<.3 else 2 if p>=.7 else 1


def start_date(date, window='364'):
    return date[:4]+'-01-01' if window=='ytd' else (dt.date.fromisoformat(date)-dt.timedelta(days=int(window))).isoformat()


def peers_for(payload,t):
    g=payload['peer_groups'][t]
    names=[r['ticker'] for r in g['direct']] if g['default_mode']=='direct' else g['sector']
    return sorted(set(p for p in names if p!=t and p in payload['names']))


class Context:
    def __init__(self,payload):
        self.p=payload
        self.dates=sorted(payload['snapshots'])
        self.rows={d:{r['ticker']:r for r in rs} for d,rs in payload['snapshots'].items()}
        self.cache={}

    def ranks_at(self,t,date,key,window='364',peers=None):
        names=tuple(peers_for(self.p,t) if peers is None else sorted(set(p for p in peers if p!=t and p in self.p['names'])))
        cache_key=t,date,key,window,names
        if cache_key in self.cache:
            return self.cache[cache_key]
        cross=self.p['relative_context'][date]['scores']
        value=cross.get(t,{}).get(key)
        lo=bisect.bisect_left(self.dates,start_date(date,window))
        hi=bisect.bisect_left(self.dates,date)
        a=[self.rows[d].get(t,{}).get('scores',{}).get(key) for d in self.dates[lo:hi]]
        own,own_n=percentile(value,a,8)
        peer,peer_n=percentile(value,[cross.get(n,{}).get(key) for n in names])
        result={'own':own,'peer':peer,'own_n':own_n,'peer_n':peer_n}
        self.cache[cache_key]=result
        return result

    def events(self,t,year,h,key,window='364',peers=None,cutoff='9999-12-31'):
        out=[];observed={}
        for y,hs in self.p['company_studies'].get(t,{}).items():
            if year!='all' and y!=str(year):
                continue
            observed.update({e['signal']:e for e in hs[str(h)]})
        for date,pack in self.p['relative_context'].items():
            e=pack['horizons'].get(str(h))
            if not e or e['exit']>cutoff or (year!='all' and date[:4]!=str(year)):
                continue
            row=observed.get(date,{**e,'return':None,'scores':{}})
            out.append({**row,**self.ranks_at(t,date,key,window,peers)})
        return sorted(out,key=lambda e:e['signal'])


def value_of(e,basis='absolute'):
    r=e.get('return')
    q=e.get('qqq_return')
    return r if basis=='absolute' and valid(r) else r-q if valid(r) and valid(q) else None


def spread(events,axis,basis='absolute'):
    groups=[[],[],[]]
    for e in events:
        b=band(e.get(axis));v=value_of(e,basis)
        if b is not None and v is not None:
            groups[b].append(v)
    return avg(groups[2])-avg(groups[0]) if groups[0] and groups[2] else None


def block_interval(events,h,stat,draws=1000,minimum=20,multiplier=1):
    if len(events)<minimum:
        return {'ci':None,'valid_draws':0,'draws':0}
    seed=51020+int(h)+len(events)
    block=(4 if int(h)==5 else 2)*multiplier
    estimates=[]
    for _ in range(draws):
        sample=[]
        while len(sample)<len(events):
            seed=(1664525*seed+1013904223)&0xffffffff
            k=(seed*len(events))//4294967296
            sample.extend(events[(k+j)%len(events)] for j in range(block))
        x=stat(sample[:len(events)])
        if valid(x):
            estimates.append(x)
    if len(estimates)<draws*.9:
        return {'ci':None,'valid_draws':len(estimates),'draws':draws}
    estimates.sort()
    return {'ci':[estimates[int(len(estimates)*.025)],estimates[min(len(estimates)-1,int(len(estimates)*.975))]],'valid_draws':len(estimates),'draws':draws}


def summarize(events,axis,h,basis='absolute',interval=True):
    groups=[[],[],[]];eligible=[];missing=0;thin=0
    for e in events:
        b=band(e.get(axis));v=value_of(e,basis)
        if b is None:
            continue
        if v is None:
            missing+=1
            continue
        groups[b].append(v);eligible.append(v)
        thin+=axis=='peer' and e['peer_n']<3
    bucket=[{'n':len(a),'mean':avg(a),'median':statistics.median(a) if a else None,
             'positive':sum(x>0 for x in a),'hit_rate':sum(x>0 for x in a)/len(a) if a else None} for a in groups]
    boot=block_interval(events,h,lambda es:spread(es,axis,basis)) if interval and len(eligible)>=20 and len(groups[0])>=5 and len(groups[2])>=5 else {'ci':None,'draws':0,'valid_draws':0}
    sensitivity=block_interval(events,h,lambda es:spread(es,axis,basis),multiplier=2) if boot['draws'] else {'ci':None,'draws':0,'valid_draws':0}
    return {'scheduled':len(events),'n':len(eligible),'missing_returns':missing,'unavailable_signal':len(events)-len(eligible)-missing,
            'thin_peer_events':thin,'baseline':avg(eligible),'baseline_hit':sum(x>0 for x in eligible)/len(eligible) if eligible else None,
            'buckets':bucket,'spread':spread(events,axis,basis),**boot,'long_block':sensitivity}


def pooled_by_date(ctx,key,h,year,axis,minimum_peers=1):
    by_date={d:{'groups':[[],[],[]],'exit':p['horizons'][str(h)]['exit']} for d,p in ctx.p['relative_context'].items() if str(h) in p['horizons'] and d[:4]==str(year)}
    for t in ctx.p['company_studies']:
        for e in ctx.events(t,year,h,key):
            if axis=='peer' and e['peer_n']<minimum_peers:
                continue
            b=band(e[axis]);v=value_of(e)
            if b is not None and v is not None:
                by_date.setdefault(e['signal'],{'groups':[[],[],[]],'exit':e['exit']})['groups'][b].append(v)
    rows=[]
    for d,pack in sorted(by_date.items()):
        groups=pack['groups']
        value=avg(groups[2])-avg(groups[0]) if len(groups[0])>=5 and len(groups[2])>=5 else None
        rows.append({'signal':d,'exit':pack['exit'],'spread':value,'low_n':len(groups[0]),'high_n':len(groups[2])})
    usable=[e['spread'] for e in rows if valid(e['spread'])]
    stat=lambda es:avg([e['spread'] for e in es if valid(e['spread'])])
    boot=block_interval(rows,h,stat) if len(usable)>=20 else {'ci':None,'draws':0,'valid_draws':0}
    long_block=block_interval(rows,h,stat,multiplier=2) if len(usable)>=20 else {'ci':None,'draws':0,'valid_draws':0}
    return {'dates':len(usable),'scheduled':len(rows),'spread':avg(usable),**boot,'long_block':long_block,
            'minimum_peers':minimum_peers,'events':rows}


def research_summary(payload):
    ctx=Context(payload)
    aggregate={}
    for key in KEYS:
        aggregate[key]={}
        for h in [5,20]:
            aggregate[key][str(h)]={}
            for y in ['2024','2025','2026']:
                aggregate[key][str(h)][y]={
                    'own':pooled_by_date(ctx,key,h,y,'own'),
                    'peer':pooled_by_date(ctx,key,h,y,'peer'),
                    'peer_min3':pooled_by_date(ctx,key,h,y,'peer',3)}
    # A reproducible default audit sample; UI uses the same event ledger for every company.
    nvda={str(h):{y:{axis:summarize(ctx.events('NVDA',y,h,'tes'),axis,h) for axis in ['own','peer']}
                 for y in ['2024','2025','2026','all']} for h in [5,20]}
    return {'aggregate':aggregate,'audit_sample_nvda':nvda,
            'design':'52-week own history, current default peers, gross stock returns; no fitted weights. Date-block intervals exploratory and unadjusted.'}
