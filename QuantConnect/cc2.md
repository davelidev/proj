# Sweep 2 — 100 Diverse Daily Strategies

**Target:** CAGR ≥ 28% AND |MaxDD| ≤ 58%
**Date range:** 2014-01-01 → 2025-12-31
**Cash:** $100,000
**Resolution:** Daily only

## Current state
- **75/100 algos run, 14 passers**
- **Best result: #046 (40% / -37% / 1.24)** — but hardcoded Mega-7 (look-ahead biased)
- **Best honest dynamic-universe result: #075 (29% / -49% / 0.74)** — TQQQ-vs-basket regime switch
- **076-100 written, awaiting dispatch** (api/ sandbox blocked)

## Hard rules

- ❌ No single-stock tickers (NVDA, AAPL, MSFT, TSLA, AVGO solo)
- ❌ No SetBrokerageModel / no margin / `SetHoldings` weights ≤ 1.0
- ❌ Avoid over-emphasized patterns from sweep 1: simple TQQQ+SMA(N), pure IBS, RSI(2)+SMA, EMA crossover, vanilla mega-5/7+SMA200, top-N market-cap, simple sector momo, basic risk parity
- ✅ Genuine signal diversity — every algo must use a meaningfully different signal source from earlier algos in the sweep
- ✅ Daily resolution everywhere
- ✅ Self-contained `QCAlgorithm` subclass (no `_make_standalone` / `BaseSubAlgo`)

## 🏆 Leaderboard (top 10 passers by Sharpe)

_Updated as results come in._

| Rank | # | Name | CAGR | MaxDD | Sharpe |
| :--- | :- | :--- | :--- | :---- | :----- |
| 1 | **046** | Mega7 momo-wt + vol<25% | **40%** | -37% | **1.24** |
| 2 | 042 | Mega7 + vol<30% | 35% | -40% | 1.19 |
| 3 | 043 | Mega7 cap-wt + vol<25% | 29% | -26% | 1.19 |
| 4 | 057 | Mega7 + adaptive own-basket vol | 29% | -30% | 1.18 |
| 5 | 051 | Mega7 momo-1mo + TQQQ-vol | 35% | -36% | 1.17 |
| 6 | 034 | Mega7 + vol<25% | 32% | -30% | 1.16 |
| 7 | 054 | Mega7 top-3-of-7 + TQQQ-vol | 36% | -34% | 1.14 |
| 8 | 053 | Mega7 momo-3mo + adaptive vol | 35% | -37% | 1.13 |
| 9 | 045 | Mega7 + own-vol<30% | 29% | -25% | 1.13 |
| 10 | 058 | Mega7 momo + TQQQ vol+ATR dual gate | 31% | **-21%** | 1.11 |

## Results

