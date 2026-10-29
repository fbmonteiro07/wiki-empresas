"""Frozen train-2024/25 pair selection, descriptive validation on previously seen 2026."""
import hashlib
import itertools
import json
import sentiment_indicator_ranking as raw
import sentiment_relative_backtest as rel

FEATURES=list(raw.FEATURES)
COST=.002  # ESTIMATE sum of one-way rates: 10bp entry + 10bp exit.
THRESHOLD=.70


def rules():
    return [{'features':list(fs),'signs':list(ss),'id':'+'.join(f+('↑' if s==1 else '↓') for f,s in zip(fs,ss))}
            for fs in itertools.combinations(FEATURES,2) for ss in itertools.product([1,-1],repeat=2)]


def singles():
    return [{'features':[f],'signs':[s],'id':f+('↑' if s==1 else '↓')} for f in FEATURES for s in [1,-1]]


def usable(e,axis):
    return rel.valid(e.get('return')) and all(rel.valid(e['raw_percentiles'][f][axis]) for f in FEATURES)


def position(e,rule,axis):
    if not usable(e,axis):return None
    scores=[e['raw_percentiles'][f][axis] if s==1 else 1-e['raw_percentiles'][f][axis] for f,s in zip(rule['features'],rule['signs'])]
    return int(sum(scores)/len(scores)>=THRESHOLD)


def outcome(e,rule,axis,cost=COST):
    p=position(e,rule,axis)
    return None if p is None else p*((1+e['return'])*(1-cost/2)/(1+cost/2)-1)


def summary(events,rule,axis,cost=COST):
    es=[e for e in events if usable(e,axis)];pos=[position(e,rule,axis) for e in es]
    net=[outcome(e,rule,axis,cost) for e in es];gross=[p*e['return'] for p,e in zip(pos,es)]
    return {'scheduled':len(events),'n':len(es),'active':sum(pos),'cash':len(es)-sum(pos),
            'exposure':sum(pos)/len(es) if es else None,'net':rel.avg(net),'gross':rel.avg(gross),
            'buy_hold':rel.avg([e['return'] for e in es]),'always_active_net':rel.avg([(1+e['return'])*(1-cost/2)/(1+cost/2)-1 for e in es]),'first':es[0]['signal'] if es else None,'last':es[-1]['signal'] if es else None,
            'thin_peers':sum(e['peer_n']<3 for e in es) if axis=='peer' else 0}


def train_candidate(train,rule,axis):
    s=summary(train,rule,axis)
    years={y:summary([e for e in train if e['signal'][:4]==y],rule,axis) for y in ['2024','2025']}
    supported=s['n']>=20 and s['active']>=4 and s['cash']>=4 and all(v['active']>=2 and v['cash']>=2 for v in years.values())
    return {'rule':rule,'train':s,'train_years':years,'eligible':supported}


def choose(train,axis):
    """Receives training events ONLY. Test values cannot influence candidate admission or ranking."""
    assert all(e['signal'][:4] in ['2024','2025'] and e['exit']<'2026-01-01' for e in train)
    candidates=[train_candidate(train,r,axis) for r in rules()]
    single_candidates=[train_candidate(train,r,axis) for r in singles()]
    # Stable predeclared enumeration resolves ties; never inspect validation return or sample.
    order=lambda c:-(c['train']['net'] if c['train']['net'] is not None else -1e99)
    pairs=[]
    for fs in itertools.combinations(FEATURES,2):
        eligible=[c for c in candidates if c['rule']['features']==list(fs) and c['eligible']]
        if eligible:pairs.append(sorted(eligible,key=order)[0])
    pairs.sort(key=order)
    eligible_singles=sorted([c for c in single_candidates if c['eligible']],key=order)
    return {'pairs':pairs,'winner':pairs[0] if pairs else None,'single':eligible_singles[0] if eligible_singles else None,
            'candidate_count':len(candidates),'eligible_candidates':sum(c['eligible'] for c in candidates),'eligible_singles':len(eligible_singles)}


def mean_bootstrap(values,h,multiplier):
    observed=rel.avg([v for v in values if v is not None]);n=len(values)
    if not n or observed is None:return {'ci':None,'p':1.,'p_mc':[1.,1.],'valid_draws':0,'draws':0,'tail_count':0}
    lengths,starts=raw.draw_starts(n,h,multiplier)
    blocks={length:[(sum(values[(i+j)%n] or 0. for j in range(length)),sum(values[(i+j)%n] is not None for j in range(length))) for i in range(n)] for length in set(lengths)}
    dist=[]
    for row in starts:
        s=c=0
        for i,length in zip(row,lengths):
            a,b=blocks[length][i];s+=a;c+=b
        if c:dist.append(s/c)
    dist.sort();valid=len(dist)>=1800
    tails=sum(abs(v-observed)+1e-12>=abs(observed) for v in dist)
    return {'ci':[dist[int(len(dist)*.025)],dist[min(len(dist)-1,int(len(dist)*.975))]] if valid else None,
            'p':(1+tails)/(len(dist)+1) if valid else 1.,'p_mc':raw.wilson(tails,len(dist)) if valid else [1.,1.],
            'valid_draws':len(dist),'draws':2000,'tail_count':tails}


