# Algo Sweep 2 — 100 Multi-Asset Strategies

**Target:** CAGR ≥ 28% AND MaxDD ≤ 58%
**Asset:** Multi-asset (sector ETFs, equities, fixed income, commodities)
**Date range:** 2014-01-01 → 2025-12-31
**Cash:** $100,000

## 🏆 Leaderboard (top 10 passers by Sharpe)

| Rank | #   | Name    | Idea | CAGR | MaxDD | Sharpe |
| :--- | :-- | :------ | :--- | :--- | :---- | :----- |
| 1 | **045** | Algo045 | Mega-7 EW + own-basket 20d annualized vol < 30% gate. | **40%** | **-37%** | **1.235** |
| 2 | **046** | Algo046 | Mega-7 + QQQ 20d vol < 25% gate + monthly 3mo-momentum weighting. | **40%** | **-37%** | **1.235** |
| 3 | **043** | Algo043 | Mega-7 fixed cap-weights + QQQ 20d annualized vol < 25% gate. | **29%** | **-26%** | **1.188** |
| 4 | 044 | Algo044 | Mega-10 EW + QQQ 20d annualized vol < 25% gate. | 29% | -26% | 1.188 |
| 5 | 042 | Algo042 | Mega-7 EW + QQQ 20d annualized vol < 30% gate (looser). | 35% | -40% | 1.187 |
| 6 | 041 | Algo041 | Mega-7 EW + QQQ 20d annualized vol < 20% gate (tighter). | 35% | -40% | 1.187 |
| 7 | 050 | Algo050 | Mega-7 EW + adaptive vol gate: today's QQQ 20d vol < 1.2 x its 252d median. | 28% | -26% | 1.140 |
| 8 | 049 | Algo049 | Mega-7 EW + dual gate: QQQ 20d ann. vol < 25% AND ATR(14)/price < 1.8%. | 28% | -26% | 1.140 |
| 9 | 053 | Algo053 | #053 — Mega-7 momo-weighted (3mo) + TQQQ vol-60 + adaptive median gate. | 36% | -34% | 1.138 |
| 10 | 054 | Algo054 | #054 — Mega-7 top-3 by 3mo momentum (zero-out bottom 4) + TQQQ vol gate. | 36% | -34% | 1.138 |

## Results

