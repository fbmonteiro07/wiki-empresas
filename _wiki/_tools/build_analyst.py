r"""Analyst Inbox — proactive, source-linked research triage for the empresas wiki."""

from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _wlib import (  # noqa: E402
    DASH, DATA, META, TODAY, changelog_entries, company_pages, html_head,
    load_estimates, parse_md_table, read, section,
)

sys.stdout.reconfigure(encoding="utf-8")

ANALYST_DATA = DATA / "analyst"
HISTORY = ANALYST_DATA / "history"
BRIEFS = META / "analyst-briefs"
BELIEFS_PATH = ANALYST_DATA / "beliefs.json"
SIGNALS_PATH = ANALYST_DATA / "signals.json"
FEEDBACK_PATH = META / "analyst-feedback.json"

BROKERS = [
    "Morgan Stanley", "BofA", "J.P. Morgan", "JPM", "UBS", "Bernstein",
    "SemiAnalysis", "Goldman Sachs", "Jefferies", "Wolfe", "Susquehanna",
    "SIG", "FT", "FundaAI", "Visible Alpha", "Bloomberg",
]

THEME_TICKERS = [
    (re.compile(r"\b(HBM|DRAM|NAND)\b|(?<!non-)\bmemory\b", re.I), ["MU", "SKHYNIX", "SAMSUNG", "NVDA"]),
    (re.compile(r"\b(High-NA|EUV|litho|WFE)\b", re.I), ["ASML", "TSM", "SAMSUNG", "SKHYNIX"]),
    (re.compile(r"\b(InP|optical|photonics|CPO)\b", re.I), ["LITE", "COHR", "AAOI", "AIXA"]),
    (re.compile(r"\b(server units?|server shipment|non-memory shortages?)\b", re.I), ["DELL", "HPE", "SMCI", "NVDA"]),
    (re.compile(r"\b(TPU|custom ASIC)\b", re.I), ["GOOG", "AVGO", "MRVL", "MEDIATEK"]),
]

FEEDBACK_SCAFFOLD = {
    "version": 1,
    "note": (
        "Hand-maintained Analyst Inbox feedback. Add objects to items using a stable "
        "signal id. disposition: useful|acted|watch|noise|dismissed. noise/dismissed "
        "items remain in signals.json for auditability but are hidden from the brief."
    ),
    "items": [],
}


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return default


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clip(text: str, limit: int = 420) -> str:
    text = re.sub(r"\s+", " ", text).strip(" —")
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "…"


def clean_md(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"\[([^]]+)]\([^)]+\)", r"\1", text)
    text = text.replace("[[", "").replace("]]", "")
    text = re.sub(r"[*_`#>]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_heading(text: str) -> str:
    text = re.sub(r"^\s*(?:\d+\.|[①-⓿❶-❿])\s*", "", text)
    text = re.sub(r"^[\U0001F300-\U0001FAFF☀-➿️★\s]+", "", text)
    return clean_md(text)


def stable_id(kind: str, source_date: str, title: str) -> str:
    raw = f"{kind}|{source_date}|{clean_heading(title).lower()}".encode("utf-8")
    return f"{kind[:4]}-{hashlib.sha1(raw).hexdigest()[:12]}"


def iso_from_name(path: Path) -> str:
    match = re.search(r"(20\d\d-\d\d-\d\d)", path.name)
    return match.group(1) if match else TODAY.isoformat()


def latest_reconciliation() -> Path | None:
    files = list(META.glob("reconciliation-*.md"))
    if not files:
        return None

    def key(path: Path):
        match = re.search(r"(20\d\d)-(\d\d)-(\d\d)", path.name)
        date_key = tuple(map(int, match.groups())) if match else (0, 0, 0)
        return date_key, path.stat().st_mtime

    return max(files, key=key)


def exact_tickers(text: str, known: set[str]) -> list[str]:
    found = []
    for ticker in re.findall(r"\[\[([A-Z][A-Z0-9]{0,11})]]", text):
        if ticker in known and ticker not in found:
            found.append(ticker)
    for ticker in sorted(known, key=len, reverse=True):
        if ticker in found:
            continue
        if re.search(rf"(?<![A-Z0-9]){re.escape(ticker)}(?![A-Z0-9])", text):
            found.append(ticker)
    return found


def infer_theme_tickers(text: str, known: set[str]) -> list[str]:
    out = []
    for pattern, tickers in THEME_TICKERS:
        if pattern.search(text):
            for ticker in tickers:
                if ticker in known and ticker not in out:
                    out.append(ticker)
    return out


def graph_context(graph: dict):
    nodes = {n["id"]: n for n in graph.get("nodes", []) if n.get("type") == "ticker"}
    relations = defaultdict(list)
    for edge in graph.get("edges", []):
        upstream, downstream = edge.get("u"), edge.get("v")
        label = edge.get("label", "")
        if edge.get("type") == "supplies":
            relations[upstream].append({"ticker": downstream, "relation": "customer", "detail": label})
            relations[downstream].append({"ticker": upstream, "relation": "supplier", "detail": label})
        elif edge.get("type") == "competes":
            relations[upstream].append({"ticker": downstream, "relation": "competitor", "detail": label})
            relations[downstream].append({"ticker": upstream, "relation": "competitor", "detail": label})
    return nodes, relations


def select_readthrough(tickers: list[str], relations: dict, book: set[str], limit: int = 7) -> list[dict]:
    rows, seen = [], set(tickers)
    for ticker in tickers:
        candidates = sorted(
            relations.get(ticker, []),
            key=lambda row: (row["ticker"] not in book, row["relation"] != "competitor", row["ticker"]),
        )
        for row in candidates:
            key = (row["ticker"], row["relation"], row["detail"])
            if row["ticker"] in seen or key in seen:
                continue
            seen.add(key)
            enriched = dict(row)
            enriched["from"] = ticker
            enriched["in_book"] = row["ticker"] in book
            rows.append(enriched)
            if len(rows) >= limit:
                return rows
    return rows


def section_excerpt(md: str, heading_rx: str, limit: int) -> str:
    body, kept = section(md, heading_rx), []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("<!--", "|", "<svg", "</svg", "<text", "<rect", "<line", "<defs", "<marker", "<path")):
            continue
        kept.append(clean_md(stripped.lstrip("-* ")))
        if sum(map(len, kept)) >= limit:
            break
    return clip(" ".join(item for item in kept if item), limit)


