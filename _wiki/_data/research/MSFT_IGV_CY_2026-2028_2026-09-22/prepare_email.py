import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'valuation.json').read_text(encoding='utf-8'))
years = ['2026', '2027', '2028']
table = data['table']
rows = ''
for ticker, name in [('MSFT', 'Microsoft (MSFT)'), ('IGV', 'IGV - portfolio estimate')]:
    for metric, label in [('pe', 'P/E'), ('pfcf', 'P/FCF')]:
        rows += '<tr><td style="padding:9px;border:1px solid #d5dce5">' + name + '</td><td style="padding:9px;border:1px solid #d5dce5">' + label + '</td>'
        rows += ''.join(f'<td style="padding:9px;border:1px solid #d5dce5;text-align:right">{table[ticker][y][metric]:.1f}x</td>' for y in years)
        rows += '</tr>'
coverage_pe = ' / '.join(f'{table["IGV"][y]["pe_coverage"]:.2%}' for y in years)
coverage_fcf = ' / '.join(f'{table["IGV"][y]["pfcf_coverage"]:.2%}' for y in years)
body = f'''<!doctype html><html><head><meta charset="utf-8"></head><body style="font-family:Arial,sans-serif;font-size:11pt;color:#202733;line-height:1.45">
<p>Hi Fernanda,</p>
<p>As requested by Felipe, below are Microsoft and IGV's valuation multiples for <b>calendar years 2026-2028</b>.</p>
<p><b>Prices:</b> September 21, 2026 close. <b>Consensus and share counts:</b> Bloomberg, retrieved September 22, 2026. Figures are multiples of calendar-year estimates, not future share-price forecasts.</p>
<table style="border-collapse:collapse;min-width:590px"><tr style="background:#173b59;color:white"><th style="padding:9px;text-align:left">Security</th><th style="padding:9px;text-align:left">Metric</th><th style="padding:9px">CY2026E</th><th style="padding:9px">CY2027E</th><th style="padding:9px">CY2028E</th></tr>{rows}</table>
<p><b>Basis and sources</b></p>
<ul>
<li><b>P/E:</b> Bloomberg adjusted EPS consensus. <b>P/FCF:</b> equity market capitalization divided by Bloomberg FCF consensus (cash from operations less capital expenditure); no additional deduction for stock-based compensation or adjustment for lease financing.</li>
<li><b>Calendarization:</b> Bloomberg <code>BEST_FPERIOD_OVERRIDE=2026BC/2027BC/2028BC</code>, with <code>BEST_EPS</code> and <code>BEST_ESTIMATE_FCF</code>. Microsoft CY2026 includes reported first-half actuals and second-half estimates. Microsoft's June fiscal year-end is calendarized.</li>
<li><b>IGV is a calculated portfolio estimate:</b> September 21 <a href="https://www.ishares.com/us/products/239771/ishares-expanded-tech-software-sector-etf/latest-holdings.csv">iShares holdings</a>, using constituent Bloomberg calendar-year estimates. Aggregate the weighted earnings/FCF yields, then invert; negative earnings and negative FCF are retained. Holdings with no estimate are excluded and covered equity weights are renormalized. Cash and the small futures overlay are excluded. This is a static-holdings calculation.</li>
<li><b>IGV equity-weight coverage (2026 / 2027 / 2028):</b> P/E {coverage_pe}; P/FCF {coverage_fcf}. The IGV figures therefore describe the covered equity basket. They can differ from published ETF valuation statistics because of period and loss-treatment conventions.</li>
</ul>
<p><b>Microsoft calculation:</b> HARD sourced inputs are observed closing price <b>$501.61</b>, consensus CY EPS <b>$18.584 / $21.290 / $25.674</b>, and consensus CY FCF <b>$44.60bn / $33.40bn / $62.94bn</b>. The forecasts are sourced estimates, not realized outcomes. Close-equivalent equity market cap of <b>$3,724.73bn</b> is DERIVED by rebasing Bloomberg's live market cap to the closing price. For example, CY2027 P/E = $501.61 / $21.290 = <b>23.6x</b>; P/FCF = $3,724.73bn / $33.40bn = <b>111.5x</b>. Source: Bloomberg, September 22, 2026.</p>
<p><b>Coverage sensitivity:</b> IGV is PARTIAL for the whole fund where estimates are missing. Assigning zero FCF yield to the uncovered CY2028 equity weight would give <b>28.5x</b> instead of <b>28.0x</b>; this is a scenario, not an imputed forecast. No proprietary forecast inputs were added.</p>
<p><b>Validation:</b> Microsoft calendar-year EPS and FCF reconcile to the four relevant quarters; all 106 equity holding prices reconcile to Bloomberg's previous close. Independent calculation review passed. These checks validate the calculation, not the forecast outcomes.</p>
<p>Prepared for Felipe Monteiro.</p>
</body></html>'''
(HERE / 'email.html').write_text(body, encoding='utf-8')
(HERE / 'email_subject.txt').write_text('Microsoft and IGV | CY2026-2028 P/E and P/FCF | 21 Sep 2026 close', encoding='utf-8')
print(HERE / 'email.html')
