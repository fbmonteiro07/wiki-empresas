"""Four raw-indicator rankings on matched dates. Exploratory, no fitted rule."""
import math
from functools import lru_cache
import sentiment_relative_backtest as rel

FEATURES={'rsi14':'RSI14','eps28':'EPS revisions','tone7':'X sentiment','mentions7':'X mentions'}


class RawContext(rel.Context):
    def raw_events(self,t,h,window='364',peers=None,cutoff='9999-12-31'):
        names=rel.peers_for(self.p,t) if peers is None else sorted(set(p for p in peers if p!=t and p in self.p['names']))
        base=self.events(t,'all',h,'tes',window,names,cutoff)
        out=[]
        for e in base:
            date=e['signal'];cross=self.p['relative_context'][date]['raw']
            current=cross.get(t,{})
            valid_peers=[p for p in names if all(rel.valid(cross.get(p,{}).get(f)) for f in FEATURES)]
            hist=[self.rows[d].get(t,{}) for d in self.dates if rel.start_date(date,window)<=d<date]
            hist=[r for r in hist if all(rel.valid(r.get(f)) for f in FEATURES)]
            complete=all(rel.valid(current.get(f)) for f in FEATURES)
            percentiles={f:{
                'own':rel.percentile(current.get(f),[r[f] for r in hist],8)[0] if complete else None,
                'peer':rel.percentile(current.get(f),[cross[p][f] for p in valid_peers])[0] if complete else None
            } for f in FEATURES}
            out.append({**e,'raw':current,'raw_percentiles':percentiles,'own_n':len(hist),'peer_n':len(valid_peers)})
        return out


def matched(events,feature,axis,basis='absolute'):
    rows=[]
    for e in events:
        usable=all(e['raw_percentiles'][f][axis] is not None for f in FEATURES)
        rows.append({**e,axis:e['raw_percentiles'][feature][axis] if usable else None})
    return rows


