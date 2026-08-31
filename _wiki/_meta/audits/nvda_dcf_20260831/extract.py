import zipfile, xml.etree.ElementTree as ET, json, re, collections, pathlib, hashlib
SOURCE=pathlib.Path(r'P:\Felipe Monteiro\US Equities\Modelos oficiais\Template DCF NVDA.xlsx')
OUT=pathlib.Path(__file__).parent
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RN='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
def ci(c):
    out=0
    for x in c: out=out*26+ord(x)-64
    return out
def cl(n):
    s=''
    while n:
        n,r=divmod(n-1,26); s=chr(65+r)+s
    return s
def shift(f,anchor,target):
    a=re.fullmatch(r'([A-Z]+)(\d+)',anchor); t=re.fullmatch(r'([A-Z]+)(\d+)',target)
    dc,dr=ci(t[1])-ci(a[1]),int(t[2])-int(a[2])
    def sub(m):
        ca,c,ra,r=m.groups()
        return ca+(c if ca else cl(ci(c)+dc))+ra+str(int(r)+(0 if ra else dr))
    pieces=re.split(r'("(?:[^"]|"")*")',f)
    return ''.join(p if i%2 else re.sub(r'(?<![\w.])([$]?)([A-Z]{1,3})([$]?)(\d+)(?![\w(])',sub,p) for i,p in enumerate(pieces))
data={'source':str(SOURCE),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'sheets':{}}
with zipfile.ZipFile(SOURCE) as z:
    strings=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        strings=[''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',N)]
    w=ET.fromstring(z.read('xl/workbook.xml'))
    rels={x.get('Id'):x.get('Target') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    data['names']=[dict(x.attrib,value=x.text) for x in w.findall('m:definedNames/m:definedName',N)]
    calc=w.find('m:calcPr',N)
    data['calc_properties']=calc.attrib if calc is not None else {}
    data['links']={p:z.read(p).decode('utf-8') for p in z.namelist() if ('externalLink' in p and p.endswith('.rels')) or p=='xl/connections.xml'}
    data['metadata']={p:z.read(p).decode('utf-8') for p in ('docProps/core.xml','docProps/app.xml') if p in z.namelist()}
    styles=ET.fromstring(z.read('xl/styles.xml'))
    fmts={int(x.get('numFmtId')):x.get('formatCode') for x in styles.findall('m:numFmts/m:numFmt',N)}
    data['styles']=[dict(x.attrib,format=fmts.get(int(x.get('numFmtId','0')))) for x in styles.findall('m:cellXfs/m:xf',N)]
    for s in w.findall('m:sheets/m:sheet',N):
        target=rels[s.get(RN)]
        p=target.lstrip('/') if target.startswith('/') else 'xl/'+target
        root=ET.fromstring(z.read(p)); cells={}; shared={}; pending=[]
        for c in root.findall('m:sheetData/m:row/m:c',N):
            f=c.find('m:f',N); v=c.find('m:v',N); val=v.text if v is not None else None
            typ=c.get('t','n')
            if typ=='s' and val is not None: val=strings[int(val)]
            elif typ=='inlineStr': val=''.join(c.find('m:is',N).itertext())
            elif typ=='n' and val is not None:
                try: val=float(val); val=int(val) if val.is_integer() else val
                except ValueError: pass
            d={'v':val,'t':typ,'s':int(c.get('s','0'))}
            if f is not None:
                d['f']=f.text or ''; d['fa']=dict(f.attrib)
                if f.get('t')=='shared':
                    if f.text: shared[f.get('si')]=(c.get('r'),f.text)
                    else: pending.append((c.get('r'),f.get('si')))
            if val is not None or f is not None: cells[c.get('r')]=d
        for addr,si in pending:
            anchor,form=shared[si]; cells[addr]['f']=shift(form,anchor,addr)
        data['sheets'][s.get('name')]={'state':s.get('state','visible'),'dimension':root.find('m:dimension',N).get('ref'),'cells':cells,'hidden_rows':[x.get('r') for x in root.findall('m:sheetData/m:row',N) if x.get('hidden')=='1'],'columns':[x.attrib for x in root.findall('m:cols/m:col',N)],'merges':[x.get('ref') for x in root.findall('m:mergeCells/m:mergeCell',N)],'conditional_formulas':[x.text for x in root.findall('m:conditionalFormatting/m:cfRule/m:formula',N)]}
    data['comments']={p:z.read(p).decode('utf-8') for p in z.namelist() if re.search(r'(comments|threadedComment).*\.xml$',p,re.I)}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'workbook.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
summary={k:v for k,v in data.items() if k not in ('sheets','styles','comments','names','links')}
summary['names_count']=len(data['names'])
summary['links_count']=len(data['links'])
summary['sheets']=[]
for name,s in data['sheets'].items():
    funcs=collections.Counter(x.upper() for d in s['cells'].values() for x in re.findall(r'([A-Za-z_][A-Za-z_0-9.]*)\s*\(',d.get('f','')))
    errors=[(a,d['v']) for a,d in s['cells'].items() if d['t']=='e']
    summary['sheets'].append({'name':name,'dimension':s['dimension'],'state':s['state'],'cells':len(s['cells']),'formulas':sum('f' in d for d in s['cells'].values()),'error_count':len(errors),'errors_first20':errors[:20],'functions':dict(funcs),'hidden_rows':s['hidden_rows'],'formula_types':dict(collections.Counter(d.get('fa',{}).get('t','normal') for d in s['cells'].values() if 'f' in d))})
    rows=collections.defaultdict(list)
    for a,d in s['cells'].items(): rows[int(re.search(r'\d+',a)[0])].append((a,d))
    lines=[]
    for r,items in sorted(rows.items()):
        lines.append('\t'.join(a+' '+str(d['v'])+(' [='+d['f']+']' if 'f' in d else '') for a,d in items))
    (OUT/(re.sub(r'[^A-Za-z0-9_-]','_',name)+'.txt')).write_text('\n'.join(lines),encoding='utf-8')
(OUT/'inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))

