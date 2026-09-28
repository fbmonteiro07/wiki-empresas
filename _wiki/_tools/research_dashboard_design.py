"""Portable Capstone dashboard presentation, shared by published research pages.

Applies the approved OpenRouter design language without transforming research data.
The sentiment publisher imports this module on every daily publication.
"""
import base64
import html
import re
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
PAGES = {
    'index.html': 'Sentiment research',
    'crowding-tracker.html': 'Attention & sentiment',
    'cnn-next-week.html': 'Fear & Greed',
    'cnn-spy-qqq-study.html': 'Fear & Greed · full study',
    'daily-brief.html': 'Daily briefing',
    'score-returns.html': 'Score & subsequent returns',
    'score-return-update.html': 'Score study · research update',
    'specialist-sales.html': 'Specialist sales',
    'narrative-diffusion.html': 'Narrative research',
}

# Legacy renderers inline colors in CSS and in SVG-generating JS. Semantic CSS
# variables keep those charts legible in both themes, including after a rerender.
COLORS = {
    '#0b1320': '--rd-bg', '#142033': '--rd-surface', '#121f31': '--rd-surface',
    '#101c2e': '--rd-soft', '#192b42': '--rd-soft',
    '#e7effb': '--rd-ink', '#e4edfa': '--rd-ink',
    '#a6b7ce': '--rd-muted', '#a5b5cb': '--rd-muted',
    '#2d4059': '--rd-border', '#2b3d55': '--rd-grid', '#2b3c53': '--rd-border',
    '#293b52': '--rd-grid', '#26384e': '--rd-grid', '#1c2d43': '--rd-soft',
    '#79adff': '--rd-blue', '#90b4ff': '--rd-blue', '#56d6c0': '--rd-teal',
    '#64d9c3': '--rd-teal', '#f295ad': '--rd-red', '#fa91a8': '--rd-red',
    '#c8a9f1': '--rd-purple', '#efb682': '--rd-orange', '#efc77f': '--rd-amber',
    '#1b3150': '--rd-blue-wash', '#1b2e46': '--rd-blue-wash',
    '#16372f': '--rd-green-wash', '#382637': '--rd-red-wash',
    '#392f21': '--rd-amber-wash', '#173333': '--rd-green-wash',
    '#162a45': '--rd-blue-wash', '#332333': '--rd-red-wash', '#342433': '--rd-red-wash',
    '#729cff': '--rd-blue', '#a1c3ff': '--rd-blue', '#e5a4b7': '--rd-red',
    '#293a50': '--rd-grid', '#9caec5': '--rd-muted', '#94a6be': '--rd-muted',
    '#e2b978': '--rd-amber', '#cfdaeb': '--rd-ink', '#355478': '--rd-border',
    '#192e4b': '--rd-blue-wash', '#122337': '--rd-blue-wash', '#192a40': '--rd-soft',
    '#1b2c44': '--rd-soft', '#1a3350': '--rd-blue-wash', '#15273d': '--rd-soft',
    '#352e25': '--rd-amber-wash', '#e8c28a': '--rd-amber', '#17283f': '--rd-surface',
    '#30455f': '--rd-border', '#57d7bd': '--rd-teal', '#ff94ac': '--rd-red',
    '#5e728e': '--rd-muted', '#9eb2cf': '--rd-muted', '#94aac9': '--rd-muted',
    '#0b1729': '--rd-soft', '#37557a': '--rd-border', '#7e9dff': '--rd-blue',
    '#83b4ff': '--rd-blue', '#8bdac8': '--rd-teal', '#9bafc8': '--rd-muted',
    '#a9b9cc': '--rd-muted', '#b5c7dc': '--rd-muted', '#1b2d46': '--rd-blue-wash',
    '#233b59': '--rd-blue-wash', '#253f61': '--rd-blue-wash', '#355070': '--rd-border',
    '#f3c479': '--rd-amber',
}


def market_context(market):
    current = (market or {}).get('meta', {}).get('current', {})
    score = current.get('score')
    if not isinstance(score, (float, int)) or not 0 <= score <= 100:
        return ''
    date = html.escape(str(current.get('timestamp', ''))[:10])
    rating = html.escape(str(current.get('rating', '')).capitalize())
    tone = 'greed' if 'greed' in rating.lower() else ('fear' if 'fear' in rating.lower() else 'neutral')
    return (f'<section class="rd-context" aria-label="Latest retained CNN reading">'
            f'<div class="rd-context-value"><p class="rd-eyebrow">LATEST RETAINED READING</p>'
            f'<strong>{score:.1f}<small>/ 100</small></strong><span class="rd-context-rating" data-tone="{tone}">{rating}</span>'
            f'<p><a href="https://www.cnn.com/markets/fear-and-greed">CNN Fear &amp; Greed</a> · {date}</p></div>'
            '<div class="rd-context-scale"><p>Market mood, in context</p>'
            f'<div class="rd-mood-scale" style="--reading:{score:.4f}%"><i></i></div>'
            '<div class="rd-mood-labels"><span>Fear</span><span>Neutral</span><span>Greed</span></div>'
            '<small>The reading above is context. The event study below uses historical zone entries and completed return windows.</small></div></section>')


