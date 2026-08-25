"""Line-ending-safe wiki patcher. INSERTS ONLY; never rewrites existing lines.

Why byte-level: several wiki pages are legitimately MIXED CRLF/LF (they were built
by different tools over time). Reading to str, splitting on '\n' and re-joining with
one chosen EOL silently rewrites every line whose terminator differed -- which shows
up as a large phantom diff that buries the real change. So every mode here keeps each
surviving line's ORIGINAL terminator and only stamps the file's DOMINANT terminator
onto the newly inserted lines.

Also: always encode BEFORE opening the target for write. open(path,'wb') truncates
immediately, so an encoding error after opening leaves a zero-byte file.
"""
import sys, io

NL = chr(10)


def _load(path):
    """-> (list_of_lines_with_their_own_terminators_as_bytes, dominant_eol_bytes)"""
    with open(path, 'rb') as fh:
        raw = fh.read()
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    eol = b"\r\n" if crlf >= lf else b"\n"
    return raw.splitlines(keepends=True), eol


def _save(path, parts):
    data = b"".join(parts)          # encode/assemble first, then open
    with open(path, 'wb') as fh:
        fh.write(data)


def _text(line_bytes):
    return line_bytes.decode('utf-8').rstrip("\r\n")


def _mk(block, eol):
    """Render an inserted block as byte-lines stamped with the dominant EOL."""
    body = block.replace("\r\n", NL).rstrip(NL).split(NL)
    return [(l + eol.decode('utf-8')).encode('utf-8') for l in body]


def _section(parts, header):
    """Return (start_index_of_header_line, end_index_exclusive)."""
    h = header.strip()
    s = None
    for i, ln in enumerate(parts):
        if _text(ln).strip() == h:
            s = i
            break
    if s is None:
        raise SystemExit('HEADER NOT FOUND: ' + header)
    lvl = len(h) - len(h.lstrip('#'))
    e = len(parts)
    for j in range(s + 1, len(parts)):
        t = _text(parts[j])
        if t.startswith('#'):
            k = len(t) - len(t.lstrip('#'))
            if k <= lvl:
                e = j
                break
    return s, e


def _splice(path, parts, at, ins):
    _save(path, parts[:at] + ins + parts[at:])


def append_end(path, header, block):
    parts, eol = _load(path)
    s, e = _section(parts, header)
    k = e
    while k > s + 1 and _text(parts[k - 1]).strip() == '':
        k -= 1
    _splice(path, parts, k, _mk('' + NL + block, eol))
    print('OK append_end', path, '@line', k + 1)


def insert_top(path, header, block, skip=1):
    """Insert after the header line, skipping `skip` non-blank lines (e.g. an italic subtitle)."""
    parts, eol = _load(path)
    s, e = _section(parts, header)
    p, cnt = s + 1, 0
    while p < e and cnt < skip:
        if _text(parts[p]).strip() == '':
            p += 1
            continue
        p += 1
        cnt += 1
    _splice(path, parts, p, _mk('' + NL + block, eol))
    print('OK insert_top', path, '@line', p + 1)


def after_table(path, header, rows):
    """Append rows after the LAST markdown table row inside the section."""
    parts, eol = _load(path)
    s, e = _section(parts, header)
    last = None
    for j in range(s + 1, e):
        if _text(parts[j]).lstrip().startswith('|'):
            last = j
    if last is None:
        raise SystemExit('NO TABLE in ' + header + ' of ' + path)
    _splice(path, parts, last + 1, _mk(rows, eol))
    print('OK after_table', path, '@line', last + 2)


def first_table(path, header, rows):
    """Append rows to the FIRST markdown table in the section (e.g. the Sinal-vs-gestao table)."""
    parts, eol = _load(path)
    s, e = _section(parts, header)
    first = last = None
    for j in range(s + 1, e):
        t = _text(parts[j]).lstrip()
        if t.startswith('|'):
            if first is None:
                first = j
            last = j
        elif first is not None and t.strip() == '':
            break
    if first is None:
        raise SystemExit('NO TABLE in ' + header + ' of ' + path)
    _splice(path, parts, last + 1, _mk(rows, eol))
    print('OK first_table', path, '@line', last + 2)


def before_prefix(path, prefix, block):
    """Insert immediately BEFORE the first line starting with `prefix`."""
    parts, eol = _load(path)
    idx = None
    for i, ln in enumerate(parts):
        if _text(ln).startswith(prefix):
            idx = i
            break
    if idx is None:
        raise SystemExit('PREFIX NOT FOUND: ' + prefix)
    _splice(path, parts, idx, _mk(block + NL, eol))
    print('OK before_prefix', path, '@line', idx + 1)


if __name__ == '__main__':
    mode, path, header = sys.argv[1], sys.argv[2], sys.argv[3]
    block = io.open(sys.stdin.fileno(), encoding='utf-8', errors='strict').read()
    fn = {'append_end': append_end, 'insert_top': insert_top, 'after_table': after_table,
          'first_table': first_table, 'before_prefix': before_prefix}[mode]
    if mode == 'insert_top' and len(sys.argv) > 4:
        fn(path, header, block, int(sys.argv[4]))
    else:
        fn(path, header, block)
