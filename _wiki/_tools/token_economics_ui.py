"""Four-panel OpenRouter study; static SVG charts also work in email attachments."""
import datetime as dt
import html
import json
import math
from pathlib import Path
from or_token_economics import BANDS, LABELS, WIKI, build

E = html.escape
LIVE = 'http://ds-cap-33:8080/wiki/_dashboards/'
COLORS = {'open': '#438cd2', 'closed': '#8b929b', 'unknown': '#c18a37', 'total': 'var(--te-total)', 'average': '#438cd2'}


def n(value, digits=2):
    return 'Unavailable' if value is None else f'{value:,.{digits}f}'


def svg(series, title, unit, coverage=None):
    points = [(date, value) for _, _, values in series for date, value in values if value is not None]
    if not points:
        return '<p class="te-empty">No priced observations available.</p>'
    dates = sorted({date for _, _, values in series for date, _ in values})
    ords = {date: dt.date.fromisoformat(date).toordinal() for date in dates}
    maximum = max(v for _, v in points)
    magnitude = 10 ** math.floor(math.log10(maximum)) if maximum > 0 else 1
    ymax = max(1e-9, math.ceil(maximum * 1.12 / magnitude * 2) / 2 * magnitude)
    left, right, top, bottom = 64, 596, 23, 245
    x = lambda d: left + (ords[d] - ords[dates[0]]) / max(1, ords[dates[-1]] - ords[dates[0]]) * (right - left)
    y = lambda v: bottom - v / ymax * (bottom - top)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 282" role="img" aria-label="{E(title)}"><title>{E(title)} · {E(unit)}</title>']
    for i in range(5):
        value = ymax * i / 4
        out.append(f'<line class="te-gridline" x1="{left}" x2="{right}" y1="{y(value):.2f}" y2="{y(value):.2f}"/><text x="{left-10}" y="{y(value)+4:.2f}" text-anchor="end">{value:,.2f}</text>')
    tick_indices = sorted({round(i * (len(dates)-1) / 4) for i in range(5)})
    for i in tick_indices:
        out.append(f'<text x="{x(dates[i]):.2f}" y="272" text-anchor="middle">{dt.date.fromisoformat(dates[i]).strftime("%d %b")}</text>')
    for key, name, values in series:
        segments, segment, previous = [], [], None
        for date, value in values:
            if value is None or (previous and ords[date] - ords[previous] > 10):
                if segment:
                    segments.append(segment)
                segment = []
            if value is not None:
                segment.append(f'{x(date):.2f},{y(value):.2f}')
            previous = date
        if segment:
            segments.append(segment)
        dash = ' stroke-dasharray="7 5"' if key in ('total', 'unknown') else ''
        for line in segments:
            out.append(f'<polyline fill="none" stroke="{COLORS[key]}" stroke-width="2.7"{dash} stroke-linejoin="round" points="{" ".join(line)}"/>')
        for date, value in values:
            if value is not None:
                matched = (coverage or {}).get((date, key))
                low = matched is not None and matched < 99
                marker = 'r="4" stroke="#c18a37" stroke-width="2"' if low else 'r="2.8"'
                hint = f' · token pricing coverage {n(matched)}%' if matched is not None else ''
                out.append(f'<circle cx="{x(date):.2f}" cy="{y(value):.2f}" {marker} fill="{COLORS[key]}"><title>{E(name)} · {date}: {n(value)} {E(unit)}{hint}</title></circle>')
    return ''.join(out) + '</svg>'


