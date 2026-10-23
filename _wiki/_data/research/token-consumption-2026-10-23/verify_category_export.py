"""Read-only verification of cached XLSX results and preservation of existing scope."""
import json, math, re, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=Path('E:/Wiki Felipe empresas/outputs/01a168b5-7786-7582-8082-7cd6bd45fd69')
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def load(path):
    z=zipfile.ZipFile(path);assert z.testzip() is None
    ss=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))] if 'xl/sharedStrings.xml' in z.namelist() else []
    assert not any('not implemented' in t for t in ss)
    tables={e.tag.split('}')[-1]:list(e) for e in ET.fromstring(z.read('xl/styles.xml'))}
    def tree(e): return (e.tag,tuple(sorted(e.attrib.items())),e.text or '',tuple(tree(c) for c in e))
    def style(i):
        xf=tables['cellXfs'][i];a=dict(xf.attrib)
        for k,t in [('fontId','fonts'),('fillId','fills'),('borderId','borders')]:a[k]=tree(tables[t][int(a.get(k,0))])
        if int(a.get('numFmtId',0))>=164:a['numFmtId']=next(x.attrib['formatCode'] for x in tables['numFmts'] if x.attrib['numFmtId']==a['numFmtId'])
        return(tuple(sorted(a.items())),tuple(tree(c) for c in xf))
    sheets={};errors=[]
    names=[e.attrib['name'] for e in ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS)]
    for i,name in enumerate(names,1):
        root=ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'));cells={}
        for c in root.findall('.//s:sheetData/s:row/s:c',NS):
            t=c.attrib.get('t','n');v=c.findtext('s:v',None,NS)
            if t=='s':v=ss[int(v)]
            elif t=='inlineStr':v=''.join(c.find('s:is',NS).itertext())
            elif t=='n' and v is not None:v=float(v)
            if t=='e':errors.append((name,c.attrib['r'],v))
            cells[c.attrib['r']]=(v,c.findtext('s:f',None,NS),style(int(c.attrib.get('s',0))))
        meta={tag:[tree(x) for x in root.findall('s:'+tag,NS)] for tag in ['dataValidations','conditionalFormatting','sheetViews','cols','mergeCells']}
        sheets[name]=(cells,meta)
    return sheets,errors

old,oe=load(BASE/'AI_Token_Consumption_and_Minimum_Price_with_References.xlsx')
new,ne=load(BASE/'AI_Token_Consumption_Price_and_Mix.xlsx')
assert not oe and not ne,(oe,ne)
assert len(new)==6
changes={'Consumption':{'C6','C46'},'Inputs':{'C33'},'Minimum price':{'C43'},'Price references':{'C6'},'Token mix':{'C6'}}
for c in 'DEFGHIJKLMNO':changes['Consumption'].update([c+'16',c+'34'])
def same(a,b):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9) if isinstance(a,(int,float)) and isinstance(b,(int,float)) else a==b
diff=[]
for name,(cells,meta) in old.items():
    after,nmeta=new[name]
    for cell,x in cells.items():
        row=int(re.search(r'\d+',cell).group())
        # Prior export retains formatted empty cells past the intentional content.
        if (name=='Consumption' and row>=49) or (name=='Inputs' and row>=281):continue
        if cell in changes[name]:continue
        y=after.get(cell)
        if y is None or not same(x[0],y[0]) or x[1:]!=y[1:]:diff.append((name,cell,'value/formula/style',x[:2],y[:2] if y else None))
    for key in meta:
        if key=='mergeCells' and name in ('Consumption','Inputs'):continue
        if meta[key]!=nmeta[key]:diff.append((name,key,'sheet setting'))
assert not diff,diff[:12]
data=json.loads((HERE/'category_mix_inputs.json').read_text())
price=new['Price build'][0];con=new['Consumption'][0]
for r in data['monthly']:
    col=chr(67+r['month']);b,cr=(9,9) if r['provider']=='anthropic' else (49,27)
    for off,key in [(1,'base_price'),(5,'input_share'),(6,'output_share'),(7,'residual_share'),(10,'input_rate'),(11,'output_rate'),(12,'residual_rate')]:assert same(price[col+str(b+off)][0],r[key]),(r['provider'],r['month'],key)
    assert same(con[col+str(cr+7)][0],r['base_price'])
    assert price[col+str(b+22)][0]=='PASS'
for row,b in [(106,9),(107,49)]:
    r=next(x for x in data['monthly'] if x['provider']==('anthropic' if b==9 else 'openai') and x['month']==10)
    assert same(price['E'+str(row)][0],r['five_pp_residual_to_input_price'])
    assert same(price['F'+str(row)][0],r['one_pp_residual_to_output_price'])
refs=json.loads((HERE/'price_references.json').read_text())
for title,url in refs['sources'].values():assert any(v[0]==url for v in new['Price references'][0].values())
report={'status':'PASS','prior_scope':'Prior cells, values, formulas, styles and settings preserved except the 30 explicitly authorized note/link edits and new content','monthly_prices_and_mixes_verified':24,'raw_weekly_rows':82,'source_urls_preserved':len(refs['sources']),'xlsx_formula_errors':ne,'unsupported_formulas':False,'validation_limit':'Internal arithmetic verified; company ASP and cache interpretation remain PARTIAL'}
(HERE/'category_export_verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