def sidebar(name, local_nav=''):
    groups = [
        ('Sentiment monitor', [('index.html', 'Research overview'), ('crowding-tracker.html', 'Market radar'),
                               ('cnn-next-week.html', 'Fear & Greed'), ('daily-brief.html', 'Daily briefing')]),
        ('Stocks & evidence', [('score-returns.html', 'Score & returns'), ('specialist-sales.html', 'Specialist sales'),
                               ('narrative-diffusion.html', 'Narrative research')]),
        ('Methodology', [('cnn-spy-qqq-study.html', 'CNN · full study')]),
    ]
    out = ['<aside class="rd-sidebar"><a class="rd-brand" href="../index.html" aria-label="Capstone research dashboards">'
           '<span class="rd-brand-mark" aria-hidden="true">C</span><span>CAPSTONE<small>RESEARCH INTELLIGENCE</small></span></a>'
           '<nav class="rd-navigation" aria-label="Research dashboards">']
    index = 0
    for title, links in groups:
        out.append('<div class="rd-nav-group"><p>' + html.escape(title) + '</p>')
        for url, label in links:
            index += 1
            selected = ' aria-current="page"' if url == name else ''
            out.append(f'<a href="{url}"{selected}><span aria-hidden="true">{index:02d}</span>{html.escape(label)}</a>')
        out.append('</div>')
    out.append('</nav>')
    if local_nav:
        out.append('<div class="rd-local-label">RADAR VIEWS</div>' + local_nav)
    out.append('<div class="rd-sidebar-footer">MARKET RESEARCH<small>CNN · Bloomberg · X · specialist sales</small>'
               '<a href="../openrouter.html#token-growth">AI demand monitor <span aria-hidden="true">↗</span></a>'
               '<a href="../index.html">All research dashboards <span aria-hidden="true">↗</span></a></div></aside>')
    return ''.join(out)


def apply_design(body, name, asof, market=None):
    if name not in PAGES or 'id="research-dashboard-design"' in body:
        return body
    body = re.sub(r'#[a-fA-F0-9]{8}\b|#[a-fA-F0-9]{6}\b|#[a-fA-F0-9]{3}\b',
                  lambda m: 'var(' + COLORS[m.group().lower()] + ')' if m.group().lower() in COLORS else m.group(), body)
    body = body.replace('content="dark"', 'content="light"')
    body = re.sub(r'<html([^>]*)>', r'<html\1 data-theme="light">', body, count=1)
    # Some original standalone studies omit optional head/body tags.
    if not re.search(r'<body\b', body):
        if '<head>' not in body:
            body = re.sub(r'(<html[^>]*>)', r'\1<head>', body, count=1)
        body = body.replace('<main>', '</head><body><main>', 1).replace('</html>', '</body></html>')
    local_nav = ''
    if name == 'crowding-tracker.html':
        body = re.sub(r'<header class="topbar">.*?</header>', '', body, count=1, flags=re.S)
        match = re.search(r'<nav class="nav".*?</nav>', body, flags=re.S)
        if match:
            local_nav = re.sub(r'<a\b.*?</a>', '', match.group(), flags=re.S)
            body = body[:match.start()] + body[match.end():]
    if name == 'specialist-sales.html':
        body = re.sub(r'<header><strong>ATTENTION &amp; SENTIMENT</strong>.*?</header>', '', body, count=1, flags=re.S)
    body = re.sub(r'<nav\b[^>]*(?:aria-label="Wiki navigation"|class="sr-top")[^>]*>.*?</nav>', '', body, flags=re.S)
    if name in ('daily-brief.html', 'score-return-update.html'):
        body = re.sub(r'(<table\b.*?</table>)',
                      r'<div class="rd-table-scroll" role="region" aria-label="Return data table" tabindex="0">\1</div>',
                      body, flags=re.S)
    font_path = WIKI / '_data/openrouter/assets/plus-jakarta-sans.woff2'
    font = ('@font-face{font-family:"Research Jakarta";font-weight:200 800;font-display:swap;src:url(data:font/woff2;base64,'
            + base64.b64encode(font_path.read_bytes()).decode() + ') format("woff2")}') if font_path.exists() else ''
    body = body.replace('</head>', '<style id="research-dashboard-design">' + font + CSS + '</style></head>', 1)
    title = html.escape(PAGES[name])
    kind = 'rd-hub' if name == 'index.html' else ('rd-radar' if name == 'crowding-tracker.html' else 'rd-study')
    main_tag = re.search(r'<main\b[^>]*>', body).group()
    main_id_match = re.search(r'\bid="([^"]+)"', main_tag)
    main_id = main_id_match.group(1) if main_id_match else 'research-main'
    shell = ('<div class="rd-app ' + kind + '"><a class="rd-skip" href="#' + main_id + '">Skip to content</a>'
             + sidebar(name, local_nav) + '<div class="rd-workspace"><header class="rd-topbar">'
             '<div><p>RESEARCH / MARKET SENTIMENT</p><h1>' + title + '</h1></div><div class="rd-actions">'
             '<span class="rd-asof">Price snapshot<b>' + html.escape(asof) + '</b></span>'
             '<button type="button" class="rd-theme" aria-label="Switch to dark theme" aria-pressed="false">'
             '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20.5 13A8.5 8.5 0 0 1 11 3.5 8.5 8.5 0 1 0 20.5 13Z"/></svg></button></div></header>')
    body = re.sub(r'(<body\b[^>]*>)', lambda m: m.group() + shell, body, count=1)
    context = market_context(market) if name in ('cnn-next-week.html', 'cnn-spy-qqq-study.html') else ''
    accessible_main = main_tag[:-1] + (' id="research-main"' if not main_id_match else '')
    accessible_main += (' tabindex="-1"' if 'tabindex=' not in main_tag else '') + '>'
    body = body.replace(main_tag, accessible_main + context, 1)
    body = body.replace('</body>', '</div></div><script>' + JS + '</script></body>')
    return body


