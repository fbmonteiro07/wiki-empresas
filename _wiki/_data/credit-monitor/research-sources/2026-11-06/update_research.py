"""Apply the bounded 2026-11-06 primary-source credit review; preserve pre-edit bytes."""
import copy
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path.cwd()
WIKI = ROOT / '_wiki'
LEDGER = WIKI / '_data/funding_deals.json'
DAY = '2026-11-06'
NOW = dt.datetime.now().isoformat(timespec='seconds')
SRC = WIKI / '_data/credit-monitor/research-sources' / DAY
ARCH = WIKI / '_data/credit-monitor/research-history' / (dt.datetime.now().strftime('%Y-%m-%dT%H%M%S') + '-pre-edit')
URL = {
 'ORCL': 'https://www.sec.gov/Archives/edgar/data/1341439/000119312526447507/d131790d8k.htm',
 'MSFT': 'https://www.sec.gov/Archives/edgar/data/789019/000119312526447173/d178557d8k.htm',
 'META': 'https://www.sec.gov/Archives/edgar/data/1326801/000119312526450074/d166273d8k.htm',
 'META_EUR': 'https://www.sec.gov/Archives/edgar/data/1326801/000119312526447522/d154804dfwp.htm',
 'GOOG': 'https://www.sec.gov/Archives/edgar/data/1652044/000119312526449835/d174184d8k.htm',
 'AMZN': 'https://www.sec.gov/Archives/edgar/data/1018724/000101872426000040/amzn-20260930.htm',
 'ANTH': 'https://www.sec.gov/Archives/edgar/data/2130357/000162828026068676/anthropicpbc-sx1ax1.htm',
 'IREN': 'https://iren.gcs-web.com/news-releases/news-release-details/iren-reports-q1-fy27-results',
}

d = json.loads(LEDGER.read_text(encoding='utf-8'))
assert not d.get('weekly_review', {}).get('reviewed_at', '').startswith(DAY), 'Already reviewed; inspect before rerunning.'
old = copy.deepcopy(d)
files = [LEDGER, WIKI/'themes/ai-compute-deals.md', WIKI/'_meta/outcomes.md'] + [WIKI/(x+'.md') for x in ['ORCL','META','MSFT','GOOG','AMZN','ANTHROPIC']]
original = {p: p.read_bytes() for p in files}
ARCH.mkdir(parents=True, exist_ok=False)
manifest = []
for p, b in original.items():
    rel = p.relative_to(WIKI)
    dest = ARCH / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b)
    manifest.append({'file':str(rel), 'sha256':hashlib.sha256(b).hexdigest(), 'bytes':len(b)})
(ARCH/'manifest.json').write_text(json.dumps({'archived_at':NOW,'files':manifest},indent=2),encoding='utf-8')

def deal(ident, date, issuer, category, instrument, size, pricing, counterparty, note, source_name, source_date, url, status):
    return dict(deal_id=ident,date=date,issuer=issuer,category=category,instrument=instrument,size=size,
                pricing=pricing,counterparty=counterparty,note=note,source=source_name+' — '+url,
                source_date=source_date,recorded_at=DAY,evidence_status=status)

