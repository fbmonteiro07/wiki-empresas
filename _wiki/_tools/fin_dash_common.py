"""Shared presentation layer for the Financials theme dashboards (fin-*.html). No data transforms.

Reuses the OpenRouter presentation shell (sidebar, topbar, Jakarta face, light/dark toggle) so the
Financials pages look like the rest of the hub, and adds a small dependency-free SVG chart kit:
line (crosshair tooltip), bars (per-bar tooltip, signed colouring), scatter and a heat-table helper.

Chart colours are the dataviz reference categorical slots, validated 2026-11-02 against the shell
surfaces (light #ffffff: CVD dE 9.1, normal 22.9, contrast WARN for slots 3-4 -> every chart prints
values or ships a table; dark #182636: all checks pass). Signed values use the blue<->red diverging pair.
"""
from __future__ import annotations

import base64
import json
from html import escape
from pathlib import Path

from openrouter_presentation import CSS as SHELL_CSS, JS as SHELL_JS

FONT = Path(__file__).resolve().parents[1] / "_data" / "openrouter" / "assets" / "plus-jakarta-sans.woff2"


def font_face() -> str:
    """Same embedded face as the hub (build_dashboards_hub.font_face)."""
    if not FONT.exists():
        return ""
    b64 = base64.b64encode(FONT.read_bytes()).decode()
    return ('@font-face{font-family:"OR Jakarta";font-weight:200 800;font-style:normal;font-display:swap;'
            f'src:url(data:font/woff2;base64,{b64}) format("woff2")}}')

FIN_CSS = r"""
:root,:root[data-theme=light]{--fs1:#2a78d6;--fs2:#eb6834;--fs3:#1baf7a;--fs4:#eda100;--fs5:#e87ba4;--fpos:#2a78d6;--fneg:#e34948;--fmid:#f0efec}
:root[data-theme=dark]{--fs1:#3987e5;--fs2:#d95926;--fs3:#199e70;--fs4:#c98500;--fs5:#d55181;--fpos:#3987e5;--fneg:#e66767;--fmid:#383835}
.fd-tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:20px 0 8px}
.fd-tile{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:18px 20px;min-width:0}
.fd-tile .l{font-size:10px;font-weight:650;letter-spacing:.65px;text-transform:uppercase;color:var(--muted)}
.fd-tile .v{font-size:27px;line-height:1.3;letter-spacing:-.8px;font-weight:650;margin:8px 0 2px;font-variant-numeric:tabular-nums}
.fd-tile .s{font-size:11px;color:var(--muted);line-height:1.6}
.fd-grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin:16px 0}
.fd-card{background:var(--surf);border:1px solid var(--border);border-radius:12px;padding:22px 24px;box-shadow:var(--shadow);min-width:0;margin:16px 0}
.fd-grid2 .fd-card{margin:0}
.fd-card h3{margin:0 0 4px}.fd-card .fd-sub{font-size:11px;color:var(--ink2);line-height:1.7;margin:0 0 12px}
.fd-legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:11px;color:var(--ink2);margin:4px 0 8px}
.fd-legend span{display:inline-flex;align-items:center;gap:6px}.fd-legend i{width:14px;height:3px;border-radius:2px;display:inline-block}
.fd-legend i.dot{width:8px;height:8px;border-radius:50%}
.fd-chart{position:relative;width:100%}.fd-chart svg{display:block;width:100%;overflow:visible}
.fd-chart text{font-family:inherit;font-size:10px;fill:var(--muted);font-variant-numeric:tabular-nums}
.fd-chart .gl{stroke:var(--grid);stroke-width:1}.fd-chart .zl{stroke:var(--base);stroke-width:1}
.fd-chart .xh{stroke:var(--base);stroke-width:1;stroke-dasharray:3 3}
.fd-tip{position:fixed;z-index:90;pointer-events:none;background:var(--surf);color:var(--ink);border:1px solid var(--border);border-radius:8px;padding:9px 12px;font-size:11px;line-height:1.6;box-shadow:0 10px 30px #10223822;max-width:300px;display:none}
.fd-tip b{font-weight:650}.fd-tip .r{display:flex;justify-content:space-between;gap:14px}.fd-tip .r span:last-child{font-variant-numeric:tabular-nums}
.fd-tip i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px}
.fd-src{font-size:10px;color:var(--muted);line-height:1.75;margin:10px 0 0;overflow-wrap:anywhere}
.fd-scroll{overflow-x:auto;max-width:100%}
table.fd-t{border-collapse:collapse;width:100%;font-size:11.5px;font-variant-numeric:tabular-nums}
table.fd-t th{font-size:10px;text-align:right;color:var(--muted);background:var(--plane);padding:8px 8px;white-space:nowrap;font-weight:650}
table.fd-t th:first-child,table.fd-t td:first-child{text-align:left;position:sticky;left:0;background:var(--surf);z-index:1}
table.fd-t th:first-child{background:var(--plane)}
table.fd-t td{text-align:right;padding:6px 8px;border-bottom:1px solid var(--grid);white-space:nowrap}
table.fd-t td.nd{color:var(--muted)}table.fd-t td.txt{text-align:left;white-space:normal;min-width:180px}
table.fd-t tr.grp td{font-weight:650;background:var(--plane)}
.fd-calc{color:var(--muted);font-size:9px;vertical-align:super}
.fd-flag{display:inline-block;font-size:9px;font-weight:700;letter-spacing:.4px;padding:1px 6px;border-radius:4px;border:1px solid var(--border);color:var(--ink2);margin-left:6px;vertical-align:1px}
.fd-callout{border:1px solid var(--border);border-left:3px solid var(--accent);padding:14px 18px;border-radius:8px;font-size:12px;line-height:1.8;background:var(--surf);color:var(--ink2);margin:14px 0}
.fd-callout.warn{border-left-color:var(--warn)}
.fd-main-q{font-size:13px;color:var(--ink2);line-height:1.8;max-width:1100px}
details.fd-tv{margin-top:10px;border:0;padding:0;background:transparent}details.fd-tv summary{font-size:11px;color:var(--s1);font-weight:600}
.fd-chips{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 12px}
.fd-chips button{font-size:11px;padding:4px 12px;border-radius:6px;border:1px solid var(--border);background:var(--surf);color:var(--ink2);cursor:pointer}
.fd-chips button[aria-pressed=true]{border-color:var(--accent);color:var(--accent);font-weight:650}
.fd-lane text{font-family:inherit;font-size:10px;fill:var(--muted)}.fd-lane .ln{font-size:11px;fill:var(--ink2);font-weight:650}
table.fd-t td details{margin:4px 0 0;border:0;padding:0;background:transparent;font-size:10.5px}table.fd-t td details summary{font-size:10.5px}
table.fd-t td.txt small{color:var(--muted)}
table.fd-reg th{text-align:left}table.fd-reg td{vertical-align:top}table.fd-reg td.txt{min-width:130px;max-width:230px}table.fd-reg td.txt.wide{min-width:280px;max-width:420px}table.fd-reg th:first-child,table.fd-reg td:first-child{position:static}
.fd-stage{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:-1px}
:root,:root[data-theme=light]{--st1:#86b6ef;--st2:#5598e7;--st3:#2a78d6;--st4:#1c5cab;--st5:#104281}
:root[data-theme=dark]{--st1:#256abf;--st2:#3987e5;--st3:#6da7ec;--st4:#9ec5f4;--st5:#cde2fb}
@media(max-width:1300px){.fd-grid2{grid-template-columns:1fr}}
@media(max-width:1020px){.fd-tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){.fd-tile .v{font-size:22px}.fd-card{padding:16px}}
"""

