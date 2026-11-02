from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
for t in sys.argv[1:]:
 s=(Path('_wiki')/(t+'.md')).read_text(encoding='utf-8')
 print('\n===== '+t+' =====')
 for part in s.split('\n## '):
  if part.startswith(('Debate / thesis','Intra-quarter','Changelog')):print('\n## '+part)
