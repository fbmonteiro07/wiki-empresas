import sys,json,re,datetime,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from collect_sources import ROOT,DATA,fetch,write_json
sys.stdout.reconfigure(encoding="utf-8")
# Deduplicate identical discoveries and correct a source-label error against the issuer PDF.
for p in DATA.glob('*_transcripts.json'):
    d=json.loads(p.read_text(encoding='utf-8')); seen=set(); out=[]
    for r in d.get('records',[]):
        key=r.get('path') or r.get('source_url','').split('?')[0].split('#')[0]
        if key in seen: continue
        seen.add(key)
        if r.get('ticker')=='KKR' and r.get('fiscal_period')=='Q4 2025' and r.get('date')=='2026-02-27':
            old=ROOT/r['path']; new=old.with_name(old.name.replace('2026-02-27','2026-02-05'))
            text=old.read_text(encoding='utf-8')
            text=text.replace('— 2026-02-27','— 2026-02-05').replace('**Call date:** 2026-02-27','**Call date:** 2026-02-05')
            text=text.replace('## Participants','**Date correction recorded 2026-10-31:** MarketBeat URL is dated 2026-02-27; the company-hosted corrected transcript dates the Q4 2025 call 2026-02-05. The source URL is preserved.\n\n## Participants')
            new.write_text(text,encoding='utf-8')
            old.unlink()
            r.update(path=new.relative_to(ROOT).as_posix(),date='2026-02-05',source_date_error='MarketBeat URL dated 2026-02-27; issuer transcript says 2026-02-05',sha256=hashlib.sha256(text.encode()).hexdigest())
        out.append(r)
    d['records']=out;write_json(p,d)
# Add the old Apollo registrant only through its pre-combination period.
cik='0001411494'; d=json.loads(fetch(f'https://data.sec.gov/submissions/CIK{cik}.json')); blocks=[d['filings']['recent']]
for x in d['filings'].get('files',[]):
    if x.get('filingFrom','')<='2022-03-01' and x.get('filingTo','')>='2021-10-31':
        blocks.append(json.loads(fetch('https://data.sec.gov/submissions/'+x['name'])))
records=[]
for b in blocks:
    for i,form in enumerate(b['form']):
        date=b['filingDate'][i]; period=b['reportDate'][i]
        if form not in ['10-K','10-Q','10-K/A','10-Q/A'] or not '2021-10-31'<=date<='2022-03-01' or period>'2021-12-31': continue
        acc=b['accessionNumber'][i];doc=b['primaryDocument'][i];url=f'https://www.sec.gov/Archives/edgar/data/1411494/{acc.replace("-","")}/{doc}'
        dest=ROOT/'APO'/'predecessor'/f'APO_PREDECESSOR_{form.replace("/","-")}_{date}_{acc}.html';dest.parent.mkdir(exist_ok=True)
        blob=dest.read_bytes() if dest.exists() else fetch(url);dest.write_bytes(blob)
        records.append(dict(ticker='APO',company='Apollo Asset Management, Inc. (pre-combination registrant)',cik=cik,form=form,filing_date=date,period_end=period,accession=acc,source_url=url,path=dest.relative_to(ROOT).as_posix(),status='archived',bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),analytical_review='not_yet_reviewed',basis='Predecessor standalone asset manager; not combined Apollo/Athene',recorded_date='2026-10-31'))
write_json(DATA/'APO_predecessor_filings.json',{'as_of':'2026-10-31','records':records})
print('Predecessor archived',len(records))

