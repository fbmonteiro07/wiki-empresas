"""Refresh the internal credit dashboard and prepare its weekly email.

stdlib only. Default is a dry run for email; --send dispatches through Outlook.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import urllib.request
import urllib.parse

from funding_common import market_health, change_text, observations

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / '_wiki/_data'
TOOLS = ROOT / '_wiki/_tools'
REPORTS = DATA / 'credit-monitor'
LIVE = 'http://ds-cap-33:8080/wiki/_dashboards/credit-monitor.html'


def summary(config, market, prior=None, errors=(), today=None):
    today = today or dt.date.today()
    health = market_health(market, config, today)
    problems = list(errors) + health['issues']
    lines = [f'AI Credit & Funding — weekly brief — {today}', '',
             'Refresh status: ' + ('PARTIAL / ATTENTION REQUIRED' if problems else 'market refresh complete'),
             f'Market observations: {health["earliest"]} through {health["latest"]} (Bloomberg local terminal).',
             f'Research ledger as of {config["asof"]}; market refreshes do not advance research dates.', '',
             'MARKET MOVES — latest completed sessions',
             'Positive changes mean higher spread or yield. Actual baseline dates are shown.']
    for s in market.get('series', []):
        pts = observations(s, today)
        if pts:
            date, last = pts[-1]
            lines += [f'- {s["label"]}: {last:.{s.get("decimals", 2)}f}{s.get("unit", "")} on {date}.',
                      f'  1w: {change_text(s, 7, today)}; 1m: {change_text(s, 30, today)}.',
                      f'  Source: Bloomberg {s["ticker"]}, {s.get("field", "PX_LAST")}, observation {date}.']
    lines += ['', 'FINANCING EVIDENCE']
    if prior is None:
        lines.append('Initial retained baseline; no prior weekly review exists. Do not interpret the full ledger as new this week.')
        changes = []
    else:
        def key(d):
            return d.get('deal_id') or (d['date'], d['issuer'], d['instrument'])
        old = {key(d): d for d in prior.get('deals', [])}
        changes = [('Added' if key(d) not in old else 'Revised', d) for d in config['deals'] if old.get(key(d)) != d]
        if not changes:
            lines.append('No changes recorded in the financing ledger since the prior retained review. This does not establish that there were no market announcements.')
    for kind, deal in changes:
        lines.append(f'- {kind}: {deal["issuer"]} | {deal["date"]} | {deal["instrument"]} | {deal["size"]} | {deal["pricing"]}. {deal["note"]} Source: {deal["source"]}.')
    if config.get('weekly_review'):
        review = config['weekly_review']
        lines += [f'Research review: {review.get("reviewed_at", "undated")} — {review.get("summary", "")}',
                  'Review sources: ' + '; '.join(review.get('sources', []))]
    lines += ['', 'RESEARCH WATCHPOINTS — dated assessments, not fresh market marks']
    for item in config.get('scoreboard', []):
        if item['status'] in ('serious', 'critical', 'gap'):
            lines.append(f'- {item["signpost"]}: {item["read"]} Source: {item["source"]}.')
    overdue = [w for w in config.get('watch', []) if len(w['date']) == 10 and w['date'] < today.isoformat()]
    lines += ['', 'COVERAGE & NEXT CHECKS',
              f'- Research evidence date: {config["asof"]}. Older source observations remain explicitly dated.',
              '- Individual-bond market coverage: ' + (f'{len(config["bonds"])} configured instruments.' if config.get('bonds') else 'not connected; project-bond yields are historical broker snapshots.'),
              f'- {len(overdue)} past-dated watchlist events need outcome review; elapsed dates alone do not establish outcomes.']
    for error in problems:
        lines.append('- Refresh limitation: ' + error)
    lines += ['', 'Dashboard: ' + LIVE, 'Compute-deal timeline: http://ds-cap-33:8080/wiki/themes/ai-compute-deals.md',
              'Attached: a dated, self-contained copy of the credit dashboard.', '',
              'Capstone internal research. Announcements, MOUs, guarantees, committed funding and delivered capacity retain distinct bases.']
    return '\n'.join(lines) + '\n'


def run_step(script, timeout=180):
    result = subprocess.run([sys.executable, str(TOOLS / script)], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout,
                            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    if result.stdout:
        print(result.stdout.strip())
    return result.returncode, result.stderr.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-fetch', action='store_true', help='Prepare a labeled retained-data preview without a Bloomberg request.')
    parser.add_argument('--send', action='store_true', help='Send the weekly email via the existing Outlook account.')
    args = parser.parse_args()
    if args.skip_fetch and args.send:
        parser.error('--skip-fetch is for preview only; cannot combine with --send')
    REPORTS.mkdir(parents=True, exist_ok=True)
    lock = REPORTS / 'refresh.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit('Refresh lock exists. Verify whether the recorded process is running before removing it.')
    os.write(fd, f'{os.getpid()} {dt.datetime.now().isoformat()}'.encode())
    os.close(fd)
    try:
        today = dt.date.today().isoformat()
        subject = f'AI Credit & Funding | Weekly summary | {today}'
        receipt = REPORTS / 'email-receipts' / (hashlib.sha256(subject.encode()).hexdigest() + '.json')
        exports = REPORTS / 'exports'
        exports.mkdir(exist_ok=True)
        bodypath = exports / f'{today}-email.txt'
        attachment = exports / f'{today}-credit-monitor.html'
        if receipt.exists():
            print('An email attempt already exists; retaining the exact report artifacts. Verify before retrying.')
            if args.send:
                return subprocess.run(['powershell.exe', '-NoProfile', '-File', str(TOOLS / 'send_credit_email.ps1'),
                    '-BodyPath', str(bodypath), '-AttachmentPath', str(attachment), '-Subject', subject, '-Verify']).returncode
            return 0
        errors = []
        if args.skip_fetch:
            errors.append('Preview only: Bloomberg refresh was skipped; retained observations used.')
        else:
            try:
                code, stderr = run_step('fetch_funding.py')
                if code:
                    errors.append('Bloomberg refresh failed; previous dataset retained. ' + stderr[-1500:])
            except subprocess.TimeoutExpired:
                errors.append('Bloomberg refresh timed out; previous dataset retained.')
        config = json.loads((DATA / 'funding_deals.json').read_text(encoding='utf-8'))
        market = json.loads((DATA / 'funding_market.json').read_text(encoding='utf-8'))
        code, stderr = run_step('build_funding_monitor.py')
        if code:
            raise RuntimeError('Dashboard build failed: ' + stderr)
        dashboard = ROOT / '_wiki/_dashboards/credit-monitor.html'
        try:
            with urllib.request.urlopen(LIVE, timeout=25) as response:
                if response.read() != dashboard.read_bytes():
                    errors.append('Live dashboard differs from the generated file; publication needs attention.')
        except Exception as exc:
            errors.append(f'Could not verify internal dashboard publication: {exc}')
        snapshots = REPORTS / 'research-history'
        snapshots.mkdir(exist_ok=True)
        older = sorted(p for p in snapshots.glob('*.json') if len(p.stem) == 10 and p.stem < today)
        prior = json.loads(older[-1].read_text(encoding='utf-8')) if older else None
        archive = snapshots / f'{today}.json'
        if not archive.exists():
            archive.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
        body = summary(config, market, prior, errors)
        bodypath.write_text(body, encoding='utf-8')
        export_html = re.sub(r'href="(?!#)([^"]+)"',
            lambda match: 'href="' + urllib.parse.urljoin(LIVE, match.group(1)) + '"',
            dashboard.read_text(encoding='utf-8'))
        attachment.write_text(export_html, encoding='utf-8')
        (REPORTS / 'latest-brief.txt').write_text(body, encoding='utf-8')
        health = market_health(market, config)
        audit = {'run_at': dt.datetime.now().isoformat(timespec='seconds'), 'subject': subject,
                 'status': 'complete' if not errors and health['ok'] else 'partial', 'errors': errors + health['issues'],
                 'market_fetched_at': market.get('fetched_at'), 'market_dates': health,
                 'research_asof': config['asof'], 'email_requested': args.send,
                 'body': str(bodypath), 'attachment': str(attachment),
                 'input_sha256': {name: hashlib.sha256((DATA / name).read_bytes()).hexdigest()
                                  for name in ('funding_deals.json', 'funding_market.json')}}
        auditpath = REPORTS / f'{today}-run.json'
        auditpath.write_text(json.dumps(audit, indent=2), encoding='utf-8')
        print(json.dumps(audit, indent=2))
        if args.send:
            result = subprocess.run(['powershell.exe', '-NoProfile', '-File', str(TOOLS / 'send_credit_email.ps1'),
                '-BodyPath', str(bodypath), '-AttachmentPath', str(attachment), '-Subject', subject, '-Send'])
            if result.returncode:
                return result.returncode
        return 0 if audit['status'] == 'complete' else 1
    finally:
        lock.unlink(missing_ok=True)


if __name__ == '__main__':
    sys.exit(main())
