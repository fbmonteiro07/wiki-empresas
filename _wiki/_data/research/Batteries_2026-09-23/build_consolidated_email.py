"""Build a self-contained email from the completed, sourced battery research."""
import html
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).absolute().parent
OUT = ROOT / "exports"
OUT.mkdir(exist_ok=True)
data = json.loads((ROOT / "imports/calculated_shares_and_checks.json").read_text(encoding="utf-8-sig"))
assert all(data["checks"].values())

def table(headers, rows):
    th = ''.join('<th style="padding:9px;border-bottom:2px solid #254c6b;text-align:left;background:#edf3f7">' + html.escape(str(x)) + '</th>' for x in headers)
    tr = ''.join('<tr>' + ''.join('<td style="padding:9px;border-bottom:1px solid #dbe2e8;vertical-align:top">' + html.escape(str(x)) + '</td>' for x in row) + '</tr>' for row in rows)
    return '<table style="border-collapse:collapse;width:100%;font-size:14px;margin:16px 0"><thead><tr>' + th + '</tr></thead><tbody>' + tr + '</tbody></table>'

broad = [data['lithium'][0], data['lithium'][1], data['lithium_prior_ytd'], data['lithium'][2]]
broad_table = table(['Period', 'World, US$bn', 'China, US$bn', 'China share'], [
    [x['period'], f"{x['world_usd']/1e9:.3f}", f"{x['china_usd']/1e9:.3f}", f"{x['china_share_pct']:.1f}%"] for x in broad
])
bess_table = table(['Customs origin', 'Imports, US$m', 'Share of import value'], [
    [x['country'], f"{x['usd']/1e6:.3f}", f"{x['share_pct']:.1f}%"] for x in data['bess_country'][:5]
])

