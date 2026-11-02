"""Financials source ingestion: stdlib only; never writes wiki research pages."""
import argparse, concurrent.futures, datetime as dt, hashlib, html, json, os, re, ssl, threading, time, urllib.parse, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'_wiki'/'_data'/'financials'
ASOF=os.environ.get('FIN_ASOF','2026-10-31')  # 2026-11-02 additions (MSCI/EFX/TRU) run with FIN_ASOF=2026-11-02
CUTOFF='2021-10-31'
CO={'JPM':('JPMorgan Chase & Co.','NYSE'),'SPGI':('S&P Global Inc.','NYSE'),'MCO':("Moody's Corporation",'NYSE'),'BX':('Blackstone Inc.','NYSE'),'KKR':('KKR & Co. Inc.','NYSE'),'GS':('The Goldman Sachs Group, Inc.','NYSE'),'V':('Visa Inc.','NYSE'),'MA':('Mastercard Incorporated','NYSE'),'APO':('Apollo Global Management, Inc.','NYSE'),'HOOD':('Robinhood Markets, Inc.','NASDAQ'),'COIN':('Coinbase Global, Inc.','NASDAQ'),'MSCI':('MSCI Inc.','NYSE'),'EFX':('Equifax Inc.','NYSE'),'TRU':('TransUnion','NYSE')}
LOCK=threading.Lock()
LAST=0.0
TLS=ssl.create_default_context()
TLS.verify_flags &= ~ssl.VERIFY_X509_STRICT  # Corporate proxy certificate lacks AKI; retain trust and hostname validation.

def fetch(url,tries=3):
    global LAST
    sec=urllib.parse.urlsplit(url).hostname.endswith('sec.gov')
    headers={'User-Agent':'Capstone Research felipe.monteiro@capstone.com.br'} if sec else {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36'}
    for attempt in range(tries):
        try:
            with LOCK:
                delay=.35-(time.monotonic()-LAST)
                if delay>0: time.sleep(delay)
                LAST=time.monotonic()
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),context=TLS,timeout=55) as r: blob=r.read()
            if len(blob)<100: raise ValueError('Unexpectedly short response')
            return blob
        except Exception:
            if attempt==tries-1: raise
            time.sleep(2*(attempt+1))

def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temp.replace(path)

def strip(s):
    s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',s,flags=re.S|re.I)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()

def sec_company(ticker,info):
    cik=str(info['cik_str']).zfill(10)
    d=ROOT/ticker
    d.mkdir(exist_ok=True)
    records,errors=[],[]
    data=json.loads(fetch(f'https://data.sec.gov/submissions/CIK{cik}.json'))
    write_json(DATA/'submissions'/f'{ticker}.json',data)
    blocks=[data['filings']['recent']]
    for extra in data['filings'].get('files',[]):
        if extra.get('filingTo','')<CUTOFF: continue
        try:
            b=json.loads(fetch('https://data.sec.gov/submissions/'+extra['name']))
            blocks.append(b)
            write_json(DATA/'submissions'/extra['name'],b)
        except Exception as exc: errors.append({'url':extra['name'],'error':str(exc)})
    seen=set()
    for block in blocks:
        for i,form in enumerate(block['form']):
            date,acc,doc=block['filingDate'][i],block['accessionNumber'][i],block['primaryDocument'][i]
            if form not in {'10-K','10-Q','10-K/A','10-Q/A'} or not CUTOFF<=date<=ASOF or acc in seen: continue
            seen.add(acc)
            url=f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-","")}/{doc}'
            dest=d/f'{ticker}_{form.replace("/","-")}_{date}_{acc}.html'
            row={'ticker':ticker,'company':data['name'],'cik':cik,'form':form,'filing_date':date,'period_end':block.get('reportDate',['']*len(block['form']))[i],'accession':acc,'source_url':url,'path':dest.relative_to(ROOT).as_posix(),'recorded_date':dt.date.today().isoformat(),'analytical_review':'not_yet_reviewed'}
            try:
                blob=dest.read_bytes() if dest.exists() else fetch(url)
                first=blob[:10000].lower()
                if len(blob)<5000 or b'undeclared automated tool' in first or b'you do not have permission' in first: raise ValueError('Response failed filing-content validation')
                if not dest.exists(): dest.write_bytes(blob)
                row.update(status='archived',bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest())
            except Exception as exc: row.update(status='failed',error=str(exc))
            records.append(row)
            write_json(DATA/f'{ticker}_filings.json',{'as_of':ASOF,'cutoff':CUTOFF,'records':records,'errors':errors})
            print(ticker,form,date,row['status'],flush=True)
    print('SEC_DONE',ticker,len(records),sum(x['status']=='archived' for x in records),flush=True)

