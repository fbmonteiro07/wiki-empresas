import hashlib, json, pathlib, zipfile, xml.etree.ElementTree as E
src = pathlib.Path(r'P:\Felipe Monteiro\US Equities\Modelos oficiais\AI Model.xlsx')
out = pathlib.Path(__file__).parent
ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
raw = src.read_bytes()
z = zipfile.ZipFile(src)
ss = [''.join(t.itertext()) for t in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', ns)]
rels = {r.attrib['Id']: r.attrib['Target'] for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
data = {'source': str(src), 'sha256': hashlib.sha256(raw).hexdigest(), 'asof': '2026-10-15', 'sheets': {}}
for s in E.fromstring(z.read('xl/workbook.xml')).find('m:sheets', ns):
    name = s.attrib['name']
    if name not in ['Anthropic', 'ARR Tracker', 'Deals Anthropic', 'Premissas ', 'Resumo |  Economics GW']:
        continue
    target = rels[s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
    root = E.fromstring(z.read(target.lstrip('/') if target.startswith('/') else 'xl/' + target))
    cells = {}
    for c in root.findall('.//m:sheetData/m:row/m:c', ns):
        v = c.findtext('m:v', None, ns)
        f = c.find('m:f', ns)
        if v is None and f is None:
            continue
        if c.attrib.get('t') == 's':
            v = ss[int(v)]
        elif v is not None and c.attrib.get('t') != 'e':
            try:
                v = float(v)
            except ValueError:
                pass
        cells[c.attrib['r']] = {'value': v, 'formula': f.text if f is not None else None, 'formula_attributes': f.attrib if f is not None else None}
    data['sheets'][name] = cells
(out / 'source_extract.json').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'source': data['source'], 'sha256': data['sha256']}, ensure_ascii=True))
cells = data['sheets']['Anthropic']
for row in range(33, 149):
    label = cells.get('A'+str(row), {}).get('value')
    vals = {col: cells.get(col+str(row), {}).get('value') for col in ['Z','AA','AB','AC','AD','AE','AF']}
    if label or any(v is not None for v in vals.values()):
        print(json.dumps({'row': row, 'label': label, 'values': vals}, ensure_ascii=True))