| #   | Name    | Idea | CAGR | MaxDD | Sharpe | Orders | Win % | P/L  | Pass | Backtest ID |
| :-- | :------ | :--- | :--- | :---- | :----- | :----- | :---- | :--- | :--- | :---------- |
| 001 | Algo001 | Sharpe-Ranked Sector Rotation: Hold top-3 of 11 sector ETFs by 63d Sharpe. | 14% | -32% | 0.562 | 554 | 73.0 | 0.95 | ❌ | 916a549d33680194707117e98bec187c |
| 002 | Algo002 | Volatility-Adjusted Momentum across 8 ETFs: top-2 by (63d return / 63d std). | 10% | -25% | 0.424 | 366 | 74.0 | 0.74 | ❌ | ce74c977a0b5c67ad240455f7688ffa5 |
| 003 | Algo003 | Drawdown-Adjusted Rotation: top-2 by 252d return divided by \|max drawdown\|. | 10% | -26% | 0.435 | 297 | 76.0 | 0.93 | ❌ | cbf071eb8c700366ec703ac3502742a3 |
| 004 | Algo004 | 3x ETF Rotation by Risk-Adjusted Return: top-2 of 8 leveraged ETFs at 50/50. | 38% | -73% | 0.792 | 412 | 69.0 | 1.04 | ❌ | 051bd42548ff442837957056187b70b8 |
| 005 | Algo005 | Cross-Asset Momentum Cascade: EW only positive 6mo-return assets, else BIL. | 10% | -24% | 0.526 | 385 | 81.0 | 0.75 | ❌ | 5e1828e021d69138dada3ff8a43c7151 |
| 006 | Algo006 | Defensive vs Aggressive Sector Pair Switch: aggressive basket if outperforming, else defensive. | 14% | -31% | 0.584 | 450 | 83.0 | 0.94 | ❌ | b49de0055e7c1b6bfa0dfaba68285f50 |
| 007 | Algo007 | Antonacci Dual Momentum (GTAA-style): SPY/EFA absolute & relative momentum vs BIL. | 14% | -31% | 0.584 | 450 | 83.0 | 0.94 | ❌ | f311ee2f2dec42b4de7b4facc0db7e90 |
| 008 | Algo008 | Equity-Bond-Gold Inverse-Vol Rotation Top 2 from a 6-asset universe. | 14% | -31% | 0.584 | 450 | 83.0 | 0.94 | ❌ | 34b987e0c00ca15cbe9ecd60f648fa03 |
| 009 | Algo009 | Region-Rotation: Top-2 of US/EU/JP/EM/CN by 90d return at 50/50. | 14% | -31% | 0.584 | 450 | 83.0 | 0.94 | ❌ | 3cee9666f988f86587004e3a3cc762c8 |
| 010 | Algo010 | TQQQ-or-bonds: Threshold-based regime switch using QQQ 50d return. | 14% | -31% | 0.584 | 450 | 83.0 | 0.94 | ❌ | 619704d9695e9ddd6799394ec1199469 |
| 011 | Algo011 | TQQQ gated by yield-curve flight-to-safety signal: TLT 30d return vs IEF 30d return. | 16% | -73% | 0.435 | 282 | 63.0 | 1.02 | ❌ | bd3d3d49eb52bc4b4849b95207af4961 |
| 012 | Algo012 | TQQQ gated by credit-spread risk-on signal: HYG 20d return vs LQD 20d return. | 16% | -73% | 0.435 | 282 | 63.0 | 1.02 | ❌ | f8058efcc4e90ec0aaaa7ba9b2636679 |
| 013 | Algo013 | TQQQ 5-day cumulative drawdown mean-reversion: buy after -8% 5d drop, exit on positive 5d or 7-day max hold. | 35% | -82% | 0.740 | 36 | 100.0 | 0.00 | ❌ | e3540538459f6ed77bd43ac3dd170c47 |
| 014 | Algo014 | Volatility-targeted TQQQ: size = clip(0.35 / annualized_realized_vol_QQQ, 0, 1). Trade only when \|dw\|>0.05. | 35% | -82% | 0.740 | 36 | 100.0 | 0.00 | ❌ | 94dfa9a09cde4c0bc64e793dcc3e5066 |
| 015 | Algo015 | TQQQ when TLT 50d return is negative (rates rising = risk-on growth tailwind); else flat. | 0% | -0% | 0.000 | 0 | 0.0 | 0.00 | ❌ | 6fcf0a9beb9efd658648cecef5a331e6 |
| 016 | Algo016 | TQQQ gap-up continuation: enter next-day after bullish gap-and-go; exit on 3-day hold or close < entry-day low. | 0% | -0% | 0.000 | 0 | 0.0 | 0.00 | ❌ | fe7c8f8e645c4a613f05e7a1902621ca |
| 017 | Algo017 | TQQQ vol compression-then-expansion: enter when ATR(14)/ATR(14, 60d ago) < 0.6 AND 20d high; exit on ratio > 1.2 or 15d hold. | 12% | -35% | 0.494 | 48 | 88.0 | 0.64 | ❌ | f3d0e898fe428f242df6a5c21006a38b |
| 018 | Algo018 | TQQQ gated by 60d realized skew of QQQ daily returns: skew > +0.5 → 100% TQQQ; else flat. Monthly recheck. | 12% | -35% | 0.494 | 48 | 88.0 | 0.64 | ❌ | 0a13c8d45edd06763ba3cf7f430ff57a |
| 019 | Algo019 | Multi-horizon momentum vote on QQQ across 5d/10d/21d/63d/126d. >=4 positive: TQQQ. <=1 positive: TLT. Else flat. | 10% | -64% | 0.315 | 544 | 45.0 | 1.63 | ❌ | 37dbc02f3404a2597e56c2260b373820 |
| 020 | Algo020 | TQQQ gated by 20d QQQ-TLT realized correlation: corr < -0.5 → 100% TQQQ; corr > 0 → flat. | 10% | -64% | 0.315 | 544 | 45.0 | 1.63 | ❌ | 87b630f15ee1655131f0db17a72f169f |
| 021 | Algo021 | TQQQ with Hard Equity-Curve Drawdown Stop (25% from peak). | 39% | -65% | 0.859 | 35 | 65.0 | 4.03 | ❌ | 2f2619f4569f0b3406adcb00cf04543c |
| 022 | Algo022 | Trailing ATR-Stop on QQQ-trended TQQQ (peak - 4*ATR(14)). | 39% | -65% | 0.859 | 35 | 65.0 | 4.03 | ❌ | 3528802028ab7dcb43b2f9935e8af489 |
| 023 | Algo023 | Scaled TQQQ position by QQQ 63d ROC strength, rest in BIL. | 11% | -45% | 0.334 | 2426 | 64.0 | 0.91 | ❌ | 1a0866bb3c15db938e8d4bc5b1fb3408 |
| 024 | Algo024 | 80% TQQQ + 20% VXX hedge overlay, monthly rebalance. | 11% | -45% | 0.334 | 2426 | 64.0 | 0.91 | ❌ | 725fefdf370af0c5c88a2fc439d5fd15 |
| 025 | Algo025 | TQQQ with 6-month drawdown stop and 60-day cooldown. | 16% | -59% | 0.447 | 1900 | 67.0 | 0.78 | ❌ | c44710adad5e028277df42449e15320c |
| 026 | Algo026 | TQQQ position scaled inversely to QQQ Bollinger %B (mean-reversion sizing). | 16% | -59% | 0.447 | 1900 | 67.0 | 0.78 | ❌ | 113685004bdad763bd2b0acb0602a5f8 |
| 027 | Algo027 | Triple-confirmation TQQQ entry with 30-day time-stop. | 26% | -71% | 0.623 | 167 | 66.0 | 1.10 | ❌ | a1780a2c6a484a47d045bb1b380a6170 |
| 028 | Algo028 | 100% TQQQ in uptrend, else 67% TQQQ + 33% SH inverse hedge. | 26% | -71% | 0.623 | 167 | 66.0 | 1.10 | ❌ | b36c73d4342d263715d3e03c7e6d5a13 |
| 029 | Algo029 | 50/50 TQQQ + UPRO with monthly rebalance — vol harvesting pair. | 32% | -73% | 0.700 | 254 | 99.0 | 21.31 | ❌ | 7beb87b231f5446ae17ad63f720046ca |
| 030 | Algo030 | Tiered vol-filter TQQQ/TLT scale-out by QQQ 20d annualized vol. | 32% | -73% | 0.700 | 254 | 99.0 | 21.31 | ❌ | a0c8febff457fbc5ee056634c25807a8 |
| 031 | Algo031 | algo_031.py | 20% | -34% | 0.858 | 1615 | 38.0 | 3.15 | ❌ | 2afd6a9c8c4b606ea1c43f31a374ca92 |
| 032 | Algo032 | algo_032.py | 20% | -34% | 0.858 | 1615 | 38.0 | 3.15 | ❌ | 21b15e16f2b2a68569fb51b4ff029464 |
| 033 | Algo033 | algo_033.py | 24% | -38% | 0.913 | 1477 | 40.0 | 3.46 | ❌ | 6ee6425f7d2459d058eff97e85cb0064 |
| 034 | Algo034 | algo_034.py | 24% | -38% | 0.913 | 1477 | 40.0 | 3.46 | ❌ | e88cb0b33557fe9b35b39def10b08ae3 |
| 035 | Algo035 | algo_035.py | -4% | -72% | -0.051 | 1883 | 41.0 | 1.35 | ❌ | 2f585be353e29cff59b603b2d82b1530 |
| 036 | Algo036 | algo_036.py | -4% | -72% | -0.051 | 1883 | 41.0 | 1.35 | ❌ | 05aee60aace49686238d25bb7020025c |
| 037 | Algo037 | algo_037.py | 26% | -67% | 0.624 | 891 | 47.0 | 1.84 | ❌ | 2857e5af355d6e1fd46ae91da0215b5b |
| 038 | Algo038 | algo_038.py | 26% | -67% | 0.624 | 891 | 47.0 | 1.84 | ❌ | 1046e8362c294bfa022dfe9d19e647cb |
| 039 | Algo039 | algo_039.py | 22% | -40% | 0.750 | 301 | 54.0 | 2.88 | ❌ | 0286ba0f72cf47a54946bc7a10259fc6 |
| 040 | Algo040 | algo_040.py | 22% | -40% | 0.750 | 301 | 54.0 | 2.88 | ❌ | e73c3437531954b7cdcb69e3b801a453 |
| 041 | Algo041 | Mega-7 EW + QQQ 20d annualized vol < 20% gate (tighter). | 35% | -40% | 1.187 | 301 | 53.0 | 6.57 | ✅ | d1ef9659bb1822eb22a62b5c61f03cbd |
| 042 | Algo042 | Mega-7 EW + QQQ 20d annualized vol < 30% gate (looser). | 35% | -40% | 1.187 | 301 | 53.0 | 6.57 | ✅ | 885d768f38c077de98d7dc2e70c555af |
| 043 | Algo043 | Mega-7 fixed cap-weights + QQQ 20d annualized vol < 25% gate. | 29% | -26% | 1.188 | 343 | 61.0 | 4.25 | ✅ | f8b323e6a4d1df9d8394fd71954b2124 |
| 044 | Algo044 | Mega-10 EW + QQQ 20d annualized vol < 25% gate. | 29% | -26% | 1.188 | 343 | 61.0 | 4.25 | ✅ | 0a4565b5a607d064db277249609b2370 |
| 045 | Algo045 | Mega-7 EW + own-basket 20d annualized vol < 30% gate. | 40% | -37% | 1.235 | 852 | 69.0 | 2.15 | ✅ | 5f285dbb6b8916b53588995771314d89 |
| 046 | Algo046 | Mega-7 + QQQ 20d vol < 25% gate + monthly 3mo-momentum weighting. | 40% | -37% | 1.235 | 852 | 69.0 | 2.15 | ✅ | 8d5aa865ab7ec76da65d21c32c3016b4 |
| 047 | Algo047 | Mega-7 + QQQ 20d vol < 25% gate + monthly inverse-vol (risk-parity) weights. | 28% | -25% | 1.133 | 1047 | 79.0 | 1.60 | ✅ | 9619932ac978fa99cb9906734fb27a75 |
| 048 | Algo048 | 5x 3x-leveraged ETF basket EW + QQQ 20d annualized vol < 20% gate (tight). | 28% | -25% | 1.133 | 1047 | 79.0 | 1.60 | ✅ | 0792c9cb2b08cede05239602c3a2dd8a |
| 049 | Algo049 | Mega-7 EW + dual gate: QQQ 20d ann. vol < 25% AND ATR(14)/price < 1.8%. | 28% | -26% | 1.140 | 665 | 59.0 | 3.01 | ✅ | c421daa003da4736f973726f8c99d74d |
| 050 | Algo050 | Mega-7 EW + adaptive vol gate: today's QQQ 20d vol < 1.2 x its 252d median. | 28% | -26% | 1.140 | 665 | 59.0 | 3.01 | ✅ | cc6e54633e84cbc4b97000d827b54b00 |
| 051 | Algo051 | #051 — Mega-7 momo-weighted (1mo) + TQQQ-vol cash gate (vol < 60%). | 24% | -19% | 1.052 | 581 | 56.0 | 2.89 | ❌ | 2591622f0fcfac6a97026ec9a2263475 |
| 052 | Algo052 | #052 — Mega-7 EW + own-basket vol gate (basket vol < 25%). | 24% | -19% | 1.052 | 581 | 56.0 | 2.89 | ❌ | 695f86045c8213fbaf2b94606dbd8bfe |
| 053 | Algo053 | #053 — Mega-7 momo-weighted (3mo) + TQQQ vol-60 + adaptive median gate. | 36% | -34% | 1.138 | 543 | 64.0 | 1.93 | ✅ | 394f3a1733dfbcef0d3d341366d8f16d |
| 054 | Algo054 | #054 — Mega-7 top-3 by 3mo momentum (zero-out bottom 4) + TQQQ vol gate. | 36% | -34% | 1.138 | 543 | 64.0 | 1.93 | ✅ | 818cf2dd44d9d1b1452d2145e56edb1c |
| 055 | Algo055 | #055 — Mega-7 momo-weighted + TQQQ trend (price > 100d SMA on TQQQ). | 15% | -24% | 0.731 | 3831 | 81.0 | 0.67 | ❌ | 01f6942dc413e7113751cbac5685913a |
| 056 | Algo056 | #056 — Top-10 mega-cap from QC fundamental universe + basket-vol gate. | 15% | -24% | 0.731 | 3831 | 81.0 | 0.67 | ❌ | a3f277837525e27aafe2867276419864 |
| 057 | Algo057 | #057 — Mega-7 EW + adaptive 252d vol comparison gate (own basket). | 31% | -21% | 1.109 | 582 | 64.0 | 2.45 | ✅ | 13e9f88e9d582c7ff9a60247ccfa9b1a |
| 058 | Algo058 | #058 — Mega-7 momo-weighted (3mo) + dual TQQQ-vol gate (vol AND ATR escalation). | 31% | -21% | 1.109 | 582 | 64.0 | 2.45 | ✅ | d5efea55bdf0cc7ee62379ec4adfb308 |
| 059 | Algo059 | #059 — Mega-7 momo-weighted (3mo) + TQQQ vol gate + 5-day cooldown. | 32% | -34% | 1.114 | 670 | 61.0 | 2.47 | ✅ | 50d4be62d911cf1cb09e5d3e1892a4ee |
| 060 | Algo060 | algo_060.py | 32% | -34% | 1.114 | 670 | 61.0 | 2.47 | ✅ | 5c855ba4426e61209e15d49ec9adeb65 |
| 061 | Algo061 | #061 — Top-7 mkt-cap momo-weighted (3mo) + TQQQ vol<60% gate. | 17% | -21% | 0.685 | 742 | 60.0 | 1.91 | ❌ | 594cf59b68e079ea2a8c4311c0fdf298 |
| 062 | Algo062 | #062 — Top-10 mkt-cap momo-weighted (3mo) + TQQQ vol<60%. | 17% | -21% | 0.685 | 742 | 60.0 | 1.91 | ❌ | c67a592376a08e209fd9ff340859621b |
| 063 | Algo063 | #063 — Top-5 mkt-cap momo-weighted (3mo) + TQQQ vol<60%. | 18% | -22% | 0.724 | 492 | 63.0 | 1.77 | ❌ | 12faf21349a629555a774e56e2c74c88 |
| 064 | Algo064 | #064 — Top-7 mkt-cap top-3-of-7 by momentum + TQQQ vol gate. | 18% | -22% | 0.724 | 492 | 63.0 | 1.77 | ❌ | 47540779b77d19af179d830d44568068 |
| 065 | Algo065 | #065 — Top-7 mkt-cap momo (3mo) + TQQQ dual vol+ATR gate (replicate #058). | 10% | -16% | 0.436 | 747 | 54.0 | 1.78 | ❌ | 904884c5f962e4365527f58706a03aa3 |
| 066 | Algo066 | #066 — Top-7 momo + TQQQ vol-50% (tighter). | 10% | -16% | 0.436 | 747 | 54.0 | 1.78 | ❌ | 1758c09de57b67f91db7637439a4c258 |
| 067 | Algo067 | #067 — Top-7 cap-weighted (by mkt cap from fundamental data) + TQQQ vol gate. | 15% | -16% | 0.733 | 571 | 55.0 | 2.90 | ❌ | 662080d179887eca77b06406019c0eb9 |
| 068 | Algo068 | #068 — Top-3 mkt-cap concentrated momo + TQQQ vol gate. | 15% | -16% | 0.733 | 571 | 55.0 | 2.90 | ❌ | 58052bb5337b4c6444fb3805b3e457c8 |
| 069 | Algo069 | #069 — Top-7 momo (3mo) + TQQQ vol gate + 80/20 sleeve mix (replicate #060). | 20% | -24% | 0.742 | 883 | 61.0 | 2.01 | ❌ | a31af77d841da688693d55f06156341e |
| 070 | Algo070 | #070 — Top-7 momo (3mo) + TQQQ vol-gate + 5d cooldown (replicate #059). | 16% | -22% | 0.641 | 652 | 61.0 | 1.84 | ❌ | f748d90e7123b17cea2ef7fd05a61b25 |
| 071 | Algo071 | #071 — 50% Top-7 dyn momo basket + 50% TQQQ + TQQQ vol<60% gate. | 24% | -29% | 0.736 | 804 | 61.0 | 2.25 | ❌ | 3029ac5a8aaa157c6bf57b7e0b151dc2 |
| 072 | Algo072 | #072 — 30% Top-7 dyn momo basket + 70% TQQQ + TQQQ vol<60% gate. | 26% | -33% | 0.732 | 696 | 58.0 | 2.77 | ❌ | 57be35dac3a86bd397f6a39cf60e4907 |
| 073 | Algo073 | #073 — 100% TQQQ when vol<35% (very calm), else Top-7 dyn momo (50/50 with TQQQ). | 24% | -33% | 0.694 | 1218 | 58.0 | 1.43 | ❌ | 78127233bfe2809eb5f7e6301638916c |
| 074 | Algo074 | #074 — Top-3 mkt-cap concentrated momo + 50% TQQQ overlay + vol gate. | 24% | -33% | 0.742 | 502 | 66.0 | 1.80 | ❌ | 2566ce6ce223b9bbd5b54444fcf352df |
| 075 | Algo075 | #075 — 100% TQQQ when vol<55%, else 100% top-7 dyn momo basket. | 29% | -49% | 0.735 | 696 | 61.0 | 1.75 | ✅ | e51103826bb62e0cb0f0fe57a742ed7f |
| 076 | Algo076 | algo_076.py | 27% | -37% | 0.712 | 901 | 57.0 | 1.60 | ❌ | d3fc1d3c0e1b8982f4d0ef2bc850f636 |
| 077 | Algo077 | #077 — #075 variant: looser calm (<60% vol) → 100% TQQQ; <85% → basket; else cash. | 33% | -42% | 0.788 | 671 | 57.0 | 2.42 | ✅ | 48c438a5c2d72b679fbc9b6e46acf210 |
| 078 | Algo078 | algo_078.py | 29% | -49% | 0.735 | 696 | 61.0 | 1.75 | ✅ | 60507287e9228a675d04022e5f05e706 |
| 079 | Algo079 | algo_079.py | 34% | -50% | 0.810 | 1368 | 70.0 | 1.38 | ✅ | 082416ce5ac5c142ab767b4b25be1249 |
| 080 | Algo080 | algo_080.py | 25% | -61% | 0.701 | 1067 | 59.0 | 1.38 | ❌ | c019bf8f35970ffff66d22387177739a |
| 081 | Algo081 | #081 — Top-7 dyn momo + TQQQ vol gate using EMA(20) of vol (smoothed). | 16% | -23% | 0.665 | 510 | 69.0 | 1.87 | ❌ | 7af913e75e5362369254019ae0fd8d99 |
| 082 | Algo082 | #082 — TQQQ regime-switch (#075 logic) with weekly rebalance instead of monthly. | 29% | -49% | 0.730 | 916 | 60.0 | 1.72 | ✅ | 2774af3d5f4d7df3af47293cb13fe51e |
| 083 | Algo083 | #083 — TQQQ regime-switch with TQQQ trend confirmation (price > own 50d SMA). | 25% | -41% | 0.670 | 1160 | 61.0 | 1.24 | ❌ | 8e6c549b66f8f26907e378551985be57 |
| 084 | Algo084 | #084 — TQQQ + dyn top-7 inv-vol weighted (basket regime by inverse name vol). | 29% | -44% | 0.735 | 888 | 58.0 | 1.96 | ✅ | 4cfb28e82240882315f62d419c75d46d |
| 085 | Algo085 | #085 — Top-5 dyn (more concentrated) + #075 regime switch. | 32% | -53% | 0.788 | 586 | 57.0 | 2.07 | ✅ | 6ec7320096da1634b5837c9871be3818 |
| 086 | Algo086 | #086 — Top-10 dyn + #075 regime switch (more diversified basket regime). | 25% | -50% | 0.655 | 888 | 57.0 | 1.83 | ❌ | 132221dca9b2202cbfc95f34d8e0d57f |
| 087 | Algo087 | #087 — Regime switch with top-3 momentum stocks (extra concentrated basket). | 29% | -49% | 0.721 | 472 | 61.0 | 1.71 | ✅ | 668cb5ba0a07471c5fe5849c2e1df54a |
| 088 | Algo088 | algo_088.py | 22% | -49% | 0.583 | 1229 | 55.0 | 1.36 | ❌ | 106daa6ab73f9feca4439db86f70b356 |
| 089 | Algo089 | #089 — Regime switch with LONGER vol window (40d). Smoother regime transitions. | 30% | -51% | 0.749 | 465 | 60.0 | 2.32 | ✅ | f3449a87ddd4363837f21fccc51ba78c |
| 090 | Algo090 | #090 — 4-tier vol-graded allocation: TQQQ, TQQQ+basket, basket, cash. | 21% | -39% | 0.600 | 2347 | 53.0 | 1.37 | ❌ | 4ae59d64d255051cce19f2d96db85d19 |
| 091 | Algo091 | #091 — Regime switch with a 3-day vol confirmation. Avoid one-day vol spike whipsaws. | 26% | -45% | 0.651 | 505 | 59.0 | 2.04 | ❌ | 76b306d5f7554cd4c8cac1183dbc4aa6 |
| 092 | Algo092 | #092 — TQQQ regime switch with QUARTERLY (not monthly) basket weight rebalance. | 27% | -50% | 0.697 | 606 | 58.0 | 1.91 | ❌ | d23a51d534d85dbc00759f32aa160c48 |
| 093 | Algo093 | #093 — Regime switch with cap-weighted basket (live mkt-cap weights from fundamentals). | 29% | -45% | 0.745 | 888 | 58.0 | 2.02 | ✅ | c849691a81d06de3ece8808346da87d7 |
| 094 | Algo094 | algo_094.py | 27% | -47% | 0.699 | 1553 | 60.0 | 1.18 | ❌ | 205a4f540839d723e2c5671ceba87630 |
| 095 | Algo095 | #095 — TQQQ regime + top-7 EW basket (no momentum weighting). Simpler basket variant of #075. | 29% | -43% | 0.746 | 885 | 59.0 | 1.94 | ✅ | 23da081296b6b41f78aaea9395ba7bd4 |
| 096 | Algo096 | algo_096.py | 21% | -35% | 0.690 | 689 | 61.0 | 1.61 | ❌ | 38f0cf712d4abf4bd69f97f2e9e54c71 |
| 097 | Algo097 | #097 — Regime switch using BOTH 20d AND 60d vol. Both must agree to flip regime. | 24% | -53% | 0.602 | 260 | 74.0 | 1.36 | ❌ | 977ea939f4d9441a8eb90a32b13c7e78 |
| 098 | Algo098 | algo_098.py | 17% | -66% | 0.495 | 1160 | 55.0 | 1.35 | ❌ | bd344082b54ac1ab2ef55efc3926bf8f |
| 099 | Algo099 | algo_099.py | 32% | -45% | 0.797 | 787 | 58.0 | 1.87 | ✅ | e5c155ad303ace8113bb70875e01272b |
| 100 | Algo100 | algo_100.py | 26% | -34% | 0.697 | 1023 | 58.0 | 1.55 | ❌ | 165352484b841e274897bb4c4d5a725c |

