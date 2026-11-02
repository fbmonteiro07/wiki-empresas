"""Read source windows with exact provenance; logs emitted scope, not full-document review."""
import sys,re,json,datetime,argparse
from pathlib import Path
from collect_sources import ROOT,DATA
sys.stdout.reconfigure(encoding='utf-8')
p=argparse.ArgumentParser();p.add_argument('glob');p.add_argument('--pattern',default='');p.add_argument('--length',type=int,default=5000);p.add_argument('--last',action='store_true');a=p.parse_args()
for path in sorted(ROOT.glob(a.glob)):
    raw=path.read_text(encoding='utf-8-sig',errors='replace')
    text=re.sub(r'<https?://[^>]*>','',raw)
    text=re.sub(r'https?://\S+','[URL in source]',text)
    text=re.sub(r'\s+',' ',text)
    matches=list(re.finditer(a.pattern,text,re.I)) if a.pattern else []
    start=max(0,(matches[-1 if a.last else 0].start()-150)) if matches else 0
    out=text[start:start+a.length]
    print('\nSOURCE',path.relative_to(ROOT).as_posix(),'OFFSET',start,'\n'+out,flush=True)
    with (DATA/'review_passages.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps({'path':path.relative_to(ROOT).as_posix(),'mode':'context window','terms':a.pattern,'start':start,'characters_emitted':len(out),'source_characters':len(raw),'reviewed_at':datetime.datetime.now().isoformat()})+'\n')

