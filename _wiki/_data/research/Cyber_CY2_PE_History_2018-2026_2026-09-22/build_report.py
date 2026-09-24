"""Map sourced Bloomberg historical multiples into the requested table."""
import collections
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
history = json.loads((HERE / 'history.json').read_text())
endpoints = json.loads((HERE / 'all_endpoint_checks.json').read_text())
identities = {}
for r in json.loads((HERE / 'identities.json').read_text()):
    identities.setdefault(r['ticker'], {})[r['field']] = r['value']
years = list(range(2018, 2027))
rows, checks, us_dates, jp_dates = [], [], {}, {}
for ticker, name in history['companies']:
    cells = []
    for year in years:
        y = str(year)
        sec = '2542797D US Equity' if ticker == 'SAIL' and year <= 2021 else ticker + ' Equity' if ticker == '4704 JP' else ticker + ' US Equity'
        raw = [r for r in endpoints[y] if r['ticker'] == sec]
        vals = {r['field']: r['value'] for r in raw}
        date = raw[0]['date'] if raw else None
        ipo = identities[sec]['EQY_INIT_PO_DT']
        cell = {'snapshot_year': year, 'eps_calendar_year': year + 2, 'security': sec, 'observation_date': date, 'price': vals.get('PX_LAST'), 'eps': vals.get('BEST_EPS'), 'pe': vals.get('BEST_PE_RATIO'), 'source': 'Bloomberg historical BEST_PE_RATIO; BEST_FPERIOD_OVERRIDE=' + str(year+2) + 'BC; retrieved 2026-09-22'}
        if ticker == 'SAIL' and 2022 <= year <= 2024:
            cell['status'] = 'Private'
        elif history['history'][y]['cutoff'] < ipo:
            cell['status'] = 'Pre-IPO'
        elif cell['pe'] is not None:
            cell['status'] = 'Available'
            original = [r for r in history['history'][y]['records'] if r['ticker'] == sec and r['date'] == date and r['field'] == 'BEST_PE_RATIO']
            checks.append({'check': f'{ticker} {year} historical endpoint matches first pull', 'pass': len(original) == 1 and abs(original[0]['value'] - cell['pe']) < 1e-9})
            # Returned EPS has three decimals. Check source consistency using rounding intervals.
            if cell['eps'] is not None:
                implied = cell['price'] / cell['pe']
                tolerance = 0.00051 + 0.00051 / cell['pe'] + cell['price'] * 0.00051 / cell['pe'] ** 2
                checks.append({'check': f'{ticker} {year} P/E vs rounded historical price/EPS', 'pass': abs(implied - cell['eps']) <= tolerance, 'implied_eps': implied, 'source_eps': cell['eps'], 'tolerance': tolerance})
        elif cell['eps'] is not None and cell['eps'] <= 0:
            cell['status'] = 'N/M'
        else:
            cell['status'] = 'N/A'
        if date:
            dates = jp_dates if ticker == '4704 JP' else us_dates
            if y in dates:
                assert dates[y] == date
            dates[y] = date
        cells.append(cell)
    rows.append({'ticker': ticker, 'name': name, 'cells': cells})

out = {'title': 'Cybersecurity historical CY+2 P/E', 'retrieved_at': history['retrieved_at'], 'years': years, 'rows': rows, 'us_dates': us_dates, 'jp_dates': jp_dates, 'checks': checks}
(HERE / 'report.json').write_text(json.dumps(out, indent=2), encoding='utf-8')

style = 'padding:7px 9px;border-bottom:1px solid #dfe4ea;white-space:nowrap;'
header = '<tr style="background:#173b59;color:white"><th style="'+style+'text-align:left">Company</th>' + ''.join('<th style="'+style+'text-align:right">'+str(y)+('*' if y==2026 else '')+'</th>' for y in years) + '</tr>'
header += '<tr style="background:#edf2f7"><td style="'+style+'">EPS calendar year</td>' + ''.join('<td style="'+style+'text-align:right">'+str(y+2)+'</td>' for y in years) + '</tr>'
table = '<table style="border-collapse:collapse;font-size:10pt">' + header
for i, row in enumerate(rows):
    table += '<tr style="background:'+('#f5f7fa' if i % 2 else '#ffffff')+'"><td style="'+style+'">'+html.escape(row['name']+' ('+row['ticker']+')')+'</td>'
    for cell in row['cells']:
        display = f'{cell["pe"]:,.1f}x' if cell['status'] == 'Available' else cell['status']
        table += '<td style="'+style+'text-align:right">'+display+'</td>'
    table += '</tr>'
table += '</table>'
body = '''<!doctype html><html><head><meta charset="utf-8"></head><body style="font-family:Arial,sans-serif;font-size:11pt;color:#202733;line-height:1.4">
<p>Hi Fernanda,</p>
<p>As requested by Felipe, below is the historical <b>calendar-year +2 forward P/E</b> table for the 15 cybersecurity companies.</p>
<p>Each column uses the <b>last local-market close of that year and the historical adjusted EPS consensus for calendar year Y+2 available at that observation date</b>. For example, 2018 uses CY2020 EPS; 2026 uses CY2028 EPS.</p>'''+table+'''
<p><b>*2026 is the latest completed close:</b> September 21, 2026 for U.S. listings and September 18, 2026 for Trend Micro in Japan. Earlier columns are year-end snapshots, not annual averages.</p>
<p><b>Source:</b> Bloomberg Desktop API, retrieved September 22, 2026. Historical <code>BEST_PE_RATIO</code> with fixed <code>BEST_FPERIOD_OVERRIDE=2020BC</code> through <code>2028BC</code>. These are Bloomberg's calendarized adjusted-consensus P/Es; fiscal-year and rolling-24-month multiples are different measures. Historical source values are retained without substituting today's consensus or subsequently reported EPS. P/Es are quoted directly from Bloomberg, rounded to one decimal.</p>
<p><b>Legend:</b> <b>N/M</b> = not meaningful because the relevant historical consensus EPS was zero or negative. <b>Pre-IPO</b> = shares had not yet listed at the observation date. <b>Private</b> = SailPoint was privately owned at year-end. Very high positive multiples are retained: small positive EPS can produce P/Es above 1,000x.</p>
<p><b>SailPoint:</b> 2018-2021 uses its original listing (Bloomberg <code>2542797D US Equity</code>). It was <a href="https://www.thomabravo.com/press-releases/thoma-bravo-completes-acquisition-of-sailpoint">taken private on August 16, 2022</a> and <a href="https://investor.sailpoint.com/shareholder-services/investor-faqs">returned to public trading on February 13, 2025</a>. The table preserves the 2022-2024 gap; the two listings have different capital structures.</p>
<p>The attached Excel and CSV files contain the complete table. The Excel file also includes the exact observation dates and method notes.</p>
<p>Prepared for Felipe Monteiro.</p></body></html>'''
(HERE / 'email.html').write_text(body, encoding='utf-8')
(HERE / 'email_subject.txt').write_text('Cybersecurity | Historical CY+2 forward P/E | 2018-2026', encoding='utf-8')
print('Status counts', collections.Counter(c['status'] for r in rows for c in r['cells']))
print('Checks',len(checks),'failures',json.dumps([c for c in checks if not c['pass']],indent=2))
for row in rows:
    print(row['ticker'], [round(c['pe'],1) if c['status']=='Available' else c['status'] for c in row['cells']])