---

## Passing Algos — Details

### 045 — Mega-7 EW + own-basket 20d annualized vol < 30% gate.

**Description:** Equal-weight long across the seven mega-cap leaders (AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA), gated on the basket's own 20-day annualized log-return volatility being below 30%. Each day the algo averages per-name log returns into a synthetic basket series, annualizes its 20-day standard deviation, and toggles fully invested versus fully cash at the threshold. The own-basket vol gate is more responsive than a generic index gate because mega-cap turbulence is captured directly rather than diluted by broader-index components. Its weakness is that a single high-vol day can flip the gate and trigger a full liquidate-rebuild round-trip.

*Overfit 3/10 — equal-weight is parameter-free; the 30% threshold and 20-day window are the only tuned values, both round.*

- **Entry:** Mega-7 basket 20d annualized log-return vol < 30% → equal-weight all 7 names at 1/7 each
- **Exit:** Basket vol >= 30% → liquidate
- **Symbols:** AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 40% | -37% | 1.24 |

> [!code]- Click to view: algo_045.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_045.py"
> ```

---

### 046 — Mega-7 + QQQ 20d vol < 25% gate + monthly 3mo-momentum weighting.

**Description:** Combines the Mega-7 basket with a QQQ 20-day annualized vol gate at 25% and adds monthly momentum-weighting: each month, each name's positive 63-day return becomes its raw weight (negative scores zeroed), normalized to sum to 1. The daily gate keeps it in or out; weights only change once a month or on a gate-on transition. Tilting away from underperformers boosts the contribution of the strongest mega-caps; the cost is single-name concentration when one stock dominates the momentum scoring (e.g., NVDA in 2023).

*Overfit 4/10 — QQQ vol threshold, vol window, and momentum lookback are all tuned; numbers are round but the parameter count is higher than the simpler vol-gate variants.*

- **Entry:** QQQ 20d annualized vol < 25% → apply current monthly momentum weights to Mega-7
- **Exit:** QQQ vol >= 25% → liquidate
- **Rebalance:** Monthly recompute positive-only 3mo momentum weights (normalized to 1)
- **Symbols:** QQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 40% | -37% | 1.24 |

> [!code]- Click to view: algo_046.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_046.py"
> ```

