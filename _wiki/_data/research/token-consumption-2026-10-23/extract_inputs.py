import hashlib, json, zipfile, datetime, re
from pathlib import Path
import xml.etree.ElementTree as E

HERE=Path(__file__).resolve().parent
src=Path(r'P:\Felipe Monteiro\US Equities\Modelos oficiais\AI Model.xlsx')
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
raw=src.read_bytes()
with zipfile.ZipFile(src) as z:
    ss=[''.join(t.itertext()) for t in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
    rel={r.attrib['Id']:r.attrib['Target'] for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    out={'source':str(src),'sha256':hashlib.sha256(raw).hexdigest(),'file_modified':datetime.datetime.fromtimestamp(src.stat().st_mtime).isoformat(),'sheets':{}}
    allnames=[]
    for s in E.fromstring(z.read('xl/workbook.xml')).find('m:sheets',ns):
        name=s.attrib['name'];allnames.append(name)
        if name not in ['ARR Tracker','Anthropic','OpenAI','Premissas ']:continue
        target=rel[s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
        root=E.fromstring(z.read(target.lstrip('/') if target.startswith('/') else 'xl/'+target))
        cells={}
        for c in root.findall('.//m:sheetData/m:row/m:c',ns):
            v=c.findtext('m:v',None,ns);f=c.find('m:f',ns)
            if v is None and f is None:continue
            if c.attrib.get('t')=='s':v=ss[int(v)]
            elif v is not None and c.attrib.get('t')!='e':
                try:v=float(v)
                except ValueError:pass
            cells[c.attrib['r']]={'value':v,'formula':f.text if f is not None else None,'type':c.attrib.get('t'),'style':c.attrib.get('s')}
        out['sheets'][name]=cells
    out['all_sheets']=allnames
(HERE/'arr_source.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='sheets'},ensure_ascii=True))
rows={}
for address,c in out['sheets'].get('ARR Tracker',{}).items():
    row=int(re.search(r'\d+',address)[0]);rows.setdefault(row,{})[address]=c['value']
for row,cells in rows.items():
    print(json.dumps({'row':row,'cells':cells},ensure_ascii=True))
