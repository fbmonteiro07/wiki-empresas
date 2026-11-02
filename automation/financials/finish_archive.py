import sys,json,re,hashlib
from pathlib import Path
from collect_sources import ROOT,DATA,fetch,write_json,transcript
from prepare_research import Reader
sys.stdout.reconfigure(encoding='utf-8')
url='https://www.helixdi.com/news-insights/kkr-launches-helix-digital-infrastructure-to-finance-and-deliver-the-next-generation-of-ai-infrastructure/'
p=ROOT/'KKR/research/2026-06-11_Helix_launch.html';p.parent.mkdir(exist_ok=True)
b=p.read_bytes() if p.exists() else fetch(url);p.write_bytes(b)
r=Reader();r.feed(b.decode('utf-8','replace'));body=r.text()
m=p.with_suffix('.md');m.write_text('# Helix Digital Infrastructure launch — KKR, KIA, NVIDIA and Vistra\n\n- Source: Helix / KKR company announcement\n- Event and publication date: 2026-06-11\n- Recorded: 2026-10-31\n- Original URL: '+url+'\n- Fidelity: Company web release; original HTML archived alongside this text extraction.\n\n'+body,encoding='utf-8')
print('HELIX',len(body))
try:
 row=transcript('KKR','https://www.marketbeat.com/earnings/reports/2024-10-24-kkr-co-inc-stock/')
 f=DATA/'KKR_transcripts.json';j=json.loads(f.read_text(encoding='utf-8-sig'));j['records']=[x for x in j['records'] if x.get('path')!=row.get('path')];j['records'].append(row);write_json(f,j);print('KKR_BACKFILL',row['status'],row.get('words'))
except Exception as e: print('KKR_BACKFILL_FAILED',str(e))
p=ROOT/'COIN/transcripts/COIN_Q3-2026-earnings_2026-10-29.md';s=p.read_text(encoding='utf-8-sig')
# The full call precedes article recommendations and advertising.
for marker in ['Read Next','About the Author','About The Author','Read more about','Related Articles']:
 if marker in s:
  n=s.index(marker)
  if n>18000: s=s[:n].rstrip()+'\n';break
p.write_text(s,encoding='utf-8')
f=DATA/'COIN_supplemental_transcripts.json';j=json.loads(f.read_text(encoding='utf-8-sig'))
for x in j['records']:
 if x.get('status')=='archived': x.update(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),words=len(s.split()),footer_trimmed=True)
write_json(f,j);print('COIN_TAIL',s[-600:])
p=ROOT/'HOOD/research/ROBINHOOD_20260901_0411.txt'
s=p.read_text(encoding='utf-8-sig')
p.with_suffix('.md').write_text('# Robinhood — upgrading to Overweight — Morgan Stanley\n\n- Source: Morgan Stanley, Michael Cyprys / Barron Thomas\n- Report date: 2026-09-01\n- Original user archive: ../../_inbox/_done/ROBINHOOD_20260901_0411.pdf\n- Rendered original: ../../relat%C3%B3rios%20bons/ROBINHOOD_20260901_0411.html\n- Fidelity: Full PDF text extraction, 32 pages; original report retained. The first two pages were reviewed for the initiation rationale, rating and price target.\n- Recorded: 2026-10-31\n\n'+s,encoding='utf-8')
print('HOOD_REPORT',len(s))