body = '''
<p>Felipe,</p>
<p><strong>Batteries are increasingly a power-infrastructure theme, with distinct opportunities in grid storage, AI backup, and distributed energy networks.</strong> The strongest conclusion from the saved feed and your emails is that deployment growth is becoming broader than EVs. The harder investment question is who captures profitable system revenue: cell makers, module suppliers, integrators, or operators.</p>
<p>Coatue's posts fit this infrastructure thesis, particularly through Base Power. On sourcing, the official US data require a distinction: <strong>China remains the largest individual origin of broad lithium-ion imports, but it is not the largest reported origin in the new category for housed storage systems.</strong> Neither measure identifies all Chinese cell content. Base Power's cell supplier remains unverified.</p>

<p style="margin-top:28px;font-size:19px;color:#173e5b"><strong>What the last 90 days say</strong></p>
<p><strong>Stationary storage has independent demand drivers.</strong> The saved posts from ARK (June 25), TrendForce (July 10), Coatue (August 14), and Gavin Baker (August 30) increasingly describe batteries as infrastructure for generation, grid flexibility, and AI. Broker emails give the economic detail: <strong>BofA's Taekyoung Ha, September 1</strong>, identifies US stationary storage as a principal growth driver for Korean manufacturers. The same day's global note from <strong>Ming Hsun Lee and colleagues</strong> reports July EV battery installations up <strong>22% year over year globally</strong>, versus down <strong>22% for Korean suppliers</strong>. Supplier and regional divergence matters; weak Korean EV exposure does not establish a global EV demand collapse.</p>
<p><strong>AI backup is about architecture and system content.</strong> In <em>Rubin moves batteries out of the tray</em>, <strong>UBS Tim Bush and colleagues, September 14</strong> (received September 13), forecasts near-rack battery backup revenue of <strong>$2.5bn in 2026 and $12.8bn in 2030</strong>, or <strong>$3.1bn and $15.9bn including capacitor backup</strong>. Building UPS is excluded. UBS models only <strong>40–50% battery-backup attachment for Rubin-class systems</strong>, allowing reserve capacity to sit elsewhere. These are broker assumptions, not NVIDIA commitments.</p>
<p>UBS estimates cells at <strong>10–15% of backup-system cost</strong> under its five-minute-duration and system-cost assumptions. The implication is that qualified modules, power conversion, and integration can capture value beyond cells. <strong>Citi Kyna Wong and colleagues, July 17</strong>, highlights Panasonic, Dynapack, and AES-KY in the battery-module chain; AES-KY should not be confused with the US utility AES Corporation. Citi's broader framing and UBS's near-rack forecast should not be added together.</p>
<p>There is already a useful earnings check: <strong>Morgan Stanley sales' Amir Amerian, July 30</strong>, describes Panasonic's overall beat and raise, but data-center batteries approximately in line or slightly below expectations. Other businesses contributed to the beat. His personal bullish view differed from research analyst Kazuo Yoshikawa's Equal-weight rating. For technical context, <a href="https://developer.nvidia.com/blog/designing-production-ready-battery-energy-storage-systems-for-ai-factories/">NVIDIA's June 10 explanation</a>, outside the review window, says rack-level smoothing is improving and campus storage manages residual fluctuations and wider site duties. Sizing all GPU volatility as a grid-level battery requirement would overstate the inference.</p>

<p style="margin-top:28px;font-size:19px;color:#173e5b"><strong>What Coatue adds</strong></p>
<p><strong>August 14 — deployment speed.</strong> Coatue's chart, attributed to BloombergNEF, says annual capacity additions increased from <strong>10GW to 100GW in four years for storage, eight for solar, and fifteen for wind</strong>. Storage excludes pumped hydro. This compares annual power-capacity additions, not cumulative installations, GWh, electricity generation, or profits. The chart was checked on <a href="https://www.coatue.com/c/takes/chart-of-the-day-2026-08-14">Coatue's official page</a>; BloombergNEF's underlying dataset was not independently reconstructed.</p>
<p><strong>August 3 — electricity delivery and Base Power.</strong> An EIA-sourced Coatue chart shows transmission and distribution taking a growing share of utility infrastructure spending. Coatue links this to its continued backing of Base Power and the Base Core launch. Production still exceeds transmission/distribution in the latest chart bar, so the graphic does not establish that delivery is already the majority. <a href="https://www.coatue.com/c/takes/chart-of-the-day-2026-08-03">Coatue's original post and chart</a>.</p>
<p><strong>My interpretation:</strong> this adds an operator/software/customer-network business model to the battery theme. Base describes coordinating home batteries for grid balancing while retaining household backup, earning revenue from grid services. That is the <a href="https://help.basepowercompany.com/en/articles/10194881">company's April 6 explanation</a>, used as background outside the window, rather than independent proof of profitability. Coatue's posts establish its backing of Base; they do not disclose positions in the listed battery stocks discussed here.</p>

<p style="margin-top:28px;font-size:19px;color:#173e5b"><strong>Do these batteries come from China? Official US import evidence</strong></p>
<p><strong>Broad lithium-ion imports — HTS 850760.</strong> This covers multiple applications, including EVs and electronics, and is not a stationary-storage-only series. Source: <a href="https://dataweb.usitc.gov/trade/search/GenImp/HTS">USITC DataWeb, publishing US Census merchandise trade statistics</a>, retrieved September 23, 2026. The query uses General Imports, General Customs Value, all countries and districts. July was the latest available month at retrieval, according to the <a href="https://www.census.gov/foreign-trade/schedule.html">Census release schedule</a>.</p>
__BROAD_TABLE__
<p>The comparable January–July periods show China's value share falling from <strong>62.0% in 2025 to 39.3% in 2026</strong>. China remains the largest individual origin in this broad category. Full-year rows provide context; partial-year import dollars should not be compared with a full year as a growth rate.</p>
<p><strong>Housed storage systems — new HTS 8507600030.</strong> Effective <strong>February 1, 2026</strong>, this code covers a housed lithium-ion energy-storage device of at least <strong>1kWh</strong>, including modules, battery-management circuitry, and the other components enabling storage and discharge. It is not limited to residential batteries and does not include separately imported cells. The previous non-EV code 8507600020 was split into 0030 and 0090. <a href="https://www.usitc.gov/tariff_affairs/documents/list_of_committee_changes_for_january-1-2026-and-february-1-2026.pdf">USITC's official changes, printed pages 60–62</a>; <a href="https://hts.usitc.gov/?query=8507.60">HTS classification</a>.</p>
<p>Reported imports in this new code totaled <strong>$2.585bn for February–July 2026</strong>. The five largest customs origins were:</p>
__BESS_TABLE__
<p>Source: USITC DataWeb/Census, September 23 extraction. The table covers the five largest origins, not the entire total. China's monthly share in this category rose from <strong>10.4% in May to 19.2% in June and 28.0% in July</strong>. Consequently, the broader decline does not establish a continuously declining share in every storage category. This new code has only a short history.</p>
<p><strong>Interpretation:</strong> these are shares of reported <em>import value</em>. They are not shares of US deployment, consumption, GWh, or underlying Chinese cell content. Customs origin, cell origin, final assembly, and shareholder nationality are different questions. <a href="https://www.census.gov/foreign-trade/reference/definitions/index.html">Customs value</a> excludes import duties and international freight/insurance; General Imports includes arrivals into bonded warehouses and foreign-trade zones. Domestic shipments, exports, inventories, and a comparable valuation bridge would be required to estimate US import penetration. These tables also cannot establish tariff causation or identify company-level suppliers.</p>
<p><strong>Base Power specifically:</strong> its <a href="https://www.basepowercompany.com/core">Base Core page</a>, checked September 23, says the product uses LFP chemistry and is built at its Austin factory. The reviewed page does not identify the cell supplier or cell country of origin. US assembly therefore does not prove US-made cells, and this review cannot classify Base Core as a Chinese finished-system import.</p>

<p style="margin-top:28px;font-size:19px;color:#173e5b"><strong>Where the investment debate is most useful</strong></p>
<p><strong>Korean localization: utilization recovery versus factory economics.</strong> <strong>BofA Ha, September 1</strong>, reports North American ESS shares of <strong>14% for LGES and 6% for Samsung SDI in 1H26</strong>, versus <strong>2% each in 2025</strong>. These broker market-share estimates have a different basis from the customs tables above. Local production and EV-line conversion create opportunity, but conversion can also limit the need for new equipment, an offset behind BofA's Neutral view on PNT. <strong>BofA Sun Jung Lee, September 1</strong>, relays a <strong>9GWh SK On–NeoVolta LFP agreement for 2027–31</strong> involving a Georgia EV plant; an additional agreement remained prospective. The next proof points are qualified throughput and margins, including profitability excluding production credits.</p>
<p><strong>China/CATL: structural strength with a cycle risk.</strong> <strong>Jefferies sales' Cristina Titu, July 10</strong>, relaying Alan Lau, flags a potentially strong 2026–27 Chinese grid-installation cycle followed by slower growth, while remaining positive on CATL structurally. September 16 commentary distinguishes unverified production rumors from management's claim of full utilization. The more recent counterweight is <strong>GS Trina Chen/Joy Zhang's materials monitor, relayed September 17 by Marcio Farid</strong>: softer lithium pricing, arriving Zimbabwe supply, slower domestic storage growth amid declining project returns, and cathode output ahead of implied demand. Structural leadership can coexist with inventory corrections and weak marginal project economics.</p>
<p><strong>Fluence: orders are insufficient.</strong> The broker sequence moves from an August 25 social relay of UBS Jon Windham's Neutral upgrade to <strong>Barclays Christine Cho's September 3 Underweight downgrade</strong> and <strong>Jefferies Julien Dumoulin-Smith's September 18 Hold downgrade recap</strong>. The <a href="https://ir.fluenceenergy.com/news-releases/news-release-details/fluence-energy-announces-revised-guidance-fiscal-year-2026">company's September 16 release</a> cuts FY26 revenue guidance from a prior <strong>$3.0bn midpoint to approximately $2.4bn</strong> and adjusted EBITDA from a <strong>$10m loss midpoint to approximately a $200m loss</strong>, principally due to the Houston manufacturing ramp despite strong demand. Throughput, deliveries, customer retention, working capital, and cash conversion are the relevant tests.</p>
<p><strong>Lithium: storage demand is not a sufficient price forecast.</strong> <strong>GS Hugo Nicolaci and colleagues, August 17</strong> (received August 16), relays Albemarle IR's view that LFP-heavy storage demand was tightening carbonate. <strong>MS Rahul Anand, September 1</strong>, identifies near-term upside from inventories, restarts, and shipment pull-forward but expects a looser longer-term supply balance. GS's September 17 checks then report weaker prices and easing supply. The chronology tempers an unconditional bullish interpretation. Shipment forecasts, installations, GW, and GWh should also be kept on their original bases.</p>
<p><strong>Brazil: capacity payments and final auction economics.</strong> <strong>UBS Luciana Carvalho/Shneur Gershuni and colleagues, September 3</strong>, reports CTG Brasil's assessment that avoided curtailment and arbitrage alone did not justify its studied co-located projects. Their September 10 note warns that registered pipeline includes duplication. <strong>BofA Gustavo Faria/Andre Silveira, August 27</strong>, highlights cost-allocation offsets; its 5GW scenario was illustrative, not a forecast. <a href="https://www.gov.br/aneel/pt-br/assuntos/noticias/2026-defeso-eleitoral/primeiros-leiloes-de-armazenamento-de-energia-do-brasil-entram-em-consulta-publica">ANEEL's July 28 consultation announcement</a> proposed December 2 and 4 auctions and 15-year contracts starting August 2028. Those are proposed terms, not awarded capacity. Qualified bids and contract returns matter more than registered volume.</p>
<p><strong>New chemistry: distinguish agreements from commercial production.</strong> <a href="https://www.catl.com/en/news/6916.html">CATL and Solarpro's July 21 announcement</a> covers a <strong>2GWh sodium-ion cooperation agreement</strong>, not commissioned volume. Sodium-ion can support storage while altering its lithium intensity. In specialty cells, <strong>GS Mark Delaney, July 24</strong>, retained Sell on QuantumScape, while <strong>BofA Ruplu Bhattacharya/Wamsi Mohan, August 17</strong>, retained Neutral on Enovix amid qualification and manufacturing questions. These development-stage cases require different evidence from established storage demand.</p>

<p><strong>Research priorities:</strong> Panasonic versus Samsung SDI on architecture and module margins; LGES/SDI/SK On on profitable conversion throughput; CATL and Sungrow on project returns and order quality; Fluence on delivery and cash conversion; lithium on inventories, restarts, and realized prices; and Brazil on final capacity-contract economics. These are priorities derived from the review, not new ratings or portfolio recommendations.</p>

<p style="margin-top:28px;font-size:19px;color:#173e5b"><strong>Coverage and verification</strong></p>
<p>The review covers <strong>June 25–September 23, 2026</strong>, through retrieval on September 23. It searched <strong>113,728 saved posts</strong> and <strong>22,323 archived broker-email bodies</strong>, supplemented by a live Outlook subject search across received-mail folders and all senders. Initial matches were <strong>309 posts, 1,017 archived emails, and 258 live subject hits</strong>, including duplicates and irrelevant matches. The selected evidence pack contains <strong>29 email copies and 57 posts</strong>, plus the Coatue follow-up. These are search and selection counts, not counts of independent research reports.</p>
<p>The saved feed and broker archive end September 22. Archived bodies may be truncated at 9,000 characters; selected live messages were read in full. This was not an exhaustive live body search of every non-broker email, and linked reports, attachments, and paywalled articles were not all opened. Broker and sales commentary is identified by author and date above; reported publication dates are distinguished from receipt dates where relevant.</p>
<p>Official import dollar values are reported inputs; percentages are derived as country value divided by world value for the same code and period. For the two main China figures: <strong>$3,825,215,075 / $9,721,366,797 × 100 = 39.3485%</strong>; <strong>$401,055,914 / $2,584,726,446 × 100 = 15.5164%</strong>. Country rows reconcile exactly to the captured official totals, and explicit monthly records reconcile to aggregate results. An independent calculation review passed arithmetic and scope checks; it was not a second live extraction. No dollars-to-GWh conversion or forecast was used.</p>
<p style="color:#596775;font-size:13px">Prepared September 23, 2026. The attachment is a portable copy of this consolidated report. Supporting emails, saved posts, official trade tables, and calculation audit are retained in the research workspace.</p>
'''.replace('__BROAD_TABLE__', broad_table).replace('__BESS_TABLE__', bess_table)

document = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Batteries: 90-day review, Coatue and US imports | 23 Sep 2026</title></head>
<body style="margin:0;padding:24px;background:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#253442">
<div style="max-width:820px;margin:0 auto">
<p style="font-size:12px;letter-spacing:1px;color:#5d7386;margin-bottom:6px">CAPSTONE RESEARCH · SEPTEMBER 23, 2026</p>
<h1 style="font-size:28px;line-height:1.2;color:#173e5b;margin:6px 0 12px">Batteries: the infrastructure opportunity</h1>
<p style="font-size:16px;color:#596775;margin-bottom:28px">90-day saved-feed and email review · Coatue / Base Power · Official US import data</p>
''' + body + '</div></body></html>'

class CheckHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.words = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'href' in values:
            self.links.append(values['href'])
        if tag in ('p', 'tr', 'h1'):
            self.words.append('\n\n')
        elif tag in ('td', 'th'):
            self.words.append(' | ')
    def handle_data(self, value):
        self.words.append(value)

check = CheckHTML()
check.feed(document)
assert len(check.links) == 13, len(check.links)
assert all(urlparse(link).scheme == 'https' and urlparse(link).netloc for link in check.links)
assert '__BROAD_TABLE__' not in document and '__BESS_TABLE__' not in document
assert all(value in document for value in ('69.1%', '59.3%', '62.0%', '39.3%', '29.2%', '26.3%', '15.5%'))
assert all(value not in document for value in ('file://', 'E:/', 'E:\\', 'C:\\'))
report = OUT / 'Batteries_90_day_review_Coatue_US_imports_2026-09-23.html'
report.write_text(document, encoding='utf-8')
plain = ''.join(check.words)
report.with_suffix('.txt').write_text(plain, encoding='utf-8')
manifest = {
    'recipient': 'felipe.monteiro@capstone.com.br',
    'subject': 'Batteries: 90-day review, Coatue and US import data | 23 Sep 2026',
    'body_path': str(report),
    'attachment_path': str(report),
    'public_source_links': check.links,
    'word_count': len(plain.split()),
    'checks': {'import_audit_checks_pass': True, 'public_links_only': True, 'no_local_links': True, 'key_import_values_present': True},
}
(OUT / 'email_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps({'report': str(report), 'words': manifest['word_count'], 'links': len(check.links), 'bytes': report.stat().st_size}))