---

### 043 — Mega-7 fixed cap-weights + QQQ 20d annualized vol < 25% gate.

**Description:** Static cap-style weights (AAPL 20%, MSFT 20%, NVDA 15%, GOOGL 15%, AMZN 15%, META 10%, TSLA 5%) held only when QQQ's 20-day annualized vol is below 25%. The hand-picked weights are roughly proportional to early-period market-cap ranking and never adjust over the backtest, so the strategy benefits from broad mega-cap appreciation but does not adapt to leadership changes (e.g., NVDA's surge would not be picked up beyond its 15%). The strict gate keeps it in cash during turbulent periods, which is what gives it the standout -26% MaxDD.

*Overfit 5/10 — seven fixed weights are seven tuned parameters even if they "look like" cap weights; plus the vol threshold and lookback. Risk of look-ahead bias in choosing today-popular names.*

- **Entry:** QQQ 20d annualized vol < 25% → apply fixed cap-style weights
- **Exit:** QQQ vol >= 25% → liquidate
- **Weights:** AAPL 0.20, MSFT 0.20, NVDA 0.15, GOOGL 0.15, AMZN 0.15, META 0.10, TSLA 0.05
- **Symbols:** QQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -26% | 1.19 |

> [!code]- Click to view: algo_043.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_043.py"
> ```

---

### 044 — Mega-10 EW + QQQ 20d annualized vol < 25% gate.

**Description:** Identical mechanism to #041/#042 (QQQ 20d vol gate + equal-weight basket) but with a broader 10-name universe: the Mega-7 plus AVGO, JPM, V. Adding three names from different industry profiles (semiconductors, financials, payments) modestly diversifies the concentration risk versus Mega-7 alone, but the added names don't have the same hyper-growth profile, which compresses CAGR (29% vs 35%) while also pulling MaxDD down (-26% vs -40%).

*Overfit 4/10 — 10 hand-picked tickers plus the 25% vol threshold; AVGO/JPM/V are reasonable mega-cap extensions but the choice over alternatives (UNH/HD/PG) is somewhat arbitrary.*

- **Entry:** QQQ 20d annualized vol < 25% → equal-weight all 10 names at 1/10 each
- **Exit:** QQQ vol >= 25% → liquidate
- **Symbols:** QQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA, AVGO, JPM, V

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -26% | 1.19 |

> [!code]- Click to view: algo_044.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_044.py"
> ```