def open_questions(md: str) -> list[str]:
    bodies = [section(md, r"Debate|thesis"), section(md, r"Catalysts"), section(md, r"Risks")]
    pattern = re.compile(r"\?|\b(unresolved|falsif|adjudicat|watch|open question|what decides|pending)\b", re.I)
    out = []
    for body in bodies:
        for line in body.splitlines():
            value = clean_md(line.lstrip("-* "))
            if len(value) >= 35 and pattern.search(value) and value not in out:
                out.append(clip(value, 280))
            if len(out) >= 6:
                return out
    return out


def previous_beliefs() -> dict:
    candidates = []
    for path in HISTORY.glob("beliefs-*.json"):
        date = iso_from_name(path)
        if date < TODAY.isoformat():
            candidates.append((date, path))
    return load_json(max(candidates)[1], {}).get("companies", {}) if candidates else {}


def build_beliefs(nodes: dict, book_positions: dict) -> tuple[dict, list[dict]]:
    previous, companies, changes = previous_beliefs(), {}, []
    pages = dict(company_pages())
    for ticker in sorted(set(nodes) | set(pages)):
        node, page = nodes.get(ticker, {}), pages.get(ticker)
        md = read(page) if page else ""
        log = sorted(changelog_entries(md), reverse=True) if md else []
        latest_date = log[0][0] if log else node.get("last_chg", "")
        latest_text = clean_md(log[0][1]) if log else ""
        thesis = node.get("thesis", "") or section_excerpt(md, r"Snapshot", 420)
        debate = section_excerpt(md, r"Debate|thesis", 1200)
        belief = {
            "ticker": ticker,
            "sector": node.get("sector", ""),
            "thesis": thesis,
            "debate_excerpt": debate,
            "risks_excerpt": section_excerpt(md, r"^Risks", 700),
            "catalysts_excerpt": section_excerpt(md, r"Catalysts", 700),
            "open_questions": open_questions(md) if md else [],
            "last_change": latest_date,
            "latest_change_excerpt": clip(latest_text, 520),
            "next_catalyst": node.get("next_catalyst", ""),
            "in_book": ticker in book_positions,
            "book_side": book_positions.get(ticker, {}).get("side", ""),
            "book_weight": book_positions.get(ticker, {}).get("weight"),
            "page": f"{ticker}.md" if page else "",
            "thesis_hash": hashlib.sha1(thesis.encode("utf-8")).hexdigest()[:12],
            "debate_hash": hashlib.sha1(debate.encode("utf-8")).hexdigest()[:12],
        }
        companies[ticker] = belief
        old = previous.get(ticker)
        if old and (old.get("thesis_hash") != belief["thesis_hash"] or old.get("debate_hash") != belief["debate_hash"]):
            changes.append({"ticker": ticker, "new": belief})
    return {
        "asof": TODAY.isoformat(),
        "note": "Derived belief ledger; company pages remain the source of truth.",
        "companies": companies,
    }, changes


def evidence_excerpt(body: str, title: str = "") -> str:
    lines = []
    for raw in body.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("|") or re.match(r"^\|?[\s:|-]+\|?$", stripped):
            continue
        value = clean_md(stripped.lstrip("-* "))
        if len(value) >= 40:
            lines.append(value)
    title_rules = [
        (r"Rating-action DATING", r"Both actions are dated"),
        (r"HBM.*\$/Gb", r"Page carried"),
        (r"DELL.*margin guide", r"THE READ"),
        (r"GOOG.*AVGO.*ANTHROPIC", r"FT .*|backstopped|on the hook"),
        (r"MSFT.*BofA", r"PO \$500"),
        (r"NVDA.*BEARISH", r"^Chan:"),
    ]
    for title_rx, line_rx in title_rules:
        if re.search(title_rx, title, re.I):
            for line in lines:
                if re.search(line_rx, line, re.I):
                    return clip(line, 560)
    preferred = re.compile(
        r"THE READ|What it decides|single most|first BEARISH|reframe|invert|wrong|"
        r"conflict|consequential|ceiling|sizes it|financed entirely|same-firm tension|"
        r"on the hook|backstopped|forward leg|cost of capital",
        re.I,
    )
    for line in lines:
        if preferred.search(line):
            return clip(line, 560)
    for line in lines:
        if re.search(r"\d|consensus|guide|management|analyst|source", line, re.I):
            return clip(line, 560)
    return clip(lines[0], 560) if lines else "See the source reconciliation for the underlying evidence."


def source_label(text: str, recon_date: str, title: str = "") -> str:
    dominant_rules = [
        (r"HBM.*\$/Gb", "SemiAnalysis + UBS"),
        (r"DRAM bit supply", "Morgan Stanley · Shawn Kim + Morgan Stanley semicap + UBS/Samsung IR"),
        (r"DELL.*(?:margin guide|own FY27 EPS guide)", "Dell Technologies Q2 FY27 earnings call + Bloomberg consensus"),
        (r"GOOG.*AVGO.*ANTHROPIC", "Financial Times"),
        (r"Rating-action DATING", "J.P. Morgan IG TMT credit · Spear/Degen"),
        (r"NVDA.*BEARISH", "Morgan Stanley · Charlie Chan"),
        (r"Demand-side ceiling", "Morgan Stanley · Shawn Kim"),
        (r"MSFT.*BofA", "BofA"),
    ]
    for title_rx, source in dominant_rules:
        if re.search(title_rx, title, re.I):
            return f"{source} · curated reconciliation {recon_date}"
    names = []
    for name in BROKERS:
        if re.search(rf"(?<![A-Za-z]){re.escape(name)}(?![A-Za-z])", text, re.I) and name not in names:
            names.append(name)
    if re.search(r"\bChan:", text) and "Morgan Stanley · Charlie Chan" not in names:
        names.insert(0, "Morgan Stanley · Charlie Chan")
    if re.search(r"\bKim\b", text) and "Morgan Stanley · Shawn Kim" not in names:
        names.insert(0, "Morgan Stanley · Shawn Kim")
    if re.search(r"management|company|earnings call|primary", text, re.I):
        names.insert(0, "management/company primary")
    prefix = " + ".join(names[:4]) if names else "underlying sources named in the finding"
    return f"{prefix} · curated reconciliation {recon_date}"


