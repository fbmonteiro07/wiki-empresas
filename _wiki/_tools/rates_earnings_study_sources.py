"""Download dated primary sources for the 2022/2026 study; stdlib only."""
from pathlib import Path
import concurrent.futures, json, subprocess, urllib.request, re
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1] / '_data/research/rates_earnings_20260930'
ROOT.mkdir(parents=True, exist_ok=True)
BASE = 'https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/'
URLS = {f'factset_{d}.pdf': BASE + f'EarningsInsight_{d}.pdf' for d in ['092526','010926','062626','010722','063022','093022','121622','123022']}
for year in [2021, 2022, 2026]:
    for kind in ['daily_treasury_yield_curve','daily_treasury_real_yield_curve']:
        URLS[f'{kind}_{year}.html'] = f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type={kind}&field_tdr_date_value={year}'
for month in ['202112','202201','202203','202206','202209','202210','202212']:
    for kind in ['daily_treasury_yield_curve','daily_treasury_real_yield_curve']:
        URLS[f'{kind}_{month}.html'] = f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type={kind}&field_tdr_date_value_month={month}'

class Table(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.row=None; self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr': self.row=[]
        if tag in ('th','td') and self.row is not None: self.cell=[]
    def handle_data(self,s):
        if self.cell is not None: self.cell.append(s)
    def handle_endtag(self,tag):
        if tag in ('th','td') and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split())); self.cell=None
        if tag=='tr' and self.row is not None:
            self.rows.append(self.row); self.row=None

def get(item):
    name,url=item; path=ROOT/name
    try:
        if not path.exists():
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            data=urllib.request.urlopen(req,timeout=45).read(); path.write_bytes(data)
        if name.endswith('.pdf'):
            subprocess.run(['pdftotext','-enc','UTF-8','-layout',str(path),str(path.with_suffix('.txt'))],check=True,capture_output=True)
            first=path.with_suffix('.txt').read_text(encoding='utf-8')[:160]
            return {'file':name,'url':url,'status':'ok','first':first}
        p=Table(); p.feed(path.read_text(encoding='utf-8'))
        (ROOT/name.replace('.html','.json')).write_text(json.dumps(p.rows,indent=2),encoding='utf-8')
        relevant=[r for r in p.rows if r and (r[0] in ['12/31/2021','01/03/2022','03/31/2022','06/30/2022','09/30/2022','10/24/2022','12/30/2022','01/02/2026','02/27/2026','06/30/2026','08/31/2026','09/25/2026','09/29/2026'] or '10 YR' in r or '10 Yr' in r)]
        return {'file':name,'url':url,'status':'ok','rows':relevant}
    except Exception as e: return {'file':name,'url':url,'status':'error','error':str(e)}

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        records=list(pool.map(get,URLS.items()))
    (ROOT/'source_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    for r in records: print(json.dumps(r))
