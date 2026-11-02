"""Archive recent company earnings 8-K exhibits with source URLs."""
import json,re,sys,urllib.parse,datetime as dt,hashlib
from collect_sources import ROOT,DATA,CO,fetch,write_json,ASOF
from prepare_research import Reader
for tk in (sys.argv[1:] or CO):
    sub=DATA/'submissions'/f'{tk}.json'
    if not sub.exists():
        print('NOT_READY',tk,flush=True); continue
    data=json.loads(sub.read_text(encoding='utf-8')); r=data['filings']['recent']
    ids=[i for i,f in enumerate(r['form']) if f=='8-K' and '2.02' in r.get('items',['']*len(r['form']))[i] and '2026-01-01'<=r['filingDate'][i]<=ASOF]
    rows=[]
    for i in ids:
        acc=r['accessionNumber'][i]; date=r['filingDate'][i]; cik=int(data['cik'])
        base=f'https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace("-","")}/'
        index=base+acc+'-index.html'
        try:
            raw=fetch(index).decode('utf-8','replace')
            files=[]
            for tr in re.findall(r'<tr[^>]*>(.*?)</tr>',raw,re.S|re.I):
                if not re.search(r'EX-99',tr,re.I): continue
                am=re.search(r'<a[^>]+href="([^"]+)"',tr)
                if not am: continue
                u=urllib.parse.urljoin(index,am.group(1)).replace('/ix?doc=','')
                if not re.search(r'\.(?:htm|html|pdf)(?:$|\?)',u,re.I): continue
                files.append(u)
            for u in files:
                name=urllib.parse.urlsplit(u).path.split('/')[-1]
                dest=ROOT/tk/'earnings'/f'{date}_{name}'
                dest.parent.mkdir(parents=True,exist_ok=True)
                b=dest.read_bytes() if dest.exists() else fetch(u)
                if len(b)<1000: raise ValueError('Unexpectedly short exhibit')
                dest.write_bytes(b)
                if dest.suffix.lower() in ('.htm','.html'):
                    p=Reader(); p.feed(b.decode('utf-8','replace'))
                    dest.with_suffix('.txt').write_text(f'Source: {u}\nFiling date: {date}\n\n'+p.text(),encoding='utf-8')
                rows.append({'ticker':tk,'filing_date':date,'source_url':u,'accession':acc,'path':dest.relative_to(ROOT).as_posix(),'status':'archived','sha256':hashlib.sha256(b).hexdigest(),'recorded_date':dt.date.today().isoformat(),'analytical_review':'not_yet_reviewed'})
                print('EARNINGS',tk,date,name,len(b),flush=True)
        except Exception as exc:
            rows.append({'ticker':tk,'filing_date':date,'source_url':index,'status':'failed','error':str(exc)})
            print('FAILED',tk,date,str(exc),flush=True)
        write_json(DATA/f'{tk}_earnings.json',{'as_of':ASOF,'records':rows})