new = [
 deal('ORCL-CAPITAL-FIN-20261028','2026-10-28','ORCL','Hyperscaler capital markets',
      'Common stock and five senior-note tranches; November 4 closing', '$10bn common offering and $10bn aggregate note principal',
      'Notes: 7.000% 2029; 7.450% 2031; 7.850% 2033; 8.000% 2037; 8.650% 2046 (coupons)',
      'Public equity and unsecured-note investors',
      '8-K confirms 86,206,897 common shares issued at the November 4 closing and $10bn notes issued/sold that day. Executes the existing October 28 $20bn capital-markets plan, excluding refinancing; no additional $20bn increment. Timeline already recorded this close November 5. General corporate uses are not ring-fenced AI spending. Does not confirm the separate chip-lease proposal or compute delivery.',
      'Oracle / 8-K Item 8.01 filed 2026-11-04; original Investor Day 2026-10-28','2026-11-04',URL['ORCL'],
      'filed stock closing and notes issuance; same existing capital plan'),
 deal('DEQ-MSFT-20261029-1','2026-10-29','MSFT','Hyperscaler debt',
      'Ten senior unsecured-note tranches issued November 4','$25bn aggregate principal',
      'Fixed coupons 4.850%-6.350%, maturities 2028-2066; two floating-rate tranches mature 2028/2029',
      'Public unsecured-note investors',
      'November 4 8-K confirms issuance under the October 29 underwriting agreement. Reuses the capital-raising register ID; do not count pricing and issuance twice. Corporate debt financing, not a new compute contract or proof of delivered capacity. Coupon levels are not credit spreads.',
      'Microsoft / 8-K Item 8.01 filed 2026-11-04','2026-11-04',URL['MSFT'],'filed notes issued'),
 deal('DEQ-META-20261103-1','2026-11-03','META','Hyperscaler debt',
      'Five US-dollar senior-note tranches completed November 5','$15bn aggregate principal',
      '5.850% 2031; 6.250% 2033; 6.550% 2036; 7.350% 2046; 7.500% 2056 (coupons)',
      'Public unsecured-note investors',
      'November 5 8-K confirms completion. Separate debt instrument from the preferred/common-forward/Class C framework META-CLASSC-FIN-20261021 and the euro offering. No additional compute MW or contract TCV.',
      'Meta / 8-K Item 8.01 filed 2026-11-05','2026-11-05',URL['META'],'filed offering completed'),
 deal('DEQ-META-20261104-1','2026-11-04','META','Hyperscaler debt',
      'Six euro-note tranches priced; November 12 settlement expected','EUR 9bn aggregate principal; not yet closed',
      '4.300% 2031; 4.650% 2033; 4.900% 2035; 5.400% 2038; 6.050% 2044; 6.400% 2065 (coupons)',
      'Euro-note investors',
      'November 4 final pricing terms expect November 12 settlement (T+5). Priced financing is not received proceeds. Keep EUR basis; no USD translation or sum with dollar issues. Same capital-raising register ID, separate from Meta USD debt and equity forwards.',
      'Meta / final pricing term sheet, FWP filed 2026-11-04','2026-11-04',URL['META_EUR'],'filed pricing; settlement future'),
 deal('DEQ-GOOG-20261102-1','2026-11-02','GOOG','Hyperscaler debt',
      'Seven euro-note tranches closed November 5','EUR 6bn aggregate principal',
      '2028 floating-rate notes; fixed coupons 3.700%-5.250%, maturities 2028-2045',
      'Euro-note investors',
      'November 5 8-K confirms closing. Native EUR principal retained; no USD conversion or incremental compute commitment. Reuses the capital-raising register ID for the same offering.',
      'Alphabet / 8-K Item 8.01 filed 2026-11-05','2026-11-05',URL['GOOG'],'filed offering closed'),
 deal('DEQ-AMZN-20261030-1','2026-10-30','AMZN','Supplier financing',
      'Secured supplier-loan facility for technology infrastructure','Up to approximately $80bn; future discretionary borrowings',
      'Variable rate; each borrowing matures five years after its draw',
      'Supplier; specific counterparty not named in the reviewed Note 5',
      'October 30 10-Q permits discretionary borrowings Q1 2027 through Q3 2028; size depends on purchase orders and pricing. Secured by certain purchased technology-infrastructure assets. Facility availability is not current drawn debt, cash proceeds or delivered equipment. Existing October 30 timeline context and capital-register ID; this addition is reconciliation, not a November 6 commitment.',
      'Amazon / Q3 10-Q Note 5 filed 2026-10-30','2026-10-30',URL['AMZN'],'filed facility; future draws discretionary'),
 deal('DEQ-ANTHROPIC-20260904-1','2026-09','Anthropic','Lab credit facility',
      'Amended and restated senior secured revolving credit facility','$15bn capacity; no borrowings at 2026-09-30; $205m standby LCs outstanding',
      'Benchmark plus margin; September 4, 2031 maturity subject to springing provisions',
      'Syndicated lenders; company credit agreement',
      'Historical backfill from November 2 S-1/A: September agreement replaces the prior $3.25bn revolver. The reviewed narrative gives the agreement month; the stable register ID is retained without inventing an exact signing day. Full facility supports letters of credit, so no borrowings does not mean zero utilization. Minimum liquidity $5bn from the quarter ending December 31, 2026. No new November proceeds; separate from the North Star SPV and conditional rent-note facility.',
      'Anthropic / S-1/A filed 2026-11-02, Credit Facility and subsequent-event provisions','2026-11-02',URL['ANTH'],'filed historical facility; no borrowings as of September 30'),
 deal('DEQ-ANTHROPIC-20260528-1','2026-Q2','Anthropic','Lab equity',
      'Series H-1 and H-2 redeemable convertible preferred stock','$65.2bn gross proceeds; completed in Q2 2026',
      '$589.0095 per share, pre-split, per the filed financial-statement note',
      'Series H preferred investors',
      'Historical backfill, not capital raised this week. November 2 S-1/A F-47 states the sale completed in Q2 2026. Retains the existing register ID (May 28 announcement); the filed quarter is used for completion-date precision. Do not add Series G-2 proceeds, partner NPA capacity, IPO scenarios or this amount to North Star financing.',
      'Anthropic / S-1/A filed 2026-11-02, financial-statement note F-47','2026-11-02',URL['ANTH'],'filed historical equity proceeds; Q2 completion'),
]
existing = {r.get('deal_id') for r in d['deals']}
assert all(r['deal_id'] not in existing for r in new)
d['deals'].extend(new)
meta = next(r for r in d['deals'] if r.get('deal_id')=='META-CLASSC-FIN-20261021')
prior_meta = copy.deepcopy(meta)
meta['size'] = '$12.5bn base preferred closed; $25bn base common forwards plus 6m option shares; ~$60bn ATM planned'
meta['note'] = ('October 29 preferred closing remains confirmed. November 5 8-K now confirms full exercise on November 4 of the 6m-share common option and additional forwards on substantially similar terms, alongside the 40m base shares. This supersedes the prior unverified common-option status. No common-forward cash settlement established; contractual settlement remains by November 19, 2027, subject to terms. Preferred option exercise and supplier indications remain unverified. The ~$60bn Class C ATM remains prospective and charter effectiveness January 19, 2027. No sum of deferred forwards and planned ATM is treated as cash received.')
meta['source'] = 'Meta / 8-K 2026-11-05 Item 8.01 (common option), 8-K 2026-10-29 (preferred close), 424B5 filings 2026-10-28 — '+URL['META']+' ; https://www.sec.gov/Archives/edgar/data/1326801/000119312526438017/d183592d8k.htm'
meta['source_date']='2026-11-05'; meta['reviewed_at']=DAY
meta['evidence_status']='filed preferred closing and common-option exercise; forward cash deferred; ATM planned'

