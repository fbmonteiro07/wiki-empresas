"""Credit monitor presentation. All research stays in its attributed inputs."""
import base64
import datetime as dt
import html
import re
from pathlib import Path
from funding_common import change_text, market_health

E = html.escape
SECTIONS = [('overview', 'Overview'), ('market', 'Market gauges'), ('spreads', 'Relative spreads'),
            ('counterparty', 'Counterparty risk'), ('repricing', 'Loan pricing'), ('issuance', 'Issuance'),
            ('ledger', 'Deal ledger'), ('scoreboard', 'Appetite signals'), ('watch', 'Watchlist')]


def enhance(page, deals, market):
    health = market_health(market, deals)
    review_date = deals['asof']
    age = (dt.date.today() - dt.date.fromisoformat(review_date)).days
    state = 'Market data current' if health['ok'] else 'Market data needs attention'
    status = 'current' if health['ok'] else 'attention'
    fontpath = Path(__file__).resolve().parents[1] / '_data/openrouter/assets/plus-jakarta-sans.woff2'
    font = ('@font-face{font-family:Jakarta;font-weight:200 800;font-display:swap;src:url(data:font/woff2;base64,'
            + base64.b64encode(fontpath.read_bytes()).decode() + ') format("woff2")}') if fontpath.exists() else ''
    nav = ''.join(f'<a href="#{key}"><span>{i:02d}</span>{title}</a>' for i, (key, title) in enumerate(SECTIONS, 1))
    sidebar = ('<aside class="credit-sidebar"><a class="credit-brand" href="index.html"><b>C</b><span>CAPSTONE<small>RESEARCH INTELLIGENCE</small></span></a>'
               '<p class="nav-label">AI CREDIT &amp; FUNDING</p><nav aria-label="Dashboard sections">' + nav + '</nav>'
               '<div class="sidebar-foot"><p>WEEKLY MONITOR</p><strong>Friday · 09:00</strong><small>America/Sao_Paulo</small>'
               '<a href="openrouter.html">AI demand monitor ↗</a><a href="index.html">All dashboards ↗</a></div></aside>')
    topbar = ('<div class="credit-topbar"><div><span class="eyebrow">RESEARCH / CAPITAL MARKETS</span><p>AI credit &amp; funding</p></div>'
              '<div class="top-actions"><span class="top-date">MARKET OBSERVATIONS<b>' + E(health['latest']) + '</b></span>'
              '<button id="print-view" type="button">Print / PDF</button><button id="theme-toggle" type="button" aria-label="Switch to dark theme" aria-pressed="false">Dark mode</button></div></div>')
    page = page.replace('<html lang="en">', '<html lang="en" data-theme="light">')
    page = page.replace('</head>', '<meta name="description" content="Capstone AI credit and funding monitor: credit spreads, funding conditions and attributed deal evidence."><style>' + font + CSS + '</style></head>')
    page = page.replace('<div class="wrap">', '<a class="skip-link" href="#main">Skip to content</a>' + sidebar + '<div class="credit-workspace">' + topbar + '<main id="main" class="wrap" tabindex="-1">', 1)
    page = page.replace('</div>\n<script>', '</main></div>\n<script>', 1)
    section_iter = iter(SECTIONS)
    page = re.sub(r'<section>', lambda _: '<section id="' + next(section_iter)[0] + '">', page)
    page = re.sub(r'<div class="meta">.*?</div>\s*</header>', '</header>', page, count=1, flags=re.S)
    rows = ''.join('<tr><td><b>' + E(s['label']) + '</b><small>Bloomberg · ' + E(s['ticker']) + '</small></td><td class="num">'
                   + E(change_text(s, 7)) + '</td></tr>' for s in market.get('series', []))
    issues = ('<ul>' + ''.join('<li>' + E(x) + '</li>' for x in health['issues']) + '</ul>') if health['issues'] else ''
    freshness = (f'<div class="freshness {status}"><span class="status-dot"></span><b>{state}</b><span>Observations {E(health["earliest"])} → {E(health["latest"])}</span>'
                 f'<span class="research-age">Research ledger · {E(review_date)} · {age} days old</span></div>' + issues)
    overview = ('<div class="weekly-grid"><article class="weekly-card"><p class="eyebrow">THE WEEK IN CREDIT</p><h2>What changed in the market</h2>'
                '<p class="sub">Seven-day lookback from each latest observation. Positive = higher spread or yield.</p><div class="tscroll"><table class="weekly-table"><tbody>' + rows + '</tbody></table></div></article>'
                '<article class="weekly-card thesis-card"><p class="eyebrow">RESEARCH LENS</p><h2>Follow the financing constraint</h2><p>' + E(deals['meeting_thesis']) + '</p>'
                f'<div class="evidence-note"><b>Research evidence · {E(review_date)}</b><p>Broker snapshots, deal terms and appetite judgments below retain their source dates. A market refresh does not update those claims.</p></div>'
                '<a class="text-link" href="../themes/ai-compute-deals.md">Open the compute-deal timeline ↗</a></article></div>')
    page = page.replace('<section id="overview">', freshness + '<section id="overview">' + overview)
    for section in ('spreads', 'counterparty', 'repricing', 'issuance', 'scoreboard'):
        page = page.replace(f'<section id="{section}">', f'<section id="{section}"><p class="section-kicker">DATED RESEARCH · LEDGER {E(review_date)}</p>')
    page = page.replace('<h2>Where the stress lives — YTD spread change by bucket</h2>', '<h2>Relative spread performance</h2>')
    page = page.replace('<h2>Neocloud repricing path</h2>', '<h2>Neocloud loan pricing · historical observations</h2>')
    page = page.replace('<h2>Watch</h2>', '<h2>Watchlist &amp; review queue</h2><p class="sub">Past dates are flagged for outcome review. An elapsed event date does not establish its outcome.</p>')
    page = re.sub(r'<b>Live bond series slot:</b>.*?automatically\.', '<b>Coverage gap:</b> Individual project-bond prices are not connected. The yields above are a dated broker snapshot; they are not live marks.', page, flags=re.S)
    for watch in deals['watch']:
        date = watch['date']
        past = bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', date) and date < dt.date.today().isoformat())
        if past:
            page = page.replace(f'<li><b class="num">{E(date)}</b>', f'<li><span class="review-label">Outcome review due</span><b class="num">{E(date)}</b>')
    choices = ''.join('<option>' + E(c) + '</option>' for c in dict.fromkeys(d['category'] for d in deals['deals']))
    toolbar = ('<div class="ledger-tools"><label>Find a deal<input id="deal-search" type="search" placeholder="Issuer, instrument, source…"></label>'
               '<label>Financing category<select id="deal-category"><option value="">All categories</option>' + choices + '</select></label>'
               '<button id="clear-filters" type="button">Reset</button><span id="deal-count" role="status" aria-live="polite"></span></div>')
    page = page.replace('<div class="card tscroll"><table>', toolbar + '<div class="card tscroll"><table id="deal-table">', 1)
    page = page.replace('</tbody></table></div>\n</section>\n\n<section id="scoreboard">', '</tbody></table><p id="no-deals" hidden>No matching deals. Clear the filters to see all records.</p></div>\n</section>\n\n<section id="scoreboard">', 1)
    page = re.sub(r'<footer>.*?</footer>', '<footer><b>CAPSTONE · INTERNAL RESEARCH</b><p>Bloomberg market observations and separately dated research. Weekly routine: Fridays at 09:00 America/Sao_Paulo, with an email summary. Weekly and monthly changes use observations on or before the lookback date, with up to four calendar days of tolerance; insufficient history stays unavailable.</p><p>Built ' + dt.date.today().isoformat() + ' · Research ledger ' + E(review_date) + ' · All amounts retain their original scope and attribution.</p></footer>', page, flags=re.S)
    return page.replace('</body>', '<script>' + JS + '</script></body>')


