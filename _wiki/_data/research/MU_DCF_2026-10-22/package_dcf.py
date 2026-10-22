"""Graft the Artifact Tool-authored DCF into the original workbook losslessly.

The generated workbook contains a cached-values MU stub solely for calculation.
Only its DCF worksheet and required style records are copied. Original sheet XML,
shared strings, relationships, cached data tables and external links stay intact.
"""
import copy, hashlib, json, zipfile, io, re
import xml.etree.ElementTree as E
from pathlib import Path

BASE=Path(r'P:\Felipe Monteiro\US Equities\Modelos oficiais\Modelo Micron.xlsx')
WORK=Path(r'C:\Users\Felipe.monteiro\.codex\visualizations\2026\10\22\01a1657d-c2e7-7bc0-aebf-c2ad321bca6e\mu_dcf')
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'outputs'/'01a1657d-c2e7-7bc0-aebf-c2ad321bca6e'/'Modelo Micron - DCF.xlsx'
S='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R='http://schemas.openxmlformats.org/package/2006/relationships'
OR='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
ns={'s':S}; E.register_namespace('',S);E.register_namespace('r',OR)
def xml(b):return E.fromstring(b)
def dump(e,original=None):
    namespaces=[]
    if original:
        namespaces=list(dict.fromkeys(pair for event,pair in E.iterparse(io.BytesIO(original),events=['start-ns'])))
        for prefix,uri in namespaces:
            if not re.match(r'ns\d+$',prefix):E.register_namespace(prefix,uri)
    b=E.tostring(e,encoding='utf-8',xml_declaration=True)
    # Preserve namespace declarations referenced only in mc:Ignorable / extension attributes.
    for prefix,uri in namespaces:
        name='xmlns'+(':'+prefix if prefix else '')
        if (name+'=').encode() not in b:
            start=b.index(b'>',b.index(b'?>')+2)
            b=b[:start]+(' '+name+'="'+uri+'"').encode()+b[start:]
    return b