CHART_JS = r"""
const FD=(()=>{
 const NS='http://www.w3.org/2000/svg';
 const tip=document.createElement('div');tip.className='fd-tip';document.body.appendChild(tip);
 const showTip=(e,html)=>{tip.innerHTML=html;tip.style.display='block';const w=tip.offsetWidth,h=tip.offsetHeight;
   let x=e.clientX+14,y=e.clientY+14;if(x+w>innerWidth-8)x=e.clientX-w-14;if(y+h>innerHeight-8)y=e.clientY-h-14;tip.style.left=x+'px';tip.style.top=y+'px';};
 const hideTip=()=>{tip.style.display='none';};
 const el=(n,a,p)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;};
 const nice=(lo,hi,n=5)=>{if(lo===hi){lo-=1;hi+=1;}const span=hi-lo,step0=span/n,mag=Math.pow(10,Math.floor(Math.log10(step0)));
   const step=[1,2,2.5,5,10].map(m=>m*mag).find(s=>s>=step0);const a=Math.floor(lo/step)*step,b=Math.ceil(hi/step)*step;const t=[];for(let v=a;v<=b+step/2;v+=step)t.push(+v.toFixed(10));return t;};
 const fmt=(v,f)=>v==null||isNaN(v)?'n.d.':(f?f(v):v.toLocaleString(undefined,{maximumFractionDigits:1}));
 function frame(host,opt){host.innerHTML='';const W=host.clientWidth||640,H=opt.height||260,m={l:opt.ml||46,r:opt.mr||14,t:12,b:opt.mb||34};
   const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,height:H,role:'img','aria-label':opt.label||''},host);return {svg,W,H,m,iw:W-m.l-m.r,ih:H-m.t-m.b};}
 function yaxis(f,ticks,y,yf){ticks.forEach(t=>{el('line',{x1:f.m.l,x2:f.W-f.m.r,y1:y(t),y2:y(t),class:t===0?'zl':'gl'},f.svg);
   const tx=el('text',{x:f.m.l-6,y:y(t)+3,'text-anchor':'end'},f.svg);tx.textContent=yf?yf(t):t;});}
 function xlabels(f,xs,x,every){const L=xs.length-1;xs.forEach((s,i)=>{if(i!==L&&(i%every||L-i<every*0.7))return;const tx=el('text',{x:x(i),y:f.H-f.m.b+15,'text-anchor':'middle'},f.svg);tx.textContent=s;});}
 // line chart: opt.xs labels, opt.series [{name,color,vals:[...]}]
 function line(host,opt){const f=frame(host,opt);const all=opt.series.flatMap(s=>s.vals).filter(v=>v!=null);
   let lo=Math.min(...all,opt.zero?0:Infinity),hi=Math.max(...all,opt.zero?0:-Infinity);const ticks=nice(lo,hi);lo=ticks[0];hi=ticks.at(-1);
   const n=opt.xs.length,x=i=>f.m.l+(n<2?f.iw/2:i*f.iw/(n-1)),y=v=>f.m.t+f.ih-(v-lo)/(hi-lo)*f.ih;
   yaxis(f,ticks,y,opt.yf);xlabels(f,opt.xs,x,Math.max(1,Math.ceil(n/(f.iw/62))));
   opt.series.forEach(s=>{let d='',pen=false;s.vals.forEach((v,i)=>{if(v==null){pen=false;return;}d+=(pen?'L':'M')+x(i).toFixed(1)+','+y(v).toFixed(1);pen=true;});
     el('path',{d,fill:'none',style:`stroke:var(${s.color})`,'stroke-width':2,'stroke-linejoin':'round','stroke-dasharray':s.dash||''},f.svg);
     s.vals.forEach((v,i)=>{if(v!=null&&(s.vals[i-1]==null)&&(s.vals[i+1]==null))el('circle',{cx:x(i),cy:y(v),r:3,style:`fill:var(${s.color})`},f.svg);});
     const li=s.vals.map((v,i)=>v!=null?i:-1).filter(i=>i>=0).at(-1);
     if(opt.endLabels&&li!=null){const tx=el('text',{x:x(li)+5,y:y(s.vals[li])+3,style:'fill:var(--ink2)'},f.svg);tx.textContent=s.short||s.name;}});
   const xh=el('line',{class:'xh',y1:f.m.t,y2:f.m.t+f.ih,visibility:'hidden'},f.svg);
   const hit=el('rect',{x:f.m.l,y:f.m.t,width:f.iw,height:f.ih,fill:'transparent'},f.svg);
   hit.addEventListener('mousemove',e=>{const r=f.svg.getBoundingClientRect(),px=(e.clientX-r.left)*f.W/r.width;
     const i=Math.max(0,Math.min(n-1,Math.round((px-f.m.l)/(f.iw/Math.max(1,n-1)))));xh.setAttribute('x1',x(i));xh.setAttribute('x2',x(i));xh.setAttribute('visibility','visible');
     showTip(e,`<b>${opt.xs[i]}</b>`+opt.series.map(s=>`<div class="r"><span><i style="background:var(${s.color})"></i>${s.name}</span><span>${fmt(s.vals[i],opt.tf||opt.yf)}${(s.notes&&s.notes[i])?' '+s.notes[i]:''}</span></div>`).join(''));});
   hit.addEventListener('mouseleave',()=>{xh.setAttribute('visibility','hidden');hideTip();});}
 // bars: opt.xs, opt.vals, opt.color (css var) or signed:true, opt.notes per bar
 function bars(host,opt){const f=frame(host,opt);const vs=opt.vals.filter(v=>v!=null);let lo=Math.min(0,...vs),hi=Math.max(0,...vs);
   const ticks=nice(lo,hi);lo=ticks[0];hi=ticks.at(-1);const n=opt.xs.length,bw=f.iw/n,x=i=>f.m.l+i*bw+bw/2,y=v=>f.m.t+f.ih-(v-lo)/(hi-lo)*f.ih;
   yaxis(f,ticks,y,opt.yf);xlabels(f,opt.xs,x,Math.max(1,Math.ceil(n/(f.iw/62))));
   opt.vals.forEach((v,i)=>{const w=Math.max(2,bw-2);let g;
     if(v==null){g=el('rect',{x:x(i)-w/2,y:y(0)-1,width:w,height:2,style:'fill:var(--base)'},f.svg);}
     else{const y0=y(0),y1=y(v),c=opt.signed?(v<0?'--fneg':'--fpos'):(opt.color||'--fs1');const top=Math.min(y0,y1),h=Math.max(1,Math.abs(y1-y0)),rr=Math.min(4,w/2,h);
       g=el('path',{d:v>=0?`M${x(i)-w/2},${y0}V${top+rr}Q${x(i)-w/2},${top} ${x(i)-w/2+rr},${top}H${x(i)+w/2-rr}Q${x(i)+w/2},${top} ${x(i)+w/2},${top+rr}V${y0}Z`
         :`M${x(i)-w/2},${y0}V${top+h-rr}Q${x(i)-w/2},${top+h} ${x(i)-w/2+rr},${top+h}H${x(i)+w/2-rr}Q${x(i)+w/2},${top+h} ${x(i)+w/2},${top+h-rr}V${y0}Z`,style:`fill:var(${c})`},f.svg);}
     const hb=el('rect',{x:x(i)-bw/2,y:f.m.t,width:bw,height:f.ih,fill:'transparent'},f.svg);
     hb.addEventListener('mousemove',e=>showTip(e,`<b>${opt.xs[i]}</b><div class="r"><span>${opt.name||''}</span><span>${fmt(v,opt.tf||opt.yf)}</span></div>${opt.notes&&opt.notes[i]?'<div>'+opt.notes[i]+'</div>':''}`));
     hb.addEventListener('mouseleave',hideTip);});}
 // scatter: opt.groups [{name,color,pts:[{x,y,label}]}]
 function scatter(host,opt){const f=frame(host,{...opt,mb:40});const P=opt.groups.flatMap(g=>g.pts);
   const xt=nice(Math.min(...P.map(p=>p.x),0),Math.max(...P.map(p=>p.x),0)),yt=nice(Math.min(...P.map(p=>p.y),0),Math.max(...P.map(p=>p.y),0));
   const x=v=>f.m.l+(v-xt[0])/(xt.at(-1)-xt[0])*f.iw,y=v=>f.m.t+f.ih-(v-yt[0])/(yt.at(-1)-yt[0])*f.ih;yaxis(f,yt,y,opt.yf);
   xt.forEach(t=>{el('line',{x1:x(t),x2:x(t),y1:f.m.t,y2:f.m.t+f.ih,class:t===0?'zl':'gl'},f.svg);const tx=el('text',{x:x(t),y:f.H-f.m.b+15,'text-anchor':'middle'},f.svg);tx.textContent=opt.xf?opt.xf(t):t;});
   const xl=el('text',{x:f.m.l+f.iw/2,y:f.H-4,'text-anchor':'middle',style:'fill:var(--ink2)'},f.svg);xl.textContent=opt.xlabel||'';
   opt.groups.forEach(g=>g.pts.forEach(p=>{const c=el('circle',{cx:x(p.x),cy:y(p.y),r:5,style:`fill:var(${g.color});stroke:var(--surf);stroke-width:2`},f.svg);
     const hb=el('circle',{cx:x(p.x),cy:y(p.y),r:11,fill:'transparent'},f.svg);
     hb.addEventListener('mousemove',e=>showTip(e,`<b>${p.label}</b><div class="r"><span>${opt.xname}</span><span>${fmt(p.x,opt.xf)}</span></div><div class="r"><span>${opt.yname}</span><span>${fmt(p.y,opt.yf)}</span></div>`));
     hb.addEventListener('mouseleave',hideTip);}));}
 // server-rendered marks (swimlanes, bar lists) carry their tooltip in data-tip
 document.addEventListener('mousemove',e=>{const t=e.target.closest&&e.target.closest('[data-tip]');if(t)showTip(e,t.getAttribute('data-tip'));});
 document.addEventListener('mouseout',e=>{const t=e.target.closest&&e.target.closest('[data-tip]');if(t&&!t.contains(e.relatedTarget))hideTip();});
 // filter chips: <button data-filter="X" data-target="tableId">; rows carry data-tags="X Y"
 document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('button[data-filter]');if(!b)return;const tg=document.getElementById(b.dataset.target);
   b.parentElement.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
   tg.querySelectorAll('tbody tr[data-tags]').forEach(r=>{r.hidden=!(b.dataset.filter==='all'||r.dataset.tags.split(' ').includes(b.dataset.filter));});});
 const registry=[];
 function mount(id,kind,opt){const host=document.getElementById(id);if(!host)return;const draw=()=>({line,bars,scatter})[kind](host,opt);registry.push(draw);draw();}
 let t;addEventListener('resize',()=>{clearTimeout(t);t=setTimeout(()=>registry.forEach(d=>d()),120);});
 return {mount,pct:v=>(v>0?'+':'')+v.toFixed(Math.abs(v)<10?1:0)+'%'};
})();
"""