def classify_finding(title: str, body: str) -> str:
    text = f"{title} {body[:1600]}"
    if re.search(r"first bearish|narrative|reframe|inversion|ceiling|de-rating|shift", title, re.I):
        return "narrative_shift"
    if re.search(r"conflict|three-way|split|disagree|collision|opposite|contradict", title, re.I):
        return "contradiction"
    if re.search(r"EPS|revenue|margin|consensus|guide|pricing|supply|volume|capex|PT\b", title, re.I):
        return "model_check"
    if re.search(r"wrong|basis|dating|error|mis-locat|must not|unit|inconsistent", title, re.I):
        return "data_quality"
    if re.search(r"conflict|three-way|split|disagree|collision|inversion|opposite|contradict", text, re.I):
        return "contradiction"
    if re.search(r"first bearish|reframe|narrative|multiple|de-rating|shift", text, re.I):
        return "narrative_shift"
    if re.search(r"EPS|revenue|margin|consensus|guide|pricing|supply|volume|capex|PT\b", text, re.I):
        return "model_check"
    return "research_idea"


def confidence_for(body: str) -> str:
    if re.search(
        r"management primary|company primary|management guide|management's own|"
        r"company guide|filing|earnings call",
        body,
        re.I,
    ):
        return "high"
    if re.search(r"two independent|three-way|corroborat", body, re.I):
        return "medium-high"
    if re.search(r"single-source|unconfirmed|ASR|draft transcript|defect", body, re.I):
        return "provisional"
    return "medium"


def action_for(kind: str, tickers: list[str]) -> str:
    names = "/".join(tickers[:4]) or "the affected theme"
    return {
        "model_check": (
            f"Open the {names} model and bridge the claim into revenue, margin and EPS; compare "
            "house, consensus and company guidance on the same period and basis."
        ),
        "contradiction": (
            f"Keep every sourced variant for {names}; identify the primary disclosure or named "
            "adjudicator that can resolve them. Do not average incompatible figures."
        ),
        "narrative_shift": (
            f"Re-grade the {names} thesis evidence and define the next falsifier. Preserve the "
            "prior framing in the page Changelog if the thesis moves."
        ),
        "data_quality": (
            f"Correct the source, unit or period mapping for {names}, then audit every dependent "
            "model, assumption and cross-page reference before adopting a new mark."
        ),
        "research_idea": (
            f"Turn the finding into a bull/base/bear question for {names}; identify the KPI and "
            "source that would make it investable."
        ),
    }[kind]


def falsifier_for(kind: str, body: str) -> str:
    for raw in body.splitlines():
        value = clean_md(raw.lstrip("-* "))
        if re.search(r"Adjudicator:|falsif|what it decides|next hard|pending", value, re.I) and len(value) >= 35:
            return clip(value, 360)
    return {
        "model_check": "A like-for-like estimate bridge or company guide that closes the identified gap.",
        "contradiction": "The next primary disclosure that puts the competing variants on one defined basis.",
        "narrative_shift": "The next reported KPI or catalyst contradicting the proposed new frame.",
        "data_quality": "A primary-source check showing the current source, unit and period mapping was already correct.",
        "research_idea": "No observable KPI or dated catalyst can be identified to test the hypothesis.",
    }[kind]


def priority_from_score(score: int) -> str:
    return "high" if score >= 68 else "medium" if score >= 46 else "watch"


def freshness_points(source_date: str) -> tuple[int, str]:
    try:
        age = (TODAY - dt.date.fromisoformat(source_date)).days
    except ValueError:
        return 0, "standing"
    if age <= 1:
        return 12, "immediate"
    if age <= 7:
        return 7, "this week"
    return 2, "standing"


def reconciliation_signals(recon: Path | None, known: set[str], relations: dict, book: set[str]) -> list[dict]:
    if recon is None:
        return []
    md = read(recon)
    match = re.search(r"##\s*[^\n]*DIVERGES[^\n]*.*?(?=\n##\s|\Z)", md, re.S | re.I)
    if not match:
        return []
    recon_date, out = iso_from_name(recon), []
    for part in re.split(r"(?m)^###\s+", match.group(0))[1:]:
        raw_title, _, body = part.partition("\n")
        if re.search(r"RESOLVED\b.*?(?:→|->)\s*CONFIRMS", raw_title, re.I):
            continue
        title = clean_heading(raw_title)
        primary = exact_tickers(title, known)
        if not primary:
            primary = infer_theme_tickers(title, known)
        if not primary:
            primary = exact_tickers(body[:2200], known)[:6]
        kind = classify_finding(title, body)
        fresh, urgency = freshness_points(recon_date)
        score = 24 + raw_title.count("🔴") * 16 + (7 if "⚠" in raw_title else 0) + fresh
        score += 18 if any(ticker in book for ticker in primary) else 0
        score += 7 if len(primary) > 1 else 0
        if re.search(r"headline|single most|first bearish|above the street high|ceiling", part, re.I):
            score += 10
        if kind in {"model_check", "contradiction", "data_quality"}:
            score += 5
        score = min(100, score)
        out.append({
            "id": stable_id("reconciliation", recon_date, title),
            "asof": TODAY.isoformat(),
            "source_date": recon_date,
            "type": kind,
            "priority": priority_from_score(score),
            "score": score,
            "title": title,
            "tickers": primary,
            "in_book": [ticker for ticker in primary if ticker in book],
            "impact": priority_from_score(score),
            "urgency": urgency,
            "confidence": confidence_for(body),
            "why_now": evidence_excerpt(body, title),
            "belief_update": (
                "This curated divergence challenges the standing thesis or model framing; keep "
                "it open until the named falsifier is observed."
            ),
            "action": action_for(kind, primary),
            "falsifier": falsifier_for(kind, body),
            "readthrough": select_readthrough(primary, relations, book),
            "source": source_label(f"{title}\n{body[:1400]}", recon_date, title),
            "evidence_paths": [f"_meta/{recon.name}"],
            "evidence_anchor": title,
            "origin": "curated_reconciliation",
        })
    return out


