"""Prepare attributed local research extracts without changing wiki prose."""
import datetime as dt, hashlib, html, json, re, sqlite3
from html.parser import HTMLParser
from pathlib import Path
from collect_sources import ROOT, DATA, CO, write_json
STRONG={'JPM':r'JPMorgan Chase|JPMorgan.{0,35}(?:bank|earnings)|\bJPM\b.{0,20}(?:EPS|NII|CET1)','SPGI':r'\bSPGI\b|S&P Global','MCO':r'\bMCO\b|Moody.s','BX':r'\bBX\b|Blackstone','KKR':r'\bKKR\b','GS':r'Goldman Sachs Group|Goldman.{0,20}earnings|\bGS\b.{0,12}EPS','V':r'\bVisa\b','MA':r'\bMastercard\b','APO':r'\bAPO\b|Apollo','HOOD':r'\bHOOD\b|\bRobinhood\b','COIN':r'\bCOIN\b|\bCoinbase\b','MSCI':r'\bMSCI\b','EFX':r'\bEFX\b|\bEquifax\b','TRU':r'\bTRU\b|\bTrans ?Union\b','CME':r'\bCME\b','ICE':r'(?-i:\bICE\b)|Intercontinental Exchange','CBOE':r'(?-i:\bCBOE\b|\bCboe\b)','NDAQ':r'\bNDAQ\b|Nasdaq,? Inc\b|Nasdaq \(NDAQ\)|(?<=, )Nasdaq(?=,)','OWL':r'\bOWL\b|Blue Owl','BLK':r'\bBLK\b|BlackRock'}
NEG={'BX':r'Blackstone Mortgage|Blackstone Secured|Blackstone Digital Infrastructure|BXMT|BXSL','KKR':r'KKR Real Estate Finance|FS KKR','APO':r'Apollo Commercial Real Estate|Quantinuum|MCK Announces','V':r'visa program|U.S. Visa Forms|will issue visas|visas to|China Press Digest','HOOD':r'under the hood','MCO':r'Healthcare|Managed Care|MCOs','MSCI':r'Index Review|QCIR|Benchmark News|Rebalanc|Reclassif|IndexAlpha|Index Analytics|Global Recap|Performance Monitor|Trade Recap|Methodology|Free Float|Country Classification|MSCI (?:EM|DM|World|China|ACWI|Emerging|Europe|Japan|Korea|Taiwan|India|Brazil|US Real|Small|Global|Indonesia|Turkey|Index|Argentina|Greece|reshuffle|review|downgrade|action|announcement)|join MSCI|vs MSCI|MSCI Rebal|GICS|MSCI Flows|MSCI Maintains|MSCI.s Message|Bom Dia|baskets|LATAM DAILY|LatAm|Andean|Mexbol','EFX':r'EFX CN','CME':r'lithium|carbonate|hydroxide|Auto1','CBOE':r'\bVIX\b|Volatility Index','NDAQ':r'S&P|\bDow\b|Russell|futures|\bNDX\b|Composite','BLK':r'Invitation|Real Conversation|Cogna|XP Education'}
class Reader(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0; self.stack=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        hide=tag in ('script','style','ix:hidden','head') or 'display:none' in attrs.get('style','').replace(' ','').lower()
        if tag not in ('br','img','meta','link','hr','input'):
            self.stack.append((tag,hide))
            if hide: self.skip+=1
        if not self.skip and tag in ('p','div','tr','br','h1','h2','h3','h4','li'): self.parts.append('\n')
        if not self.skip and tag in ('td','th'): self.parts.append(' | ')
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                for _,hidden in self.stack[i:]:
                    if hidden: self.skip=max(0,self.skip-1)
                del self.stack[i:]; break
        if not self.skip and tag in ('p','div','tr','h1','h2','h3','h4','li'): self.parts.append('\n')
    def handle_data(self,data):
        if not self.skip: self.parts.append(data)
    def text(self):
        s=re.sub(r'[ \t]+',' ',''.join(self.parts))
        return re.sub(r'\n\s*\n+','\n\n',s).strip()
def extract_filings():
    for tk in CO:
        for p in sorted((ROOT/tk).glob('*.html')):
            if not re.search(r'_202[456]-',p.name): continue
            dest=p.parent/'filings_text'/(p.stem+'.txt')
            if dest.exists(): continue
            reader=Reader()
            blob=p.read_bytes()
            try: source=blob.decode('utf-8-sig')
            except UnicodeDecodeError: source=blob.decode('cp1252',errors='replace')
            reader.feed(source)
            text=reader.text(); dest.parent.mkdir(exist_ok=True)
            dest.write_text('Source archive: '+p.name+'\n\n'+text,encoding='utf-8')
            print('TEXT',tk,p.name,len(text),flush=True)
def commentary(only=None, through='2026-10-31'):
    raw=json.loads((ROOT/'_wiki/_data/sentiment/sellside_mail_raw.json').read_text(encoding='utf-8'))
    meta={}; selected={}
    for r in raw:
        if not '2026-01-01'<=r['d']<=through: continue
        subject=r.get('subject','')
        tks=[t for t,p in STRONG.items() if (only is None or t in only) and re.search(p,subject,re.I) and not (t in NEG and re.search(NEG[t],subject,re.I))]
        if tks: meta[r['id']]=r; selected[r['id']]=tks
    records=[]; seen=set()
    with (ROOT/'_wiki/_data/sentiment/sellside_mail_bodies.jsonl').open(encoding='utf-8') as f:
        for line in f:
            obj=json.loads(line); mid=obj.get('id')
            if mid not in selected: continue
            m=meta[mid]; body=obj.get('body','')
            key=(m['d'],m['subject'],hashlib.sha256(body.encode()).hexdigest())
            if key in seen: continue
            seen.add(key)
            slug=re.sub(r'[^a-zA-Z0-9_-]+','-',m['subject']).strip('-')[:100]
            h=hashlib.sha256(mid.encode()).hexdigest()[:8]
            for tk in selected[mid]:
                path=ROOT/tk/'commentary'/f'{m["d"]}_{slug}_{h}.md'
                path.parent.mkdir(parents=True,exist_ok=True)
                status='cache_at_length_limit' if len(body)>=8900 else 'cached_email_body'
                text=f'# {m["subject"]}\n\n- **Date received:** {m["d"]} {m.get("t","")} (local archive timestamp)\n- **Source sender:** {m["from"]}\n- **Source archive:** _wiki/_data/sentiment/sellside_mail_bodies.jsonl + sellside_mail_raw.json\n- **Fidelity:** Cached email body; original collection capped bodies at 9,000 characters. This is not necessarily the complete linked research report.\n- **Archive quality:** {status}; {len(body):,} characters.\n- **Recorded:** {dt.date.today()}\n\n## Cached source text\n\n{body}\n'
                path.write_text(text,encoding='utf-8')
                records.append({'ticker':tk,'date':m['d'],'subject':m['subject'],'sender':m['from'],'path':path.relative_to(ROOT).as_posix(),'source_id':mid,'body_chars':len(body),'quality':status,'sha256':hashlib.sha256(body.encode()).hexdigest(),'analytical_review':'not_yet_reviewed'})
    if only is not None:
        prior=json.loads((DATA/'commentary_manifest.json').read_text(encoding='utf-8-sig'))
        records=[x for x in prior['records'] if x['ticker'] not in only]+records
    write_json(DATA/'commentary_manifest.json',{'as_of':'2026-10-31' if only is None else through,'selection':'Company-specific subject matches; named affiliate and language false positives excluded. Cached bodies are not assumed to contain the full linked report.','records':records})
    print('COMMENTARY',json.dumps({t:sum(r['ticker']==t for r in records) for t in CO}),flush=True)
def corpus_search():
    con=sqlite3.connect(ROOT/'_wiki/_data/search.db')
    q={'JPM':'"JPMorgan Chase"','SPGI':'"S&P Global" OR SPGI','MCO':'MCO OR "Moodys" OR "Moody\'s"','BX':'Blackstone','KKR':'KKR','GS':'"Goldman Sachs Group"','V':'Visa','MA':'Mastercard','APO':'"Apollo Global" OR APO','HOOD':'Robinhood OR HOOD','COIN':'Coinbase OR COIN','MSCI':'"MSCI Inc" OR "MSCI (MSCI)"','EFX':'Equifax','TRU':'TransUnion','CME':'"CME Group"','ICE':'"Intercontinental Exchange"','CBOE':'Cboe','NDAQ':'"Nasdaq Inc" OR NDAQ','OWL':'"Blue Owl"','BLK':'BlackRock'}
    result={}
    for tk,query in q.items():
        rows=con.execute("SELECT path,kind,ticker,date,title,snippet(docs,5,'[',']',' ... ',70) FROM docs WHERE docs MATCH ? AND kind IN ('report','call','briefing','stratechery') ORDER BY bm25(docs) LIMIT 60",(query,)).fetchall()
        result[tk]=[dict(zip(['path','kind','ticker','date','title','excerpt'],r)) for r in rows]
    write_json(DATA/'local_corpus_discovery.json',result)
    print('LOCAL_SEARCH',json.dumps({t:len(v) for t,v in result.items()}))
if __name__=='__main__':
    import sys
    for mode in sys.argv[1:] or ['commentary','corpus','filings']:
        if mode.startswith('commentary:'):
            commentary(mode.split(':')[1].split(','), '2026-11-02'); continue
        {'commentary':commentary,'corpus':corpus_search,'filings':extract_filings}[mode]()