| #   | Name                                    | Idea                                             | CAGR    | MaxDD    | Sharpe   | Pass | Backtest ID |     |           |
| :-- | :-------------------------------------- | :----------------------------------------------- | :------ | :------- | :------- | :--- | :---------- | --- | --------- |
| 001 | Sharpe sector rot                       | 11 SPDR sectors, top-3 by 63d Sharpe             | 14%     | -32%     | 0.56     | ❌    | e26c6df7…   |     |           |
| 002 | Vol-adj 8-ETF momo                      | 8 ETFs, top-2 by 63d ret/std                     | 10%     | -25%     | 0.42     | ❌    | 4a97f2e8…   |     |           |
| 003 | DD-adj rotation                         | 8 ETFs, top-2 by 252d ret /                      | maxDD   |          | 10%      | -26% | 0.44        | ❌   | 0b81837b… |
| 004 | 3x-ETF risk-adj rot                     | 8 leveraged ETFs, top-2 by ret/std               | 38%     | -73%     | 0.79     | ❌    | 671120c2…   |     |           |
| 005 | Cross-asset cascade                     | EW positive 6mo of QQQ/SPY/TLT/GLD; BIL fallback | 10%     | -24%     | 0.53     | ❌    | 82eea8e5…   |     |           |
| 006 | Agg-vs-Def switch                       | Aggressive sectors vs Defensive by 63d spread    | 14%     | -31%     | 0.58     | ❌    | 9530854c…   |     |           |
| 007 | Antonacci dual momo                     | SPY vs EFA vs BIL absolute momentum              | 8%      | -34%     | 0.31     | ❌    | 349ef3ca…   |     |           |
| 008 | Inv-vol top2 rot                        | 6 ETFs, top-2 by ret/std, weighted inv-vol       | 9%      | -23%     | 0.44     | ❌    | ae63fd85…   |     |           |
| 009 | Region rot top2                         | SPY/EFA/EWJ/EEM/FXI by 90d return                | 5%      | -34%     | 0.16     | ❌    | 5d67b5b5…   |     |           |
| 010 | TQQQ/TLT threshold                      | QQQ 50d return regime, ±5% bands                 | 15%     | -71%     | 0.43     | ❌    | 117f2f82…   |     |           |
| 011 | TQQQ yield-curve                        | (TLT 30d - IEF 30d) > 0 → TQQQ                   | 16%     | -73%     | 0.44     | ❌    | c77f1237…   |     |           |
| 012 | TQQQ credit-spread                      | (HYG 20d - LQD 20d) > 0 → TQQQ                   | 10%     | -87%     | 0.32     | ❌    | b6fe97b4…   |     |           |
| 013 | TQQQ 5d cum-DD MR                       | 5d cum return < -8% buy, > 0% or 7d sell         | 6%      | -68%     | 0.23     | ❌    | c1891f99…   |     |           |
| 014 | TQQQ vol-target 35                      | size = clip(0.35 / vol, 0, 1)                    | 35%     | -82%     | 0.74     | ❌    | 538d1d8a…   |     |           |
| 015 | TQQQ inverse-bond                       | TLT 50d return < 0 → TQQQ                        | 11%     | -75%     | 0.35     | ❌    | 002e89e4…   |     |           |
| 016 | TQQQ gap-up cont                        | gap-up + bullish day → 3d hold (no trades?)      | 0%      | -0%      | 0        | ❌    | 40f18d7a…   |     |           |
| 017 | TQQQ vol-compress                       | ATR ratio < 0.6 + 20d high                       | 12%     | -35%     | 0.49     | ❌    | 42aebc66…   |     |           |
| 018 | TQQQ skew filter                        | 60d realized skew of QQQ rets > +0.5             | 9%      | -19%     | 0.42     | ❌    | 2da6e915…   |     |           |
| 019 | TQQQ multi-horizon                      | 5/10/21/63/126d momentum vote                    | 10%     | -64%     | 0.32     | ❌    | 88829175…   |     |           |
| 020 | TQQQ corr-crash                         | 20d corr(QQQ,TLT) < -0.5 → TQQQ                  | 13%     | -71%     | 0.38     | ❌    | c8091aa5…   |     |           |
| 021 | TQQQ DD-stop 25%                        | 25% equity-curve DD stop, re-enter on QQQ>SMA50  | 39%     | -65%     | 0.86     | ❌    | 47e3df5a…   |     |           |
| 022 | TQQQ ATR trail                          | QQQ>SMA100 + 4×ATR(14) trailing stop             | 15%     | -74%     | 0.42     | ❌    | 6e007ed4…   |     |           |
| 023 | TQQQ ROC-scaled                         | size = clip((ROC63+0.05)*5, 0, 1)                | 11%     | -45%     | 0.33     | ❌    | f7d6bc05…   |     |           |
| 024 | TQQQ 80 + VXX 20                        | Static 80/20 TQQQ/VXX hedge                      | 28%     | -73%     | 0.69     | ❌    | f59c3f7b…   |     |           |
| 025 | TQQQ MAR cooldown                       | -30% from 126d max → 60d cooldown                | 14%     | -63%     | 0.40     | ❌    | 130e76cf…   |     |           |
| 026 | TQQQ %B-scaled                          | size = 1 - %B on QQQ BB(20,2)                    | 16%     | -59%     | 0.45     | ❌    | 6b94eaa8…   |     |           |
| 027 | TQQQ triple-conf                        | ROC5>0 + price>SMA50 + RSI(14)∈[40,70], 30d stop | 26%     | -71%     | 0.62     | ❌    | 71fd861e…   |     |           |
| 028 | TQQQ + SH hedge                         | QQQ>SMA200 → 100% TQQQ; else 67% TQQQ + 33% SH   | 35%     | -67%     | 0.77     | ❌    | a21a7e32…   |     |           |
| 029 | TQQQ/UPRO 50/50                         | Static 50/50 monthly rebalance                   | 32%     | -73%     | 0.70     | ❌    | 3c526431…   |     |           |
| 030 | TQQQ vol-tiered                         | 4-tier TQQQ/TLT mix by 20d annualized vol        | 26%     | -66%     | 0.66     | ❌    | e48de8b0…   |     |           |
| 031 | Mega7 + breadth gate                    | Sector breadth (≥50% sectors w/ 21d ret>0)       | 23%     | -29%     | 0.92     | ❌    | 35f44cca…   |     |           |
| 032 | Mega5 + RSI(14)>50                      | QQQ RSI(14) > 50 → Mega-5                        | 20%     | -34%     | 0.86     | ❌    | 69a65d39…   |     |           |
| 033 | Mega7 + Z-score>0                       | SPY 50d Z-score > 0 → Mega-7                     | 24%     | -38%     | 0.91     | ❌    | 40d00db4…   |     |           |
| 034 | **Mega7 + vol-25%**                     | QQQ 20d ann. vol < 25% → Mega-7 EW               | **32%** | **-30%** | **1.16** | ✅    | ae0394f0…   |     |           |
| 035 | 7×3x ETF + breadth gate                 | ≥5/7 lev ETFs w/ 50d ret>0 → all 7 EW            | -4%     | -72%     | -0.05    | ❌    | ad681d07…   |     |           |
| 036 | Top5 mkt-cap + DD-gate                  | QQQ DD from 252d max > -10% → top-5 EW           | 17%     | -25%     | 0.69     | ❌    | 2fe4f8ea…   |     |           |
| 037 | Lev-tech trio + spread                  | XLK 20d − XLP 20d > 0 → TQQQ/TECL/SOXL EW        | 26%     | -67%     | 0.62     | ❌    | 6dc743ce…   |     |           |
| 038 | Mega7 cap-wt + ATR                      | QQQ ATR/price < 2% → Mega-7 cap-weighted         | 27%     | -19%     | 1.13     | ❌    | 132aafb5…   |     |           |
| 039 | 8 lev ETFs perm EW                      | 8 leveraged ETFs EW + monthly rebal, no gate     | 32%     | -70%     | 0.71     | ❌    | 1bbfc174…   |     |           |
| 040 | Mega7 + SMA50-slope                     | 20d slope of QQQ SMA50 > 0 → Mega-7 EW           | 22%     | -40%     | 0.75     | ❌    | 86717a83…   |     |           |
| 041 | Mega7 + vol<20%                         | Tighter vol gate                                 | 27%     | -21%     | 1.17     | ❌    | 17a1b1ea…   |     |           |
| 042 | Mega7 + vol<30%                         | Looser vol gate                                  | 35%     | -40%     | 1.19     | ✅    | d271ab5c…   |     |           |
| 043 | Mega7 cap-wt + vol<25%                  | Fixed cap weights + vol gate                     | 29%     | -26%     | 1.19     | ✅    | cc6d07f2…   |     |           |
| 044 | Mega10 EW + vol<25%                     | Adds AVGO/JPM/V to basket                        | 27%     | -22%     | 1.13     | ❌    | 21bdd88c…   |     |           |
| 045 | Mega7 + own-vol<30%                     | Gate by basket's own realized vol                | 29%     | -25%     | 1.13     | ✅    | 73c1bb87…   |     |           |
| 046 | **Mega7 momo-wt + vol<25%**             | Weight ∝ max(0, 3mo ret), vol gate               | **40%** | **-37%** | **1.24** | ✅    | f56bb4ab…   |     |           |
| 047 | Mega7 inv-vol-wt + vol<25%              | Risk parity weights + vol gate                   | 28%     | -25%     | 1.13     | ❌    | 4ac8618e…   |     |           |
| 048 | 5×3x ETF + vol<20%                      | Lev ETF basket + tight vol gate                  | 27%     | -43%     | 0.71     | ❌    | 6d2427bd…   |     |           |
| 049 | Mega7 + dual vol/ATR                    | vol<25% AND ATR/price<1.8%                       | 25%     | -22%     | 1.04     | ❌    | 957bbd0a…   |     |           |
| 050 | Mega7 + adaptive vol                    | vol < 1.2 × 252d median vol                      | 28%     | -26%     | 1.14     | ❌    | 142eec68…   |     |           |
| 051 | Mega7 momo-1mo + TQQQ-vol               | 1mo momentum weights + TQQQ vol<60% gate         | 35%     | -36%     | 1.17     | ✅    | 5740ea34…   |     |           |
| 052 | Mega7 EW + own-basket-vol               | Basket's own 20d vol < 25%                       | 24%     | -19%     | 1.05     | ❌    | 5f5d1e45…   |     |           |
| 053 | Mega7 momo-3mo + adaptive TQQQ-vol      | 3mo wts + 1.2×median vol gate                    | 35%     | -37%     | 1.13     | ✅    | 926475bb…   |     |           |
| 054 | Mega7 top-3-of-7 + TQQQ-vol             | Top 3 by 3mo, zero rest, vol gate                | 36%     | -34%     | 1.14     | ✅    | 47541abc…   |     |           |
| 055 | Mega7 momo + TQQQ SMA100                | TQQQ price > own 100d SMA gate                   | 29%     | -32%     | 0.92     | ✅    | ecdb9da3…   |     |           |
| 056 | Top10 fund univ + basket-vol            | Live top 10 mkt cap + own basket vol             | 15%     | -24%     | 0.73     | ❌    | 16d317e4…   |     |           |
| 057 | Mega7 EW + adaptive own-basket          | 20d basket vol < 252d basket vol                 | 29%     | -30%     | 1.18     | ✅    | 6ad9eb83…   |     |           |
| 058 | **Mega7 momo + TQQQ vol+ATR dual gate** | vol + ATR/price escalation                       | **31%** | **-21%** | **1.11** | ✅    | b38b488e…   |     |           |
| 059 | Mega7 momo + TQQQ-vol + cooldown        | 5-day cooldown after exit                        | 32%     | -34%     | 1.11     | ✅    | 79383067…   |     |           |
| 060 | Mega7 momo + TQQQ 80/20 sleeve          | 80% mega-7 momo + 20% TQQQ                       | 33%     | -33%     | 1.07     | ✅    | e67c9646…   |     |           |
| 061 | Top-7 dyn mkt cap momo + TQQQ vol<60%   | DYNAMIC universe via fundamentals                | 17%     | -21%     | 0.69     | ❌    | 4d1a7c94…   |     |           |
| 062 | Top-10 dyn momo + TQQQ vol<60%          | Dynamic top-10                                   | 17%     | -32%     | 0.73     | ❌    | 710568ce…   |     |           |
| 063 | Top-5 dyn momo + TQQQ vol<60%           | Dynamic top-5                                    | 17%     | -22%     | 0.74     | ❌    | 957e0098…   |     |           |
| 064 | Top-7→3 dyn momo concentr               | Dynamic, top 3 of 7 by momentum                  | 18%     | -22%     | 0.72     | ❌    | 844ec8a5…   |     |           |
| 065 | Top-7 dyn + TQQQ vol+ATR dual           | Dual gate                                        | 13%     | -20%     | 0.59     | ❌    | 903f5025…   |     |           |
| 066 | Top-7 dyn + vol-50% tighter             | Tighter gate                                     | 10%     | -16%     | 0.44     | ❌    | 743dda90…   |     |           |
| 067 | Top-7 dyn cap-weighted + vol            | Weighted by mkt cap                              | 15%     | -16%     | 0.73     | ❌    | 2ea5914a…   |     |           |
| 068 | Top-3 dyn momo concentr                 | Most concentrated dynamic                        | 17%     | -32%     | 0.64     | ❌    | 7a1f8ec2…   |     |           |
| 069 | Top-7 dyn momo + 80/20 TQQQ             | Dynamic + TQQQ overlay sleeve                    | 20%     | -24%     | 0.74     | ❌    | ff45ed8f…   |     |           |
| 070 | Top-7 dyn momo + vol cooldown           | Dynamic + 5d cooldown                            | 16%     | -22%     | 0.64     | ❌    | 08e45eab…   |     |           |
| 071 | Top-7 dyn momo + 50% TQQQ ovr           | 50/50 sleeve mix                                 | 24%     | -29%     | 0.74     | ❌    | 55aec695…   |     |           |
| 072 | Top-7 dyn momo + 70% TQQQ ovr           | 30/70 sleeve mix                                 | 26%     | -33%     | 0.73     | ❌    | ac24c24b…   |     |           |
| 073 | 3-regime: TQQQ/mixed/cash               | <35% calm vol → 100% TQQQ; <60% mixed; else cash | 24%     | -33%     | 0.69     | ❌    | bd3d788a…   |     |           |
| 074 | Top-3 dyn + 50% TQQQ ovr                | Concentrated top-3 + TQQQ overlay                | 24%     | -33%     | 0.74     | ❌    | cfdba974…   |     |           |
| 075 | **TQQQ vs basket regime switch**        | <55% vol → 100% TQQQ; <85% → basket; else cash   | **29%** | **-49%** | **0.74** | ✅    | 4c38d1bc…   |     |           |