for s in d['scoreboard']:
    if s['signpost']=='Supply absorption':
        s.update(read='Primary filings confirm November 4-5 closings for Oracle ($10bn stock / $10bn notes), Microsoft ($25bn notes), Meta ($15bn USD notes) and Alphabet (EUR 6bn notes). Meta EUR 9bn remains priced for November 12. This establishes access for named issuers, not a comprehensive weekly or YTD issuance aggregate. Historical JPM/MS universe totals retain their source dates.',source='Oracle and Microsoft 8-Ks 2026-11-04; Meta and Alphabet 8-Ks 2026-11-05; Meta FWP 2026-11-04')
    elif s['signpost']=='Duration channel':
        s.update(read='Oracle completed the public-capital legs of its October 28 plan on November 4. The positive-FCF target for 2H FY28, lease-adjusted leverage and vendor-financing dependence still require execution. Closing does not validate undisclosed chip-lease terms or site permitting.',source='Oracle 8-K 2026-11-04; Investor Day / Hilary Maxson 2026-10-28')
    elif s['signpost']=='Hyperscaler financing flexibility':
        s.update(read='Completed corporate note offerings broaden financing access. Meta also exercised the 6m common-share forward option November 4, but forward cash settlement remains deferred. Amazon disclosed up to ~$80bn supplier borrowing at its discretion in 2027-28, not current proceeds. Native-currency principal, debt, equity and contingent capacity remain separate.',source='Meta 8-K 2026-11-05; Amazon 10-Q Note 5 2026-10-30; named-issuer filings November 4-5')
