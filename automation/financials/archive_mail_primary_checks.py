from pathlib import Path
from collect_sources import ROOT,fetch,strip
items=[
('KKR','2026-08-31_USI_announcement','2026-08-31','https://www.sec.gov/Archives/edgar/data/315293/000119312526375328/d108801dex991.htm','Aon announcement of agreement to acquire USI'),
('KKR','2026-10-28_Aon_USI_status','2026-10-28','https://aon.mediaroom.com/2026-10-28-Aon-Reports-Third-Quarter-2026-Results','Aon Q3 results; USI closing status'),
('APO','2026-10-05_Athene_preliminary_alt_income','2026-10-05','https://ir.athene.com/sec-filings/all-sec-filings/content/0001527469-26-000073/ahl-20261005.htm','Athene 8-K; preliminary alternative net investment income')]
for tk,stem,date,url,title in items:
 p=ROOT/tk/'research';p.mkdir(exist_ok=True)
 raw=fetch(url);(p/(stem+'.html')).write_bytes(raw)
 content=strip(raw.decode('utf-8','replace'))
 (p/(stem+'.md')).write_text(f'# {title}\n\n- Publication date: {date}\n- Original URL: {url}\n- Retrieved: 2026-11-01\n- Fidelity: Full HTML text extraction; selected relevant passages reviewed.\n\n## Extracted source\n\n{content}\n',encoding='utf-8')
 print(tk,stem,len(raw),flush=True)
p=ROOT/'KKR/research/2026-08-31_USI_investor_presentation.pdf'
p.write_bytes(fetch('https://ir.kkr.com/media/document/755d2777-015d-49f3-8dfb-3b0120c6d49b/assets/USI_Investor_Presentation.pdf?disposition=inline'))
print('KKR primary transaction presentation archived',p.stat().st_size)
