"""Render the wiki dashboards hub (_dashboards/index.html) from the hand-edited
registry _data/dashboards.json, in the OpenRouter dashboard's presentation shell
(sidebar + sticky topbar + Jakarta face + light/dark theme), imported from
openrouter_presentation.py so the two pages stay visually in sync.

Page order: overview (headline + tiles) → 00 Home base (comp sheet, panels,
modelos, the wiki itself) → 01 Temático (thematic groups, e.g. Memória) →
filter → Daily · Weekly · On demand · Explainers · Archive (collapsed) →
Unregistered (only when something on disk has no card).

Cards come from two surfaces:
  * wiki dashboards — files under _dashboards (registry `cards`), dated by mtime;
  * the Capstone hub — the Capstone-Wiki clone served at /dashboards/ on the LAN
    server (registry `hub.cards`), dated by the clone's file mtime when the clone
    is reachable (P: / UNC), tagged "Capstone hub".
Mirrors of wiki pages inside the clone are listed in `hub.skipped` with a reason
and are neither carded nor reported as unregistered.

A thematic group (registry `themes.groups[].members`, wiki hrefs or "hub:<path>")
pulls its cards out of the cadence sections; the card keeps its cadence badge,
date and stale rule, it just lives with its theme.

Each card shows: last-updated date (file mtime, or a fixed `asof`), cadence pill,
topic, the routine that rebuilds it and a STALE flag (daily > N business days,
weekly > N days; thresholds in the registry).

stdlib only. Writes ONLY _dashboards/index.html. Run standalone or as the last
step of refresh_features.py.
"""
from __future__ import annotations

import base64
import datetime as dt
import html
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
WIKI = TOOLS.parent
DASH = WIKI / "_dashboards"
REG = WIKI / "_data" / "dashboards.json"
OUT = DASH / "index.html"
FONT = WIKI / "_data" / "openrouter" / "assets" / "plus-jakarta-sans.woff2"
TODAY = dt.date.today()

sys.path.insert(0, str(TOOLS))
from openrouter_presentation import CSS as OR_CSS, JS as OR_JS  # noqa: E402  shared shell (theme vars, sidebar, topbar, tiles)

CADENCE_LABEL = {"daily": "daily", "weekly": "weekly", "ondemand": "on demand",
                 "explainer": "explainer", "archive": "snapshot", "unregistered": "unregistered"}
TILE_COLOR = {"daily": "var(--accent)", "weekly": "var(--s1)", "ondemand": "var(--s4)",
              "explainer": "var(--s3)", "archive": "var(--base)", "themes": "var(--s5)"}