---

### 041 — Mega-7 EW + QQQ 20d annualized vol < 20% gate (tighter).

**Description:** Equal-weight Mega-7 held only when QQQ's 20-day annualized log-return vol sits below 20% — a tighter threshold than #042's 30%. The tighter gate is in cash more often, which mechanically reduces both upside and drawdown. The CAGR (35%) actually matches #042 because the additional cash periods coincide with the worst drawdown stretches, suggesting the 20% threshold captures most of the meaningful drawdown reduction without sacrificing trend exposure.

*Overfit 3/10 — equal-weight basket is parameter-free; the 20% vol threshold and 20-day window are tuned but both are round values.*

- **Entry:** QQQ 20d annualized vol < 20% → equal-weight Mega-7 at 1/7 each
- **Exit:** QQQ vol >= 20% → liquidate
- **Symbols:** QQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 35% | -40% | 1.19 |

> [!code]- Click to view: algo_041.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_041.py"
> ```

---

### 042 — Mega-7 EW + QQQ 20d annualized vol < 30% gate (looser).

**Description:** Same logic as #041 but with a looser 30% vol threshold, leaving the strategy invested more of the time. With identical CAGR (35%) and MaxDD (-40%) to #041, the looser threshold doesn't cost — meaning that between 20% and 30% vol, mega-caps tend to perform well enough on average to justify exposure. The pair of near-identical results is suspicious: it strongly suggests QQQ's 20d vol rarely sits in the 20-30% band on this dataset, so #041 and #042 are nearly the same strategy in practice.

*Overfit 3/10 — same parameter count as #041; the 30% number is round but the near-identical results to #041 should make one cautious about claiming meaningful threshold selection here.*

- **Entry:** QQQ 20d annualized vol < 30% → equal-weight Mega-7 at 1/7 each
- **Exit:** QQQ vol >= 30% → liquidate
- **Symbols:** QQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 35% | -40% | 1.19 |

> [!code]- Click to view: algo_042.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_042.py"
> ```

---

### 049 — Mega-7 EW + dual gate: QQQ 20d ann. vol < 25% AND ATR(14)/price < 1.8%.

**Description:** Mega-7 equal-weight conditioned on two simultaneous gates: QQQ 20-day annualized vol below 25% AND the QQQ ATR(14)/price ratio below 1.8%. The dual gate is more conservative than either alone: short-term vol can be calm while daily ranges are wide and vice versa, so requiring both filters captures only truly placid markets. The result is materially lower MaxDD (-26%) with a small CAGR penalty (28%) versus single-gate variants.

*Overfit 5/10 — two tuned thresholds (25% vol, 1.8% ATR/price), two indicator periods (20d vol, 14d ATR). Vulnerable to small parameter shifts.*

