from pathlib import Path
p=Path('E:/.claude/scripts/build_wiki_html.py');s=p.read_text(encoding='utf-8');assert '// Direct page links' not in s
old="  if(el){el.style.display='block';\n";new="  if(el){el.style.display='block';\n    if(location.hash !== '#'+t){history.replaceState(null,'','#'+encodeURIComponent(t));}\n";assert s.count(old)==1;s=s.replace(old,new,1)
old='</script></body></html>"""';new='''// Direct page links preserve the existing layout and let source inventories return to an issuer.
function openLinkedPage(){
  var t;
  try{t=decodeURIComponent(location.hash.slice(1));}catch(e){return;}
  if(t && document.getElementById('p-'+t)){show(t);}
}
window.addEventListener('hashchange',openLinkedPage);
openLinkedPage();
</script></body></html>"""''';assert s.count(old)==1;s=s.replace(old,new,1)
backup=Path('automation/financials/build_wiki_html_before_links.py');backup.write_text(p.read_text(encoding='utf-8'),encoding='utf-8');p.write_text(s,encoding='utf-8')
print('Enabled direct issuer/theme links in the existing HTML builder; layout unchanged.')