d['scoreboard'].append({'signpost':'IREN funding conditions and deployment','status':'serious','read':'IREN reports $15bn remaining FY27 capex from September 30, against $9bn cash/committed GPU finance/prepayments and $6bn targeted sources. The $9bn includes restricted cash, undrawn facilities and prepayments not received; fully funded refers to the 0.3GW IT program with conditions. The >$4bn operating-ARR target moves from year-end to January 31, possibly end-February 2027. Horizon 1 is in service for Microsoft; delivered MW is not specified. Aggregate timing changes are not assigned to Microsoft.','source':'IREN / Daniel Roberts, Q1 FY27 release 2026-11-05, footnotes 4-5 and 11 — '+URL['IREN']})

for w in d['watch']:
    if w['event'].startswith('Oracle: test October 28'):
        w['event']='Oracle: November 4 stock/notes closing resolves the capital-markets execution component of the October 28 plan. Continue checking vendor-financing terms, lease-adjusted leverage, FCF timetable and site permits; no chip lease confirmed (8-K November 4).'
    elif w['event'].startswith('Meta common forwards:'):
        w['event']='Meta common forwards: latest contractual settlement date. November 5 8-K confirms November 4 exercise of all 6m common-option shares; verify actual forward settlements/proceeds, preferred option exercise and Class C ATM launch. Common-option exercise is not cash settlement.'
    elif w['event'].startswith('Read full JPM'):
        w['event']='Read full JPM / Spear-Degen November 6 Weekly IG TMT Review; MS / Tyler-Guerrero November 2 ORCL Credit; MS / Tirupattur November 6 AI-credit podcast; BofA November 5 HY & Loan Strategy. This review screened Outlook metadata/previews only; no numerical conclusion adopted from headlines.'
d['watch'].extend([
 {'date':'2026-11-12','event':'Meta EUR 9bn notes: expected settlement per November 4 FWP; obtain filed close before classifying proceeds as received.'},
 {'date':'2026-12-31','event':'Anthropic: first quarter-end $5bn minimum-liquidity test under the September revolver per November 2 S-1/A. Last draw observation September 30: no borrowings, $205m standby LCs. Refresh actual draws/LCs and IPO pricing; no outcome inferred today.'},
 {'date':'2027-01-31','event':'IREN: revised >$4bn operating-ARR target, potentially extending to end-February; verify escrow releases, financing availability and prepayment receipts. November 5 company release; preserve 0.3GW IT scope and avoid assuming all $9bn is unrestricted cash.'},
 {'date':'ongoing','event':'Amazon: track any actual borrowing under the up-to-$80bn supplier facility; disclosed discretionary window Q1 2027-Q3 2028, five-year maturity per draw (10-Q filed October 30).'}
])
d['asof']='2026-11-05'
d['weekly_review']={
 'reviewed_at':NOW,'window_start':'2026-10-30','window_end':DAY,
 'summary':('Primary evidence through November 5. Oracle completed the same October 28 capital plan ($10bn common/$10bn notes), Microsoft issued $25bn notes, Meta completed $15bn USD notes, and Alphabet closed EUR 6bn notes. Meta EUR 9bn is priced for November 12, not yet closed. Amounts retain native currencies; no aggregate cash total or new compute commitment inferred.\n'
 'Meta also exercised the full 6m-share common-forward option November 4; cash settlement remains deferred. Amazon disclosed an up-to-~$80bn supplier facility with discretionary draws in Q1 2027-Q3 2028, not cash received. Anthropic additions are historical backfills: $65.2bn Series H completed in Q2; $15bn September revolver had no borrowings and $205m standby LCs at September 30. These are not new November raises.\n'
 'IREN November 5 funding and deployment disclosures are reconciled to the existing timeline: restricted cash, undrawn capacity and unreceived prepayments remain conditional; no duplicate commitment added. Operating-ARR timing moved to January/possibly February; no inference that Microsoft caused or bore the aggregate delay.\n'
 'Coverage: graph context; relevant company Debate/Changelogs, canonical assumptions and compute-deal history; full-corpus financing search; selected original SEC offering/credit-facility provisions and IREN release footnotes. Outlook subject/metadata/previews supplied broker leads, not full-report conclusions. No exhaustive filing/mailbox audit claimed. No new funded North Star, Apollo/SpaceX lease close, Nebius draw or OpenAI chip-finance/equity close established in this bounded review. Past-dated AVGO/SPCX watch outcomes and site permits remain unverified. Old broker snapshots and issuance totals retain original dates. Quote gaps and market baselines are reported separately by the refresh.'),
 'sources':[
  'Oracle / 8-K 2026-11-04 — '+URL['ORCL'], 'Microsoft / 8-K 2026-11-04 — '+URL['MSFT'],
  'Meta / 8-K 2026-11-05 and FWP 2026-11-04 — '+URL['META']+' ; '+URL['META_EUR'],
  'Alphabet / 8-K 2026-11-05 — '+URL['GOOG'], 'Amazon / 10-Q Note 5 2026-10-30 — '+URL['AMZN'],
  'Anthropic / S-1/A 2026-11-02, F-47 and Credit Facility — '+URL['ANTH'],
  'IREN / Daniel Roberts, Q1 FY27 release 2026-11-05 — '+URL['IREN'],
 ]}