HUB_CSS = r"""
.hub-overview .oc-tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;margin:24px 0 20px}

@media(max-width:1300px){.hub-overview .oc-tiles{grid-template-columns:repeat(4,minmax(0,1fr))}}

@media(max-width:600px){.hub-overview .oc-tiles{grid-template-columns:repeat(2,minmax(0,1fr))!important}}

.oc-tile .l i{width:8px;height:8px;border-radius:50%;display:inline-block;background:var(--c);margin-right:7px;vertical-align:1px}

.oc-tile.is-crit .v{color:var(--crit)}.oc-tile.is-good .v{color:var(--good)}

.hub-filter{margin:4px 0 8px}

.hub-filter input{width:100%;padding:12px 16px;font:inherit;font-size:13px;color:var(--ink);background:var(--surf);border:1px solid var(--border);border-radius:10px;box-shadow:var(--shadow)}

.hub-filter input::placeholder{color:var(--muted)}

.hub-section{margin-top:44px}.hub-section .oc-kicker{display:block}

.hub-section>h2,.hub-section>summary h2{margin:0 0 6px}.hub-section .sub{display:block;margin-bottom:18px}

.hub-home{margin-top:8px;margin-bottom:36px}

.hub-themes{margin-top:8px;margin-bottom:36px}

.hub-group{margin-top:22px;padding-top:18px;border-top:1px solid var(--grid)}

.hub-group:first-of-type{margin-top:0;padding-top:0;border-top:0}

.hub-group-title{margin:0 0 4px;font-size:17px;font-weight:650;letter-spacing:-.35px}

.hub-group-title small{font-weight:500;color:var(--muted);font-size:11px;margin-left:8px;font-variant-numeric:tabular-nums}

.hub-group-sub{display:block;font-size:12px;color:var(--ink2);line-height:1.7;margin:0 0 14px;max-width:1050px}

.hub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}

.hub-grid.hub-grid-home{grid-template-columns:repeat(2,minmax(0,1fr))}

.hub-grid-home .hub-card{padding:24px 26px;border-color:color-mix(in srgb,var(--accent) 35%,var(--border))}

.hub-grid-home .hub-card h3{font-size:19px;letter-spacing:-.5px}

.hub-grid-home .hub-card p{font-size:13px}

@media(max-width:760px){.hub-grid.hub-grid-home{grid-template-columns:1fr}}

@media(max-width:600px){.hub-grid{grid-template-columns:1fr}}

.hub-card{display:flex;flex-direction:column;gap:9px;min-width:0;background:var(--surf);border:1px solid var(--border);border-radius:12px;padding:20px 22px;box-shadow:var(--shadow);text-decoration:none!important;color:var(--ink);transition:border-color .15s,transform .15s}

.hub-card:hover{border-color:var(--accent);transform:translateY(-1px)}

.hub-card.is-stale{border-left:3px solid var(--crit)}

.hub-card h3{margin:0;font-size:15px;font-weight:650;letter-spacing:-.25px;line-height:1.35;color:var(--ink)}

.hub-card p{margin:0;font-size:12px;line-height:1.7;color:var(--ink2)}

.hub-top{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font-size:10px;font-weight:650;letter-spacing:.65px;text-transform:uppercase;color:var(--muted)}

.hub-meta{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:center;margin-top:auto;padding-top:10px;border-top:1px solid var(--grid);font-size:11px;color:var(--muted);font-variant-numeric:tabular-nums}

.hub-routine{overflow-wrap:anywhere}.hub-routine::before{content:'\21BB  ';color:var(--base)}

.pill{display:inline-block;padding:1px 8px;border-radius:9px;font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;line-height:1.7}

.pill.cad-daily{background:color-mix(in srgb,var(--accent) 14%,var(--surf));color:var(--accent)}

.pill.cad-weekly{background:color-mix(in srgb,var(--s1) 14%,var(--surf));color:var(--s1)}

.pill.cad-ondemand{background:color-mix(in srgb,var(--s4) 18%,var(--surf));color:var(--s4)}

.pill.cad-explainer{background:color-mix(in srgb,var(--s3) 18%,var(--surf));color:var(--s3)}

.pill.cad-archive{background:var(--grid);color:var(--ink2)}

.pill.cad-unregistered,.hub-stale{background:color-mix(in srgb,var(--crit) 14%,var(--surf));color:var(--crit)}

.hub-stale{padding:1px 8px;border-radius:9px;font-weight:700}

.hub-file{border:1px dashed var(--base);border-radius:5px;padding:0 6px}

.hub-surface{border:1px solid color-mix(in srgb,var(--s1) 45%,var(--border));color:var(--s1);border-radius:5px;padding:0 6px}

details.hub-section{background:transparent;border:0;border-radius:0;padding:0;margin-top:44px;font-size:inherit}

details.hub-section>summary{list-style:none;cursor:pointer;font-weight:inherit;color:inherit}

details.hub-section>summary::-webkit-details-marker{display:none}

details.hub-section>summary h2::before{content:'\25B8  ';color:var(--muted)}details[open].hub-section>summary h2::before{content:'\25BE  '}

.hub-unreg h2,.hub-unreg .oc-kicker{color:var(--crit)}

.hub-credit{margin-top:44px;font-size:10px;color:var(--muted);line-height:1.8;border-top:1px solid var(--grid);padding-top:14px;overflow-wrap:anywhere}

.hub-credit code{background:var(--grid);padding:1px 5px;border-radius:4px}

.or-nav-count{margin-left:auto;font-size:10px;color:#7791a8;font-variant-numeric:tabular-nums}

.or-navigation a[aria-current=location] .or-nav-count{color:#8bd5c3}

.or-navigation a.or-nav-sub{padding-left:38px;font-size:11px;margin-top:-2px}

.or-sidebar-footer a+a{margin-top:8px}

.hidden{display:none!important}

@media(max-width:1020px){.or-navigation a.or-nav-sub{padding-left:12px}}
"""

