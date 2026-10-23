"""Read-only check: references added without changing the original model."""
import json, math, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
base=Path('E:/Wiki Felipe empresas/outputs/01a168b5-7786-7582-8082-7cd6bd45fd69')
source=base/'AI_Token_Consumption_and_Minimum_Price.xlsx'
output=base/'AI_Token_Consumption_and_Minimum_Price_with_References.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def load(p):
    z=zipfile.ZipFile(p);assert z.testzip() is None
    ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():ss=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))]
    assert not any('not implemented' in t for t in ss)
    styles=ET.fromstring(z.read('xl/styles.xml'))
    tables={e.tag.split('}')[-1]:list(e) for e in styles}
    def tree(e):return(e.tag,tuple(sorted(e.attrib.items())),e.text or '',tuple(tree(c) for c in e))
    def style(i):
        xf=tables['cellXfs'][i];attrs=dict(xf.attrib)
        for k,t in [('fontId','fonts'),('fillId','fills'),('borderId','borders')]:
            attrs[k]=tree(tables[t][int(attrs.get(k,0))])
        nf=int(attrs.get('numFmtId',0))
        if nf>=164:attrs['numFmtId']=next(x.attrib['formatCode'] for x in tables['numFmts'] if int(x.attrib['numFmtId'])==nf)
        return(tuple(sorted(attrs.items())),tuple(tree(c) for c in xf))
    sheets=[];errors=[]
    for i in range(1,6):
        name=f'xl/worksheets/sheet{i}.xml'
        if name not in z.namelist():continue
        root=ET.fromstring(z.read(name));cells={}
        for c in root.findall('.//s:sheetData/s:row/s:c',ns):
            t=c.attrib.get('t','n');v=c.findtext('s:v',default=None,namespaces=ns)
            if t=='s':v=ss[int(v)]
            elif t=='inlineStr':v=''.join(c.find('s:is',ns).itertext())
            elif t=='n' and v is not None:v=float(v)
            if t=='e':errors.append((i,c.attrib['r'],v))
            cells[c.attrib['r']]=(v,c.findtext('s:f',default=None,namespaces=ns),style(int(c.attrib.get('s',0))))
        meta={tag:[tree(x) for x in root.findall('s:'+tag,ns)] for tag in ['dataValidations','conditionalFormatting','sheetViews','cols','mergeCells']}
        sheets.append((cells,meta))
    return sheets,errors

old,oe=load(source);new,ne=load(output)
assert len(old)==4 and len(new)==5
assert not oe and not ne,(oe,ne)
diff=[]
for i in range(4):
    a,am=old[i];b,bm=new[i]
    for cell,x in a.items():
        y=b.get(cell)
        if y is None:diff.append((i+1,cell,'missing'));continue
        if isinstance(x[0],float) and isinstance(y[0],float):same=math.isclose(x[0],y[0],rel_tol=1e-12,abs_tol=1e-10)
        else:same=x[0]==y[0]
        if not same or x[1:]!=y[1:]:diff.append((i+1,cell,'value/formula/style'))
    for tag in am:
        if am[tag]!=bm[tag]:diff.append((i+1,tag,'sheet setting'))
assert not diff,diff[:20]
refs=json.loads(Path(__file__).with_name('price_references.json').read_text(encoding='utf8'))
sheet=new[4][0]
for start,kind in [(10,'history'),(30,'current'),(49,'modifiers')]:
    for j,row in enumerate(refs[kind]):
        for k,col in enumerate('GHI',4):
            expected='n.q.' if row[k] is None else row[k]
            assert sheet[f'{col}{start+j}'][0]==expected,(kind,j,col)
        assert row[2]==sheet[f'E{start+j}'][0]
for title,url in refs['sources'].values():assert any(v[0]==url for v in sheet.values())
report={'original_tabs_preserved':True,'preserved':'Values, formulas, cell styles, column settings, sheet views, validations and conditional formats','reference_rows':37,'source_urls':len(refs['sources']),'errors':[],'output':str(output)}
Path(__file__).with_name('reference_export_verification.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
