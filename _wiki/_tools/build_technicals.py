"""Technical-indicator dashboard over every listed wiki name.

Reads  _data/technicals/prices.json (fetch_technicals_bbg.py, local BBG)
Writes _data/technicals/signals.json  (screener rows, levels, flags)
       _dashboards/technicals.html    (screener + RSI/200D map + per-name charts)

Indicators (all on daily closes, BBG split-adjusted):
  RSI(14)      Wilder smoothing; signal = SMA(9) of RSI
  SMA 20/50/200 and % distance of price from each
  Support / resistance = clusters of swing lows / highs (pivot = extreme of a
    +/-5-bar window) over the last 2 years. Two pivots join a level when they sit
    within a tolerance of 0.75 x ATR(14)% (floored 1.5%, capped 4%) and at least
    10 bars apart. A level touched 2x = double bottom, 3x+ = triple bottom.
  Bull divergence  = latest touch of the nearest multi-touch support printed a
    lower-or-equal low than the prior touch with a HIGHER RSI.
Technical read only - no Capstone view, no broker attribution needed (price data: BBG).
"""
import datetime as dt
import json
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
WIKI = Path(__file__).resolve().parents[1]
DATA = WIKI / '_data' / 'technicals'
OUT_HTML = WIKI / '_dashboards' / 'technicals.html'

PIVOT_K = 5
LOOKBACK = 504          # ~2 trading years for level detection and charts
MIN_GAP = 10
NEAR_PCT = 2.5          # "at support" when within this % (or 0.6 ATR) of the level


def sma(x, n):
    out, s = [None] * len(x), 0.0
    for i, v in enumerate(x):
        s += v
        if i >= n: s -= x[i - n]
        if i >= n - 1: out[i] = s / n
    return out


def sma_opt(x, n):
    out = [None] * len(x)
    for i in range(len(x)):
        w = x[i - n + 1:i + 1] if i >= n - 1 else []
        if len(w) == n and all(v is not None for v in w): out[i] = sum(w) / n
    return out


def rsi(c, n=14):
    out = [None] * len(c)
    if len(c) <= n: return out
    g = [max(c[i] - c[i - 1], 0) for i in range(1, len(c))]
    l = [max(c[i - 1] - c[i], 0) for i in range(1, len(c))]
    ag, al = sum(g[:n]) / n, sum(l[:n]) / n
    for i in range(n, len(c)):
        if i > n:
            ag = (ag * (n - 1) + g[i - 1]) / n
            al = (al * (n - 1) + l[i - 1]) / n
        out[i] = 100.0 if al == 0 else 100 - 100 / (1 + ag / al)
    return out


def atr(h, l, c, n=14):
    tr = [h[0] - l[0]] + [max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])) for i in range(1, len(c))]
    out, a = [None] * len(c), None
    for i, v in enumerate(tr):
        if i == n - 1: a = sum(tr[:n]) / n
        elif i >= n: a = (a * (n - 1) + v) / n
        out[i] = a
    return out


def pivots(x, k, low=True):
    idx = []
    for i in range(k, len(x) - k):
        w = x[i - k:i + k + 1]
        if (x[i] == min(w)) if low else (x[i] == max(w)):
            if not idx or i - idx[-1] > k: idx.append(i)
    return idx


def cluster(points, tol):
    """points: [(price, i)] -> levels [{px, touches:[i...]}] greedy by price."""
    levels = []
    for px, i in sorted(points):
        if levels and abs(px / levels[-1]['px'] - 1) <= tol:
            lv = levels[-1]
            lv['pts'].append((px, i))
            lv['px'] = sum(p for p, _ in lv['pts']) / len(lv['pts'])
        else:
            levels.append({'px': px, 'pts': [(px, i)]})
    out = []
    for lv in levels:
        pts = sorted(lv['pts'], key=lambda t: t[1])
        kept = []
        for p in pts:                      # touches must be separate swings
            if kept and p[1] - kept[-1][1] < MIN_GAP:
                if (p[0] < kept[-1][0]): kept[-1] = p
                continue
            kept.append(p)
        out.append({'px': sum(p for p, _ in kept) / len(kept), 'pts': kept})
    return out


def pct(a, b):
    return None if a is None or b in (None, 0) else (a / b - 1) * 100


def r(x, nd=2):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(x, nd)


