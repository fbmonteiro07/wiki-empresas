# -*- coding: utf-8 -*-
"""EOL-preserving, additive-only insert helper for /wiki-ingest scripted patches."""
import io, os, sys

def _eol(raw):
    return '\r\n' if raw.count(b'\r\n') > raw.count(b'\n') - raw.count(b'\r\n') else '\n'

def load(path):
    raw = open(path, 'rb').read()
    return raw.decode('utf-8'), _eol(raw)

def save(path, text, eol):
    body = text.replace('\r\n', '\n')
    if eol == '\r\n':
        body = body.replace('\n', '\r\n')
    open(path, 'wb').write(body.encode('utf-8'))

def insert_after(path, anchor, block, occurrence=1):
    """Insert `block` (LF-separated) immediately after the line containing `anchor`."""
    text, eol = load(path)
    lines = text.split(eol)
    hit = 0
    for i, ln in enumerate(lines):
        if anchor in ln:
            hit += 1
            if hit == occurrence:
                new = block.rstrip('\n').split('\n')
                lines[i+1:i+1] = new
                save(path, eol.join(lines), eol)
                return True
    raise SystemExit(f'ANCHOR NOT FOUND in {path}: {anchor!r} (occurrence {occurrence})')

def insert_before(path, anchor, block, occurrence=1):
    text, eol = load(path)
    lines = text.split(eol)
    hit = 0
    for i, ln in enumerate(lines):
        if anchor in ln:
            hit += 1
            if hit == occurrence:
                new = block.rstrip('\n').split('\n')
                lines[i:i] = new
                save(path, eol.join(lines), eol)
                return True
    raise SystemExit(f'ANCHOR NOT FOUND in {path}: {anchor!r} (occurrence {occurrence})')

def append_end(path, block):
    text, eol = load(path)
    lines = text.split(eol)
    lines += block.rstrip('\n').split('\n')
    save(path, eol.join(lines), eol)
    return True
