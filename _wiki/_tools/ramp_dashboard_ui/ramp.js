(()=>{
 'use strict';
 const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 const theme=$('#ramp-theme');
 function syncTheme(){const dark=document.documentElement.dataset.theme==='dark';theme.textContent=dark?'◐ Light mode':'◐ Dark mode';theme.setAttribute('aria-pressed',String(dark));theme.setAttribute('aria-label','Switch to '+(dark?'light':'dark')+' theme');}
 theme.addEventListener('click',()=>{document.documentElement.dataset.theme=document.documentElement.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('capstone-ramp-theme',document.documentElement.dataset.theme);}catch{}syncTheme();});syncTheme();
 const panels=$$('.ramp-panel'),last={adoption:'adoption',models:'prov',spending:'spend',tokens:'tokens',sources:'basis'};
 const groups=Object.fromEntries(panels.map(p=>[p.id,p.dataset.group]));
 function resolve(hash){const target=document.getElementById(hash),panel=target?.closest('.ramp-panel');return panel?{panel,target}:{panel:$('#adoption'),target:$('#adoption')};}
 function show(id,scroll=false){
  const {panel,target}=resolve(id),group=panel.dataset.group;last[group]=panel.id;
  panels.forEach(p=>p.hidden=p!==panel);
  // On narrow screens, begin at the latest observation; retain subsequent user scrolling.
  requestAnimationFrame(()=>panel.querySelectorAll('.chart-wrap').forEach(w=>{if(!w.dataset.positioned&&w.scrollWidth>w.clientWidth+1){w.scrollLeft=w.scrollWidth-w.clientWidth;w.dataset.positioned='true';}}));
  $$('.ramp-tabs a').forEach(a=>{if(a.dataset.group===group)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  $$('.ramp-subnav a').forEach(a=>{a.hidden=a.dataset.group!==group;if(a.hash==='#'+panel.id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  $$('.tile[data-target]').forEach(t=>t.setAttribute('aria-current',String(t.dataset.target===panel.id)));
  if(typeof hide==='function')hide();
  if(target!==panel){let p=target;while(p&&p!==panel){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}if(scroll)target.scrollIntoView({block:'start'});}
  else if(scroll)window.scrollTo({top:0,behavior:'instant'});
 }
 document.addEventListener('click',event=>{
  const group=event.target.closest('.ramp-tabs a'),tile=event.target.closest('.tile[data-target]'),anchor=event.target.closest('a[href^="#"]');
  let id=group?last[group.dataset.group]:tile?tile.dataset.target:anchor?.hash.slice(1);
  if(id&&document.getElementById(id)?.closest('.ramp-panel')){event.preventDefault();history.pushState(null,'','#'+id);show(id,true);if(anchor?.classList.contains('skip-link')){const chart=$('#'+id+' svg.chart');chart?.focus();chart?.scrollIntoView({block:'center'});}}
 });
 $$('.tile[data-target]').forEach(t=>t.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();t.click();}}));
 const fromHash=()=>show(location.hash.slice(1));window.addEventListener('hashchange',fromHash);window.addEventListener('popstate',fromHash);fromHash();
 const snapshotIds=['adoption','vendor','sshare','prov','ladder','vintage','tokens'];
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const value=v=>Number.isFinite(v)?v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})+'%':'—';
 for(const id of snapshotIds){
  const panel=document.getElementById(id),hit=panel.querySelector('.hit'),chart=hit&&CHARTS[hit.dataset.c];
  if(!chart||chart.unit!=='%'||chart.dates.length<2)continue;
  const n=chart.dates.length-1,latest=chart.dates[n],previous=chart.dates[n-1];
  const box=document.createElement('div');box.className='snapshot';box.dataset.chart=hit.dataset.c;
  let html='<h3>Latest observations · '+esc(latest)+'</h3><table><thead><tr><th scope="col">Series</th><th scope="col" class="r">'+esc(latest)+'</th><th scope="col" class="r">'+esc(previous)+'</th><th scope="col" class="r">Change <span class="delta-label">percentage points</span></th></tr></thead><tbody>';
  chart.rows.forEach(r=>{const now=r.v[n],prior=r.v[n-1],change=Number.isFinite(now)&&Number.isFinite(prior)?now-prior:null,rounded=change===null?null:Number(change.toFixed(2));
   const delta=rounded===null?'—':(rounded>0?'+':rounded<0?'−':'')+Math.abs(rounded).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
   html+='<tr><td><i class="series-key" style="background:'+esc(r.c)+'"></i>'+esc(r.n)+'</td><td class="r">'+value(now)+'</td><td class="r">'+value(prior)+'</td><td class="r '+(rounded>0?'positive':rounded<0?'negative':'delta-neutral')+'">'+delta+'</td></tr>';});
  box.innerHTML=html+'</tbody></table>';
  const chartWrap=hit.closest('.chart-wrap');let after=chartWrap?.nextElementSibling;if(!after?.classList.contains('lg'))after=chartWrap;
  if(after)after.after(box);
 }
 // Keep the original hover data and crosshair; also support keyboard and touch.
 $$('.ramp-panel svg.chart').forEach(svg=>{
  if(!svg.querySelector('.hit'))return;svg.setAttribute('tabindex','0');svg.setAttribute('aria-describedby','chart-keyboard-help');
  svg.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End','Escape'].includes(e.key))return;e.preventDefault();if(e.key==='Escape'){hide();return;}
   const hits=[...svg.querySelectorAll('.hit')],old=svg.dataset.cursor===undefined?hits.length-1:Number(svg.dataset.cursor);
   const index=e.key==='Home'?0:e.key==='End'?hits.length-1:Math.max(0,Math.min(hits.length-1,old+(e.key==='ArrowRight'?1:-1)));svg.dataset.cursor=index;
   const hit=hits[index];hit.scrollIntoView({block:'nearest',inline:'nearest'});const rect=hit.getBoundingClientRect();hide();hit.dispatchEvent(new MouseEvent('mousemove',{bubbles:true,clientX:rect.x+rect.width/2,clientY:Math.max(12,rect.y+rect.height/2)}));
  });svg.addEventListener('blur',()=>hide());
 });
 document.addEventListener('pointerdown',e=>{if(e.pointerType!=='touch'||!e.target.classList?.contains('hit'))return;e.target.dispatchEvent(new MouseEvent('mousemove',{bubbles:true,clientX:e.clientX,clientY:e.clientY}));});
 window.addEventListener('scroll',()=>hide(),{passive:true});
})();
