from pathlib import Path
import json,re
from collections import Counter
root=Path.cwd();data=root/'_wiki/_data/financials';tks=['JPM','SPGI','MCO','BX','KKR','GS','V','MA','APO','HOOD','COIN']
counts={}
for t in tks:
 files=[]
 for f in [data/f'{t}_filings.json',data/f'{t}_predecessor_filings.json']:
  if f.exists():files += [x for x in json.loads(f.read_text(encoding='utf-8-sig'))['records'] if x['status']=='archived']
 tx=list((root/t/'transcripts').glob('*.md'));counts[t]=(len(files),len(tx),0,0,0)
p=root/'INDEX.md';s=p.read_text(encoding='utf-8-sig');m=re.search(r'^\| Ticker \|.*?^\| \*\*TOTAL\*\*[^\n]*',s,re.M|re.S);assert m
old={}
for ln in m[0].splitlines():
 q=re.match(r'^\|\s*([A-Z][A-Z0-9.]*)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|',ln)
 if q:old[q[1]]=tuple(int(q[i]) for i in range(2,7))
assert not any(t in old for t in tks);old.update(counts);total=tuple(sum(v[i] for v in old.values()) for i in range(5))
table=['| Ticker | SEC | Transcripts | Decks | Equity calls | Briefings |','|---|---|---|---|---|---|']+[f'| {t} | '+' | '.join(str(x) for x in old[t])+' |' for t in sorted(old)]+['| **TOTAL** | '+' | '.join(f'**{n}**' for n in total)+' |']
s=s[:m.start()]+'\n'.join(table)+s[m.end():]
s=re.sub(r'^_\d+ companies[^\n]*',f'_{len(old)} companies · {total[0]} SEC filings · {total[1]} transcript documents · {total[2]} presentations · {total[3]} equity-call links · {total[4]} legacy briefing datapoints. Financials added 2026-10-31; existing-company counts retained._',s,count=1,flags=re.M)
notice='\n**Financials added 2026-10-31:** [overview](_wiki/themes/financials.md) · [coverage ledger](_wiki/_meta/financials-coverage.md). Transcript totals count source documents, including duplicate company/public versions; the ledger separately counts unique quarters. Financials cached commentary is listed in each source inventory and is not counted as legacy briefing datapoints.\n'
s=s.replace('\n## Summary\n',notice+'\n## Summary\n',1)
s+='\n## Financials — source inventories added 2026-10-31\n\n'
for t,c in counts.items():s+=f'### {t}\n\n- **Wiki:** [{t} synthesis](_wiki/{t}.md).\n- **Archive:** {c[0]} SEC filings and {c[1]} transcript documents; [complete dated inventory]({t}/research/SOURCES.html) / [Markdown]({t}/SOURCES.md).\n- **Earnings and commentary:** separate company releases/supplements, cached sell-side research and source-quality labels in the inventory.\n\n'
p.write_text(s,encoding='utf-8');print('Archive index updated:',len(old),'companies',total)
