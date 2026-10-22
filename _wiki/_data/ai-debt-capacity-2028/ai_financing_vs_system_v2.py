"""v2 after the double-check skeptic (2026-10-22). Changes vs v1:
- Hyperscaler cohort = 4 names (MSFT/AMZN/GOOG/META) on LIKE-FOR-LIKE 4-name marks (GS 800 / 35% / 420 are 5-name incl. ORCL).
- 2026 anchor = Barclays 4-name YTD-Aug 197.7 + moderate Q4 (MS 10-01) -> FY26 ~235 on 4-name consensus capex 723 -> 0.325.
- 2027 share 0.33 (GS 35% is 5-name; 4-name run-rate 0.325), 2028 share 0.30 (GS: 2027 peaks).
- 2028 big-4 total capex = consensus 1,119 x JPM/consensus (1,229/1,014) = 1,356 (the stated method, correctly applied).
- Non-hyper residual uses the house PLAYERS-consistent 4-name AI sums (1,192 / 1,550) so the residual is 693 / 1,362, not 760 / 1,488.
- Non-hyper external share = ASSUMPTION 0.75 (range 0.60-0.90), identification shown, not claimed as calibrated.
- Denominators: US Treasury CY26 ~2.1tn (PARTIAL), China net ex-swap 1.66tn, Germany capital-market 349.5, NSR rescale on 16.5tn.
All USD bn, flows per calendar year unless STOCK.
"""
import json

house_total_ai = {2026: 901.6, 2027: 1885.4, 2028: 2913.1}        # HARD (house AI Model, Aug-26 vintage)
house_big4_ai_players = {2026: 681.9, 2027: 1192.2, 2028: 1550.5}  # per-name PLAYERS sums (dashboard); BR.hyper = 1,125/1,425 (model r18, offset sits in 'outros')
big4_total_cons = {2026: 723.0, 2027: 1014.1, 2028: 1118.9}       # HARD BBG BEST_CAPEX live 2026-10-22 (skeptic pull)
big4_total_jpm = {2027: 1229.3}                                   # HARD JPM Anmuth 10-15 per-name sum
big4_total_jpm[2028] = big4_total_cons[2028] * big4_total_jpm[2027] / big4_total_cons[2027]   # 1,356 EST (stated method)
big4_ocf = {2026: 687, 2027: 921, 2028: 1197}                      # PARTIAL (pasted exhibit; 4- or 5-name perimeter unverified)

# hyperscaler share of TOTAL capex
big4_issuance_2026 = 197.7 + 40        # ANCHOR: Barclays 4-name YTD-Aug-20 197.7 (HARD) + Q4 'moderate' ~40 (EST) -> ~238
hyper_share = {2026: big4_issuance_2026 / big4_total_cons[2026], 2027: 0.33, 2028: 0.30}

# non-hyperscaler external share: identification range, central 0.75 (ASSUMPTION)
nonhyper_share = {'lo': 0.60, 'mid': 0.75, 'hi': 0.90}

def leg(y, hyper_total, share_key='mid', total_ai=None, big4_ai=None):
    total_ai = house_total_ai[y] if total_ai is None else total_ai
    big4_ai = house_big4_ai_players[y] if big4_ai is None else big4_ai
    resid = total_ai - big4_ai
    h = hyper_total * hyper_share[y]
    n = resid * nonhyper_share[share_key]
    return dict(hyper=round(h), nonhyper=round(n), total=round(h + n), resid=round(resid), hyper_total=round(hyper_total))

out = {}
for y in (2027, 2028):
    out[f'{y}_central_house_jpm'] = leg(y, big4_total_jpm[y])
    out[f'{y}_house_consensus'] = leg(y, big4_total_cons[y])
    out[f'{y}_lo'] = leg(y, big4_total_cons[y], 'lo')
    out[f'{y}_hi'] = leg(y, big4_total_jpm[y], 'hi')
# alternative total-AI perimeters (same shares): GS semis bottom-up and NSR
out['2027_gs_ai_infra_1300'] = leg(2027, big4_total_jpm[2027], 'mid', total_ai=1300)
out['2028_gs_ai_infra_2000'] = leg(2028, big4_total_jpm[2028], 'mid', total_ai=2000)
out['2027_nsr_2190'] = leg(2027, big4_total_jpm[2027], 'mid', total_ai=2190)
out['2028_nsr_3330'] = leg(2028, big4_total_jpm[2028], 'mid', total_ai=3330)

