"""Read cached AI Model values and build AI Labs revenue; stdlib, read-only workbook."""
import argparse, datetime as dt, hashlib, json, math, re, zipfile
from pathlib import Path
from io import BytesIO
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'_data'/'ai-labs-revenue'
UI=Path(__file__).with_name('ai_labs_revenue_ui')
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
DEFAULT_WB=Path('P:/Felipe Monteiro/US Equities/Modelos oficiais/AI Model.xlsx')
DEFAULT_TEMPLATE=Path('P:/Felipe Monteiro/US Equities/Capstone-Wiki/ai-labs/index.html')
class Workbook:
    def __init__(self,path):
        self.raw=path.read_bytes()
        z=zipfile.ZipFile(BytesIO(self.raw))
        strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels={x.get('Id'):x.get('Target') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        self.sheets={}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS):
            target=rels[sheet.get(REL)]
            part=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            cells={}
            for c in ET.fromstring(z.read(part)).findall('.//s:sheetData/s:row/s:c',NS):
                v=c.findtext('s:v',default=None,namespaces=NS)
                if c.get('t')=='s' and v is not None: v=strings[int(v)]
                elif c.get('t')=='inlineStr': v=''.join(c.find('s:is',NS).itertext())
                elif v is not None and c.get('t') not in ('e','str'): v=float(v)
                cells[c.get('r')]=v
            self.sheets[sheet.get('name')]=cells
    def value(self,s,c): return self.sheets[s].get(c)
    def number(self,s,c):
        v=self.value(s,c)
        if not isinstance(v,(int,float)) or not math.isfinite(v): raise ValueError(f'Invalid cache: {s}!{c}: {v!r}')
        return v
    def row(self,s,label,maximum=None):
        rows={int(re.search(r'\d+',c).group()) for c,v in self.sheets[s].items() if c.rstrip('0123456789') in ('A','B') and str(v).strip()==label}
        if maximum is not None: rows={r for r in rows if r<=maximum}
        if len(rows)!=1: raise ValueError(f'Ambiguous row {s}: {label}: {rows}')
        return rows.pop()
