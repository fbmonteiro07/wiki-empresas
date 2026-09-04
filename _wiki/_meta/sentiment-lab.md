# Sentiment lab — can anything in the sentiment data set be made leading?

_Generated 2026-09-03 by `_wiki/_tools/sentiment_lab.py` (raw tables in `_data/sentiment/lab.json`). Bloomberg weekly panel, 99 names, 139 weeks Jan-2024 → Aug-2026. Returns are universe-relative = minus the same week's cross-sectional mean of the same-horizon buy-and-hold return (a daily-rebalanced EW index is the wrong benchmark: its rebalancing premium biases 8–12 week windows). Means are shown with medians because buy-and-hold returns are right-skewed. **12-week windows overlap heavily — divide printed t-stats by ~3 for 12w, ~2 for 4w; the by-year sign consistency is the better evidence.**_

## Verdict (2026-09-03)

1. **Pure sentiment has no hidden leading component.** Tone residual after the same-week return, tone-vs-price divergence, attention acceleration, Twitter-vs-news disagreement, attention streaks: all ≈ 0 IC at every horizon, in-sample and 2026. Whatever tone and attention know, price already shows.
2. **"Very hot → falls" is false unconditionally** (attention z ≥ 2.5: 4w −0.8%, t −0.8; attention deciles flat). It is **true conditionally**: hot & low short interest (crowded long) −3.0%/−8.6% (4w/12w) in 2025 and −3.1%/−9.6% in 2026, nil in 2024. Hot & high short interest does the opposite (+6%/+9%/+13% at 12w, three years). Hot after a ≥3% up-week continued in 2026 (+12% 12w) — a momentum year, not a fade.
3. **The one sentiment-specific cell that is consistent three years running: panic** (attention z ≥ 1.5 and tone z ≤ −1) → 12w −4.4% / −8.6% / −6.2% (2024/25/26), 4w negative every year. Bad-news attention persists; it is continuation, not reversal. n ≈ 100 episodes.
4. **What forecasts 8–12 week relative returns here is positioning and revisions, not the crowd:** short-interest level D10−D1 at 12w +8% / +25% / +30% (2024/25/26) — but its ex-momentum IC was **negative in 2024** (−0.053) and hugely positive after: a regime bet, not a stable signal. BULL composite (tone + tone change + news tone + EPS revision + rating drift) D10−D1 at 12w +9.9% / +11.2% / +7.3% — the most stable multi-week spread in the set, positive every year.
5. **Aggregate timing:** loudest-quartile weeks for the whole universe → 12w +15% vs +24% for the quietest; Spearman −0.14, n=125 overlapping. Weakly contrarian, anecdotal.

Proposed "leading" construction (to paper-trade, not to claim): a **slow ranking at 8–12 weeks** = BULL composite as the core, a **panic flag** as a short-side overlay, and short interest as a **regime-aware tilt** (only when the squeeze regime is on), plus the pre-print positioning read from the event study. Weekly sentiment stays a coincident crowding gauge.

## Battery output