CSS = r"""
:root{--paper:#f3f6f8;--card:#fff;--ink:#20334a;--ink2:#55667b;--mut:#65768a;--grid:#e6ebf0;--line:#dfe6ed;--axis:#c9d3df;--s1:#387dbc;--s2:#bf704d;--s3:#258979;--shadow:0 3px 14px #20334a04}
:root[data-theme=dark]{--paper:#101923;--card:#172330;--ink:#e2eaf2;--ink2:#bdcada;--mut:#a0b0c1;--grid:#2b3c4c;--line:#304354;--axis:#41576c;--s1:#78afe1;--s2:#edab85;--s3:#6cc8b6}
html{scroll-behavior:smooth}body{padding:0;font-family:Jakarta,'Segoe UI',sans-serif;font-size:13px}button,input,select{font:inherit}button,input,select{border:1px solid var(--line);border-radius:7px;background:var(--card);color:var(--ink);padding:10px 13px;min-height:40px}button{cursor:pointer}button:hover{border-color:var(--s3)}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--s1);outline-offset:3px}[hidden]{display:none!important}
.credit-sidebar{position:fixed;inset:0 auto 0 0;width:226px;background:#152e43;color:#b9cbda;display:flex;flex-direction:column;padding:28px 17px;z-index:30}.credit-brand{display:flex;gap:12px;align-items:center;text-decoration:none;color:#f4f8fb;padding:0 10px 35px;letter-spacing:1.7px;font-weight:750}.credit-brand>b{border:1px solid #739c9c;color:#99d8c9;display:grid;place-items:center;width:34px;height:34px;border-radius:9px;font-size:22px}.credit-brand small{display:block;font-size:7px;letter-spacing:1.2px;margin-top:5px;color:#a0b7c8}.nav-label{font-size:9px;letter-spacing:1.1px;margin:0 13px 15px;color:#a3baca}.credit-sidebar nav a{display:flex;align-items:center;gap:13px;color:#bfd0de;text-decoration:none;font-size:11px;padding:12px;border-radius:6px;margin-bottom:3px}.credit-sidebar nav a span{color:#92adbf;font-size:9px}.credit-sidebar nav a:hover,.credit-sidebar nav a[aria-current=true]{color:#fff;background:#244657;box-shadow:inset 3px 0 #7ac7b6}.sidebar-foot{margin-top:auto;border-top:1px solid #ffffff1a;padding:19px 12px 0}.sidebar-foot p{font-size:8px;letter-spacing:1px}.sidebar-foot strong{display:block;color:#edf4f9;font-size:13px;margin:7px 0}.sidebar-foot small{font-size:9px}.sidebar-foot a{display:block;font-size:10px;color:#bcd0df;margin-top:15px;text-decoration:none}
.credit-workspace{margin-left:226px}.credit-topbar{padding:20px 36px;background:var(--card);border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:20px}.credit-topbar .eyebrow{font-size:8px;color:var(--mut);letter-spacing:1.4px}.credit-topbar p{font-size:19px;font-weight:650;margin-top:3px}.top-actions{display:flex;align-items:center;gap:10px}.top-actions button{font-size:10px}.top-date{font-size:8px;text-align:right;color:var(--mut);margin-right:8px;letter-spacing:.5px}.top-date b{display:block;font-size:11px;margin-top:3px;color:var(--ink);letter-spacing:0}.wrap{max-width:1500px;padding:30px 36px 60px;margin:auto;outline:none}.wrap>header{padding:0 0 20px;border:0}.wrap>header .eyebrow{color:var(--s3);font-size:9px}.wrap h1{font-size:32px;letter-spacing:-1.1px;margin:10px 0;line-height:1.3;font-weight:650}.dek{font-size:12px;line-height:1.9;max-width:90ch}.freshness{padding:13px 16px;border:1px solid var(--line);background:var(--card);border-radius:8px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;font-size:10px;color:var(--ink2)}.status-dot{width:7px;height:7px;border-radius:50%;background:var(--s3)}.attention .status-dot{background:var(--s2)}.research-age{margin-left:auto;color:var(--s2)}section{margin-top:30px;scroll-margin-top:20px}h2{font-size:19px;font-weight:650;letter-spacing:-.35px;margin-bottom:8px}.sub{font-size:11px;line-height:1.9;max-width:110ch}.section-kicker{font-size:8px;letter-spacing:1.2px;color:var(--s2);font-weight:700;margin-bottom:8px}
.weekly-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:18px;margin-bottom:20px}.weekly-card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px;min-width:0}.weekly-card .eyebrow{color:var(--s3);font-size:8px;letter-spacing:1.3px;margin-bottom:9px}.weekly-card h2{font-size:18px}.weekly-card>p:not(.eyebrow){font-size:11px;line-height:1.9;color:var(--ink2)}.weekly-table{font-size:10px}.weekly-table td{padding:12px 0}.weekly-table td:last-child{text-align:right;white-space:nowrap;font-size:9px}.weekly-table small{display:block;color:var(--mut);font-size:8px;font-weight:400;margin-top:4px}.weekly-table tr:last-child td{border:0}.thesis-card{border-top:3px solid var(--s3)}.evidence-note{padding:13px 0;border-top:1px solid var(--line);margin-top:17px;font-size:10px;color:var(--ink2)}.evidence-note p{font-size:10px;line-height:1.8;margin-top:5px}.text-link{font-size:10px;text-decoration:none;font-weight:650}
.tiles{grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}.tile{padding:18px;border-radius:10px;min-width:0}.tl{font-size:9px;line-height:1.7;min-height:30px;text-transform:uppercase;letter-spacing:.3px}.tv{font-size:27px;letter-spacing:-.7px;font-weight:650}.tu{font-size:12px}.td{font-size:9px;line-height:1.8;margin-top:9px}.tile-source{font-size:8px;color:var(--mut);margin-top:5px}.gpanels{grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.lpanel{min-width:0}figure.lpanel{padding:21px 21px 12px;border-radius:12px}figure.lpanel figcaption{font-size:11px;font-weight:500}.chart-value{display:block;font-size:27px;font-weight:650;letter-spacing:-.6px;margin:7px 0 2px}.chart-value small{font-size:11px;margin-left:5px}.chart-source{display:block;font-size:9px;font-weight:400;color:var(--mut);margin-bottom:15px}.card{padding:24px;border-radius:12px}.card>svg{max-width:1000px;margin:auto}.srow{font-size:11px;line-height:1.9;padding:13px 0}.chip{font-size:9px;margin-top:2px}.src{font-size:10px}.note{font-size:10px;line-height:1.9}.legend{font-size:10px}.ledger-tools{display:flex;flex-wrap:wrap;align-items:end;gap:13px;margin:17px 0}.ledger-tools label{font-size:9px;font-weight:650;display:flex;flex-direction:column;gap:6px}.ledger-tools input{width:270px;max-width:100%}.ledger-tools select{width:210px;max-width:100%}.ledger-tools input,.ledger-tools select,.ledger-tools button{font-size:11px}.ledger-tools #deal-count{margin-left:auto;font-size:10px;color:var(--mut);padding-bottom:11px}#deal-table{min-width:1000px;font-size:11px}#deal-table th{font-size:9px;background:var(--paper)}#deal-table td{padding:14px 11px;line-height:1.8}#deal-table td:last-child{min-width:285px}#deal-table td:nth-child(2){min-width:125px}#deal-table tr[data-category]:hover{background:var(--paper)}#no-deals{padding:25px;text-align:center;color:var(--mut)}.review-label{display:inline-block;font-size:8px;color:var(--s2);border:1px solid var(--line);border-radius:4px;padding:2px 6px;margin:0 8px 4px 0}ul.watch li{font-size:11px;line-height:1.9;padding:12px 0}footer{font-size:10px;line-height:1.9}footer>b{font-size:9px;letter-spacing:1px}footer p{margin-top:7px}.skip-link{position:fixed;top:-100px;left:240px;background:var(--card);z-index:99;padding:12px}.skip-link:focus{top:12px}
@media(max-width:1250px){.tiles{grid-template-columns:repeat(3,minmax(0,1fr))}.weekly-grid{grid-template-columns:1fr}.wrap{padding:25px}.credit-topbar{padding:20px 25px}}
@media(max-width:900px){.credit-sidebar{position:sticky;top:0;width:auto;display:block;padding:6px 12px;overflow-x:auto}.credit-brand,.nav-label,.sidebar-foot{display:none}.credit-sidebar nav{display:flex;width:max-content}.credit-sidebar nav a{margin:0;font-size:10px;padding:10px}.credit-sidebar nav a span{display:none}.credit-workspace{margin-left:0}.credit-topbar{padding:17px 20px}.wrap{padding:24px 20px}.top-date{display:none}section{scroll-margin-top:70px}}
@media(max-width:600px){.credit-topbar p{font-size:14px}.top-actions{gap:6px}.top-actions button{font-size:9px;padding:7px}.credit-topbar{padding:14px}.wrap{padding:23px 14px}.wrap h1{font-size:27px}.research-age{margin-left:0;width:100%}.freshness{font-size:9px}.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}.tile{padding:15px}.tv{font-size:24px}.gpanels{grid-template-columns:1fr}.weekly-card{padding:18px}.weekly-table td:last-child{white-space:normal;max-width:135px}.card{padding:15px}.card>svg{min-width:480px}.card:has(>svg){overflow-x:auto}.ledger-tools label{flex:1 1 100%}.ledger-tools input,.ledger-tools select{width:100%}.skip-link{left:14px}.srow{gap:7px}.chip{padding:2px 6px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{.credit-sidebar,.top-actions,.ledger-tools,.skip-link{display:none}.credit-workspace{margin:0}.credit-topbar{padding:0 0 15px}.wrap{padding:15px 0;max-width:none}.weekly-grid{grid-template-columns:1fr}.gpanels{grid-template-columns:1fr 1fr}.card,.tile,.lpanel,.weekly-card{box-shadow:none;break-inside:avoid}.tscroll{overflow:visible}#deal-table{min-width:0;font-size:8px}#deal-table td{min-width:0!important;padding:5px}#deal-table th{font-size:7px}.tiles{grid-template-columns:repeat(5,minmax(0,1fr))}.tv{font-size:21px}.card>svg{min-width:0}}
"""