def transcript(ticker,url):
    raw=fetch(url).decode('utf-8','replace')
    tm=re.search(r'<title>(.*?)</title>',raw,re.S)
    title=strip(tm.group(1)) if tm else ''
    qm=re.search(r'Q([1-4])\s+(20\d\d)',title)
    dm=re.search(r'/reports/(20\d\d)-(\d{1,2})-(\d{1,2})-',url)
    if not qm or not dm: raise ValueError('Missing fiscal quarter or call date: '+title)
    q,fy=map(int,qm.groups())
    date=dt.date(*map(int,dm.groups())).isoformat()
    if date>ASOF: return {'ticker':ticker,'source_url':url,'date':date,'status':'future_excluded'}
    sections=re.findall(r'<section class="transcript-line-(?:left|right)[^"]*">(.*?)</section>',raw,re.S)
    turns,participants=[],{}
    for s in sections:
        nm=re.search(r'<div class="font-weight-bold">\s*([^<]+?)\s*(?:<div class="secondary-title[^>]*>(.*?)</div>)?\s*</div>',s,re.S)
        ts=re.search(r'<time datetime="([^"]+)"',s)
        ps=re.findall(r'<p class="pb-2 mb-0">(.*?)</p>',s,re.S)
        if not nm: continue
        name,role=strip(nm.group(1)),strip(nm.group(2) or '')
        if role: participants[name]=role
        turns.append((name,ts.group(1) if ts else '', '\n\n'.join(strip(p) for p in ps)))
    words=sum(len(x[2].split()) for x in turns)
    if len(turns)<15 or words<2000: raise ValueError(f'Incomplete or unavailable transcript: {len(turns)} turns / {words} words')
    label=f'Q{q} '+(f'FY{fy}' if ticker=='V' else str(fy))
    dest=ROOT/ticker/'transcripts'/f'{ticker}_Q{q}-{"FY" if ticker=="V" else ""}{fy}-earnings_{date}.md'
    dest.parent.mkdir(parents=True,exist_ok=True)
    lines=[f'# {CO[ticker][0]} — {label} Earnings Call — {date}','',f'- **Company:** {CO[ticker][0]}',f'- **Ticker:** {ticker}',f'- **Fiscal period:** {label}',f'- **Call date:** {date}',f'- **Source:** {url}',f'- **Retrieved:** {dt.date.today()}',f'- **Completeness:** All {len(turns)} speaker turns served by MarketBeat / Quartr; {words:,} words.','- **Fidelity:** Third-party transcription, not a company-certified transcript. Check load-bearing numbers against company releases and SEC filings.','','## Participants','']
    lines += [f'- {n} — {r}' for n,r in participants.items()]+['','## Transcript','']
    for name,ts,body in turns: lines += [f'**{name}** {ts}','',body,'']
    text='\n'.join(lines)
    dest.write_text(text,encoding='utf-8')
    return {'ticker':ticker,'date':date,'fiscal_period':label,'source_url':url,'path':dest.relative_to(ROOT).as_posix(),'status':'archived','turns':len(turns),'words':words,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(), 'sha256_basis':'file bytes','analytical_review':'not_yet_reviewed','recorded_date':dt.date.today().isoformat()}

def transcripts_company(ticker):
    url=f'https://www.marketbeat.com/stocks/{CO[ticker][1]}/{ticker}/earnings/'
    raw=fetch(url).decode('utf-8','replace')
    cache=DATA/'discovery'/f'{ticker}_marketbeat.html'
    cache.parent.mkdir(parents=True,exist_ok=True)
    cache.write_text(raw,encoding='utf-8')
    links=sorted(set(urllib.parse.urljoin(url,html.unescape(x)).split('?')[0].split('#')[0] for x in re.findall(r'href=["\x27]([^"\x27]*/earnings/reports/[^"\x27]+)',raw)))
    records=[]
    for link in links:
        try: row=transcript(ticker,link)
        except Exception as exc: row={'ticker':ticker,'source_url':link,'status':'failed','error':str(exc)}
        records.append(row)
        write_json(DATA/f'{ticker}_transcripts.json',{'as_of':ASOF,'discovery_url':url,'records':records})
        print('TRANSCRIPT',ticker,link.split('/')[-2],row['status'],row.get('words',''),flush=True)
    if not links: write_json(DATA/f'{ticker}_transcripts.json',{'as_of':ASOF,'discovery_url':url,'records':[],'error':'No report links found'})

def main():
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=['sec','transcripts'])
    p.add_argument('--tickers',nargs='*',default=list(CO))
    a=p.parse_args()
    DATA.mkdir(parents=True,exist_ok=True)
    if a.mode=='sec':
        mapping=json.loads(fetch('https://www.sec.gov/files/company_tickers.json'))
        by={x['ticker']:x for x in mapping.values()}
        res=DATA/'company_resolution.json'
        merged=json.loads(res.read_text(encoding='utf-8-sig')) if res.exists() else {}
        merged.update({t:by[t] for t in a.tickers})
        write_json(res,merged)
        for t in a.tickers:
            try: sec_company(t,by[t])
            except Exception as exc: print('COMPANY_FAILED',t,str(exc),flush=True)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            fs={pool.submit(transcripts_company,t):t for t in a.tickers}
            for f in concurrent.futures.as_completed(fs):
                try: f.result()
                except Exception as exc: print('COMPANY_FAILED',fs[f],str(exc),flush=True)
if __name__=='__main__': main()

