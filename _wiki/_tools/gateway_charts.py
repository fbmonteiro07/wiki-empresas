"""Auditable gateway charts and an offline HTML email attachment; stdlib only."""
import datetime as dt
import hashlib
import html
import json
import math
from collections import defaultdict
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
OR_SOURCE = 'https://openrouter.ai/rankings'
VC_SOURCE = 'https://vercel.com/ai-gateway/leaderboards/models'
LIVE = 'http://DS-CAP-33:8080/wiki/_dashboards/'
ALIASES = {'z-ai': 'zai', 'x-ai': 'xai', 'meta-llama': 'meta', 'nousresearch': 'nous'}
NAMES = {'openai': 'OpenAI', 'anthropic': 'Anthropic', 'google': 'Google', 'deepseek': 'DeepSeek',
         'zai': 'Z.ai', 'xai': 'xAI', 'moonshotai': 'Moonshot', 'qwen': 'Qwen', 'meta': 'Meta',
         'tencent': 'Tencent', 'xiaomi': 'Xiaomi', 'minimax': 'MiniMax', 'mistralai': 'Mistral',
         'nvidia': 'NVIDIA', 'inclusionai': 'InclusionAI', 'alibaba': 'Alibaba', 'spacexai': 'SpaceX AI'}
COLORS = {'total': '#2563eb', 'standard': '#0f766e', 'free': '#d97706', 'deepseek': '#2563eb',
          'zai': '#d97706', 'openai': '#059669', 'anthropic': '#dc6841', 'google': '#7c3aed',
          'tencent': '#0891b2', 'xiaomi': '#be185d', 'qwen': '#6554c0', 'moonshotai': '#64748b',
          'tokens': '#2563eb', 'spend': '#d97706'}
PALETTE = ['#0891b2', '#7c3aed', '#be185d', '#0f766e', '#475569']


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(value, encoding='utf-8')
    tmp.replace(path)


def lab_key(value):
    value = (value or 'unknown').lower()
    return ALIASES.get(value, value)


def name(value):
    return NAMES.get(value, value)


def color(key):
    return COLORS.get(key, PALETTE[int(hashlib.sha256(key.encode()).hexdigest()[:8], 16) % len(PALETTE)])


def pct(now, before):
    return (now / before - 1) * 100 if before else None


def baseline(snapshots, current):
    # A seven-day pair takes priority over an intervening adhoc snapshot.
    day = dt.date.fromisoformat(current['date'])
    options = [s for s in snapshots if 4 <= (day - dt.date.fromisoformat(s['date'])).days <= 10]
    return min(options, key=lambda s: (abs((day - dt.date.fromisoformat(s['date'])).days - 7), s['date'])) if options else None


def parse_snapshot(folder):
    rows = read(folder / 'rank_week.json')['data']
    if not rows:
        raise ValueError('Empty token ranking')
    catalog = {}
    for c in read(folder / 'catalog.json')['data']:
        for key in (c.get('permaslug'), c.get('slug')):
            if key:
                catalog[key] = c
    labs, models, totals = defaultdict(float), {}, defaultdict(float)
    for row in rows:
        slug, variant = row['model_permaslug'], row.get('variant', 'standard')
        key = slug + ':' + variant
        if key in models:
            raise ValueError('Duplicate model/variant across time buckets: ' + key)
        values = [float(row[field]) for field in ('total_prompt_tokens', 'total_completion_tokens')]
        if any(not math.isfinite(v) or v < 0 for v in values):
            raise ValueError('Invalid token count')
        tokens = sum(values)
        c = catalog.get(slug, {})
        author = lab_key(c.get('author') or slug.split('/')[0])
        model_name = c.get('short_name') or c.get('name') or slug.split('/')[-1]
        models[key] = {'name': model_name + (' · free' if variant == 'free' else ' · ' + variant), 'tokens': tokens, 'lab': author}
        labs[author] += tokens
        totals['total'] += tokens
        totals['free' if variant == 'free' else 'standard'] += tokens
    if totals['total'] <= 0:
        raise ValueError('Zero total tokens')
    # Rows in earlier date buckets carry dormant models' real window usage.
    # Sum every row, and use the last bucket ONLY to label the window end.
    end = max(r['date'][:10] for r in rows)
    month = None
    if (folder / 'rank_month.json').exists():
        month = sum(float(r['total_prompt_tokens']) + float(r['total_completion_tokens'])
                    for r in read(folder / 'rank_month.json')['data'])
    return {'date': end, 'snapshot': folder.name, **totals, 'labs': dict(labs), 'models': models, 'month': month}