```
lab: 139 weeks × 99 names, 2024-01-05 → 2026-08-28. All returns universe-relative.

H1 — decile of the signal (10 = hottest / most bullish) → mean forward relative return
  z_att                     1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1192)
    D1          -0.07%|-0.42%  +0.05%|-0.69%  +0.14%|-1.48%  +1.40%|-2.56%  +2.07%|-3.66%
    D2          -0.18%|-0.60%  -0.14%|-1.12%  -0.12%|-2.17%  +0.19%|-3.50%  +1.03%|-5.14%
    D5          -0.29%|-0.67%  -0.62%|-1.30%  -0.89%|-2.58%  -1.85%|-5.05%  -3.43%|-6.47%
    D9          +0.08%|-0.66%  +0.04%|-1.11%  +0.07%|-2.09%  +0.23%|-3.82%  +0.27%|-5.58%
    D10         -0.01%|-0.62%  -0.02%|-0.94%  +0.28%|-2.13%  +1.05%|-2.55%  +1.94%|-4.07%
    D10−D1               +0.06%           -0.07%           +0.15%           -0.35%           -0.13%
  z_tone                    1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1231)
    D1          -0.18%|-0.58%  -0.29%|-1.09%  -1.05%|-2.57%  -2.12%|-3.84%  -2.26%|-5.88%
    D2          -0.23%|-0.58%  -0.37%|-1.20%  -0.70%|-1.94%  -0.33%|-3.31%  -0.41%|-4.82%
    D5          -0.12%|-0.57%  -0.32%|-1.18%  -0.47%|-2.46%  -0.76%|-3.75%  -2.98%|-6.47%
    D9          +0.27%|-0.41%  +0.35%|-1.03%  +0.50%|-1.61%  +1.60%|-2.46%  +3.34%|-3.61%
    D10         -0.04%|-0.32%  +0.27%|-0.63%  +0.72%|-1.45%  +0.98%|-2.07%  +0.98%|-4.20%
    D10−D1               +0.14%           +0.57%           +1.76%           +3.10%           +3.24%
  BULL                      1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1230)
    D1          +0.18%|-0.54%  +0.12%|-1.01%  -0.17%|-2.39%  -1.12%|-3.54%  -3.59%|-7.35%
    D2          -0.30%|-0.65%  -0.47%|-1.23%  -1.10%|-2.57%  -2.49%|-4.14%  -4.14%|-6.23%
    D5          -0.45%|-0.54%  -0.92%|-1.50%  -1.29%|-3.00%  -2.01%|-4.72%  -2.28%|-6.95%
    D9          +0.04%|-0.43%  +0.17%|-0.96%  +0.88%|-1.06%  +2.17%|-2.76%  +3.70%|-3.98%
    D10         +0.41%|-0.36%  +1.10%|-0.50%  +2.30%|-0.87%  +4.38%|-0.86%  +6.34%|-2.24%
    D10−D1               +0.23%           +0.98%           +2.47%           +5.50%           +9.93%
  z_news                    1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1182)
    D1          +0.04%|-0.45%  +0.23%|-0.73%  -0.02%|-2.39%  +0.55%|-3.46%  +0.83%|-4.66%
    D2          -0.38%|-0.60%  -0.46%|-1.45%  -0.38%|-2.62%  -0.10%|-3.62%  +0.16%|-5.08%
    D5          +0.38%|-0.29%  +0.64%|-0.45%  +1.04%|-1.10%  +1.46%|-2.45%  +2.29%|-3.95%
    D9          -0.32%|-0.78%  +0.25%|-1.00%  +0.58%|-1.72%  +1.34%|-2.37%  +1.48%|-4.31%
    D10         -0.04%|-0.81%  -0.00%|-1.10%  -0.12%|-2.33%  +0.52%|-3.93%  +0.67%|-5.47%
    D10−D1               -0.08%           -0.23%           -0.10%           -0.02%           -0.15%
  z_tone_chg                1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1212)
    D1          -0.10%|-0.60%  -0.24%|-0.78%  -0.25%|-1.52%  -0.65%|-2.73%  -1.65%|-6.48%
    D2          -0.34%|-0.54%  -0.56%|-1.20%  -0.75%|-2.23%  -1.01%|-3.89%  +0.16%|-4.67%
    D5          +0.17%|-0.48%  +0.52%|-0.65%  +0.64%|-1.46%  +0.98%|-3.05%  +1.32%|-4.45%
    D9          +0.39%|-0.37%  +0.35%|-1.06%  +0.45%|-2.01%  +1.26%|-2.69%  +1.02%|-4.91%
    D10         -0.38%|-0.71%  -0.36%|-1.40%  -0.44%|-1.78%  -0.55%|-2.97%  -0.73%|-5.04%
    D10−D1               -0.28%           -0.13%           -0.19%           +0.09%           +0.92%
  HOT                       1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1183)
    D1          -0.04%|-0.39%  -0.21%|-0.86%  -0.08%|-1.69%  +1.04%|-2.74%  +1.43%|-4.62%
    D2          -0.44%|-0.82%  -0.20%|-1.37%  -0.32%|-2.34%  -0.24%|-3.59%  +0.46%|-4.28%
    D5          +0.15%|-0.45%  +0.32%|-0.89%  +0.30%|-1.72%  -0.17%|-4.04%  -0.57%|-5.93%
    D9          +0.13%|-0.53%  +0.46%|-1.01%  +0.63%|-1.64%  +1.69%|-3.13%  +2.22%|-4.59%
    D10         -0.34%|-0.89%  -0.62%|-1.30%  -0.65%|-2.46%  -0.24%|-3.21%  +0.29%|-5.17%
    D10−D1               -0.30%           -0.41%           -0.58%           -1.28%           -1.14%
  CROWD                     1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1073)
    D1          +0.46%|-0.47%  +1.26%|-0.73%  +2.92%|-1.40%  +6.57%|-2.22%  +11.62%|-2.81%
    D2          +0.15%|-0.37%  +0.51%|-0.73%  +0.44%|-1.52%  +1.72%|-2.74%  +3.13%|-2.72%
    D5          -0.25%|-0.46%  -0.39%|-1.18%  -0.69%|-1.84%  -1.30%|-3.42%  -2.84%|-6.05%
    D9          -0.05%|-0.46%  -0.26%|-1.12%  -0.67%|-1.84%  -1.83%|-4.34%  -2.60%|-5.60%
    D10         -0.15%|-0.64%  -0.64%|-1.06%  -1.24%|-2.61%  -2.26%|-4.36%  -3.43%|-6.14%
    D10−D1               -0.61%           -1.90%           -4.16%           -8.83%          -15.05%
  SQUEEZE                   1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1078)
    D1          -0.44%|-0.64%  -0.68%|-1.16%  -0.93%|-1.89%  -1.65%|-2.90%  -2.27%|-4.69%
    D2          -0.21%|-0.43%  -0.39%|-0.85%  -0.78%|-1.92%  -1.66%|-3.49%  -3.77%|-6.45%
    D5          +0.03%|-0.24%  +0.00%|-0.56%  -0.40%|-1.95%  -1.72%|-4.01%  -2.98%|-5.73%
    D9          +0.04%|-0.82%  +0.08%|-0.76%  +1.13%|-2.03%  +2.07%|-4.71%  +4.49%|-5.43%
    D10         +0.69%|-0.35%  +1.47%|-0.79%  +2.97%|-1.30%  +6.35%|-1.79%  +10.29%|-2.87%
    D10−D1               +1.13%           +2.15%           +3.90%           +8.00%          +12.56%
  z_si                      1w               2w               4w               8w              12w   mean | median   (n per cell ≈ 1092)
    D1          -0.31%|-0.67%  -0.81%|-1.38%  -1.77%|-2.62%  -4.34%|-5.41%  -7.16%|-7.41%
    D2          -0.45%|-0.83%  -0.91%|-1.37%  -1.99%|-2.91%  -4.28%|-4.67%  -6.47%|-8.15%
    D5          -0.06%|-0.59%  -0.25%|-0.85%  -0.18%|-1.41%  +0.22%|-1.71%  +0.32%|-2.23%
    D9          +0.62%|-0.25%  +1.08%|-0.59%  +2.09%|-1.28%  +4.95%|-2.59%  +7.05%|-4.22%
    D10         +0.46%|-0.68%  +1.40%|-0.98%  +3.53%|-1.73%  +7.22%|-3.59%  +12.00%|-3.81%
    D10−D1               +0.77%           +2.21%           +5.30%          +11.56%          +19.16%

H2 — very hot (attention z ≥ 1.5) split by what price did the SAME week
  hot & up ≥ +3% rel                       n= 408  +0.11% (hit 46%, t +0.3)  +0.90% (hit 44%, t +1.0)  +4.75% (hit 44%, t +2.2)
  hot & flat                               n= 226  -0.50% (hit 45%, t -1.2)  +0.26% (hit 40%, t +0.3)  -2.65% (hit 41%, t -1.4)
  hot & down ≤ −3% rel                     n= 297  -0.21% (hit 46%, t -0.5)  -1.74% (hit 35%, t -2.1)  -3.61% (hit 39%, t -2.2)
  hot & down ≤ −8% rel (capitulation?)     n= 150  -0.27% (hit 45%, t -0.4)  -1.48% (hit 34%, t -1.0)  -1.71% (hit 43%, t -0.7)
  very hot z ≥ 2.5, any                    n= 238  +0.23% (hit 49%, t +0.5)  -0.81% (hit 38%, t -0.8)  -0.60% (hit 39%, t -0.2)
  cold z ≤ −1.5, any                       n= 650  -0.05% (hit 48%, t -0.2)  +0.17% (hit 47%, t +0.3)  +3.06% (hit 46%, t +2.0)
  euphoria: att z ≥1.5 & tone z ≥1         n= 421  -0.16% (hit 48%, t -0.5)  -0.11% (hit 40%, t -0.2)  -0.71% (hit 39%, t -0.5)
  panic: att z ≥1.5 & tone z ≤ −1          n= 100  -0.89% (hit 43%, t -1.6)  -1.73% (hit 33%, t -1.3)  -6.43% (hit 41%, t -2.8)

H3 — hot (attention z ≥ 1) × short-interest tercile
  hot & lowSI   n= 435  -0.44% (t -1.4)  -1.79% (t -3.1)  -5.59% (t -4.5)
  hot & midSI   n= 502  +0.21% (t +0.8)  -0.11% (t -0.2)  -1.03% (t -0.7)
  hot & highSI  n= 520  +0.21% (t +0.5)  +2.20% (t +2.3)  +8.59% (t +3.7)
  cold & lowSI  n= 353  +0.10% (t +0.4)  -0.25% (t -0.4)  -2.68% (t -1.5)
  cold & highSI n= 504  -0.07% (t -0.2)  +1.44% (t +1.6)  +11.26% (t +4.8)

H4 — consecutive weeks in the top attention quintile (streak length at week t) → forward
  streak =1   n=1731  -0.11% (t -0.6)  -0.29% (t -0.7)  +0.06% (t +0.1)
  streak =2   n= 305  +0.41% (t +0.8)  +1.40% (t +1.3)  +4.23% (t +1.7)
  streak =3   n=  50  -0.29% (t -0.3)  +2.26% (t +0.9)  +5.67% (t +0.8)
  streak ≥4   n=  16  -0.96% (t -0.4)  +5.82% (t +1.0)  +11.12% (t +1.2)

H5/H6/H7/H9/H10 — rank IC by horizon (raw | controlling for past-4w return)
  H5 tone residual (ex same-week return)       1w:+0.007|+0.003(t+0.3)  2w:+0.014|+0.007(t+0.7)  4w:+0.013|+0.006(t+0.6)  8w:+0.007|+0.000(t+0.0)
  H6 divergence: tone-chg z − same-week ret z  1w:-0.008|+0.002(t+0.2)  2w:-0.013|+0.002(t+0.2)  4w:-0.027|-0.005(t-0.4)  8w:-0.036|-0.015(t-1.3)
  H7 attention acceleration                    1w:-0.008|-0.006(t-0.6)  2w:-0.009|-0.011(t-1.2)  4w:-0.001|-0.004(t-0.4)  8w:+0.001|-0.001(t-0.1)
  H9 Twitter tone − news tone                  1w:+0.004|+0.006(t+0.5)  2w:+0.002|+0.003(t+0.3)  4w:-0.010|-0.007(t-0.7)  8w:-0.003|+0.000(t+0.0)
  H10 short-interest 4w change                 1w:-0.017|-0.015(t-1.5)  2w:-0.027|-0.024(t-2.2)  4w:-0.019|-0.017(t-1.5)  8w:-0.012|-0.012(t-1.2)
  NEW crowding: attention − short interest     1w:-0.005|-0.005(t-0.4)  2w:-0.020|-0.021(t-1.7)  4w:-0.024|-0.023(t-1.7)  8w:-0.028|-0.027(t-1.9)
  NEW squeeze: attention + short interest      1w:-0.001|-0.006(t-0.5)  2w:+0.001|-0.008(t-0.6)  4w:+0.005|-0.002(t-0.2)  8w:+0.002|-0.008(t-0.6)
  ref: short interest level                    1w:+0.010|+0.005(t+0.3)  2w:+0.024|+0.019(t+1.1)  4w:+0.033|+0.027(t+1.6)  8w:+0.031|+0.020(t+1.0)
  ref: attention                               1w:-0.004|-0.006(t-0.6)  2w:-0.009|-0.017(t-1.7)  4w:-0.006|-0.012(t-1.2)  8w:-0.010|-0.015(t-1.5)
  ref: tone                                    1w:+0.008|-0.002(t-0.2)  2w:+0.016|-0.003(t-0.3)  4w:+0.026|+0.004(t+0.4)  8w:+0.026|+0.001(t+0.1)
  ref: same-week return (reversal?)            1w:-0.000|-0.009(t-0.6)  2w:+0.004|-0.018(t-1.2)  4w:+0.021|-0.005(t-0.3)  8w:+0.040|+0.015(t+0.9)
  ref: past-4w return (momentum)               1w:+0.029|+0.000(t  –)  2w:+0.044|+0.000(t  –)  4w:+0.061|+0.000(t  –)  8w:+0.056|+0.000(t  –)

H8 — whole-universe attention (total tweets vs trailing 4w) vs the universe's own forward return
  Q1 quietest  weeks= 34  1w:+1.03%  4w:+6.00%  12w:+24.43%
  Q2           weeks= 34  1w:+2.19%  4w:+6.26%  12w:+20.66%
  Q3           weeks= 34  1w:+1.14%  4w:+4.06%  12w:+12.38%
  Q4 loudest   weeks= 35  1w:+1.04%  4w:+6.18%  12w:+15.45%
  Spearman(agg attention, universe fwd): 1w:-0.04(n=136)  2w:+0.07(n=135)  4w:+0.02(n=133)  8w:-0.13(n=129)  12w:-0.14(n=125)

OOS — the conditionals that looked interesting, fit years vs 2026
  hot & up ≥3%       24-25: n= 288 4w -0.90% (t -0.9) 12w +2.37% (t +1.1)   |  2026: n= 120 4w +5.52% (t +2.6) 12w +12.43% (t +2.3)
  hot & down ≤−8%    24-25: n=  98 4w -1.30% (t -0.9) 12w -2.50% (t -0.9)   |  2026: n=  52 4w -1.92% (t -0.6) 12w +0.77% (t +0.1)
  euphoria           24-25: n= 298 4w -0.64% (t -0.9) 12w -2.49% (t -1.6)   |  2026: n= 123 4w +1.35% (t +0.7) 12w +5.65% (t +1.3)
  panic              24-25: n=  80 4w -0.63% (t -0.5) 12w -6.46% (t -2.9)   |  2026: n=  20 4w -6.71% (t -1.9) 12w -6.20% (t -0.6)
  streak ≥4          24-25: n=  12 4w +10.65% (t +1.8) 12w +15.83% (t +1.6)   |  2026: n=   4 4w -3.83% (t -0.3) 12w -7.76% (t   –)
  cold z≤−1.5        24-25: n= 492 4w -0.70% (t -1.3) 12w +1.95% (t +1.4)   |  2026: n= 158 4w +3.17% (t +1.8) 12w +8.49% (t +1.4)
  tone_resid         ex-mom IC  24-25: 1w:+0.006 4w:+0.004 8w:+0.002   |  2026: 1w:-0.004 4w:+0.011 8w:-0.006
  diverg             ex-mom IC  24-25: 1w:+0.001 4w:-0.005 8w:-0.010   |  2026: 1w:+0.005 4w:-0.003 8w:-0.034
  att_accel          ex-mom IC  24-25: 1w:-0.011 4w:-0.003 8w:-0.003   |  2026: 1w:+0.007 4w:-0.009 8w:+0.005
  z_si_chg           ex-mom IC  24-25: 1w:-0.013 4w:-0.031 8w:-0.010   |  2026: 1w:-0.021 4w:+0.031 8w:-0.022

BY YEAR — the interaction cells and the composites, each calendar year separately (4w | 12w mean, t)
  hot & lowSI             2024: n=152 +0.45% (t+0.5) | -0.35% (t-0.3)  2025: n=172 -2.99% (t-4.1) | -8.56% (t-4.2)  2026: n=111 -3.12% (t-2.0) | -9.61% (t-2.5)
  hot & highSI            2024: n=181 +2.08% (t+1.4) | +6.06% (t+2.0)  2025: n=190 +1.26% (t+0.8) | +8.79% (t+2.2)  2026: n=149 +3.82% (t+1.9) | +12.75% (t+2.4)
  cold & highSI           2024: n=186 +1.35% (t+1.2) | +9.41% (t+3.2)  2025: n=185 +0.84% (t+0.7) | +5.65% (t+2.0)  2026: n=133 +2.44% (t+1.0) | +26.31% (t+3.2)
  cold & lowSI            2024: n=129 +1.76% (t+1.4) | +0.66% (t+0.3)  2025: n=139 -1.73% (t-2.1) | -1.50% (t-0.5)  2026: n= 85 -0.98% (t-0.6) | -14.72% (t-3.9)
  panic (hot & tone≤−1)   2024: n= 41 -1.00% (t-0.5) | -4.35% (t-1.7)  2025: n= 39 -0.26% (t-0.1) | -8.62% (t-2.3)  2026: n= 20 -6.71% (t-1.9) | -6.20% (t-0.6)
  hot & up ≥3%            2024: n=141 -0.26% (t-0.2) | +1.04% (t+0.5)  2025: n=147 -1.51% (t-1.0) | +3.65% (t+1.0)  2026: n=120 +5.52% (t+2.6) | +12.43% (t+2.3)
  hot & down ≤−3%         2024: n= 95 -2.37% (t-1.9) | -6.28% (t-2.9)  2025: n=123 -0.99% (t-0.9) | -2.97% (t-1.1)  2026: n= 79 -2.26% (t-0.9) | +0.31% (t+0.1)
  D10−D1 BULL       2024: 1w +0.75% 4w +3.22% 12w +9.89%  2025: 1w +0.19% 4w +2.63% 12w +11.18%  2026: 1w -0.48% 4w +1.01% 12w +7.25%
  ex-mom IC BULL       2024: 1w +0.008 4w +0.033 12w +0.027  2025: 1w +0.009 4w +0.016 12w +0.024  2026: 1w -0.018 4w +0.011 12w +0.074
  D10−D1 CROWD      2024: 1w -0.33% 4w -1.08% 12w -8.38%  2025: 1w -0.83% 4w -5.92% 12w -19.15%  2026: 1w -0.65% 4w -6.03% 12w -19.85%
  ex-mom IC CROWD      2024: 1w -0.010 4w +0.001 12w -0.010  2025: 1w -0.013 4w -0.045 12w -0.055  2026: 1w +0.014 4w -0.025 12w -0.028
  D10−D1 SQUEEZE    2024: 1w +0.63% 4w +1.86% 12w +5.61%  2025: 1w +1.39% 4w +3.33% 12w +13.86%  2026: 1w +1.45% 4w +8.06% 12w +24.33%
  ex-mom IC SQUEEZE    2024: 1w -0.037 4w -0.038 12w -0.037  2025: 1w +0.009 4w +0.014 12w +0.033  2026: 1w +0.015 4w +0.028 12w +0.088
  D10−D1 z_si       2024: 1w +0.16% 4w +2.39% 12w +8.13%  2025: 1w +1.09% 4w +6.69% 12w +25.15%  2026: 1w +1.18% 4w +7.70% 12w +29.89%
  ex-mom IC z_si       2024: 1w -0.019 4w -0.027 12w -0.053  2025: 1w +0.025 4w +0.062 12w +0.096  2026: 1w +0.011 4w +0.060 12w +0.141
  D10−D1 z_tone     2024: 1w +0.29% 4w +1.81% 12w +4.39%  2025: 1w +0.32% 4w +1.56% 12w +3.76%  2026: 1w -0.36% 4w +2.03% 12w -0.48%
  ex-mom IC z_tone     2024: 1w -0.004 4w +0.005 12w -0.001  2025: 1w +0.014 4w +0.006 12w -0.009  2026: 1w -0.022 4w -0.003 12w +0.022
  D10−D1 z_att      2024: 1w -0.32% 4w -0.62% 12w -3.82%  2025: 1w +0.15% 4w +0.09% 12w +2.63%  2026: 1w +0.46% 4w +1.45% 12w +1.42%
  ex-mom IC z_att      2024: 1w -0.032 4w -0.014 12w -0.022  2025: 1w +0.004 4w -0.024 12w -0.010  2026: 1w +0.017 4w +0.011 12w +0.028
```
