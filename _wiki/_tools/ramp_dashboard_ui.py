"""Presentation only for the Ramp dashboard; source series and calculations stay in its builder."""
from html import escape, unescape
from pathlib import Path
import re

ASSETS = Path(__file__).with_suffix('')
GROUPS = [('adoption', 'Adoption', 'adoption'), ('models', 'Model mix', 'prov'),
          ('spending', 'Spending', 'spend'), ('tokens', 'Tokens', 'tokens'), ('sources', 'Sources & methods', 'basis')]
PANELS = {
 'adoption': ('adoption', 'Business AI adoption'),
 'vendor': ('adoption', 'Vendor penetration'),
 'sshare': ('adoption', 'AI share of business spend'),
 'prov': ('models', 'Provider usage'),
 'ladder': ('models', 'Model tiers'),
 'vintage': ('models', 'Model age'),
 'launch': ('models', 'Launch curves'),
 'cross': ('spending', 'Price vs volume'),
 'spend': ('spending', 'Spend per employee'),
 'segments': ('spending', 'Company segments'),
 'tokens': ('tokens', 'Token volume & prices'),
 'basis': ('sources', 'Sources & methodology'),
}


def growth_spotlight(page, metadata):
    """Promote the existing growth-table cells without recalculating any rates."""
    table = next((m[0] for m in re.finditer(r'<table\b[^>]*>.*?</table>', page, re.S)
                  if '<th>Cohort / percentile</th>' in m[0]), None)
    if table is None:
        raise ValueError('Ramp cohort growth table missing.')
    text = lambda value: unescape(re.sub(r'<[^>]+>', '', value)).strip()
    headers = [text(v) for v in re.findall(r'<th\b[^>]*>(.*?)</th>', table, re.S)]
    if headers[2:6] != ['m/m', '3-mo compound, %/mo', '12-mo compound, %/mo', 'y/y']:
        raise ValueError('Ramp growth columns changed; refusing to mislabel rates.')
    rows = {}
    for row in re.findall(r'<tr>(.*?)</tr>', table, re.S):
        cells = [text(v) for v in re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.S)]
        if cells:
            rows[cells[0]] = cells
    cards = []
    for key, source_name, label, color in [
        ('top1', 'Top 1% cohort', 'Top 1% cohort', 'var(--s3)'),
        ('top10', 'Top 10% cohort', 'Top 10% cohort', 'var(--s2)'),
        ('median', 'All companies (median)', 'Overall median', 'var(--s1)'),
    ]:
        row = rows[source_name]
        cards.append('<div class="growth-card" data-cohort="'+key+'" style="--cohort-color:'+color+'">'
            '<h3>'+label+'</h3><div class="growth-rate"><strong>'+escape(row[5])+'</strong><span>y/y</span></div>'
            '<div class="growth-facts"><span><b class="growth-mom">'+escape(row[2])+'</b> m/m</span>'
            '<span><b class="growth-level">'+escape(row[1])+'</b> / employee</span></div></div>')
    return ('<aside class="growth-spotlight" aria-labelledby="growth-title"><div class="growth-heading"><div>'
        '<h2 id="growth-title">AI spend growth</h2><p>Monthly spend per employee · '+escape(headers[1])+'</p></div>'
        '<a href="#spend-growth">Growth history ↗</a></div><div class="growth-cards">'+''.join(cards)+'</div>'
        '<p class="growth-source"><a href="#basis">Ramp Economics Lab</a> · retrieved '+escape(metadata.get('fetched_at', 'Unavailable'))+
        ' · Restated series. Cohorts are re-cut monthly.</p></aside>')


