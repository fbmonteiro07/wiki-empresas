import base64,json
from pathlib import Path
p=Path('_wiki/_data/financials/email_review_2026-11-01')
ids=[]
for i in range(33):
    parts=sorted(p.glob(f'{i:02d}.b64part*'))
    assert parts,(i,'missing chunks')
    raw=base64.b64decode(''.join(x.read_text(encoding='ascii').strip() for x in parts))
    obj=json.loads(raw.decode('utf-8'))
    ids.append(obj['id'])
    (p/f'{i:02d}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(set(ids))==33
print('Decoded and validated 33 unique Outlook messages.')
print('First message fields:',list(obj))
