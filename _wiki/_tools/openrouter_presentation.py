"""Shared presentation shell for the OpenRouter dashboard. No data transforms."""
from html import escape


def overview(fragment):
    """Group the existing long note without changing its content."""
    start = fragment.find('<p class="oc-note-p">')
    if start >= 0:
        end = fragment.index('</p>', start) + 4
        fragment = (fragment[:start] + '<details><summary>Definitions, coverage &amp; interpretation</summary>'
                    + fragment[start:end] + '</details>' + fragment[end:])
    return fragment.replace('<h1 id="oc-title">', '<h2 class="oc-headline" id="oc-title">').replace('</h1>', '</h2>')


def shell(asof):
    groups = [
        ("Demand & adoption", [("open-vs-closed", "Open vs closed"), ("token-growth", "Top models"), ("gateway-pulse", "Growth & share"), ("vercel", "Vercel Gateway")]),
        ("Economics", [("growth", "System growth"), ("value", "Tokens & dollars"), ("labs", "Lab leaderboard"), ("cloud", "Cross-cloud pricing"), ("neo", "Neocloud market"), ("gpu-pricing", "GPU pricing")]),
        ("Research", [("weekly", "Weekly brief"), ("method", "Method & sources")]),
    ]
    links = []
    index = 0
    for label, items in groups:
        links.append('<div class="or-nav-group"><p>' + escape(label) + '</p>')
        for anchor, title in items:
            index += 1
            links.append(f'<a href="#{anchor}"><span class="or-nav-number" aria-hidden="true">{index:02d}</span>{escape(title)}</a>')
        links.append('</div>')
    return (
        '<div class="or-dashboard"><a class="or-skip" href="#dashboard-main">Skip to dashboard</a>'
        '<aside class="or-sidebar"><a class="or-brand" href="index.html" aria-label="Capstone research dashboards">'
        '<span class="or-brand-mark" aria-hidden="true">C</span><span>CAPSTONE<small>RESEARCH INTELLIGENCE</small></span></a>'
        '<nav class="or-navigation" aria-label="Dashboard sections">' + ''.join(links) + '</nav>'
        '<div class="or-sidebar-footer"><span class="or-status-dot"></span>AI demand monitor<small>OpenRouter + Vercel AI Gateway</small>'
        '<a href="../index.html">Back to research wiki <span aria-hidden="true">↗</span></a></div></aside>'
        '<div class="or-workspace"><header class="or-topbar"><div><p class="or-breadcrumb">RESEARCH / AI INFRASTRUCTURE</p>'
        '<h1>AI demand monitor</h1></div><div class="or-topbar-actions">'
        '<span class="or-asof">OpenRouter snapshot <b>' + escape(asof) + '</b></span>'
        '<button type="button" class="or-theme" aria-label="Switch to dark theme" aria-pressed="false">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20.5 13A8.5 8.5 0 0 1 11 3.5 8.5 8.5 0 1 0 20.5 13Z"/></svg></button>'
        '</div></header><main id="dashboard-main" class="or-main" tabindex="-1">'
    )


