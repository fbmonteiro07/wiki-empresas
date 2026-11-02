"""Materialize explicitly selected research emails from connector responses; no mailbox changes."""
from pathlib import Path
import sys,json,hashlib,datetime,re
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path.cwd();DATA=ROOT/'_wiki/_data/financials';OUT=DATA/'email_review_2026-11-01';OUT.mkdir(exist_ok=True)
allowed=set('JPM SPGI MCO BX KKR GS V MA APO HOOD COIN'.split())
print('Ready for selected email records',flush=True)
for line in sys.stdin:
 if line.strip()=='END':break
 x=json.loads(line);assert set(x['tickers'])<=allowed
 digest=hashlib.sha256(x['id'].encode()).hexdigest()[:12];p=OUT/(digest+'.json')
 if p.exists():
  old=json.loads(p.read_text(encoding='utf-8'))
  assert old==x,'Existing retrieval differs; preserve before updating'
 else:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Saved '+digest,flush=True)
print('Selected email ingestion finished',flush=True)