def estimate_signals(known: set[str], relations: dict, book: set[str]) -> list[dict]:
    house = load_json(DATA / "house.json", {}).get("companies", {})
    estimates = load_estimates()
    estimate_companies = estimates.get("companies", {})
    estimate_date, out = estimates.get("asof", TODAY.isoformat()), []
    for ticker, company_house in house.items():
        company_estimates = estimate_companies.get(ticker, {})
        if ticker not in known or company_estimates.get("ccy", "USD") != "USD" or "error" in company_estimates:
            continue
        for year, period in (("2026", "CY2026"), ("2027", "CY2027")):
            house_year = company_house.get("years", {}).get(year, {})
            street_year = company_estimates.get("periods", {}).get(period, {})
            checks = []
            if house_year.get("eps") is not None and street_year.get("eps") not in (None, 0):
                checks.append(("EPS", house_year["eps"], street_year["eps"], ""))
            if house_year.get("rev") is not None and street_year.get("rev") not in (None, 0):
                checks.append(("revenue", house_year["rev"], street_year["rev"] / 1000.0, "$bn"))
            for metric, house_value, street_value, unit in checks:
                delta = (house_value / street_value - 1.0) * 100.0
                if abs(delta) < 15.0:
                    continue
                direction = "above" if delta > 0 else "below"
                title = f"{ticker} — {year} {metric} house view is {abs(delta):.0f}% {direction} consensus"
                score = min(100, 36 + int(min(abs(delta), 30)) + (18 if ticker in book else 0))
                house_fmt = "$" + (f"{house_value:,.2f}" if metric == "EPS" else f"{house_value:,.1f}bn")
                street_fmt = "$" + (f"{street_value:,.2f}" if metric == "EPS" else f"{street_value:,.1f}bn")
                out.append({
                    "id": stable_id("estimate", estimate_date, title),
                    "asof": TODAY.isoformat(), "source_date": estimate_date,
                    "type": "model_check", "priority": priority_from_score(score), "score": score,
                    "title": title, "tickers": [ticker], "in_book": [ticker] if ticker in book else [],
                    "impact": priority_from_score(score), "urgency": "standing", "confidence": "provisional",
                    "why_now": (
                        f"Capstone carries {year} {metric} at {house_fmt} versus Bloomberg consensus at "
                        f"{street_fmt} as of {estimate_date}, a derived {delta:+.1f}% gap. Revenue "
                        "comparisons require a basis check."
                    ) if metric == "revenue" else (
                        f"Capstone carries {year} {metric} at {house_fmt} versus Bloomberg consensus at "
                        f"{street_fmt} as of {estimate_date}, a derived {delta:+.1f}% gap."
                    ),
                    "belief_update": "The house/Street disagreement requires an explicit driver bridge.",
                    "action": action_for("model_check", [ticker]),
                    "falsifier": "A same-period, same-definition bridge showing the apparent gap is only a basis mismatch.",
                    "readthrough": select_readthrough([ticker], relations, book),
                    "source": f"{clean_md(company_house.get('source', 'Capstone house model'))} · Bloomberg consensus {estimate_date}",
                    "evidence_paths": ["_data/house.json", "_data/estimates.json"],
                    "evidence_anchor": f"{ticker} {year} {metric}", "origin": "house_vs_consensus",
                    "values": {"house": house_value, "consensus": street_value, "delta_pct": round(delta, 2), "unit": unit},
                })
    return out


def parse_catalyst_table(md: str, heading_rx: str) -> list[list[str]]:
    _, rows = parse_md_table(section(md, heading_rx))
    return rows