CSS = r"""
:root,:root[data-theme=light]{color-scheme:light;--plane:#f4f6f9;--surf:#fff;--ink:#192b40;--ink2:#536478;--muted:#66788a;--grid:#e7edf3;--base:#c9d3de;--border:#dfe6ee;--s1:#3778c9;--s2:#168675;--s3:#b6789c;--s4:#bd8730;--s5:#527eae;--good:#137a62;--crit:#bf545f;--warn:#a56e19;--arrbar:#d4e3f5;--accent:#147d71;--wash:#eaf5f2;--shadow:0 3px 16px #20334a04}
:root[data-theme=dark]{color-scheme:dark;--plane:#111c29;--surf:#182636;--ink:#e6edf5;--ink2:#b3c0cf;--muted:#94a7bc;--grid:#293a4d;--base:#4d6075;--border:#304258;--s1:#72a6ea;--s2:#4fbaa7;--s3:#d59cba;--s4:#d6a956;--s5:#89afd6;--good:#66c8ad;--crit:#ef939b;--warn:#e4b66c;--arrbar:#2c507d;--accent:#70cfbe;--wash:#1e3a3d;--shadow:none}
body{background:var(--plane);color:var(--ink)}
.or-dashboard{font-family:"OR Jakarta","Segoe UI",Arial,sans-serif;font-size:14px;line-height:1.6}
.or-dashboard a{color:var(--s1);text-underline-offset:3px}
.or-dashboard button,.or-dashboard select{font-family:inherit}
.or-dashboard :focus-visible{outline:2px solid var(--accent);outline-offset:4px}
.or-dashboard [id]{scroll-margin-top:112px}
.or-sidebar{position:fixed;inset:0 auto 0 0;width:232px;background:#11263b;color:#e9eff6;display:flex;flex-direction:column;padding:29px 16px 20px;z-index:60;overflow:auto}
.or-sidebar .or-brand{display:flex;align-items:center;gap:11px;padding:0 12px 30px;color:#fff;text-decoration:none;font-size:14px;font-weight:750;letter-spacing:1.9px;line-height:1.4}
.or-brand-mark{display:grid;place-items:center;width:32px;height:36px;border:1px solid #4b7b87;border-radius:7px;color:#8ed3c3;font-size:22px;font-weight:500}
.or-brand small{display:block;font-size:7px;letter-spacing:1.15px;color:#a3b6c9;margin-top:5px}
.or-nav-group{margin:0 0 22px}.or-nav-group p{margin:0 12px 9px;color:#8ca6bd;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px}
.or-navigation a{display:flex;align-items:center;gap:11px;padding:9px 12px;margin:3px 0;color:#b9c9d8;border-radius:6px;text-decoration:none;font-size:11.5px;transition:background .15s,color .15s}
.or-nav-number{color:#7791a8;font-size:10px;font-variant-numeric:tabular-nums}
.or-navigation a:hover{background:#ffffff09;color:#fff}
.or-navigation a[aria-current=location]{background:#244557;color:#fff;box-shadow:inset 3px 0 #77cbb8}
.or-navigation a[aria-current=location] .or-nav-number{color:#8bd5c3}
.or-sidebar-footer{margin-top:auto;border-top:1px solid #ffffff16;padding:18px 12px 0;font-size:10px;color:#c1d1df}
.or-sidebar-footer small{display:block;color:#91a9bf;font-size:9px;margin-top:5px}.or-sidebar-footer a{display:block;margin-top:16px;color:#a9bfd1;text-decoration:none}
.or-status-dot{width:6px;height:6px;background:#7bc6b3;display:inline-block;border-radius:50%;margin-right:7px}
.or-workspace{margin-left:232px;min-width:0}
.or-topbar{position:sticky;top:0;z-index:45;display:flex;justify-content:space-between;align-items:center;gap:20px;min-height:91px;padding:18px 38px;background:var(--surf);color:var(--ink);border-bottom:1px solid var(--border)}
.or-topbar .or-breadcrumb{color:var(--muted);font-size:9px;letter-spacing:1.5px;font-weight:650;margin:0 0 3px}
.or-topbar h1{font-size:20px;letter-spacing:-.55px;font-weight:650;line-height:1.4;color:var(--ink)}
.or-topbar-actions{display:flex;align-items:center;gap:22px}.or-asof{font-size:10px;color:var(--muted);text-align:right}.or-asof b{display:block;font-size:12px;font-weight:600;color:var(--ink2);font-variant-numeric:tabular-nums}
.or-theme{display:grid;place-items:center;width:36px;height:36px;background:var(--plane);border:1px solid var(--border);border-radius:8px;color:var(--ink2);cursor:pointer}.or-theme svg{width:16px;height:16px}
.or-main{max-width:1440px;padding:34px 38px 80px;margin:0 auto;outline:none}
.or-main h2{font-family:inherit;font-size:24px;font-weight:650;line-height:1.35;letter-spacing:-.7px;border:0;margin:40px 0 10px;padding:0}
.or-main h3{font-size:16px;font-weight:650;letter-spacing:-.25px}.or-main .sub{font-size:13px;color:var(--ink2);line-height:1.75;margin-bottom:20px;max-width:1050px}
.or-main .card,.or-main .oc-card,.or-main .gc-card{background:var(--surf);border:1px solid var(--border);border-radius:12px;padding:24px;box-shadow:var(--shadow)}
.or-main .grid2,.or-main .oc-grid2{grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.or-main .grid2>div{min-width:0}
.or-main .tile,.or-main .oc-tile,.or-main .gc-kpi{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:20px 22px;box-shadow:var(--shadow);min-width:0}
.or-main .tlabel,.or-main .oc-tile .l,.or-main .gc-kpi>span{font-size:10px;font-weight:650;letter-spacing:.65px;text-transform:uppercase;color:var(--muted)}
.or-main .tval,.or-main .oc-tile .v,.or-main .gc-kpi strong{font-size:30px;line-height:1.3;letter-spacing:-1px;font-weight:650;margin:9px 0 4px;color:var(--ink);font-variant-numeric:tabular-nums}
.or-main .tsub,.or-main .oc-tile .s,.or-main .gc-kpi small{font-size:11px;color:var(--muted);line-height:1.6}
.or-main .callout{border:1px solid var(--border);border-left:3px solid var(--s1);padding:18px 22px;border-radius:8px;font-size:12px;line-height:1.85;background:var(--surf);color:var(--ink2)}
.or-main .callout.warn{border-left-color:var(--warn)}
.or-main table{font-size:12px}.or-main th{font-size:10px;letter-spacing:.3px;background:var(--plane);padding:12px 10px;color:var(--muted)}.or-main td{padding:11px 10px;border-bottom:1px solid var(--grid)}
.or-main .note{font-size:11px;line-height:1.85;overflow-wrap:anywhere}.or-main details{background:var(--surf);border:1px solid var(--border);border-radius:8px;margin-top:12px;padding:12px 16px;font-size:12px}.or-main summary{cursor:pointer;color:var(--ink2);font-weight:600}
.or-main .barrow{grid-template-columns:180px minmax(40px,1fr) 92px 82px;margin:9px 0;font-size:12px}.or-main .barrow2{grid-template-columns:140px minmax(30px,1fr) 110px;margin:9px 0;font-size:12px}
.or-main .legend{font-size:11px}.or-main .barfill,.or-main .bartrack{height:12px}
.or-main .oc{background:transparent;font-family:inherit;margin-bottom:42px}.or-main .oc-inner{max-width:none;margin:0;padding:0}
.or-main .oc .oc-headline{font-size:27px;line-height:1.35;font-weight:650;letter-spacing:-.85px;max-width:1000px;margin:9px 0 12px}
.or-main .oc-kicker,.or-main .gc-eyebrow,.or-cover-kicker{font-size:9px;letter-spacing:1.5px;text-transform:uppercase;font-weight:750;color:var(--accent);margin:0 0 9px}
.or-main .oc-sub{font-size:12px;line-height:1.85;max-width:1100px}.or-main .oc-tiles{grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:24px 0 20px}
.or-main .oc-card h3{font-family:inherit;font-size:14px;margin:0 0 8px}.or-main .oc-h3sub{font-size:10.5px;line-height:1.7;min-height:54px}.or-main .oc-legend{font-size:10px;line-height:1.65;gap:8px 14px}
.or-main .oc-credit{font-size:10px;margin-top:16px;color:var(--muted);overflow-wrap:anywhere}.or-main .oc-note-p{font-size:11px;line-height:1.9}.or-main .oc details .oc-note-p{margin:10px 0}
.or-main .or-cover{background:var(--surf);color:var(--ink);color-scheme:inherit;border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);margin:0 0 48px;font-family:inherit}
.or-main .or-cover-inner{max-width:none;margin:0;padding:28px}
.or-main .or-cover .or-cover-title{font-family:inherit;color:var(--ink);font-size:24px;font-weight:650;line-height:1.4;letter-spacing:-.7px;gap:12px}.or-main .or-cover-title svg{width:21px;height:21px;color:var(--accent)}
.or-main .or-cover .or-cover-subtitle{font-family:inherit;font-size:12px;line-height:1.8;color:var(--ink2);margin-top:6px}
.or-main .or-cover-toolbar{margin:23px 0 16px;height:auto;display:flex;align-items:center;justify-content:space-between;gap:16px}.or-cover-unit{font-size:10px;letter-spacing:.4px;color:var(--muted)}
.or-main .or-cover-switch{background:var(--plane);border-color:var(--border);padding:3px;border-radius:7px}.or-main .or-cover .or-cover-switch button{font-size:11px;line-height:22px;font-family:inherit;padding:3px 14px;color:var(--muted);border-radius:4px}
.or-main .or-cover .or-cover-switch button[aria-pressed=true]{background:var(--surf);color:var(--accent);box-shadow:0 1px 4px #00000010;font-weight:700}
.or-main .or-cover-plot text{font-family:inherit;font-size:10px;fill:var(--muted)}.or-cover-grid{stroke:var(--grid);stroke-width:1;stroke-dasharray:3 5}
.or-main .or-cover-tooltip{background:var(--surf);color:var(--ink);border-color:var(--border);font-family:inherit;box-shadow:0 10px 30px #10223820}.or-main .or-cover-tooltip small{color:var(--muted)}.or-main .or-cover-tooltip-total{border-color:var(--border)}
.or-cover-legend{border-top:1px solid var(--grid);padding:18px 0 16px;margin-top:0}.or-cover-legend>p{font-size:10px;color:var(--muted);margin:0 0 10px}.or-cover-legend-items{display:flex;flex-wrap:wrap;gap:9px 18px}.or-cover-legend-items span{display:inline-flex;align-items:center;gap:6px;font-size:10px;color:var(--ink2)}.or-cover-legend-items i{width:8px;height:8px;border-radius:2px;flex:none}
.or-main .or-cover .or-cover-credit{font-size:10px;line-height:1.8;font-family:inherit;color:var(--muted);margin:0;border-top:1px solid var(--grid);padding-top:14px}
.or-main .gateway-charts{--gc-bg:var(--surf);--gc-ink:var(--ink);--gc-muted:var(--ink2);--gc-border:var(--border);font-family:inherit;margin:0 0 42px}
.or-main .gateway-charts h2{font-size:25px;margin:0 0 10px}.or-main .gc-intro{font-size:12px;line-height:1.8}.or-main .gc-kpis{gap:14px}.or-main .gc-card h3{font-family:inherit;font-size:15px;margin-bottom:10px}
.or-main .gc-sub{font-size:11px;line-height:1.8;min-height:40px}.or-main .gc-nav{gap:8px;margin:18px 0 24px}.or-main .gc-nav a{border:1px solid var(--border);border-radius:6px;padding:6px 12px;background:var(--surf);font-size:10px;text-decoration:none;color:var(--ink2)}.or-main .gc-nav a:hover{color:var(--accent);border-color:var(--accent)}
.or-main .gc-note,.or-main .gc-source{font-size:10px;line-height:1.85}.or-main .gc-method{border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:8px;font-size:11px;line-height:1.85}.or-main .gc-eyebrow{margin-top:0}
.or-main .gpu-monitor{--gp-bg:var(--plane);--gp-card:var(--surf);--gp-line:var(--border);--gp-ink:var(--ink);--gp-muted:var(--ink2);background:transparent;padding:0;margin-top:48px;font-family:inherit;font-size:13px}
.or-main .gpu-monitor .gp-kicker{color:var(--accent);font-size:10px}.or-main .gpu-monitor h2{font-size:25px}.or-main .gpu-monitor h3{font-size:16px}.or-main .gpu-monitor .gp-muted{font-size:12px;line-height:1.8}.or-main .gpu-monitor .gp-unit{color:var(--accent);font-size:11px}.or-main .gpu-monitor a,.or-main .gpu-monitor summary{color:var(--s1)}
.or-main .gpu-monitor select,.or-main .gpu-monitor button{background:var(--surf);color:var(--ink);border-color:var(--border);font-size:12px}.or-main .gpu-monitor .gp-fall{color:var(--good)}.or-main .gpu-monitor .gp-rise{color:var(--warn)}.or-main .gpu-monitor tbody tr:hover{background:var(--plane)}
.or-main .gpu-monitor .gp-panel,.or-main .gpu-monitor .gp-card{border-radius:12px;padding:24px}.or-main .gpu-monitor th,.or-main .gpu-monitor td{font-size:12px}
.or-main .gpu-monitor svg text{fill:var(--muted)}.or-main .gpu-monitor svg [stroke="#2b3c52"]{stroke:var(--grid)}.or-main .gpu-monitor .gp-sd{color:var(--s1)}.or-main .gpu-monitor .gp-sa{color:var(--s2)}
.or-main .gpu-monitor .gp-header h2{margin:0}
.or-main .gc-warning,.or-main .gpu-monitor .gp-warning{background:color-mix(in srgb,var(--warn) 10%,var(--surf));color:var(--warn);border:1px solid color-mix(in srgb,var(--warn) 24%,var(--surf));border-left:3px solid var(--warn);border-radius:7px;padding:12px 16px;font-size:11px;line-height:1.7}
.or-main #weekly{margin-top:48px;border-top:1px solid var(--border);padding-top:16px;font-size:13px}
.or-skip{position:fixed;left:250px;top:-100px;z-index:100;background:var(--surf);padding:12px 18px;border-radius:6px}.or-skip:focus{top:12px}
@media(min-width:1021px) and (max-width:1300px){.or-sidebar{width:204px;padding-left:10px;padding-right:10px}.or-workspace{margin-left:204px}.or-main{padding:28px 24px 70px}.or-topbar{padding-left:24px;padding-right:24px}.or-main .oc-grid2,.or-main .gc-grid,.or-main .grid2{grid-template-columns:1fr}.or-main .oc-h3sub{min-height:0}.or-main .oc-tile,.or-main .gc-kpi{padding:16px}.or-main .oc-tile .v{font-size:26px}}
@media(max-width:1020px){.or-sidebar{position:sticky;top:0;inset:auto;top:0;width:auto;height:52px;padding:0 18px;display:block;overflow:auto;border-bottom:1px solid #ffffff12}.or-brand,.or-sidebar .or-brand,.or-sidebar-footer,.or-nav-group p,.or-nav-number{display:none}.or-navigation{display:flex;width:max-content;gap:6px;height:100%;align-items:center}.or-nav-group{display:contents}.or-navigation a{padding:8px 12px;font-size:11px;white-space:nowrap}.or-navigation a[aria-current=location]{box-shadow:inset 0 -2px #77cbb8}.or-workspace{margin-left:0}.or-topbar{position:relative;padding:20px 24px}.or-main{padding:26px 24px 64px}.or-main [id]{scroll-margin-top:76px}.or-main .oc-grid2,.or-main .gc-grid,.or-main .grid2{grid-template-columns:1fr}.or-main .oc-h3sub{min-height:0}.or-main .gc-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.or-skip{left:16px}}
@media(max-width:600px){.or-topbar{padding:16px;min-height:82px;gap:12px}.or-topbar h1{font-size:18px}.or-topbar .or-breadcrumb{font-size:7px;letter-spacing:1px}.or-topbar-actions{gap:10px}.or-asof{font-size:8px}.or-asof b{font-size:10px}.or-theme{width:30px;height:30px}.or-main{padding:24px 14px 50px}.or-main .oc h1{font-size:23px;letter-spacing:-.6px}.or-main .oc-sub{font-size:11px}.or-main .oc-tiles{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.or-main .oc-tile,.or-main .gc-kpi{padding:15px}.or-main .oc-tile .v,.or-main .gc-kpi strong{font-size:25px}.or-main .oc-tile .l{font-size:8px;letter-spacing:.3px}.or-main .card,.or-main .oc-card,.or-main .gc-card{padding:17px}.or-main .or-cover-inner{padding:20px 16px}.or-main .or-cover .or-cover-title{font-size:22px}.or-main .or-cover-unit{font-size:8px;max-width:165px}.or-main .or-cover-toolbar{gap:8px}.or-main .or-cover .or-cover-switch button{padding:3px 10px}.or-main .or-cover-plot{height:285px}.or-main .or-cover-legend-items{gap:8px 12px}.or-cover-legend-items span{font-size:9px}.or-main h2{font-size:22px}.or-main .barrow{grid-template-columns:110px minmax(30px,1fr) 66px;font-size:10px;gap:6px}.or-main .barmom{display:none}.or-main .barrow2{grid-template-columns:100px minmax(25px,1fr) 74px!important;font-size:10px;gap:6px}.or-main .gpu-monitor .gp-header{flex-wrap:wrap}.or-main .gpu-monitor .gp-panel,.or-main .gpu-monitor .gp-card{padding:16px}.or-main .gpu-monitor select{max-width:100%}.or-main .gpu-monitor .gp-controls label{max-width:100%;min-width:0}.or-main .gpu-monitor .gp-grid{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){.or-dashboard *{scroll-behavior:auto!important;transition:none!important}}
@media(max-width:1020px){.or-sidebar{scrollbar-width:none}.or-sidebar::-webkit-scrollbar{display:none}}
@media(max-width:600px){.or-main .oc .oc-headline{font-size:23px;letter-spacing:-.6px}}
@media print{.or-sidebar,.or-topbar-actions,.or-skip{display:none}.or-workspace{margin:0}.or-topbar{position:static;padding:0 0 20px}.or-main{padding:20px 0;max-width:none}.or-main .card,.or-main .oc-card,.or-main .gc-card,.or-main .or-cover{break-inside:avoid;box-shadow:none}.or-main .oc-grid2{grid-template-columns:1fr}}
"""


