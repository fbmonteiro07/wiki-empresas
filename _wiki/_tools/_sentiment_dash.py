# -*- coding: utf-8 -*-
"""HTML renderer for the bull/bear × hot/cold sentiment dashboard (called by build_sentiment.py --step dash).
Self-contained, theme-aware (light default, dark via prefers-color-scheme or data-theme), no external assets.
Palette: dataviz reference instance — categorical blue #2a78d6 / orange #eb6834, diverging blue<->red, neutral gray midpoint.
Two tracks: own tweet corpus (May-2026→) and Bloomberg social/news history (Jan-2024→, the backward track)."""
import json, datetime as dt

CSS = """
:root{color-scheme:light;--bg:#fcfcfb;--surf:#ffffff;--line:#e6e4df;--ink:#0b0b0b;--ink2:#52514e;--ink3:#8a887f;--grid:#eeece7;
 --blue:#2a78d6;--orange:#eb6834;--red:#e34948;--aqua:#1baf7a;--mid:#f0efec;--blue-soft:#cde2fb;--red-soft:#fbd6d5;--orange-soft:#fde0d3;--chip:#f3f2ee}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#141413;--surf:#1a1a19;--line:#33322f;--ink:#fff;--ink2:#c3c2b7;--ink3:#8f8e86;--grid:#262623;
 --blue:#3987e5;--orange:#d95926;--red:#e66767;--aqua:#199e70;--mid:#383835;--blue-soft:#1c3c66;--red-soft:#5a2626;--orange-soft:#5a3320;--chip:#232321}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#141413;--surf:#1a1a19;--line:#33322f;--ink:#fff;--ink2:#c3c2b7;--ink3:#8f8e86;--grid:#262623;
 --blue:#3987e5;--orange:#d95926;--red:#e66767;--aqua:#199e70;--mid:#383835;--blue-soft:#1c3c66;--red-soft:#5a2626;--orange-soft:#5a3320;--chip:#232321}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{padding:22px 28px 10px;border-bottom:1px solid var(--line)}h1{margin:0 0 4px;font-size:22px}h2{font-size:16px;margin:0 0 10px}h3{font-size:13.5px;margin:14px 0 6px;color:var(--ink2)}
.sub{color:var(--ink2);font-size:13px}.wrap{padding:16px 28px 40px;max-width:1500px}
.kpis{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0 6px}.kpi{background:var(--surf);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:150px}
.kpi b{display:block;font-size:20px;font-weight:600}.kpi span{color:var(--ink2);font-size:12px}
section{background:var(--surf);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:16px 0}
.row{display:flex;gap:16px;flex-wrap:wrap}.col{flex:1 1 420px;min-width:0}
table{border-collapse:collapse;width:100%;font-size:12.5px}th,td{padding:5px 8px;border-bottom:1px solid var(--grid);text-align:right;white-space:nowrap}
th{color:var(--ink2);font-weight:600;cursor:pointer;user-select:none;position:sticky;top:0;background:var(--surf)}th:first-child,td:first-child,th.l,td.l{text-align:left}
tr:hover td{background:var(--chip)}.tk{font-weight:600}.nm{color:var(--ink3);font-size:11px;font-weight:400;margin-left:6px}
.barwrap{display:inline-block;width:96px;height:12px;position:relative;vertical-align:middle}
.barwrap i{position:absolute;left:50%;top:0;width:1px;height:12px;background:var(--ink3);opacity:.5}
.barwrap b{position:absolute;top:1px;height:10px;border-radius:3px}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11px;font-weight:600;background:var(--chip);color:var(--ink2)}
.tag.hb{background:var(--orange-soft)}.tag.cb{background:var(--blue-soft)}.tag.hr{background:var(--red-soft)}
.scroll{overflow:auto;max-height:640px;border:1px solid var(--grid);border-radius:6px}.scroll[style*="max-height:none"] th{position:static}
svg{display:block;max-width:100%}.tip{position:fixed;pointer-events:none;background:var(--surf);border:1px solid var(--line);border-radius:6px;padding:6px 9px;font-size:12px;box-shadow:0 2px 8px rgba(0,0,0,.12);display:none;z-index:9;max-width:340px}
.legend{display:flex;gap:14px;font-size:12px;color:var(--ink2);margin:4px 0 8px;flex-wrap:wrap}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
select,input{font:inherit;padding:4px 8px;border:1px solid var(--line);border-radius:6px;background:var(--surf);color:var(--ink)}
.note{color:var(--ink2);font-size:12.5px}.warn{border-left:3px solid var(--orange);padding:6px 10px;background:var(--chip);border-radius:4px;font-size:12.5px;margin:8px 0}
.tw{font-size:12px;border-left:2px solid var(--line);padding:4px 8px;margin:4px 0;color:var(--ink2)}.tw b{color:var(--ink)}
details summary{cursor:pointer;font-weight:600}dl{display:grid;grid-template-columns:200px 1fr;gap:4px 14px;font-size:12.5px}dt{color:var(--ink2)}
.pos{color:var(--blue)}.neg{color:var(--red)}.hzbar{display:flex;gap:10px;align-items:center;margin:0 0 10px;font-size:13px}
"""