d.setdefault('history',[]).append({'recorded_at':NOW,'reason':'November 6 bounded primary-source credit review; distinguish closings, pricing, future draws and historical backfills.',
 'archive':str((ARCH/'_data/funding_deals.json').relative_to(WIKI)).replace('\\','/'),
 'sha256':hashlib.sha256(original[LEDGER]).hexdigest(),'previous_asof':old['asof'],'previous_weekly_review':old.get('weekly_review'),
 'previous_scoreboard':old['scoreboard'],'previous_watch':old['watch'],'changed_deals':[{'deal_id':meta['deal_id'],'previous':prior_meta}],
 'added_deal_ids':[r['deal_id'] for r in new]})

texts = {p: b.decode('utf-8') for p,b in original.items() if p.suffix=='.md'}
def prepend_section(s, pattern, text):
    m=re.search(pattern,s,re.M)
    assert m, pattern
    return s[:m.end()]+'\n\n'+text+'\n'+s[m.end():]

for ticker in ['ORCL','META','MSFT','GOOG','AMZN','ANTHROPIC']:
    p=WIKI/(ticker+'.md'); s=texts[p]; superseded=[]
    if ticker=='ORCL':
        for line in s.splitlines():
            if line.startswith('- 🆕 **2026-11-03 — the $20bn priced'):
                superseded.append(line)
                s=s.replace(line,line.replace('both offerings close 2026-11-04','both offerings were subsequently confirmed closed/issued 2026-11-04 (Oracle [8-K filed November 4]('+URL['ORCL']+'))'),1)
        oldphrase='Timing of the $10bn equity and $10bn debt is not given.'
        if oldphrase in s:
            superseded.append('October 28 vintage: '+oldphrase)
            s=s.replace(oldphrase,'Subsequent update: both public offerings closed/issued November 4 (Oracle 8-K filed November 4).',1)
        bullet='**2026-11-06 credit review — capital-plan execution confirmed.** Oracle\'s [November 4 8-K, Item 8.01]('+URL['ORCL']+') confirms the common offering closed November 4 with **86,206,897 shares** and **$10bn notes issued/sold**. This executes the existing **$10bn equity / $10bn gross-debt** plan (**ORCL-CAPITAL-FIN-20261028**), already recorded in the timeline November 5. It is not another $20bn increment, a chip-lease confirmation or a delivered-capacity milestone. FCF targets, vendor financing and permits still require separate evidence.'
    elif ticker=='META':
        m=re.search(r'^\*\*2026-10-30 credit update[^\n]+',s,re.M);assert m
        superseded.append(m.group())
        bullet='**2026-11-06 credit review — common-option exercise and separate debt closings.** The [November 5 8-K, Item 8.01]('+URL['META']+') confirms that on **November 4** underwriters exercised **all 6m additional common shares** and Meta entered additional forwards on substantially similar terms. The 40m base forward and its **$25bn gross offering** remain distinct from cash settlement, due by **November 19, 2027** subject to terms. The **$12.5bn preferred base** closed October 29; preferred option exercise and the planned **~$60bn Class C ATM** remain unverified. Same equity ID **META-CLASSC-FIN-20261021**. The same 8-K confirms **$15bn USD notes completed November 5** (**DEQ-META-20261103-1**). Separately, the [November 4 euro pricing sheet]('+URL['META_EUR']+') prices **EUR 9bn** for expected **November 12 settlement** (**DEQ-META-20261104-1**); no close assumed, no FX aggregation.'
        s=s[:m.start()]+s[m.end():]
    elif ticker=='MSFT':
        bullet='**2026-11-06 credit review — corporate financing completed.** Microsoft\'s [November 4 8-K, Item 8.01]('+URL['MSFT']+') confirms **$25bn of senior unsecured notes issued** under the October 29 agreement: ten tranches, including two floating-rate series and fixed coupons **4.850%-6.350%**, with maturities **2028-2066**. Stable capital-register ID **DEQ-MSFT-20261029-1**. This is corporate debt, separate from landlord project bonds and any delivered AI capacity. The historical through-August zero-issuance observation below retains its date. IREN\'s [November 5 release]('+URL['IREN']+') confirms Horizon 1 in service for Microsoft, but discloses no delivered MW and does not attribute its aggregate ARR delay to Microsoft; the earlier Jefferies counterparty identification remains speculation.'
    elif ticker=='GOOG':
        bullet='**2026-11-06 credit review — euro-note closing.** Alphabet\'s [November 5 8-K, Item 8.01]('+URL['GOOG']+') confirms **EUR 6bn notes closed November 5**, following the November 2 underwriting agreement: one 2028 floating-rate series and fixed coupons **3.700%-5.250%** across **2028-2045**. Stable register ID **DEQ-GOOG-20261102-1**. Keep native EUR principal and distinguish corporate funding from compute contracts, guarantees and delivered capacity.'
    elif ticker=='AMZN':
        bullet='**2026-11-06 credit review — supplier facility draw basis.** [Q3 10-Q Note 5, filed October 30]('+URL['AMZN']+') permits borrowing **up to approximately $80bn** at Amazon\'s discretion **Q1 2027-Q3 2028**, dependent on purchase orders/pricing, at variable rates with **five-year maturity per draw** and security over certain purchased technology infrastructure. No current draw or cash proceeds are established by this disclosure. This reconciles the existing **DEQ-AMZN-20261030-1** and October 30 timeline context; it is not a November 6 commitment or a new compute contract.'
    else:
        bullet='**2026-11-06 credit review — date and utilization clarification.** The [November 2 S-1/A, F-47 and Credit Facility]('+URL['ANTH']+') states that the **$65.2bn gross Series H sale completed in Q2 2026** (**DEQ-ANTHROPIC-20260528-1**). The **September $15bn revolver** (**DEQ-ANTHROPIC-20260904-1**) replaces $3.25bn; at **September 30** there were **no borrowings drawn and $205m standby LCs outstanding**. The $5bn minimum-liquidity covenant begins with the quarter ending **December 31, 2026**; maturity is September 4, 2031, subject to springing terms. These are historical funding disclosures, not November proceeds or a priced IPO, and remain separate from North Star and the conditional rent-note facility.'
    s=prepend_section(s,r'^## (?:Current state|State of play)[^\n]*$',bullet)
    change='- **2026-11-06 — Friday credit review.** '+('Revised current financing status; prior values retained below. ' if superseded else 'Added dated primary financing/execution evidence; no prior forecast, rating or price target superseded. ')+ 'Reconciled the funding ledger and compute-deal financing history; corporate capital is not compute delivery.'
    if superseded: change+='\n\n  **Prior dated wording preserved:**\n\n'+'\n\n'.join('  '+v for v in superseded)
    s=prepend_section(s,r'^## Changelog\s*$',change)
    texts[p]=s