def shell(title: str, breadcrumb: str, asof_label: str, asof: str, groups, footer: tuple[str, str]) -> str:
    links, i = [], 0
    for label, items in groups:
        links.append('<div class="or-nav-group"><p>' + escape(label) + '</p>')
        for anchor, name in items:
            i += 1
            links.append(f'<a href="#{anchor}"><span class="or-nav-number" aria-hidden="true">{i:02d}</span>{escape(name)}</a>')
        links.append('</div>')
    return (
        '<div class="or-dashboard"><a class="or-skip" href="#dashboard-main">Skip to dashboard</a>'
        '<aside class="or-sidebar"><a class="or-brand" href="index.html" aria-label="Capstone research dashboards">'
        '<span class="or-brand-mark" aria-hidden="true">C</span><span>CAPSTONE<small>RESEARCH INTELLIGENCE</small></span></a>'
        '<nav class="or-navigation" aria-label="Dashboard sections">' + ''.join(links) + '</nav>'
        f'<div class="or-sidebar-footer"><span class="or-status-dot"></span>{escape(footer[0])}<small>{escape(footer[1])}</small>'
        '<a href="../index.html#TH-financials">Financials theme page <span aria-hidden="true">↗</span></a>'
        '<a href="index.html">All dashboards <span aria-hidden="true">↗</span></a></div></aside>'
        f'<div class="or-workspace"><header class="or-topbar"><div><p class="or-breadcrumb">{escape(breadcrumb)}</p>'
        f'<h1>{escape(title)}</h1></div><div class="or-topbar-actions">'
        f'<span class="or-asof">{escape(asof_label)} <b>{escape(asof)}</b></span>'
        '<button type="button" class="or-theme" aria-label="Switch to dark theme" aria-pressed="false">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20.5 13A8.5 8.5 0 0 1 11 3.5 8.5 8.5 0 1 0 20.5 13Z"/></svg></button>'
        '</div></header><main id="dashboard-main" class="or-main" tabindex="-1">'
    )