def catalyst_signals(known: set[str], relations: dict, book: set[str]) -> list[dict]:
    path = META / "catalysts.md"
    if not path.is_file():
        return []
    md, out = read(path), []
    for cells in parse_catalyst_table(md, r"Upcoming"):
        if len(cells) < 3:
            continue
        event_date, ticker, catalyst = clean_md(cells[0]), clean_md(cells[1]), clean_md(cells[2])
        if ticker not in known:
            continue
        try:
            days = (dt.date.fromisoformat(event_date) - TODAY).days
        except ValueError:
            continue
        if days < 0 or days > 45:
            continue
        score = 25 + (20 if ticker in book else 0) + min(catalyst.count("🔴"), 2) * 9
        if days <= 1:
            score, urgency = score + 24, "immediate"
        elif days <= 7:
            score, urgency = score + 15, "this week"
        elif days <= 21:
            score, urgency = score + 7, "upcoming"
        else:
            urgency = "calendar"
        score = min(100, score)
        label = re.sub(r"^[🆕🔴⚠️✅⏳\U0001F300-\U0001FAFF☀-➿️★\s]+", "", catalyst)
        label = re.sub(
            r"^20\d\d-\d\d-\d\d(?:\s*\([^)]*\))?\s*[—:-]\s*",
            "",
            label,
        )
        title = f"{ticker} — {event_date}: {clip(label, 92)}"
        out.append({
            "id": stable_id("catalyst", event_date, f"{ticker}|{catalyst}"),
            "asof": TODAY.isoformat(), "source_date": event_date, "event_date": event_date,
            "type": "catalyst", "priority": priority_from_score(score), "score": score,
            "title": title, "tickers": [ticker], "in_book": [ticker] if ticker in book else [],
            "impact": priority_from_score(score), "urgency": urgency, "confidence": "medium",
            "why_now": clip(catalyst, 560),
            "belief_update": "A dated event can resolve or reframe an open debate.",
            "action": (
                "Freeze the pre-event bull/base/bear expectations and the exact datapoints that "
                "arbitrate the debate; log the outcome after the event."
            ),
            "falsifier": "The event passes without addressing the identified debate or without a measurable expectation gap.",
            "readthrough": select_readthrough([ticker], relations, book),
            "source": f"{ticker} page catalyst ledger; underlying source/date retained in the catalyst text",
            "evidence_paths": ["_meta/catalysts.md", f"{ticker}.md"],
            "evidence_anchor": catalyst, "origin": "catalyst_calendar",
        })
    for cells in parse_catalyst_table(md, r"Passed.*post-mortem"):
        if len(cells) < 3:
            continue
        event_date, ticker, catalyst = clean_md(cells[0]), clean_md(cells[1]), clean_md(cells[2])
        if ticker not in known:
            continue
        score = 58 + (16 if ticker in book else 0)
        title = f"{ticker} — catalyst passed without a logged outcome"
        out.append({
            "id": stable_id("postmortem", event_date, f"{ticker}|{catalyst}"),
            "asof": TODAY.isoformat(), "source_date": event_date, "event_date": event_date,
            "type": "postmortem", "priority": priority_from_score(score), "score": score,
            "title": title, "tickers": [ticker], "in_book": [ticker] if ticker in book else [],
            "impact": priority_from_score(score), "urgency": "overdue", "confidence": "high",
            "why_now": clip(catalyst, 520),
            "belief_update": "The feedback loop is incomplete until the original bull/bear question is scored.",
            "action": f"Write a source-attributed bull won|bear won|neutral outcome for {ticker} in outcomes.md.",
            "falsifier": "An existing outcome entry is found under a different but equivalent event date.",
            "readthrough": [], "source": "Catalyst outcome ledger",
            "evidence_paths": ["_meta/catalysts.md", "_meta/outcomes.md"],
            "evidence_anchor": catalyst, "origin": "outcome_loop",
        })
    return out


def worklist_signals(known: set[str], book: set[str]) -> list[dict]:
    work = load_json(META / "worklist.json", {})
    source_date, out = work.get("asof", TODAY.isoformat()), []
    for ticker in work.get("bbg_missing", []):
        title, score = f"{ticker} — Bloomberg consensus missing", 54 + (16 if ticker in book else 0)
        out.append({
            "id": stable_id("data_gap", source_date, title), "asof": TODAY.isoformat(),
            "source_date": source_date, "type": "data_gap", "priority": priority_from_score(score),
            "score": score, "title": title, "tickers": [ticker] if ticker in known else [],
            "in_book": [ticker] if ticker in book else [], "impact": priority_from_score(score),
            "urgency": "this week", "confidence": "high",
            "why_now": "The current consensus snapshot cannot support a house-vs-Street or revision analysis for this name.",
            "belief_update": "Ranking confidence is reduced until the missing consensus series is restored.",
            "action": f"Run the merge-safe Bloomberg estimate fetch for {ticker}, then rebuild the snapshot and Analyst Inbox.",
            "falsifier": "A valid, current estimate record already exists under a different Bloomberg identifier.",
            "readthrough": [], "source": f"Wiki remediation worklist {source_date}",
            "evidence_paths": ["_meta/worklist.json"], "evidence_anchor": title, "origin": "worklist",
        })
    for ticker in work.get("no_transcript", []):
        title, score = f"{ticker} — latest earnings transcript absent", 43 + (16 if ticker in book else 0)
        out.append({
            "id": stable_id("data_gap", source_date, title), "asof": TODAY.isoformat(),
            "source_date": source_date, "type": "data_gap", "priority": priority_from_score(score),
            "score": score, "title": title, "tickers": [ticker] if ticker in known else [],
            "in_book": [ticker] if ticker in book else [], "impact": priority_from_score(score),
            "urgency": "standing", "confidence": "high",
            "why_now": "The wiki cannot verify management wording or build a reliable commentary-evolution view without the transcript.",
            "belief_update": "Narrative and management-credibility conclusions remain provisional.",
            "action": f"Fetch the latest {ticker} earnings transcript into the ticker transcript folder, ingest it, and rebuild.",
            "falsifier": "The company has not held a relevant earnings call or publishes no transcript.",
            "readthrough": [], "source": f"Wiki remediation worklist {source_date}",
            "evidence_paths": ["_meta/worklist.json"], "evidence_anchor": title, "origin": "worklist",
        })
    return out


def belief_change_signals(changes: list[dict], relations: dict, book: set[str]) -> list[dict]:
    out = []
    for item in changes:
        ticker, new = item["ticker"], item["new"]
        source_date = new.get("last_change") or TODAY.isoformat()
        title = f"{ticker} — derived thesis/debate state changed since the prior daily snapshot"
        score = min(100, 62 + (18 if ticker in book else 0))
        out.append({
            "id": stable_id("belief_change", source_date, title), "asof": TODAY.isoformat(),
            "source_date": source_date, "type": "narrative_shift",
            "priority": priority_from_score(score), "score": score, "title": title,
            "tickers": [ticker], "in_book": [ticker] if ticker in book else [],
            "impact": priority_from_score(score), "urgency": "immediate", "confidence": "high",
            "why_now": clip(new.get("latest_change_excerpt") or "The thesis or Debate section fingerprint changed.", 560),
            "belief_update": "The standing thesis or debate wording changed; inspect the Changelog before adopting the new frame.",
            "action": action_for("narrative_shift", [ticker]),
            "falsifier": "The fingerprint moved only because of formatting or a derived snapshot insertion.",
            "readthrough": select_readthrough([ticker], relations, book),
            "source": f"{ticker} page Changelog {source_date}",
            "evidence_paths": [f"{ticker}.md"], "evidence_anchor": new.get("latest_change_excerpt", ""),
            "origin": "belief_diff",
        })
    return out


