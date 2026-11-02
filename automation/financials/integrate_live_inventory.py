from pathlib import Path
p=Path('automation/financials/extract_usi.py');s=p.read_text(encoding='utf-8-sig').replace("'-layout',str(p/", "'-layout','-enc','UTF-8',str(p/");p.write_text(s,encoding='utf-8')
p=Path('automation/financials/build_inventory.py');s=p.read_text(encoding='utf-8-sig')
def change(a,b):
 global s
 assert a in s,a[:100]
 s=s.replace(a,b)
change("commentary=rows(DATA/'commentary_manifest.json');ir=", "commentary=rows(DATA/'commentary_manifest.json');live=rows(DATA/'live_email_manifest.json');ir=")
change(" for p in (ROOT/tk/'research').glob('*.md'):", " for x in live:\n  if x['ticker']==tk:records.append(dict(x,kind='Outlook research email',status='archived'))\n for p in (ROOT/tk/'research').glob('*.md'):")
change("x['review_scope_recorded']='2026-10-31'", "x['review_scope_recorded']='2026-11-01'")
change("x['kind']=='Cached commentary'", "x['kind'] in {'Cached commentary','Outlook research email'}")
change("Research cut-off: 2026-10-31.", "Filings/results cut-off: 2026-10-31. Live email review: 2026-11-01.")
change("cached commentary candidates.", "commentary documents (cached and live-retrieved versions).")
change("'Cached commentary bodies were capped at 9,000 characters in the original email collection; linked reports may be unavailable.", "'Cached commentary bodies were capped at 9,000 characters in the original email collection. Selected live Outlook messages retrieved on November 1 preserve the connector-returned body; linked reports are not automatically included.")
change("recorded 2026-10-31.", "recorded 2026-11-01.")
change("'as_of':'2026-10-31'", "'as_of':'2026-11-01'")
change("_Recorded 2026-10-31.", "_Recorded 2026-11-01.")
change("distinct cached emails. Cross-company emails can appear under multiple tickers.", "distinct emails. Cached/live versions and cross-company copies can appear as separate documents; identities are deduplicated for the email count.")
change("- Commentary: subject-screened candidates from existing cached emails. The original collection truncated long bodies, so an archived email is not proof that its linked report was obtained. False matches and invitations are preserved under _discovery and excluded.", "- Commentary: subject-screened cached candidates plus 33 selected live Outlook messages reviewed on 2026-11-01 (36 company-specific copies). The old collection truncated long bodies. The live collection preserves the connector-returned body, but neither guarantees the linked report was obtained. False matches and invitations are preserved under _discovery and excluded. This was a targeted 2026 year-to-date search; pagination remains available for broader historical review.")
change("## Open items", "## Live email review audit\n\n[Queries, selection and pagination](../_data/financials/email_review_2026-11-01/search_audit.json) and [live source manifest](../_data/financials/live_email_manifest.json) preserve the audit trail. Canonical matches to older cached messages use sender, normalized subject and received date within one day; report dates and received UTC timestamps are separate. Goldman HOOD/COIN result alerts remain headline-only. The Redburn prediction-market volume conflict is flagged rather than adopted.\n\n## Open items")
# The replacement above introduced literal newlines inside one quoted source line; encode them as escapes.
s=s.replace("'## Live email review audit\n\n[Queries", "'## Live email review audit\\n\\n[Queries").replace("adopted.\n\n## Open items'", "adopted.\\n\\n## Open items'")
p.write_text(s,encoding='utf-8')
print('Inventory includes live email versions and dated review scope.')