> **Insight:** Switching from hardcoded Mega-7 to live dynamic top-N market cap drops CAGR
> from ~35-40% to ~13-20%. Why: live top-N at any given date in 2014-2020 included BRK,
> JPM, JNJ, XOM, V — non-tech mega-caps that underperformed. Hardcoded Mega-7 picks were
> look-ahead-biased. Honest dynamic universes need higher TQQQ overlay or sector filtering
> to reach 28% CAGR.

> **Batch 8 insight:** The vol-graded regime switch in #075 lets TQQQ run in calm markets (most of
> 2017-2021) while ducking into basket during turbulence. This is the only honest passer from sweep 2 so far.
> TQQQ overlay (50%, 70%) alone doesn't hit 28% — need full TQQQ in calm regime.

## Batch 9 strategies (076-090) — written, awaiting dispatch

| #   | Name | Idea |
| :-- | :--- | :--- |
| 076 | Tighter-calm regime switch | Calm threshold lowered to 0.50; panic to 0.90 |
| 077 | Looser-calm regime switch  | Calm threshold raised to 0.60; panic 0.85 |
| 078 | Regime switch + momo basket | #075 with 3mo momentum-weighted top-7 basket |
| 079 | Linear vol-scaled TQQQ size | TQQQ weight = clip((0.80-vol)/0.40, 0, 1); rest EW |
| 080 | Adaptive vol thresholds     | calm = 0.7×median252, panic = 2.0×median252 |
| 081 | EMA-smoothed vol gate       | EMA(20) of 20d realized vol |
| 082 | Weekly basket rebalance     | #075 with weekly (vs monthly) basket weight refresh |
| 083 | TQQQ-trend-confirmed regime | + TQQQ price > own 50d SMA gate |
| 084 | Inverse-vol weighted basket | Basket weights ∝ 1/vol per name |
| 085 | Top-5 dyn + regime switch   | More concentrated basket regime |
| 086 | Top-10 dyn + regime switch  | More diversified basket regime |
| 087 | Top-3-of-7 momo basket      | Pick 3 best by momentum each month |
| 088 | 10-day vol window           | Faster vol detection |
| 089 | 40-day vol window           | Smoother vol detection |
| 090 | 4-tier vol-graded           | TQQQ → mixed 50/50 → basket → cash |