def data_table(headers, rows):
    return '<details class="te-data"><summary>View data &amp; coverage</summary><div class="te-scroll"><table><thead><tr>' + ''.join('<th>'+E(x)+'</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+E(str(v))+'</td>' for v in row)+'</tr>' for row in rows) + '</tbody></table></div></details>'


def render(report):
    history = report['history']
    latest = history[-1]
    total = latest['buckets']['total']
    all_keys = ('open', 'closed', 'unknown', 'total')
    price_coverage = [p['buckets']['total']['coverage_pct'] for p in history]
    def curves(metric, scale=1):
        return [(key, LABELS[key], [(p['window_end'], (p['buckets'][key][metric] / scale if p['buckets'][key][metric] is not None else None)) for p in history]) for key in all_keys]
    charts = [
        ('te-volume', '01', 'Token volumes', 'Trillion tokens · trailing seven days', curves('tokens', 1e12), 'T tokens',
         'Observed prompt + completion tokens. Unclassified traffic remains visible instead of being assigned to open or closed models.'),
        ('te-average', '02', 'Average listed token price', '$ per million tokens · unweighted catalogue index',
         [('average', 'Equal-weight mean · 50:50 input/output', [(p['snapshot'], p['average']['blend']) for p in history])], '$ / M tokens',
         'Each model gets equal weight; its price is the average of input and output list prices. Includes text models without observed usage. Model roster changes affect the index. Free variants and routers excluded.'),
        ('te-wap', '03', 'Volume-weighted token price', '$ per million matched tokens · list-price estimate', curves('wap'), '$ / M tokens',
         'Uses observed input/output volumes and snapshot list prices. Free tokens remain in the denominator. Unpriced tokens are excluded from both numerator and denominator.'),
        ('te-spend', '04', 'Estimated weekly token spend', '$ million · matched tokens only · list prices, cache off', curves('spend', 1e6), '$ M',
         'A list-price scenario for matched token usage. Coverage and traffic mix can move the series. It is not realized revenue, a billing forecast or a guaranteed upper bound.')]
    out = ['<style>'+CSS+'</style><section class="token-economics" id="token-economics" aria-labelledby="te-title">',
           '<p class="te-eyebrow">OPENROUTER / VOLUME, PRICE &amp; VALUE</p><h2 id="te-title">Token economics in four charts</h2>',
           '<p class="te-intro">How much usage is growing, what models cost, and how token mix translates into estimated spend. Open-weight, closed-weight and unclassified traffic, using prices captured alongside each usage snapshot.</p>',
           f'<div class="te-period"><b>{E(report["history_start"])} → {E(report["asof"])}</b><span>{len(history)} captured observations · seven-day windows can overlap</span><a href="{LIVE}token-economics.html">Open standalone study ↗</a></div>',
           '<div class="te-kpis">']
    cards = [('Weekly tokens', n(total['tokens']/1e12)+'T', 'HARD · window ending '+report['asof'], 'hard'),
             ('Weighted list price', '$'+n(total['wap'])+' / M', 'PARTIAL · matched token mix', 'partial'),
             ('Estimated weekly spend', '$'+n(total['spend']/1e6 if total['spend'] is not None else None)+'M', 'PARTIAL · list prices, cache off', 'partial'),
             ('Token pricing coverage', n(total['coverage_pct'])+'%', 'Matched tokens / all feed tokens', 'hard')]
    for title, value, detail, tag in cards:
        out.append(f'<div class="te-kpi"><span>{title}</span><strong>{E(value)}</strong><small class="te-{tag}">{E(detail)}</small></div>')
    series_coverage = ' · '.join(LABELS[key]+': '+n(latest['buckets'][key]['coverage_pct'])+'%' for key in BANDS)
    out += ['</div>', f'<p class="te-coverage">Pricing coverage across history: <b>{n(min(price_coverage))}%–{n(max(price_coverage))}%</b>. Latest matching coverage by category: <b>{E(series_coverage)}</b>.<br>Dollar estimates cover matched tokens only; missing prices are never treated as zero. “Closed-weight” is a listing proxy, not a license audit. Snapshot list prices applied to the prior week do not capture intraweek price changes.</p>', '<div class="te-panels">']
    for cid, index, title, subtitle, series, unit, note in charts:
        out.append(f'<article class="te-panel" id="{cid}"><p class="te-figure">FIGURE {index}</p><h3>{title}</h3><p class="te-unit">{subtitle}</p>')
        coverage = {(p['window_end'], key): p['buckets'][key]['coverage_pct'] for p in history for key in all_keys} if cid in ('te-wap','te-spend') else None
        out.append(svg(series, title, unit, coverage))
        out.append('<div class="te-legend">' + ''.join(f'<span><i style="--series:{COLORS[key]}" class="{"te-dash" if key in ("total","unknown") else ""}"></i>{E(label)}</span>' for key, label, _ in series) + '</div>')
        out.append('<p class="te-chart-note">'+E(note)+'</p>')
        if coverage:
            out.append('<p class="te-chart-note">Amber rings mark observations with less than 99% of that category’s tokens matched to prices. Coverage can change between observations.</p>')
        out.append(f'<p class="te-source">Source: <a href="https://openrouter.ai/rankings">OpenRouter</a> · Capstone calculations · {E(report["history_start"])} to {E(report["asof"])}; latest price vintage {E(report["latest_snapshot"])}.</p>')
        if cid == 'te-average':
            headers = ['Price vintage', 'Listed models', 'Input $/M', 'Output $/M', '50:50 index $/M']
            rows = [[p['snapshot'], p['average']['models'], n(p['average']['input']), n(p['average']['output']), n(p['average']['blend'])] for p in history]
        else:
            headers = ['Window start', 'Window end'] + [label + ' ('+unit+')' for _, label, _ in series] + [LABELS[key]+' coverage %' for key in all_keys]
            rows = [[p['window_start'], p['window_end']] + [n(dict(values).get(p['window_end'])) for _, _, values in series] + [n(p['buckets'][key]['coverage_pct']) for key in all_keys] for p in history]
        out.append(data_table(headers, rows)+'</article>')
    out.append('</div>')
    out += ['<details class="te-method"><summary>How the study is calculated · inputs, checks &amp; sensitivity</summary>',
            '<div class="te-grounding"><span class="te-hard">HARD · observed tokens and listed rates</span><span class="te-partial">PARTIAL · snapshot-price application and weight classification</span><span class="te-estimate">ESTIMATE · cache-hit scenarios</span></div>',
            '<ol><li><b>Volume:</b> sum prompt and completion tokens across every row, including models last active earlier in the window.</li>',
            '<li><b>Average price:</b> calculate (input list price + output list price) ÷ 2 for each valid standard text model, then average across models. This 50:50 convention is not actual input/output mix.</li>',
            '<li><b>Estimated spend:</b> sum input tokens × input price + output tokens × output price for exact, same-vintage price matches.</li>',
            '<li><b>Weighted price:</b> estimated matched spend ÷ matched tokens × 1,000,000. Free-tagged tokens are included at zero price; missing prices remain unknown.</li></ol>']
    out.append(f'<div class="te-worked"><b>Latest arithmetic · window {latest["window_start"]} to {latest["window_end"]}</b><p>Matched input: {n(total["input_tokens"],0)} tokens; output: {n(total["output_tokens"],0)} tokens.</p><p>Per-model input costs sum to ${n(total["input_cost"])}; output costs sum to ${n(total["output_cost"])}.</p><p>${n(total["input_cost"])} + ${n(total["output_cost"])} = ${n(total["spend"])} estimated spend.</p><p>${n(total["spend"])} ÷ {n(total["priced_tokens"],0)} matched tokens × 1,000,000 = <b>${n(total["wap"],4)} per million tokens</b>.</p><p>Input observations: OpenRouter ranking and model-list snapshots dated {E(latest["snapshot"])}.</p></div>')
    out.append('<h3>Cache sensitivity · scenarios, not measured discounts</h3><p>Replace the indicated fraction of input tokens with each model’s observed cache-read price. Keep the full input rate when a cache-read rate is absent. Cache-write charges, context tiers and non-token fees remain outside these scenarios.</p>')
    sensitivity = [[label, '$'+n(total[key]/1e6 if total[key] is not None else None)+'M', n((total[key]/total['spend']-1)*100) + '%' if total['spend'] else 'Unavailable']
                   for label,key in [('0% input cache reads','spend'),('50% input cache reads','cache50'),('70% input cache reads','cache70')]]
    out.append(data_table(['Scenario (ESTIMATE)', 'Matched weekly spend', 'Change vs cache off'], sensitivity))
    out.append('<h3>Checks &amp; limits</h3><ul class="te-checks">')
    for check in report['checks']:
        out.append('<li><b class="te-check-'+check['status'].lower()+'">'+E(check['status'])+'</b><span>'+E(check['name'])+'<small>'+E(check['kind'])+'</small></span></li>')
    out.append('</ul><p><b>No realized-spend calibration:</b> there is no verified, comparable billed-spend anchor. We fit no arbitrary factor. The separate weekly chart feed checks token scope and units only. Pricing coverage, routing, discounts, caching, context tiers and product mix limit interpretation.</p>')
    for key in ('scope', 'classification', 'spend', 'cache_sensitivity'):
        out.append('<p>'+E(report['method'][key])+'</p>')
    raw = latest['raw_diagnostics']
    out.append('<h3>Public-feed diagnostic · unresolved cost-like field</h3><p>The latest ranking includes <code>total_usage</code>, with a raw sum of <b>'+n(raw['total_usage_raw_sum'],6)+'</b> in <b>unverified units</b>, including '+str(raw['positive_usage_free_rows'])+' free-tagged rows with positive values. This differs numerically from the modeled list-price spend; those quantities are not compared as dollars or ratio-calibrated until their units, scope and fee treatment are verified. The observed public cache/BYOK counters sum to '+n(raw['cached_tokens_raw_sum'],0)+' / '+n(raw['byok_tokens_raw_sum'],0)+'; this does not establish zero real caching or BYOK usage.</p>')
    out.append(data_table(['Capture', 'Raw total_usage (unverified units)', 'Positive usage rows', 'Positive free-tagged rows', 'Raw cached tokens'], [[p['snapshot'],n(p['raw_diagnostics']['total_usage_raw_sum'],6),p['raw_diagnostics']['positive_total_usage_rows'],p['raw_diagnostics']['positive_usage_free_rows'],n(p['raw_diagnostics']['cached_tokens_raw_sum'],0)] for p in history]))
    out.append('<p><b>Historical coverage:</b> matching usage and price captures begin in July 2026. Earlier values are not reconstructed using today’s catalogue; absent snapshots are not interpolated. The model universe changes over time, so the average is not a constant-quality price index. Model absence does not establish a launch or retirement.</p>')
    out.append('<p><b>Vercel:</b> the public leaderboard supplies daily shares, without absolute volume or dollar totals. Keep the existing Vercel share study separate; no implied absolute spend or cross-gateway total is calculated. <a href="https://vercel.com/docs/ai-gateway/leaderboards">Vercel export methodology</a>.</p>')
    out.append('<p><b>Source definitions:</b> <a href="https://openrouter.ai/docs/api/api-reference/models/list-all-models-and-their-properties">OpenRouter model/pricing API</a> · <a href="https://openrouter.ai/docs/cookbook/administration/data-api">Public traffic scope</a> · <a href="https://openrouter.ai/docs/guides/best-practices/prompt-caching">OpenRouter cache pricing</a>. '+E(report['reference'])+'</p>')
    if report['warnings']:
        out.append('<ul>'+''.join('<li>'+E(w)+'</li>' for w in report['warnings'])+'</ul>')
    return ''.join(out)+'</details></section>'


def standalone(report):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenRouter · Token economics</title><style>body{margin:0;background:#f4f7fa;padding:30px;font-family:system-ui,sans-serif}main{max-width:1240px;margin:auto}body>main>a{display:inline-block;margin:0 0 25px;color:#397bbb;font-size:12px}@media(max-width:600px){body{padding:14px}}@media print{body{padding:0;background:white}}</style></head><body><main><a href="'+LIVE+'openrouter.html#token-economics">← OpenRouter + Vercel dashboard</a>'+render(report)+'</main></body></html>'


def publish(wiki=WIKI):
    report = build(wiki)
    path = wiki / '_dashboards/token-economics.html'
    temp = path.with_suffix('.tmp')
    temp.write_text(standalone(report), encoding='utf-8')
    temp.replace(path)
    return render(report), report


CSS = r"""
.token-economics{--te-bg:#fff;--te-ink:#20334a;--te-muted:#576b80;--te-line:#dde6ee;--te-soft:#f4f7fa;--te-total:#253a50;color:var(--te-ink);font-family:inherit;font-size:13px;line-height:1.7;margin:36px 0 44px;scroll-margin-top:85px}.token-economics *{box-sizing:border-box}.token-economics h2{font-size:28px;letter-spacing:-.7px;line-height:1.3;margin:8px 0 12px;color:var(--te-ink)}.token-economics h3{font-size:18px;letter-spacing:-.25px;line-height:1.4;margin:3px 0 7px;color:var(--te-ink)}.token-economics a{color:#397fb6}.te-eyebrow{color:#298877;font-size:9px;letter-spacing:1.6px;font-weight:750;margin:0}.te-intro{max-width:870px;color:var(--te-muted);font-size:12px;line-height:1.9;margin:0 0 18px}.te-period{display:flex;flex-wrap:wrap;gap:7px 16px;font-size:10px;color:var(--te-muted);margin-bottom:20px}.te-period a{margin-left:auto;text-decoration:none}.te-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin-bottom:16px}.te-kpi{border:1px solid var(--te-line);border-radius:10px;padding:17px 19px;background:var(--te-bg)}.te-kpi>span{display:block;font-size:9px;text-transform:uppercase;letter-spacing:.4px;color:var(--te-muted)}.te-kpi>strong{display:block;font-size:27px;font-weight:650;letter-spacing:-.8px;margin:6px 0}.te-kpi small{font-size:9px}.te-hard{color:#238471}.te-partial{color:#427ea8}.te-estimate{color:#a8782f}.te-coverage{font-size:10px;line-height:1.85;padding:13px 16px;background:var(--te-soft);border-left:3px solid #c49854;margin:0 0 22px;color:var(--te-muted)}.te-panels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.te-panel{padding:24px;background:var(--te-bg);border:1px solid var(--te-line);border-radius:12px;min-width:0;break-inside:avoid}.te-figure{font-size:8px;color:#397fb6;letter-spacing:1.4px;font-weight:750;margin:0 0 7px}.te-unit{font-size:10px;color:var(--te-muted);margin:0 0 13px}.te-panel svg{display:block;width:100%;height:auto;margin:0 0 12px}.te-panel svg text{font:11px system-ui,sans-serif;fill:var(--te-muted)}.te-gridline{stroke:var(--te-line);stroke-width:1;stroke-dasharray:2 3}.te-legend{display:flex;flex-wrap:wrap;gap:5px 13px;font-size:9px;min-height:22px;color:var(--te-muted)}.te-legend span{display:inline-flex;align-items:center;gap:6px}.te-legend i{display:inline-block;width:19px;border-top:2px solid var(--series)}.te-legend i.te-dash{border-top-style:dashed}.te-chart-note{color:var(--te-muted);font-size:10px;line-height:1.8;min-height:52px;margin:12px 0}.te-source{border-top:1px solid var(--te-line);padding-top:11px;color:var(--te-muted);font-size:9px;line-height:1.8;margin:10px 0}.te-source a{text-decoration:none}.te-data{margin-top:10px;font-size:10px}.te-data summary{color:#397fb6;cursor:pointer;font-weight:600}.te-scroll{overflow:auto;max-height:340px;margin-top:10px}.te-data table{width:100%;border-collapse:collapse}.te-data th,.te-data td{padding:8px!important;border-bottom:1px solid var(--te-line);text-align:right;white-space:nowrap;font-size:10px!important;color:var(--te-ink)}.te-data th{color:var(--te-muted);font-weight:600}.te-data th:first-child,.te-data td:first-child{text-align:left}.te-method{margin-top:22px;padding:20px 24px;background:var(--te-bg);border:1px solid var(--te-line);border-radius:10px;font-size:11px;color:var(--te-muted)}.te-method>summary{color:var(--te-ink);cursor:pointer;font-weight:650;font-size:12px}.te-method p,.te-method li{font-size:11px;line-height:1.9}.te-method h3{font-size:15px;margin-top:24px}.te-grounding{display:flex;flex-wrap:wrap;gap:8px 20px;margin:18px 0;font-size:10px}.te-worked{background:var(--te-soft);border-radius:8px;padding:16px 20px;margin:18px 0}.te-worked p{margin:6px 0}.te-checks{list-style:none;padding:0}.te-checks li{display:flex;gap:12px;padding:9px 0;border-bottom:1px solid var(--te-line)}.te-checks b{min-width:86px;font-size:9px}.te-checks small{display:block;font-size:10px;color:var(--te-muted)}.te-check-pass{color:#298877}.te-check-partial,.te-check-unavailable,.te-check-review{color:#ad782e}.te-check-fail{color:#ba455a}.te-method a:focus-visible,.te-data summary:focus-visible,.te-method>summary:focus-visible{outline:2px solid #438cd2;outline-offset:4px}
.or-main .token-economics{--te-bg:var(--surf);--te-ink:var(--ink);--te-muted:var(--ink2);--te-line:var(--border);--te-soft:var(--plane);--te-total:var(--ink);font-family:inherit}.or-main .token-economics h2{font-size:25px}.or-main .token-economics .te-panel h3{font-size:16px}.or-main .te-method details{background:none}.or-main .token-economics .te-kpi{padding:18px}.or-main .token-economics .te-kpi>strong{font-size:27px}
@media(max-width:1100px){.te-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.te-panel{padding:18px}}@media(max-width:800px){.te-panels{grid-template-columns:1fr}.te-period a{margin-left:0}.te-chart-note{min-height:0}}@media(max-width:500px){.te-kpi{padding:14px}.te-kpi>strong,.or-main .token-economics .te-kpi>strong{font-size:23px}.te-kpi small{font-size:8px}.te-panel{padding:15px}.token-economics h2{font-size:24px}.te-method{padding:16px}.te-worked{padding:13px}}
@media print{.token-economics,.or-main .token-economics{--te-bg:#fff;--te-ink:#111;--te-muted:#444;--te-line:#ddd;--te-soft:#f8f8f8;--te-total:#222}.te-panels{grid-template-columns:1fr 1fr;gap:12px}.te-panel{padding:14px}.te-data,.te-period>a,.te-method{display:none}.te-chart-note{font-size:9px}.te-kpis{grid-template-columns:repeat(4,minmax(0,1fr))}}
"""
