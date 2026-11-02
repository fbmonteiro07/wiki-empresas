import sys,re,json,html
from pathlib import Path
from collect_sources import ROOT,DATA,fetch,write_json
sys.stdout.reconfigure(encoding='utf-8')
url='https://www.marketscreener.com/news/coinbase-global-third-quarter-2026-earnings-call-transcript-ce785fdad08ef622'
blob=fetch(url);raw=blob.decode('utf-8','replace')
dest=DATA/'discovery'/'COIN_Q3_2026_marketscreener.html';dest.write_bytes(blob)
links=sorted(set(html.unescape(x) for x in re.findall(r'https?[^\s"<>]+',raw) if '.pdf' in x or 'content_files' in x))
print(json.dumps(links,indent=2))