- **Entry:** QQQ 20d annualized vol < 25% AND ATR(14)/QQQ price < 0.018 → EW Mega-7
- **Exit:** Either condition fails → liquidate
- **Symbols:** QQQ (signals), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 28% | -26% | 1.14 |

> [!code]- Click to view: algo_049.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_049.py"
> ```

---

### 050 — Mega-7 EW + adaptive vol gate: today's QQQ 20d vol < 1.2 x its 252d median.

**Description:** Instead of a fixed threshold, the gate is adaptive: today's QQQ 20-day vol must be below 1.2× the trailing 252-day median of 20-day vols. The strategy is in market when current vol is only modestly elevated relative to its own one-year regime. In structurally low-vol years the gate is tight; in higher-vol years it widens automatically. Equal-weight Mega-7 when gate is on; cash when off. This adaptive design reduces sensitivity to absolute vol regimes versus fixed-threshold #041–#044.

*Overfit 3/10 — only one tuned scalar (1.2× multiplier); window lengths (20d, 252d) and the median operator are standard.*

- **Entry:** today's QQQ 20d vol < 1.2 × trailing 252d median of 20d vols → EW Mega-7
- **Exit:** Vol exceeds 1.2× median → liquidate
- **Symbols:** QQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 28% | -26% | 1.14 |

> [!code]- Click to view: algo_050.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_050.py"
> ```

---

### 053 — Mega-7 momo-weighted (3mo) + TQQQ vol-60 + adaptive median gate.

**Description:** Mega-7 with monthly 3-month momentum weights, but the regime gate is on TQQQ's 21-day annualized vol with a two-stage rule: while the 252-day rolling window is still warming up, use a fixed 60% threshold; once full, switch to the adaptive 1.2× median rule. Gate-on applies the momentum weights; gate-off liquidates. Combines the momentum tilt of #046 with TQQQ-based regime sensing, which reacts earlier than QQQ-based gates because TQQQ's 3× leverage amplifies daily moves.

*Overfit 5/10 — momentum window, fixed and adaptive thresholds, and an extra warmup-bridge mechanism. Some parameters are interdependent.*

- **Entry:** TQQQ vol gate on (fixed v<60% during warmup, adaptive v<1.2×median otherwise) → apply monthly momentum weights to Mega-7
- **Exit:** Gate fails → liquidate
- **Rebalance:** Monthly recompute positive-only 3mo momentum weights
- **Symbols:** TQQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 36% | -34% | 1.14 |

> [!code]- Click to view: algo_053.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_053.py"
> ```

---

### 054 — Mega-7 top-3 by 3mo momentum (zero-out bottom 4) + TQQQ vol gate.

**Description:** Concentrates the basket on only the top 3 mega-cap names by 3-month return each month, weighted by positive momentum. The bottom 4 are dropped entirely. Combined with a TQQQ 21d vol < 60% gate. Much more concentrated than #053, so single-stock dispersion drives results. The identical headline stats to #053 (36% / -34% / 1.14) suggest the top-3 vs full-7 difference is small in this period because the bottom 4 rarely have positive momentum that would have meaningfully diluted the top names.

*Overfit 6/10 — top-3 selection adds explicit ranking; vol threshold and momentum lookback complete the parameter set. Concentration risk in any one period.*

- **Entry:** TQQQ 21d annualized vol < 60% → top-3 Mega-7 by 3mo return, weighted by positive momentum
- **Exit:** Vol gate fails → liquidate; monthly drops names no longer in top-3
- **Symbols:** TQQQ (signal), Mega-7 (rotating top-3)

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 36% | -34% | 1.14 |

> [!code]- Click to view: algo_054.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_054.py"
> ```

---

### 047 — Mega-7 + QQQ 20d vol < 25% gate + monthly inverse-vol (risk-parity) weights.

**Description:** QQQ 20d vol gate at 25%, but instead of equal-weight or momentum-weight, the Mega-7 are weighted by inverse 60-day return volatility (risk parity). Less-volatile names like AAPL/MSFT get higher weight than NVDA/TSLA. Combined with the calm-vol regime filter, the portfolio sees relatively smooth equity contribution from each name. The CAGR (28%) is lower than EW variants because high-vol winners are under-weighted, but MaxDD (-25%) is the best of the vol-gate family.

*Overfit 4/10 — vol threshold + lookback + inverse-vol window. The inverse-vol scheme is principled but the 60d window is a tuned choice.*

- **Entry:** QQQ 20d annualized vol < 25% → apply inverse-vol weights to Mega-7
- **Exit:** Vol gate fails → liquidate
- **Rebalance:** Monthly inverse-vol weights from 60d std of daily log returns
- **Symbols:** QQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 28% | -25% | 1.13 |

> [!code]- Click to view: algo_047.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_047.py"
> ```

---

### 048 — 5x 3x-leveraged ETF basket EW + QQQ 20d annualized vol < 20% gate (tight).

**Description:** Equal-weight basket of five 3× leveraged sector ETFs (TQQQ, TECL, SOXL, UPRO, FAS) at 20% each — totals to 100% notional, no margin — conditioned on the tightest 20% QQQ vol gate. The tight gate is essential: 3× leveraged ETFs experience devastating decay in high-vol environments. By restricting exposure to truly calm markets, the strategy captures leveraged trend without the typical 3× ETF drawdown profile. The basket is less diversified than it looks — TQQQ, TECL, and SOXL all overlap heavily with Nasdaq.

*Overfit 4/10 — five hand-picked 3× ETFs plus the tight vol threshold. The 20% gate is essential to making 3× ETFs viable, so this tuning has a clear theoretical basis.*

- **Entry:** QQQ 20d annualized vol < 20% → 20% each in TQQQ, TECL, SOXL, UPRO, FAS
- **Exit:** Vol gate fails → liquidate
- **Symbols:** QQQ (signal), TQQQ, TECL, SOXL, UPRO, FAS

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 28% | -25% | 1.13 |

> [!code]- Click to view: algo_048.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_048.py"
> ```

---

### 059 — Mega-7 momo-weighted (3mo) + TQQQ vol gate + 5-day cooldown.

**Description:** Same backbone as #053 (TQQQ 21d vol < 60% gate + monthly 3mo-momentum weights on Mega-7) with a 5-day cooldown after gate-off. The cooldown prevents fast on/off whipsaws around the threshold by forcing a waiting period before re-entry. The CAGR drop from #053's 36% to 32% reflects the cost of missing fast bounces; the -34% MaxDD is unchanged, suggesting the cooldown only modestly improves drawdowns on this dataset.

*Overfit 6/10 — momentum lookback, vol threshold, and an additional cooldown integer. Each parameter is small but they multiply combinatorially.*

- **Entry:** TQQQ 21d annualized vol < 60% AND cooldown == 0 → apply monthly momentum weights
- **Exit:** Vol gate fails → liquidate AND start 5-day cooldown
- **Symbols:** TQQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 32% | -34% | 1.11 |