def extremes(rows, limit=8):
    gains = sorted((r for r in rows if r['value'] > 0), key=lambda r: -r['value'])[:limit // 2]
    losses = sorted((r for r in rows if r['value'] < 0), key=lambda r: r['value'])[:limit // 2]
    return gains + sorted(losses, key=lambda r: -r['value'])


def point_series(key, label, dates, values):
    return {'key': key, 'name': label, 'color': color(key), 'points': list(zip(dates, values))}


def collect(wiki=WIKI):
    data = wiki / '_data'
    warnings, snapshots = [], {}
    pointer = (data / 'openrouter' / 'latest.txt').read_text(encoding='utf-8').strip()
    # Do not advance beyond the upstream's last successful snapshot.
    for folder in sorted((data / 'openrouter' / 'raw').glob('20*')):
        if folder.name > pointer:
            continue
        try:
            manifest = folder / '_manifest.json'
            if manifest.exists():
                endpoints = read(manifest).get('endpoints', {})
                if any(endpoints.get(k, {}).get('ok') is False for k in ('rank_week', 'catalog')):
                    raise ValueError('Upstream collection marked incomplete')
            snap = parse_snapshot(folder)
            snapshots[snap['date']] = snap
        except (ValueError, KeyError, OSError, TypeError) as exc:
            warnings.append('Skipped OpenRouter ' + folder.name + ': ' + str(exc))
    snaps = sorted(snapshots.values(), key=lambda s: s['date'])
    if not snaps:
        raise ValueError('No valid OpenRouter token snapshots')
    cur = snaps[-1]
    prev = baseline(snaps, cur)
    if cur['snapshot'] != pointer:
        warnings.append('Latest OpenRouter raw snapshot could not be charted; older values retained.')
    dates = [s['date'] for s in snaps]
    gap = (dt.date.fromisoformat(cur['date']) - dt.date.fromisoformat(prev['date'])).days if prev else None
    period = (f"{prev['date']} → {cur['date']} · {gap} days" + (' · not strict WoW' if gap != 7 else '')) if prev else 'No comparable 4–10 day baseline'
    osource = f"OpenRouter · windows ending {dates[0]} to {dates[-1]} · all prompt + completion tokens in the public feed."
    charts = []

    def add(cid, title, subtitle, kind, source, **extra):
        charts.append(dict(id=cid, title=title, subtitle=subtitle, kind=kind, source=source, **extra))

    add('or-volume', '01 · Is token demand growing?', 'OpenRouter · trailing 7-day volume · trillion tokens', 'line', osource,
        unit='T', series=[point_series(k, label, dates, [s.get(k, 0) / 1e12 for s in snaps])
                          for k, label in [('total', 'Total'), ('standard', 'Other variants'), ('free', 'Free-tagged')]])
    growth = []
    for s in snaps:
        p = baseline(snaps, s)
        if p:
            days = (dt.date.fromisoformat(s['date']) - dt.date.fromisoformat(p['date'])).days
            growth.append({'name': f"{p['date'][5:]} → {s['date'][5:]} ({days}d)", 'value': pct(s['total'], p['total'])})
    add('or-growth', '02 · Is growth accelerating?', 'OpenRouter · change in trailing 7-day volume · actual comparison intervals shown', 'bars', osource,
        unit='%', rows=growth, signed=True)
    leaders = sorted(cur['labs'], key=cur['labs'].get, reverse=True)[:6]
    add('or-lab-history', '03 · Who is taking token share?', 'OpenRouter · six largest labs today, held fixed across history · %', 'line', osource,
        unit='%', series=[point_series(k, name(k), dates, [s['labs'][k] / s['total'] * 100 if k in s['labs'] else None for s in snaps]) for k in leaders])
    lab_moves, model_moves = [], []
    if prev:
        lab_moves = [{'name': name(k), 'value': cur['labs'][k] / cur['total'] * 100 - prev['labs'][k] / prev['total'] * 100}
                     for k in cur['labs'].keys() & prev['labs'].keys()]
        model_moves = [{'name': cur['models'][k]['name'], 'value': (cur['models'][k]['tokens'] - prev['models'][k]['tokens']) / 1e12}
                       for k in cur['models'].keys() & prev['models'].keys()]
    add('or-lab-movers', '04 · Labs gaining / losing share', 'OpenRouter · '+period+' · percentage points', 'bars', osource,
        unit='pp', rows=extremes(lab_moves), signed=True)
    add('or-model-movers', '05 · Models adding / losing tokens', 'OpenRouter · '+period+' · change in trillion tokens', 'bars', osource,
        unit='T', rows=extremes(model_moves), signed=True,
        note='Only model variants present in both snapshots. Free and standard variants stay separate. An absent row is not assumed to be zero.')
    add('or-free-mix', '06 · How much is free-tagged usage?', 'OpenRouter · free-tagged tokens as a share of total · %', 'line', osource,
        unit='%', series=[point_series('free', 'Free-tagged share', dates, [s.get('free', 0) / s['total'] * 100 for s in snaps])],
        note='The free variant is a feed tag. Other variants can also have zero prices or promotions; this is not a precise paid/free revenue split.')

    vc = None
    if (data / 'vercel' / 'dashboard.json').exists():
        vd = read(data / 'vercel' / 'dashboard.json')
        folder = data / 'vercel' / 'raw' / vd['raw_snapshot']
        raw = read(folder / 'labs.json')['rows']
        bylab = defaultdict(dict)
        for r in raw:
            if r['metric'] == 'tokens' and r['date'] <= vd['asof']:
                bylab[r['name']][r['date']] = r['share_percent']
        start = min(d for values in bylab.values() for d in values)
        first, end = dt.date.fromisoformat(start), dt.date.fromisoformat(vd['asof'])
        days = [(first + dt.timedelta(days=i)).isoformat() for i in range((end - first).days + 1)]
        labs = vd['datasets']['labs']['tokens']
        top = [r['name'] for r in labs if r['name'].lower() != 'other'][:6]
        vsource = f"Vercel AI Gateway · daily shares through {vd['asof']} · all modalities · CC BY 4.0."
        vp = ' to '.join(vd['current_period']) + ' vs ' + ' to '.join(vd['previous_period'])
        add('vc-lab-history', '07 · Where is Vercel usage shifting?', 'Vercel · daily token shares · six largest labs on latest day · %', 'line', vsource,
            unit='%', series=[point_series(lab_key(k), name(lab_key(k)), days, [bylab[k].get(d) for d in days]) for k in top],
            note='Gaps remain gaps. The share export does not disclose absolute token volumes or their growth.')
        for dataset, cid, title in [('labs', 'vc-lab-movers', '08 · Vercel labs gaining / losing share'), ('models', 'vc-model-movers', '09 · Vercel models gaining / losing share')]:
            available = [r for r in vd['datasets'][dataset]['tokens'] if r['name'].lower() != 'other']
            moves = [{'name': name(lab_key(r['name'])) if dataset == 'labs' else r['name'], 'value': r['change_pp']} for r in available if r['change_pp'] is not None]
            excluded = sum(r['change_pp'] is None for r in available)
            add(cid, title, 'Vercel · change in mean daily token share · pp', 'bars', vsource,
                unit='pp', rows=extremes(moves), signed=True,
                note=vp+f'. Requires all 14 days. {excluded} current entries excluded for incomplete coverage. Means are unweighted.')
        token_means = {r['name']: r['mean_7d'] for r in labs}
        spend_means = {r['name']: r['mean_7d'] for r in vd['datasets']['labs']['spend']}
        paired = [k for k in token_means if k.lower() != 'other' and token_means[k] is not None and spend_means.get(k) is not None]
        paired = sorted(paired, key=lambda k: token_means[k], reverse=True)[:6]
        add('vc-token-spend', '10 · Do tokens translate into spend?', 'Vercel · mean daily shares over '+ ' to '.join(vd['current_period'])+' · %', 'grouped', vsource,
            unit='%', rows=[{'name': name(lab_key(k)), 'values': [token_means[k], spend_means[k]]} for k in paired],
            labels=['Token share', 'Estimated spend share'], colors=[color('tokens'), color('spend')],
            note='Spend is estimated at labs’ list prices. The gap reflects pricing and workload mix, not realized lab revenue.')
        vc = {'asof': vd['asof'], 'current_period': vd['current_period'], 'previous_period': vd['previous_period'], 'history_start': start}
    else:
        warnings.append('Vercel data is unavailable.')
    for source, date in [('OpenRouter', cur['date']), ('Vercel', vc['asof'] if vc else None)]:
        if date and (dt.date.today() - dt.date.fromisoformat(date)).days > 2:
            warnings.append(source+' data is stale: '+date)
    return {'generated_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'schema_version': 1,
            'openrouter': {'asof': cur['date'], 'snapshot': cur['snapshot'], 'history_start': dates[0], 'baseline': prev['date'] if prev else None,
                          'interval_days': gap, 'tokens_7d': cur['total'], 'tokens_30d': cur['month'], 'growth_pct': pct(cur['total'], prev['total']) if prev else None,
                          'free_share_pct': cur.get('free', 0) / cur['total'] * 100, 'observations': len(snaps)},
            'vercel': vc, 'charts': charts, 'warnings': warnings}


def fmt(value, unit='', signed=False):
    if value is None:
        return 'n/a'
    return (f'{value:+.2f}' if signed else f'{value:.2f}') + (' '+unit if unit else '')


def nice_max(value):
    if value <= 0:
        return 1
    magnitude = 10 ** math.floor(math.log10(value))
    return math.ceil(value / magnitude / .5) * magnitude * .5


def svg_start(title, height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 {height}" role="img" aria-label="{html.escape(title, quote=True)}"><title>{html.escape(title)}</title>']


def text(x, y, value, anchor='start', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {extra}>{html.escape(str(value))}</text>'


def line_svg(c):
    left, right, top, bottom = 53, 598, 20, 235
    points = [p for s in c['series'] for p in s['points']]
    if not points:
        return '<p>No comparable history yet.</p>'
    dates = sorted(set(p[0] for p in points))
    ordinals = {d: dt.date.fromisoformat(d).toordinal() for d in dates}
    first, last = ordinals[dates[0]], ordinals[dates[-1]]
    scale = nice_max(max((p[1] for p in points if p[1] is not None), default=0) * 1.08)
    x = lambda d: left + (ordinals[d] - first) / max(1, last - first) * (right - left)
    y = lambda v: bottom - v / scale * (bottom - top)
    out = svg_start(c['title'], 270)
    for i in range(5):
        v = scale * i / 4
        out.append(f'<line class="gc-gridline" x1="{left}" x2="{right}" y1="{y(v)}" y2="{y(v)}"/>')
        out.append(text(left-9, y(v)+4, f'{v:g}', 'end'))
    indices = sorted({round(i * (len(dates)-1) / min(4, max(1, len(dates)-1))) for i in range(min(4, len(dates)-1)+1)})
    for i in indices:
        out.append(text(x(dates[i]), 259, dates[i][5:], 'middle'))
    for s in c['series']:
        segment = []
        for d, value in s['points'] + [(None, None)]:
            if value is None:
                if segment:
                    out.append(f'<polyline fill="none" stroke="{s["color"]}" stroke-width="2.8" points="'+ ' '.join(segment)+'"/>')
                segment = []
                continue
            segment.append(f'{x(d):.2f},{y(value):.2f}')
        for d, value in s['points']:
            if value is not None:
                radius = 3.5 if len(dates) < 20 else 1.7
                out.append(f'<circle cx="{x(d):.2f}" cy="{y(value):.2f}" r="{radius}" fill="{s["color"]}"><title>{html.escape(s["name"]+" · "+d+": "+fmt(value,c["unit"]))}</title></circle>')
    return ''.join(out) + '</svg>'


def bars_svg(c):
    rows = c['rows']
    if not rows:
        return '<p>No comparable observations yet.</p>'
    grouped = c['kind'] == 'grouped'
    signed = c.get('signed', False)
    step = 58 if grouped else 48
    left, right, top = 218, 594, 32
    bound = nice_max(max((max(r['values']) if grouped else abs(r['value'])) for r in rows) * 1.25)
    zero = (left + right) / 2 if signed else left
    scale = ((right - left) / 2 if signed else right - left) / bound
    height = top + len(rows) * step + 10
    out = svg_start(c['title'], height)
    for value in ([-bound, 0, bound] if signed else [0, bound / 2, bound]):
        xx = zero + value * scale
        out.append(f'<line class="gc-gridline" x1="{xx}" x2="{xx}" y1="24" y2="{height-10}"/>')
        out.append(text(xx, 15, f'{value:g}', 'middle'))
    for i, row in enumerate(rows):
        yy = top + i * step
        label = row['name']
        # The complete name remains in the hover title and the data table.
        words, lines = label.split(), ['']
        for word in words:
            if len(lines[-1] + ' ' + word) > 27 and lines[-1]:
                lines.append(word)
            else:
                lines[-1] = (lines[-1] + ' ' + word).strip()
        if len(lines) > 2:
            lines = [lines[0], lines[1][:24] + '…']
        lines = [line if len(line) <= 29 else line[:26]+'…' for line in lines]
        out.append('<g><title>'+html.escape(label)+'</title>')
        for j, line in enumerate(lines):
            out.append(text(2, yy+14+j*16, line))
        out.append('</g>')
        values = row['values'] if grouped else [row['value']]
        for j, value in enumerate(values):
            end = zero + value * scale
            bar_y = yy + j * 22
            fill = c['colors'][j] if grouped else ('#0d9488' if value >= 0 else '#e06652')
            out.append(f'<rect x="{min(zero,end):.2f}" y="{bar_y}" width="{abs(end-zero):.2f}" height="16" rx="3" fill="{fill}"><title>{html.escape(label+": "+fmt(value,c["unit"],signed))}</title></rect>')
            anchor = 'end' if value < 0 else 'start'
            out.append(text(end + (-5 if value < 0 else 5), bar_y+13, f'{value:+.2f}' if signed else f'{value:.2f}', anchor, 'class="gc-value"'))
    return ''.join(out) + '</svg>'


def table(c):
    if c['kind'] == 'line':
        headers = ['Window end / day'] + [s['name'] for s in c['series']]
        series = [dict(s['points']) for s in c['series']]
        dates = sorted(set(d for s in series for d in s))
        rows = [[d] + [fmt(s.get(d), c['unit']) for s in series] for d in dates]
    else:
        headers = ['Name'] + (c['labels'] if c['kind'] == 'grouped' else ['Change'])
        rows = [[r['name']] + [fmt(v,c['unit'],c.get('signed',False)) for v in (r['values'] if c['kind'] == 'grouped' else [r['value']])] for r in c['rows']]
    return '<details class="gc-data"><summary>View data</summary><div class="gc-scroll"><table><thead><tr>'+''.join('<th>'+html.escape(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div></details>'


CSS = '''
.gateway-charts{--gc-bg:#fff;--gc-ink:#14263b;--gc-muted:#536579;--gc-border:#dce5ef;color:var(--gc-ink);font:15px/1.5 system-ui,sans-serif;scroll-margin-top:70px}
.gateway-charts *{box-sizing:border-box}.gateway-charts a{color:#2563eb}.gateway-charts h2{font-size:29px;letter-spacing:-.7px;margin:0 0 8px;color:var(--gc-ink)}
.gateway-charts .gc-intro{color:var(--gc-muted);max-width:850px;margin:0 0 22px}.gc-eyebrow{font-size:11px;letter-spacing:1.8px;font-weight:700;color:#0f766e;text-transform:uppercase;margin:22px 0 7px}
.gc-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:20px}.gc-kpi{border-top:3px solid #2563eb;background:var(--gc-bg);padding:17px;border-radius:8px;box-shadow:0 1px 4px #14263b0b}
.gc-kpi span{display:block;color:var(--gc-muted);font-size:12px}.gc-kpi strong{display:block;font-size:28px;letter-spacing:-.7px;line-height:1.45}.gc-kpi small{font-size:11px;color:var(--gc-muted)}
.gc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.gc-card{padding:21px;background:var(--gc-bg);border:1px solid var(--gc-border);border-radius:12px;min-width:0;break-inside:avoid;scroll-margin-top:65px}
.gateway-charts .gc-card h3{font-size:18px;line-height:1.35;margin:0 0 7px;color:var(--gc-ink)}.gc-sub{font-size:12px;line-height:1.6;color:var(--gc-muted);min-height:40px;margin:0 0 8px}
.gateway-charts .gc-card svg{display:block;width:100%;height:auto;overflow:visible;margin:7px 0 12px}.gateway-charts svg text{fill:var(--gc-muted);font:14px system-ui,sans-serif}.gateway-charts svg .gc-value{font-size:13px;font-weight:600;fill:var(--gc-ink)}.gc-gridline{stroke:var(--gc-border);stroke-width:1}
.gc-legend{display:flex;gap:8px 16px;flex-wrap:wrap;margin:10px 0;font-size:12px;color:var(--gc-muted)}.gc-legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
.gc-note,.gc-source{font-size:11px;line-height:1.6;color:var(--gc-muted);margin:10px 0 0}.gc-source{border-top:1px solid var(--gc-border);padding-top:9px}.gc-data{font-size:11px;margin-top:8px}.gc-data summary{cursor:pointer;color:#2563eb}.gc-scroll{overflow:auto;max-height:270px}.gc-data table{width:100%;border-collapse:collapse}.gc-data td,.gc-data th{padding:7px;text-align:right;white-space:nowrap;border-bottom:1px solid var(--gc-border);font-size:11px}.gc-data td:first-child,.gc-data th:first-child{text-align:left}
.gc-method{padding:18px 22px;border-left:3px solid #0f766e;background:var(--gc-bg);border-radius:5px;margin:20px 0;font-size:12px;color:var(--gc-muted)}.gc-warning{padding:12px 16px;background:#fff3cd;color:#734b00;border-radius:8px;margin:10px 0}
.gc-nav{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;margin:17px 0 22px}.gc-pairs{border:1px solid var(--gc-border);border-radius:8px;padding:14px 18px;margin:20px 0;background:var(--gc-bg)}
@media(prefers-color-scheme:dark){.gateway-charts{--gc-bg:#152131;--gc-ink:#eef4fd;--gc-muted:#a9b9cf;--gc-border:#304157}.gateway-charts a,.gc-data summary{color:#89b6ff}.gc-eyebrow{color:#5dd7c0}}
@media(max-width:960px){.gc-grid{grid-template-columns:1fr}.gc-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.gc-card{padding:14px}.gc-kpi{padding:12px}.gc-kpi strong{font-size:23px}.gateway-charts h2{font-size:25px}}
@media print{.gateway-charts{--gc-bg:#fff;--gc-ink:#111;--gc-muted:#444;--gc-border:#ddd}.gc-grid{display:block}.gc-card{margin:14px 0}.gc-data,.gc-nav{display:none}.gc-card svg{max-height:310px}.gc-kpis{grid-template-columns:repeat(4,1fr)}}
'''


def render(report):
    o, v = report['openrouter'], report['vercel']
    e = html.escape
    period = f"vs {o['baseline']} · {o['interval_days']} days" if o['baseline'] else 'No comparable baseline'
    cards = [
        ('OpenRouter · 7-day tokens', fmt(o['tokens_7d']/1e12, 'T'), 'Window ending '+o['asof']),
        ('OpenRouter · token growth', fmt(o['growth_pct'], '%', True), period),
        ('OpenRouter · free-tagged share', fmt(o['free_share_pct'], '%'), 'Share of all feed tokens'),
        ('Vercel · daily share history', str((dt.date.fromisoformat(v['asof'])-dt.date.fromisoformat(v['history_start'])).days+1)+' days' if v else 'n/a', 'Through '+v['asof'] if v else 'No successful data')]
    out = ['<style>'+CSS+'</style><section class="gateway-charts" id="token-growth"><p class="gc-eyebrow">Gateway research · weekly pulse</p><h2>Token growth &amp; share shifts</h2>',
           '<p class="gc-intro">Follow demand, see who gains share, and separate token adoption from estimated spend. Ten simple views of the two gateways, with dated comparisons and underlying data.</p>',
           '<nav class="gc-nav"><a href="#or-volume">Demand</a><a href="#or-lab-history">OpenRouter share</a><a href="#vc-lab-history">Vercel share</a><a href="'+LIVE+'ai-gateways-charts.html">Standalone chart pack</a><a href="'+LIVE+'gateway-weekly.html">Weekly brief</a></nav>',
           '<div class="gc-kpis">'+''.join('<div class="gc-kpi"><span>'+e(label)+'</span><strong>'+e(value)+'</strong><small>'+e(sub)+'</small></div>' for label,value,sub in cards)+'</div>']
    for warning in report['warnings']:
        out.append('<p class="gc-warning">'+e(warning)+'</p>')
    out.append('<div class="gc-grid">')
    for c in report['charts']:
        out.append('<article class="gc-card" id="'+c['id']+'"><h3>'+e(c['title'])+'</h3><p class="gc-sub">'+e(c['subtitle'])+'</p>')
        if c['kind'] == 'line':
            legend = [(s['name'],s['color']) for s in c['series']]
        elif c['kind'] == 'grouped':
            legend = list(zip(c['labels'],c['colors']))
        else:
            legend = [('Increase','#0d9488'),('Decrease','#e06652')]
        out.append('<div class="gc-legend">'+''.join('<span><i style="background:'+col+'"></i>'+e(label)+'</span>' for label,col in legend)+'</div>')
        out.append(line_svg(c) if c['kind'] == 'line' else bars_svg(c))
        if c.get('note'):
            out.append('<p class="gc-note">'+e(c['note'])+'</p>')
        out.append('<p class="gc-source"><a href="'+(VC_SOURCE if c['id'].startswith('vc-') else OR_SOURCE)+'">'+e(c['source'])+'</a></p>'+table(c)+'</article>')
    out.append('</div>')
    if o.get('tokens_30d') is not None:
        out.append('<div class="gc-pairs"><b>Relative scale.</b> OpenRouter: <b>'+fmt(o['tokens_30d']/1e12,'T')+'</b> observed tokens in the trailing 30-day feed (snapshot '+e(o['snapshot'])+'). Vercel described <b>tens of trillions per month</b> in its <a href="https://vercel.com/blog/ai-gateway-production-index-september-2026">17 Sep 2026 Production Index</a>, without an exact total. This disclosure does not support a precise size multiple.</div>')
    out.append('<div class="gc-method"><b>Reading the charts.</b> OpenRouter uses all prompt + completion tokens in each ranking snapshot, including rows whose last-active date is earlier than the window end. This scope can differ from text-only metrics elsewhere in the dashboard. History starts '+e(o['history_start'])+'; '+str(o['observations'])+' observations. Growth compares trailing 7-day totals; only pairs 7 days apart are strict WoW. We prefer an exact seven-day baseline, otherwise the closest one within 4–10 days. No annualization or interpolation.<br><br>Vercel weekly changes compare two complete sets of seven daily shares using simple averages, not volume-weighted weekly shares. Missing entries remain unknown. Lab movers require observations in both periods. Chart colors denote increases/decreases, not investment recommendations. Neither gateway represents the entire AI market, and their shares cannot be added.<br><br>Sources: <a href="'+OR_SOURCE+'">OpenRouter</a> and <a href="'+VC_SOURCE+'">Vercel AI Gateway</a> (<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>). Transformations: aggregation, daily-share averages and changes. Built '+e(report['generated_at'])+'.</div></section>')
    return ''.join(out)


def publish(wiki=WIKI):
    report = collect(wiki)
    fragment = render(report)
    page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenRouter + Vercel · Token growth and share shifts</title><style>body{margin:0;padding:28px;background:#f3f6fa}main{max-width:1200px;margin:auto}@media(prefers-color-scheme:dark){body{background:#0c1521}}@media(max-width:520px){body{padding:12px}}</style></head><body><main>'+fragment+'</main></body></html>'
    reports = wiki / '_data' / 'ai-gateways'
    write(reports / 'charts.json', json.dumps(report, ensure_ascii=False, indent=2))
    write(wiki / '_dashboards' / 'ai-gateways-charts.html', page)
    write(reports / 'exports' / (dt.date.today().isoformat()+'-ai-gateways-charts.html'), page)
    return fragment


if __name__ == '__main__':
    publish()
    print('Published ten gateway charts and an offline HTML attachment.')
