from pathlib import Path

dash=Path(r'E:\Wiki Felipe empresas\_wiki\_dashboards')
source=(dash/'market-breadth.html').read_text(encoding='utf-8')
for theme in ('light','dark'):
    value=source.replace('<html lang="en" data-visualize-standalone>',f'<html lang="en" data-visualize-standalone data-theme="{theme}">')
    value=value.replace('&lt;html lang=&quot;en&quot; data-visualize-standalone&gt;',f'&lt;html lang=&quot;en&quot; data-visualize-standalone data-theme=&quot;{theme}&quot;&gt;')
    value=value.replace('color-scheme:light dark',f'color-scheme:{theme}')
    value=value.replace('color-scheme: light dark',f'color-scheme: {theme}')
    (dash/f'market-breadth-qa-{theme}.html').write_text(value,encoding='utf-8')