JS = r"""
(()=>{
 const links=[...document.querySelectorAll('.or-navigation a')];
 const sections=links.map(a=>({a,el:document.getElementById(a.hash.slice(1))})).filter(x=>x.el);
 const activate=a=>links.forEach(link=>{if(link===a)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});
 let queued=false;
 function current(){
  queued=false;
  const cutoff=window.innerWidth>1020?135:95;
  const ordered=sections.map(x=>({...x,top:x.el.getBoundingClientRect().top})).sort((a,b)=>a.top-b.top);
  const passed=ordered.filter(x=>x.top<=cutoff);
  if(ordered.length)activate((passed.at(-1)||ordered[0]).a);
 }
 function schedule(){if(!queued){queued=true;requestAnimationFrame(current);}}
 window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);
 window.addEventListener('hashchange',schedule);links.forEach(a=>a.addEventListener('click',()=>activate(a)));
 const theme=document.querySelector('.or-theme');
 if(theme)theme.addEventListener('click',()=>{
  const dark=document.documentElement.dataset.theme!=='dark';
  document.documentElement.dataset.theme=dark?'dark':'light';
  theme.setAttribute('aria-pressed',String(dark));theme.setAttribute('aria-label',dark?'Switch to light theme':'Switch to dark theme');
 });
 current();
})();
"""
