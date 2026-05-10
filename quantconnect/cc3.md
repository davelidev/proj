# Sweep 3 — 200 Diverse Daily Strategies

**Target:** CAGR ≥ 28% AND |MaxDD| ≤ 58%
**Date range:** 2014-01-01 → 2025-12-31
**Cash:** $100,000
**Resolution:** Daily only

## 🏆 Leaderboard (top 10 passers by Sharpe)

**Batch 1 Status:** Generated, validation ✅, QC submission pending (cluster at capacity)

| Rank | # | Name | CAGR | MaxDD | Sharpe | Pass |
| :--- | :- | :--- | :--- | :---- | :----- | :--- |
| — | — | Awaiting batch 1 results... | — | — | — | — |

## Results

### Batch 1 (Strategies 001–010): Davey-Adapted Entries + Momentum/Vol Gates

Each strategy targets the dynamic top-10 mega-cap basket via AddUniverse by market cap.

| #   | Name | Signal Type | Universe | CAGR | MaxDD | Sharpe | Pass | Backtest ID |
| :-- | :--- | :---------- | :------- | :--- | :---- | :----- | :--- | :---------- |
| 001 | Algo001 | RSI(5) < 30 + vol gate | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 002 | Algo002 | Stochastic %K < 30 / > 70 | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 003 | Algo003 | ATR-breakout (20d ± 1.5×ATR) | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 004 | Algo004 | 3-bar inside-outside + momentum | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 005 | Algo005 | SMA(5) cross SMA(20) | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 006 | Algo006 | Range contraction + breakout | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 007 | Algo007 | Day-of-week + 21d momentum | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 008 | Algo008 | CCI(14) > 100 / < -100 | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 009 | Algo009 | Bollinger Band lower touch | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 010 | Algo010 | Percentile mean-reversion | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |

### Batch 2 (Strategies 011–020): Davey-Adapted Entries + Distinct Signals

Each strategy targets the dynamic top-10 mega-cap basket via AddUniverse by market cap.

| #   | Name | Signal Type | Universe | CAGR | MaxDD | Sharpe | Pass | Backtest ID |
| :-- | :--- | :---------- | :------- | :--- | :---- | :----- | :--- | :---------- |
| 011 | Algo011 | Highest close (10d) breakout + 5d momentum gate | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 012 | Algo012 | ADX(14) > 25 triggers 5d high breakout | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 013 | Algo013 | MACD (12,26,9) crossover | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 014 | Algo014 | Keltner Channel (20, 1.5×ATR) breakout | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 015 | Algo015 | Williams %R(-14) extremes | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 016 | Algo016 | Close > open + volume surge (1.2×) | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 017 | Algo017 | Pullback pattern + SMA(20) bounce | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 018 | Algo018 | Highest high (21d) breakout at ADX > 30 | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 019 | Algo019 | RSI(14) divergence detector | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 020 | Algo020 | Volume-weighted momentum (1.2× + 5d return) | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |

### Batch 3 (Strategies 021–030): Davey-Adapted Entries + Final Mega-Cap Signals

Each strategy targets the dynamic top-10 mega-cap basket via AddUniverse by market cap.

| #   | Name | Signal Type | Universe | CAGR | MaxDD | Sharpe | Pass | Backtest ID |
| :-- | :--- | :---------- | :------- | :--- | :---- | :----- | :--- | :---------- |
| 021 | Algo021-Envelope | Envelope breakout: price > SMA(20) ± 10% + volume surge | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 022 | Algo022-ConsClosures | 3+ consecutive closes > SMA(50) = strong uptrend signal | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 023 | Algo023-SupRes | Close > prev 21d high (long) / < 21d low (short) | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 024 | Algo024-IntraBar | (close-open) > 2×(high-low) = bullish continuation | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 025 | Algo025-MFO | Money Flow Index extremes (< 30 oversold, > 70 overbought) | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 026 | Algo026-ROC | ROC(5d) threshold: > 5% long, < -5% short | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 027 | Algo027-BollingerB | Bollinger %B (20,2): < 0 oversold, > 1 overbought | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 028 | Algo028-Reversal | 2-bar reversal after new 10d high (contrarian short) | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 029 | Algo029-Trendline | Higher highs AND higher lows trendline detection → long | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |
| 030 | Algo030-LinReg | Linear regression slope (20d): slope > 0 long, < 0 short | Mega-cap top-10 | _pending_ | _pending_ | _pending_ | — | — |

**Status:** ✅ Generation complete, ⏳ Pending QC submission (cluster at capacity)

_Results will be appended as submissions complete._
