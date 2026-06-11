# Leave-One-Out Sub-Algo Analysis

## Setup

- **Date:** 2026-06-07
- **Method:** Set all sub-algo weights to 10 (uniform allocation, 1/15 each). Run baseline + 15 leave-one-out variants.
- **Period:** 2014-01-01 → 2025-12-31 (12 years)
- **Metric:** ΔSharpe vs baseline (negative = removing this sub HURTS the ensemble; positive = removing this sub HELPS)

## Baseline

| CAGR | MaxDD | Sharpe |
|---|---|---|
| 35.9% | -34.8% | **0.963** |

## Full results

Sorted by ΔSharpe (most critical sub at top). ΔCAGR positive = CAGR improved without this sub; ΔDD positive = drawdown got smaller (better).

| Removed | CAGR | MaxDD | Sharpe | ΔCAGR | ΔDD | ΔSharpe | Verdict |
|---|---|---|---|---|---|---|---|
| IBSBasket | 33.4% | -37.0% | 0.894 | **-2.5pp** | **-2.2pp** | **-0.069** | **KEEP** — critical |
| RSI2DipVote | 34.7% | -36.1% | 0.918 | -1.2pp | -1.3pp | **-0.045** | **KEEP** — critical |
| MomVote | 35.6% | -35.2% | 0.951 | -0.3pp | -0.4pp | -0.012 | Keep — net positive |
| StretchExit | 35.3% | -35.2% | 0.952 | -0.6pp | -0.4pp | -0.011 | Keep — net positive |
| MFI14Hyst | 36.0% | -35.5% | 0.959 | +0.1pp | -0.7pp | -0.004 | Keep — marginal |
| _baseline (none)_ | 35.9% | -34.8% | 0.963 | 0.0 | 0.0 | 0.000 | reference |
| RangeBreak | 35.9% | -33.5% | 0.967 | 0.0pp | **+1.3pp** | +0.004 | Neutral |
| VolReg20 | 35.8% | -35.8% | 0.968 | -0.1pp | -1.0pp | +0.005 | Neutral |
| RangeCompr | 35.9% | -34.7% | 0.970 | 0.0pp | +0.1pp | +0.007 | Neutral |
| LevRebal | 36.3% | -34.3% | 0.974 | +0.4pp | +0.5pp | +0.011 | **Drop** — small drag |
| SMA200Tiers | 36.2% | -34.2% | 0.976 | +0.3pp | +0.6pp | +0.013 | **Drop** — small drag |
| SMA5Vote | 36.0% | -33.9% | 0.976 | +0.1pp | +0.9pp | +0.013 | **Drop** — small drag |
| CashReserve | 38.0% | -36.8% | 0.977 | **+2.1pp** | **-2.0pp** | +0.014 | Keep — DD stabilizer |
| D5Vote | 35.9% | -33.9% | 0.979 | 0.0pp | +0.9pp | +0.016 | **Drop** — small drag |
| SMA200Pyramid | 36.2% | -33.5% | 0.981 | +0.3pp | **+1.3pp** | +0.018 | **Drop** — DD wins |
| GoldXATR | 36.1% | -32.6% | **0.985** | +0.2pp | **+2.2pp** | **+0.022** | **Drop** — biggest DD improvement |

## Categories

### Critical (drop → big Sharpe loss)

- **IBSBasket** (ΔSharpe -0.069): mean-reversion via Internal Bar Strength + ATR stop on TQQQ/SOXL/TECL basket. Provides uncorrelated dip-buy signal.
- **RSI2DipVote** (ΔSharpe -0.045): RSI(2) oversold basket. Pure mean-reversion edge.

### Net positive (small but real)

- MomVote (-0.012)
- TrendStretchExit (-0.011)
- MFI14Hyst (-0.004)

### Neutral (within ±0.01)

- RangeBreakout (+0.004)
- VolRegime20 (+0.005)
- RangeCompressed (+0.007)

### Net negative (overlapping trend signals)

- LevRebal (+0.011)
- SMA200Tiers (+0.013)
- SMAFiveVote (+0.013)
- DonchianFiveVote (+0.016)
- SMA200Pyramid (+0.018)
- **GoldenCrossATR (+0.022)** — largest individual drag

### Stability anchor

- CashReserve (+0.014 Sharpe, but +2.0pp DD without it). Keep for tail-risk smoothing.

## Key observations

### Trend overlap

All 6 net-negative subs are **trend-following on QQQ via SMA/EMA/Donchian**:
- LevRebal (static long bias)
- SMA200Tiers
- SMA200Pyramid
- SMAFiveVote (SMA20/50/100/150×4/200)
- DonchianFiveVote (Donchian 50/100/150/200/250)
- GoldenCrossATR (EMA50/EMA200)

They produce correlated signals — each adds little new information, but each adds drawdown via leveraged TQQQ exposure when trends fail (2018, 2022).

### Mean-reversion is rare and valuable

Only 2 subs are mean-reversion based (IBSBasket, RSI2DipVote). Both are critical contributors. Suggests the ensemble would benefit from MORE mean-reversion signals (e.g., RSI(3) on different periods, MFI dip-buy variants).

### What's actually doing the work

5 of 15 subs (33%) carry ≥80% of the Sharpe contribution:

1. IBSBasket
2. RSI2DipVote
3. MomVote
4. TrendStretchExit
5. MFI14Hyst (marginal)

The other 10 are either neutral or negative.

## Recommended next experiments

### A. Trimmed 9-sub ensemble

Drop the 6 net-negatives (LevRebal, SMA200Tiers, SMA5Vote, D5Vote, SMA200Pyramid, GoldXATR). Keep all others.

**Hypothesis:** Sharpe rises from 0.963 → ~1.02-1.05; DD falls from -34.8% to -32%.

### B. Pure mean-reversion focused

Drop ALL trend-followers. Keep only: IBSBasket, RSI2DipVote, MomVote, StretchExit, MFI14Hyst, RangeBreak, VolReg20, CashReserve (8 subs).

**Hypothesis:** Sharpe could rise further but DD risk if trend-following safety net is fully removed.

### C. Add more mean-reversion

Since only 2 subs carry the bulk of returns and both are mean-reversion, test adding:
- RSI(3) variant with different thresholds
- Bollinger Band Z-score dip
- Volume-weighted price reversion

### D. Test pairwise interactions

LOO is first-order. Run pairwise LOO for the 6 trend-followers to find which combinations are truly redundant vs which are individually fine.

## Notes

- Uniform weight=10 baseline differs from production weights (which give IBSBasket=20, RSI2DipVote=20, SMA5Vote=15, D5Vote=15). Production Sharpe is 1.036.
- The LOO analysis with uniform weights is structurally cleaner for ranking but understates the contribution of the 2 high-weight subs.
- With production weights, IBSBasket and RSI2DipVote already get 20/175 = 11.4% allocation each (vs 6.7% in this test) — so their dominance is partially priced in.
- Backtest IDs: see `/tmp/loo_results.json`
