import json, zipfile, posixpath, re
import xml.etree.ElementTree as E
from pathlib import Path

OUT=Path(__file__).parent
N={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
R='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
BASE=Path(r'P:\Felipe Monteiro\US Equities\Modelos oficiais')
def extract(path,selected=None):
    z=zipfile.ZipFile(path)
    ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        ss=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
    rel={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    result={'path':str(path),'modified':path.stat().st_mtime,'sheets':{},'names':[]}
    w=E.fromstring(z.read('xl/workbook.xml'))
    for el in w.findall('s:definedNames/s:definedName',N): result['names'].append(dict(el.attrib,text=el.text))
    result['calc']=dict(w.find('s:calcPr',N).attrib) if w.find('s:calcPr',N) is not None else {}
    for sh in w.findall('s:sheets/s:sheet',N):
        name=sh.get('name')
        if selected and name not in selected: continue
        target=rel[sh.get(R)]
        target=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
        root=E.fromstring(z.read(target)); cells={}
        for c in root.findall('.//s:sheetData/s:row/s:c',N):
            v=c.find('s:v',N); f=c.find('s:f',N); val=v.text if v is not None else None
            if c.get('t')=='s': val=ss[int(val)] if val else None
            elif c.get('t')=='inlineStr': val=''.join(c.find('s:is',N).itertext())
            elif val is not None:
                try: val=float(val); val=int(val) if val.is_integer() else val
                except ValueError: pass
            if val is not None or f is not None: cells[c.get('r')]={'v':val,'f': f.text if f is not None else None,'fa':dict(f.attrib) if f is not None else None,'s':c.get('s'),'t':c.get('t')}
        result['sheets'][name]={'cells':cells,'dimension':root.find('s:dimension',N).get('ref'),'cols':E.tostring(root.find('s:cols',N),encoding='unicode') if root.find('s:cols',N) is not None else '', 'merges':[x.get('ref') for x in root.findall('s:mergeCells/s:mergeCell',N)]}
    return result

if __name__=='__main__':
    for key,filename,selected in [('mu','Modelo Micron.xlsx',None),('tsm_template','Template DCF TSM.xlsx',None),('tsm_current','Modelo Felipe TSM 3Q26 DCF versão final.xlsm',['DCF'])]:
        data=extract(BASE/filename,selected)
        (OUT/(key+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        lines=[]
        for name,s in data['sheets'].items():
            lines.append('\nSHEET '+name+' '+s['dimension'])
            rows={}
            for addr,c in s['cells'].items(): rows.setdefault(int(re.search(r'\d+',addr)[0]),[]).append((addr,c))
            for row,cs in rows.items(): lines.append(' | '.join(a+': '+str(c['v'])+(' [='+str(c['f'])+']' if c['f'] else '') for a,c in cs))
        (OUT/(key+'_rows.txt')).write_text('\n'.join(lines),encoding='utf-8')
        print(key,[(n,s['dimension'],len(s['cells'])) for n,s in data['sheets'].items()],data['calc'])