p=WIKI/'themes/ai-compute-deals.md';s=texts[p]
assert all(r['deal_id'] not in s for r in new if r['deal_id'] not in ['ORCL-CAPITAL-FIN-20261028']), 'Existing financing ID found; inspect duplicate before proceeding.'
intro=('## 2026-11-06 recorded — corporate financing review; no incremental compute commitments\n\n'
 'Duplicate check: reviewed company pages, this timeline and the capital-raising register before recording. **ORCL-CAPITAL-FIN-20261028** already carries the November 4 close (recorded November 5); no duplicate closing event is added. **META-CLASSC-FIN-20261021** receives only the newly filed common-option exercise. Existing capital-register **DEQ** IDs below are reused for distinct corporate instruments; they are financing context, not new compute IDs, MW or contract TCV. Amazon\'s October 30 supplier-facility context is assigned its existing register ID, without another commitment. Anthropic\'s Series H and revolver are historical backfills. IREN\'s November 5 disclosure is already recorded above/in the history and is not duplicated.\n\n')
idx=s.find('\n');s=s[:idx+1]+'\n'+intro+s[idx+1:]
history='### Recorded 2026-11-06 — primary financing milestones and historical backfills\n\n| Event / source date | Stable ID | Original terms and subsequent evidence | Execution / reconciliation |\n|---|---|---|---|\n'
history+='| November 4 exercise; November 5 filing | META-CLASSC-FIN-20261021 | Prior: October 28 common prospectus had 40m base shares plus a 6m-share option; October 30 review left exercise unverified. Now the [Meta 8-K]('+URL['META']+') confirms full 6m exercise and additional forwards November 4. | Common-option status resolved; no forward cash settlement or preferred-option exercise assumed. Original preferred/base/ATM terms retained. |\n'
for r in new:
    if r['deal_id']=='ORCL-CAPITAL-FIN-20261028':continue
    history+='| '+r['date']+' original scope; source '+r['source_date']+'; recorded '+DAY+' | '+r['deal_id']+' | '+r['instrument']+' — **'+r['size']+'**. '+r['pricing']+'. ['+r['source'].split(' — ')[0]+']('+r['source'].split(' — ')[-1]+') | '+r['note']+' |\n'