JS = r"""
const D = window.__SENT__;
const W = D.weeks, P = D.panel, N = D.names, HZ = D.horizons, L = D.long;
const fmt = (x,d=2)=> x==null?'–':(+x).toFixed(d);
const pct = (x,d=1)=> x==null?'–':((x*100).toFixed(d)+'%');
const sgn = (x,d=2)=> x==null?'–':((x>0?'+':'')+(+x).toFixed(d));
const cls = x => x==null?'':(x>0?'pos':x<0?'neg':'');
const quadOf = (r,mh,mb) => (r.HOT==null||r.BULL==null)?'':((r.HOT>=mh?'hot':'cold')+'-'+(r.BULL>=mb?'bull':'bear'));
const quad = r => quadOf(r, D.medHOT, D.medBULL);
const tip = document.getElementById('tip');
function showTip(e,html){tip.innerHTML=html;tip.style.display='block';const x=Math.min(e.clientX+14,innerWidth-360),y=e.clientY+14;tip.style.left=x+'px';tip.style.top=y+'px';}
function hideTip(){tip.style.display='none';}
function zbar(v,posColor,negColor){ if(v==null) return '<span class="barwrap"><i></i></span>';
  const w=Math.min(Math.abs(v),3)/3*48; const left = v>=0?48:48-w;
  return `<span class="barwrap"><i></i><b style="left:${left}px;width:${w}px;background:${v>=0?posColor:negColor}"></b></span>`; }
const hz = ()=>document.getElementById('hz').value;
// ---------- weekly picks: what we would have seen
function pkState(){ return {track:document.getElementById('pk_track').value, sig:document.getElementById('pk_sig').value, n:+document.getElementById('pk_n').value, h:document.getElementById('pk_h').value, win:document.getElementById('pk_win').value}; }
function pkStats(rows, n, h){ const out=[]; let ct=1,cb=1,cs=1;
  for(const r of rows){ const tv=r.top.slice(0,n).map(x=>x[h]).filter(x=>x!=null), bv=r.bot.slice(0,n).map(x=>x[h]).filter(x=>x!=null); if(!tv.length||!bv.length) continue;
    const mt=tv.reduce((a,b)=>a+b,0)/tv.length, mb=bv.reduce((a,b)=>a+b,0)/bv.length; if(h=='r1'){ct*=1+mt; cb*=1+mb; cs*=1+(mt-mb);}
    out.push({w:r.w, mt, mb, sp:mt-mb, ct:ct-1, cb:cb-1, cs:cs-1}); }
  return out; }
function pkColor(v){ if(v==null) return 'transparent'; const a=Math.min(Math.abs(v)/0.08,1); return v>=0?`rgba(42,120,214,${0.15+0.75*a})`:`rgba(227,73,72,${0.15+0.75*a})`; }
function renderPicks(){
  const PK=D.picks; if(!PK) return; const st=pkState(); const T=PK[st.track]; const sel=document.getElementById('pk_sig');
  if(sel.dataset.track!==st.track){ sel.innerHTML=''; Object.keys(T.picks).forEach(k=>{const o=document.createElement('option');o.value=k;o.textContent=T.labels[k]||k;sel.appendChild(o);}); sel.value=T.picks[st.sig]?st.sig:(T.picks['att']?'att':Object.keys(T.picks)[0]); sel.dataset.track=st.track; st.sig=sel.value; }
  const rows=T.picks[st.sig]||[]; const S=pkStats(rows,st.n,st.h); if(!S.length) return;
  const hit=S.filter(x=>x.sp>0).length/S.length, mt=S.reduce((a,x)=>a+x.mt,0)/S.length, mb=S.reduce((a,x)=>a+x.mb,0)/S.length;
  const hl=st.h=='r1'?'next week':'next 15 days';
  document.getElementById('pk_kpis').innerHTML=`<div class="kpi"><b class="${cls(mt)}">${pct(mt,2)}</b><span>mean ${hl} relative return of the top-${st.n} (${S.length} weeks)</span></div><div class="kpi"><b class="${cls(mb)}">${pct(mb,2)}</b><span>mean ${hl} relative return of the bottom-${st.n}</span></div><div class="kpi"><b class="${cls(mt-mb)}">${pct(mt-mb,2)}</b><span>spread per period · positive in ${pct(hit,0)} of weeks</span></div>`+(st.h=='r1'?`<div class="kpi"><b class="${cls(S[S.length-1].cs)}">${pct(S[S.length-1].cs,1)}</b><span>cumulative long-top / short-bottom, whole span, no costs</span></div>`:'');
  // curve (next-week compounding only)
  const svg=document.getElementById('pk_curve'); const W=svg.clientWidth||1000,H=260,m={l:52,r:16,t:12,b:28};
  if(st.h!=='r1'){ svg.outerHTML=`<svg id="pk_curve" height="40"><text x="${m.l}" y="24" font-size="12" fill="var(--ink3)">Cumulative curve is shown for the next-week horizon only (15-day windows overlap).</text></svg>`; }
  else { const vals=S.flatMap(x=>[x.ct,x.cb,x.cs]); const lo=Math.min(0,...vals), hi=Math.max(0.01,...vals); const X=i=>m.l+i/(S.length-1||1)*(W-m.l-m.r), Y=v=>m.t+(hi-v)/(hi-lo||1)*(H-m.t-m.b);
    let s=`<svg id="pk_curve" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">`; const steps=[lo,0,hi];
    for(const g of steps) s+=`<line x1="${m.l}" x2="${W-m.r}" y1="${Y(g)}" y2="${Y(g)}" stroke="${g==0?'var(--ink3)':'var(--grid)'}"/><text x="${m.l-6}" y="${Y(g)+4}" font-size="10.5" fill="var(--ink3)" text-anchor="end">${pct(g,0)}</text>`;
    const every=Math.max(1,Math.round(S.length/10)); S.forEach((x,i)=>{ if(i%every==0) s+=`<text x="${X(i)}" y="${H-8}" font-size="10.5" fill="var(--ink3)" text-anchor="middle">${x.w.slice(0,7)}</text>`; });
    for(const [k,c] of [['ct','var(--blue)'],['cb','var(--red)'],['cs','var(--orange)']]){ s+=`<path d="${S.map((x,i)=>`${i?'L':'M'}${X(i)},${Y(x[k])}`).join(' ')}" fill="none" stroke="${c}" stroke-width="2"/>`; const last=S[S.length-1]; s+=`<text x="${W-m.r-2}" y="${Y(last[k])+4}" font-size="11" fill="var(--ink2)" text-anchor="end">${pct(last[k],0)}</text>`; }
    svg.outerHTML=s+'</svg>'; }
  // grid
  const win=st.win==='all'?rows.length:Math.min(rows.length,+st.win); const R=rows.slice(rows.length-win); const cw=Math.max(44,Math.floor((Math.min(1400,(document.getElementById('pk_grid').clientWidth||1200))-70)/win));
  let g=`<table style="border-collapse:separate;border-spacing:2px;font-size:11px;width:auto"><thead><tr><th class="l" style="position:static;padding:2px 6px">rank</th>`+R.map(r=>`<th style="position:static;padding:2px 0;min-width:${cw}px;font-weight:500;color:var(--ink3)">${r.w.slice(5)}</th>`).join('')+'</tr></thead><tbody>';
  const cell=(x)=>x?`<td style="padding:0"><div title="${x.t} · ${(D.picks.names[x.t]||'').replace(/"/g,'')} · signal ${x.v} · next wk rel ${pct(x.r1)} (raw ${pct(x.raw1)}) · 15d rel ${pct(x.r15)}" style="background:${pkColor(x[st.h])};border-radius:3px;height:22px;line-height:22px;text-align:center;font-weight:600;color:var(--ink)">${x.t}</div></td>`:'<td></td>';
  for(let i=0;i<st.n;i++) g+=`<tr><td class="l" style="padding:0 6px;color:var(--ink3);white-space:nowrap">top ${i+1}</td>`+R.map(r=>cell(r.top[i])).join('')+'</tr>';
  g+=`<tr><td class="l" style="padding:2px 6px;color:var(--ink3);font-size:10px">spread</td>`+R.map(r=>{const s_=S.find(x=>x.w===r.w); return `<td style="text-align:center;color:var(--ink2);font-size:10.5px;padding:0" class="${cls(s_?s_.sp:null)}">${s_?pct(s_.sp,1):''}</td>`;}).join('')+'</tr>';
  for(let i=0;i<st.n;i++) g+=`<tr><td class="l" style="padding:0 6px;color:var(--ink3);white-space:nowrap">bottom ${i+1}</td>`+R.map(r=>cell(r.bot[i])).join('')+'</tr>';
  document.getElementById('pk_grid').innerHTML=g+'</tbody></table>';
  // all-signal summary table
  let t='<thead><tr><th class="l">Signal</th><th>top-'+st.n+'</th><th>bottom-'+st.n+'</th><th>spread</th><th>spread &gt; 0</th><th>weeks</th>'+(st.h=='r1'?'<th>cumulative spread</th>':'')+'</tr></thead><tbody>';
  const summ=Object.keys(T.picks).map(k=>{const s_=pkStats(T.picks[k],st.n,st.h); if(!s_.length) return null; const a=s_.reduce((q,x)=>q+x.mt,0)/s_.length,b=s_.reduce((q,x)=>q+x.mb,0)/s_.length; return {k,a,b,sp:a-b,hit:s_.filter(x=>x.sp>0).length/s_.length,n:s_.length,cum:s_[s_.length-1].cs};}).filter(Boolean).sort((x,y)=>y.sp-x.sp);
  for(const r of summ) t+=`<tr style="${r.k===st.sig?'background:var(--chip)':''}"><td class="l"><b>${T.labels[r.k]||r.k}</b></td><td class="${cls(r.a)}">${pct(r.a,2)}</td><td class="${cls(r.b)}">${pct(r.b,2)}</td><td class="${cls(r.sp)}"><b>${pct(r.sp,2)}</b></td><td>${pct(r.hit,0)}</td><td>${r.n}</td>${st.h=='r1'?`<td class="${cls(r.cum)}">${pct(r.cum,1)}</td>`:''}</tr>`;
  document.getElementById('pk_tbl').innerHTML=t+'</tbody>';
}
// ---------- lead / lag
function renderLeadLag(){
  const LL=D.leadlag; if(!LL) return; const C=LL.long.ccf, P=LL.long.partial, V=LL.long.verdict, lab=LL.labels, lags=LL.lags;
  const short=k=>lab[k]?lab[k].split(' (')[0].split(',')[0]:k;
  // small-multiple CCF bars
  const keys=Object.keys(C); let g='';
  for(const k of keys){ const c=C[k]; const W=300,H=130,m={l:26,r:6,t:18,b:22}; const mx=Math.max(0.06,...lags.map(l=>Math.abs((c[String(l)]||{}).ic||0)));
    const bw=(W-m.l-m.r)/lags.length, Y=v=>m.t+(mx-v)/(2*mx)*(H-m.t-m.b);
    let s=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}"><text x="${m.l}" y="12" font-size="11.5" font-weight="600" fill="var(--ink)">${short(k)}</text><text x="${W-m.r}" y="12" font-size="10.5" fill="var(--ink3)" text-anchor="end">${V[k]||''}</text>`;
    s+=`<line x1="${m.l}" x2="${W-m.r}" y1="${Y(0)}" y2="${Y(0)}" stroke="var(--ink3)"/>`;
    const x0=m.l+lags.indexOf(0)*bw; s+=`<rect x="${x0}" y="${m.t}" width="${bw}" height="${H-m.t-m.b}" fill="var(--chip)" opacity=".7"/>`;
    lags.forEach((l,i)=>{const o=c[String(l)]||{}; const v=o.ic||0; const x=m.l+i*bw+bw*0.18, w=bw*0.64, y0=Math.min(Y(0),Y(v)), hh=Math.abs(Y(v)-Y(0)); const sig=Math.abs(o.t||0)>=2;
      s+=`<rect x="${x}" y="${y0}" width="${w}" height="${Math.max(hh,1)}" rx="2" fill="${v>=0?'var(--blue)':'var(--red)'}" opacity="${sig?1:0.45}"><title>k=${l>0?'+':''}${l}: IC ${sgn(v,3)} · t ${fmt(o.t,1)} · ${o.n||0} weeks · hit ${pct(o.hit,0)}</title></rect><text x="${x+w/2}" y="${H-8}" font-size="10" fill="var(--ink3)" text-anchor="middle">${l>0?'+'+l:l}</text>`;});
    s+=`<text x="${m.l-4}" y="${Y(mx)+4}" font-size="9.5" fill="var(--ink3)" text-anchor="end">${mx.toFixed(2)}</text><text x="${m.l-4}" y="${Y(-mx)+4}" font-size="9.5" fill="var(--ink3)" text-anchor="end">−${mx.toFixed(2)}</text>`;
    g+=`<div style="flex:0 0 310px">${s}</svg></div>`; }
  document.getElementById('ccfgrid').innerHTML=g+'<div class="note" style="flex:1 1 100%">Shaded column = k=0 (coincident). Faded bars = |t|&lt;2. Bars left of the shade = sentiment reacting to price; right = sentiment leading price.</div>';
  // table
  let h='<thead><tr><th class="l">Signal</th>'+lags.map(l=>`<th>k=${l>0?'+':''}${l}</th>`).join('')+'<th>partial +1 (ex-momentum)</th><th>t</th><th class="l">Verdict</th></tr></thead><tbody>';
  for(const k of keys){const c=C[k], p=(P[k]||{})['1']||{};
    h+=`<tr><td class="l"><b>${lab[k]||k}</b></td>`+lags.map(l=>{const o=c[String(l)]||{}; const b=Math.abs(o.t||0)>=2; return `<td class="${cls(o.ic)}" style="${l==0?'background:var(--chip);':''}${b?'font-weight:600':'opacity:.6'}">${sgn(o.ic,3)}</td>`;}).join('')+`<td class="${cls(p.ic_partial)}"><b>${sgn(p.ic_partial,3)}</b> <span class="nm">raw ${sgn(p.ic_raw,3)}</span></td><td>${fmt(p.t_partial,1)}</td><td class="l">${V[k]||''}</td></tr>`;}
  document.getElementById('cct').innerHTML=h+'</tbody>';
  // by year (k=+1)
  const BY=LL.long.by_year; const yrs=Object.keys(BY).sort(); const ykeys=['tone','att','eps_rev','si','BULL'];
  let y='<thead><tr><th class="l">Signal</th>'+yrs.map(v=>`<th>${v} k=+1</th><th>${v} k=0</th>`).join('')+'</tr></thead><tbody>';
  for(const k of ykeys){ y+=`<tr><td class="l">${short(k)}</td>`+yrs.map(v=>{const a=((BY[v]||{})[k]||{})['1']||{}, b=((BY[v]||{})[k]||{})['0']||{}; return `<td class="${cls(a.ic)}">${sgn(a.ic,3)} <span class="nm">n=${a.n||0}</span></td><td class="${cls(b.ic)}" style="opacity:.7">${sgn(b.ic,3)}</td>`;}).join('')+'</tr>'; }
  document.getElementById('ccy').innerHTML=y+'</tbody>';
  // reverse
  const RV=LL.long.reverse; let r='<thead><tr><th class="l">Return of week t → signal at end of week t+1</th><th>IC</th><th>t</th><th>weeks</th></tr></thead><tbody>';
  for(const k of Object.keys(RV)){const o=RV[k]; r+=`<tr><td class="l">${lab[k]||k}</td><td class="${cls(o.ic)}"><b>${sgn(o.ic,3)}</b></td><td>${fmt(o.t,1)}</td><td>${o.n}</td></tr>`;}
  document.getElementById('ccr').innerHTML=r+'</tbody>';
  // double sorts
  const DS=LL.long.double_sort; let ds='';
  for(const k of Object.keys(DS)){const c=DS[k]; const rows=['mom_lo','mom_mid','mom_hi'], cols=['sig_lo','sig_mid','sig_hi'];
    let t=`<div class="col" style="flex:1 1 300px"><div class="note"><b>${short(k)}</b></div><table><thead><tr><th class="l">past 4w ↓ / signal →</th><th>low</th><th>mid</th><th>high</th><th>hi−lo</th></tr></thead><tbody>`;
    for(const rr of rows){const v=cols.map(cc=>(c[`${rr}|${cc}`]||{}).mean); const d_=(v[2]!=null&&v[0]!=null)?v[2]-v[0]:null; t+=`<tr><td class="l">${rr.replace('mom_','mom ')}</td>`+v.map(x=>`<td class="${cls(x)}">${pct(x)}</td>`).join('')+`<td class="${cls(d_)}"><b>${pct(d_)}</b></td></tr>`;}
    ds+=t+'</tbody></table></div>';}
  document.getElementById('dsgrid').innerHTML=ds;
  // own corpus
  const OC=LL.own.ccf, OP=LL.own.partial, ol=LL.own_labels; const olags=[-3,-2,-1,0,1,2,3];
  let o='<thead><tr><th class="l">Signal</th>'+olags.map(l=>`<th>k=${l>0?'+':''}${l}</th>`).join('')+'<th>partial +1</th></tr></thead><tbody>';
  for(const k of Object.keys(OC)){const c=OC[k], p=(OP[k]||{})['1']||{}; if(!Object.keys(c).length) continue;
    o+=`<tr><td class="l">${ol[k]||k}</td>`+olags.map(l=>{const q=c[String(l)]||{}; const b=Math.abs(q.t||0)>=2; return `<td class="${cls(q.ic)}" style="${l==0?'background:var(--chip);':''}${b?'font-weight:600':'opacity:.6'}">${sgn(q.ic,3)}</td>`;}).join('')+`<td class="${cls(p.ic_partial)}">${sgn(p.ic_partial,3)}</td></tr>`;}
  document.getElementById('cco').innerHTML=o+'</tbody>';
}
// ---------- earnings event study
function renderEvents(){
  const E=D.events; if(!E) return; const st=E.stats, SIG=E.signals, OUTS=Object.keys(E.outcomes);
  let h='<thead><tr><th class="l">Pre-print signal</th>'+OUTS.map(o=>`<th>IC ${o}</th><th>Q5−Q1</th>`).join('')+'<th>n</th></tr></thead><tbody>';
  for(const k of Object.keys(SIG)){ const any=OUTS.some(o=>st[`${k}|${o}`]); if(!any) continue;
    h+=`<tr><td class="l"><b>${SIG[k]}</b></td>`+OUTS.map(o=>{const x=st[`${k}|${o}`]||{}; return `<td class="${cls(x.ic)}">${sgn(x.ic,3)}</td><td class="${cls(x.q5_q1)}">${pct(x.q5_q1)}</td>`;}).join('')+`<td>${(st[`${k}|tot15`]||st[`${k}|react`]||{}).n||'–'}</td></tr>`;}
  document.getElementById('evt').innerHTML=h+'</tbody>';
  const C=E.conditional; const rows=['hot','mid','cold'], cols=['beat','inline','miss'];
  let c='<thead><tr><th class="l">Attention into print</th>'+cols.map(x=>`<th colspan="3">${x}</th>`).join('')+'</tr><tr><th></th>'+cols.map(()=>'<th>react</th><th>15d</th><th>n</th>').join('')+'</tr></thead><tbody>';
  for(const r of rows){ c+=`<tr><td class="l"><b>${r}</b></td>`+cols.map(x=>{const v=C[`${r}|${x}`]||{}; return `<td class="${cls(v.react)}">${pct(v.react)}</td><td class="${cls(v.tot15)}">${pct(v.tot15)}</td><td>${v.n||0}</td>`;}).join('')+'</tr>';}
  document.getElementById('evc').innerHTML=c+'</tbody>';
  const years=[...new Set(Object.values(st).flatMap(x=>Object.keys(x.by_year||{})))].sort();
  let y='<thead><tr><th class="l">Signal</th>'+years.map(v=>`<th>${v}</th>`).join('')+'</tr></thead><tbody>';
  for(const k of Object.keys(SIG)){const x=st[`${k}|tot15`]; if(!x||!Object.keys(x.by_year||{}).length) continue;
    y+=`<tr><td class="l">${SIG[k]}</td>`+years.map(v=>{const b=(x.by_year||{})[v]; return b?`<td class="${cls(b.ic)}">${sgn(b.ic,3)} <span class="nm">n=${b.n}</span></td>`:'<td>–</td>';}).join('')+'</tr>';}
  document.getElementById('evy').innerHTML=y+'</tbody>';
  let r='<thead><tr><th class="l">Ticker</th><th>Print</th><th>Surprise</th><th>BBG att Δ</th><th>BBG tone</th><th>Own att Δ</th><th>Own tone</th><th>SS notes</th><th>SS net rtg</th><th>SS avg PT Δ</th><th>EPS rev</th><th>Run-up</th><th>React</th><th>15d</th><th>Drift</th></tr></thead><tbody>';
  for(const e of E.recent){ r+=`<tr><td class="l"><span class="tk">${e.t}</span></td><td>${e.date}${e.after?' pm':' am'}</td><td class="${cls(e.surprise)}">${e.surprise==null?'–':sgn(e.surprise*100,0)+'%'}</td><td>${e.bbg_att==null?'–':(e.bbg_att>0?'+':'')+(Math.exp(e.bbg_att)*100-100).toFixed(0)+'%'}</td><td>${sgn(e.bbg_tone,3)}</td><td>${e.own_att==null?'–':(e.own_att>0?'+':'')+(Math.exp(e.own_att)*100-100).toFixed(0)+'%'}</td><td>${sgn(e.own_tone)}</td><td>${fmt(e.ss_n,0)}</td><td>${sgn(e.ss_net,1)}</td><td>${e.ss_pt==null?'–':sgn(e.ss_pt*100,1)+'%'}</td><td>${e.eps_rev==null?'–':sgn(e.eps_rev*100,1)+'%'}</td><td class="${cls(e.runup)}">${pct(e.runup)}</td><td class="${cls(e.react)}">${pct(e.react)}</td><td class="${cls(e.tot15)}">${pct(e.tot15)}</td><td class="${cls(e.drift)}">${pct(e.drift)}</td></tr>`;}
  document.getElementById('evr').innerHTML=r+'</tbody>';
}

// ---------- ranking table (own corpus)
let sortKey='HOT', sortDir=-1;
function renderTable(){
  const wk = document.getElementById('wk').value; const row = P[wk];
  const rows = Object.keys(row).map(t=>({t,...row[t]})).filter(r=>r.HOT!=null||r.BULL!=null);
  rows.sort((a,b)=>{const x=a[sortKey],y=b[sortKey]; if(x==null&&y==null)return 0; if(x==null)return 1; if(y==null)return -1; return (x<y?-1:x>y?1:0)*sortDir;});
  const cols=[['t','Ticker'],['HOT','HOT z'],['att','Attention Δ'],['m_cur','Curated /wk'],['m_wire','Wire /wk'],['BULL','BULL z'],['tone','Tone'],['bull','#bull'],['bear','#bear'],['eps_rev','EPS rev 4w'],['rating','Rating Δ4w'],['si','SI % float'],['ss_n','SS notes /wk'],['ss_att','SS flow Δ'],['ss_tone','SS tone'],['ss_act','SS net rtg'],['ss_pt','SS avg PT Δ'],['ret_m4w','Ret −4w'],['ret_1w','Fwd 1w'],['ret_15d','Fwd 15d'],['ret_4w','Fwd 4w'],['q','Quadrant']];
  let h='<thead><tr>'+cols.map(c=>`<th class="${c[0]=='t'||c[0]=='q'?'l':''}" data-k="${c[0]}">${c[1]}${sortKey==c[0]?(sortDir<0?' ▼':' ▲'):''}</th>`).join('')+'</tr></thead><tbody>';
  for(const r of rows){ const q=quad(r); const c=q=='hot-bull'?'hb':q=='cold-bear'?'cb':q=='hot-bear'?'hr':'';
    h+=`<tr><td class="l"><span class="tk">${r.t}</span><span class="nm">${(N[r.t]||'').slice(0,26)}</span></td>
    <td>${zbar(r.HOT,'var(--orange)','var(--ink3)')} ${sgn(r.HOT)}</td><td>${r.att==null?'–':(r.att>0?'+':'')+(Math.exp(r.att)*100-100).toFixed(0)+'%'}</td><td>${fmt(r.m_cur,0)}</td><td>${fmt(r.m_wire,0)}</td>
    <td>${zbar(r.BULL,'var(--blue)','var(--red)')} ${sgn(r.BULL)}</td><td>${sgn(r.tone)}</td><td>${r.bull}</td><td>${r.bear}</td><td>${r.eps_rev==null?'–':sgn(r.eps_rev*100,1)+'%'}</td><td>${sgn(r.rating)}</td><td>${fmt(r.si,1)}</td><td>${fmt(r.ss_n,0)}</td><td>${r.ss_att==null?'–':(r.ss_att>0?'+':'')+(Math.exp(r.ss_att)*100-100).toFixed(0)+'%'}</td><td>${sgn(r.ss_tone)}</td><td>${sgn(r.ss_act,1)}</td><td>${r.ss_pt==null?'–':sgn(r.ss_pt*100,1)+'%'}</td>
    <td class="${cls(r.ret_m4w)}">${pct(r.ret_m4w)}</td><td class="${cls(r.ret_1w)}">${pct(r.ret_1w)}</td><td class="${cls(r.ret_15d)}">${pct(r.ret_15d)}</td><td class="${cls(r.ret_4w)}">${pct(r.ret_4w)}</td><td class="l"><span class="tag ${c}">${q}</span></td></tr>`; }
  const T=document.getElementById('tbl'); T.innerHTML=h+'</tbody>';
  T.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k; if(k=='q')return; if(sortKey==k)sortDir*=-1; else {sortKey=k;sortDir=-1;} renderTable();});
  document.getElementById('tblnote').textContent = `${rows.length} names · week ending ${wk} · forward returns here are raw local-currency returns (blank until the window has elapsed); the backtest uses universe-relative returns.`;
}

// ---------- scatter HOT × BULL
function renderScatter(){
  const wk=document.getElementById('wk').value; const row=P[wk]; const svg=document.getElementById('sc'); const Wd=svg.clientWidth||900, H=440, m={l:44,r:16,t:16,b:36};
  const pts=Object.keys(row).map(t=>({t,...row[t]})).filter(r=>r.HOT!=null&&r.BULL!=null);
  const X=v=>m.l+(Math.max(-3,Math.min(3,v))+3)/6*(Wd-m.l-m.r), Y=v=>m.t+(3-Math.max(-3,Math.min(3,v)))/6*(H-m.t-m.b);
  let s=`<svg viewBox="0 0 ${Wd} ${H}" width="${Wd}" height="${H}">`;
  s+=`<rect x="${X(0)}" y="${m.t}" width="${X(3)-X(0)}" height="${Y(0)-m.t}" fill="var(--orange-soft)" opacity=".35"/>`;
  s+=`<rect x="${m.l}" y="${Y(0)}" width="${X(0)-m.l}" height="${Y(-3)-Y(0)}" fill="var(--blue-soft)" opacity=".35"/>`;
  for(const g of [-2,-1,1,2]){s+=`<line x1="${X(g)}" x2="${X(g)}" y1="${m.t}" y2="${H-m.b}" stroke="var(--grid)"/><line y1="${Y(g)}" y2="${Y(g)}" x1="${m.l}" x2="${Wd-m.r}" stroke="var(--grid)"/>`;}
  s+=`<line x1="${X(0)}" x2="${X(0)}" y1="${m.t}" y2="${H-m.b}" stroke="var(--ink3)"/><line y1="${Y(0)}" y2="${Y(0)}" x1="${m.l}" x2="${Wd-m.r}" stroke="var(--ink3)"/>`;
  const lab=(x,y,t,a)=>`<text x="${x}" y="${y}" font-size="11" fill="var(--ink3)" text-anchor="${a||'start'}">${t}</text>`;
  s+=lab(Wd-m.r-4,m.t+14,'HOT · BULL','end')+lab(m.l+6,m.t+14,'COLD · BULL')+lab(m.l+6,H-m.b-8,'COLD · BEAR')+lab(Wd-m.r-4,H-m.b-8,'HOT · BEAR','end');
  s+=lab(Wd/2,H-6,'HOT z (attention: curated + wire mentions vs trailing 4 weeks) →','middle');
  s+=`<text transform="translate(12 ${H/2}) rotate(-90)" font-size="11" fill="var(--ink3)" text-anchor="middle">BULL z (tone, tone Δ, EPS revision, rating drift) →</text>`;
  for(const r of pts){const q=quad(r); const c=q=='hot-bull'?'var(--orange)':q=='cold-bear'?'var(--blue)':'var(--ink3)';
    s+=`<circle cx="${X(r.HOT)}" cy="${Y(r.BULL)}" r="5" fill="${c}" stroke="var(--surf)" stroke-width="2" data-t="${r.t}"/>`;
    if(Math.abs(r.HOT)>1.2||Math.abs(r.BULL)>1.2||['NVDA','TSM','MU','AVGO','GOOG','META','MSFT','AMZN','AAPL'].includes(r.t)) s+=`<text x="${X(r.HOT)+7}" y="${Y(r.BULL)+4}" font-size="10.5" fill="var(--ink2)">${r.t}</text>`;}
  svg.outerHTML=s.replace('<svg','<svg id="sc"')+'</svg>';
  document.querySelectorAll('#sc circle').forEach(c=>{c.onmousemove=e=>{const r=row[c.dataset.t];showTip(e,`<b>${c.dataset.t}</b> ${N[c.dataset.t]||''}<br>HOT ${sgn(r.HOT)} · BULL ${sgn(r.BULL)}<br>curated ${fmt(r.m_cur,0)}/wk · wire ${fmt(r.m_wire,0)}/wk · tone ${sgn(r.tone)}<br>EPS rev 4w ${r.eps_rev==null?'–':sgn(r.eps_rev*100,1)+'%'} · rating Δ ${sgn(r.rating)} · SI ${fmt(r.si,1)}%<br>${quad(r)}`);};c.onmouseleave=hideTip;});
}

// ---------- backtest blocks (shared by both tracks)
function btTable(B, keys, lab, el, years){
  let h='<thead><tr><th class="l">Component</th>'+Object.keys(HZ).map(k=>`<th>IC ${k}</th>`).join('')+'<th>t (sel.)</th><th>hit (sel.)</th><th>Q5−Q1 (sel.)</th>'+(years||[]).map(y=>`<th>IC ${y}</th>`).join('')+'<th>weeks</th></tr></thead><tbody>';
  const sel=hz();
  for(const k of keys){const b=B[`${k}|rel_ret_${sel}`]||{};
    h+=`<tr><td class="l"><b>${lab[k]}</b></td>`+Object.keys(HZ).map(hh=>{const x=(B[`${k}|rel_ret_${hh}`]||{}).mean_ic; return `<td class="${cls(x)}" style="${hh==sel?'font-weight:600':''}">${sgn(x,3)}</td>`;}).join('')
      +`<td>${fmt(b.t,1)}</td><td>${pct(b.hit,0)}</td><td class="${cls(b.q5_q1)}">${pct(b.q5_q1)}</td>`+(years||[]).map(y=>{const v=((b.by_year||{})[y]||{}).mean_ic; return `<td class="${cls(v)}">${sgn(v,3)}</td>`;}).join('')+`<td>${b.weeks||'–'}</td></tr>`;}
  el.innerHTML=h+'</tbody>';
}
function icBars(B, keys, lab, id){
  const svg=document.getElementById(id); const Wd=svg.clientWidth||600,H=26*keys.length+30,m={l:190,r:50,t:10,b:20}; const sel=hz(); const vals=keys.map(k=>(B[`${k}|rel_ret_${sel}`]||{}).mean_ic??0);
  const mx=Math.max(0.12,...vals.map(Math.abs)); const X=v=>m.l+(v+mx)/(2*mx)*(Wd-m.l-m.r); const bh=(H-m.t-m.b)/keys.length;
  let s=`<svg viewBox="0 0 ${Wd} ${H}" width="${Wd}" height="${H}"><line x1="${X(0)}" x2="${X(0)}" y1="${m.t}" y2="${H-m.b}" stroke="var(--ink3)"/>`;
  keys.forEach((k,i)=>{const v=vals[i],y=m.t+i*bh+3; const x0=Math.min(X(0),X(v)),w=Math.abs(X(v)-X(0));
    s+=`<text x="${m.l-8}" y="${y+bh/2+1}" font-size="11.5" fill="var(--ink2)" text-anchor="end">${lab[k]}</text><rect x="${x0}" y="${y}" width="${w}" height="${bh-6}" rx="3" fill="${v>=0?'var(--blue)':'var(--red)'}"/><text x="${v>=0?X(v)+5:X(v)-5}" y="${y+bh/2+1}" font-size="11" fill="var(--ink2)" text-anchor="${v>=0?'start':'end'}">${sgn(v,3)}</text>`;});
  svg.outerHTML=s.replace('<svg',`<svg id="${id}"`)+'</svg>';
}
function quadBars(Q, id){
  const qs=['hot-bull','hot-bear','cold-bull','cold-bear']; const svg=document.getElementById(id); const W2=svg.clientWidth||500,H2=230,m2={l:40,r:10,t:16,b:40}; const sel=hz();
  const qv=qs.map(q=>(Q[`${q}|rel_ret_${sel}`]||{}).mean??0); const qm=Math.max(0.005,...qv.map(Math.abs)); const Y=v=>m2.t+(qm-v)/(2*qm)*(H2-m2.t-m2.b); const bw=(W2-m2.l-m2.r)/qs.length;
  let s=`<svg viewBox="0 0 ${W2} ${H2}" width="${W2}" height="${H2}"><line x1="${m2.l}" x2="${W2-m2.r}" y1="${Y(0)}" y2="${Y(0)}" stroke="var(--ink3)"/>`;
  qs.forEach((q,i)=>{const v=qv[i],x=m2.l+i*bw+bw*0.2,w=bw*0.6,y0=Math.min(Y(0),Y(v)),hh=Math.abs(Y(v)-Y(0)); const o=Q[`${q}|rel_ret_${sel}`]||{};
    s+=`<rect x="${x}" y="${y0}" width="${w}" height="${hh}" rx="3" fill="${v>=0?'var(--blue)':'var(--red)'}"><title>${q}: mean ${pct(v,2)} · hit ${pct(o.hit,0)} · n=${o.n||0}</title></rect><text x="${x+w/2}" y="${y0-5}" font-size="11.5" fill="var(--ink2)" text-anchor="middle">${pct(v,2)}</text><text x="${x+w/2}" y="${H2-m2.b+16}" font-size="11.5" fill="var(--ink2)" text-anchor="middle">${q}</text><text x="${x+w/2}" y="${H2-m2.b+30}" font-size="10.5" fill="var(--ink3)" text-anchor="middle">n=${o.n||0} · hit ${pct(o.hit,0)}</text>`;});
  svg.outerHTML=s.replace('<svg',`<svg id="${id}"`)+'</svg>';
}
function icSeries(B, id, series, everyN){
  const svg=document.getElementById(id); const W3=svg.clientWidth||900,H3=230,m3={l:44,r:16,t:12,b:28}; const sel=hz();
  const base=(B[`${series[0][0]}|rel_ret_${sel}`]||{ics:[]}).ics; const wks=base.map(x=>x[0]); if(!wks.length){svg.outerHTML=`<svg id="${id}" height="40"></svg>`;return;}
  const X3=i=>m3.l+i/(wks.length-1||1)*(W3-m3.l-m3.r), Y3=v=>m3.t+(0.4-Math.max(-0.4,Math.min(0.4,v)))/0.8*(H3-m3.t-m3.b);
  let s3=`<svg viewBox="0 0 ${W3} ${H3}" width="${W3}" height="${H3}">`;
  for(const g of [-0.2,0,0.2]) s3+=`<line x1="${m3.l}" x2="${W3-m3.r}" y1="${Y3(g)}" y2="${Y3(g)}" stroke="${g==0?'var(--ink3)':'var(--grid)'}"/><text x="${m3.l-6}" y="${Y3(g)+4}" font-size="10.5" fill="var(--ink3)" text-anchor="end">${g}</text>`;
  wks.forEach((w,i)=>{ if(i%everyN==0) s3+=`<text x="${X3(i)}" y="${H3-8}" font-size="10.5" fill="var(--ink3)" text-anchor="middle">${everyN>4?w.slice(0,7):w.slice(5)}</text>`;});
  for(const [k,c,l] of series){const ics=(B[`${k}|rel_ret_${sel}`]||{ics:[]}).ics; const idx=Object.fromEntries(wks.map((w,i)=>[w,i]));
    const pth=ics.filter(x=>idx[x[0]]!=null).map((x,i)=>`${i?'L':'M'}${X3(idx[x[0]])},${Y3(x[1])}`).join(' ');
    s3+=`<path d="${pth}" fill="none" stroke="${c}" stroke-width="${wks.length>40?1.5:2}"/>`+(wks.length>60?'':ics.filter(x=>idx[x[0]]!=null).map(x=>`<circle cx="${X3(idx[x[0]])}" cy="${Y3(x[1])}" r="4" fill="${c}" stroke="var(--surf)" stroke-width="2"><title>${l} · ${x[0]} · IC ${sgn(x[1],3)} · n=${x[2]}</title></circle>`).join(''));}
  svg.outerHTML=s3.replace('<svg',`<svg id="${id}"`)+'</svg>';
}
const LAB={att:'Attention (curated Δ)',news:'Wire volume Δ',tone:'Tweet tone',tone_chg:'Tone change',eps_rev:'EPS revision 4w',rating:'Rating drift 4w',si:'Short interest',ss_att:'Sell-side note flow Δ',ss_tone:'Sell-side note tone',ss_act:'Sell-side net rating chg',ss_pt:'Sell-side avg PT chg %',ss_est:'Sell-side net est. revisions',HOT:'HOT composite',BULL:'BULL composite'};
const LLAB={att:'BBG Twitter count Δ',news:'BBG news count Δ',tone:'BBG Twitter sentiment',tone_chg:'BBG sentiment change',news_tone:'BBG news sentiment',eps_rev:'EPS revision 4w',rating:'Rating drift 4w',si:'Short interest',HOT:'HOT composite',BULL:'BULL composite'};
function renderBacktest(){
  const keys=Object.keys(LAB); btTable(D.backtest,keys,LAB,document.getElementById('bt'));
  icBars(D.backtest,keys,LAB,'icbar'); quadBars(D.quadrants,'qbar'); icSeries(D.backtest,'icts',[['att','var(--orange)','Attention'],['BULL','var(--blue)','BULL composite']],2);
  if(L){const lk=Object.keys(LLAB); btTable(L.backtest,lk,LLAB,document.getElementById('lbt'),L.years);
    icBars(L.backtest,lk,LLAB,'licbar'); quadBars(L.quadrants,'lqbar'); icSeries(L.backtest,'licts',[['att','var(--orange)','BBG Twitter count Δ'],['BULL','var(--blue)','BULL composite']],9);
    renderLongTable();}
  document.querySelectorAll('.hzlab').forEach(e=>e.textContent=hz());
}
function renderLongTable(){
  const row=L.latest; const rows=Object.keys(row).map(t=>({t,...row[t]})).filter(r=>r.HOT!=null||r.BULL!=null).sort((a,b)=>(b.HOT??-9)-(a.HOT??-9));
  let h='<thead><tr><th class="l">Ticker</th><th>HOT z</th><th>Tweets /wk (BBG)</th><th>Δ vs 4w</th><th>News /wk</th><th>BULL z</th><th>BBG sentiment</th><th>pos / neg</th><th>EPS rev 4w</th><th>Rating Δ4w</th><th>SI %</th><th class="l">Quadrant</th></tr></thead><tbody>';
  for(const r of rows){const q=quadOf(r,L.medHOT,L.medBULL); const c=q=='hot-bull'?'hb':q=='cold-bear'?'cb':q=='hot-bear'?'hr':'';
    h+=`<tr><td class="l"><span class="tk">${r.t}</span><span class="nm">${(N[r.t]||'').slice(0,26)}</span></td><td>${zbar(r.HOT,'var(--orange)','var(--ink3)')} ${sgn(r.HOT)}</td><td>${fmt(r.cnt,0)}</td><td>${r.att==null?'–':(r.att>0?'+':'')+(Math.exp(r.att)*100-100).toFixed(0)+'%'}</td><td>${fmt(r.ncnt,0)}</td><td>${zbar(r.BULL,'var(--blue)','var(--red)')} ${sgn(r.BULL)}</td><td>${sgn(r.tone,3)}</td><td>${r.pos} / ${r.neg}</td><td>${r.eps_rev==null?'–':sgn(r.eps_rev*100,1)+'%'}</td><td>${sgn(r.rating)}</td><td>${fmt(r.si,1)}</td><td class="l"><span class="tag ${c}">${q}</span></td></tr>`;}
  document.getElementById('ltbl').innerHTML=h+'</tbody>';
}

// ---------- ticker explorer
function renderTicker(){
  const t=document.getElementById('tk').value; const rows=W.map(w=>({w,...(P[w][t]||{})}));
  const svg=document.getElementById('tkc'); const Wd=svg.clientWidth||900; const ph=110,gap=26,m={l:52,r:16,t:8}; const H=m.t+3*(ph+gap);
  const X=i=>m.l+i/(W.length-1)*(Wd-m.l-m.r-10);
  const panels=[['Curated mentions / week (orange) and wire mentions (gray) — own corpus','m'],['Tweet tone (lexicon, −1..+1), shrunk toward 0 when few scored tweets','tone'],['Price (Friday close, local ccy)','px']];
  let s=`<svg viewBox="0 0 ${Wd} ${H}" width="${Wd}" height="${H}">`;
  panels.forEach((p,pi)=>{const top=m.t+pi*(ph+gap); s+=`<text x="${m.l}" y="${top+10}" font-size="11.5" fill="var(--ink2)">${p[0]}</text>`;
    if(p[1]=='m'){const mx=Math.max(1,...rows.map(r=>Math.max(r.m_cur||0,r.m_wire||0))); const Y=v=>top+ph-(v/mx)*(ph-18); const bw=(X(1)-X(0))*0.38;
      rows.forEach((r,i)=>{s+=`<rect x="${X(i)-bw}" y="${Y(r.m_cur||0)}" width="${bw-1}" height="${top+ph-Y(r.m_cur||0)}" rx="2" fill="var(--orange)"><title>${r.w} curated ${fmt(r.m_cur,0)}</title></rect><rect x="${X(i)+1}" y="${Y(r.m_wire||0)}" width="${bw-1}" height="${top+ph-Y(r.m_wire||0)}" rx="2" fill="var(--ink3)"><title>${r.w} wire ${fmt(r.m_wire,0)}</title></rect>`;});
      s+=`<text x="${m.l-6}" y="${top+ph}" font-size="10" fill="var(--ink3)" text-anchor="end">0</text><text x="${m.l-6}" y="${Y(mx)+8}" font-size="10" fill="var(--ink3)" text-anchor="end">${mx.toFixed(0)}</text>`;}
    else if(p[1]=='tone'){const Y=v=>top+18+(1-Math.max(-1,Math.min(1,v)))/2*(ph-18); s+=`<line x1="${m.l}" x2="${Wd-m.r}" y1="${Y(0)}" y2="${Y(0)}" stroke="var(--grid)"/>`;
      const pts=rows.map((r,i)=>r.tone==null?null:[X(i),Y(r.tone),r]).filter(Boolean); s+=`<path d="${pts.map((q,i)=>`${i?'L':'M'}${q[0]},${q[1]}`).join(' ')}" fill="none" stroke="var(--blue)" stroke-width="2"/>`;
      pts.forEach(q=>{s+=`<circle cx="${q[0]}" cy="${q[1]}" r="4" fill="${q[2].tone>=0?'var(--blue)':'var(--red)'}" stroke="var(--surf)" stroke-width="2"><title>${q[2].w} tone ${sgn(q[2].tone)} · ${q[2].bull} bull / ${q[2].bear} bear tweets</title></circle>`;});
      s+=`<text x="${m.l-6}" y="${Y(1)+4}" font-size="10" fill="var(--ink3)" text-anchor="end">+1</text><text x="${m.l-6}" y="${Y(-1)+4}" font-size="10" fill="var(--ink3)" text-anchor="end">−1</text>`;}
    else{const px=rows.map(r=>r.px).filter(v=>v!=null); if(px.length){const lo=Math.min(...px),hi=Math.max(...px); const Y=v=>top+18+(hi-v)/((hi-lo)||1)*(ph-18);
      const pts=rows.map((r,i)=>r.px==null?null:[X(i),Y(r.px),r]).filter(Boolean); s+=`<path d="${pts.map((q,i)=>`${i?'L':'M'}${q[0]},${q[1]}`).join(' ')}" fill="none" stroke="var(--ink)" stroke-width="2"/>`;
      pts.forEach(q=>{s+=`<circle cx="${q[0]}" cy="${q[1]}" r="3.5" fill="var(--ink)" stroke="var(--surf)" stroke-width="2"><title>${q[2].w} ${fmt(q[2].px,2)}</title></circle>`;});
      s+=`<text x="${m.l-6}" y="${Y(hi)+4}" font-size="10" fill="var(--ink3)" text-anchor="end">${hi.toFixed(0)}</text><text x="${m.l-6}" y="${Y(lo)+4}" font-size="10" fill="var(--ink3)" text-anchor="end">${lo.toFixed(0)}</text>`;}}
    if(pi==2) rows.forEach((r,i)=>{ if(i%2==0) s+=`<text x="${X(i)}" y="${top+ph+14}" font-size="10.5" fill="var(--ink3)" text-anchor="middle">${r.w.slice(5)}</text>`;});
  });
  svg.outerHTML=s.replace('<svg','<svg id="tkc"')+'</svg>';
  const hs=(D.top_handles[t]||[]).map(x=>`@${x[0]} (${x[1].toFixed(0)})`).join(' · ');
  const ex=(D.examples[t]||[]).map(e=>`<div class="tw"><b>@${e.h}</b> <span style="color:var(--ink3)">${e.d} · tone ${sgn(e.s)} · eng ${e.e}</span><br>${e.t.replace(/</g,'&lt;')}</div>`).join('');
  document.getElementById('tkinfo').innerHTML=`<div class="note"><b>${t}</b> · ${N[t]||''} · top handles: ${hs||'–'}</div>${ex||'<div class="note">No high-engagement curated tweets in the last weeks.</div>'}`;
}
function init(){
  const wk=document.getElementById('wk'); W.slice().reverse().forEach(w=>{const o=document.createElement('option');o.value=w;o.textContent=w;wk.appendChild(o);});
  const tk=document.getElementById('tk'); D.tickers.slice().sort().forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t+' — '+(N[t]||'').slice(0,28);tk.appendChild(o);}); tk.value='NVDA';
  wk.onchange=()=>{renderTable();renderScatter();}; tk.onchange=renderTicker; document.getElementById('hz').onchange=renderBacktest;
  renderTable();renderScatter();renderBacktest();renderTicker();renderEvents();renderLeadLag();
  if(D.picks){ ['pk_track','pk_sig','pk_n','pk_h','pk_win'].forEach(id=>document.getElementById(id).onchange=renderPicks); renderPicks(); }
  window.addEventListener('resize',()=>{renderScatter();renderBacktest();renderTicker(); if(D.picks) renderPicks();});
}
init();
"""

