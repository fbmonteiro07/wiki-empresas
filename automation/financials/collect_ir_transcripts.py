"""Download company-hosted transcript PDFs and preserve text with fidelity labels."""
import concurrent.futures,datetime as dt,hashlib,json,re,subprocess,urllib.parse
from collect_sources import ROOT,DATA,fetch,write_json
PDFTEXT=r'C:\Users\Felipe.monteiro\AppData\Local\Programs\Git\mingw64\bin\pdftotext.exe'
jobs=[]
p=DATA/'discovery/APO_ir_links.json'
if p.exists():
    jobs += [('APO',r['url'],'company-hosted earnings transcript') for r in json.loads(p.read_text(encoding='utf-8'))['links'] if 'transcript' in (r['url']+' '+r['title']).lower() and '.pdf' in r['url'].lower()]
jobs += [
('JPM','https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2026/3rd-quarter/3q26-earnings-transcript.pdf','company-hosted Q3 2026 earnings transcript'),
('JPM','https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2024/1st-quarter/jpm-1q24-earnings-call-transcript.pdf','company-hosted Q1 2024 earnings transcript'),
('JPM','https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2024/2nd-quarter/jpm-2q24-earnings-call-transcript-final.pdf','company-hosted Q2 2024 earnings transcript'),
('KKR','https://ir.kkr.com/media/document/2f89ef3f-cf71-45a8-ab72-b2a0ac803767/assets/KKR_Q425_Earnings_Transcript.pdf?disposition=inline','company-hosted Q4 2025 earnings transcript; actual call date 2026-02-05'),
('COIN','https://investor.coinbase.com/files/content_files/Q3_26-Earnings-Presentation-Transcript.pdf','company-hosted Q3 2026 prepared earnings presentation'),
('COIN','https://investor.coinbase.com/files/content_files/Q3_26-Earnings-Call-Transcript.pdf','company-hosted Q3 2026 Q&A call'),
]
jobs=list(dict.fromkeys(jobs))
def one(job):
    tk,url,desc=job
    name=urllib.parse.unquote(urllib.parse.urlsplit(url).path.split('/')[-1]).replace('+',' ')
    name=re.sub(r'[^a-zA-Z0-9_.-]+','-',name)[:145]
    path=ROOT/tk/'transcripts'/'originals'/name
    path.parent.mkdir(parents=True,exist_ok=True)
    row={'ticker':tk,'source_url':url,'description':desc,'path':path.relative_to(ROOT).as_posix(),'recorded_date':dt.date.today().isoformat(),'analytical_review':'not_yet_reviewed'}
    try:
        b=path.read_bytes() if path.exists() else fetch(url)
        if not b.startswith(b'%PDF'): raise ValueError('Not a PDF')
        path.write_bytes(b)
        textpath=path.with_suffix('.txt')
        subprocess.run([PDFTEXT,'-layout',str(path),str(textpath)],check=True,capture_output=True)
        s=textpath.read_text(encoding='utf-8',errors='replace')
        md=path.parent.parent/(tk+'_IR_'+path.stem+'.md')
        md.write_text(f'# {tk} — {desc}\n\n- **Source:** {url}\n- **Original PDF:** [PDF](originals/{path.name})\n- **Retrieved:** {dt.date.today()}\n- **Fidelity:** Full text extraction of company-hosted PDF; page breaks preserved. Check original PDF for tables and footnotes.\n\n## Source text\n\n'+s,encoding='utf-8')
        row.update(status='archived',text_path=md.relative_to(ROOT).as_posix(),chars=len(s),sha256=hashlib.sha256(b).hexdigest(),opening=s[:650])
        print('IR_TRANSCRIPT',tk,name,len(s),flush=True)
    except Exception as exc:
        row.update(status='failed',error=str(exc))
        print('IR_FAILED',tk,name,str(exc),flush=True)
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    rows=list(pool.map(one,jobs))
write_json(DATA/'ir_transcripts.json',{'as_of':'2026-10-31','records':rows})