> [!code]- Click to view: algo_059.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_059.py"
> ```

---

### 060 — Mega-7 momo (80%) + TQQQ (20%) sleeve, TQQQ vol-60% gate.

**Description:** A sleeve mix of 80% momentum-weighted Mega-7 + 20% TQQQ when TQQQ 21d annualized vol is below 60%; full cash above. The 20% TQQQ sleeve adds a leveraged-Nasdaq kicker on top of the momentum-weighted single-name exposure. The 5%-rebalance threshold (3% for the sleeve) controls trade frequency. Identical CAGR / MaxDD / Sharpe to #059 (32% / -34% / 1.11) suggesting the TQQQ kicker and the #059 cooldown are roughly equivalent risk-adjustments at this calibration.

*Overfit 5/10 — sleeve weights (80/20), vol threshold, momentum lookback. The 80/20 split is a tuned allocation pair.*

- **Entry:** TQQQ 21d annualized vol < 60% → 80% Mega-7 (momo-weighted) + 20% TQQQ
- **Exit:** Vol gate fails → liquidate everything
- **Rebalance:** Monthly momentum reweighting of the 80% sleeve
- **Symbols:** TQQQ, AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 32% | -34% | 1.11 |

> [!code]- Click to view: algo_060.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_060.py"
> ```

---

### 057 — Mega-7 EW + adaptive 252d vol comparison gate (own basket).

**Description:** Equal-weight Mega-7, gated on a single comparison: today's 20-day basket vol versus the basket's own 252-day vol. In-market when 20d vol < 252d vol — i.e., the recent regime is calmer than the trailing year average. No tuned threshold at all — the comparison **is** the threshold. This makes the strategy maximally adaptive to changing volatility regimes. Lowest MaxDD in the Mega-7 EW family (-21%).

*Overfit 2/10 — zero numerical thresholds beyond the window lengths (20d, 252d), both standard. The cleanest tuning footprint of any algo in this set.*

- **Entry:** Mega-7 basket 20d annualized vol < basket 252d annualized vol → EW Mega-7
- **Exit:** 20d vol >= 252d vol → liquidate
- **Symbols:** AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 31% | -21% | 1.11 |

> [!code]- Click to view: algo_057.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_057.py"
> ```

---

### 058 — Mega-7 momo-weighted (3mo) + dual TQQQ-vol gate (vol AND ATR escalation).

**Description:** Hysteretic two-condition gate: hard exit when TQQQ 21d vol >= 60% OR TQQQ ATR(14)/price > 6%; re-enter only when vol < 60% AND ATR(14)/price < 4.5%. The asymmetric thresholds (4.5% re-entry vs 6% exit) create a Schmitt-trigger-style buffer that prevents rapid on/off cycling. Monthly momentum-weighted rebalance while in market. Identical headline result to #057 (31% / -21% / 1.11) but achieved with very different machinery.

*Overfit 7/10 — vol threshold (0.60), two ATR thresholds (0.06, 0.045), ATR period (14), momentum lookback. The asymmetric exit/re-entry pair is two extra fitted scalars.*

- **Entry (from cash):** TQQQ 21d vol < 60% AND ATR(14)/price < 4.5% → apply monthly momentum weights
- **Exit (from market):** TQQQ 21d vol >= 60% OR ATR(14)/price > 6% → liquidate
- **Symbols:** TQQQ (signal), AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 31% | -21% | 1.11 |

> [!code]- Click to view: algo_058.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_058.py"
> ```

---

### 079 — TQQQ size scales linearly by inverse vol; rest in dyn top-7 EW.

**Description:** Continuous sizing rather than binary regime switch: TQQQ weight scales linearly from 1.0 (at TQQQ 21d vol = 40%) to 0.0 (at vol = 80%), with the remaining weight equal-weighted across a dynamic top-7 mega-cap basket selected by fundamental market cap. As vol rises, the algo gradually shifts from leveraged-Nasdaq to single-name equity. The smooth allocation curve avoids the all-or-nothing exits of regime strategies but trades constantly when vol oscillates near the band edges.

*Overfit 4/10 — two anchor points (vol=0.40 → 100% TQQQ, vol=0.80 → 0%) and a top-N=7. Linear interpolation between fitted endpoints is more tunable than it looks.*

- **Entry:** Always invested; `tqqq_w = clip((0.80 - vol) / 0.40, 0, 1)`; remainder split equal-weight across dynamic top-7
- **Exit:** No flat-cash state; only weight adjustments
- **Rebalance:** Triggered when target TQQQ weight changes by > 5%
- **Symbols:** TQQQ + dynamic top-7 mega-caps from QC Fundamentals

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 34% | -50% | 0.81 |

> [!code]- Click to view: algo_079.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_079.py"
> ```

---

### 099 — TQQQ + dyn top-7 momo with HARD daily exit on -8% TQQQ drop.

**Description:** Standard #075-style 3-regime switch (TQQQ when vol<55%, dyn top-7 momo basket when 55-85%, cash when >=85%) augmented by a hard tail-risk exit: any day TQQQ closes down ≥ 8% from the prior close, liquidate everything and skip the next day (1-day cooldown). The hard stop is intended to prevent catastrophic single-day losses on TQQQ. In practice, -8% TQQQ days are rare enough that the overlay mainly contributes during March 2020 and October 2022.

*Overfit 6/10 — adds two parameters (-8% threshold, 1-day cooldown) on top of the regime triple. The -8% TQQQ threshold is uncomfortably specific.*

- **Entry:** Regime switch as in #075 (TQQQ when vol<55%, momo top-7 basket when 55-85%)
- **Exit (tail):** TQQQ daily return <= -8% → liquidate + skip next day
- **Exit (regime):** Vol crosses 85% → liquidate to cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 32% | -45% | 0.80 |

> [!code]- Click to view: algo_099.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_099.py"
> ```

---

### 077 — #075 variant: looser calm (<60% vol) → 100% TQQQ; <85% → basket; else cash.

**Description:** A looser-calm variant of #075: the threshold to go all-in TQQQ is raised from 55% to 60%, giving TQQQ exposure in more market conditions. The middle "basket" band shrinks accordingly. Result: higher CAGR (33% vs 29%) with somewhat worse MaxDD (-42% vs -49%) — broadly the same risk-reward shape, just shifted along the curve toward more aggression.

*Overfit 5/10 — three threshold values (60%/85%/momentum lookback) with the looser calm an explicit move from #075's 55%.*

- **Entry (TQQQ):** TQQQ 21d vol < 60% → 100% TQQQ
- **Entry (basket):** 60% <= vol < 85% → momentum-weighted top-7 dyn basket
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 33% | -42% | 0.79 |

> [!code]- Click to view: algo_077.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_077.py"
> ```

---

### 085 — Top-5 dyn (more concentrated) + #075 regime switch.

**Description:** Same regime triple as #075 (vol<55% → TQQQ; <85% → momo basket; else cash) but the basket is concentrated to the top 5 dynamic mega-caps instead of 7. Higher concentration lifts CAGR (32% vs 29%) because of stronger single-name contribution, at the cost of worse MaxDD (-53% vs -49%) since dispersion within the basket has fewer offsets.

*Overfit 5/10 — same regime parameters as #075 plus TOP_N=5 vs 7 — a small but explicit additional choice.*

- **Entry (TQQQ):** TQQQ 21d vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → momentum-weighted top-5 dyn mega-cap basket
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-5 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 32% | -53% | 0.79 |

> [!code]- Click to view: algo_085.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_085.py"
> ```