def _bt(bt, k, h): return bt.get(f"{k}|rel_ret_{h}", {})

def render(panel, daily, bbg, long=None, events=None, ss=None, leadlag=None, picks=None):
    weeks = panel["weeks"]; last = weeks[-1]; row = panel["panel"][last]
    hs = sorted(r["HOT"] for r in row.values() if r["HOT"] is not None); bs = sorted(r["BULL"] for r in row.values() if r["BULL"] is not None)
    med_hot = hs[len(hs) // 2] if hs else 0; med_bull = bs[len(bs) // 2] if bs else 0
    cutoff = (dt.date.fromisoformat(last) - dt.timedelta(21)).isoformat()
    examples = {}
    for t, days in daily["tickers"].items():
        ex = [dict(x, d=d) for d, r in days.items() if d >= cutoff for x in r.get("top", [])]
        ex.sort(key=lambda x: -x["e"]); examples[t] = ex[:5]
    bt = panel["backtest"]; q = panel["quadrants"]; H = panel.get("horizons", {"1w": 7, "15d": 15, "4w": 28})
    long_payload = None; long_html = ""
    if long:
        lw = long["weeks"]; llast = lw[-1]; lrow = long["panel"][llast]
        lhs = sorted(r["HOT"] for r in lrow.values() if r.get("HOT") is not None); lbs = sorted(r["BULL"] for r in lrow.values() if r.get("BULL") is not None)
        years = sorted({w[:4] for w in lw})
        long_payload = {"backtest": long["backtest"], "quadrants": long["quadrants"], "latest": lrow, "weeks": lw, "years": years,
                        "medHOT": lhs[len(lhs) // 2] if lhs else 0, "medBULL": lbs[len(lbs) // 2] if lbs else 0}
        la15, lb15 = _bt(long["backtest"], "att", "15d"), _bt(long["backtest"], "BULL", "15d")
        lt15 = _bt(long["backtest"], "tone", "15d")
        by = lambda b: " · ".join(f"{y} {v['mean_ic']:+.3f}" for y, v in b.get("by_year", {}).items())
        xval = long.get("xval")
        long_html = f"""
<section><h2>Backward track — Bloomberg Twitter & news sentiment, {lw[0]} → {llast}</h2>
<div class="note">Bloomberg computes a daily Twitter sentiment score, tweet count, positive/negative counts and the same for news per security. It is <b>all of X</b> (not our handle list), history back to 2024, and it lets the same components be tested over <b>{len(lw)} weekly cross-sections</b> instead of 17. Same construction as above: attention = weekly count vs own trailing 4 weeks; tone = count-weighted weekly sentiment; EPS revision, rating drift and short interest identical.</div>
{('<div class="note" style="margin-top:6px"><b>Does our curated corpus agree with Bloomberg\'s all-of-X count?</b> Weekly cross-sectional rank correlation between the two attention measures over the overlapping weeks: mean %+.2f (%d weeks). Tone: %+.2f.</div>' % (xval['att'], xval['n'], xval['tone'])) if xval else ''}
<div class="kpis">
 <div class="kpi"><b>{la15.get('mean_ic', 0):+.3f}</b><span>IC, BBG Twitter count Δ → fwd 15d ({la15.get('weeks', 0)}w, hit {la15.get('hit', 0):.0%}) · {by(la15)}</span></div>
 <div class="kpi"><b>{lt15.get('mean_ic', 0):+.3f}</b><span>IC, BBG Twitter sentiment → fwd 15d ({lt15.get('weeks', 0)}w, hit {lt15.get('hit', 0):.0%}) · {by(lt15)}</span></div>
 <div class="kpi"><b>{lb15.get('mean_ic', 0):+.3f}</b><span>IC, BULL composite → fwd 15d ({lb15.get('weeks', 0)}w, hit {lb15.get('hit', 0):.0%}) · {by(lb15)}</span></div>
</div>
<div class="row"><div class="col"><table id="lbt"></table></div>
<div class="col"><div class="note"><b>Mean IC, forward <span class="hzlab"></span></b></div><svg id="licbar" height="290"></svg>
<div class="note" style="margin-top:10px"><b>Quadrant mean forward <span class="hzlab"></span> relative return</b></div><svg id="lqbar" height="230"></svg></div></div>
<div class="note" style="margin-top:8px"><b>IC through time, forward <span class="hzlab"></span></b> — <span style="color:var(--orange)">■</span> BBG Twitter count Δ · <span style="color:var(--blue)">■</span> BULL composite</div><svg id="licts" height="230"></svg>
<h3>Latest week on the Bloomberg track (week ending {llast})</h3>
<div class="scroll" style="max-height:420px"><table id="ltbl"></table></div>
</section>"""
    ev_payload = None; ev_html = ""
    if events:
        st = events["stats"]; SIG = events["signals"]; OUTS = events["outcomes"]
        # keep only the fields the page needs; per-event list trimmed to the last 120 for the "recent prints" table
        recent = sorted(events["events"], key=lambda e: e["date"], reverse=True)[:120]
        ev_payload = {"stats": st, "signals": SIG, "outcomes": OUTS, "conditional": events["conditional"], "n": events["n_events"], "recent": recent,
                      "own_from": events.get("own_from"), "ss_from": events.get("ss_from")}
        g = lambda k, o: st.get(f"{k}|{o}", {})
        ev_html = f"""
<section><h2>Earnings event windows — {events['n_events']:,} prints, Jan-2024 → Aug-2026</h2>
<div class="note">For every earnings announcement of the 99 names: signals measured over the <b>10 calendar days before</b> the print (vs the prior 30 days as baseline) and outcomes measured from the last close before the print: <b>reaction</b> (to the next close), <b>15 days total</b>, and <b>drift</b> (from the post-print close to day +15). All returns are relative to the equal-weight universe. IC = Spearman across events; Q5−Q1 = top minus bottom quintile mean outcome. Own-corpus signals exist from {events.get('own_from')} (n≈100), sell-side from {events.get('ss_from') or 'n/a'}.</div>
<div class="kpis">
 <div class="kpi"><b>{g('bbg_tone','tot15').get('ic',0):+.3f}</b><span>IC, pre-print Twitter sentiment (BBG) → 15d · Q5−Q1 {g('bbg_tone','tot15').get('q5_q1',0)*100:+.1f}% · n={g('bbg_tone','tot15').get('n',0)}</span></div>
 <div class="kpi"><b>{g('own_att','tot15').get('ic',0):+.3f}</b><span>IC, curated-handle attention into print → 15d · Q5−Q1 {g('own_att','tot15').get('q5_q1',0)*100:+.1f}% · n={g('own_att','tot15').get('n',0)}</span></div>
 <div class="kpi"><b>{g('surprise','react').get('ic',0):+.3f}</b><span>IC, EPS surprise → reaction (the benchmark any signal must be judged against) · n={g('surprise','react').get('n',0)}</span></div>
 <div class="kpi"><b>{g('post_tone_shift','drift').get('ic',0):+.3f}</b><span>IC, post-print sentiment shift (days 0..+3) → drift to +15d · sentiment confirms the move, it does not predict the drift</span></div>
</div>
<h3>Signal × outcome</h3><div class="scroll" style="max-height:none"><table id="evt"></table></div>
<div class="row" style="margin-top:12px"><div class="col"><h3>Attention into the print × result (BBG Twitter attention terciles; beat/miss = EPS surprise beyond ±2%)</h3><div class="scroll" style="max-height:none"><table id="evc"></table></div>
<div class="note" style="margin-top:8px">Read across a row: for the same result, does being "hot" into the print change the payoff? Read down a column: the crowding premium or penalty.</div></div>
<div class="col"><h3>IC by year, 15-day total</h3><div class="scroll" style="max-height:none"><table id="evy"></table></div></div></div>
<h3>Most recent prints with a full 15-day window</h3>
<div class="scroll" style="max-height:380px"><table id="evr"></table></div>
</section>"""
    ll_html = ""
    if leadlag:
        L_ = leadlag["long"]; sp = leadlag["span"]
        lead_sigs = [k for k, v in L_["verdict"].items() if v.startswith("leading")]
        lag_sigs = [k for k, v in L_["verdict"].items() if v.startswith("lagging")]
        coin_sigs = [k for k, v in L_["verdict"].items() if v == "coincident"]
        lab = leadlag["labels"]
        ll_html = f"""
<section><h2>Lead or lag? Cross-correlation of each signal with weekly returns, {sp[0]} → {sp[1]}</h2>
<div class="note">The forward-IC tables above cannot tell a <b>leading</b> signal from sentiment that simply <b>follows price</b>. This section does. For each signal measured at the end of week <i>t</i>, the bars show the rank correlation with the universe-relative return of week <i>t+k</i>: <b>k&lt;0</b> is the return that happened <i>before</i> the signal (sentiment reacting to price), <b>k=0</b> is the same week (coincident), <b>k&gt;0</b> is the return that came <i>after</i> (the signal leading). Weekly returns do not overlap, so each bar's t-stat is honest. The <b>partial IC</b> column repeats the k=+1 test after controlling for the past 4 weeks' return: a signal that is only re-packaged momentum goes to zero there.</div>
<div class="kpis">
 <div class="kpi"><b>{', '.join(lab.get(k, k).split(' (')[0].split(',')[0] for k in lead_sigs) or 'none'}</b><span>classified <b>leading</b> (|IC| at k=+1..+2 is significant and at least as large as the coincident/lagging side)</span></div>
 <div class="kpi"><b>{', '.join(lab.get(k, k).split(' (')[0].split(',')[0] for k in coin_sigs) or 'none'}</b><span>classified <b>coincident</b> (moves with the same week's return)</span></div>
 <div class="kpi"><b>{', '.join(lab.get(k, k).split(' (')[0].split(',')[0] for k in lag_sigs) or 'none'}</b><span>classified <b>lagging</b> (mostly reacts to the return that already happened)</span></div>
</div>
<div id="ccfgrid" class="row"></div>
<h3>The table behind the bars — IC by lag, partial IC at k=+1 after momentum, verdict</h3>
<div class="scroll" style="max-height:none"><table id="cct"></table></div>
<div class="row" style="margin-top:12px"><div class="col"><h3>Regime check — IC at k=+1 by year</h3><div class="scroll" style="max-height:none"><table id="ccy"></table></div></div>
<div class="col"><h3>Reverse direction — does this week's return predict next week's signal?</h3><div class="scroll" style="max-height:none"><table id="ccr"></table></div>
<div class="note" style="margin-top:6px">A large positive number here is the signature of a lagging signal: price moves first, the crowd talks about it afterwards.</div></div></div>
<h3>Double sort — signal tercile inside each momentum tercile → mean forward 15-day relative return</h3>
<div class="note">Rows = past-4-week return tercile, columns = signal tercile. If the signal only proxies momentum the columns look alike inside each row; if it adds information the right column beats the left <i>within</i> rows.</div>
<div id="dsgrid" class="row"></div>
<h3>Own corpus + sell-side, {leadlag['own']['span'][0]} → {leadlag['own']['span'][1]} ({leadlag['own']['weeks']} weeks — indicative only)</h3>
<div class="scroll" style="max-height:none"><table id="cco"></table></div>
</section>"""
    pk_html = ""
    if picks:
        pk_html = f"""
<section><h2>What we would have seen — each week's strongest signals, and what the stock did next</h2>
<div class="note">Every Friday, rank the universe on one signal. The grid shows the <b>top names</b> (upper block) and <b>bottom names</b> (lower block) that week, coloured by the stock's <b>universe-relative return over the following week</b> (or the following 15 days). The curve compounds an equal-weight basket of the top names, of the bottom names, and the long-top / short-bottom spread, rebalanced weekly. Blue = the pick went up relative to the universe, red = it went down. Hover any cell for the name, the signal value and the raw return.</div>
<div class="hzbar"><b>Track</b> <select id="pk_track"><option value="long">Bloomberg, {picks['long']['span'][0]} → {picks['long']['span'][1]}</option><option value="own">Own corpus + sell-side, {picks['own']['span'][0]} → {picks['own']['span'][1]}</option></select>
<b>Signal</b> <select id="pk_sig"></select> <b>N per side</b> <select id="pk_n"><option>3</option><option selected>5</option><option>10</option></select>
<b>Colour by</b> <select id="pk_h"><option value="r1" selected>next week</option><option value="r15">next 15 days</option></select>
<b>Show</b> <select id="pk_win"><option value="13">last 13 weeks</option><option value="26" selected>last 26 weeks</option><option value="52">last 52 weeks</option><option value="all">all</option></select></div>
<div class="kpis" id="pk_kpis"></div>
<div class="legend"><span><i style="background:var(--blue)"></i>top-N basket, cumulative relative return</span><span><i style="background:var(--red)"></i>bottom-N basket</span><span><i style="background:var(--orange)"></i>long top / short bottom spread</span><span>weekly rebalance, equal weight, universe-relative, no costs</span></div>
<svg id="pk_curve" height="260"></svg>
<div id="pk_grid" style="overflow-x:auto;margin-top:10px"></div>
<h3>Every signal on this track at the chosen N — mean next-period relative return of the picks</h3>
<div class="scroll" style="max-height:none"><table id="pk_tbl"></table></div>
</section>"""
    payload = {"weeks": weeks, "panel": panel["panel"], "names": panel["names"], "tickers": panel["tickers"], "backtest": bt, "quadrants": q, "horizons": H,
               "top_handles": panel["top_handles"], "examples": examples, "medHOT": med_hot, "medBULL": med_bull, "long": long_payload, "events": ev_payload,
               "leadlag": leadlag, "picks": picks,
               "ss": ({"since": ss.get("since"), "emails": ss.get("emails"), "matched": ss.get("matched"), "firms": ss.get("firms", [])[:12]} if ss else None)}
    top = lambda key, rev: sorted([(t, r) for t, r in row.items() if r[key] is not None], key=lambda x: (-1 if rev else 1) * x[1][key])[:5]
    a15, b15 = _bt(bt, "att", "15d"), _bt(bt, "BULL", "15d")
    def qv(k, h="15d"): v = q.get(f"{k}|rel_ret_{h}", {}); return f"{v.get('mean', 0)*100:+.2f}% (n={v.get('n', 0)}, hit {v.get('hit', 0):.0%})"
    html = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Sentiment · hot/cold × bull/bear</title>
<style>{CSS}</style>
<div id="tip" class="tip"></div>
<header><h1>Sentiment indicator — hot/cold × bull/bear</h1>
<div class="sub">Generated {panel['asof']} · latest complete week ending <b>{last}</b> · {len(panel['tickers'])} names · own corpus {len(weeks)} weeks since {weeks[0]}{(' · Bloomberg track ' + str(len(long['weeks'])) + ' weeks since ' + long['weeks'][0]) if long else ''} · <a href="index.html">← dashboards hub</a> · rebuild: <code>py _wiki/_tools/build_sentiment.py</code></div>
<div class="kpis">
 <div class="kpi"><b>{panel['tweets_matched']:,}</b><span>tweets mapped to a wiki ticker (of {panel['tweets_scanned']:,} scanned since {daily['start']}, ex-retweets)</span></div>
 <div class="kpi"><b>{a15.get('mean_ic', 0):+.3f}</b><span>IC, own-corpus attention → fwd 15d relative return ({a15.get('weeks', 0)} weeks, hit {a15.get('hit', 0):.0%})</span></div>
 <div class="kpi"><b>{b15.get('mean_ic', 0):+.3f}</b><span>IC, BULL composite → fwd 15d relative return ({b15.get('weeks', 0)} weeks, hit {b15.get('hit', 0):.0%})</span></div>
 <div class="kpi"><b>{qv('hot-bear').split(' ')[0]}</b><span>hot-bear quadrant, mean fwd 15d relative return</span></div>
 <div class="kpi"><b>{qv('hot-bull').split(' ')[0]}</b><span>hot-bull quadrant, mean fwd 15d relative return</span></div>
</div>
<div class="sub">Hottest now: {' · '.join(f"<b>{t}</b> {r_['HOT']:+.1f}" for t, r_ in top('HOT', True))} &nbsp;|&nbsp; Coldest: {' · '.join(f"<b>{t}</b> {r_['HOT']:+.1f}" for t, r_ in top('HOT', False))}<br>
Most bullish: {' · '.join(f"<b>{t}</b> {r_['BULL']:+.1f}" for t, r_ in top('BULL', True))} &nbsp;|&nbsp; Most bearish: {' · '.join(f"<b>{t}</b> {r_['BULL']:+.1f}" for t, r_ in top('BULL', False))}</div>
</header>
<div class="wrap">
<div class="warn">⚠ Read the own-corpus backtest as a <b>first look</b>: 14–17 weekly cross-sections, overlapping forward windows (t-stats overstate independence), one regime (the May–Aug 2026 AI up-leg), lexicon tone (not LLM-scored), and attention measured on the ~440 accounts the twitter-briefing routine follows. The Bloomberg track below is the longer, all-of-X check.</div>

<section><h2>Ranking — week ending <select id="wk"></select></h2>
<div class="legend"><span><i style="background:var(--orange)"></i>HOT z (attention above own trailing 4w)</span><span><i style="background:var(--ink3)"></i>cold</span><span><i style="background:var(--blue)"></i>BULL z</span><span><i style="background:var(--red)"></i>BEAR</span><span>Click a header to sort. z-scores are cross-sectional within the week, clipped ±3.</span></div>
<div class="scroll"><table id="tbl"></table></div><div class="note" id="tblnote"></div></section>

<section><h2>Map — where every name sits this week</h2>
<div class="legend"><span><i style="background:var(--orange)"></i>hot-bull</span><span><i style="background:var(--blue)"></i>cold-bear</span><span><i style="background:var(--ink3)"></i>mixed quadrants</span><span>Hover a dot for the components. Quadrant cuts are the week's medians.</span></div>
<svg id="sc" height="440"></svg></section>

<section><h2>Did it work? Own corpus, May–Aug 2026</h2>
<div class="hzbar"><b>Forward horizon</b> <select id="hz"><option value="1w">1 week</option><option value="15d" selected>15 days</option><option value="4w">4 weeks</option></select> <span class="note">(applies to every chart and the "sel." columns; the table always shows the IC for all three)</span></div>
<div class="row"><div class="col">
<div class="note">Rank IC = Spearman correlation each Friday between the component and the forward <b>universe-relative</b> return (stock minus equal-weight universe mean, local currency). Q5−Q1 = top-quintile minus bottom-quintile mean forward return. Positive IC means "high score → outperformed".</div>
<table id="bt"></table></div>
<div class="col"><div class="note"><b>Mean IC, forward <span class="hzlab"></span></b></div><svg id="icbar" height="260"></svg>
<div class="note" style="margin-top:10px"><b>Quadrant mean forward <span class="hzlab"></span> relative return</b> (hot/cold and bull/bear split at each week's median)</div><svg id="qbar" height="230"></svg></div></div>
<div class="note" style="margin-top:8px"><b>IC through time, forward <span class="hzlab"></span></b> — <span style="color:var(--orange)">■</span> attention · <span style="color:var(--blue)">■</span> BULL composite</div><svg id="icts" height="230"></svg>
<div class="note">Reading so far (15d): attention IC {a15.get('mean_ic', 0):+.3f} (hit {a15.get('hit', 0):.0%}); BULL composite IC {b15.get('mean_ic', 0):+.3f} — the most-upgraded, most-praised names lag. Quadrants at 15d: hot-bear {qv('hot-bear')}, cold-bear {qv('cold-bear')}, hot-bull {qv('hot-bull')}, cold-bull {qv('cold-bull')}.</div>
</section>
{long_html}
{pk_html}
{ll_html}
{ev_html}
<section><h2>Ticker explorer — <select id="tk"></select></h2>
<svg id="tkc" height="420"></svg><div id="tkinfo"></div></section>

<section><details><summary>Methodology, sources and what is deliberately left out</summary>
<dl>
<dt>Own tweet corpus</dt><dd>twitter-briefing routine (daily 09:00, twitterapi.io) → <code>E:\\.claude\\data\\twitter-briefing\\tweets.sqlite</code>. ~440 handles curated by the briefing skill (semis, micro, AI/ML, hedge funds, wires). Retweets dropped; replies and quotes kept. Dense coverage from May 2026 only — earlier months are not backfilled (decision 2026-09-02).</dd>
<dt>Bloomberg track</dt><dd>bdh fields TWITTER_SENTIMENT_DAILY_AVG, TWITTER_PUBLICATION_COUNT, TWITTER_POS/NEG_SENTIMENT_COUNT, NEWS_SENTIMENT_DAILY_AVG, NEWS_PUBLICATION_COUNT since 2023-12 for every name with a Bloomberg line. Bloomberg's own classifier; coverage of non-US lines is thinner.</dd>
<dt>Ticker mapping (own corpus)</dt><dd>Cashtag ($NVDA) or company-name alias (case-sensitive for ambiguous names: Apple, Meta, Oracle, Arm Holdings, Samsung…). A tweet naming N tickers gives each 1/N (N≤3) or 0.25/N (lists). Private names (OpenAI, Anthropic, Cerebras) excluded — no price.</dd>
<dt>Attention (HOT)</dt><dd>log((count this week + 0.5) / (mean of trailing 4 weeks + 0.5)), curated and wire (or BBG Twitter and BBG news) separately; each z-scored across names; HOT = mean of the two z. Needs ≥2 prior weeks.</dd>
<dt>Tone</dt><dd>Own corpus: finance lexicon (~80 bull / ~100 bear stems, 3-word negation flip), per tweet in [−1,1]; weekly engagement-weighted mean, shrunk by n/(n+5). <b>Not LLM-scored</b> — the upgrade path. Bloomberg track: count-weighted weekly mean of the daily sentiment score.</dd>
<dt>BULL composite</dt><dd>Mean z of: tone, tone change vs trailing 4w, Bloomberg BEST_EPS (1BF) 4-week % revision (|Δ|>25% dropped as fiscal-roll artefacts), BEST_ANALYST_RATING 4-week drift (Bloomberg track adds news sentiment). Short interest is a separate crowding leg.</dd>
<dt>Returns & horizons</dt><dd>PX_LAST Friday closes, local currency; forward 1w / 15d / 4w (calendar days); backtest uses universe-relative returns. Non-USD names carry FX noise in raw returns. Forward windows overlap week to week, so treat t-stats as indicative.</dd>
<dt>Sell-side e-mails</dt><dd>Outlook desktop over COM, store-side DASL filter on ~65 broker sender domains, subject + body (bodies fetched by EntryID, URLs stripped, text cut at the first disclaimer marker, first ~6k chars scanned for tickers; tone and actions read in ±250-char windows around each ticker mention; rating changes from "Rating: From X to Y" / "upgrade to" patterns, PT changes from "Price target: From $A to $B" / "PT to $B from $A", estimate direction from "raising/lowering estimates"), all mail folders except deleted/junk/sent. Mailbox retention starts 2026-01-31, so this leg covers Feb-2026 onward. Ticker mapping = cashtag / alias / ticker token (short tickers need parentheses or a "US" suffix); tone = the same lexicon; actions = upgrade/downgrade/PT raise/cut regex on the subject; noise (webinars, invites, corporate access) dropped. Blast e-mails naming N tickers weight 1/N.</dd>
<dt>Lead/lag test</dt><dd>Cross-correlation function on weekly non-overlapping universe-relative returns: IC(k) = mean over weeks of Spearman(signal at week t, return of week t+k), k = −4…+4. Partial IC = Spearman partial correlation controlling for the past-4-week return. Double sort = tercile × tercile on the same week. Verdict rule: leading if |IC(+1,+2)| is significant (|t|≥2) and ≥60% of the larger of the coincident/lagging sides; lagging if the k&lt;0 side dominates; coincident if k=0 dominates. Signals built with a trailing window (attention, tone change, EPS revision) mechanically embed weeks t−4…t, so their k&lt;0 bars partly reflect construction.</dd>
<dt>Event windows</dt><dd>Announcement dates, times and EPS actual/estimate from Bloomberg EARN_ANN_DT_TIME_HIST_WITH_EPS. After-close prints (or no time) use the day's close as base; pre-market prints use the prior close. Pre-window = 10 calendar days, baseline = the 30 days before that. Outcomes relative to an equal-weight index of the 99 names. |surprise| > 100% and |EPS revision| > 25% dropped as artefacts.</dd>
<dt>Not yet in</dt><dd>Corpus report tone, house-tone leg from reconciliation deltas and the outcomes ledger, options skew / 13F positioning, LLM tone scorer, Jan–Apr 2026 own-corpus backfill.</dd>
<dt>Files</dt><dd><code>_wiki/_data/sentiment/</code>: tweet_daily.json · bbg_history.json · bbg_long.json · panel_weekly.json · panel_long.json; builder <code>_wiki/_tools/build_sentiment.py</code> (steps tweets, bbg, bbglong, panel, long, dash; <code>--no-bbg</code> reuses cached history).</dd>
</dl></details></section>
</div>
<script>window.__SENT__ = {json.dumps(payload, ensure_ascii=False).replace('</', '<\\/')};</script>
<script>{JS}</script>
"""
    return html