HUB_JS = r"""
(function(){

  var root=document.documentElement, KEY='wiki-dash-theme';

  var btn=document.querySelector('.or-theme');

  if(btn){

    var isDark=root.dataset.theme==='dark';

    btn.setAttribute('aria-pressed',String(isDark));btn.setAttribute('aria-label',isDark?'Switch to light theme':'Switch to dark theme');

    btn.addEventListener('click',function(){try{localStorage.setItem(KEY,root.dataset.theme||'light');}catch(e){}});

  }

  var q=document.getElementById('q');if(!q)return;

  var cards=[].slice.call(document.querySelectorAll('.hub-card'));

  var secs=[].slice.call(document.querySelectorAll('.hub-section'));

  var groups=[].slice.call(document.querySelectorAll('.hub-group'));

  var autoOpened={};

  function apply(){

    var t=q.value.trim().toLowerCase();

    cards.forEach(function(c){c.classList.toggle('hidden',!!t&&c.getAttribute('data-s').indexOf(t)<0);});

    groups.forEach(function(g){g.classList.toggle('hidden',!g.querySelector('.hub-card:not(.hidden)'));});

    secs.forEach(function(s){

      var any=s.querySelector('.hub-card:not(.hidden)');

      s.classList.toggle('hidden',!any);

      if(s.tagName!=='DETAILS')return;

      if(t&&any&&!s.open){s.open=true;autoOpened[s.id]=true;}

      if(!t&&autoOpened[s.id]){s.open=false;delete autoOpened[s.id];}

    });

  }

  q.addEventListener('input',apply);

  function openHash(){try{var d=document.getElementById(location.hash.slice(1));if(d&&d.tagName==='DETAILS')d.open=true;}catch(e){}}

  window.addEventListener('hashchange',openHash);openHash();

})();
"""


def bdays_after(d0: dt.date, d1: dt.date) -> int:
    """Weekdays in (d0, d1]."""
    n, d = 0, d0
    while d < d1:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def file_date(p: Path) -> dt.date:
    return dt.datetime.fromtimestamp(p.stat().st_mtime).date()


def stale_note(cadence: str, updated: dt.date | None, rules: dict) -> str | None:
    if updated is None:
        return None
    if cadence == "daily":
        lim = int(rules.get("daily", {}).get("business_days", 2))
        age = bdays_after(updated, TODAY)
        if age > lim:
            return f"stale · {age} business days"
    elif cadence == "weekly":
        lim = int(rules.get("weekly", {}).get("days", 9))
        age = (TODAY - updated).days
        if age > lim:
            return f"stale · {age} days"
    return None


def short_title(s: dict) -> str:
    return s["title"].split(" — ")[0].split(" (")[0]


def card_html(c: dict, updated: dt.date | None, stale: str | None, date_note: str | None = None) -> str:
    e = html.escape
    cad = c["cadence"]
    if c.get("asof"):
        when = f"snapshot {c['asof']}"
    elif updated is not None:
        when = f"updated {updated.isoformat()}"
    else:
        when = date_note or "date unavailable"
    top = [f"<span class='pill cad-{e(cad)}'>{e(CADENCE_LABEL.get(cad, cad))}</span>"]
    if c.get("topic"):
        top.append(f"<span class='hub-topic'>{e(c['topic'])}</span>")
    if c.get("surface") == "hub":
        top.append("<span class='hub-surface'>Capstone hub</span>")
    if c.get("type") == "file":
        top.append("<span class='hub-file'>file</span>")
    if c.get("also"):
        top.append(f"<span class='hub-file'>also in {e(c['also'])}</span>")
    meta = [f"<span class='hub-upd'>{e(when)}</span>"]
    if c.get("routine"):
        meta.append(f"<span class='hub-routine'>{e(c['routine'])}</span>")
    if stale:
        meta.append(f"<span class='hub-stale'>⚠ {e(stale)}</span>")
    search = " ".join(str(c.get(k, "")) for k in ("title", "desc", "topic", "routine", "href", "cadence", "surface", "group")).lower()
    cls = "hub-card" + (" is-stale" if stale else "")
    return (f"<a class='{cls}' href='{e(c['href'])}' data-s='{e(search)}'>"
            f"<div class='hub-top'>{''.join(top)}</div>"
            f"<h3>{e(c['title'])}</h3><p>{e(c['desc'])}</p>"
            f"<div class='hub-meta'>{''.join(meta)}</div></a>")


