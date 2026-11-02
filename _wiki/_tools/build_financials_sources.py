"""Render the Financials provenance catalog; reads research, writes only dashboards."""
from pathlib import Path
import html,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
WIKI=Path(__file__).resolve().parents[1];DATA=WIKI/'_data/financials';OUT=WIKI/'_dashboards/financials-sources.html'
def esc(x):return html.escape(str(x),quote=True)
def main():
 p=DATA/'source_inventory.json'
 if not p.exists():print('Financials source inventory unavailable; existing catalog retained.');return
 inv=json.loads(p.read_text(encoding='utf-8-sig'));cov=json.loads((DATA/'coverage.json').read_text(encoding='utf-8-sig'));total=cov['totals']
 parts=['''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Financials — source catalog</title><style>
:root{color-scheme:dark;--bg:#121319;--fg:#e7e9ef;--muted:#a8afbd;--line:#313540;--panel:#1c202a;--link:#8eb4ff}html[data-theme="paper"]{color-scheme:light;--bg:#f8fafc;--fg:#1e293b;--muted:#526176;--line:#d8e0e9;--panel:#eaf0f5;--link:#1d5c9b}body{font:14px/1.55 system-ui,sans-serif;margin:32px auto;padding:0 24px;max-width:1450px;background:var(--bg);color:var(--fg)}h1{font-size:28px}a{color:var(--link)}p{max-width:105ch}nav{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}nav a{border:1px solid var(--line);padding:5px 12px;border-radius:5px;text-decoration:none}nav a.active{background:var(--panel);font-weight:700}.muted{color:var(--muted)}section{margin-top:24px}table{width:100%;border-collapse:collapse;font-size:12px}th,td{padding:10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--panel);position:sticky;top:0}td:first-child{white-space:nowrap}code{font-size:11px;overflow-wrap:anywhere}td:nth-child(3){min-width:240px;max-width:520px}.scroll{overflow:auto}.tag{display:inline-block;padding:2px 6px;background:var(--panel);border-radius:3px}@media(max-width:720px){body{padding:0 12px}h1{font-size:23px}th{position:static}}
</style></head><body><p><a href="../index.html#TH-financials">← Financials overview</a></p><h1>Financials — source catalog</h1>''']
 parts.append(f'<p class="muted">Filings/results cut-off: 2026-10-31 (2026-11-02 for MSCI, EFX, TRU, CME, ICE, CBOE, NDAQ, OWL and BLK, added that day); live email review: 2026-11-01 · {total["sec"]} SEC filings · {total["transcript_documents"]} transcript documents / {total["unique_quarter_calls"]} distinct quarterly calls · {total["earnings_exhibits"]} earnings exhibits · {total["commentary_candidates"]} company-commentary entries.</p>')
 parts.append('<p>Publisher links open company/SEC sources; Outlook links open the original email and require mailbox access. Every entry also identifies its downloaded local file. Email bodies and licensed reports remain in the local master archive; this LAN catalog exposes provenance, not those full texts. An email excerpt is not necessarily the complete linked analyst report.</p><p><strong>Archived does not mean fully read.</strong> Review scope records citations or selected passages. Bloomberg consensus (as of the latest estimates refresh) renders on each company page; cite its FY lines, not the CY lines, for fiscal-year claims.</p>')
 parts.append('<nav><a href="#ALL">All companies</a>'+''.join(f'<a href="#{esc(x["ticker"])}">{esc(x["ticker"])}</a>' for x in cov['companies'])+'</nav>')
 for co in cov['companies']:
  tk=co['ticker'];c=co['counts'];parts.append(f'<section id="company-{tk}" data-ticker="{tk}"><h2><a href="../index.html#{tk}">{tk} — {esc(co["name"])}</a></h2><p class="muted">{c["sec"]} filings · {c["unique_quarter_calls"]} distinct quarterly calls · latest 10-Q: period {co["latest_10q_period"]}, filed {co["latest_10q_date"]}. Amounts and source vintages are discussed on the company page.</p><div class="scroll"><table><thead><tr><th>Date</th><th>Type / period</th><th>Document / local archive file</th><th>Publisher / access</th><th>Quality / review scope</th></tr></thead><tbody>')
  records=sorted([x for x in inv['records'] if x['ticker']==tk],key=lambda x:(x['date'],x['kind'],x['path']),reverse=True)
  for x in records:
   typ=x['kind']+(' · '+x.get('fiscal_period','') if x.get('fiscal_period') else '')
   if x.get('period_end'):typ+=' · period '+x['period_end']
   label=x.get('title') or x.get('subject') or x['path'];pub=x.get('sender') or ('SEC EDGAR' if 'SEC' in typ or typ.startswith('Earnings') else 'Company IR' if typ.startswith('Company') else '')
   url=x.get('source_url','');access_label='Original email (Outlook)' if x['kind']=='Outlook research email' else 'Original publisher source';link=f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{access_label} ↗</a>' if url else '<span class="tag">Local archive only</span>'
   fidelity={'cache_at_length_limit':'Cached email excerpt; reached the 9,000-character limit','cached_email_body':'Cached email body; linked report may not be included'}.get(x.get('fidelity',''),x.get('fidelity',''))
   review=x['review_status'].replace('Selected passage emitted for review','Excerpt extracted; analytical review not confirmed')
   parts.append('<tr><td>'+esc(x['date'])+'</td><td>'+esc(typ)+'</td><td>'+esc(label)+'<br><code>'+esc(x['path'])+'</code></td><td>'+esc(pub)+'<br>'+link+'</td><td>'+esc(fidelity)+'<br><span class="muted">'+esc(review)+'</span></td></tr>')
  parts.append('</tbody></table></div></section>')
 parts.append('''<p class="muted">Source: local Financials ingestion manifests, recorded 2026-11-01. Duplicate versions remain separate documents and are deduplicated in quarterly-call and email-identity counts. <a href="../_meta/financials-coverage.md">Coverage ledger</a> · <a href="../_data/financials/validation.json">Validation results</a></p><script>
try{if(localStorage.getItem('wikitheme')==='paper')document.documentElement.dataset.theme='paper';}catch(e){}
function selectCompany(){var t=location.hash.slice(1)||'ALL';if(!document.getElementById('company-'+t))t='ALL';document.querySelectorAll('section[data-ticker]').forEach(function(s){s.hidden=t!=='ALL'&&s.dataset.ticker!==t;});document.querySelectorAll('nav a').forEach(function(a){a.classList.toggle('active',a.hash==='#'+t);});window.scrollTo(0,0);}
window.addEventListener('hashchange',selectCompany);selectCompany();
</script></body></html>''')
 OUT.parent.mkdir(exist_ok=True);OUT.write_text('\n'.join(parts),encoding='utf-8');print(f'Financials source catalog: {len(inv["records"])} entries -> {OUT}')
if __name__=='__main__':main()
