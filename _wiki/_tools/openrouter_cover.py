"""Opening Top Models chart, using OpenRouter's own calendar-week chart feed.

Offline renderer: or_fetch.py captures model_chart.json during the normal refresh.
The source's first-seen series order and UTC weekly-pace formula are retained.
The dashboard applies a muted palette and identifies the latest complete mix.
"""
import base64
import datetime as dt
import html
import json
import math
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
SOURCE = 'https://openrouter.ai/rankings'
ENDPOINT = 'https://openrouter.ai/api/frontend/v1/rankings/model-rankings-chart'
COLORS = ['#477ec0', '#269788', '#d9ac56', '#cc8268', '#b55d72',
          '#658dab', '#8b9e65', '#9c82bc', '#60afb2', '#c587a5',
          '#b69756', '#777caf', '#bd8c86', '#748d70', '#a37195',
          '#509b81', '#a5a375', '#7d6c9b', '#bd7961', '#54857a']
DAY_WEIGHTS = [.1431, .1483, .1525, .1515, .1484, .1257, .1305]


def validate(payload):
    chart = payload['data']
    rows = chart['data']
    stamp = dt.datetime.fromtimestamp(chart['cachedAt'] / 1000, dt.timezone.utc)
    if not rows:
        raise ValueError('Empty weekly history')
    prior = None
    for row in rows:
        date = dt.date.fromisoformat(row['x'])
        if date.weekday() != 0 or (prior and (date - prior).days != 7):
            raise ValueError('Expected contiguous Monday calendar weeks')
        if date > stamp.date() or not row['ys']:
            raise ValueError('Invalid weekly bucket')
        for value in row['ys'].values():
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError('Invalid token count')
        prior = date
    return chart


def load_chart(wiki):
    # A failed refresh must never replace the last usable year of history.
    errors = []
    for path in sorted((wiki / '_data/openrouter/raw').glob('*/model_chart.json'), reverse=True):
        try:
            return validate(json.loads(path.read_text(encoding='utf-8'))), path
        except (ValueError, KeyError, TypeError, OSError) as exc:
            errors.append(str(exc))
    raise ValueError('No usable Top Models history: ' + '; '.join(errors))


def weekly_forecast(chart):
    """Increment above observed tokens, matching the source's weekly pace.

    This is an estimate, never counted as observed usage. The source uses UTC
    whole hours, weekday weights and a cap relative to the previous week.
    """
    now = dt.datetime.fromtimestamp(chart['cachedAt'] / 1000, dt.timezone.utc)
    rows = chart['data']
    start = dt.date.fromisoformat(rows[-1]['x'])
    if start != now.date() - dt.timedelta(days=now.weekday()):
        return 0
    elapsed = sum(DAY_WEIGHTS[:now.weekday()]) + DAY_WEIGHTS[now.weekday()] * now.hour / 24
    total = sum(rows[-1]['ys'].values())
    previous = sum(rows[-2]['ys'].values()) if len(rows) > 1 else total
    extra = total * (1 / max(.01, elapsed) - 1)
    return max(0, extra if total > previous > 0 else min(extra, previous * 1.1))


