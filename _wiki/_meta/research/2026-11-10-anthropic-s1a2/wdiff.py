import re, sys, difflib
t = open(sys.argv[1], encoding='utf-8').read()
hs = re.split(r'\n(?=@@ )', t)
out = []
for h in hs:
    lines = h.split('\n')
    head = lines[0]
    A = ' '.join(l[2:] for l in lines[1:] if l.startswith('- '))
    B = ' '.join(l[2:] for l in lines[1:] if l.startswith('+ '))
    aw, bw = A.split(), B.split()
    sm = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
    segs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': continue
        old = ' '.join(aw[i1:i2]); new = ' '.join(bw[j1:j2])
        pre = ' '.join(aw[max(0,i1-8):i1]); post = ' '.join(aw[i2:i2+6])
        segs.append(f'  …{pre} [-{old}-]{{+{new}+}} {post}…')
    if segs:
        out.append(head.split(' ctx:')[0])
        out += segs
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(out))
print(len(out), sum(len(x) for x in out))