def main():
    old=zipfile.ZipFile(BASE);new=zipfile.ZipFile(WORK/'dcf_generated.xlsx')
    styles=xml(old.read('xl/styles.xml'));newstyles=xml(new.read('xl/styles.xml'))
    maps={}
    for group in ['numFmts','fonts','fills','borders','cellStyleXfs','cellXfs','dxfs']:
        src=newstyles.find('s:'+group,ns)
        dst=styles.find('s:'+group,ns)
        if dst is None:
            dst=E.Element('{'+S+'}'+group,{'count':'0'})
            order=['numFmts','fonts','fills','borders','cellStyleXfs','cellXfs','cellStyles','dxfs','tableStyles','colors','extLst']
            idx=next((i for i,e in enumerate(styles) if order.index(e.tag.split('}')[-1])>order.index(group)),len(styles))
            styles.insert(idx,dst)
        maps[group]={}
        if src is None: continue
        if group=='numFmts':
            ids=[int(e.get('numFmtId')) for e in dst];nextid=max([163]+ids)+1
            for e in src:
                dup=next((x for x in dst if x.get('formatCode')==e.get('formatCode')),None)
                if dup is not None:maps[group][int(e.get('numFmtId'))]=int(dup.get('numFmtId'))
                else:
                    x=copy.deepcopy(e);maps[group][int(e.get('numFmtId'))]=nextid;x.set('numFmtId',str(nextid));nextid+=1;dst.append(x)
        else:
            for i,e in enumerate(src):
                x=copy.deepcopy(e)
                for attr,ref in [('fontId','fonts'),('fillId','fills'),('borderId','borders'),('xfId','cellStyleXfs'),('numFmtId','numFmts')]:
                    if attr in x.attrib and int(x.get(attr)) in maps.get(ref,{}):x.set(attr,str(maps[ref][int(x.get(attr))]))
                maps[group][i]=len(dst);dst.append(x)
        dst.set('count',str(len(dst)))
    sheet=xml(new.read('xl/worksheets/sheet1.xml'))
    strings=list(xml(new.read('xl/sharedStrings.xml'))) if 'xl/sharedStrings.xml' in new.namelist() else []
    for c in sheet.findall('.//s:c',ns):
        if 's' in c.attrib:c.set('s',str(maps['cellXfs'][int(c.get('s'))]))
        if c.get('t')=='s':
            v=c.find('s:v',ns);content=copy.deepcopy(strings[int(v.text)]);content.tag='{'+S+'}is';c.remove(v);c.append(content);c.set('t','inlineStr')
    for row in sheet.findall('.//s:row',ns):
        if 's' in row.attrib:row.set('s',str(maps['cellXfs'][int(row.get('s'))]))
    for c in sheet.findall('s:cols/s:col',ns):
        if 'style' in c.attrib:c.set('style',str(maps['cellXfs'][int(c.get('style'))]))
    for r in sheet.findall('.//s:cfRule',ns):
        if 'dxfId' in r.attrib:r.set('dxfId',str(maps['dxfs'][int(r.get('dxfId'))]))
    workbook=xml(old.read('xl/workbook.xml'));sheets=workbook.find('s:sheets',ns)
    rels=xml(old.read('xl/_rels/workbook.xml.rels'))
    nextsheet=max(int(sh.get('sheetId')) for sh in sheets)+1
    nextrel=max(int(r.get('Id').replace('rId','')) for r in rels if r.get('Id').startswith('rId'))+1
    path='xl/worksheets/sheet_dcf_memory.xml'
    sheets.insert(0,E.Element('{'+S+'}sheet',{'name':'DCF Memory','sheetId':str(nextsheet),'{'+OR+'}id':'rId'+str(nextrel)}))
    E.SubElement(rels,'{'+R+'}Relationship',{'Id':'rId'+str(nextrel),'Type':OR+'/worksheet','Target':'worksheets/sheet_dcf_memory.xml'})
    for n in workbook.findall('s:definedNames/s:definedName',ns):
        if 'localSheetId' in n.attrib:n.set('localSheetId',str(int(n.get('localSheetId'))+1))
    for view in workbook.findall('s:bookViews/s:workbookView',ns):view.set('activeTab','0');view.set('firstSheet','0')
    calc=workbook.find('s:calcPr',ns)
    if calc is not None:calc.set('fullCalcOnLoad','1');calc.set('forceFullCalc','1')
    types=xml(old.read('[Content_Types].xml'))
    E.SubElement(types,'{'+CT+'}Override',{'PartName':'/'+path,'ContentType':'application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'})
    # calcChain can be rebuilt by Excel; the original dependency chain lacks the new sheet.
    remove={'xl/calcChain.xml'}
    for r in list(rels):
        if r.get('Type','').endswith('/calcChain'):rels.remove(r)
    for t in list(types):
        if t.get('PartName')=='/xl/calcChain.xml':types.remove(t)
    changed={name:dump(e,old.read(name)) for name,e in [('xl/styles.xml',styles),('xl/workbook.xml',workbook),('xl/_rels/workbook.xml.rels',rels),('[Content_Types].xml',types)]}
    changed[path]=dump(sheet,new.read('xl/worksheets/sheet1.xml'))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
        for info in old.infolist():
            if info.filename not in remove:z.writestr(copy.copy(info),changed.pop(info.filename,old.read(info.filename)))
        for name,contents in changed.items():z.writestr(name,contents)
    saved=zipfile.ZipFile(OUT)
    allowed={'xl/styles.xml','xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml'}|remove
    assert all(old.read(n)==saved.read(n) for n in old.namelist() if n not in allowed)
    assert saved.testzip() is None
    for n in saved.namelist():
        if n.endswith('.xml') or n.endswith('.rels'):xml(saved.read(n))
    assert len(saved.namelist())==len(old.namelist())+1-int('xl/calcChain.xml' in old.namelist())
    report={'output':str(OUT),'original_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'preserved_original_sheets':5,'new_sheets':1,'native_dcf_data_tables':len(sheet.findall('.//s:f[@t="dataTable"]',ns)),'all_original_sheet_parts_identical':True,'bytes':OUT.stat().st_size}
    (WORK/'preservation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
if __name__=='__main__':main()
