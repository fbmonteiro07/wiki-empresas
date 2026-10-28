"""Build the audited quarterly headcount figure with stdlib only; never fill gaps."""
import datetime as dt
from html import escape
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / 'bloomberg_quarterly_raw.json').read_text(encoding='utf-8'))
rows = []
for period, item in raw['quarterly'].items():
    year, quarter = map(int, period.split('Q'))
    month = {1: 9, 2: 12, 3: 3, 4: 6}[quarter]
    calendar_year = year - 1 if quarter <= 2 else year
    day = 31 if month in (3, 12) else 30
    end = dt.date(calendar_year, month, day)
    securities = [sec for msg in item['response'] for sec in msg.get('securityData', [])]
    assert len(securities) == 1 and securities[0]['security'] == 'MSFT US Equity'
    security = securities[0]
    assert not security.get('securityError') and not security.get('fieldExceptions')
    fields = security['fieldData']
    number = fields.get('NUM_OF_EMPLOYEES')
    assert number == fields.get('BS_NUMBER_EMPLOYEES')
    rows.append({'fiscal_period': period, 'label': f'F{quarter}Q{str(year)[2:]}',
                 'period_end': end.isoformat(), 'date_label': end.strftime('%b %Y'),
                 'bloomberg_headcount': number, 'chart_headcount': number,
                 'source': 'Bloomberg / Microsoft annual report' if number else 'Unavailable',
                 'retrieved_on': '2026-10-27', 'overrides': item['overrides']})

# Independently dated company observation, not an invented Bloomberg quarterly value.
assert rows[-1]['period_end'] == '2026-09-30' and rows[-1]['bloomberg_headcount'] is None
rows[-1].update(chart_headcount=223000, source='Microsoft Facts About Microsoft',
                source_url='https://news.microsoft.com/facts-about-microsoft/',
                source_as_of='2026-09-30',
                basis='Worldwide employees; full-time definition not explicitly restated')
assert [r['chart_headcount'] for r in rows] == [228000, None, None, None, 228000, None, None, None, 223000, 223000]

data = {'security': 'MSFT US Equity', 'retrieved_on': '2026-10-27',
        'bloomberg_fields': ['NUM_OF_EMPLOYEES', 'BS_NUMBER_EMPLOYEES'],
        'method': 'Fiscal-quarter overrides; missing values stay null; no interpolation or carry-forward.',
        'bloomberg_current_headcount_as_of': '2026-06-30', 'rows': rows}
(HERE / 'headcount_series.json').write_text(json.dumps(data, indent=2), encoding='utf-8')

W, H = 1600, 940
LEFT, RIGHT, TOP, BOTTOM = 125, 1510, 245, 695
blue, teal, ink, muted = '#2455A6', '#008273', '#172B43', '#5F6F82'
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<rect width="1600" height="940" fill="#FFFFFF"/>',
         '<style>text{font-family:Arial,sans-serif;font-variant-numeric:tabular-nums}</style>']

def text(x, y, value, size=22, fill=ink, weight=400, anchor='start'):
    parts.append(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')

def line(x1, y1, x2, y2, color='#DFE5EC', width=1):
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')

def xpos(i): return LEFT + 55 + i * (RIGHT - LEFT - 110) / 9
def ypos(value): return BOTTOM - (value - 200000) / 40000 * (BOTTOM - TOP)

text(75, 65, 'MICROSOFT  /  MSFT', 19, blue, 700)
text(75, 116, 'Headcount by quarter', 43, ink, 700)
text(75, 157, 'Bloomberg confirms annual totals but leaves the six missing quarters unavailable.', 24, muted)

parts.append(f'<circle cx="85" cy="202" r="8" fill="{blue}"/>')
text(105, 209, 'Bloomberg + annual report', 20, muted)
parts.append(f'<rect x="436" y="194" width="16" height="16" rx="2" fill="{teal}"/>')
text(465, 209, 'Microsoft fact sheet', 20, muted)
parts.append('<rect x="728" y="193" width="22" height="19" fill="#F0F3F6"/>')
text(762, 209, 'ND: no quarterly count available', 20, muted)

for i, row in enumerate(rows):
    if row['chart_headcount'] is None:
        parts.append(f'<rect x="{xpos(i)-44}" y="{TOP}" width="88" height="{BOTTOM-TOP}" fill="#F4F6F8"/>')
        text(xpos(i), TOP + 35, 'ND', 20, '#8A96A5', 600, 'middle')

for value in range(200000, 240001, 10000):
    y = ypos(value)
    line(LEFT, y, RIGHT, y)
    text(LEFT - 16, y + 7, f'{value:,}', 19, muted, anchor='end')

for i, row in enumerate(rows):
    x = xpos(i)
    line(x, BOTTOM, x, BOTTOM + 7, '#A6B2C0')
    text(x, BOTTOM + 38, row['label'], 20, ink, 700, 'middle')
    text(x, BOTTOM + 67, row['date_label'], 17, muted, anchor='middle')
    count = row['chart_headcount']
    if count is None:
        continue
    y = ypos(count)
    color = teal if i == len(rows) - 1 else blue
    if i == len(rows) - 1:
        parts.append(f'<rect x="{x-9}" y="{y-9}" width="18" height="18" rx="2" fill="{color}"/>')
    else:
        parts.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{color}"/>')
    text(x, y - 24, f'{count:,}', 25, color, 700, 'middle')

text(75, 815, 'People at period end. Fiscal year ends in June. Axis starts at 200,000. Missing quarters are not connected or filled.', 20, muted)
text(75, 857, 'Source: Bloomberg Desktop API, NUM_OF_EMPLOYEES / BS_NUMBER_EMPLOYEES, retrieved 27 Oct 2026.', 18, muted)
text(75, 886, 'Sep 2026: Microsoft fact sheet, as of 30 Sep 2026; retrieved 27 Oct 2026. Worldwide employees; full-time basis not restated.', 18, muted)
text(75, 918, 'Annual-report counts are approximate full-time employees. Bloomberg current-headcount date remains 30 Jun 2026.', 18, muted)
parts.append('</svg>')
(HERE / 'MSFT_headcount_quarterly.svg').write_text('\n'.join(parts), encoding='utf-8')
print('Validated 10 quarters: three Bloomberg totals, one separate company fact-sheet observation, six missing totals.')
print(HERE / 'MSFT_headcount_quarterly.svg')
