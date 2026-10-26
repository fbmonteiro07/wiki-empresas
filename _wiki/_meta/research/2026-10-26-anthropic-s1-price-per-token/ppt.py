import json
# ---- HARD: Anthropic S-1 (2026-10-26), $M
rev={'1Q25':376,'2Q25':787,'3Q25':1382,'4Q25':2040,'1Q26':4731,'2Q26':11555}
comp={'1Q25':944,'2Q25':1390,'3Q25':2047,'4Q25':2945,'1Q26':3387,'2Q26':5558}
rev_1H25,rev_1H26=1163,16286; cogs_1H25,cogs_1H26=1019,2380; rev_FY25,cogs_FY25=4585,2773
cons_1H26=13100; csp_share_1H26=0.48; chan_fee_incr=2700; sm_1H26=3168; sm_1H25=120; mkt_incr=273
# ---- HARD within sample: Ramp TSM panel (pulled 2026-10-14), Anthropic monthly volume (tok) / spend ($)
d=json.load(open(r'E:/Wiki Felipe empresas/_wiki/_data/ramp-ai-index/panel.json',encoding='utf-8'))['tokens']
m=d['months_complete']; V=d['monthly_volume_by_maker']['anthropic']; S=d['monthly_spend_by_maker']['anthropic']
def px(months): 
    i=[m.index(x) for x in months]; return sum(S[j] for j in i)/sum(V[j] for j in i)*1e6
P={'1H25':px(['2025-0%d'%k for k in range(1,7)]),'2Q25':px(['2025-04','2025-05','2025-06']),
   '1Q26':px(['2026-01','2026-02','2026-03']),'2Q26':px(['2026-04','2026-05','2026-06']),
   '1H26':px(['2026-0%d'%k for k in range(1,7)]),'Jun26':px(['2026-06']),'3Q26':px(['2026-07','2026-08','2026-09'])}
print('Ramp realized $/Mtok (all tokens incl cache):',{k:round(v,3) for k,v in P.items()})
# ---- 1) price/cost ratio (tokens cancel): HARD only
for lab,r,c in [('FY24',386,752),('1H25',rev_1H25,cogs_1H25),('FY25',rev_FY25,cogs_FY25),('1H26',rev_1H26,cogs_1H26)]:
    print(f'{lab}: rev/COGS {r/c:.2f}x  GM {1-c/r:.1%}  COGS per $1 rev {c/r:.3f}')
# channel fees (derived residual): 1H26 S&M nature less marketing
mkt_1H26_lo=mkt_incr; mkt_1H26_hi=mkt_incr+sm_1H25          # 1H25 marketing between 0 and all of 1H25 S&M
chan_hi=sm_1H26-mkt_1H26_lo; chan_lo=sm_1H26-mkt_1H26_hi
print(f'channel fees 1H26 ~{chan_lo:.0f}-{chan_hi:.0f} = {chan_lo/rev_1H26:.1%}-{chan_hi/rev_1H26:.1%} of revenue, {chan_lo/(csp_share_1H26*rev_1H26):.0%}-{chan_hi/(csp_share_1H26*rev_1H26):.0%} of CSP-marketplace revenue')
ch=(chan_lo+chan_hi)/2
print(f'GM after channel fees 1H26: {1-(cogs_1H26+ch)/rev_1H26:.1%}')
# ---- 2) cost per token = realized price x COGS/rev
cpt_1H25=P['1H25']*cogs_1H25/rev_1H25; cpt_1H26=P['1H26']*cogs_1H26/rev_1H26
print(f'cost/Mtok 1H25 ${cpt_1H25:.3f} -> 1H26 ${cpt_1H26:.3f} ({cpt_1H26/cpt_1H25-1:+.0%});  price {P["1H25"]:.2f}->{P["1H26"]:.2f} ({P["1H26"]/P["1H25"]-1:+.0%})')
print(f'GP/Mtok 1H26 serving-basis ${P["1H26"]-cpt_1H26:.3f}; after channel ${P["1H26"]*(1-(cogs_1H26+ch)/rev_1H26):.3f}')
# ---- 3) implied tokens = revenue / realized price  ($M / ($/Mtok) = 1e12 tok) -> quadrillion = /1e3
cons_share=cons_1H26/rev_1H26
for q in ['1Q26','2Q26']:
    allin=rev[q]/P[q]/1e3; cons=rev[q]*cons_share/P[q]/1e3
    print(f'{q}: tokens all-in {allin:.1f}Q/qtr = {allin/3:.2f}Q/mo ; consumption-only {cons:.1f}Q = {cons/3:.2f}Q/mo')