def apply_feedback(signals: list[dict]) -> None:
    if not FEEDBACK_PATH.exists():
        write_json(FEEDBACK_PATH, FEEDBACK_SCAFFOLD)
    feedback = load_json(FEEDBACK_PATH, FEEDBACK_SCAFFOLD)
    by_id = {item.get("id"): item for item in feedback.get("items", []) if item.get("id")}
    for signal in signals:
        item = by_id.get(signal["id"], {})
        signal["feedback"] = item.get("disposition", "")
        signal["feedback_note"] = item.get("note", "")
        signal["hidden"] = signal["feedback"] in {"noise", "dismissed"}
        if signal["feedback"] in {"useful", "acted"}:
            signal["score"] = min(100, signal["score"] + 4)


def dedupe_signals(signals: list[dict]) -> list[dict]:
    best = {}
    for signal in signals:
        if signal.get("origin") == "catalyst_calendar":
            key = "catalyst:" + ",".join(signal.get("tickers", [])) + ":" + signal.get("event_date", "")
        else:
            key = signal["id"]
        prior = best.get(key)
        if prior is None or signal["score"] > prior["score"]:
            best[key] = signal
    return sorted(best.values(), key=lambda signal: (-signal["score"], signal["title"]))


def carry_forward_open_signals(signals: list[dict]) -> list[dict]:
    """Keep unresolved curated findings visible after a new reconciliation lands."""
    candidates = []
    for path in HISTORY.glob("signals-*.json"):
        date = iso_from_name(path)
        if date < TODAY.isoformat():
            candidates.append((date, path))
    if not candidates:
        return signals

    prior = load_json(max(candidates)[1], {}).get("signals", [])
    current_titles = {clean_heading(signal.get("title", "")).lower() for signal in signals}
    for old in prior:
        if old.get("origin") != "curated_reconciliation" or old.get("hidden"):
            continue
        title_key = clean_heading(old.get("title", "")).lower()
        if not title_key or title_key in current_titles:
            continue
        try:
            age = (TODAY - dt.date.fromisoformat(old.get("source_date", ""))).days
        except ValueError:
            continue
        if age < 1 or age > 21:
            continue
        carried = dict(old)
        carried["asof"] = TODAY.isoformat()
        carried["urgency"] = "standing"
        carried["score"] = max(35, int(carried.get("score", 35)) - 6)
        carried["priority"] = priority_from_score(carried["score"])
        carried["carried_from"] = old.get("source_date", "")
        signals.append(carried)
        current_titles.add(title_key)
    return signals


def focus_list(signals: list[dict], beliefs: dict, book_seed: bool) -> list[dict]:
    by_ticker = defaultdict(list)
    for signal in signals:
        if not signal.get("hidden"):
            for ticker in signal.get("tickers", []):
                by_ticker[ticker].append(signal)
    rows = []
    for ticker, items in by_ticker.items():
        belief = beliefs.get(ticker, {})
        score = max(item["score"] for item in items) + min(12, max(0, len(items) - 1) * 2)
        if belief.get("in_book"):
            score += 5 if book_seed else 16
        rows.append({
            "ticker": ticker, "focus_score": min(120, score),
            "in_book": bool(belief.get("in_book")), "signal_count": len(items),
            "high_count": sum(1 for item in items if item["priority"] == "high"),
            "sector": belief.get("sector", ""), "thesis": belief.get("thesis", ""),
            "next_catalyst": belief.get("next_catalyst", ""),
            "why": [item["title"] for item in items[:3]],
        })
    rows.sort(key=lambda row: (-row["focus_score"], -row["high_count"], row["ticker"]))
    return rows


def evidence_link(path: str, html_mode: bool = False) -> str:
    if path.startswith("_meta/"):
        return "../" + path if html_mode else path.removeprefix("_meta/")
    return "../" + path


def render_readthrough(rows: list[dict]) -> str:
    if not rows:
        return "—"
    return "; ".join(
        f"{row['ticker']} ({row['relation']}{': ' + row['detail'] if row.get('detail') else ''})"
        for row in rows
    )