CSS = r"""
:root,:root[data-theme=light]{color-scheme:light;--rd-bg:#f4f6f9;--rd-surface:#fff;--rd-soft:#f7f9fb;--rd-ink:#192b40;--rd-muted:#647588;--rd-border:#dfe6ee;--rd-grid:#e7edf3;--rd-blue:#3778c9;--rd-teal:#168675;--rd-red:#b85269;--rd-purple:#9372b4;--rd-orange:#b97544;--rd-amber:#a06e23;--rd-blue-wash:#eaf1fa;--rd-green-wash:#eaf5f2;--rd-red-wash:#f8eef1;--rd-amber-wash:#fbf4e7;--rd-shadow:0 3px 16px #20334a04}
:root[data-theme=dark]{color-scheme:dark;--rd-bg:#111c29;--rd-surface:#182636;--rd-soft:#1c2c3f;--rd-ink:#e6edf5;--rd-muted:#a5b6c8;--rd-border:#304258;--rd-grid:#293a4d;--rd-blue:#80ace6;--rd-teal:#6bc5b3;--rd-red:#e29bad;--rd-purple:#bea2dc;--rd-orange:#d7a17b;--rd-amber:#e0b56d;--rd-blue-wash:#213a56;--rd-green-wash:#1e3a3d;--rd-red-wash:#392f41;--rd-amber-wash:#3a3428;--rd-shadow:none}
body,.sr-page{margin:0;background:var(--rd-bg);color:var(--rd-ink)}
.rd-app{font:14px/1.65 "Research Jakarta","Segoe UI",Arial,sans-serif;color:var(--rd-ink)}.rd-app *{box-sizing:border-box}.rd-app [hidden]{display:none!important}
.rd-app button,.rd-app input,.rd-app select{font-family:inherit;color-scheme:inherit}.rd-app a{color:var(--rd-blue);text-underline-offset:3px}.rd-app :focus-visible{outline:2px solid var(--rd-teal);outline-offset:4px}.rd-app [id]{scroll-margin-top:114px}
.rd-sidebar{position:fixed;inset:0 auto 0 0;width:232px;z-index:60;background:#11263b;color:#e9eff6;display:flex;flex-direction:column;padding:28px 16px 20px;overflow:auto;scrollbar-width:thin;scrollbar-color:#476176 transparent}
.rd-sidebar .rd-brand{display:flex;align-items:center;gap:11px;padding:0 12px 28px;text-decoration:none;color:#fff;font-size:14px;font-weight:750;letter-spacing:1.9px;line-height:1.4}.rd-brand-mark{display:grid;place-items:center;width:32px;height:36px;border:1px solid #4b7b87;border-radius:7px;color:#8ed3c3;font-size:22px;font-weight:500}.rd-brand small{display:block;font-size:7px;letter-spacing:1.15px;color:#a3b6c9;margin-top:5px}
.rd-nav-group{margin:0 0 21px}.rd-nav-group>p,.rd-local-label{margin:0 12px 9px;color:#8ca6bd;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px}
.rd-navigation a{display:flex;align-items:center;gap:11px;padding:9px 12px;margin:3px 0;color:#b9c9d8;border-radius:6px;text-decoration:none;font-size:11.5px}.rd-navigation a>span{color:#7791a8;font-size:10px;font-variant-numeric:tabular-nums}.rd-navigation a:hover{background:#ffffff09;color:#fff}.rd-navigation a[aria-current=page]{background:#244557;color:#fff;box-shadow:inset 3px 0 #77cbb8}.rd-navigation a[aria-current=page]>span{color:#8bd5c3}
.rd-sidebar-footer{margin-top:auto;border-top:1px solid #ffffff16;padding:18px 12px 0;font-size:9px;color:#c1d1df;letter-spacing:.7px}.rd-sidebar-footer small{display:block;color:#91a9bf;font-size:9px;letter-spacing:0;margin:5px 0 12px}.rd-sidebar-footer a{display:block;color:#a9bfd1;font-size:10px;text-decoration:none;letter-spacing:0;margin-top:9px}
.rd-sidebar .nav{position:static;display:flex;flex-direction:column;gap:0;background:transparent;border:0;padding:0;margin:0 0 22px;overflow:visible}.rd-sidebar .nav button{text-align:left;border:0;padding:8px 12px;margin:2px 0;border-radius:6px;color:#b9c9d8;font-size:10.5px;font-weight:500}.rd-sidebar .nav button[aria-selected=true]{background:#244557;color:#fff}.rd-sidebar .nav-number{color:#8ca6bd;font-size:9px}
.rd-workspace{margin-left:232px;min-width:0}.rd-topbar{position:sticky;top:0;z-index:45;display:flex;justify-content:space-between;align-items:center;gap:20px;min-height:91px;padding:18px 38px;background:var(--rd-surface);border-bottom:1px solid var(--rd-border)}.rd-topbar p{color:var(--rd-muted);font-size:9px;letter-spacing:1.5px;font-weight:650;margin:0 0 3px}.rd-topbar h1{margin:0;font-size:20px;letter-spacing:-.55px;font-weight:650;line-height:1.4}.rd-actions{display:flex;align-items:center;gap:22px}.rd-asof{text-align:right;color:var(--rd-muted);font-size:10px;white-space:nowrap}.rd-asof b{display:block;color:var(--rd-ink);font-size:12px;font-weight:600;font-variant-numeric:tabular-nums}.rd-theme{display:grid;place-items:center;width:36px;height:36px;background:var(--rd-soft);border:1px solid var(--rd-border);border-radius:8px;color:var(--rd-muted);cursor:pointer}.rd-theme svg{width:16px;height:16px}
.rd-app main{max-width:1440px;margin:0 auto;padding:32px 38px 75px;outline:none}.rd-app main>h1,.rd-app .view-head h1,.rd-app .wl h1,.rd-app .sr-header h1{font:650 27px/1.35 "Research Jakarta","Segoe UI",sans-serif;letter-spacing:-.8px;color:var(--rd-ink)}.rd-app main h2{font-family:inherit;font-size:18px;line-height:1.4;font-weight:650;letter-spacing:-.35px}.rd-app main h3{font-family:inherit;font-size:15px;font-weight:650;letter-spacing:-.2px}
.rd-app main p,.rd-app .view-head p{font-size:12px;line-height:1.85;color:var(--rd-muted)}.rd-app main small{color:var(--rd-muted)}.rd-app main a:hover{text-decoration:underline}.rd-app main .eyebrow,.rd-eyebrow,.rd-app .sr-eyebrow{font-size:9px;font-weight:750;letter-spacing:1.5px;text-transform:uppercase;color:var(--rd-teal)}
.rd-app .card,.rd-app .wl-card,.rd-app .sr-card,.rd-app .insight{background:var(--rd-surface);border:1px solid var(--rd-border);border-radius:12px;box-shadow:var(--rd-shadow);min-width:0}.rd-app .card-head,.rd-app .wl-card-head,.rd-app .sr-card-head{padding:23px 24px 16px}.rd-app .card-body,.rd-app .wl-card-body,.rd-app .sr-card-body{padding:0 24px 23px}.rd-app .card-head p,.rd-app .wl-card-head p{font-size:11px;margin-top:6px;line-height:1.8}
.rd-app .view-head{margin-bottom:24px}.rd-app .metrics{background:none;border:0;gap:14px;border-radius:0;overflow:visible;margin:24px 0}.rd-app .metric{border:1px solid var(--rd-border)!important;border-radius:10px;background:var(--rd-surface);padding:20px;min-width:0}.rd-app .metric-label{font-size:10px;letter-spacing:.5px;text-transform:uppercase;font-weight:650}.rd-app .metric-value{font-size:30px;letter-spacing:-1px;font-weight:650;margin:8px 0 4px}.rd-app .metric-note{font-size:10px;line-height:1.7}.rd-app .metric .unit{font-size:11px}
.rd-app .radar-grid{grid-template-columns:minmax(0,1.5fr) minmax(330px,1fr)}.rd-app .stock-grid{grid-template-columns:minmax(0,1.8fr) minmax(280px,1fr)}.rd-app .radar-grid>*,.rd-app .stock-grid>*,.rd-app .split>*{min-width:0}.rd-app .chart .label{stroke:var(--rd-surface)}.rd-app .chart text{font-family:inherit}.rd-app .chart-note{font-size:10px;line-height:1.8;border-color:var(--rd-grid)}.rd-app .legend{font-size:10px;gap:10px 16px}.rd-app .rank-title{font-size:9px;letter-spacing:.8px}.rd-app .rank-row{background:var(--rd-surface);padding:12px 0}.rd-app .rank-row strong{font-size:12px}.rd-app .rank-change{font-size:13px}.rd-app .rank-return{font-size:10px}.rd-app .rank-foot{font-size:10px;line-height:1.8}
.rd-app .control,.rd-app .btn,.rd-app .sr-toolbar select,.rd-app .sr-button,.rd-app .wl select,.rd-app .wl button.wl-btn{background:var(--rd-surface);color:var(--rd-ink);border:1px solid var(--rd-border);border-radius:7px;font-family:inherit;font-size:11px;line-height:1.5;padding:9px 12px;min-height:38px;max-width:100%}.rd-app .btn.primary{background:var(--rd-blue);color:#fff}.rd-app .seg{background:var(--rd-soft);border-color:var(--rd-border)}.rd-app .seg button{font-size:10px;font-family:inherit}.rd-app .seg button[aria-pressed=true]{background:var(--rd-surface);color:var(--rd-teal)}
.rd-app .callout,.rd-app .wl-callout,.rd-app .mkt-note{font-size:11px;line-height:1.85;background:var(--rd-blue-wash);color:var(--rd-ink);border-radius:8px;padding:15px 18px}.rd-app .callout.amber,.rd-app .wl-callout.warn{background:var(--rd-amber-wash);color:var(--rd-amber);border-left:3px solid var(--rd-amber)}.rd-app .inline-note,.rd-app .insight p{font-size:11px;line-height:1.8}.rd-app .insight .eyebrow{font-size:9px}
.rd-app main table{font-size:12px;width:100%;border-collapse:collapse}.rd-app main th{font-size:10px;letter-spacing:.25px;background:var(--rd-soft);color:var(--rd-muted);font-weight:650}.rd-app main th,.rd-app main td{padding:11px 14px;border-color:var(--rd-grid)}.rd-app .name-cell{font-size:10px}.rd-app .table-top{padding:18px 24px}.rd-app .table-wrap,.rd-app .scroll,.rd-app .wl-scroll{overflow:auto}
.rd-app main details{padding:16px 18px;background:var(--rd-surface);border:1px solid var(--rd-border);border-radius:8px;margin-top:14px;font-size:12px}.rd-app main summary{font-size:12px;font-weight:600;color:var(--rd-ink);cursor:pointer}.rd-app .source-item details,.rd-app details.source-item{border-left:0;border-right:0;border-radius:0;padding:12px 0}.rd-app .excerpt{font-size:11px;line-height:1.8}.rd-app .footer{font-size:10px;line-height:1.7}
.rd-context{display:grid;grid-template-columns:1fr 1.3fr;gap:40px;padding:25px 28px;margin:0 0 30px;background:var(--rd-surface);border:1px solid var(--rd-border);border-radius:12px;box-shadow:var(--rd-shadow)}.rd-context-value>strong{display:inline-block;font-size:43px;font-weight:650;letter-spacing:-1.5px;line-height:1.3;margin:6px 14px 5px 0;font-variant-numeric:tabular-nums}.rd-context-value>strong small{font-size:13px;font-weight:400;letter-spacing:0;margin-left:8px}.rd-context-rating{vertical-align:6px;background:var(--rd-amber-wash);color:var(--rd-amber);padding:5px 10px;border-radius:5px;font-size:11px;font-weight:650}.rd-app .rd-context-value>p:last-child{margin:0;font-size:10px}.rd-context-scale{align-self:center;max-width:590px}.rd-app .rd-context-scale>p{font-size:12px;font-weight:600;color:var(--rd-ink);margin:0 0 18px}.rd-mood-scale{height:8px;border-radius:4px;background:linear-gradient(to right,#ba7080 0%,#c29a5b 30%,#c4cbd0 50%,#79aaa0 70%,#2d897b 100%);position:relative}.rd-mood-scale i{position:absolute;left:var(--reading);top:-5px;width:3px;height:18px;background:var(--rd-ink);border-radius:2px;box-shadow:0 0 0 2px var(--rd-surface)}.rd-mood-labels{display:flex;justify-content:space-between;color:var(--rd-muted);font-size:9px;margin:10px 0}.rd-context-scale>small{font-size:10px;line-height:1.7;display:block}
.rd-app .wl{font-family:inherit;font-size:13px;color:var(--rd-ink)}.rd-app .wl> .wl-head:first-child{margin-bottom:22px;align-items:center}.rd-app .wl> .wl-head:first-child h1{max-width:800px}.rd-app .wl p{font-size:11px;color:var(--rd-muted);line-height:1.8}.rd-app .wl label{font-size:10px;color:var(--rd-muted);font-weight:600;display:flex;flex-direction:column;gap:6px;max-width:100%}.rd-app .wl-head>label{min-width:150px}.rd-app .wl-controls{padding:18px 20px;background:var(--rd-surface);border:1px solid var(--rd-border);border-radius:10px;align-items:end;gap:18px;margin-bottom:18px}.rd-app .wl-controls label{flex:1}.rd-app .wl-controls select{width:100%;background:var(--rd-soft)}.rd-app .wl-controls:before{content:'STUDY SETTINGS';font-size:9px;font-weight:700;letter-spacing:1px;color:var(--rd-teal);align-self:center;margin-right:8px}
.rd-app .wl .wl-title{font-size:27px;line-height:1.35;font-weight:650;letter-spacing:-.8px;margin:7px 0 8px}.rd-app main .rd-eyebrow,.rd-app .wl .wl-eyebrow{font-size:9px;letter-spacing:1.4px;font-weight:750;color:var(--rd-teal);margin:0}
.rd-app .wl-summary{gap:14px;margin-bottom:18px}.rd-app .wl-tile{position:relative;padding:20px;border:1px solid var(--rd-border);border-top:3px solid var(--rd-amber);background:var(--rd-surface);color:var(--rd-ink);border-radius:10px;box-shadow:var(--rd-shadow);font-family:inherit;cursor:pointer}.rd-app .wl-tile[data-tone=greed]{border-top-color:var(--rd-teal)}.rd-app .wl-tile[aria-pressed=true]{border-color:var(--rd-blue);box-shadow:0 0 0 1px var(--rd-blue);background:var(--rd-blue-wash)}.rd-app .wl-tile strong{display:block;font-size:30px;line-height:1.4;font-weight:650;margin:5px 0 3px;letter-spacing:-.8px}.rd-app .wl-tile strong span{font-size:11px!important}.rd-app .wl-tile small{font-size:10px;line-height:1.6;color:var(--rd-muted)}.wl-threshold-label{font-size:9px;letter-spacing:.9px;text-transform:uppercase;font-weight:700;color:var(--rd-muted)}.wl-selected{float:right;font-size:8px;letter-spacing:.3px;font-weight:700;color:var(--rd-blue);visibility:hidden}.wl-tile[aria-pressed=true] .wl-selected{visibility:visible}.rd-app .wl-tile p{border-top:1px solid var(--rd-border);padding-top:10px;margin-top:12px;display:flex;justify-content:space-between;gap:10px}.wl-tile p span{font-size:10px;color:var(--rd-muted)}.wl-tile p b{display:block;color:var(--rd-ink);font-size:15px;font-weight:650;letter-spacing:-.3px}
.rd-app .wl-baseline{background:var(--rd-soft);border:1px solid var(--rd-border);padding:15px 20px;font-size:11px;color:var(--rd-ink);gap:22px;margin-bottom:26px}.rd-app .wl-baseline b{font-size:16px;font-weight:650;margin:0 4px}.rd-app .wl-baseline small{font-size:10px}.rd-app .wl-card{margin-bottom:23px}.rd-app .wl-card h2{font-size:17px}.rd-app .wl-legend{font-size:10px;color:var(--rd-muted);gap:9px 16px}.rd-app .wl-note{font-size:10px;line-height:1.85;color:var(--rd-muted);padding:13px 24px;background:var(--rd-soft);border-color:var(--rd-grid)}.rd-app .wl svg text{font-family:inherit;fill:var(--rd-muted)}.rd-app .wl-group:hover .wl-hover,.rd-app .wl-group:focus .wl-hover{fill:var(--rd-blue-wash)}.rd-app .wl-stats{gap:18px;padding-top:6px}.rd-app .wl-stats strong{font-size:27px;font-weight:650;letter-spacing:-.8px}.rd-app .wl-stats span{font-size:10px;color:var(--rd-muted);line-height:1.7;margin-top:5px}.rd-app .wl-up{color:var(--rd-teal)}.rd-app .wl-down{color:var(--rd-red)}.rd-app .wl-small{font-size:10px;color:var(--rd-muted)}.rd-app .wl-split{gap:20px}.rd-app .wl .wl-empty{font-size:12px;color:var(--rd-muted)}.rd-app .wl details p{font-size:11px}
.rd-app .mkt{background:var(--rd-surface);border:0;border-radius:12px;padding:22px 0;margin:12px 0}.rd-app .mkt>h2{font-size:25px}.rd-app .mkt svg text{fill:var(--rd-muted)}.rd-app .mkt>h3{margin-top:30px}.rd-app .mkt-note{margin:20px 0}.rd-app .mkt details{padding:16px}.rd-app .mkt-legend{font-size:11px}
.rd-app .sr-context{background:var(--rd-blue-wash);border-color:var(--rd-border);border-radius:12px}.rd-app .sr-page,.rd-app .sr-panel{font-family:inherit}.rd-app .sr-toolbar{padding:18px 20px;background:var(--rd-surface);border:1px solid var(--rd-border);border-radius:10px}.rd-app .sr-toolbar select{min-width:0}.rd-app .sr-top{display:none}
.rd-hub main>.grid{gap:20px;margin-top:27px}.rd-hub .grid>a.card{padding:26px;text-decoration:none;display:flex;flex-direction:column;gap:8px}.rd-hub .grid>a.card h2{font-size:18px;margin:0}.rd-hub .grid>a.card p{font-size:12px;margin:0}.rd-hub .grid>a.card:hover{border-color:var(--rd-teal);box-shadow:0 4px 20px #20334a09}.rd-hub .grid>a[href="cnn-next-week.html"]{grid-column:1/-1;order:-1;border-top:3px solid var(--rd-teal);background:var(--rd-green-wash)}.rd-hub .grid>a[href="cnn-next-week.html"] h2{font-size:24px}.rd-hub .grid>a[href="cnn-next-week.html"]:before{content:'MARKET SENTIMENT / CNN';font-size:9px;letter-spacing:1.4px;color:var(--rd-teal);font-weight:700}.rd-hub .note{background:var(--rd-blue-wash);font-size:11px;line-height:1.8}.rd-hub .meta{font-size:10px;margin-top:20px}
.rd-skip{position:fixed;left:250px;top:-100px;z-index:100;background:var(--rd-surface);padding:12px 18px;border-radius:6px}.rd-skip:focus{top:12px}
.rd-table-scroll{max-width:100%;overflow:auto;margin:15px 0;border:1px solid var(--rd-border);border-radius:8px}.rd-app .rd-table-scroll table{margin:0}.rd-app #score-return-email{font-family:inherit!important;border:1px solid var(--rd-border)}
.rd-context-rating[data-tone=greed]{background:var(--rd-green-wash);color:var(--rd-teal)}.rd-context-rating[data-tone=neutral]{background:var(--rd-soft);color:var(--rd-muted)}
@media(min-width:1021px) and (max-width:1350px){.rd-sidebar{width:210px;padding-left:10px;padding-right:10px}.rd-workspace{margin-left:210px}.rd-app main{padding:28px 24px 70px}.rd-topbar{padding-left:24px;padding-right:24px}.rd-app .radar-grid,.rd-app .stock-grid,.rd-app .wl-split,.rd-app .sr-charts,.rd-app .sr-bottom{grid-template-columns:1fr}.rd-app .wl-controls:before{display:none}.rd-app .wl-summary{grid-template-columns:repeat(2,minmax(0,1fr))}.rd-app .wl-tile p{justify-content:flex-start;gap:35px}.rd-context{gap:24px}}
@media(max-width:1020px){.rd-sidebar{position:sticky;inset:auto;top:0;width:auto;height:auto;min-height:50px;max-height:100px;padding:0 16px;display:block;overflow:auto;scrollbar-width:none}.rd-sidebar::-webkit-scrollbar{display:none}.rd-sidebar .rd-brand,.rd-sidebar-footer,.rd-nav-group>p,.rd-navigation a>span,.rd-local-label{display:none}.rd-navigation{display:flex;width:max-content;align-items:center;gap:5px;min-height:50px}.rd-nav-group{display:contents}.rd-navigation a{white-space:nowrap;padding:8px 11px;font-size:10px}.rd-navigation a[aria-current=page]{box-shadow:inset 0 -2px #77cbb8}.rd-sidebar .nav{display:flex;flex-direction:row;gap:5px;width:max-content;margin:0 0 7px}.rd-sidebar .nav button{font-size:10px;white-space:nowrap;padding:7px 10px}.rd-sidebar .nav-number{display:none}.rd-workspace{margin-left:0}.rd-topbar{position:relative;padding:20px 24px}.rd-app main{padding:26px 24px 65px}.rd-app [id]{scroll-margin-top:120px}.rd-app .radar-grid,.rd-app .stock-grid,.rd-app .wl-split,.rd-app .sr-charts,.rd-app .sr-bottom{grid-template-columns:1fr}.rd-app .wl-summary{grid-template-columns:repeat(2,minmax(0,1fr))}.rd-app .wl-controls:before{display:none}.rd-skip{left:16px}}
@media(max-width:600px){.rd-topbar{padding:16px;min-height:82px;gap:12px}.rd-topbar h1{font-size:18px}.rd-topbar p{font-size:7px;letter-spacing:1px}.rd-actions{gap:10px}.rd-asof{font-size:8px}.rd-asof b{font-size:10px}.rd-theme{width:30px;height:30px}.rd-app main{padding:22px 14px 50px}.rd-app main>h1,.rd-app .view-head h1,.rd-app .wl h1{font-size:23px;letter-spacing:-.6px}.rd-app .rd-context{grid-template-columns:1fr;padding:21px;gap:20px;margin-bottom:25px}.rd-context-value>strong{font-size:38px}.rd-context-scale{max-width:none}.rd-context-scale>small{font-size:9px}.rd-app .wl-head{align-items:start;flex-direction:column;gap:15px}.rd-app .wl-controls{padding:15px;gap:13px}.rd-app .wl-controls label{flex:1 1 100%}.rd-app .wl-controls select{font-size:10px}.rd-app .wl-summary{gap:10px}.rd-app .wl-tile{padding:14px}.rd-app .wl-tile strong{font-size:26px}.rd-app .wl-tile small{font-size:9px}.wl-threshold-label{font-size:8px;letter-spacing:.3px}.wl-selected{font-size:7px}.rd-app .wl-tile p{gap:10px;flex-wrap:wrap}.wl-tile p b{font-size:13px}.rd-app .wl-baseline{gap:12px 20px;padding:15px}.rd-app .wl-baseline>span:first-child{flex-basis:100%}.rd-app .wl-card-head,.rd-app .wl-card-body,.rd-app .card-head,.rd-app .card-body{padding-left:17px;padding-right:17px}.rd-app .wl-card-head{padding-top:19px}.rd-app .wl-card h2{font-size:15px}.rd-app .wl-chart>svg{min-width:520px}.rd-app .wl-chart{overflow:auto}.rd-app .wl-stats{gap:8px}.rd-app .wl-stats strong{font-size:23px}.rd-app .wl-stats span{font-size:9px}.rd-app .wl-note{padding:12px 17px;font-size:9px}.rd-app .metrics{gap:10px;grid-template-columns:repeat(2,minmax(0,1fr))}.rd-app .metric{padding:15px}.rd-app .metric-label{font-size:8px}.rd-app .metric-value{font-size:25px}.rd-app .metric-note{font-size:9px}.rd-app .metric-value .unit{font-size:9px}.rd-app .radar-grid{grid-template-columns:minmax(0,1fr)}.rd-app .view-head .tag{font-size:10px}.rd-hub .grid>a.card{padding:21px}.rd-hub .grid>a[href="cnn-next-week.html"] h2{font-size:21px}.rd-app .sr-header{flex-wrap:wrap}.rd-app .sr-context{grid-template-columns:1fr}.rd-app .sr-toolbar{padding:15px}.rd-app .sr-toolbar label{max-width:100%}.rd-app .sr-toolbar select{min-width:0;max-width:100%}}
@media(prefers-reduced-motion:reduce){.rd-app *{scroll-behavior:auto!important;transition:none!important}}
@media(max-width:600px){.rd-app .wl .wl-title{font-size:23px;letter-spacing:-.6px}}
@media print{.rd-sidebar,.rd-actions,.rd-skip{display:none}.rd-workspace{margin:0}.rd-topbar{position:static;padding:0 0 20px}.rd-app main{padding:20px 0;max-width:none}.rd-app .card,.rd-app .wl-card,.rd-app .rd-context{break-inside:avoid;box-shadow:none}.rd-app .wl-chart>svg{min-width:0}}
"""

JS = r"""
(()=>{
 const button=document.querySelector('.rd-theme');
 if(button)button.addEventListener('click',()=>{
  const dark=document.documentElement.dataset.theme!=='dark';
  document.documentElement.dataset.theme=dark?'dark':'light';
  button.setAttribute('aria-pressed',String(dark));
  button.setAttribute('aria-label',dark?'Switch to light theme':'Switch to dark theme');
 });
})();
"""