# June month: geometric path inside 2Q26 constrained to sum = 11,555; end-Mar ARR $30bn (SemiAnalysis) -> Mar month ~2.5bn
for g in [1.20,1.25,1.30]:
    a=rev['2Q26']/(g+g**2+g**3); jun=a*g**3
    print(f' g={g}: Jun rev ${jun:,.0f}M -> all-in {jun/P["Jun26"]/1e3:.1f}Q/mo, cons-only {jun*cons_share/P["Jun26"]/1e3:.1f}Q/mo (SemiAnalysis ~5Q Jun)')
# y/y decomposition 2Q: revenue = price x volume
print(f'2Q y/y: revenue {rev["2Q26"]/rev["2Q25"]:.1f}x = price {P["2Q26"]/P["2Q25"]:.2f}x * volume {rev["2Q26"]/rev["2Q25"]/(P["2Q26"]/P["2Q25"]):.0f}x')
print(f'revenue per $ compute: 2Q25 {rev["2Q25"]/comp["2Q25"]:.2f}x  2Q26 {rev["2Q26"]/comp["2Q26"]:.2f}x ; serving share of compute 1H26 <= {cogs_1H26/8945:.0%}')
# list-price plausibility (ESTIMATE mix): 65:1 in:out, 90% cache-read @10% of input
for name,i,o in [('Sonnet $3/$15',3,15),('Sonnet5 $2/$10',2,10),('Opus $5/$25',5,25)]:
    for cache in (0.8,0.9):
        inp=65/66; b=inp*(cache*0.1*i+(1-cache)*i)+(1-inp)*o
        print(f'  list blend {name} cache {cache:.0%}: ${b:.2f}/Mtok')

# ---- SKEPTIC FIX (double-check 2026-10-26, verdict PARTIAL): Ramp publishes a second price series
# (price_usd_per_m['anthropic|all_tokens'] = 7-day token cost / 7-day token count, sampled on week-end dates).
# It agrees with spend/volume within ~5% in 2025 but runs ~1.5x higher in 2026. Carry BOTH as a range.
W=d['weeks']; vw=d['volume_by_maker']['anthropic']; pdts=d['price_dates']; PS=d['price_usd_per_m']['anthropic|all_tokens']
def ps(a,b):
    i=[k for k,w in enumerate(pdts) if a<=w<=b and PS[k]]; vv=[vw[W.index(pdts[k])] for k in i]
    return sum(PS[k]*x for k,x in zip(i,vv))/sum(vv)
Q={'1H25':ps('2025-01-12','2025-06-29'),'2Q25':ps('2025-04-06','2025-06-29'),'1H26':ps('2026-01-04','2026-06-28'),
   '2Q26':ps('2026-04-05','2026-06-28'),'Jun26':ps('2026-06-07','2026-06-28')}
print('\nRamp published 7-day price series, volume-weighted $/Mtok:',{k:round(v,3) for k,v in Q.items()})
print('RANGE (spend/volume .. published series):')
lo_hi=lambda k:(P[k],Q[k])
for k in ['2Q25','2Q26','Jun26']: print(f'  price {k}: ${lo_hi(k)[0]:.2f}-{lo_hi(k)[1]:.2f}/Mtok')
t=[rev['2Q26']/p/1e3/3 for p in lo_hi('2Q26')]; print(f'  2Q26 tokens all-in {min(t):.2f}-{max(t):.2f}Q/mo')
for g in (1.20,1.30):
    a=rev['2Q26']/(g+g**2+g**3); jun=a*g**3
    print(f'  g={g}: June all-in {jun/Q["Jun26"]/1e3:.1f}-{jun/P["Jun26"]/1e3:.1f}Q/mo, cons-only {jun*cons_share/Q["Jun26"]/1e3:.1f}-{jun*cons_share/P["Jun26"]/1e3:.1f}Q/mo')
c26=[x*cogs_1H26/rev_1H26 for x in lo_hi('1H26')]; c25=[x*cogs_1H25/rev_1H25 for x in lo_hi('1H25')]
print(f'  allocated serving cost/Mtok 1H25 ${c25[0]:.2f}-{c25[1]:.2f} -> 1H26 ${c26[0]:.3f}-{c26[1]:.3f}')
tc25=(comp['1Q25']+comp['2Q25'])/(rev_1H25/P['1H25']); tc26=[8945/(rev_1H26/x) for x in lo_hi('1H26')]
print(f'  total compute/Mtok 1H25 ${tc25:.2f} -> 1H26 ${tc26[0]:.2f}-{tc26[1]:.2f}')
pr=[lo_hi('2Q26')[i]/lo_hi('2Q25')[i] for i in (0,1)]; print(f'  2Q y/y price {pr[0]:.2f}-{pr[1]:.2f}x -> volume {rev["2Q26"]/rev["2Q25"]/pr[1]:.0f}-{rev["2Q26"]/rev["2Q25"]/pr[0]:.0f}x')