def render_brief(payload: dict, recon: Path | None) -> str:
    active = [signal for signal in payload["signals"] if not signal.get("hidden")]
    ideas = [s for s in active if s["type"] not in {"catalyst", "postmortem", "data_gap"}][:12]
    catalysts = [
        s for s in active
        if s["type"] == "catalyst" and s["urgency"] in {"immediate", "this week"}
    ][:10]
    hygiene = [s for s in active if s["type"] in {"postmortem", "data_gap"}][:10]
    lines = [
        "# Daily Analyst Brief", "",
        f"_Generated {TODAY.isoformat()} · {len(active)} active signals · latest reconciliation: "
        f"{recon.name if recon else 'none'}._", "",
    ]
    if payload["book"]["seed"]:
        lines += [
            "> ⚠️ **Portfolio priority is provisional.** _data/book.json is still a seed with "
            "unknown weights. Book badges identify seeded names but do not represent real exposure.",
            "",
        ]
    lines += [
        "## Focus list", "",
        "| Rank | Ticker | Book | Signals | Why focus now |",
        "|---:|---|---|---:|---|",
    ]
    for rank, row in enumerate(payload["focus"][:12], 1):
        why = "; ".join(row["why"][:2])
        lines.append(
            f"| {rank} | **{row['ticker']}** | {'seed' if row['in_book'] else '—'} | "
            f"{row['signal_count']} | {why} |"
        )
    if not payload["focus"]:
        lines.append("| — | _No active signals_ | | | |")

    lines += ["", "## Highest-priority ideas", ""]
    for rank, signal in enumerate(ideas, 1):
        icon = "🔴" if signal["priority"] == "high" else "🟡" if signal["priority"] == "medium" else "⚪"
        seeded = f" · seeded book: {', '.join(signal['in_book'])}" if signal["in_book"] else ""
        lines += [
            f"### {rank}. {icon} {signal['title']}", "",
            f"_{signal['type'].replace('_', ' ').upper()} · {signal['impact'].upper()} IMPACT · "
            f"{signal['urgency'].upper()} · {signal['confidence'].upper()} CONFIDENCE_", "",
            f"- **Tickers:** {', '.join(signal['tickers']) or 'cross-theme'}{seeded}",
            f"- **Why now:** {signal['why_now']}",
            f"- **Belief update:** {signal['belief_update']}",
            f"- **Action:** {signal['action']}",
            f"- **Falsifier:** {signal['falsifier']}",
            f"- **Read-through:** {render_readthrough(signal['readthrough'])}",
            f"- **Attribution:** {signal['source']}.",
        ]
        paths = " · ".join(
            f"[{Path(path).name}]({evidence_link(path)})" for path in signal["evidence_paths"]
        )
        lines += [f"- **Evidence:** {paths} · signal {signal['id']}", ""]

    lines += ["## Catalysts requiring preparation", ""]
    if catalysts:
        for signal in catalysts:
            lines.append(
                f"- **{signal['title']}** — {signal['why_now']} "
                f"_Action:_ {signal['action']} ({signal['id']})"
            )
    else:
        lines.append("_No immediate or this-week catalysts parsed._")

    lines += ["", "## Research hygiene", ""]
    if hygiene:
        for signal in hygiene:
            lines.append(
                f"- **{signal['title']}** — {signal['action']} "
                f"_Source: {signal['source']}._ ({signal['id']})"
            )
    else:
        lines.append("_No open data gaps or catalyst post-mortems._")

    lines += [
        "", "## Feedback loop", "",
        "Record useful, acted, watch, noise, or dismissed against a signal ID in "
        "_meta/analyst-feedback.json. Noise/dismissed items remain in the audit data "
        "but disappear from the default brief.", "",
        "_This is a research-triage artifact, not an instruction to trade. Company pages "
        "and primary sources remain authoritative._", "",
    ]
    return "\n".join(lines)


def render_dashboard(payload: dict) -> str:
    head, foot = html_head(
        "Analyst Inbox",
        f"{TODAY.isoformat()} · proactive research triage · source-linked and reviewable",
    )
    signals = payload["signals"]
    active = [signal for signal in signals if not signal.get("hidden")]
    counts = defaultdict(int)
    for signal in active:
        counts[signal["priority"]] += 1
    parts = [head, """
<style>
.summary{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:8px 0 22px}
.stat,.card,.warning{background:#fff;border:1px solid #dde2ea;border-radius:10px;padding:14px}
.stat b{display:block;font-size:24px;color:#0f1729}.stat span{color:#6b7280;font-size:12px}
.warning{background:#fff8e1;border-color:#ead28a;margin:10px 0 18px}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.controls button{border:1px solid #ccd3df;background:#fff;border-radius:16px;padding:5px 11px;cursor:pointer}
.controls button.on{background:#0f1729;color:#fff}.cards{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.card{position:relative}.card h3{font-size:15px;margin:0 0 7px;color:#0f1729;padding-right:58px}
.card p{margin:7px 0;font-size:13px}
.badge{display:inline-block;border-radius:10px;padding:2px 7px;margin:0 4px 4px 0;font-size:10px;font-weight:700;text-transform:uppercase;background:#eef1f6}
.badge.high{background:#fdecea;color:#b42318}.badge.medium{background:#fff3cd;color:#8a6d1b}
.badge.watch{background:#eef1f6;color:#596273}.book{position:absolute;right:12px;top:12px;background:#e8f1ff;color:#1856a8}
.lbl{font-weight:700;color:#374151}.ev{color:#667085;font-size:12px}.ev a{color:#1c5fd6;text-decoration:none}
@media(max-width:800px){.summary{grid-template-columns:1fr 1fr}.cards{grid-template-columns:1fr}}
</style>
"""]
    parts.append(
        f"<div class='summary'><div class='stat'><b>{len(active)}</b><span>active signals</span></div>"
        f"<div class='stat'><b>{counts['high']}</b><span>high priority</span></div>"
        f"<div class='stat'><b>{sum(1 for s in active if s['in_book'])}</b><span>seeded-book signals</span></div>"
        f"<div class='stat'><b>{len(payload['focus'])}</b><span>names in focus queue</span></div></div>"
    )
    if payload["book"]["seed"]:
        parts.append(
            "<div class='warning'><b>Portfolio ranking is provisional.</b> "
            "<code>_data/book.json</code> is a seed with unknown weights.</div>"
        )
    parts.append(
        "<h2>Where to focus</h2><table class='sortable'><thead><tr><th class='r'>Rank</th>"
        "<th>Ticker</th><th>Book</th><th class='r'>Signals</th><th>Why now</th>"
        "</tr></thead><tbody>"
    )
    for rank, row in enumerate(payload["focus"][:15], 1):
        why = "; ".join(row["why"][:2])
        parts.append(
            f"<tr><td class='r' data-v='{rank}'>{rank}</td><td class='tk'>"
            f"<a href='../{row['ticker']}.md'>{row['ticker']}</a></td>"
            f"<td>{'seed' if row['in_book'] else '—'}</td>"
            f"<td class='r' data-v='{row['signal_count']}'>{row['signal_count']}</td>"
            f"<td>{html.escape(why)}</td></tr>"
        )
    parts.append("</tbody></table>")
    parts.append(
        "<h2>Signal queue</h2><div class='controls'>"
        "<button class='on' data-filter='all'>All</button><button data-filter='high'>High</button>"
        "<button data-filter='medium'>Medium</button><button data-filter='book'>Book</button>"
        "<button data-filter='model_check'>Model checks</button>"
        "<button data-filter='contradiction'>Contradictions</button>"
        "<button data-filter='catalyst'>Catalysts</button></div><div class='cards'>"
    )
    for signal in signals:
        if signal.get("hidden"):
            continue
        in_book = "1" if signal["in_book"] else "0"
        book_badge = '<span class="badge book">BOOK</span>' if signal["in_book"] else ""
        parts.append(
            f"<article class='card' data-priority='{signal['priority']}' "
            f"data-type='{signal['type']}' data-book='{in_book}'>{book_badge}"
            f"<h3>{html.escape(signal['title'])}</h3>"
            f"<span class='badge {signal['priority']}'>{signal['priority']}</span>"
            f"<span class='badge'>{html.escape(signal['type'].replace('_', ' '))}</span>"
            f"<span class='badge'>{html.escape(signal['confidence'])} confidence</span>"
            f"<p><span class='lbl'>Why now:</span> {html.escape(signal['why_now'])}</p>"
            f"<p><span class='lbl'>Action:</span> {html.escape(signal['action'])}</p>"
            f"<p><span class='lbl'>Falsifier:</span> {html.escape(signal['falsifier'])}</p>"
            f"<p><span class='lbl'>Read-through:</span> {html.escape(render_readthrough(signal['readthrough']))}</p>"
            f"<p class='ev'><span class='lbl'>Attribution:</span> {html.escape(signal['source'])}<br>"
        )
        links = [
            f"<a href='{html.escape(evidence_link(path, True))}'>{html.escape(Path(path).name)}</a>"
            for path in signal["evidence_paths"]
        ]
        parts.append(
            f"Evidence: {' · '.join(links)} · <code>{signal['id']}</code></p></article>"
        )
    parts += ["</div>", """
<script>
document.querySelectorAll('.controls button').forEach(function(b){b.onclick=function(){
  document.querySelectorAll('.controls button').forEach(function(x){x.classList.remove('on')});
  b.classList.add('on');var f=b.getAttribute('data-filter');
  document.querySelectorAll('.cards .card').forEach(function(c){
    var show=f==='all'||c.getAttribute('data-priority')===f||c.getAttribute('data-type')===f||
      (f==='book'&&c.getAttribute('data-book')==='1');
    c.style.display=show?'block':'none';
  });
};});
</script>
""", foot]
    return "\n".join(parts)


