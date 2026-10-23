"""Read-only OOXML checks on the exported workbook."""
import json, math, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

base=Path(__file__).resolve().parent
book=Path('E:/Wiki Felipe empresas/outputs/01a168b5-7786-7582-8082-7cd6bd45fd69/AI_Token_Consumption_and_Minimum_Price.xlsx')
inputs=json.loads((base/'model_inputs.json').read_text(encoding='utf-8'))
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
errors=[]; counts={}; cells={}
with zipfile.ZipFile(book) as z:
    assert z.testzip() is None
    assert not any(p.startswith('xl/externalLinks/') for p in z.namelist())
    for i,name in enumerate(['Consumption','Minimum price','Token mix','Inputs'],1):
        root=ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'))
        cells[name]={c.attrib['r']:c for c in root.findall('.//s:sheetData/s:row/s:c',ns)}
        counts[name]=sum(c.find('s:f',ns) is not None for c in cells[name].values())
        errors.extend((name,a,c.findtext('s:v',default='',namespaces=ns)) for a,c in cells[name].items() if c.attrib.get('t')=='e')
    assert not errors,errors
    def v(sheet,address):
        return float(cells[sheet][address].findtext('s:v',namespaces=ns))
    for e in inputs['monthly_expected']:
        c=chr(67+e['month']);cr=9 if e['provider']=='anthropic' else 27;pr=9 if cr==9 else 25
        for sheet,address,expected in [('Consumption',c+str(cr+8),e['base_gross_tokens_Q_month']),('Consumption',c+str(cr+9),e['api_gross_tokens_Q_month']),('Minimum price',c+str(pr+3),e['minimum_reference']),('Minimum price',c+str(pr+5),e['reference_gross_tokens_Q_month'])]:
            assert math.isclose(v(sheet,address),expected,rel_tol=1e-9), (sheet,address,v(sheet,address),expected)
    for col in 'DEFGHIJKLMNO':
        for row in (16,27):assert math.isclose(v('Token mix',f'{col}{row}'),1,abs_tol=1e-12)
    for col in 'DEFGHIJKLM':
        for row in (272,273):assert abs(v('Inputs',f'{col}{row}'))<.1
    assert v('Inputs','D4')==1 and v('Inputs','D5')==0
report={'workbook':str(book),'size_bytes':book.stat().st_size,'formula_counts':counts,'errors':errors,'cached_outputs':'96 outputs match prepared monthly calculations','mix_totals':'All 24 provider-month shares equal 100%','external_links':0,'input_defaults':'Gross ARR; November/December price change 0%'}
(base/'export_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
