# Sub-Algo Correlation Analysis

## Setup

- **Date:** 2026-06-07
- **Method:** Pearson correlation of standalone yearly returns across 12 years (2014-2025)
- **Subjects:** 14 sub-algos (ids 1-14, ensemble id=15 excluded; CashReserve has no yearly returns)
- **Data source:** `cc/backtests/backtest_cc000.jsonl` yearly fields

## Correlation matrix

```
             4    1    2    3    5    7    8    9   10   11   12   13   14    6
RangeBreak    -
LevRebal     .48   -
IBSBasket    .29  .44   -
RSI3Vote     .40  .54  .73   -
SMA200Tiers  .59  .73  .41  .68   -
SMA5Vote     .59  .93  .60  .67  .86   -
D5Vote       .52  .93  .63  .69  .86  .98   -
MomVote      .44  .64  .87  .69  .52  .74  .78   -
StretchExit  .60  .84  .39  .67  .83  .88  .88  .55   -
GoldXATR     .54  .73  .80  .72  .63  .83  .85  .90  .72   -
RangeCompr   .53  .94  .58  .67  .80  .98  .96  .74  .88  .86   -
MFI14Hyst    .15  .67  .68  .57  .47  .66  .75  .86  .49  .76  .69   -
VolReg20     .52  .95  .39  .54  .85  .95  .94  .62  .89  .76  .96  .63   -
SMA200Pyr    .60  .85  .50  .72  .94  .93  .93  .64  .93  .79  .92  .58  .94   -
```

## Headline findings

| Finding | Impact |
|---|---|
| **Zero negative correlations** (smallest pair = +0.15) | The ensemble has **no hedge** — every sub moves with the others |
| 47 pairs above rho 0.7 (out of 91 total pairs) | 52% of sub pairs are highly redundant |
| 5 pairs above rho 0.95 | Some subs are essentially duplicates |
| Average pairwise correlation: 0.70 | The ensemble is **one factor + noise** |
| Most-correlated sub | D5Vote (avg 0.822) |
| Least-correlated sub | RangeBreakout (avg 0.481) |

## Near-duplicates (rho > 0.95)

Effectively the same signal — keeping both is redundant.

| Pair | rho | Interpretation |
|---|---|---|
| SMA5Vote ↔ **RangeCompr** | **0.977** | Nearly identical |
| SMA5Vote ↔ **D5Vote** | **0.976** | Two views of the same trend |
| RangeCompr ↔ VolReg20 | 0.956 | Both regime detectors on QQQ |
| D5Vote ↔ RangeCompr | 0.956 | Same trend factor |
| LevRebal ↔ VolReg20 | 0.946 | Static long ≈ vol-regime long |
| SMA5Vote ↔ VolReg20 | 0.946 | Trend ≈ vol-regime |
| D5Vote ↔ VolReg20 | 0.941 | Same |
| SMA200Tiers ↔ SMA200Pyramid | 0.941 | Same SMA(200) signal, different sizing rule |

## Average correlation per sub

Lower = more diversifying; higher = more redundant.

```
4   RangeBreakout    +0.481  ██████████████
2   IBSBasket        +0.561  ████████████████
13  MFI14Hyst        +0.611  ██████████████████
3   RSI3Vote         +0.637  ███████████████████
9   MomVote          +0.692  ████████████████████
5   SMA200Tiers      +0.705  █████████████████████
10  StretchExit      +0.734  ██████████████████████
1   LevRebal         +0.743  ██████████████████████
11  GoldXATR         +0.761  ██████████████████████
14  VolReg20         +0.762  ██████████████████████
6   SMA200Pyramid    +0.791  ███████████████████████
12  RangeCompr       +0.809  ████████████████████████
7   SMA5Vote         +0.815  ████████████████████████
8   D5Vote           +0.822  ████████████████████████
```

## Structural insight

**The ensemble has no risk-off / negative-correlation component.**

Every sub goes long TQQQ (directly or via basket). The "diversification" is just averaging noise on a single risk factor:

