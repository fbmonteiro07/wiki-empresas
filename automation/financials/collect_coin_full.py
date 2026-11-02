import sys,json,re,hashlib
from pathlib import Path
from collect_sources import ROOT,DATA,fetch,write_json
from prepare_research import Reader
sys.stdout.reconfigure(encoding='utf-8')
urls=['https://www.fool.com/earnings/call-transcripts/2026/10/30/coinbase-coin-q3-2026-earnings-call-transcript/','https://stockanalysis.com/stocks/coin/transcripts/720306-q3-2026/']
records=[]
for url in urls:
    r=dict(ticker='COIN',source_url=url,call_date='2026-10-29',fiscal_period='Q3 2026',recorded_date='2026-10-31',analytical_review='not_yet_reviewed')
    try:
        b=fetch(url,tries=1);reader=Reader();reader.feed(b.decode('utf-8','replace'));text=reader.text()
        idx=text.find('Full Conference Call Transcript')
        if idx<0: idx=text.find('Shan Aggarwal')
        if idx<0: raise ValueError('No transcript opening')
        text=text[idx:]
        for marker in ['More COIN analysis','Read the original article','Premium Investing Services','Related Stocks']:
            if marker in text: text=text.split(marker)[0]
        if len(text)<16000 or 'Alesia' not in text or 'Brian' not in text: raise ValueError('Short or invalid call')
        rawpath=ROOT/'COIN/transcripts/originals/COIN_Q3_2026_public_call.html';rawpath.write_bytes(b)
        path=ROOT/'COIN/transcripts/COIN_Q3-2026-earnings_2026-10-29.md'
        path.write_text('# Coinbase Global — Q3 2026 earnings Q&A — 2026-10-29\n\n- **Source:** '+url+'\n- **Call date:** 2026-10-29\n- **Publication date:** 2026-10-30\n- **Retrieved:** 2026-10-31\n- **Fidelity:** Public third-party transcript, full served call text; company presentation separately archived. Original web HTML retained.\n\n## Transcript\n\n'+text,encoding='utf-8')
        r.update(status='archived',path=path.relative_to(ROOT).as_posix(),raw_path=rawpath.relative_to(ROOT).as_posix(),words=len(text.split()),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        records.append(r);print('ARCHIVED',len(text),text[-550:]);break
    except Exception as e: r.update(status='failed',error=str(e));records.append(r);print('FAILED',url,str(e))
write_json(DATA/'COIN_supplemental_transcripts.json',{'as_of':'2026-10-31','records':records})