def build(workbook,asof,template,output,*,persist=True):
    w=Workbook(workbook); tracker='ARR Tracker'
    news=json.loads((DATA/'sources.json').read_text(encoding='utf-8-sig'))
    assert len({x['id'] for x in news['observations']})==len(news['observations'])
    for o in news['observations']:
        assert o['source_id'] in news['sources']
        assert news['sources'][o['source_id']]['published']<=news['checked']
    months=[]
    def col_number(col):
        result=0
        for ch in col: result=result*26+ord(ch)-64
        return result
    headers={c[:-1]:v for c,v in w.sheets[tracker].items() if re.fullmatch(r'[A-Z]+3',c)}
    for col,value in sorted(headers.items(),key=lambda item:col_number(item[0])):
        if not isinstance(value,(int,float)) or not 43831<=value<=73050: continue
        date=(dt.datetime(1899,12,30)+dt.timedelta(days=value)).date()
        if date.day!=1: raise ValueError(f'Month header is not month-start: {tracker}!{col}3')
        months.append({'date':date.isoformat(),'col':col,'status':'Forecast' if date.isoformat()[:7]>=asof[:7] else 'Model estimate'})
    if len(months)<12 or len({m['date'] for m in months})!=len(months):
        raise ValueError('ARR Tracker needs at least 12 distinct monthly headers')
    month_ids=[int(m['date'][:4])*12+int(m['date'][5:7]) for m in months]
    if any(b-a!=1 for a,b in zip(month_ids,month_ids[1:])):
        raise ValueError('ARR Tracker month headers are not consecutive')
    specs=[('openai_net','OpenAI','net','Average Monthly Reported ARR ($M)',True),
           ('openai_gross','OpenAI','gross','(=) OpenAI Gross Revenue ARR ($M)',False),
           ('anthropic_gross','Anthropic','gross','Average Monthly Reported ARR Gross ($M) adj',True),
           ('anthropic_net','Anthropic','net','Net Avg Monthly Reported ARR ($M)',False)]
    series=[]
    for key,company,basis,label,reported_basis in specs:
        row=w.row(tracker,label)
        points=[{**m,'value':w.number(tracker,f"{m['col']}{row}"),'cell':f"{tracker}!{m['col']}{row}"}
                for m in months if w.value(tracker,f"{m['col']}{row}") is not None]
        series.append({'id':key,'company':company,'basis':basis,'reported_basis':reported_basis,'points':points})
    annual=[]
    for company in ['OpenAI','Anthropic']:
        row=w.row(company,'Receita',maximum=10)
        # The first contiguous annual band is revenue; later bands are backlog checks.
        headers=sorted(((c[:-1],v) for c,v in w.sheets[company].items() if re.fullmatch(r'[A-Z]+1',c)),key=lambda item:col_number(item[0]))
        started=False
        for col,period in headers:
            match=re.fullmatch(r'CY(\d{2})(E?)',str(period))
            if started and not match: break
            if not match: continue
            started=True
            if int(match[1])<24: continue
            annual.append({'company':company,'period':period,'value':w.number(company,f'{col}{row}'),
                           'basis':'net' if company=='OpenAI' else 'gross','cell':f'{company}!{col}{row}',
                           'status':'Forecast' if match[2] else 'Workbook historical'})
    quarterly=[]
    qrows=sorted({int(c[1:]) for c,v in w.sheets[tracker].items() if re.fullmatch(r'B\d+',c) and str(v).strip()=='Receita trimestral (reported)'})
    anth_row=w.row(tracker,'Average Monthly Reported ARR Gross ($M) adj')
    if len(qrows)!=2 or not qrows[0]<anth_row<qrows[1]:
        raise ValueError('Quarterly revenue labels moved outside their company blocks')
    for company,row in zip(['OpenAI','Anthropic'],qrows):
        for month in months:
            date=dt.date.fromisoformat(month['date']); col=month['col']
            if date.month%3 or w.value(tracker,f'{col}{row}') is None: continue
            quarterly.append({'company':company,'period':f'Q{date.month//3} {date.year}','value':w.number(tracker,f'{col}{row}'),
                              'cell':f'{tracker}!{col}{row}','basis':'net' if company=='OpenAI' else 'gross'})
    combined_monthly={}
    for basis in ['reported','net','gross']:
        components=[s for s in series if s['reported_basis']] if basis=='reported' else [s for s in series if s['basis']==basis]
        if {s['company'] for s in components}!={'OpenAI','Anthropic'}:
            raise ValueError(f'Combined system requires exactly the two labs: {basis}')
        maps=[{p['date']:p for p in s['points']} for s in components]
        points=[]
        # Join by month; a missing component does not become zero.
        for date in sorted(set(maps[0]) & set(maps[1])):
            parts=[m[date] for m in maps]
            points.append({'date':date,'value':sum(p['value'] for p in parts),
                           'status':'Forecast' if any(p['status']=='Forecast' for p in parts) else 'Model estimate',
                           'cell':' + '.join(p['cell'] for p in parts),
                           'components':[{'company':s['company'],'basis':s['basis'],'value':p['value'],'cell':p['cell']} for s,p in zip(components,parts)]})
        combined_monthly[basis]={'id':'system_'+basis,'company':'Combined system',
                                 'basis':'mixed basis' if basis=='reported' else basis,'points':points}
    combined_annual=[]
    for period in dict.fromkeys(a['period'] for a in annual):
        parts=[a for a in annual if a['period']==period]
        if {a['company'] for a in parts}=={'OpenAI','Anthropic'} and len(parts)==2:
            combined_annual.append({'period':period,'value':sum(a['value'] for a in parts),
                                    'basis':'OpenAI net + Anthropic gross','cell':' + '.join(a['cell'] for a in parts),
                                    'status':'Forecast' if any(a['status']=='Forecast' for a in parts) else 'Workbook historical',
                                    'components':parts})
    combined={'method':'Arithmetic sum of OpenAI and Anthropic for matching periods; no missing values filled with zero.',
              'monthly':combined_monthly,'annual':combined_annual}
    payload={'asof':asof,'unit':'USD million','workbook':str(workbook),'combined':combined,
             'workbook_saved':dt.datetime.fromtimestamp(workbook.stat().st_mtime,dt.timezone.utc).isoformat(),
             'workbook_sha256':hashlib.sha256(w.raw).hexdigest(),'series':series,'annual':annual,'quarterly':quarterly,**news}
    fiscal_headers=[(c[:-1],str(v)[2:]) for c,v in w.sheets[tracker].items() if re.fullmatch(r'[A-Z]+3',c) and re.fullmatch(r'FY20\d{2}',str(v))]
    annual_rows=[w.row(tracker,label) for label in ['(=) OpenAI Net Revenue ($M)','(=) Anthropic Gross Revenue ($M)']]
    fiscal_headers=[(col,year) for col,year in fiscal_headers if all(w.value(tracker,f'{col}{row}') is not None for row in annual_rows)]
    if not fiscal_headers: raise ValueError('No common fiscal-year revenue totals in ARR Tracker')
    col,year=max(fiscal_headers,key=lambda item:item[1])
    for company,label in [('OpenAI','(=) OpenAI Net Revenue ($M)'),('Anthropic','(=) Anthropic Gross Revenue ($M)')]:
        row=w.row(tracker,label)
        matches=[x for x in annual if x['company']==company and x['period'].rstrip('E')=='CY'+year[-2:]]
        if len(matches)!=1 or abs(w.number(tracker,f'{col}{row}')-matches[0]['value'])>0.01:
            raise ValueError(f'{company} annual tie-out failed for {year}')
    pretty=json.dumps(payload,ensure_ascii=False,indent=2)+'\n'
    if persist: save_snapshot(pretty)
    baseline=DATA/'legacy-wfs-2026-06-11.html'
    if not baseline.exists():
        original=template.read_text(encoding='utf-8-sig')
        if 'id="p-revenue"' in original: raise ValueError('First build requires original WFS template')
        baseline.write_text(original,encoding='utf-8')
    html=baseline.read_text(encoding='utf-8')
    html=html.replace('<div class="tab active" data-panel="p-overview">Overview</div>',
                      '<div class="tab active" data-panel="p-revenue">Revenue &amp; sources</div>\n<div class="tab" data-panel="p-overview">WFS overview · Jun 11</div>')
    html=html.replace('<div class="panel active" id="p-overview">','<div class="panel" id="p-overview">')
    html=html.replace('data-panel="p-arr">ARR Tracker</div>','data-panel="p-arr">WFS ARR · Jun 11</div>')
    html=html.replace('PnL estimado (Wells Fargo Securities) · USD milhões · fonte: oAI and Anth.xlsx',
                      f'Revenue: Capstone AI Model · news sources checked {news["checked"]} · USD millions')
    html=html.replace('Extraído em 11-jun-2026','Updated '+asof)
    html=html.replace('</style>',(UI/'revenue.css').read_text(encoding='utf-8-sig')+'\n</style>',1)
    html=re.sub(r'(<div class="panel" id="p-[^"]+">)',r'\1<div class="legacy-note">Historical Wells Fargo snapshot · extracted June 11, 2026. Revenue &amp; sources contains the current Capstone update.</div>',html)
    html=html.replace('<!-- OVERVIEW -->',(UI/'revenue.html').read_text(encoding='utf-8-sig')+'\n<!-- OVERVIEW -->',1)
    html=html.replace("if (t.dataset.panel === 'p-overview') Plotly.Plots.resize('arr-chart');",
                      "if (t.dataset.panel === 'p-overview' && window.Plotly) Plotly.Plots.resize('arr-chart');\n  if (t.dataset.panel === 'p-revenue') window.renderRevenue?.();")
    html=html.replace("Plotly.newPlot('arr-chart', [","if (window.Plotly) Plotly.newPlot('arr-chart', [")
    encoded=json.dumps(payload,ensure_ascii=False).replace('</','<\\/')
    script='<script>const REVENUE_DATA = '+encoded+';\n'+(UI/'revenue.js').read_text(encoding='utf-8-sig')+'\n</script>'
    html=html.replace('</body>',script+'\n</body>')
    output.mkdir(parents=True,exist_ok=True)
    (output/'index.html').write_text(html,encoding='utf-8')
    (output/'revenue-data.json').write_text(pretty,encoding='utf-8')
    print(json.dumps({'output':str(output/'index.html'),'workbook_sha256':payload['workbook_sha256'],
                      'monthly_points':sum(len(s['points']) for s in series),'news_observations':len(news['observations']),
                      'annual_revenue':[x for x in annual if x['period'].rstrip('E')=='CY'+year[-2:]]},indent=2))
    return payload

def save_snapshot(pretty):
    DATA.mkdir(parents=True,exist_ok=True)
    history=DATA/'history'; history.mkdir(exist_ok=True)
    snapshot=DATA/'model.json'
    if snapshot.exists() and snapshot.read_text(encoding='utf-8')!=pretty:
        old=snapshot.read_bytes(); prior=history/('model-'+hashlib.sha256(old).hexdigest()[:12]+'.json')
        if not prior.exists(): prior.write_bytes(old)
    snapshot.write_text(pretty,encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workbook',type=Path,default=DEFAULT_WB)
    p.add_argument('--asof',required=True)
    p.add_argument('--template',type=Path,default=DEFAULT_TEMPLATE)
    p.add_argument('--output',type=Path,default=ROOT/'_dashboards'/'ai-labs')
    a=p.parse_args(); dt.date.fromisoformat(a.asof); build(a.workbook,a.asof,a.template,a.output)

