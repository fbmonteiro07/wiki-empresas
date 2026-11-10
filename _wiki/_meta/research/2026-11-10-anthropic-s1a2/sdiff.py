import difflib, sys, re
def units(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    out, buf = [], []
    def flush():
        if buf:
            txt = ' '.join(buf)
            for s in re.split(r'(?<=[.;:])\s+(?=[A-Z“(•])', txt):
                s = s.strip()
                if s: out.append(s)
            buf.clear()
    for l in lines:
        if '|' in l or re.fullmatch(r'[\divxlcF\-–]+', l.strip()) or len(l) < 3:
            flush()
            if not re.fullmatch(r'[\divxlcF\-–]+', l.strip()):  # drop bare page numbers
                out.append(l.strip())
        else:
            buf.append(l.strip())
    flush()
    return out
a, b = units(sys.argv[1]), units(sys.argv[2])
norm = lambda s: re.sub(r'\s+', ' ', s)
sm = difflib.SequenceMatcher(None, [norm(x) for x in a], [norm(x) for x in b], autojunk=False)
out = []; n=0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal': continue
    A, B = a[i1:i2], b[j1:j2]
    # skip pure page-reference changes
    if re.sub(r'\d+', '#', ' '.join(A)) == re.sub(r'\d+', '#', ' '.join(B)) and len(' '.join(A))<400 and re.findall(r'\d+',' '.join(A))!=[] and all(len(x)<6 for x in re.findall(r'\d[\d,.]*',' '.join(A))) and 'page' in ' '.join(A).lower():
        continue
    n+=1
    ctx = ' / '.join(x[:70] for x in a[max(0,i1-1):i1])
    out.append(f'@@ [{n}] {tag} A{i1} B{j1} ctx: {ctx}')
    out += ['- ' + x for x in A] + ['+ ' + x for x in B]
open(sys.argv[3], 'w', encoding='utf-8').write('\n'.join(out))
print(n, 'hunks', sum(len(x) for x in out), 'chars')
