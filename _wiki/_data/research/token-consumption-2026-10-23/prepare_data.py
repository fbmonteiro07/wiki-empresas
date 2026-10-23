"""Prepare auditable source aggregates and independent expectations, not XLSX authoring."""
import calendar, collections, datetime, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
src=json.loads((HERE/'arr_source.json').read_text(encoding='utf-8'))
study=HERE.parent/'token-pricing-2026-10-23'
p=json.loads((study/'raw/tokenPrices.json').read_text(encoding='utf-8'))
v=json.loads((study/'raw/tokenVolumes.json').read_text(encoding='utf-8'))
px={(r['usage_date'],r['model_maker'],r['token_type']):r for r in p}
makers=('anthropic','openai')
def fam(m,n):
    n=n.lower()
    if m=='anthropic':return next((f.title() for f in ('opus','sonnet','haiku','fable','mythos') if f in n),'Other')
    if 'embedding' in n or 'moderation' in n:return 'Embedding/moderation'
    if any(x in n for x in ('realtime','audio','tts','whisper','transcribe','image','sora','dall')):return 'Media/audio'
    if 'astra' in n:return 'Astra'
    if any(x in n for x in ('luna','mini','nano')):return 'Luna/mini/nano'
    if 'sol' in n:return 'Sol'
    if 'terra' in n:return 'Terra'
    return 'Other text/legacy'
cols=['P','Q','R','S','T','U','V','W','X','Y','Z','AA']
arr={}
for m,gr,nr in [('anthropic',98,84),('openai',95,81)]:
    arr[m]={k:[src['sheets']['ARR Tracker'][c+str(r)]['value'] for c in cols] for k,r in [('gross',gr),('net',nr)]}
    arr[m]['cells']={k:[c+str(r) for c in cols] for k,r in [('gross',gr),('net',nr)]}
arr['anthropic']['api_share']=src['sheets']['Anthropic']['AB11']['value']
arr['openai']['api_share']=src['sheets']['OpenAI']['AB29']['value']
assert all(isinstance(x,(int,float)) and x>0 for m in makers for k in ('gross','net') for x in arr[m][k])
models=collections.defaultdict(lambda:collections.defaultdict(dict))
for r in v:
    if r['model_maker'] in makers and r['period_end'].startswith('2026'):
        models[r['period_end'],r['model_maker']][r['series_key']][r['metric_key']]=r['metric_value']
weekly=[];fg=collections.defaultdict(lambda:[0,0,0])
for (dt,m),mm in sorted(models.items()):
    month=int(dt[5:7]);q=px[dt,m,'all_tokens'];T=S=M=Z=0
    for n,x in mm.items():
        t=x.get('token_volume',0);s=x.get('token_spend');T+=t;S+=s or 0
        if s is None:M+=t
        elif t==0:Z+=s
        f=fg[m,month,fam(m,n)];f[0]+=t
        if s is not None and t>0:f[1]+=t;f[2]+=s
    weekly.append({'date':dt,'provider':m,'month':month,'N':q['token_count_7d'],'C':q['token_cost_usd_7d'],'T':T,'S':S,'missing':M,'zero_token_cost':Z})
families={'anthropic':['Opus','Sonnet','Haiku','Fable','Mythos','Other'], 'openai':['Luna/mini/nano','Sol','Terra','Astra','Other text/legacy','Embedding/moderation','Media/audio']}
family_rows=[{'provider':m,'month':month,'family':f,'total_tokens':fg[m,month,f][0],'matched_tokens':fg[m,month,f][1],'matched_cost':fg[m,month,f][2]} for m in makers for month in range(1,11) for f in families[m]]
monthly=[]
for m in makers:
    for month in range(1,13):
        used=min(month,10);rr=[r for r in weekly if r['provider']==m and r['month']==used]
        C=sum(r['C'] for r in rr);N=sum(r['N'] for r in rr);T=sum(r['T'] for r in rr);S=sum(r['S'] for r in rr);M=sum(r['missing'] for r in rr);Z=sum(r['zero_token_cost'] for r in rr)
        pub=C/N*1e6;matched=(S-Z)/(T-M)*1e6;floor=min(pub,matched)
        gross=arr[m]['gross'][month-1]/1000;net=arr[m]['net'][month-1]/1000
        api_gross=gross*arr[m]['api_share'] if m=='anthropic' else net*arr[m]['api_share']+gross-net
        monthly.append({'provider':m,'month':month,'price_month':used,'gross_arr_busd':gross,'net_arr_busd':net,'api_gross_arr_busd':api_gross,'published_price':pub,'matched_price':matched,'minimum_reference':floor,'base_gross_tokens_Q_month':gross/12/pub,'reference_gross_tokens_Q_month':gross/12/floor,'api_gross_tokens_Q_month':api_gross/12/pub,'gap':T/N-1,'coverage':(T-M)/T,'weeks':len(rr),'start':(datetime.date.fromisoformat(rr[0]['date'])-datetime.timedelta(days=6)).isoformat(),'end':rr[-1]['date'],'price_status':'Full weekly sample' if month<10 else 'Partial through Oct 11' if month==10 else 'ESTIMATE: October held flat'})
out={'asof':'2026-10-23','source':{k:src[k] for k in ['source','sha256','file_modified']},'arr':arr,'weekly':weekly,'families':families,'family_rows':family_rows,'monthly_expected':monthly,'method':'Monthly token-weighted means over nonoverlapping weeks ending in month; not exact calendar-month billing. October through Oct11; November/December carry October price/mix. Full-ARR and API-only equivalents are conditional scenarios, not measured company consumption.'}
(HERE/'model_inputs.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'weekly_rows':len(weekly),'family_rows':len(family_rows),'october':[r for r in monthly if r['month']==10]},indent=2))
