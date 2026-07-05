# Leave-One-Out Sub-Algo Analysis

## Setup

- **Date:** 2026-07-04
- **Method:** All sub-algo weights at 10 (uniform, 1/13 each). Run baseline + 13 leave-one-out variants.
- **Period:** 2014-01-01 → 2025-12-31 (12 years)
- **Metric:** ΔSharpe vs baseline (negative = removing this sub HURTS the ensemble; positive = removing this sub HELPS)

## Baseline

| CAGR | MaxDD | Sharpe |
|---|---|---|
| 38% | -34% | **0.977** |

## Full results

Sorted by ΔSharpe (most critical sub at top). ΔCAGR positive = CAGR improved without this sub; ΔDD positive = drawdown got smaller (better).

| Removed | CAGR | MaxDD | Sharpe | ΔCAGR | ΔDD | ΔSharpe | Verdict |
|---|---|---|---|---|---|---|---|
| RSI2DipVote | 38% | -38% | 0.940 | 0pp | -4pp | **-0.037** | **KEEP** — most critical |
| IBSBasket | 38% | -38% | 0.955 | 0pp | -4pp | **-0.022** | **KEEP** — critical |
| StretchExit | 38% | -36% | 0.961 | 0pp | -2pp | -0.016 | **KEEP** — critical |
| MomVote | 38% | -36% | 0.962 | 0pp | -2pp | -0.015 | **KEEP** — critical |
| MFI14Hyst | 38% | -35% | 0.965 | 0pp | -1pp | -0.012 | Keep — net positive |
| _baseline (none)_ | 38% | -34% | 0.977 | 0.0 | 0.0 | 0.000 | reference |
| GoldXATR | 38% | -34% | 0.980 | 0pp | 0pp | +0.003 | Neutral |
| SMA200Tiers | 39% | -35% | 0.982 | +1pp | -1pp | +0.005 | Neutral |
| VolReg20 | 39% | -36% | 0.985 | +1pp | -2pp | +0.008 | Neutral |
| SMA5Vote | 39% | -34% | 0.986 | +1pp | 0pp | +0.009 | Neutral |
| LevRebal | 38% | -32% | 0.987 | 0pp | **+2pp** | +0.010 | Neutral |
| RangeCompr | 39% | -34% | 0.988 | +1pp | 0pp | +0.011 | **Drop** — small drag |
| D5Vote | 39% | -34% | 0.991 | +1pp | 0pp | +0.014 | **Drop** — small drag |
| SMA200Pyramid | 39% | -34% | 0.993 | +1pp | 0pp | **+0.016** | **Drop** — biggest drag |

## Categories

### Critical (drop → Sharpe loss ≥ 0.012)

- **RSI2DipVote** (ΔSharpe -0.037): RSI(2) oversold basket on TQQQ/SOXL/TECL. Pure mean-reversion edge, also worsens DD when removed (-4pp).
- **IBSBasket** (ΔSharpe -0.022): IBS dip-buy with ATR stop. Uncorrelated mean-reversion signal, also worsens DD when removed (-4pp).
- **StretchExit** (ΔSharpe -0.016): Trend entry gated by stretch < 5%, exits when overstretched. Acts as a timing filter that prevents top-chasing.
- **MomVote** (ΔSharpe -0.015): ROC/UpDay/TII momentum votes. Adds a non-SMA momentum dimension that complements the reversion subs.
- **MFI14Hyst** (ΔSharpe -0.012): MFI(14) with hysteresis. Volume/money-flow signal uncorrelated with price-based subs.

### Neutral (within ±0.011)

- GoldXATR (+0.003) — death cross + ATR stop; nearly irrelevant now that StretchExit and MomVote cover similar ground
- SMA200Tiers (+0.005)
- VolReg20 (+0.008)
- SMA5Vote (+0.009)
- LevRebal (+0.010) — static long bias; adds 2pp drawdown protection (LevRebal gets stopped out hard in bad years, dragging the ensemble down)

### Net negative (overlapping trend signals)

- RangeCompr (+0.011)
- **D5Vote (+0.014)**
- **SMA200Pyramid (+0.016)** — largest individual drag

## Key observations

### Changed vs previous LOO (2026-06-07)

Previous analysis included CashReserve and RangeBreakout (since removed). Notable shifts:

- **GoldXATR**: was the biggest drag (+0.022) → now nearly neutral (+0.003). StretchExit now absorbs its role as a timing/exit filter.
- **StretchExit**: was marginal (-0.011) → now clearly critical (-0.016). Its stretch-gated entry is uniquely valuable.
- **MomVote**: was marginal (-0.012) → now clearly critical (-0.015). Momentum dimension is non-redundant.
- **IBSBasket**: was most critical (-0.069) → now second (-0.022). Sharpe is higher overall, compressing absolute deltas.
- **SMA200Pyramid**: remains biggest positive-ΔSharpe drag (+0.018 → +0.016). Consistent finding.

### Mean-reversion dominates

The two most critical subs (RSI2DipVote, IBSBasket) are both pure mean-reversion. Together they account for most of the ensemble's alpha over the trend-following baseline. Both also protect drawdown: removing either adds 4pp to MaxDD.

### Trend subs are largely redundant

5 of 13 subs produce ΔSharpe > 0 (removing helps): RangeCompr, D5Vote, SMA200Pyramid, SMA5Vote, SMA200Tiers. All are SMA/Donchian trend-following on QQQ — correlated signals that pile up leveraged TQQQ exposure without adding new information.

### What's actually doing the work

4 subs carry most of the Sharpe edge:
1. RSI2DipVote (-0.037)
2. IBSBasket (-0.022)
3. StretchExit (-0.016)
4. MomVote (-0.015)

The rest are either neutral diversifiers or slight drags.

## Recommended next experiments

### A. Trimmed 9-sub ensemble

Drop the 3 clearest drags (D5Vote, SMA200Pyramid, RangeCompr). Keep all others.

**Hypothesis:** Sharpe rises from 0.977 → ~1.00+; DD unchanged or improves.

### B. Double down on mean-reversion

Since RSI2DipVote and IBSBasket dominate, test adding:
- RSI(3) oversold variant with different thresholds
- Bollinger Band Z-score dip-buy
- MFI dip-buy (complement to the existing hysteresis filter)

### C. Pairwise LOO on trend subs

LOO is first-order. The 5 neutral/drag trend subs may have pairwise interactions — some combos might be complementary even if individually redundant. Run pairwise drops for SMA200Tiers, SMA5Vote, D5Vote, RangeCompr, SMA200Pyramid.

## Notes

- All weights uniform (10 each, 13 subs). This is also the current production configuration.
- Baseline 38%/-34%/0.977 matches current production ensemble exactly (same weights).
- Backtest IDs: see `/tmp/loo_results_new.json`
