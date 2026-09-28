import concurrent.futures
import hashlib
import json
import pathlib
import ssl
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent
CONTEXT = ssl.create_default_context()
CONTEXT.verify_flags &= ~ssl.VERIFY_X509_STRICT

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.extend(v for k, v in attrs if k == 'href')

def fetch(i):
    msg = json.loads((ROOT / f'email_core_{i}.json').read_text(encoding='utf-8'))
    parser = Links()
    body = msg['body']
    parser.feed(body['content'] if isinstance(body, dict) else body)
    url = next(u for u in parser.links if ('/eqr/article/' in u if i < 3 else '/Article?' in u))
    url = url.replace(' ', '%20')
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(request, timeout=40, context=CONTEXT) as response:
            payload = response.read()
            mime = response.headers.get('Content-Type', '')
            final_url = response.url
        ext = '.pdf' if payload.startswith(b'%PDF-') else '.html'
        dest = ROOT / f'report_response_{i}{ext}'
        dest.write_bytes(payload)
        result = {'email': i, 'title': msg['subject'], 'source_url': url, 'final_url': final_url, 'mime': mime, 'bytes': len(payload), 'file': str(dest), 'sha256': hashlib.sha256(payload).hexdigest()}
    except Exception as error:
        result = {'email': i, 'title': msg['subject'], 'source_url': url, 'error': str(error)}
    (ROOT / f'download_{i}.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(fetch, [1, 2, 3]):
            print(json.dumps(result))
