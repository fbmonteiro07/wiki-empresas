import sys
sys.path.insert(0,'automation/financials')
from collect_sources import ROOT,fetch
from prepare_research import Reader
urls=[('2026-09-28_Helix_Samsung_commitment','https://www.helixdi.com/news-insights/samsung-commits-1-billion-to-helix-digital-infrastructure-to-support-global-ai-infrastructure-buildout/','Helix / KKR','2026-09-28'),('2026-09-29_Samsung_Helix','https://news.samsung.com/global/samsung-to-invest-usd-1-billion-in-ai-infrastructure-company-helix','Samsung Global Newsroom','2026-09-29')]
for name,url,source,date in urls:
 p=ROOT/'KKR/research'/f'{name}.html';b=fetch(url);p.write_bytes(b);r=Reader();r.feed(b.decode('utf-8','replace'));s=r.text();p.with_suffix('.md').write_text(f'# {source} — Samsung investment in Helix\n\n- Source: {source}\n- Publication date: {date}\n- Original URL: {url}\n- Recorded: 2026-10-31\n- Fidelity: Company web announcement, original HTML retained.\n\n'+s,encoding='utf-8');print(name,len(s))
