"""Focused credit monitor. Reads retained data; never fetches or sends mail."""
import datetime as dt
import html
import json
import re
from pathlib import Path
from fetch_credit_watch import board_instruments
from funding_common import change, observations

ROOT = Path(__file__).resolve().parents[2]
ASSETS = Path(__file__).with_name('credit_monitor_ui')
FOCUS = ('CRWV', 'ORCL', 'NBIS', 'IREN', 'MSFT', 'AMZN', 'GOOGL', 'META')
SECTIONS = ('overview', 'alerts', 'workbook', 'market', 'yields', 'relative-spreads', 'counterparty',
            'repricing', 'issuance', 'ledger', 'scoreboard', 'watch')
COLORS = ('#3869d4', '#d27c39', '#8c5cbe', '#258f83', '#568aa0', '#bf5577', '#738446', '#646bc0')
E = html.escape


def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def instrument_view(config, stored, today):
    """Only observations establish levels. Coupons never fill missing yields."""
    points = observations(stored, today)
    last_date, last = points[-1] if points else (None, None)
    stale = bool(points and ((today - dt.date.fromisoformat(last_date)).days > 4
                            or stored.get('status') == 'stale' or stored.get('error')))
    unit, field = config['unit'], config['field']
    mismatch = stored.get('unit', unit) != unit or stored.get('field', field) != field
    warning = config.get('validation_warning', '')
    if mismatch or warning:
        points, last_date, last, stale = [], None, None, False
    clean = {'points': points, 'unit': unit}
    return {
        'id': config['id'], 'label': config['label'], 'group': config['group'],
        'unit': unit, 'field': field, 'board': config['board'],
        'ticker': stored.get('ticker'), 'candidate': (config.get('candidates') or [''])[0],
        'points': points, 'last': last, 'date': last_date,
        'status': 'unverified' if warning else 'missing' if not points else 'stale' if stale else 'available',
        'validationWarning': warning,
        'changes': {str(days): change(clean, days, today) for days in (1, 7, 30)},
        'error': 'Stored units or field do not match this instrument.' if mismatch else stored.get('error', ''),
    }


def flat_view(entry, history, today, refreshed):
    """Official workbook CDS (CDS_FLAT_SPREAD, bp). A different basis from the board's PX_LAST — never netted with it."""
    if not entry:
        return None
    rows = sorted((r for r in history if r.get('kind') == 'cds' and r.get('id') == entry['bbg']),
                  key=lambda r: (r.get('date', ''), r.get('time', '')))
    daily = {'unit': 'bp', 'points': [[r['date'], r.get('spread')] for r in rows]}  # last pull of each day wins
    points = []
    for date, value in observations(daily, today):
        if not points or value != points[-1][1]:  # a morning pull that repeats the prior close is a carried mark, not a print
            points.append((date, value))
    return {'bbg': entry['bbg'], 'field': 'CDS_FLAT_SPREAD', 'last': entry.get('spread_bp'),
            'quoted': refreshed, 'stale': bool(entry.get('stale')),
            'snapshot': entry.get('spread_snapshot_bp'), 'dSnapshot': entry.get('d_snapshot_bp'),
            'msDesk': entry.get('ms_desk_0824_bp'), 'dMsDesk': entry.get('d_vs_ms_bp'),
            'points': points, 'markDate': points[-1][0] if points else None,
            'change1': change({'unit': 'bp', 'points': points}, 1, today)}


def step_breaks(issuers, floor=50, ratio=0.5):
    """One-session CDS moves of at least `floor` bp and `ratio` of the prior level: check for a ticker or convention break."""
    notes = []
    for c in issuers:
        pts = (c['cds'] or {}).get('points', [])
        for (d0, v0), (d1, v1) in zip(pts, pts[1:]):
            if abs(v1 - v0) >= floor and v0 and abs(v1 - v0) / abs(v0) >= ratio:
                notes.append({'id': c['id'], 'from': [d0, v0], 'to': [d1, v1]})
    return notes


def twin_histories(issuers, minimum=10):
    """Flag issuer CDS series that print the same value on the same day — a proxy curve, not two markets."""
    notes = []
    for i, a in enumerate(issuers):
        for b in issuers[i + 1:]:
            if not (a['cds'] and b['cds']):
                continue
            other = dict(b['cds']['points'])
            same = sorted(d for d, v in a['cds']['points'] if other.get(d) == v)
            if len(same) >= minimum:
                notes.append({'pair': [a['id'], b['id']], 'days': len(same), 'first': same[0], 'last': same[-1]})
    return notes


