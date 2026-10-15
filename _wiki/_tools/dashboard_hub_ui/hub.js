(function(){
  'use strict';
  var root=document.documentElement, KEY='wiki-dash-theme', btn=document.querySelector('.or-theme');
  function syncTheme(){var dark=root.dataset.theme==='dark';btn.setAttribute('aria-pressed',String(dark));btn.setAttribute('aria-label',dark?'Switch to light theme':'Switch to dark theme');document.getElementById('theme-label').textContent=dark?'Light mode':'Dark mode';}
  if(btn){syncTheme();btn.addEventListener('click',function(){syncTheme();try{localStorage.setItem(KEY,root.dataset.theme||'dark');}catch(e){}});}
  var q=document.getElementById('q');if(!q)return;
  var cards=[].slice.call(document.querySelectorAll('.hub-card')), secs=[].slice.call(document.querySelectorAll('.hub-section')), groups=[].slice.call(document.querySelectorAll('.hub-group'));
  var clear=document.getElementById('clear-search'), count=document.getElementById('search-count'), details=document.getElementById('show-details'), autoOpened={};
  function normalize(text){return text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[._/\-]+/g,' ');}
  function apply(){
    var t=normalize(q.value.trim()), matches=0;
    cards.forEach(function(c){var hidden=!!t&&normalize(c.getAttribute('data-s')).indexOf(t)<0;c.classList.toggle('hidden',hidden);if(!hidden)matches++;});
    groups.forEach(function(g){g.classList.toggle('hidden',!g.querySelector('.hub-card:not(.hidden)'));});
    secs.forEach(function(s){
      var any=s.querySelector('.hub-card:not(.hidden)');s.classList.toggle('hidden',!any);
      if(s.tagName!=='DETAILS')return;
      if(t&&any&&!s.open){s.open=true;autoOpened[s.id]=true;}
      if(!t&&autoOpened[s.id]){s.open=false;delete autoOpened[s.id];}
    });
    clear.hidden=!t;count.textContent=t?matches+' matches':cards.length+' dashboard links';
    document.getElementById('no-results').hidden=matches!==0;
    window.dispatchEvent(new Event('scroll'));
  }
  q.addEventListener('input',apply);clear.addEventListener('click',function(){q.value='';apply();q.focus();});
  details.addEventListener('click',function(){var show=document.body.classList.toggle('hub-show-details');details.setAttribute('aria-pressed',String(show));details.textContent=show?'Hide details':'Show details';});
  document.addEventListener('keydown',function(ev){if(ev.key==='/'&&!ev.ctrlKey&&!ev.metaKey&&!ev.altKey&&!ev.target.closest('input,textarea,select,[contenteditable="true"]')){ev.preventDefault();q.focus();}if(ev.key==='Escape'&&document.activeElement===q){q.value='';apply();}});
  function openHash(){try{var d=document.getElementById(location.hash.slice(1));if(d&&d.tagName==='DETAILS')d.open=true;}catch(e){}}
  window.addEventListener('hashchange',openHash);openHash();apply();
})();
