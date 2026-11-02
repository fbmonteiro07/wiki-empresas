"""Print source passages for analyst review, and log only passages actually emitted."""
import argparse,datetime,json,re,sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from collect_sources import ROOT,DATA,CO
p=argparse.ArgumentParser(); p.add_argument('ticker'); p.add_argument('kind',choices=['release','call','commentary','filing']); p.add_argument('--terms',default=''); p.add_argument('--limit',type=int,default=16000); p.add_argument('--date',default=''); a=p.parse_args()
tk=a.ticker
if a.kind=='release':
    paths=sorted((ROOT/tk/'earnings').glob('*.txt'),reverse=True)
elif a.kind=='call':
    paths=sorted((ROOT/tk/'transcripts').glob(tk+'_Q*.md'),key=lambda x:x.name[-13:],reverse=True)
elif a.kind=='commentary':
    paths=sorted((ROOT/tk/'commentary').glob('*.md'),reverse=True)
else:
    paths=sorted((ROOT/tk/'filings_text').glob('*10-K*.txt'),reverse=True)[:1]+sorted((ROOT/tk/'filings_text').glob('*10-Q*.txt'),reverse=True)[:1]
if a.date: paths=[x for x in paths if a.date in x.name]
limit=a.limit
logs=[]
for path in paths:
    if limit<=0: break
    s=path.read_text(encoding='utf-8',errors='replace')
    if a.kind=='commentary':
        s=re.sub(r'<https?://[^>]+>','',s)
        s=re.sub(r'https?://\S+','[source link in archived note]',s)
        s=re.sub(r'\n[ \t]*\n+', '\n\n',s)
        s=re.sub(r'[ \t]+',' ',s)
    if a.terms:
        blocks=re.split(r'\n\s*\n',s)
        chosen=[b for b in blocks if re.search(a.terms,b,re.I)]
        text='\n\n'.join(chosen)
    else: text=s
    text=text[:limit]
    if not text.strip(): continue
    print('\nSOURCE',path.relative_to(ROOT).as_posix(),'\n'+text,flush=True)
    logs.append({'path':path.relative_to(ROOT).as_posix(),'mode':'selected passages' if a.terms else 'opening text','terms':a.terms,'characters_emitted':len(text),'source_characters':len(s),'reviewed_at':datetime.datetime.now().isoformat()})
    limit-=len(text)
with (DATA/'review_passages.jsonl').open('a',encoding='utf-8') as f:
    for row in logs: f.write(json.dumps(row)+'\n')