def sector_map():
    m = json.loads((WIKI / '_data' / 'index_meta.json').read_text(encoding='utf-8'))
    out = {}
    for s in m['sections']:
        title = s['title'].replace('—', '-').replace('�', '-')
        for e in s.get('entries', []):
            out.setdefault(e['ticker'], (title, e.get('thesis', '')))
    return out


def analyse(t, s):
    d, o, h, l, c = s['d'], s['o'], s['h'], s['l'], s['c']
    n = len(c)
    s20, s50, s200 = sma(c, 20), sma(c, 50), sma(c, 200)
    rs = rsi(c); rsig = sma_opt(rs, 9); at = atr(h, l, c)
    last = c[-1]
    atr_pct = at[-1] / last * 100 if at[-1] else 2.0
    tol = min(max(0.75 * atr_pct, 1.5), 4.0) / 100
    lo0 = max(0, n - LOOKBACK)
    lows = [i for i in pivots(l, PIVOT_K, True) if i >= lo0]
    highs = [i for i in pivots(h, PIVOT_K, False) if i >= lo0]
    # the most recent bars cannot be confirmed pivots; add today's window low if it is the 2y-window floor area
    sup = [lv for lv in cluster([(l[i], i) for i in lows], tol)]
    res = [lv for lv in cluster([(h[i], i) for i in highs], tol)]

    def fmt(lv, kind):
        return {'px': r(lv['px'], 4), 'n': len(lv['pts']), 'kind': kind,
                'touch': [[d[i], r(p, 4), r(rs[i], 1)] for p, i in lv['pts']],
                'dist': r(pct(last, lv['px']), 2)}

    near = max(NEAR_PCT, 0.6 * atr_pct)
    supports = sorted([fmt(lv, 'S') for lv in sup if lv['px'] <= last * (1 + tol)], key=lambda z: -z['px'])
    resist = sorted([fmt(lv, 'R') for lv in res if lv['px'] > last * (1 + tol)], key=lambda z: z['px'])
    multi = [z for z in supports if z['n'] >= 2]
    ns = multi[0] if multi else None
    # broken multi-touch support: a 2x+ swing-low level sitting ABOVE price, lost within the last 15 bars
    broken = None
    for lv in sup:
        if len(lv['pts']) >= 2 and lv['px'] > last * (1 + tol) and lv['px'] < last * 1.15:
            lost = [i for i in range(max(1, n - 10), n) if c[i] < lv['px'] <= c[i - 1]]
            if lost:
                cand = fmt(lv, 'B'); cand['lost'] = d[lost[-1]]
                if not broken or cand['n'] > broken['n']: broken = cand
    div = False
    if ns and ns['n'] >= 2:
        (d1, p1, r1), (d2, p2, r2) = ns['touch'][-2], ns['touch'][-1]
        div = p2 <= p1 * 1.005 and r1 is not None and r2 is not None and r2 > r1 + 2

    def ret(k):
        return r(pct(last, c[-1 - k]), 2) if n > k else None
    ytd_i = next((i for i in range(n - 1, -1, -1) if d[i] < f'{d[-1][:4]}-01-01'), None)
    w52 = c[-252:]
    cross = None
    for i in range(n - 1, max(200, n - 252), -1):
        if s50[i] and s200[i] and s50[i - 1] and s200[i - 1]:
            if (s50[i] > s200[i]) != (s50[i - 1] > s200[i - 1]):
                cross = {'d': d[i], 'type': 'golden' if s50[i] > s200[i] else 'death', 'ago': n - 1 - i}
                break
    flags = []
    rv = rs[-1]
    if rv is not None and rv < 30: flags.append('oversold')
    if rv is not None and rv > 70: flags.append('overbought')
    if ns and abs(ns['dist']) <= near: flags.append('at_support')
    if ns and ns['n'] >= 3 and abs(ns['dist']) <= near: flags.append('triple')
    if broken: flags.append('broken')
    if div and ns and abs(ns['dist']) <= near: flags.append('bull_div')
    if cross and cross['ago'] <= 20: flags.append(cross['type'])
    if s200[-1] and s200[-2] and (c[-1] > s200[-1]) != (c[-2] > s200[-2]):
        flags.append('x200_up' if c[-1] > s200[-1] else 'x200_dn')
    if rv is not None and rsig[-1] is not None and rs[-2] is not None and rsig[-2] is not None:
        if rs[-2] <= rsig[-2] and rv > rsig[-1]: flags.append('rsi_up')
        if rs[-2] >= rsig[-2] and rv < rsig[-1]: flags.append('rsi_dn')
    # percentile of today's % vs 200D in its own 3y history
    dev = [pct(c[i], s200[i]) for i in range(n) if s200[i]]
    devp = r(sum(1 for v in dev if v <= dev[-1]) / len(dev) * 100, 0) if dev else None
    row = {'t': t, 'last': r(last, 4), 'date': d[-1],
           'r1d': ret(1), 'r1w': ret(5), 'r1m': ret(21), 'r3m': ret(63),
           'ytd': r(pct(last, c[ytd_i]), 2) if ytd_i is not None else None,
           'rsi': r(rv, 1), 'rsig': r(rsig[-1], 1),
           'v20': r(pct(last, s20[-1]), 2), 'v50': r(pct(last, s50[-1]), 2), 'v200': r(pct(last, s200[-1]), 2),
           'v200p': devp, 'trend': None if not (s50[-1] and s200[-1]) else ('up' if s50[-1] > s200[-1] else 'down'),
           'cross': cross, 'hi52': r(pct(last, max(w52)), 2), 'lo52': r(pct(last, min(w52)), 2),
           'atr': r(atr_pct, 2), 'tol': r(tol * 100, 2),
           'sup': ns, 'sup1': supports[0] if supports else None, 'res': resist[0] if resist else None,
           'broken': broken, 'div': div, 'flags': flags}
    w = slice(lo0, n)
    series = {'d': d[w], 'o': o[w], 'h': h[w], 'l': l[w], 'c': c[w],
              's20': [r(x, 3) for x in s20[w]], 's50': [r(x, 3) for x in s50[w]], 's200': [r(x, 3) for x in s200[w]],
              'rsi': [r(x, 1) for x in rs[w]], 'rsig': [r(x, 1) for x in rsig[w]],
              'levels': ([z for z in supports if z['n'] >= 2][:4] + [z for z in resist if z['n'] >= 2][:3]
                         + ([broken] if broken else []))}
    return row, series


