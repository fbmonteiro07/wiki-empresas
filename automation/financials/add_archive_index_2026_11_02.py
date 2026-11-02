"""Add the 2026-11-02 Financials names (MSCI, EFX, TRU) to the root archive INDEX.md, same format as update_archive_index.py."""
from pathlib import Path
import json,re
root=Path.cwd();data=root/'_wiki/_data/financials';tks=['MSCI','EFX','TRU']
counts={}
for t in tks:
 files=[x for x in json.loads((data/f'{t}_filings.json').read_text(encoding='utf-8-sig'))['records'] if x['status']=='archived']
 tx=list((root/t/'transcripts').glob('*.md'));counts[t]=(len(files),len(tx),0,0,0)
p=root/'INDEX.md';s=p.read_text(encoding='utf-8-sig');m=re.search(r'^\| Ticker \|.*?^\| \*\*TOTAL\*\*[^\n]*',s,re.M|re.S);assert m
old={}
for ln in m[0].splitlines():
 q=re.match(r'^\|\s*([A-Z][A-Z0-9.]*)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|',ln)
 if q:old[q[1]]=tuple(int(q[i]) for i in range(2,7))
assert not any(t in old for t in tks);old.update(counts);total=tuple(sum(v[i] for v in old.values()) for i in range(5))
table=['| Ticker | SEC | Transcripts | Decks | Equity calls | Briefings |','|---|---|---|---|---|---|']+[f'| {t} | '+' | '.join(str(x) for x in old[t])+' |' for t in sorted(old)]+['| **TOTAL** | '+' | '.join(f'**{n}**' for n in total)+' |']
s=s[:m.start()]+'\n'.join(table)+s[m.end():]
s=re.sub(r'^_\d+ companies[^\n]*',f'_{len(old)} companies · {total[0]} SEC filings · {total[1]} transcript documents · {total[2]} presentations · {total[3]} equity-call links · {total[4]} legacy briefing datapoints. Financials added 2026-10-31 (MSCI, EFX, TRU on 2026-11-02); existing-company counts retained._',s,count=1,flags=re.M)
s=s.replace('**Financials added 2026-10-31:**','**Financials added 2026-10-31 (MSCI, EFX, TRU on 2026-11-02):**',1)
s+='\n## Financials — source inventories added 2026-11-02\n\n'
for t,c in counts.items():s+=f'### {t}\n\n- **Wiki:** [{t} synthesis](_wiki/{t}.md).\n- **Archive:** {c[0]} SEC filings and {c[1]} transcript documents; [complete dated inventory]({t}/research/SOURCES.html) / [Markdown]({t}/SOURCES.md).\n- **Earnings and commentary:** separate company releases/supplements, cached sell-side excerpts and source-quality labels in the inventory.\n\n'
p.write_bytes(s.encode('utf-8'));print('Archive index updated:',len(old),'companies',total)