def validate(payload: dict, known: set[str]) -> None:
    ids = set()
    for signal in payload["signals"]:
        required = [
            "id", "title", "source_date", "source", "why_now", "action",
            "falsifier", "evidence_paths",
        ]
        missing = [key for key in required if not signal.get(key)]
        if missing:
            raise ValueError(f"signal {signal.get('title', '?')} missing {missing}")
        if signal["id"] in ids:
            raise ValueError(f"duplicate signal id {signal['id']}")
        ids.add(signal["id"])
        bad = [ticker for ticker in signal.get("tickers", []) if ticker not in known]
        if bad:
            raise ValueError(f"unknown tickers {bad} in {signal['id']}")


def main() -> None:
    for directory in (ANALYST_DATA, HISTORY, BRIEFS, DASH):
        directory.mkdir(parents=True, exist_ok=True)
    graph = load_json(DATA / "graph_full.json", {})
    nodes, relations = graph_context(graph)
    known = set(nodes) | {ticker for ticker, _ in company_pages()}
    book_raw = load_json(DATA / "book.json", {"seed": True, "positions": []})
    book_positions = {
        position["tk"]: position
        for position in book_raw.get("positions", [])
        if position.get("tk")
    }
    book = set(book_positions)

    beliefs, belief_changes = build_beliefs(nodes, book_positions)
    recon = latest_reconciliation()
    signals = []
    signals += reconciliation_signals(recon, known, relations, book)
    signals += estimate_signals(known, relations, book)
    signals += catalyst_signals(known, relations, book)
    signals += worklist_signals(known, book)
    signals += belief_change_signals(belief_changes, relations, book)
    signals = carry_forward_open_signals(signals)
    signals = dedupe_signals(signals)
    apply_feedback(signals)
    signals.sort(key=lambda signal: (signal.get("hidden", False), -signal["score"], signal["title"]))
    focus = focus_list(signals, beliefs["companies"], bool(book_raw.get("seed", False)))

    payload = {
        "asof": TODAY.isoformat(),
        "latest_reconciliation": recon.name if recon else "",
        "book": {
            "asof": book_raw.get("asof", ""),
            "seed": bool(book_raw.get("seed", False)),
            "positions": len(book_positions),
        },
        "stats": {
            "signals": len(signals),
            "active": sum(1 for signal in signals if not signal.get("hidden")),
            "high": sum(
                1 for signal in signals
                if not signal.get("hidden") and signal["priority"] == "high"
            ),
            "belief_changes": len(belief_changes),
            "focus_names": len(focus),
        },
        "focus": focus,
        "signals": signals,
    }
    validate(payload, known)

    write_json(BELIEFS_PATH, beliefs)
    write_json(SIGNALS_PATH, payload)
    write_json(HISTORY / f"beliefs-{TODAY.isoformat()}.json", beliefs)
    write_json(HISTORY / f"signals-{TODAY.isoformat()}.json", payload)
    brief = render_brief(payload, recon)
    (META / "analyst-brief-latest.md").write_text(brief, encoding="utf-8")
    (BRIEFS / f"{TODAY.isoformat()}.md").write_text(brief, encoding="utf-8")
    (DASH / "analyst-inbox.html").write_text(render_dashboard(payload), encoding="utf-8")
    print(
        f"analyst: {payload['stats']['active']} active signals "
        f"({payload['stats']['high']} high) · {len(focus)} focus names · "
        f"{len(belief_changes)} belief changes"
    )
    print(f"  -> {BELIEFS_PATH}")
    print(f"  -> {SIGNALS_PATH}")
    print(f"  -> {META / 'analyst-brief-latest.md'}")
    print(f"  -> {DASH / 'analyst-inbox.html'}")


if __name__ == "__main__":
    main()