def enhance(page, metadata, monthly, token_week):
    spotlight = growth_spotlight(page, metadata)
    original_header = re.search(r'<header>.*?</header>', page, re.S)[0]
    original_intro = re.search(r'<p>.*?</p>', original_header, re.S)[0]
    original_footer = re.search(r'<footer>(.*?)</footer>', page, re.S)[1]
    nav = '<nav class="ramp-tabs" aria-label="Dashboard views">' + ''.join(
        f'<a href="#{first}" data-group="{group}">{label}</a>' for group, label, first in GROUPS) + '</nav>'
    nav += '<nav class="ramp-subnav" aria-label="Charts in this view">' + ''.join(
        f'<a href="#{key}" data-group="{group}">{label}</a>' for key, (group, label) in PANELS.items()) + '</nav>'
    page = re.sub(r'<nav class="toc">.*?</nav>', '', page, count=1, flags=re.S)
    pulled = escape(metadata.get('fetched_at', 'Unavailable'))
    header = ('<a class="skip-link" href="#adoption">Skip to chart</a>'
        '<header class="ramp-masthead"><a class="ramp-brand" href="index.html"><span class="ramp-brand-mark">C</span>CAPSTONE<small>Research</small></a>'
        '<div class="ramp-actions"><button id="ramp-theme" type="button" aria-label="Switch to light theme" aria-pressed="true">◐ Light mode</button>'
        '<a href="index.html">All dashboards ↗</a></div></header>'
        '<div class="ramp-heading"><div><p class="ramp-eyebrow">AI / ENTERPRISE ADOPTION</p><h1>Ramp AI Index</h1>'
        '<p>Adoption · provider usage · spending · token economics</p></div><div class="ramp-asof">'
        f'<b>Monthly data · {escape(monthly)}</b><br>Token sample · week to {escape(token_week)}<small>Ramp data retrieved {pulled}</small></div></div>')
    page = page.replace(original_header, header, 1)
    found = []
    def section(match):
        key, content = match.groups()
        if key not in PANELS:
            raise ValueError('Unknown Ramp section: '+key)
        found.append(key)
        group, label = PANELS[key]
        old_head = re.search(r'<h2>(.*?)</h2>', content, re.S)[1]
        unit = re.search(r'<span class="k">.*?</span>', old_head, re.S)
        unit = unit[0] if unit else ''
        content = re.sub(r'<h2>.*?</h2>', '<h2>'+label+unit+'</h2>', content, count=1, flags=re.S)
        if key != 'basis':
            lead = re.search(r'<p class="sub">.*?</p>', content, re.S)
            lead_text = lead[0] if lead else ''
            if lead:
                content = content.replace(lead[0], '', 1)
            content = re.sub(r'<p class="sub">(.*?)</p>', lambda p: '<details class="ramp-context"><summary>Context &amp; definitions</summary><p class="sub">'+p[1]+'</p></details>', content, flags=re.S)
            def note(n):
                classes, body = n.groups()
                heading = re.search(r'<b>(.*?)</b>', body, re.S)
                title = heading[1] if heading else 'Context & caveats'
                ident = ' id="spend-restatement"' if 'warnn' in classes and key == 'spend' else ''
                return '<details class="ramp-context"'+ident+'><summary>'+title+'</summary><div class="'+classes+'">'+body+'</div></details>'
            content = re.sub(r'<div class="(note[^"]*)">(.*?)</div>', note, content, flags=re.S)
            content += '<details class="ramp-context"><summary>Analysis &amp; interpretation</summary><div class="original-heading">'+old_head+'</div>'+lead_text+'</details>'
            if key == 'spend' and 'id="spend-restatement"' in content:
                alert = '<div class="ramp-alert"><b>Restated series</b><span>Use this vintage when quoting levels or growth.</span><a href="#spend-restatement">See revision details</a></div>'
                content = content.replace('</h2>', '</h2>'+alert, 1)
        else:
            content = content.replace('<h2>'+label, '<h2>'+label, 1)
            content += '<details class="ramp-source-details"><summary>Data coverage, retrieval and build details</summary>'+original_intro+'</details><div class="source-note">'+original_footer+'</div>'
        content = re.sub(r'<svg\b[^>]*class="chart".*?</svg>', lambda svg: '<div class="chart-wrap">'+svg[0]+'</div>', content, flags=re.S)
        if 'chart-wrap' in content:
            content = content.replace('</h2>', '</h2><p class="ramp-scroll-hint">Swipe the chart horizontally · tap a point for values</p>',1)
        if key == 'spend':
            content = content.replace('<h3>Growth by cohort and percentile', '<h3 id="spend-growth" class="growth-chart-title">Growth by cohort and percentile', 1)
        if key == 'adoption':
            content = nav + '<section id="adoption" class="ramp-panel" data-group="'+group+'">'+content+'</section>'
            return content
        return '<section id="'+key+'" class="ramp-panel" data-group="'+group+'">'+content+'</section>'
    page = re.sub(r'<section id="([^"]+)">(.*?)</section>', section, page, flags=re.S)
    if found != list(PANELS):
        raise ValueError('Ramp section order changed; refusing to drop or mislabel content.')
    targets = iter(['adoption','vendor','prov','ladder','spend','tokens'])
    page = re.sub(r'<div class="tile ([^"]*)">', lambda m: '<div class="tile '+m[1]+'" role="link" tabindex="0" data-target="'+next(targets)+'">',page,count=6)
    basis = ('<div class="ramp-basis"><span><b>Ramp customer panel.</b> Adoption counts paying firms; vendor penetration overlaps. Model share measures named-model usage; tokens come from the separate TSM sample.</span>'
             '<a href="#basis">Sources &amp; measurement basis ↗</a></div><p id="chart-keyboard-help" hidden>Use left and right arrows to inspect chart observations; Home and End jump to the first and last points. Escape dismisses values.</p>')
    page = page.replace('<main>', '<main>'+spotlight, 1)
    page = page.replace('</main>', basis+'</main>', 1)
    page = re.sub(r'<footer>.*?</footer>', '<footer class="ramp-footer"><span>CAPSTONE / INTERNAL RESEARCH</span><a href="#basis">Source: Ramp Economics Lab · '+pulled+'</a><span>Monthly panel · weekly token sample</span></footer>',page,count=1,flags=re.S)
    init = '<script>document.documentElement.dataset.theme="dark";try{const theme=localStorage.getItem("capstone-ramp-theme");if(theme==="light"||theme==="dark")document.documentElement.dataset.theme=theme;}catch{}</script>'
    page = page.replace('<style>', init+'<style>',1).replace('</style>', (ASSETS/'ramp.css').read_text(encoding='utf-8')+'</style>',1)
    script = '<script>'+(ASSETS/'ramp.js').read_text(encoding='utf-8')+'</script>'
    return page.replace('</body>',script+'</body>',1) if '</body>' in page else page+script
