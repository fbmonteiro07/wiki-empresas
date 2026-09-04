import sys
# usage: _ins.py <target.md> <payload.txt> <anchor.txt> <before|after>
tgt, pay, anc, mode = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
raw = open(tgt, 'rb').read().decode('utf-8')
anchor = open(anc, encoding='utf-8').read().replace('\r\n', '\n').rstrip('\n')
payload = open(pay, encoding='utf-8').read().replace('\r\n', '\n').rstrip('\n')

CRLF = '\r\n'
crlf = raw.count(CRLF)
lf = raw.count('\n') - crlf
eol = CRLF if crlf >= lf else '\n'

flat = raw.replace(CRLF, '\n')
if flat.count(anchor) != 1:
    print('ERR anchor count=%d' % flat.count(anchor))
    sys.exit(2)

i = flat.index(anchor)
if mode == 'after':
    j = i + len(anchor)
    new = flat[:j] + '\n' + payload + flat[j:]
else:
    new = flat[:i] + payload + '\n' + flat[i:]

open(tgt, 'wb').write(new.replace('\n', eol).encode('utf-8'))
print('OK %s +%d lines (eol=%s)' % (tgt, payload.count('\n') + 1, 'CRLF' if eol == CRLF else 'LF'))