JS = r"""
(()=>{
 const theme=document.querySelector('#theme-toggle');
 theme.addEventListener('click',()=>{const dark=document.documentElement.dataset.theme!=='dark';document.documentElement.dataset.theme=dark?'dark':'light';theme.textContent=dark?'Light mode':'Dark mode';theme.setAttribute('aria-pressed',String(dark));theme.setAttribute('aria-label',dark?'Switch to light theme':'Switch to dark theme');});
 document.querySelector('#print-view').addEventListener('click',()=>window.print());
 const search=document.querySelector('#deal-search'), category=document.querySelector('#deal-category'), table=document.querySelector('#deal-table');
 function filter(){let visible=0;const query=search.value.toLowerCase().trim();table.querySelectorAll('tr[data-category]').forEach(row=>{row.hidden=!!((category.value&&row.dataset.category!==category.value)||(query&&!row.textContent.toLowerCase().includes(query)));if(!row.hidden)visible++;});table.querySelectorAll('tr.cat').forEach(row=>{let next=row.nextElementSibling,any=false;while(next&&!next.classList.contains('cat')){if(!next.hidden)any=true;next=next.nextElementSibling;}row.hidden=!any;});document.querySelector('#deal-count').textContent=visible+' of '+table.querySelectorAll('tr[data-category]').length+' records';const empty=document.querySelector('#no-deals');if(empty)empty.hidden=visible>0;}
 search.addEventListener('input',filter);category.addEventListener('change',filter);document.querySelector('#clear-filters').addEventListener('click',()=>{search.value='';category.value='';filter();search.focus();});filter();
 const links=[...document.querySelectorAll('.credit-sidebar nav a')];
 const sections=[...document.querySelectorAll('main>section')];let queued=false;
 function activeSection(){let current=sections[0];sections.forEach(s=>{if(s.getBoundingClientRect().top<=150)current=s;});links.forEach(a=>{if(a.hash==='#'+current.id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});queued=false;}
 window.addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(activeSection);}},{passive:true});activeSection();
})();
"""
