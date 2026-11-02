import subprocess
from pathlib import Path
p=Path('KKR/research');stem='2026-08-31_USI_investor_presentation'
subprocess.run([r'C:\Users\Felipe.monteiro\AppData\Local\Programs\Git\mingw64\bin\pdftotext.exe','-layout','-enc','UTF-8',str(p/(stem+'.pdf')),str(p/(stem+'.txt'))],check=True,capture_output=True)
s=(p/(stem+'.txt')).read_text(encoding='utf-8')
assert '$3.3' in s and '$2.0' in s and '17 billion' in s
url='https://ir.kkr.com/media/document/755d2777-015d-49f3-8dfb-3b0120c6d49b/assets/USI_Investor_Presentation.pdf?disposition=inline'
(p/(stem+'.md')).write_text(f'# KKR - sale of USI to Aon transaction presentation\n\n- Publication date: 2026-08-31\n- Original URL: {url}\n- Retrieved: 2026-11-01\n- Fidelity: Full PDF text extraction; transaction and capital-allocation pages reviewed.\n\n## Source text\n\n{s}',encoding='utf-8')
print('Transaction presentation extracted; conditional proceeds and ANI figures present.')