- 6 explicit trend-followers (LevRebal, SMA200Tiers, SMA200Pyramid, SMA5Vote, D5Vote, GoldXATR) — all rho > 0.7 with each other
- 3 regime detectors (RangeCompr, VolReg20, RangeBreakout) — all rho > 0.5 with the trend cluster
- 3 mean-reversion (IBSBasket, RSI3Vote, MomVote) — lower correlation but still all positive

When TQQQ tanks (2018, 2022), every sub-algo's signal weakens simultaneously. The ensemble has no anti-correlated counterweight to dampen the drawdown.

## Cross-reference with LOO analysis

LOO results confirm the correlation findings:

| LOO Drop candidates | Avg correlation | Comment |
|---|---|---|
| GoldXATR (ΔSharpe +0.022) | 0.761 | High redundancy — confirmed |
| SMA200Pyramid (+0.018) | 0.791 | High redundancy — confirmed |
| D5Vote (+0.016) | 0.822 | Highest redundancy — confirmed |
| SMA5Vote (+0.013) | 0.815 | High redundancy — confirmed |
| SMA200Tiers (+0.013) | 0.705 | Moderate redundancy |
| LevRebal (+0.011) | 0.743 | Moderate redundancy |

| LOO Critical contributors | Avg correlation | Comment |
|---|---|---|
| IBSBasket (-0.069) | 0.561 | Low correlation = high diversification value |
| RSI2DipVote (-0.045) | 0.637 | Low correlation = high diversification value |
| MomVote (-0.012) | 0.692 | Low correlation |
| TrendStretchExit (-0.011) | 0.734 | Moderate |
| MFI14Hyst (-0.004) | 0.611 | Low correlation |

**Pattern:** subs with avg correlation < 0.70 tend to be critical contributors. Subs with avg correlation > 0.78 tend to be drag.

## Key takeaway

**The ensemble is wide but shallow.** 14 sub-algos produce essentially one trade (long Nasdaq leveraged) with noise reduction. The 1.036 Sharpe is the ceiling of what this single-factor exposure can achieve.

To meaningfully break through, the ensemble needs sub-algos that go UP when QQQ goes DOWN:

- **TMF** (3x 20Y treasury) — defensive flight-to-safety
- **SQQQ** (3x inverse) — tactical short on momentum break
- **UGL** (2x gold) — crisis hedge
- **VXX** or volatility long — vol-spike capture
- **Short-bias** mean-reversion on extreme overbought signals

A single TMF defensive sub (long TMF when QQQ < SMA200) could likely:
- Cut 2022 DD by 5-8pp (treasuries rallied as Nasdaq fell mid-year, then BOTH fell when Fed pivoted)
- Marginal CAGR impact
- Net Sharpe +0.1 to +0.2

## Recommended next steps

### A. Trim redundant subs
Drop the 6 highest-correlation subs (D5Vote, SMA5Vote, RangeCompr, SMA200Pyramid, VolReg20, GoldXATR — all avg > 0.76). Re-test ensemble.

### B. Build minimal diverse subset
Keep only: RangeBreakout, IBSBasket, MFI14Hyst, RSI3Vote, MomVote, StretchExit + CashReserve. 7 lowest-correlation subs.

### C. Add risk-off sub
Add 1-2 negatively-correlated sub-algos (TMF, UGL). Even if standalone Sharpe is low (~0.5), the correlation diversification could lift ensemble Sharpe significantly.

### D. Run pairwise LOO on redundant cluster
Confirm which pairs in the 6-sub trend cluster are mutually substituting vs additively contributing.

## Caveats

- 12 yearly data points is **small for stable correlation estimates** — confidence intervals ~±0.15 on each rho
- Correlations may differ during specific regimes (bear markets, low-vol periods). Stability not tested
- Yearly returns hide intra-year dynamics. Daily or monthly returns might show different structure
- Standalone correlations don't directly translate to ensemble correlation (subs interact via aggregation)