def contrast(test,pair,other,axis,h):
    a=summary(test,pair,axis);b=summary(test,other,axis)
    values=[outcome(e,pair,axis)-outcome(e,other,axis) if usable(e,axis) else None for e in test]
    valid=[v for v in values if v is not None];increment=rel.avg(valid)
    support=all(s['n']>=20 and s['active']>=5 and s['cash']>=5 for s in [a,b])
    empty={'ci':None,'p':1.,'p_mc':[1.,1.],'valid_draws':0,'draws':0,'tail_count':0}
    boot=mean_bootstrap(values,h,1) if support else dict(empty);long=mean_bootstrap(values,h,2) if support else dict(empty)
    loo=[(sum(valid)-v)/(len(valid)-1) for v in valid] if len(valid)>1 else []
    positive=bool(boot['ci'] and long['ci'] and boot['ci'][0]>0 and long['ci'][0]>0)
    return {'rule':other,'comparison':b,'increment':increment,'support':support,'bootstrap':boot,'long_block':long,
            'p_raw':max(boot['p'],long['p']),'loo_min':min(loo) if loo else None,'positive_intervals':positive,
            'sensitivity':{str(bp):summary(test,pair,axis,bp/10000)['net']-summary(test,other,axis,bp/10000)['net'] if valid else None for bp in [0,20,50]},
            'values':values}


def experiment(ctx,t,axis,h,cutoff):
    events=ctx.raw_events(t,h,'364',None,cutoff)
    train=[e for e in events if e['signal'][:4] in ['2024','2025'] and e['exit']<'2026-01-01']
    test=[e for e in events if e['signal'][:4]=='2026']
    selected=choose(train,axis)
    result={'axis':axis,'horizon':h,'selection':selected,'test':None,'contrasts':[],'ledger':[]}
    # All six pair identities/orientations frozen in training; table order never uses 2026.
    for candidate in selected['pairs']:candidate['validation']=summary(test,candidate['rule'],axis)
    if not selected['winner'] or not selected['single']:return result
    pair=selected['winner']['rule'];single=selected['single']['rule']
    components=[{'features':[f],'signs':[s],'id':f+('↑' if s==1 else '↓')} for f,s in zip(pair['features'],pair['signs'])]
    result['test']=summary(test,pair,axis)
    for label,other in zip(['best_single','component_1','component_2'],[single,*components]):
        c=contrast(test,pair,other,axis,h);c['benchmark']=label;result['contrasts'].append(c)
    for e in events:
        result['ledger'].append({k:e[k] for k in ['signal','cutoff','entry','exit','return']}|{
            'period':'train' if e['signal']<'2026-01-01' else 'validation','eligible':usable(e,axis),
            'pair_position':position(e,pair,axis),'single_position':position(e,single,axis),
            'pair_net':outcome(e,pair,axis),'single_net':outcome(e,single,axis),
            'component_positions':[position(e,r,axis) for r in components],
            'raw_percentiles':{f:e['raw_percentiles'][f][axis] for f in FEATURES}})
    return result


def company(payload,t,ctx=None):
    ctx=ctx or raw.RawContext(payload)
    cutoff=max(r['cutoff'] for r in payload['snapshots'][payload['meta']['signal_asof']])
    experiments=[experiment(ctx,t,a,h,cutoff) for a in ['own','peer'] for h in [5,20]]
    # Fixed12 hypotheses, including unavailable choices as p=1.
    slots=[(e,c) for e in experiments for c in (e['contrasts'] or [None]*3)]
    ps=raw.holm([c['p_raw'] if c else 1. for e,c in slots])
    upper=raw.holm([max(c['bootstrap']['p_mc'][1],c['long_block']['p_mc'][1]) if c else 1. for e,c in slots])
    for (e,c),p,u in zip(slots,ps,upper):
        if c:c['p_holm']=p;c['p_holm_mc_upper']=u;c['passes']=bool(c['support'] and c['positive_intervals'] and p<=.05 and u<=.05 and c['loo_min'] is not None and c['loo_min']>0)
    for e in experiments:
        e['passes']=bool(e['contrasts'] and all(c['passes'] for c in e['contrasts']))
        e['status']='No train-qualified pair' if not e['selection']['winner'] else 'No train-qualified single benchmark' if not e['selection']['single'] else 'Insufficient validation sample' if not all(c['support'] for c in e['contrasts']) else 'Passes local incremental screen' if e['passes'] else 'Incremental value unconfirmed'
        e['beats_all_observed']=bool(e['contrasts'] and all(c['increment'] is not None and c['increment']>0 for c in e['contrasts']))
    return {'ticker':t,'cutoff':cutoff,'experiments':experiments}


def selection_document(companies):
    return {t:[{'axis':e['axis'],'horizon':e['horizon'],'pair':e['selection']['winner']['rule'] if e['selection']['winner'] else None,
                'single':e['selection']['single']['rule'] if e['selection']['single'] else None,
                'pair_order':[c['rule'] for c in e['selection']['pairs']]} for e in p['experiments']] for t,p in companies.items()}


def research(payload):
    ctx=raw.RawContext(payload);companies={}
    for i,t in enumerate(payload['company_studies']):
        companies[t]=company(payload,t,ctx)
        if (i+1)%24==0:print(f'Frozen pair tests: {i+1}/96',flush=True)
    selections=selection_document(companies)
    return {'train':'2024–2025','validation':'2026','cost_roundtrip':COST,'threshold':THRESHOLD,'window':'364',
            'selection_hash':hashlib.sha256(json.dumps(selections,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
            'selections':selections,'companies':companies}
