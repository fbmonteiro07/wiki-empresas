r"""
FEATURE 7 — Canonical-assumptions ledger.

The same industry-level number (ASIC share 2027, WFE CY28, GW deployed, HBM
pricing) gets cited with different values on different pages — different
sources, horizons or bases. This renders _data/assumptions.json (hand-curated:
one canonical framing + every sourced variant per metric) into a standing page,
and scans every company page + theme for citations of each metric that are NOT
yet reconciled into the ledger ("sightings"), so basis conflation gets caught
instead of compounding. The scope traps matter as much as the numbers (e.g.
800V/IT-load GW must never be folded into facility-GW-deployed).

Writes _meta/assumptions.md + _dashboards/assumptions.html. Read-only on pages.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_assumptions.py"
"""
import sys, json, re, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import WIKI, META, DATA, DASH, read, html_head, TODAY
sys.stdout.reconfigure(encoding="utf-8")

STATUS_PILL = {"live-debate": ("due", "live debate"), "house-vs-street": ("dn", "house vs street"),
               "scope-trap": ("dn", "scope trap"), "consistent": ("up", "consistent"),
               "converging": ("up", "converging")}


def scan_pages():
    """Yield (relpath, text) for every company page + theme page."""
    for p in sorted(WIKI.glob("*.md")):
        if p.name.startswith(("_", "00_")):
            continue
        yield p.name, read(p)
    for p in sorted((WIKI / "themes").glob("*.md")):
        if p.name.startswith(("_", "00_")):
            continue
        yield f"themes/{p.name}", read(p)


def sightings(metric, pages):
    """Files matching any of the metric's patterns that are not already in any
    variant's cited_in list -> candidate citations to reconcile."""
    known = set()
    for v in metric.get("variants", []):
        known.update(v.get("cited_in", []))
    rxs = [re.compile(pat, re.I) for pat in metric.get("patterns", [])]
    out = []
    for rel, txt in pages:
        if rel in known:
            continue
        for rx in rxs:
            m = rx.search(txt)
            if m:
                frag = txt[max(0, m.start() - 40):m.end() + 60].replace("\n", " ").strip()
                out.append((rel, frag))
                break
    return out


def main():
    ledger = json.loads((DATA / "assumptions.json").read_text(encoding="utf-8"))
    metrics = ledger.get("metrics", {})
    pages = list(scan_pages())

    md = [f"# Canonical assumptions — one number per debate\n",
          f"_Generated {TODAY.isoformat()} from `_data/assumptions.json` (asof {ledger.get('asof','?')}). "
          f"Every cross-page industry number lives here once, with all sourced variants. When a new source "
          f"disagrees, add a variant to the JSON — never silently rebase a page. "
          f"Rebuild: `py _wiki/_tools/build_assumptions.py`._\n"]
    h_parts = []
    n_sight = 0
    for mid, m in metrics.items():
        pill_cls, pill_txt = STATUS_PILL.get(m.get("status", ""), ("due", m.get("status", "?")))
        md.append(f"## {m['title']}  `{mid}`\n")
        md.append(f"_{m['definition']}_\n")
        md.append(f"**Canonical:** {m['canonical']}\n")
        if m.get("scope_note"):
            md.append(f"> ⚠️ **Scope:** {m['scope_note']}\n")
        md.append("| Value | Source | Date | Scope |")
        md.append("|---|---|---|---|")
        for v in m.get("variants", []):
            md.append(f"| {v['value']} | {v['source']} | {v['date']} | {v.get('scope','')} |")
        if m.get("debate"):
            md.append(f"\n**Debate:** {m['debate']}\n")
        s = sightings(m, pages)
        n_sight += len(s)
        if s:
            md.append("**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):")
            for rel, frag in s:
                md.append(f"- `{rel}` — …{frag}…")
            md.append("")

        # html block
        hb = [f"<h2>{html.escape(m['title'])} <span class='pill {pill_cls}'>{pill_txt}</span></h2>",
              f"<p class='byline'>{html.escape(m['definition'])}</p>",
              f"<p><b>Canonical:</b> {html.escape(m['canonical'])}</p>"]
        if m.get("scope_note"):
            hb.append(f"<p style='background:#fff3cd;padding:8px 12px;border-radius:6px'>⚠️ "
                      f"<b>Scope:</b> {html.escape(m['scope_note'])}</p>")
        hb.append("<table><thead><tr><th>Value</th><th>Source</th><th>Date</th><th>Scope</th></tr></thead><tbody>")
        for v in m.get("variants", []):
            hb.append(f"<tr><td>{html.escape(v['value'])}</td><td>{html.escape(v['source'])}</td>"
                      f"<td>{v['date']}</td><td>{html.escape(v.get('scope',''))}</td></tr>")
        hb.append("</tbody></table>")
        if m.get("debate"):
            hb.append(f"<p><b>Debate:</b> {html.escape(m['debate'])}</p>")
        if s:
            hb.append("<p class='mut'><b>Unreconciled sightings:</b></p><ul>")
            for rel, frag in s:
                hb.append(f"<li><code>{html.escape(rel)}</code> — …{html.escape(frag)}…</li>")
            hb.append("</ul>")
        h_parts.append("\n".join(hb))

    META.mkdir(parents=True, exist_ok=True)
    (META / "assumptions.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    head, foot = html_head("Canonical assumptions — one number per debate",
                           f"{TODAY.isoformat()} · every cross-page number, all variants, scope traps flagged")
    (DASH / "assumptions.html").write_text(head + "\n".join(h_parts) + foot, encoding="utf-8")

    print(f"assumptions: {len(metrics)} metrics, "
          f"{sum(len(m.get('variants', [])) for m in metrics.values())} variants, "
          f"{n_sight} unreconciled sightings")
    print(f"  -> {META/'assumptions.md'}")
    print(f"  -> {DASH/'assumptions.html'}")


if __name__ == "__main__":
    main()
