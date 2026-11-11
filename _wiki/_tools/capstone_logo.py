"""Capstone symbol for the dashboard shells.

Every dashboard shell (hub, OpenRouter, sentiment, fin, Ramp, DC delay, credit monitor, Aterio hyperscalers) draws a
"C" badge as `<span class="...brand-mark">C</span>`. `apply(html)` swaps that badge for the Capstone symbol
(_data/openrouter/assets/capstone-logo.png, the logo of the deck pipelines), inlined as a data URI so the page stays one
self-contained file. Idempotent: a page that already carries the logo comes back unchanged. Stdlib only.
"""
from __future__ import annotations

import base64
import re
from pathlib import Path

LOGO = Path(__file__).resolve().parents[1] / "_data" / "openrouter" / "assets" / "capstone-logo.png"
_BADGE = re.compile(r"""<span class=(["'])([\w-]*brand-mark)\1[^>]*>C</span>""")
# the badge classes set a box with a border and a letter; the image keeps the box size and drops the rest.
# On the navy sidebars the symbol is a touch brighter and a little larger than the old letter box.
CSS = ("<style>img.cap-logo{display:block;object-fit:contain;border:0!important;border-radius:0!important;padding:0!important;"
       "background:none!important;flex:none}"
       ".or-sidebar img.cap-logo,.side img.cap-logo{width:36px!important;height:36px!important;filter:brightness(1.35)}</style>")
_uri: str | None = None


def uri() -> str:
    global _uri
    if _uri is None:
        _uri = "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode("ascii")
    return _uri


def apply(html: str) -> str:
    if not _BADGE.search(html):
        return html
    u = uri()
    html = _BADGE.sub(lambda m: f'<img class="{m[2]} cap-logo" src="{u}" alt="" aria-hidden="true">', html)
    return html.replace("</head>", CSS + "</head>", 1) if "</head>" in html else CSS + html


if __name__ == "__main__":   # one-off: patch already-built pages in place, e.g. py capstone_logo.py ../_dashboards/x.html
    import sys
    for p in sys.argv[1:]:
        f = Path(p); s = f.read_text(encoding="utf-8"); t = apply(s)
        if t != s:
            f.write_bytes(t.encode("utf-8"))
        print(("patched  " if t != s else "no badge ") + str(f))