def compact(value):
    for factor, suffix in [(1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')]:
        if value >= factor:
            return f'{value / factor:g}{suffix}'
    return f'{value:g}'


def nice_step(maximum):
    raw = maximum / 4
    power = 10 ** math.floor(math.log10(max(raw, 1)))
    return next(n * power for n in [1, 2, 2.5, 4, 5, 8, 10] if n * power >= raw)


def chart_svg(rows, series, colors, forecast, mode):
    totals = [sum(row['ys'].values()) for row in rows]
    maximum = max(totals[:-1] + [totals[-1] + forecast])
    step = nice_step(maximum)
    top = math.ceil(maximum / step) * step
    floor = 10 ** math.floor(math.log10(max(1, min(t for t in totals if t > 0))))
    if mode == 'log':
        top = max(floor * 10, 10 ** math.ceil(math.log10(maximum)))
        ticks = [10 ** n for n in range(int(math.log10(floor)), int(math.log10(top)) + 1)]
    else:
        ticks = [step * n for n in range(1, int(round(top / step)) + 1)]
    baseline, height = 292, 280
    def bar_height(value):
        if mode == 'linear':
            return height * value / top
        return max(0, height * math.log(max(value, floor) / floor) / math.log(top / floor))
    out = [f'<svg class="or-cover-plot" data-scale="{mode}" viewBox="0 0 1036 342" '
           f'role="group" aria-label="Weekly tokens by model, {mode} scale"'
           + (' hidden' if mode == 'log' else '') + '>',
           f'<defs><pattern id="or-cover-hatch-{mode}" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<rect width="6" height="6" fill="#bbc4d1"/><rect width="3" height="6" fill="#ccd3dd"/></pattern></defs>']
    for tick in ticks:
        out.append(f'<line class="or-cover-grid" x1="48" x2="1002" y1="{baseline - bar_height(tick):.3f}" y2="{baseline - bar_height(tick):.3f}"/>')
        out.append(f'<text class="or-cover-y" x="6" y="{baseline - bar_height(tick) + 4:.3f}">{compact(tick)}</text>')
    pitch = (1002 - 48) / len(rows)
    for index, row in enumerate(rows):
        x, width = 48 + pitch * index, pitch - 2
        extra = forecast if index == len(rows) - 1 else 0
        observed = totals[index]
        total = observed + extra
        label = f"Week of {row['x']}: {observed / 1e12:.2f} trillion observed tokens"
        if extra:
            label += f'; weekly pace {total / 1e12:.2f} trillion (estimate)'
        out.append(f'<g class="or-cover-week" data-week="{index}" tabindex="0" role="graphics-symbol" aria-label="{html.escape(label)}">')
        out.append(f'<rect class="or-cover-hit" x="{x:.3f}" y="0" width="{width:.3f}" height="292" fill="transparent"/>')
        cumulative = 0
        total_height = bar_height(total)
        for key in series:
            value = row['ys'].get(key, 0)
            if not value:
                continue
            # A logarithmic total with proportional segments preserves the mix,
            # matching the source's log transformation for stacked bars.
            bottom = baseline - total_height * cumulative / total
            segment_height = total_height * value / total
            cumulative += value
            out.append(f'<rect class="or-cover-segment" x="{x:.3f}" y="{bottom - segment_height:.3f}" '
                       f'width="{width:.3f}" height="{segment_height:.3f}" fill="{colors[key]}"/>')
        if extra:
            segment_height = total_height * extra / total
            out.append(f'<rect class="or-cover-segment" x="{x:.3f}" y="{baseline - total_height:.3f}" '
                       f'width="{width:.3f}" height="{segment_height:.3f}" fill="url(#or-cover-hatch-{mode})"/>')
        out.append('</g>')
    for index, row in enumerate(rows):
        date = dt.date.fromisoformat(row['x'])
        label = date.strftime('%b') + ' ' + str(date.day) + (', ' + str(date.year) if index == 0 else '')
        out.append(f'<text class="or-cover-x" data-tick="{index}" x="{48 + pitch * (index + .5):.3f}" y="315" text-anchor="middle"'
                   + ('' if index % 6 == 0 else ' hidden') + f'>{label}</text>')
    out.append('</svg>')
    return ''.join(out)


CSS = '''
.or-cover{background:#fbfcfe;color:#0c1014;color-scheme:light;scroll-margin-top:0;font-family:"OR Jakarta",Arial,sans-serif}
.or-cover *{box-sizing:border-box}
.or-cover-inner{max-width:1280px;margin:0 auto;padding:6px 6px 12px}
.or-cover .or-cover-title{display:flex;align-items:center;gap:8px;font:600 20px/28px "OR Jakarta",Arial,sans-serif;color:#0c1014;margin:0;border:0;padding:0;letter-spacing:-.5px}
.or-cover-title svg{width:16px;height:16px;flex:none}
.or-cover .or-cover-subtitle{font:500 14px/21px "OR Jakarta",Arial,sans-serif;margin:6px 0 0;color:#5d5e62}
.or-cover-toolbar{display:flex;justify-content:flex-end;margin:40px 27px 7px 0;height:30px}
.or-cover-switch{display:inline-flex;border:1px solid #dedee1;border-radius:6px;padding:2px;background:#f4f4f6;gap:0}
.or-cover .or-cover-switch button{appearance:none;cursor:pointer;border:0;border-radius:4px;padding:2px 9px;background:transparent;color:#626367;font:12px/20px Arial,sans-serif;min-width:37px;margin:0;box-shadow:none}
.or-cover .or-cover-switch button[aria-pressed="true"]{background:#fbfcfe;color:#963cff;box-shadow:0 1px 3px #00000018}
.or-cover button:focus-visible{outline:2px solid #963cff;outline-offset:3px}
.or-cover-canvas{position:relative;width:100%}
.or-cover-plot{display:block;width:100%;height:342px;overflow:visible}
.or-cover [hidden]{display:none!important}
.or-cover-plot text{font:12px "OR Jakarta",Arial,sans-serif;fill:#737478;font-variant-numeric:tabular-nums;pointer-events:none}
.or-cover-week{outline:none}
.or-cover-week:hover .or-cover-hit,.or-cover-week:focus .or-cover-hit{fill:#0f172a06}
.or-cover-week:focus-visible .or-cover-hit{stroke:#963cff;stroke-width:1}
.or-cover-segment{pointer-events:none}
.or-cover-tooltip{position:absolute;z-index:50;width:308px;max-width:calc(100% - 16px);background:#fff;color:#17191d;border:1px solid #e4e5e8;box-shadow:0 7px 30px #17203320;border-radius:8px;padding:13px 14px;pointer-events:none;font:12px/1.65 "OR Jakarta",Arial,sans-serif}
.or-cover-tooltip strong{font-size:13px;display:block;margin-bottom:7px}
.or-cover-tooltip-row{display:flex;gap:7px;align-items:center}
.or-cover-tooltip-row i{width:8px;height:8px;border-radius:2px;flex:none}
.or-cover-tooltip-row span{overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.or-cover-tooltip-row b{margin-left:auto;white-space:nowrap;font-weight:500;font-variant-numeric:tabular-nums}
.or-cover-tooltip-total{border-top:1px solid #eee;margin-top:7px;padding-top:6px;display:flex;justify-content:space-between}
.or-cover-tooltip small{display:block;color:#686a72;font-size:10px;margin-top:4px}
.or-cover .or-cover-credit{margin:0 28px 0 6px;color:#898b91;font:10px/17px "OR Jakarta",Arial,sans-serif}
.or-cover-credit a{color:inherit;text-decoration:none}
.or-cover-credit a:hover{text-decoration:underline}
@media(max-width:600px){.or-cover-inner{padding:12px 8px}.or-cover-toolbar{margin-top:27px;margin-right:6px}.or-cover .or-cover-title{font-size:19px}.or-cover .or-cover-subtitle{font-size:12px}.or-cover-credit{max-width:95%}}
'''

JS = r'''
(()=>{
const root=document.getElementById('token-growth');
if(!root || !root.classList.contains('or-cover')) return;
const data=JSON.parse(root.querySelector('.or-cover-data').textContent);
const canvas=root.querySelector('.or-cover-canvas'), tip=root.querySelector('.or-cover-tooltip');
const plots=[...root.querySelectorAll('.or-cover-plot')];
const buttons=[...root.querySelectorAll('[data-cover-scale]')];
const number=n=>(n/1e12).toLocaleString('en-US',{maximumFractionDigits:2})+'T';
function resize(){
 const width=canvas.clientWidth || 1036, left=48, right=width<600?8:34;
 const pitch=(width-left-right)/data.rows.length;
 const interval=Math.max(1,Math.round(110/pitch));
 for(const svg of plots){
  svg.setAttribute('viewBox',`0 0 ${width} 342`);
  svg.querySelectorAll('.or-cover-grid').forEach(line=>line.setAttribute('x2',width-right));
  svg.querySelectorAll('[data-week]').forEach(g=>{
   const x=left+Number(g.dataset.week)*pitch;
   for(const r of g.querySelectorAll('rect')){
    r.setAttribute('x',x);r.setAttribute('width',Math.max(.8,pitch-Math.min(2,pitch*.12)));
   }
  });
  svg.querySelectorAll('[data-tick]').forEach(t=>{
   const i=Number(t.dataset.tick);t.setAttribute('x',left+(i+.5)*pitch);
   if(i%interval===0 && (i===0 || left+(i+.5)*pitch<width-26))t.removeAttribute('hidden');else t.setAttribute('hidden','');
  });
 }
 tip.hidden=true;
}
function hide(){tip.hidden=true;}
function show(g){
 const i=Number(g.dataset.week), row=data.rows[i], total=Object.values(row.ys).reduce((a,b)=>a+b,0);
 tip.replaceChildren();
 const title=document.createElement('strong');title.textContent='Week of '+new Date(row.x+'T00:00:00Z').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});tip.append(title);
 for(const [key,value] of Object.entries(row.ys).sort((a,b)=>(a[0]==='Others')-(b[0]==='Others') || b[1]-a[1])){
  const line=document.createElement('div');line.className='or-cover-tooltip-row';
  const swatch=document.createElement('i');swatch.style.background=data.colors[key];
  const name=document.createElement('span');name.textContent=data.names[key] || key;
  const count=document.createElement('b');count.textContent=number(value)+' · '+(value/total*100).toFixed(1)+'%';
  line.append(swatch,name,count);tip.append(line);
 }
 const summary=document.createElement('div');summary.className='or-cover-tooltip-total';
 const label=document.createElement('span');label.textContent='Observed tokens';
 const amount=document.createElement('b');amount.textContent=number(total);summary.append(label,amount);tip.append(summary);
 if(i===data.rows.length-1 && data.forecast>0){
  const note=document.createElement('small');note.textContent='Hatched area: weekly pace '+number(total+data.forecast)+' (estimate). Week in progress; captured '+data.asof+'.';tip.append(note);
 }
 if(!plots.find(p=>!p.hasAttribute('hidden')).dataset.scale.includes('linear')){
  const note=document.createElement('small');note.textContent='Logarithmic totals; segment heights retain each model’s token share.';tip.append(note);
 }
 tip.hidden=false;
 const box=g.getBoundingClientRect(), frame=canvas.getBoundingClientRect();
 const x=box.left-frame.left, tw=tip.offsetWidth;
 tip.style.left=Math.max(4,Math.min(frame.width-tw-4,x>frame.width/2?x-tw-12:x+box.width+12))+'px';
 tip.style.top='0px';
}
buttons.forEach(button=>button.addEventListener('click',()=>{
 const mode=button.dataset.coverScale;
 buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 plots.forEach(p=>{if(p.dataset.scale===mode)p.removeAttribute('hidden');else p.setAttribute('hidden','');});
 hide();resize();
}));
for(const svg of plots){
 svg.querySelectorAll('[data-week]').forEach(g=>{
  g.addEventListener('pointerenter',()=>show(g));
  g.addEventListener('focus',()=>show(g));g.addEventListener('click',()=>show(g));
  g.addEventListener('blur',hide);
  g.addEventListener('keydown',e=>{
   if(e.key==='Escape'){hide();return;}
   if(e.key==='ArrowLeft'||e.key==='ArrowRight'){
    e.preventDefault();const i=Math.max(0,Math.min(data.rows.length-1,Number(g.dataset.week)+(e.key==='ArrowRight'?1:-1)));
    svg.querySelector(`[data-week="${i}"]`).focus();
   }
  });
 });
 svg.addEventListener('pointerleave',hide);
}
document.addEventListener('pointerdown',e=>{if(!canvas.contains(e.target))hide();});
if(typeof ResizeObserver!=='undefined')new ResizeObserver(resize).observe(canvas);
else window.addEventListener('resize',resize);
resize();
})();
'''


def render(wiki=None):
    wiki = Path(wiki) if wiki else WIKI
    try:
        chart, path = load_chart(wiki)
    except ValueError:
        return '<section id="token-growth"><h1>Top Models</h1><p>Weekly OpenRouter history is temporarily unavailable.</p></section>'
    rows = chart['data']
    series = list(dict.fromkeys(key for row in rows for key in row['ys']))
    colors = {key: COLORS[index % len(COLORS)] for index, key in enumerate(series)}
    colors['Others'] = '#bcc9d6'
    names = {'Others': 'Others'}
    pointer = (wiki / '_data/openrouter/latest.txt').read_text(encoding='utf-8').strip()
    catalog = json.loads((wiki / '_data/openrouter/raw' / pointer / 'catalog.json').read_text(encoding='utf-8'))['data']
    by_slug = {m.get('permaslug', m['slug']): m.get('short_name', m['name']) for m in catalog}
    for key in series:
        base, _, variant = key.partition(':')
        if base in by_slug:
            names[key] = by_slug[base] + (f' ({variant})' if variant else '')
    forecast = weekly_forecast(chart)
    asof = dt.datetime.fromtimestamp(chart['cachedAt'] / 1000, dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    data = dict(rows=rows, colors=colors, names=names, forecast=forecast, asof=asof)
    font_path = wiki / '_data/openrouter/assets/plus-jakarta-sans.woff2'
    font = ('@font-face{font-family:"OR Jakarta";font-weight:200 800;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,'
            + base64.b64encode(font_path.read_bytes()).decode() + ') format("woff2")}') if font_path.exists() else ''
    age = (dt.datetime.now(dt.timezone.utc).timestamp() * 1000 - chart['cachedAt']) / 86400000
    stale = ' · Last successful capture; awaiting refresh' if age > 3 else ''
    stamp = dt.datetime.fromtimestamp(chart['cachedAt'] / 1000, dt.timezone.utc).date()
    completed = [row for row in rows if dt.date.fromisoformat(row['x']) + dt.timedelta(days=7) <= stamp]
    legend_row = completed[-1] if completed else rows[-1]
    legend_items = ''.join('<span><i style="background:' + colors[key] + '"></i>' + html.escape(names.get(key, key)) + '</span>'
                           for key in sorted(legend_row['ys'], key=lambda key: (key == 'Others', -legend_row['ys'][key])))
    legend = ('<div class="or-cover-legend"><p>Model mix · week of ' + legend_row['x']
              + (' (complete week)' if completed else ' (in progress)')
              + ' · Hover or select any bar for its breakdown</p><div class="or-cover-legend-items">' + legend_items + '</div></div>')
    return ('<style>' + font + CSS + '</style><section class="or-cover" id="token-growth" aria-labelledby="or-cover-title">'
            '<div class="or-cover-inner"><p class="or-cover-kicker">Model adoption / OpenRouter</p><h2 class="or-cover-title" id="or-cover-title">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 3v16a2 2 0 0 0 2 2h16M8 17v-3M13 17V5M18 17V9"/></svg>Top models</h2>'
            '<p class="or-cover-subtitle">Weekly token usage by model. Follow demand and the changing model mix across OpenRouter.</p>'
            '<div class="or-cover-toolbar"><span class="or-cover-unit">CALENDAR WEEKS · TRILLIONS OF TOKENS</span><div class="or-cover-switch" role="group" aria-label="Y-axis scale">'
            '<button type="button" data-cover-scale="linear" aria-pressed="true">Linear</button>'
            '<button type="button" data-cover-scale="log" aria-pressed="false">Log</button></div></div>'
            '<div class="or-cover-canvas">' + chart_svg(rows, series, colors, forecast, 'linear')
            + chart_svg(rows, series, colors, forecast, 'log')
            + '<div class="or-cover-tooltip" role="tooltip" hidden></div></div>'
            + legend +
            '<p class="or-cover-credit">Source: <a href="' + SOURCE + '" target="_blank" rel="noopener">OpenRouter</a>, as of '
            + asof + '. Licensed under CC BY 4.0. · Hatched area: estimated weekly pace.' + stale + '</p></div>'
            '<script type="application/json" class="or-cover-data">' + json.dumps(data, ensure_ascii=True).replace('<', '\\u003c')
            + '</script></section><script>' + JS + '</script>')
