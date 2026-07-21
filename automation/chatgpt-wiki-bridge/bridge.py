#!/usr/bin/env python3
"""Local HTTP bridge from the ChatGPT Chrome helper to the wiki inbox.

The server only listens on loopback. It accepts structured summary payloads from
the companion Chrome extension and writes attributed Markdown files to _inbox.
Stdlib only, by design.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


BRIDGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BRIDGE_DIR.parents[1]
DEFAULT_INBOX = REPO_ROOT / "_inbox"
STATE_DIR = BRIDGE_DIR / "state"
SEEN_PATH = STATE_DIR / "seen.json"
MAX_BODY_BYTES = 1_000_000
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SAFE_TOKEN_RE = re.compile(r"[^A-Za-z0-9._-]+")
write_lock = threading.Lock()


def clean_text(value: Any, limit: int) -> str:
    if value is None:
        return ""
    text = str(value).replace("\x00", "").strip()
    return text[:limit]


def clean_list(value: Any, limit: int = 40) -> list[str]:
    if isinstance(value, str):
        items = re.split(r"[,;\n]", value)
    elif isinstance(value, list):
        items = value
    else:
        items = []
    result: list[str] = []
    for item in items:
        text = clean_text(item, 100)
        if text and text not in result:
            result.append(text)
        if len(result) >= limit:
            break
    return result


def safe_filename_token(value: str, fallback: str, limit: int = 60) -> str:
    token = SAFE_TOKEN_RE.sub("_", value).strip("._-")
    return (token or fallback)[:limit]


def normalize_payload(raw: dict[str, Any]) -> dict[str, Any]:
    summary = clean_text(raw.get("summary"), 800_000)
    if len(summary) < 40:
        raise ValueError("summary must contain at least 40 characters")

    source_date = clean_text(raw.get("source_date"), 10)
    if source_date and not DATE_RE.fullmatch(source_date):
        raise ValueError("source_date must be YYYY-MM-DD or blank")

    tickers = [
        safe_filename_token(t.upper(), "", 12)
        for t in clean_list(raw.get("tickers"))
    ]
    tickers = [t for t in tickers if t]

    return {
        "title": clean_text(raw.get("title"), 240) or "Untitled research summary",
        "source_type": clean_text(raw.get("source_type"), 40) or "unknown",
        "source_name": clean_text(raw.get("source_name"), 240) or "Unknown - verify before patching",
        "source_date": source_date,
        "source_url": clean_text(raw.get("source_url"), 2_000),
        "tickers": tickers,
        "themes": clean_list(raw.get("themes")),
        "chat_title": clean_text(raw.get("chat_title"), 240),
        "summary": summary,
    }


def payload_digest(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def load_seen() -> set[str]:
    try:
        data = json.loads(SEEN_PATH.read_text(encoding="utf-8"))
        return set(data if isinstance(data, list) else [])
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return set()


def save_seen(seen: set[str]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temp = SEEN_PATH.with_suffix(".tmp")
    temp.write_text(json.dumps(sorted(seen), indent=2), encoding="utf-8")
    os.replace(temp, SEEN_PATH)


def render_markdown(payload: dict[str, Any], imported_at: dt.datetime) -> str:
    tickers = ", ".join(payload["tickers"]) or "Not identified"
    themes = ", ".join(payload["themes"]) or "Not identified"
    source_date = payload["source_date"] or "Unknown - verify before patching"
    source_url = payload["source_url"] or "Not provided"
    chat_title = payload["chat_title"] or "Not provided"
    imported = imported_at.strftime("%d %B %Y %H:%M %Z").strip()

    return (
        f"# {payload['title']}\n\n"
        f"- **Source type:** {payload['source_type']}\n"
        f"- **Original source / analyst / show:** {payload['source_name']}\n"
        f"- **Original publication date:** {source_date}\n"
        f"- **Source URL:** {source_url}\n"
        f"- **Companies / tickers:** {tickers}\n"
        f"- **Themes:** {themes}\n"
        f"- **ChatGPT conversation:** {chat_title}\n"
        f"- **Imported locally:** {imported}\n\n"
        "> Processing note: this is a ChatGPT-generated secondary summary. "
        "Attribute every datapoint to the original source and publication date, "
        "not to ChatGPT. Do not patch unattributed claims without review.\n\n"
        "## Summary\n\n"
        f"{payload['summary'].rstrip()}\n"
    )


def choose_output_path(inbox: Path, payload: dict[str, Any], digest: str) -> Path:
    prefix = payload["source_date"] or "undated"
    kind = safe_filename_token(payload["source_type"].upper(), "SUMMARY", 24)
    ticker_part = "-".join(payload["tickers"][:5]) or "MULTI"
    title = safe_filename_token(payload["title"], "summary", 70)
    base = f"{prefix}__ChatGPT__{kind}__{ticker_part}__{title}"
    candidate = inbox / f"{base}.md"
    if not candidate.exists():
        return candidate
    return inbox / f"{base}__{digest[:8]}.md"


def ingest_payload(raw: dict[str, Any], inbox: Path) -> tuple[Path | None, bool]:
    payload = normalize_payload(raw)
    digest = payload_digest(payload)
    with write_lock:
        seen = load_seen()
        if digest in seen:
            return None, True
        inbox.mkdir(parents=True, exist_ok=True)
        output = choose_output_path(inbox, payload, digest)
        now = dt.datetime.now().astimezone()
        output.write_text(render_markdown(payload, now), encoding="utf-8")
        seen.add(digest)
        save_seen(seen)
        return output, False


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "ChatGPTWikiBridge/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stdout.write(f"[{self.log_date_time_string()}] {fmt % args}\n")
        sys.stdout.flush()

    def _origin_allowed(self) -> bool:
        origin = self.headers.get("Origin", "")
        marker = self.headers.get("X-Wiki-Bridge", "")
        return marker == "chatgpt-chrome-extension" and (
            not origin or origin.startswith("chrome-extension://")
        )

    def _preflight_allowed(self) -> bool:
        origin = self.headers.get("Origin", "")
        requested = self.headers.get("Access-Control-Request-Headers", "").lower()
        return origin.startswith("chrome-extension://") and "x-wiki-bridge" in requested

    def _send_json(self, status: int, body: dict[str, Any]) -> None:
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        origin = self.headers.get("Origin", "")
        if origin.startswith("chrome-extension://"):
            self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def do_OPTIONS(self) -> None:  # noqa: N802
        if not self._preflight_allowed():
            self._send_json(403, {"ok": False, "error": "origin not allowed"})
            return
        self.send_response(204)
        origin = self.headers.get("Origin", "")
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Wiki-Bridge")
        self.send_header("Access-Control-Max-Age", "600")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/health":
            self._send_json(404, {"ok": False, "error": "not found"})
            return
        inbox = self.server.inbox  # type: ignore[attr-defined]
        self._send_json(200, {"ok": True, "inbox": str(inbox)})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/ingest":
            self._send_json(404, {"ok": False, "error": "not found"})
            return
        if not self._origin_allowed():
            self._send_json(403, {"ok": False, "error": "origin not allowed"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY_BYTES:
            self._send_json(413, {"ok": False, "error": "invalid payload size"})
            return
        try:
            raw = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(raw, dict):
                raise ValueError("payload must be an object")
            inbox = self.server.inbox  # type: ignore[attr-defined]
            output, duplicate = ingest_payload(raw, inbox)
            self._send_json(
                200,
                {
                    "ok": True,
                    "duplicate": duplicate,
                    "file": str(output) if output else None,
                },
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, OSError) as exc:
            self._send_json(400, {"ok": False, "error": str(exc)})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    parser.add_argument("--check", action="store_true", help="validate configuration and exit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inbox = args.inbox.resolve()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        print("Refusing to bind outside loopback.", file=sys.stderr)
        return 2
    if args.check:
        print(json.dumps({"ok": True, "inbox": str(inbox), "exists": inbox.is_dir()}))
        return 0 if inbox.is_dir() else 1

    server = ThreadingHTTPServer((args.host, args.port), BridgeHandler)
    server.inbox = inbox  # type: ignore[attr-defined]
    print(f"ChatGPT -> wiki bridge listening on http://{args.host}:{args.port}")
    print(f"Inbox: {inbox}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