s=prepend_section(s,r'^## Confirmations, revisions and execution history\s*$',history)
s=prepend_section(s,r'^## Changelog\s*$', '- **2026-11-06 — Friday credit review:** reconciled Oracle\'s already-recorded closing; appended Meta common-option confirmation and seven existing capital-register IDs for corporate debt, supplier finance and historical lab funding. Preserved original dates, native currencies, prior Meta status and all prior terms. No incremental compute commitment; IREN update already present. Company Changelogs and funding-ledger pre-edit archive preserve old values.')
texts[p]=s

p=WIKI/'_meta/outcomes.md';s=texts[p]
outcomes=[
 '- META 2026-11-04 — neutral — Common-option watch resolved: all 6m additional common shares exercised into forwards; no current cash settlement implied. Preferred option remains unverified. [Meta 8-K November 5]('+URL['META']+').',
]
for line in outcomes:
    signature=' '.join(line.split()[:3])
    assert signature not in s, 'Outcome exists; inspect instead of duplicating.'
anchor='Add lines here after each catalyst resolves. Newest first.'
assert anchor in s;s=s.replace(anchor,anchor+'\n\n'+'\n'.join(outcomes),1);texts[p]=s

# All transformations must succeed before applying; refuse concurrent overwrites.
for p,b in original.items():assert p.read_bytes()==b, 'Concurrent modification: '+str(p)
for p,s in texts.items():p.write_text(s,encoding='utf-8',newline='\n')
LEDGER.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
audit={'reviewed_at':NOW,'archive':str(ARCH.relative_to(WIKI)),'ledger_before_sha256':hashlib.sha256(original[LEDGER]).hexdigest(),
       'ledger_after_sha256':hashlib.sha256(LEDGER.read_bytes()).hexdigest(),'added_ids':[r['deal_id'] for r in new],
       'revised_ids':[meta['deal_id']],'source_urls':URL,'changed_files':[str(p.relative_to(WIKI)) for p in files],
       'coverage_note':'Bounded primary provisions and original company release; full-corpus FTS run; Outlook previews only. Original SEC HTML/text archived; IREN release read through web tool after direct Python TLS-proxy certificate failure.'}
(SRC/'research-update-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'updated':len(files),'deal_count':len(d['deals']),'archive':str(ARCH),'added':audit['added_ids']},indent=2))