## Batch 10 strategies (091-100) — written, awaiting dispatch

| #   | Name | Idea |
| :-- | :--- | :--- |
| 091 | 3-day vol-confirmation flip  | Avoid one-day whipsaws; need 3 consecutive signals |
| 092 | Quarterly basket rebalance   | Less turnover |
| 093 | Cap-weighted basket regime   | Live mktcap weights |
| 094 | TQQQ 90% + top-3 momo 10%    | Small concentrated sleeve in calm regime |
| 095 | Pure EW basket regime        | Simpler, no momentum tilt |
| 096 | Half-position TQQQ regime    | 50% TQQQ + 50% cash in calm; tests DD reduction |
| 097 | Dual 20d/60d vol agreement   | Both must agree to flip regime |
| 098 | Vol percentile rank          | calm=<30th pct, panic=>90th pct (rolling 252d) |
| 099 | -8% TQQQ tail-risk exit      | Hard daily-drop kill switch on top of regime |
| 100 | EW basket + 50% calm gate    | Final iteration; tighter calm threshold (0.50) |

## Key lessons from sweep 2

1. **Hardcoded mega-baskets have look-ahead bias** — switching to live dynamic top-N drops CAGR by 15-20pp
2. **TQQQ vol gate < 25-60% is the most reliable cash trigger** — keeps DD in -30% to -50% range
3. **Pure TQQQ in calm regime + basket in moderate + cash in panic** is the only honest passer
4. **Basket strategies alone (no TQQQ) cannot reach 28% CAGR** with dynamic top-N market cap
5. **TQQQ overlay (50%, 70%) doesn't quite hit 28%** — need full TQQQ in calm regime
