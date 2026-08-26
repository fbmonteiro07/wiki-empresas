# -*- coding: utf-8 -*-
"""Diff-aware EOL repair: for every line that survives unchanged from the git-HEAD
version of a file, restore that line's ORIGINAL terminator. New lines keep the
file's dominant terminator. Prevents scripted edits from silently normalising
mixed-EOL wiki pages (see memory: wiki-pages-mixed-line-endings)."""
import difflib, subprocess, sys, os

REPO = r"E:\Wiki Felipe empresas"


def split_keep(b):
    """bytes -> list of (payload_bytes, terminator_bytes)"""
    out = []
    i = 0
    n = len(b)
    start = 0
    while i < n:
        if b[i:i + 2] == b'\r\n':
            out.append((b[start:i], b'\r\n'))
            i += 2
            start = i
        elif b[i:i + 1] == b'\n':
            out.append((b[start:i], b'\n'))
            i += 1
            start = i
        else:
            i += 1
    if start < n:
        out.append((b[start:], b''))
    return out


def dominant(pairs):
    crlf = sum(1 for _, t in pairs if t == b'\r\n')
    lf = sum(1 for _, t in pairs if t == b'\n')
    return b'\r\n' if crlf > lf else b'\n'


def fix(relpath):
    path = os.path.join(REPO, relpath)
    head = subprocess.run(['git', '-C', REPO, 'show', 'HEAD:' + relpath.replace('\\', '/')],
                          capture_output=True).stdout
    cur = open(path, 'rb').read()
    hp = split_keep(head)
    cp = split_keep(cur)
    dom = dominant(hp)
    a = [p for p, _ in hp]
    b = [p for p, _ in cp]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    newterms = [dom] * len(cp)
    restored = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                if newterms[j1 + k] != hp[i1 + k][1]:
                    restored += 1
                newterms[j1 + k] = hp[i1 + k][1]
    # last line: if original file had no trailing newline, respect current state
    if cp and cp[-1][1] == b'':
        newterms[-1] = b''
    out = b''.join(p + t for (p, _), t in zip(cp, newterms))
    if out != cur:
        open(path, 'wb').write(out)
    return restored, out != cur


if __name__ == '__main__':
    for rel in sys.argv[1:]:
        r, changed = fix(rel)
        print('%-40s restored=%d changed=%s' % (rel, r, changed))