# like-for-like 4-name hyperscaler 2027/2028 marks (for G2)
marks_4name = {'BofA 09-15': {2027: 215, 2028: 125}, 'JPM 10-15': {2027: 80 + 75 + 75 + 25, 2028: 80 + 125 + 75 + 20},
               'GS scaled 5->4 names (skeptic)': {2027: 384}, 'MS Nowak 09-07 "$290bn debt needed" (cum 27-28?)': {2027: 145, 2028: 145}}

# NSR rescale on the right base (16.5tn cumulative DC capex 2026-30)
nsr = {2026: 1132, 2027: 2190, 2028: 3330, 2029: 3810, 2030: 4150}
nsr_ext = {y: {'nsr_ocf_3.7tn': round(3700 * nsr[y] / 16500), 'consensus_ocf_5.7tn': round(5700 * nsr[y] / 16500)} for y in (2027, 2028)}

# cash-gap reconciliation for the hyperscaler leg
recon = {}
for y in (2027, 2028):
    gap = house_big4_ai_players[y] - big4_ocf[y]
    nonai = big4_total_jpm[y] - house_big4_ai_players[y]
    recon[y] = dict(ai_capex_minus_ocf=round(gap), non_ai_capex=round(nonai), returns_est=100, sum=round(gap + nonai + 100),
                    modelled_debt=out[f'{y}_central_house_jpm']['hyper'])

# system denominators (USD bn)
fx = dict(eur=1.17, gbp=1.33, jpy=150.0, cny=7.1)
sysd = {
    'OECD sovereign+corporate borrowing 2026 (as reported, gross)': 29000,
    'OECD sovereign gross 2026': 18000,
    'OECD corporate bonds 2025': 6800,
    'OECD corp bonds + syndicated loans 2025': 13800,
    'US LT fixed-income issuance 2025 (SIFMA)': 11500,
    'USD IG gross 2027 (GS)': 2400,
    'US Treasury net marketable borrowing CY2026 (~Q2 190 + Q3 739 + Q4 628 + Q1 EST ~550)': 2100,
    'US Treasury net >=10y supply after Fed holdings (Exante via Nascimento 09-11)': 400,
    'Europe sovereign+EU gross 2026 (FR 310 + DE cap-mkt 349.5 + IT ~330 + ES MLT 176.9 + EU 180) EUR + UK 246.2 GBP': (310 + 349.5 + 330 + 176.9 + 180) * fx['eur'] + 246.2 * fx['gbp'],
    'China govt net 2026 ex hidden-debt swap (5.89 + 1.3 + 4.6 CNY tn)': (5.89 + 1.3 + 4.6) * 1000 / fx['cny'],
    'Japan JGB gross FY26': 180.7 * 1000 / fx['jpy'],
    'Japan JGB new money FY26': 28.6 * 1000 / fx['jpy'],
    'Private credit AUM (STOCK)': 1850,
    'Private credit dry powder (STOCK)': 500,
    'Private capital dry powder all strategies (STOCK, GS)': 4500,
    'IEA energy investment 2026 (spend, compare with AI CAPEX not financing)': 3400,
    'World gross saving (~27% x 118tn GDP)': 0.27 * 118000,
    'World GDP 2026': 118000,
    'US GDP 2026': 31800,
}
def ratios(x):
    return {k: round(100 * x / v, 1) for k, v in sysd.items()}

res = dict(hyper_share=hyper_share, big4_total_jpm=big4_total_jpm, legs=out, marks_4name=marks_4name, nsr_rescaled=nsr_ext,
           reconciliation=recon, system_usd_bn={k: round(v) for k, v in sysd.items()},
           ratios_2027_central=ratios(out['2027_central_house_jpm']['total']),
           ratios_2028_central=ratios(out['2028_central_house_jpm']['total']),
           exante_duration_crowding={'hyper >10y issuance 2026': 200, 'hyper >10y issuance 2027': 300, 'UST net >=10y after Fed': 400, 'share_2026': 0.5, 'share_2027': 0.75})
print(json.dumps(res, indent=1))