def page(title: str, description: str, body: str, mounts: list[tuple[str, str, dict]]) -> str:
    """Full HTML document. mounts = [(element id, 'line'|'bars'|'scatter', options)]."""
    js_mounts = "\n".join(f"FD.mount({json.dumps(i)},{json.dumps(k)},{json.dumps(o, ensure_ascii=False)});"
                          for i, k, o in mounts)
    # option objects may carry formatter names; resolve them client-side
    js_mounts = (js_mounts.replace('"yf": "pct"', '"yf": FD.pct').replace('"tf": "pct"', '"tf": FD.pct')
                 .replace('"xf": "pct"', '"xf": FD.pct'))
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{escape(title)}</title><meta name="description" content="{escape(description)}">'
        '<style>' + font_face() + '*{box-sizing:border-box}body{margin:0}'
        + SHELL_CSS + FIN_CSS + '</style></head><body>' + body +
        '</main></div></div><script>' + SHELL_JS + CHART_JS + js_mounts + '</script></body></html>'
    )


def fmt_num(v, d=1, suffix="") -> str:
    if v is None:
        return "n.d."
    return f"{v:,.{d}f}{suffix}"


def fmt_pct(v, d=0, calc=False) -> str:
    if v is None:
        return "n.d."
    s = f"{v:+.{d}f}%"
    return s + ('<span class="fd-calc" title="Capstone arithmetic from the prior-year release">c</span>' if calc else "")


def heat_style(v, cap=60.0) -> str:
    """Diverging cell wash (blue up / red down), text stays in ink."""
    if v is None:
        return ""
    a = min(abs(v) / cap, 1.0) * 42
    var = "--fpos" if v >= 0 else "--fneg"
    return f' style="background:color-mix(in srgb,var({var}) {a:.0f}%,var(--surf))"'


def legend(items: list[tuple[str, str]], dot: bool = False) -> str:
    cls = ' class="dot"' if dot else ""
    return '<div class="fd-legend">' + "".join(
        f'<span><i{cls} style="background:var({c})"></i>{escape(n)}</span>' for n, c in items) + "</div>"


def table(headers: list[str], rows: list[list[str]], cls: str = "fd-t") -> str:
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>" + "".join(c if c.startswith("<td") else f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="fd-scroll"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
