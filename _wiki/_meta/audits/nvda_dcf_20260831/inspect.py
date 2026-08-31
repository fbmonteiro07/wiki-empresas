import json,sys,re
from pathlib import Path
w=json.loads((Path(__file__).parent/'workbook.json').read_text(encoding='utf-8'))
name=sys.argv[1]; rows=sys.argv[2]; cols=sys.argv[3] if len(sys.argv)>3 else ''
allowed=set()
for r in rows.split(','):
    a,*b=r.split('-'); allowed.update(range(int(a),int(b[0] if b else a)+1))
cc=set(cols.split(','))
for a,d in w['sheets'][name]['cells'].items():
    col,row=re.fullmatch(r'([A-Z]+)(\d+)',a).groups()
    if int(row) in allowed and (not cols or col in cc):
        print(a,repr(d['v']),('='+d['f'] if 'f' in d else ''),str(d.get('fa','')))

