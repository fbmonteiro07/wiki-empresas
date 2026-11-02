"""Archive BlackRock's pre-reorganization registrant filings (2026-11-02), same pattern as the APO predecessor block in repair_archive.py.

BlackRock moved to a new holding company (CIK 0002012383) when the GIP acquisition closed on 2024-10-01; the
pre-2024-Q3 10-K/10-Qs sit under the old registrant (CIK 0001364742, since renamed BlackRock Finance, Inc.).
"""
import json,hashlib
from collect_sources import ROOT,DATA,fetch,write_json
cik='0001364742'; d=json.loads(fetch(f'https://data.sec.gov/submissions/CIK{cik}.json')); blocks=[d['filings']['recent']]
for x in d['filings'].get('files',[]):
    if x.get('filingTo','')>='2021-10-31' and x.get('filingFrom','')<='2024-09-30':
        blocks.append(json.loads(fetch('https://data.sec.gov/submissions/'+x['name'])))
records=[];seen=set()
for b in blocks:
    for i,form in enumerate(b['form']):
        date=b['filingDate'][i]; period=b['reportDate'][i]; acc=b['accessionNumber'][i]
        if form not in ['10-K','10-Q','10-K/A','10-Q/A'] or not '2021-10-31'<=date<='2024-09-30' or period>'2024-06-30' or acc in seen: continue
        seen.add(acc); doc=b['primaryDocument'][i]; url=f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-","")}/{doc}'
        dest=ROOT/'BLK'/'predecessor'/f'BLK_PREDECESSOR_{form.replace("/","-")}_{date}_{acc}.html';dest.parent.mkdir(parents=True,exist_ok=True)
        blob=dest.read_bytes() if dest.exists() else fetch(url)
        if len(blob)<5000: raise ValueError('Short filing '+url)
        dest.write_bytes(blob)
        records.append(dict(ticker='BLK',company=d['name']+' (pre-reorganization registrant; BlackRock, Inc. until 2024-10-01)',cik=cik,form=form,filing_date=date,period_end=period,accession=acc,source_url=url,path=dest.relative_to(ROOT).as_posix(),status='archived',bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),analytical_review='not_yet_reviewed',basis='Same operating business before the GIP/holding-company reorganization; pre-GIP, pre-HPS and pre-Preqin financials.',recorded_date='2026-11-02'))
        print('BLK predecessor',form,date,period,flush=True)
write_json(DATA/'BLK_predecessor_filings.json',{'as_of':'2026-11-02','records':records})
print('Predecessor archived',len(records))
