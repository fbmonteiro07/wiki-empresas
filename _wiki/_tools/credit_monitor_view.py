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
SECTIONS = ('overview', 'alerts', 'market', 'yields', 'relative-spreads', 'counterparty',
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


def model(config, watch, today=None):
    today = today or dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).date()
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
        issuers.append({'id': company, 'name': issuer.get('name', company),
                        'focus': company in FOCUS, 'color': COLORS[index % len(COLORS)],
                        'cds': next((s for s in own if s['group'] == 'cds'), None),
                        'bonds': bonds, 'main': main['id'] if main else None})
    dates = [s['date'] for s in instruments if s['date']]
    return {'today': today.isoformat(), 'fetched': watch.get('fetched_at'),
            'feed': watch.get('bbg_status', {}), 'issuers': issuers,
            'latest': max(dates) if dates else None}


def json_script(data):
    return json.dumps(data, ensure_ascii=False, allow_nan=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


def enhance(page, deals, market):
    data = model(read_json(ROOT / '_wiki/_data/credit_watch_config.json'),
                 read_json(ROOT / '_wiki/_data/credit_watch.json'))
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
    for key, content in zip(SECTIONS, sections):
        if key == 'yields':
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
        'RESEARCH': ''.join(research), 'RESEARCH_DATE': E(deals['asof']),
        'DATA': json_script(data),
    }
    template = (ASSETS / 'monitor.html').read_text(encoding='utf-8')
    return re.sub(r'@@([A-Z_]+)@@', lambda m: parts[m[1]], template)
