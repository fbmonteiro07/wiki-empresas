import json,zipfile,xml.etree.ElementTree as E,re,hashlib
from pathlib import Path
P=Path(__file__).parent;w=json.loads((P/'workbook.json').read_text(encoding='utf-8'));n={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
source=Path(r'R:\Modelo Felipe NVDA .xlsx')
with zipfile.ZipFile(source) as z:
    wb=E.fromstring(z.read('xl/workbook.xml'));rels={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',n)]
    s=next(x for x in wb.findall('m:sheets/m:sheet',n) if x.get('name')=='Total rev')
    target=rels[s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')];p=target.lstrip('/') if target.startswith('/') else 'xl/'+target
    root=E.fromstring(z.read(p));selected={}
    for c in root.findall('m:sheetData/m:row/m:c',n):
        a=c.get('r')
        if re.fullmatch(r'(EV|EW|EX|EY|EZ|FA)(7|11|15|17)',a) or re.fullmatch(r'(A|B|C)(7|11|15|17)',a):
            val=c.find('m:v',n);val=val.text if val is not None else None
            if c.get('t')=='s' and val is not None:val=strings[int(val)]
            else:
                try:val=float(val)
                except:pass
            f=c.find('m:f',n);selected[a]={'value':val,'formula':f.text if f is not None else None}
    report={'path':str(source),'selected_source_cells':selected,'reconciliation':[]}
    for dest,src in zip('DEFGHI',['EV','EW','EX','EY','EZ','FA']):
        actual=sum(selected[src+str(r)]['value'] for r in [7,11,15,17]);saved=w['sheets']['Capa DCF - Base']['cells'][dest+'57']['v']
        report['reconciliation'].append({'cell':dest+'57','saved':saved,'linked_workbook_now':actual,'diff':actual-saved})
report['cell_formats']={}
for s,cells in [('Capa DCF - Base',['D88','E88','H99','C42','C43','C46','C47','C48','C51']),('ROIC Cloud',['D7','D12','G27'])]:
    for a in cells:
        cell=w['sheets'][s]['cells'][a];report['cell_formats'][s+'!'+a]=w['styles'][cell['s']]
report['source_unchanged']=hashlib.sha256(Path(w['source']).read_bytes()).hexdigest()==w['sha256']
(P/'source_checks.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))

