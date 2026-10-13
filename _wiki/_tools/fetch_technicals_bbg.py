"""Daily OHLCV history for every listed wiki name, from the local Bloomberg Desktop API.

Writes _data/technicals/prices.json  {asof, start, names: {TICKER: {bbg, d:[...], o,h,l,c,v}}}
Feeds build_technicals.py (RSI / moving averages / multi-touch support levels).

Terminal logged out -> prices.json is left untouched (same guard as fetch_estimates).
Usage:  py fetch_technicals_bbg.py [--years 3] [TICKER ...]
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WIKI = Path(__file__).resolve().parents[1]
OUT = WIKI / '_data' / 'technicals'
OUT.mkdir(parents=True, exist_ok=True)

# mirrors E:/.claude/scripts/fetch_estimates.py BBG_TKR (non-US primary listings)
BBG_TKR = {"IFX": "IFX GR Equity", "AIXA": "AIXA GR Equity",
           "SAMSUNG": "005930 KS Equity", "SKHYNIX": "000660 KS Equity", "KIOXIA": "285A JP Equity",
           "TOKYOELEC": "8035 JP Equity", "ADVANTEST": "6857 JP Equity", "BESI": "BESI NA Equity",
           "DISCO": "6146 JP Equity", "SMIC": "981 HK Equity", "MEDIATEK": "2454 TT Equity",
           "CEREBRAS": "CBRS US Equity"}
PRIVATE = {"ANTHROPIC", "OPENAI", "NSCALE"}          # wiki pages with no listed equity
BENCH = {"SPX": "SPX Index", "NDX": "NDX Index", "SOX": "SOX Index"}


def wiki_tickers():
    skip = {"00_INDEX", "_TEMPLATE"}
    return sorted(p.stem for p in WIKI.glob('*.md') if p.stem not in skip and p.stem not in PRIVATE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--years', type=float, default=3)
    ap.add_argument('tickers', nargs='*')
    a = ap.parse_args()
    from market_breadth_bbg import Client
    try:
        client = Client()
    except Exception as exc:
        print(f'[technicals] Bloomberg unavailable ({exc}) - prices.json untouched')
        return 0
    names = a.tickers or wiki_tickers()
    sec = {t: BBG_TKR.get(t, f'{t} US Equity') for t in names}
    sec.update({k: v for k, v in BENCH.items() if not a.tickers})
    end = dt.date.today()
    start = end - dt.timedelta(days=int(365.25 * a.years) + 10)
    out_path = OUT / 'prices.json'
    old = json.loads(out_path.read_text(encoding='utf-8')) if out_path.exists() else {}
    res = dict(old.get('names', {})) if a.tickers else {}
    inv = {v: k for k, v in sec.items()}
    bbg = list(sec.values())
    fields = ['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST', 'PX_VOLUME']
    for i in range(0, len(bbg), 20):
        chunk = bbg[i:i + 20]
        for msg in client.hist(chunk, fields, start.strftime('%Y%m%d'), end.strftime('%Y%m%d')):
            sd = msg.get('securityData') or {}
            t = inv.get(sd.get('security'))
            rows = [r for r in sd.get('fieldData') or [] if r.get('PX_LAST') is not None]
            if not t or not rows:
                if t: print(f'[technicals] {t}: no data ({sd.get("securityError")})')
                continue
            def col(f, nd=4):
                return [None if r.get(f) is None else round(float(r[f]), nd) for r in rows]
            c = col('PX_LAST')
            res[t] = {'bbg': sec[t], 'd': [r['date'] for r in rows],
                      'o': [x if x is not None else c[k] for k, x in enumerate(col('PX_OPEN'))],
                      'h': [x if x is not None else c[k] for k, x in enumerate(col('PX_HIGH'))],
                      'l': [x if x is not None else c[k] for k, x in enumerate(col('PX_LOW'))],
                      'c': c, 'v': [None if x is None else int(x) for x in col('PX_VOLUME', 0)]}
        print(f'[technicals] {min(i + 20, len(bbg))}/{len(bbg)}', flush=True)
    client.close()
    if not res:
        print('[technicals] empty pull - prices.json untouched')
        return 0
    out_path.write_text(json.dumps({'asof': end.isoformat(), 'start': start.isoformat(), 'names': res},
                                   separators=(',', ':')), encoding='utf-8')
    missing = sorted(set(sec) - set(res))
    print(f'[technicals] wrote {len(res)} series -> {out_path} ; missing: {missing}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
