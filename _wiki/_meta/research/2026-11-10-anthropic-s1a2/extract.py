import re, sys, html
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8', errors='replace').read()
t = re.sub(r'(?is)<(script|style).*?</\1>', ' ', t)
t = re.sub(r'(?i)</t[dh]>', ' | ', t)
t = re.sub(r'(?i)</tr>', '\n', t)
t = re.sub(r'(?i)<br\s*/?>', '\n', t)
t = re.sub(r'(?i)</(p|div|h\d|li|table)>', '\n', t)
t = re.sub(r'(?s)<[^>]+>', '', t)
t = html.unescape(t).replace('\xa0', ' ')
out = []
for line in t.split('\n'):
    line = re.sub(r'[ \t]+', ' ', line).strip()
    line = re.sub(r'(\|\s*)+\|', '|', line)
    line = re.sub(r'\$\s*\|\s*', '$', line)
    line = re.sub(r'\|\s*\)', ')', line)
    line = re.sub(r'\|\s*%', '%', line)
    if line.strip(' |'):
        out.append(line)
open(dst, 'w', encoding='utf-8').write('\n'.join(out))
print(dst, len(out))