def font_face() -> str:
    if not FONT.exists():
        return ""
    b64 = base64.b64encode(FONT.read_bytes()).decode()
    return ('@font-face{font-family:"OR Jakarta";font-weight:200 800;font-style:normal;font-display:swap;'
            f'src:url(data:font/woff2;base64,{b64}) format("woff2")}}')


def first_existing(paths: list[str]) -> Path | None:
    for p in paths:
        try:
            if Path(p).is_dir():
                return Path(p)
        except OSError:
            continue
    return None


def main() -> int:
    e = html.escape
    reg = json.loads(REG.read_text(encoding="utf-8"))
    rules = reg.get("stale", {})
    sections = reg["sections"]
    ignore = set(reg.get("ignore", {}).keys())
    hub = reg.get("hub", {})
    hub_dir = first_existing(hub.get("base_paths", []))
    hub_url = hub.get("base_url", "/dashboards/")
    hub_note = None if hub_dir else "date unavailable (Capstone-Wiki clone offline)"
    themes = reg.get("themes", {})
    groups = [g for g in themes.get("groups", []) if g.get("members")]
    member_groups: dict[str, list[str]] = {}          # href -> theme group ids (a card may sit in several)
    for g in groups:
        for m in g["members"]:
            member_groups.setdefault(hub_url + m[4:] if m.startswith("hub:") else m, []).append(g["id"])
    gtitle = {g["id"]: g["title"] for g in groups}

    collected: list[tuple[dict, dt.date | None, str | None]] = []   # every card before placement
    missing: list[str] = []
    registered: set[str] = set()
    subhub_dirs: set[str] = set()

    # ---- wiki dashboards (files under _dashboards) ----
    for c in reg["cards"]:
        href = c["href"]
        p = DASH / href
        registered.add(href)
        if c.get("subhub") and "/" in href:
            subhub_dirs.add(href.rsplit("/", 1)[0])
        if not p.exists():
            missing.append(href)
            continue
        updated = dt.date.fromisoformat(c["asof"]) if c.get("asof") else file_date(p)
        collected.append((c, updated, None))

    # ---- Capstone hub (Capstone-Wiki clone served at /dashboards/) ----
    hub_paths: set[str] = set()
    for c in hub.get("cards", []):
        path = c["path"]
        hub_paths.add(path.split("/")[0])
        c = dict(c, href=hub_url + path, surface="hub")
        updated = None
        if hub_dir is not None:
            f = hub_dir / (path + "index.html" if path.endswith("/") else path)
            if f.exists():
                updated = file_date(f)
            else:
                missing.append(c["href"])
        collected.append((c, updated, hub_note))
    skipped = set(k.split("/")[0] for k in hub.get("skipped", {}).keys())

    # ---- place: thematic group or cadence section ----
    by_sec: dict[str, list[str]] = {s["id"]: [] for s in sections}
    counts = {s["id"]: 0 for s in sections}
    by_group: dict[str, list[str]] = {g["id"]: [] for g in groups}
    stale_list: list[tuple[str, str, str, int]] = []   # (href, title, note, age)
    placed: set[str] = set()
    for c, updated, note in collected:
        stale = stale_note(c["cadence"], updated, rules)
        if stale:
            stale_list.append((c["href"], c["title"], stale, (TODAY - updated).days))
        gids = member_groups.get(c["href"])
        if gids:
            for gid in gids:
                also = " · ".join(gtitle[x] for x in gids if x != gid)
                by_group[gid].append(card_html(dict(c, group=" ".join(gtitle[x] for x in gids), also=also), updated, stale, note))
            placed.add(c["href"])
        else:
            sec = c["cadence"] if c["cadence"] in by_sec else sections[-1]["id"]
            by_sec[sec].append(card_html(c, updated, stale, note))
            counts[sec] += 1
    unknown_members = [m for m in member_groups if m not in placed]
    theme_total = len(placed)                           # unique cards across all theme groups

    # ---- 00 home base ----
    home = reg.get("home", {})
    home_cards: list[str] = []
    for c in home.get("cards", []):
        c = dict(c)
        updated, note = None, None
        st = c.get("stat", "")
        if st.startswith("wiki:"):
            f = WIKI / st[5:]
            updated = file_date(f) if f.exists() else None
        elif st.startswith("hub:"):
            hub_paths.add(st[4:].split("/")[0])   # a home card covers its clone folder for the unregistered scan
            if hub_dir is None:
                note = hub_note
            else:
                f = hub_dir / st[4:]
                updated = file_date(f) if f.exists() else None
        stale = stale_note(c["cadence"], updated, rules)
        if stale:
            stale_list.append((c["href"], c["title"], stale, (TODAY - updated).days))
        home_cards.append(card_html(c, updated, stale, note))

    # ---- files on disk / folders in the clone that nobody registered ----
    unreg: list[tuple[str, str, Path]] = []   # (href, label, file)
    for p in sorted(DASH.rglob("*.html")):
        rel = p.relative_to(DASH).as_posix()
        if rel == "index.html" or rel in registered or rel in ignore:
            continue
        if any(rel.startswith(d + "/") for d in subhub_dirs):
            continue
        unreg.append((rel, rel, p))
    if hub_dir is not None:
        for d in sorted(hub_dir.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and (d / "index.html").exists() \
                    and d.name not in hub_paths and d.name not in skipped:
                unreg.append((hub_url + d.name + "/", f"Capstone hub · {d.name}/", d / "index.html"))
    unreg_cards = [card_html({"href": href, "title": label, "cadence": "unregistered",
                              "desc": "On disk but not in _data/dashboards.json — add it with a cadence, routine and topic (or list it under hub.skipped / ignore with a reason).",
                              "routine": "", "surface": "hub" if href.startswith(hub_url) else ""},
                             file_date(f), None) for href, label, f in unreg]

    total = sum(counts.values()) + len(home_cards) + theme_total
    stale_word = f"{len(stale_list)} stale today" if stale_list else "nothing stale today"
    offset = 1 if theme_total else 0            # Temático takes 01 when it has members; cadence sections follow

    # ---- sidebar nav (OpenRouter shell) ----
    nav = []
    if home_cards:
        nav += ["<div class='or-nav-group'><p>Start here</p>",
                f"<a href='#home'><span class='or-nav-number' aria-hidden='true'>00</span>{e(home.get('title', 'Home base'))}"
                f"<span class='or-nav-count'>{len(home_cards)}</span></a></div>"]
    if theme_total:
        nav.append("<div class='or-nav-group'><p>By theme</p>"
                   f"<a href='#themes'><span class='or-nav-number' aria-hidden='true'>01</span>{e(themes.get('title', 'Temático'))}"
                   f"<span class='or-nav-count'>{theme_total}</span></a>")
        for g in groups:
            if by_group[g["id"]]:
                nav.append(f"<a class='or-nav-sub' href='#theme-{e(g['id'])}'>{e(g['title'])}<span class='or-nav-count'>{len(by_group[g['id']])}</span></a>")
        nav.append("</div>")
    nav.append("<div class='or-nav-group'><p>By refresh cadence</p>")
    for i, s in enumerate(sections, 1 + offset):
        if counts[s["id"]]:
            nav.append(f"<a href='#{s['id']}'><span class='or-nav-number' aria-hidden='true'>{i:02d}</span>{e(short_title(s))}"
                       f"<span class='or-nav-count'>{counts[s['id']]}</span></a>")
    nav.append("</div>")
    if unreg_cards:
        nav.append("<div class='or-nav-group'><p>Housekeeping</p><a href='#unregistered'>"
                   f"<span class='or-nav-number' aria-hidden='true'>{len(sections) + 1 + offset:02d}</span>Unregistered"
                   f"<span class='or-nav-count'>{len(unreg_cards)}</span></a></div>")

    shell = (
        "<div class='or-dashboard'><a class='or-skip' href='#dashboard-main'>Skip to dashboards</a>"
        "<aside class='or-sidebar'><a class='or-brand' href='../index.html' aria-label='Capstone research wiki'>"
        "<span class='or-brand-mark' aria-hidden='true'>C</span><span>CAPSTONE<small>RESEARCH INTELLIGENCE</small></span></a>"
        f"<nav class='or-navigation' aria-label='Hub sections'>{''.join(nav)}</nav>"
        f"<div class='or-sidebar-footer'><span class='or-status-dot'></span>Wiki dashboards<small>Generated {TODAY.isoformat()} · {total} dashboards · {e(stale_word)}</small>"
        "<a href='../index.html'>Back to research wiki <span aria-hidden='true'>↗</span></a>"
        f"<a href='{e(hub_url)}'>Capstone hub index (LAN server) <span aria-hidden='true'>↗</span></a></div></aside>"
        "<div class='or-workspace'><header class='or-topbar'><div><p class='or-breadcrumb'>RESEARCH / DASHBOARDS HUB</p>"
        "<h1>Wiki dashboards</h1></div><div class='or-topbar-actions'>"
        f"<span class='or-asof'>Generated <b>{TODAY.isoformat()}</b></span>"
        "<button type='button' class='or-theme' aria-label='Switch to dark theme' aria-pressed='false'>"
        "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.6' aria-hidden='true'><path d='M20.5 13A8.5 8.5 0 0 1 11 3.5 8.5 8.5 0 1 0 20.5 13Z'/></svg></button>"
        "</div></header><main id='dashboard-main' class='or-main' tabindex='-1'>"
    )

    # ---- overview: kicker, headline, sub, tiles ----
    tiles = []
    if theme_total:
        tiles.append(f"<div class='oc-tile'><div class='l'><i style='--c:{TILE_COLOR['themes']}'></i>{e(themes.get('title', 'Temático'))}</div>"
                     f"<div class='v'>{theme_total}</div><div class='s'>{e(' · '.join(g['title'] for g in groups if by_group[g['id']]))}</div></div>")
    for s in sections:
        if not counts[s["id"]]:
            continue
        tiles.append(f"<div class='oc-tile'><div class='l'><i style='--c:{TILE_COLOR.get(s['id'], 'var(--base)')}'></i>{e(short_title(s))}</div>"
                     f"<div class='v'>{counts[s['id']]}</div><div class='s'>{e(s.get('kicker', ''))}</div></div>")
    if stale_list:
        worst = max(stale_list, key=lambda x: x[3])
        tiles.append(f"<div class='oc-tile is-crit'><div class='l'><i style='--c:var(--crit)'></i>Stale</div><div class='v'>{len(stale_list)}</div>"
                     f"<div class='s'>{e(worst[1])} · {e(worst[2].split('· ', 1)[-1])}</div></div>")
    else:
        tiles.append("<div class='oc-tile is-good'><div class='l'><i style='--c:var(--good)'></i>Stale</div><div class='v'>0</div>"
                     "<div class='s'>every daily and weekly page inside its window</div></div>")
    n_rhythms = sum(1 for s in sections if counts[s["id"]])
    n_groups = sum(1 for g in groups if by_group[g["id"]])
    n_hub = len(hub.get("cards", []))
    headline = f"{total} dashboards · {n_rhythms} refresh rhythms"
    if n_groups:
        headline += f" · {n_groups} theme{'s' if n_groups > 1 else ''}"
    headline += f" — {stale_word}"
    overview = (
        "<section class='oc hub-overview' id='overview'><p class='oc-kicker'>Capstone · research wiki + Capstone hub · by theme and by refresh cadence</p>"
        f"<h2 class='oc-headline'>{e(headline)}</h2>"
        "<p class='oc-sub'>Daily pages rebuild on the 18:15 chain, the 09:45 comp rotina and the Claude tasks; weekly ones on the Monday jobs and the Friday heartbeats; "
        "on-demand models and studies move only when their workbook or Bloomberg pull is rerun; explainers and snapshots never change. "
        "A thematic group gathers one subject across cadences — its cards keep their cadence badge and stale rule. "
        f"Cards tagged <b>Capstone hub</b> ({n_hub}) live on the team hub at {e(hub_url)} and open on the LAN server. "
        "A card is flagged <b>stale</b> when a daily page is older than 2 business days or a weekly page older than 9 days. "
        "Dates are file modification times unless the card is a dated snapshot.</p>"
        f"<div class='oc-tiles'>{''.join(tiles)}</div></section>"
    )

    parts = [overview]
    if home_cards:
        parts.append("<section class='hub-section hub-home' id='home'>"
                     f"<span class='oc-kicker'>00 · {e(home.get('kicker', ''))}</span><h2>{e(home.get('title', 'Home base'))}</h2>"
                     f"<span class='sub'>{e(home.get('blurb', ''))}</span>"
                     f"<div class='hub-grid hub-grid-home'>{''.join(home_cards)}</div></section>")
    if theme_total:
        gparts = []
        for g in groups:
            if not by_group[g["id"]]:
                continue
            gparts.append(f"<div class='hub-group' id='theme-{e(g['id'])}'>"
                          f"<h3 class='hub-group-title'>{e(g['title'])}<small>{len(by_group[g['id']])}</small></h3>"
                          f"<span class='hub-group-sub'>{e(g.get('blurb', ''))}</span>"
                          f"<div class='hub-grid'>{''.join(by_group[g['id']])}</div></div>")
        parts.append("<section class='hub-section hub-themes' id='themes'>"
                     f"<span class='oc-kicker'>01 · {e(themes.get('kicker', ''))}</span><h2>{e(themes.get('title', 'Temático'))}</h2>"
                     f"<span class='sub'>{e(themes.get('blurb', ''))}</span>{''.join(gparts)}</section>")

    parts.append("<div class='hub-filter'><input id='q' type='search' placeholder='Filter by title, description, topic, theme or routine… (e.g. memória, 18:15, weekly, Bloomberg, Capstone hub)' autocomplete='off'></div>")

    # ---- cadence sections ----
    for i, s in enumerate(sections, 1 + offset):
        cards = by_sec[s["id"]]
        if not cards:
            continue
        kicker = f"{i:02d} · {s['kicker']}" if s.get("kicker") else f"{i:02d}"
        head = (f"<span class='oc-kicker'>{e(kicker)}</span><h2>{e(s['title'])}</h2>"
                f"<span class='sub'>{e(s.get('blurb', ''))}</span>")
        grid = f"<div class='hub-grid'>{''.join(cards)}</div>"
        if s.get("collapsed"):
            parts.append(f"<details class='hub-section' id='{s['id']}'><summary>{head}</summary>{grid}</details>")
        else:
            parts.append(f"<section class='hub-section' id='{s['id']}'>{head}{grid}</section>")
    if unreg_cards:
        parts.append("<section class='hub-section hub-unreg' id='unregistered'>"
                     f"<span class='oc-kicker'>{len(sections) + 1 + offset:02d} · housekeeping</span><h2>Unregistered</h2>"
                     "<span class='sub'>Files found on disk, or folders in the Capstone-Wiki clone, that no card describes. Register them in _data/dashboards.json (cadence · routine · topic) or list them under ignore / hub.skipped with a reason.</span>"
                     f"<div class='hub-grid'>{''.join(unreg_cards)}</div></section>")
    parts.append("<p class='hub-credit'>Registry <code>_wiki/_data/dashboards.json</code> (hand-edit) → <code>_tools/build_dashboards_hub.py</code>, "
                 "the last step of <code>refresh_features.py</code>. Shell and theme shared with the OpenRouter dashboard (<code>openrouter_presentation.py</code>). "
                 f"Capstone hub cards point at <code>{e(hub_url)}</code> on the LAN server and are dated from the Capstone-Wiki clone"
                 + (f" (<code>{e(str(hub_dir))}</code>)" if hub_dir else " (clone not reachable at build time)") +
                 ". Thematic groups pull cards out of the cadence lists without changing their cadence. "
                 "Stale = daily older than 2 business days, weekly older than 9 days. Anything on disk without a card appears under Unregistered.</p>")


    page = (
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'><title>Wiki dashboards</title>"
        "<script>try{var t=localStorage.getItem('wiki-dash-theme');if(t==='dark'||t==='light')document.documentElement.dataset.theme=t;}catch(e){}</script>"
        f"<style>{font_face()}{OR_CSS}{HUB_CSS}</style></head><body>"
        f"{shell}{''.join(parts)}</main></div></div>"
        f"<script>{OR_JS}</script><script>{HUB_JS}</script></body></html>"
    )
    OUT.write_text(page, encoding="utf-8")

    print(f"hub -> {OUT}  ({total} cards: home {len(home_cards)}, "
          + (f"themes {theme_total} unique [" + ", ".join(f"{g['title']} {len(by_group[g['id']])}" for g in groups if by_group[g['id']]) + "], " if theme_total else "")
          + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
          + f"; Capstone hub {n_hub}" + ("" if hub_dir else " — clone OFFLINE, hub dates unavailable") + ")")
    if stale_list:
        print("STALE: " + "; ".join(f"{h} ({n})" for h, _, n, _ in stale_list))
    if missing:
        print("[WARN] registered but missing on disk: " + ", ".join(missing))
    if unknown_members:
        print("[WARN] theme members with no card: " + ", ".join(unknown_members))
    if unreg:
        print("[WARN] unregistered (shown in the Unregistered section): " + ", ".join(h for h, _, _ in unreg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
