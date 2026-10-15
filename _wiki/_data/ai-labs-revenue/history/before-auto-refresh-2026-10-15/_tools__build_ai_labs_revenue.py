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
def build(workbook,asof,template,output):
    w=Workbook(workbook); tracker='ARR Tracker'
    news=json.loads((DATA/'sources.json').read_text(encoding='utf-8-sig'))
    assert len({x['id'] for x in news['observations']})==len(news['observations'])
    for o in news['observations']:
        assert o['source_id'] in news['sources']
        assert news['sources'][o['source_id']]['published']<=asof
    months=[]
    for col in ['C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z','AA']:
        date=(dt.datetime(1899,12,30)+dt.timedelta(days=w.number(tracker,f'{col}3'))).date().isoformat()
        months.append({'date':date,'col':col,'status':'Forecast' if date[:7]>=asof[:7] else 'Model estimate'})
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
        for col in ['Z','AA','AB','AC','AD','AE','AF']:
            if w.value(company,f'{col}{row}') is None: continue
            period=w.value(company,f'{col}1')
            annual.append({'company':company,'period':period,'value':w.number(company,f'{col}{row}'),
                           'basis':'net' if company=='OpenAI' else 'gross','cell':f'{company}!{col}{row}',
                           'status':'Forecast' if 'E' in str(period) else 'Workbook historical'})
    quarterly=[]
    for company,row in [('OpenAI',33),('Anthropic',51)]:
        for col,period in [('R','Q1 2026'),('U','Q2 2026'),('X','Q3 2026')]:
            quarterly.append({'company':company,'period':period,'value':w.number(tracker,f'{col}{row}'),
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
    for company,row in [('OpenAI',11),('Anthropic',44)]:
        total=next(x['value'] for x in annual if x['company']==company and x['period']=='CY26E')
        if abs(w.number(tracker,f'AB{row}')-total)>0.01: raise ValueError(f'{company} annual tie-out failed')
    DATA.mkdir(parents=True,exist_ok=True)
    history=DATA/'history'; history.mkdir(exist_ok=True)
    snapshot=DATA/'model.json'; pretty=json.dumps(payload,ensure_ascii=False,indent=2)+'\n'
    if snapshot.exists() and snapshot.read_text(encoding='utf-8')!=pretty:
        old=snapshot.read_bytes(); prior=history/('model-'+hashlib.sha256(old).hexdigest()[:12]+'.json')
        if not prior.exists(): prior.write_bytes(old)
    snapshot.write_text(pretty,encoding='utf-8')
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
                      f'Revenue: Capstone AI Model · news sources checked {asof} · USD millions')
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
                      'annual_revenue':[x for x in annual if x['period']=='CY26E']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workbook',type=Path,default=DEFAULT_WB)
    p.add_argument('--asof',required=True)
    p.add_argument('--template',type=Path,default=DEFAULT_TEMPLATE)
    p.add_argument('--output',type=Path,default=ROOT/'_dashboards'/'ai-labs')
    a=p.parse_args(); dt.date.fromisoformat(a.asof); build(a.workbook,a.asof,a.template,a.output)