@lru_cache(maxsize=32)
def draw_starts(n,h,multiplier):
    block=(4 if int(h)==5 else 2)*multiplier
    lengths=[block]*(n//block)+([n%block] if n%block else [])
    seed=51020+int(h)+n
    out=[]
    for _ in range(2000):
        starts=[]
        for _length in lengths:
            seed=(1664525*seed+1013904223)&0xffffffff
            starts.append((seed*n)//4294967296)
        out.append(starts)
    return lengths,out


def ranking_bootstrap(events,axis,h,basis,multiplier=1):
    observed=rel.spread(events,axis,basis);n=len(events)
    rows=[]
    for e in events:
        b=rel.band(e.get(axis));v=rel.value_of(e,basis)
        rows.append((v,1,0.,0) if v is not None and b==0 else (0.,0,v,1) if v is not None and b==2 else (0.,0,0.,0))
    lengths,starts=draw_starts(n,int(h),multiplier)
    blocks={length:[tuple(sum(rows[(i+j)%n][c] for j in range(length)) for c in range(4)) for i in range(n)] for length in set(lengths)}
    dist=[]
    for sample in starts:
        ls=hs=0.;ln=hn=0
        for i,length in zip(sample,lengths):
            a,b,c,d=blocks[length][i];ls+=a;ln+=b;hs+=c;hn+=d
        if ln and hn:
            dist.append(hs/hn-ls/ln)
    dist.sort();enough=len(dist)>=1800
    tails=sum(abs(x-observed)+1e-12>=abs(observed) for x in dist) if observed is not None else len(dist)
    p=(1+tails)/(len(dist)+1) if enough and observed is not None else 1.
    bounds=wilson(tails,len(dist)) if enough else [1.,1.]
    return {'ci':[dist[int(len(dist)*.025)],dist[min(len(dist)-1,int(len(dist)*.975))]] if enough else None,
            'p':p,'p_mc':bounds,'tail_count':tails,'draws':2000,'valid_draws':len(dist)}


def wilson(k,n):
    # Monte Carlo uncertainty only; does not calibrate the bootstrap hypothesis test.
    q=k/n;z2=1.96**2;den=1+z2/n
    center=(q+z2/(2*n))/den
    radius=1.96*math.sqrt(q*(1-q)/n+z2/(4*n*n))/den
    return [(1+n*max(0.,center-radius))/(n+1),(1+n*min(1.,center+radius))/(n+1)]


def holm(values):
    order=sorted(range(len(values)),key=lambda i:values[i]);out=[1.]*len(values);previous=0.
    for j,i in enumerate(order):
        previous=max(previous,min(1.,(len(values)-j)*values[i]));out[i]=previous
    return out


def sign(x):
    return 0 if x is None or abs(x)<1e-12 else 1 if x>0 else -1


def supported(s,total=20,extreme=5):
    return s['n']>=total and s['buckets'][0]['n']>=extreme and s['buckets'][2]['n']>=extreme


def one_result(all_events,year,axis,feature,h,basis,cutoff):
    es=matched(all_events,feature,axis,basis)
    selected=[e for e in es if year=='all' or e['signal'][:4]==str(year)]
    s=rel.summarize(selected,axis,h,basis,interval=False)
    empty={'ci':None,'p':1.,'p_mc':[1.,1.],'tail_count':0,'draws':0,'valid_draws':0}
    boot=ranking_bootstrap(selected,axis,h,basis) if supported(s) else dict(empty)
    long=ranking_bootstrap(selected,axis,h,basis,2) if supported(s) else dict(empty)
    test_year=cutoff[:4] if year=='all' else str(year)
    years={y:rel.summarize([e for e in es if e['signal'][:4]==y],axis,h,basis,interval=False) for y in ['2024','2025','2026'] if y<=min(cutoff[:4],test_year)}
    direction=sign(s['spread'])
    valid_years=[v for v in years.values() if supported(v,10,3)]
    same_years=sum(sign(v['spread'])==direction and direction!=0 for v in valid_years)
    eligible=[e for e in selected if rel.band(e.get(axis)) is not None and rel.value_of(e,basis) is not None]
    extremes=[e for e in eligible if rel.band(e[axis]) in [0,2]]
    loo=[rel.spread([e for e in selected if e is not dropped],axis,basis) for dropped in extremes]
    loo_same=sum(sign(v)==direction and direction!=0 for v in loo)
    loo_supported=s['n']-1>=20 and s['buckets'][0]['n']-1>=5 and s['buckets'][2]['n']-1>=5
    training=rel.summarize([e for e in es if e['signal'][:4]<test_year],axis,h,basis,interval=False)
    test=years.get(test_year)
    temporal=supported(training) and test is not None and supported(test,10,3)
    confirmed=temporal and sign(training['spread'])==sign(test['spread'])!=0
    intervals=all(b['ci'] and ((b['ci'][0]>0 and direction>0) or (b['ci'][1]<0 and direction<0)) for b in [boot,long])
    return {'feature':feature,'axis':axis,'horizon':int(h),**s,'bootstrap':boot,'long_block':long,'p_raw':max(boot['p'],long['p']),
            'years':{y:{'n':v['n'],'low_n':v['buckets'][0]['n'],'high_n':v['buckets'][2]['n'],'spread':v['spread']} for y,v in years.items()},
            'year_supported':len(valid_years),'year_same_sign':same_years,
            'sample_first':eligible[0]['signal'] if eligible else None,'sample_last':eligible[-1]['signal'] if eligible else None,
            'loo':{'tested':len(loo),'same_sign':loo_same,'supported':loo_supported,'range':[min(v for v in loo if v is not None),max(v for v in loo if v is not None)] if any(v is not None for v in loo) else None},
            'temporal':{'train_n':training['n'],'train_spread':training['spread'],'test_year':test_year,'test_n':test['n'] if test else 0,'test_spread':test['spread'] if test else None,'available':temporal,'confirmed':bool(confirmed)},
            'checks':{'sample':supported(s),'intervals':bool(intervals),'outlier':bool(loo and loo_same==len(loo) and loo_supported),
                      'years':len(valid_years)>=2 and same_years==len(valid_years) and test is not None and supported(test,10,3),'prior_direction':bool(confirmed)}}


def company_ranking(payload,t,year='2026',window='364',peers=None,basis='absolute',cutoff=None):
    cutoff=cutoff or max(r['cutoff'] for r in payload['snapshots'][payload['meta']['signal_asof']])
    ctx=RawContext(payload);all_rows=[]
    for h in [5,20]:
        events=ctx.raw_events(t,h,window,peers,cutoff)
        for axis in ['own','peer']:
            all_rows.extend(one_result(events,year,axis,f,h,basis,cutoff) for f in FEATURES)
    adjusted=holm([r['p_raw'] for r in all_rows])
    lower=holm([max(r['bootstrap']['p_mc'][0],r['long_block']['p_mc'][0]) for r in all_rows])
    upper=holm([max(r['bootstrap']['p_mc'][1],r['long_block']['p_mc'][1]) for r in all_rows])
    for row,p,lo,hi in zip(all_rows,adjusted,lower,upper):
        row['p_holm']=p;row['p_holm_mc']=[lo,hi];row['checks']['multiple_tests']=p<=.05 and hi<=.05
        row['mc_borderline']=lo<=.05<hi
        row['robustness']='Sparse' if not row['checks']['sample'] else 'Within-company screen passes' if all(row['checks'].values()) else 'MC borderline' if row['mc_borderline'] else 'Some consistency' if row['checks']['intervals'] and row['checks']['outlier'] else 'Weak / unstable'
    for h in [5,20]:
        for axis in ['own','peer']:
            order=sorted([r for r in all_rows if r['horizon']==h and r['axis']==axis],key=lambda r:(r['spread'] is None,-abs(r['spread'] or 0),list(FEATURES).index(r['feature'])))
            for rank,row in enumerate(order,1):
                row['rank']=rank if row['spread'] is not None else None
    return {'ticker':t,'year':year,'window':window,'basis':basis,'cutoff':cutoff,'peers':rel.peers_for(payload,t) if peers is None else peers,'rows':all_rows}


def ranking_summary(payload):
    result={}
    for i,t in enumerate(payload['company_studies']):
        result[t]=company_ranking(payload,t,year='all')
        if (i+1)%24==0:
            print(f'Raw-indicator rankings: {i+1}/{len(payload["company_studies"])} companies',flush=True)
    return {'features':FEATURES,'default_year':'all','default_window':'364','default_basis':'absolute','companies':result}