def main():
    src = json.loads((DATA / 'prices.json').read_text(encoding='utf-8'))
    secs = sector_map()
    rows, series, bench = [], {}, {}
    for t, s in src['names'].items():
        if len(s['c']) < 220: print(f'[technicals] {t}: short history ({len(s["c"])})')
        try:
            row, ser = analyse(t, s)
        except Exception as exc:
            print(f'[technicals] {t}: {exc}'); continue
        row['bbg'] = s['bbg']
        if s['bbg'].endswith('Index'):
            row['sector'] = 'Benchmarks'; bench[t] = row
        else:
            row['sector'], row['thesis'] = secs.get(t, ('Other', ''))
        rows.append(row); series[t] = ser
    eq = [x for x in rows if x['sector'] != 'Benchmarks']
    def share(f): return r(sum(1 for x in eq if f(x)) / len(eq) * 100, 0)
    breadth = {'n': len(eq), 'a50': share(lambda x: (x['v50'] or -1) > 0), 'a200': share(lambda x: (x['v200'] or -1) > 0),
               'up': share(lambda x: x['trend'] == 'up'), 'os': sum(1 for x in eq if 'oversold' in x['flags']),
               'ob': sum(1 for x in eq if 'overbought' in x['flags']), 'sup': sum(1 for x in eq if 'at_support' in x['flags']),
               'brk': sum(1 for x in eq if 'broken' in x['flags']), 'div': sum(1 for x in eq if 'bull_div' in x['flags'])}
    asof = max(x['date'] for x in rows)
    (DATA / 'signals.json').write_text(json.dumps({'asof': asof, 'breadth': breadth, 'rows': rows}, ensure_ascii=False, indent=1), encoding='utf-8')
    payload = json.dumps({'asof': asof, 'built': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'breadth': breadth,
                          'rows': rows, 'series': series}, ensure_ascii=False, separators=(',', ':'))
    tpl = (Path(__file__).resolve().parent / 'technicals.template.html').read_text(encoding='utf-8')
    OUT_HTML.write_text(tpl.replace('/*__DATA__*/null', payload), encoding='utf-8', newline='\n')
    print(f'[technicals] {len(eq)} names + {len(bench)} benchmarks, asof {asof} -> {OUT_HTML} '
          f'({OUT_HTML.stat().st_size/1e6:.1f} MB) | breadth {breadth}')


if __name__ == '__main__':
    main()