---

### 089 — Regime switch with LONGER vol window (40d). Smoother regime transitions.

**Description:** #075 regime switch but using a 40-day vol window instead of the standard 21-day. The longer window smooths regime transitions, reducing false flips during temporary spikes. Same thresholds (55%/85%) and basket logic. Smoother transitions give a marginally better CAGR (30%) but also slightly worse MaxDD (-51%) because the algo is slower to exit when vol genuinely escalates.

*Overfit 4/10 — the only difference from #075 is the vol window length; everything else equal. Window length is a tuned parameter but the magnitude of change is mild.*

- **Entry (TQQQ):** TQQQ 40d annualized vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → momentum-weighted top-7 dyn basket
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 30% | -51% | 0.75 |

> [!code]- Click to view: algo_089.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_089.py"
> ```

---

### 095 — TQQQ regime + top-7 EW basket (no momentum weighting). Simpler basket variant of #075.

**Description:** Same vol-regime switch as #075 but the basket is purely equal-weighted across the top-7 dynamic mega-caps — no momentum tilt. Simpler and more robust: removes one tuning surface (the 63-day momentum lookback). CAGR matches #075 (29%) and MaxDD is mildly better (-43% vs -49%), suggesting the momentum weighting in #075 isn't adding much beyond EW on this dataset.

*Overfit 3/10 — pure regime switch + EW basket. Lowest parameter count of the regime-switch family.*

- **Entry (TQQQ):** TQQQ 21d vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → EW top-7 dyn mega-cap basket (1/7 each)
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -43% | 0.75 |

> [!code]- Click to view: algo_095.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_095.py"
> ```

---

### 093 — Regime switch with cap-weighted basket (live mkt-cap weights from fundamentals).

**Description:** #075 regime triple with the basket weights determined by live market capitalization from QC fundamentals (each name weighted by its proportion of total basket market cap). More principled than fixed cap-style weights (#043) because weights update as cap ranking evolves over time. Same calm-vol → TQQQ logic.

*Overfit 3/10 — basket weights are derived from fundamentals (not fitted); only the regime thresholds and TOP_N are tuned.*

- **Entry (TQQQ):** TQQQ 21d vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → cap-weighted top-7 dyn mega-cap basket
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -45% | 0.74 |

> [!code]- Click to view: algo_093.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_093.py"
> ```

---

### 075 — 100% TQQQ when vol<55%, else 100% top-7 dyn momo basket.

**Description:** The progenitor of the regime-switch family in this sweep. Three regimes by TQQQ 21-day annualized vol: <55% → 100% TQQQ (leveraged); 55-85% → momentum-weighted top-7 dynamic mega-cap basket; >=85% → 100% cash. The dynamic universe (selected by fundamental market cap each pass) gives the basket survivorship resistance — it always holds today's leaders, not a fixed list. The core bet is that 3× leverage works when realized vol is low; switching to single-name equity preserves capital in choppier regimes; full cash protects in panic.

*Overfit 5/10 — two vol thresholds (55%, 85%), momentum lookback (63d), TOP_N=7. The triple-state design adds combinatorial parameter interactions, but the core thresholds are intuitive.*

- **Entry (TQQQ):** TQQQ 21d vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → momentum-weighted top-7 dyn mega-cap basket
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -49% | 0.73 |

> [!code]- Click to view: algo_075.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_075.py"
> ```

---

### 078 — momentum-weighted basket version of #075.

**Description:** Functionally equivalent to #075 — same thresholds (55%/85%), same top-7 dynamic universe, same monthly momentum-weighted basket. The result is identical (29% / -49% / 0.73) because the parameters are the same. The two files appear to be near-duplicates kept as separate IDs for record-keeping.

*Overfit 5/10 — same parameter footprint as #075; no meaningful difference in tuning surface.*

- **Entry (TQQQ):** TQQQ 21d vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → momentum-weighted top-7 dyn mega-cap basket
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -49% | 0.73 |

> [!code]- Click to view: algo_078.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_078.py"
> ```

---

### 084 — TQQQ + dyn top-7 inv-vol weighted (basket regime by inverse name vol).

**Description:** Regime switch as in #075, but in the basket band each name is weighted by its inverse 60-day daily-return vol (risk parity within the basket). Lower-vol names like MSFT/AAPL get more weight than higher-vol like NVDA/TSLA. Same CAGR as #075 (29%) with a small MaxDD improvement (-44% vs -49%), reflecting the more defensive in-basket weighting.

*Overfit 4/10 — same regime parameters as #075 plus the 60d inv-vol window. The inverse-vol weighting is principled and reduces tuning compared to explicit momentum weights.*

- **Entry (TQQQ):** TQQQ 21d vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → inverse-vol-weighted top-7 dyn basket (60d window)
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -44% | 0.73 |

> [!code]- Click to view: algo_084.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_084.py"
> ```

---

### 082 — TQQQ regime-switch (#075 logic) with weekly rebalance instead of monthly.

**Description:** #075 regime triple but the in-basket momentum-weight recomputation happens every ISO week instead of every month. Faster rebalancing tracks momentum shifts more responsively but increases turnover and transaction-cost drag. Result is statistically identical to #075 (29% / -49% / 0.73) — on this dataset, the extra rebalances don't materially change outcomes, suggesting weekly momentum scores are highly autocorrelated.

*Overfit 5/10 — same parameters as #075 plus a weekly cadence (vs monthly). Cadence is itself a fitted choice.*

- **Entry (TQQQ):** TQQQ 21d vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → momentum-weighted top-7 basket, **weekly rebalance**
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-7 mega-caps

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -49% | 0.73 |

> [!code]- Click to view: algo_082.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_082.py"
> ```

---

### 087 — Regime switch with top-3 momentum stocks (extra concentrated basket).

**Description:** Same regime triple as #075 but the basket is the top 3 of 7 by 3-month return, weighted by positive momentum (zero out the others). Extremely concentrated. CAGR matches #075 (29%) at slightly worse Sharpe (0.72 vs 0.73) — the extra concentration adds dispersion without a corresponding return premium on this period, since the largest mega-caps tend to co-move during basket regimes.

*Overfit 6/10 — #075 parameters plus an explicit top-3-of-7 selection. Highly sensitive to single-name dispersion in basket periods.*

- **Entry (TQQQ):** TQQQ 21d vol < 55% → 100% TQQQ
- **Entry (basket):** 55% <= vol < 85% → top-3 of dyn top-7 by 3mo momentum, weighted by positive momentum
- **Exit:** vol >= 85% → cash
- **Symbols:** TQQQ + dynamic top-3 (selected from top-7 mega-caps)

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -49% | 0.72 |

> [!code]- Click to view: algo_087.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_087.py"
> ```

---