def model(config, watch, today=None, workbook=None, history=()):
    today = today or dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).date()
    flat = {c['bbg']: c for c in (workbook or {}).get('cds', [])}
    stored = {s['id']: s for s in watch.get('series', [])}
    warnings = {i['company'] + '_CDS5Y': i.get('cds_validation_warning', '')
                for i in config.get('board', {}).get('issuers', [])}
    instruments = [instrument_view({**c, 'validation_warning': warnings.get(c['id'], '')},
                                   stored.get(c['id'], {}), today) for c in board_instruments(config)]
    issuers = []
    ordered = sorted(config.get('board', {}).get('issuers', []),
                     key=lambda c: FOCUS.index(c['company']) if c['company'] in FOCUS else len(FOCUS))
    for index, issuer in enumerate(ordered):
        company = issuer['company']
        own = [s for s in instruments if s['board']['issuer'] == company]
        bonds = sorted((s for s in own if s['group'] == 'bond'), key=lambda s: s['board']['mty'])
        # Stable benchmark, independent of which instrument happens to have a quote.
        main = min(bonds, key=lambda s: (s['board'].get('ccy', 'USD') != 'USD',
                                        s['board']['kind'] == 'convertible',
                                        not s['board'].get('headline'), s['board']['mty']), default=None)
        issuers.append({'id': company, 'name': issuer.get('name', company), 'tier': issuer.get('tier', ''),
                        'focus': company in FOCUS, 'color': COLORS[index % len(COLORS)],
                        'cds': next((s for s in own if s['group'] == 'cds'), None),
                        'flat': flat_view(flat.get(issuer.get('cds')), history, today, (workbook or {}).get('refreshed_at')),
                        'bonds': bonds, 'main': main['id'] if main else None})
    dates = [s['date'] for s in instruments if s['date']]
    hyperscalers = [c for c in issuers if c['tier'].startswith('hyperscaler')]
    return {'today': today.isoformat(), 'fetched': watch.get('fetched_at'),
            'feed': watch.get('bbg_status', {}), 'issuers': issuers,
            'twins': twin_histories(hyperscalers), 'steps': step_breaks(hyperscalers),
            'latest': max(dates) if dates else None}


def read_jsonl(path):
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except OSError:
        return []
    rows = []
    for line in lines:
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue
    return rows


def json_script(data):
    return json.dumps(data, ensure_ascii=False, allow_nan=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


def enhance(page, deals, market):
    data = model(read_json(ROOT / '_wiki/_data/credit_watch_config.json'),
                 read_json(ROOT / '_wiki/_data/credit_watch.json'),
                 workbook=read_json(ROOT / '_wiki/_data/credit_workbook.json'),
                 history=read_jsonl(ROOT / '_wiki/_data/credit-monitor/workbook/history.jsonl'))
    sections = re.findall(r'<section>(.*?)</section>', page, re.S)
    if len(sections) != len(SECTIONS):
        raise ValueError('Credit research section layout changed; refusing to mislabel source sections.')
    research = []
    review = deals.get('weekly_review', {})
    if review:
        paragraphs = ''.join('<p>' + E(p) + '</p>' for p in review.get('summary', '').splitlines() if p)
        sources = ''.join('<li>' + E(s) + '</li>' for s in review.get('sources', []))
        research.append('<details class="research-item" id="research-review"><summary>Latest research review'
                        '<span>' + E(deals['asof']) + '</span></summary><div class="research-body">' + paragraphs
                        + '<details><summary>Sources and dates</summary><ul>' + sources + '</ul></details></div></details>')
    workbook_html = ''
    for key, content in zip(SECTIONS, sections):
        if key == 'yields':
            continue
        if key == 'workbook':
            # the official workbook (AI_Credit_Live.xlsx) renders in the market-monitor view, above the issuer board
            workbook_html = '<section id="workbook" class="surface workbook-section" aria-labelledby="workbook-title">' + content + '</section>'
            continue
        title = re.search(r'<h2>(.*?)</h2>', content, re.S)
        label = re.sub('<[^>]+>', '', title[1]) if title else 'Market overview &amp; issuance'
        if title:
            content = content.replace(title[0], '', 1)
        if key == 'ledger':
            content = content.replace('<table>', '<table id="deal-table">', 1)
            content = '<label class="research-search">Find a deal<input id="deal-search" type="search" placeholder="Company, instrument, source"></label>' + content
        research.append(f'<details class="research-item" id="{key}"><summary>{label}<span>Open ↗</span></summary>'
                        f'<div class="research-body">{content}</div></details>')
    parts = {
        'LEGACY_CSS': re.search(r'<style>(.*?)</style>', page, re.S)[1],
        'LEGACY_JS': re.search(r'<script>(.*?)</script>', page, re.S)[1],
        'CSS': (ASSETS / 'monitor.css').read_text(encoding='utf-8'),
        'JS': (ASSETS / 'monitor.js').read_text(encoding='utf-8'),
        'RESEARCH': ''.join(research), 'RESEARCH_DATE': E(deals['asof']), 'WORKBOOK': workbook_html,
        'DATA': json_script(data),
    }
    template = (ASSETS / 'monitor.html').read_text(encoding='utf-8')
    return re.sub(r'@@([A-Z_]+)@@', lambda m: parts[m[1]], template)
