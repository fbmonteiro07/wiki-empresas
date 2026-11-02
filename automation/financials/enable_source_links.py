from pathlib import Path
p=Path('E:/.claude/scripts/build_wiki_html.py');s=p.read_text(encoding='utf-8')
assert 'def financials_source_links(' not in s
s=s.replace('import json\n','import json\nimport posixpath\nfrom urllib.parse import urlsplit, urlunsplit, unquote\n',1)
needle='ROOT = WIKI.parent\n'
addition='''ROOT = WIKI.parent

# Public provenance for Financials; keep local copies usable in offline file mode.
_source_inventory = WIKI / "_data" / "financials" / "source_inventory.json"
FINANCIALS_SOURCES = {}
if _source_inventory.is_file():
    for _record in json.loads(_source_inventory.read_text(encoding="utf-8-sig")).get("records", []):
        for _key in ("path", "text_path", "original_path"):
            if _record.get(_key):
                FINANCIALS_SOURCES[_record[_key].replace("\\\\", "/")] = _record


def financials_source_links(body):
    def link(match):
        href = html.unescape(match.group(1))
        url = urlsplit(href)
        if url.scheme or url.netloc or href.startswith(("/", "#")):
            return match.group(0)
        path = posixpath.normpath(posixpath.join("_wiki", unquote(url.path)))
        source = FINANCIALS_SOURCES.get(path)
        if not source:
            return match.group(0)
        public = source.get("source_url")
        if not public or urlsplit(public).scheme not in ("http", "https"):
            public = "_dashboards/financials-sources.html#" + source["ticker"]
        return match.group(0) + ' data-public-url="' + html.escape(public, quote=True) + '"'
    return re.sub(r'<a href="([^"]+)"', link, body)


def rebase_theme_links(body):
    def link(match):
        href = html.unescape(match.group(1))
        url = urlsplit(href)
        if url.scheme or url.netloc or href.startswith(("/", "#", "?")):
            return match.group(0)
        path = posixpath.normpath(posixpath.join("themes", url.path))
        rebased = urlunsplit((url.scheme, url.netloc, path, url.query, url.fragment))
        return '<a href="' + html.escape(rebased, quote=True) + '"'
    return re.sub(r'<a href="([^"]+)"', link, body)
'''
assert s.count(needle)==1;s=s.replace(needle,addition)
old='        files.append((m.group(1) if m else "", f))'
new='''        source = FINANCIALS_SOURCES.get(f.relative_to(ROOT).as_posix(), {})
        files.append((source.get("date") or (m.group(1) if m else ""), f))'''
assert s.count(old)==1;s=s.replace(old,new)
old='        themes[s]["html"] = rewrite(themes[s]["html"])';new='        themes[s]["html"] = rebase_theme_links(rewrite(themes[s]["html"]))';assert s.count(old)==1;s=s.replace(old,new)
old='    tpl = r"""<!DOCTYPE html>';new='    page_divs = [financials_source_links(body) for body in page_divs]\n\n'+old;assert s.count(old)==1;s=s.replace(old,new)
old='// Direct page links preserve the existing layout and let source inventories return to an issuer.'
new='''// The LAN server intentionally excludes raw archives; use original publisher sources there.
if(location.protocol==='http:' || location.protocol==='https:'){
  document.querySelectorAll('a[data-public-url]').forEach(function(a){a.href=a.dataset.publicUrl;});
}
'''+old
assert s.count(old)==1;s=s.replace(old,new)
compile(s,str(p),'exec')
Path('automation/financials/build_wiki_html_before_source_links.py').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
p.write_text(s,encoding='utf-8')
print('Added publisher links for LAN browsing, local source links for offline use, dated IR calls and theme-relative links.')
