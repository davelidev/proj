# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [102](#strategy-102) | ✅    | —               | 32%  | -46%  | 0.826  | 215   | 286   | 0.75     | 3.09         | 3/10   |
| [103](#strategy-103) | ✅    | —               | 32%  | -43%  | 0.826  | 196   | 249   | 0.79     | 3.29         | 3/10   |
| [104](#strategy-104) | ✅    | —               | 31%  | -43%  | 0.803  | 191   | 254   | 0.75     | 3.37         | 3/10   |
| [106](#strategy-106) | ✅    | —               | 34%  | -42%  | 0.864  | 320   | 361   | 0.89     | 2.94         | 3/10   |
| [107](#strategy-107) | ✅    | —               | 38%  | -49%  | 0.887  | 314   | 247   | 1.27     | 2.51         | 3/10   |
| [108](#strategy-108) | ✅    | —               | 28%  | -41%  | 0.789  | 190   | 169   | 1.12     | 2.39         | 3/10   |
| [109](#strategy-109) | ✅    | —               | 31%  | -45%  | 0.806  | 199   | 254   | 0.78     | 3.10         | 3/10   |
| [110](#strategy-110) | ✅    | —               | 31%  | -49%  | 0.779  | 180   | 48    | 3.75     | 1.69         | 3/10   |
| [115](#strategy-115) | ✅    | —               | 37%  | -57%  | 0.796  | 34    | 51    | 0.67     | 9.51         | 2/10   |
| [117](#strategy-117) | ✅    | —               | 39%  | -46%  | 0.892  | 290   | 247   | 1.17     | 2.06         | 4/10   |
| [126](#strategy-126) | ✅    | —               | 32%  | -56%  | 0.777  | 181   | 81    | 2.23     | 2.36         | 3/10   |
| [136](#strategy-136) | ✅    | —               | 29%  | -50%  | 0.714  | 362   | 309   | 1.17     | 2.01         | 3/10   |
| [137](#strategy-137) | ✅    | —               | 30%  | -57%  | 0.718  | 289   | 236   | 1.22     | 2.16         | 3/10   |
| [138](#strategy-138) | ✅    | —               | 32%  | -50%  | 0.761  | 209   | 152   | 1.38     | 2.37         | 3/10   |
| [142](#strategy-142) | ✅    | —               | 30%  | -58%  | 0.705  | 192   | 163   | 1.18     | 2.61         | 3/10   |
| [143](#strategy-143) | ✅    | —               | 33%  | -48%  | 0.813  | 292   | 229   | 1.28     | 2.49         | 3/10   |
| [144](#strategy-144) | ✅    | —               | 37%  | -48%  | 0.881  | 318   | 261   | 1.22     | 2.47         | 3/10   |
| [145](#strategy-145) | ✅    | —               | 36%  | -53%  | 0.846  | 313   | 256   | 1.22     | 2.40         | 3/10   |
| [146](#strategy-146) | ✅    | —               | 39%  | -53%  | 0.881  | 365   | 214   | 1.71     | 1.83         | 3/10   |
| [147](#strategy-147) | ✅    | —               | 36%  | -56%  | 0.84   | 336   | 233   | 1.44     | 2.05         | 3/10   |
| [148](#strategy-148) | ✅    | —               | 36%  | -49%  | 0.85   | 327   | 290   | 1.13     | 2.46         | 3/10   |
| [149](#strategy-149) | ✅    | —               | 40%  | -56%  | 0.877  | 371   | 208   | 1.78     | 1.78         | 3/10   |
| [150](#strategy-150) | ✅    | —               | 39%  | -58%  | 0.87   | 361   | 212   | 1.70     | 1.85         | 3/10   |


---
## Strategy-102
### ROC+D200 + 4% Trail (cc3_103.py)

**Description:** A trend-following strategy on QQQ identical in structure to the 3% trail variant but with a looser trailing stop threshold. Holding TQQQ requires positive short-term momentum, price above the long-term range midpoint, and a pullback from the recent high within the tolerance. Failure of any condition rotates the portfolio to short-term Treasuries.

*Overfit 3/10 — Same three-component structure as cc3_102 with the trailing stop widened to 4% from the 20-day high. Three tuned parameters: ROC(20), D200 midpoint regime, and 4% trail threshold.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry:** ROC(20) > 0 AND price > D200 mid AND drawdown from 20d high > -4% → 100% TQQQ
- **Exit:** Any condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -46% | 0.826 | 215 | 286 | 0.75 | 3.09 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -22% | 🔴 -2% | 🟢 85% | 🔴 -9% | 🟢 66% | 🟢 208% | 🟢 28% | 🔴 -19% | 🟢 68% | 🟢 38% | 🟢 34% |

> [!code]- Click to view: cc3_103.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_103.py"
> ```


---

## Strategy-103
### ROC+D200 + 6% Trail (cc3_104.py)

**Description:** A trend-following strategy on QQQ that gates TQQQ exposure behind positive short-term momentum, a long-term range regime filter, and a trailing drawdown tolerance. This variant uses a 6% trailing stop from the recent high, allowing deeper retracements before exiting. When the combined signal is negative the portfolio holds short-term Treasuries.

*Overfit 3/10 — Three tuned parameters: ROC(20) threshold at zero, 200-day high/low midpoint regime, and 6% trailing drawdown stop from the 20-day high. Non-standard midpoint regime adds specificity.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry:** ROC(20) > 0 AND price > D200 mid AND drawdown from 20d high > -6% → 100% TQQQ
- **Exit:** Any condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -43% | 0.826 | 196 | 249 | 0.79 | 3.29 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -11% | 🔴 -2% | 🟢 85% | 🔴 -15% | 🟢 66% | 🟢 232% | 🟢 39% | 🔴 -19% | 🟢 56% | 🟢 20% | 🟢 42% |

> [!code]- Click to view: cc3_104.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_104.py"
> ```


---

## Strategy-104
### ROC+D200 + 8% Trail (cc3_105.py)

**Description:** A trend-following strategy on QQQ that applies three filters before holding a leveraged tech ETF: positive short-term momentum, price above the midpoint of the long-term price range, and a loose trailing drawdown tolerance. This variant uses the widest trailing stop of the series at 8% below the recent high, minimizing whipsaw exits.

*Overfit 3/10 — Three tuned parameters: ROC(20), 200-day midpoint regime, and 8% trailing stop from the 20-day high. The 8% threshold is the loosest of the trail variants, introducing a curve-fit choice on stop width.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry:** ROC(20) > 0 AND price > D200 mid AND drawdown from 20d high > -8% → 100% TQQQ
- **Exit:** Any condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -43% | 0.803 | 191 | 254 | 0.75 | 3.37 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -11% | 🔴 -2% | 🟢 85% | 🔴 -15% | 🟢 66% | 🟢 185% | 🟢 39% | 🔴 -19% | 🟢 56% | 🟢 28% | 🟢 42% |

> [!code]- Click to view: cc3_105.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_105.py"
> ```


---

## Strategy-106
### 3-State 30/70 + 6% Trail (cc3_107.py)

**Description:** A three-state trend-following strategy on QQQ that adjusts leverage in a graded way based on two signals: a short-term momentum indicator and a long-term price range regime, combined with a trailing stop tolerance. When both signals and the drawdown guard are positive the portfolio is fully in TQQQ; when only one signal agrees it holds a partial allocation; otherwise cash. This variant's mixed state holds 30% TQQQ / 70% BIL.

*Overfit 3/10 — Three parameters: ROC(20), D200 midpoint, and 6% trailing stop. The 30/70 mixed-state split is a tuned allocation choice not derived from first principles.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** ROC(20) > 0 AND price > D200 mid AND trail > -6% → 100% TQQQ
- **Entry (MR):** Only one of ROC/D200 true AND trail > -6% → 30% TQQQ / 70% BIL
- **Exit:** Both signals fail OR trail breached → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -42% | 0.864 | 320 | 361 | 0.89 | 2.94 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🔴 -6% | 🔴 -1% | 🟢 95% | 🔴 -16% | 🟢 71% | 🟢 230% | 🟢 34% | 🔴 -22% | 🟢 65% | 🟢 28% | 🟢 39% |

> [!code]- Click to view: cc3_107.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_107.py"
> ```


---

## Strategy-107
### ROC+D200 + SHV Defense (cc3_108.py)

**Description:** A three-state trend-following strategy on QQQ that swaps the defensive cash vehicle from BIL to SHV (short-term Treasury bills). The three states are fully invested in the leveraged Nasdaq ETF, half-and-half between that ETF and SHV, or entirely in SHV. Regime is determined by the combination of a momentum indicator and a long-term price range midpoint.

*Overfit 3/10 — Two standard components: ROC(20) and D200 midpoint. The 50/50 mixed-state split and choice of SHV over BIL add slight specificity. Rated 3/10 for the three-state allocation tuning.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** ROC(20) > 0 AND price > D200 mid → 100% TQQQ
- **Entry (MR):** Only one signal true → 50% TQQQ / 50% SHV
- **Exit:** Both signals false → 100% SHV
- **Symbols:** Signal: QQQ. Execution: TQQQ / SHV
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -49% | 0.887 | 314 | 247 | 1.27 | 2.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | 🟢 6% | ⚪ 0% | 🟢 101% | 🔴 -12% | 🟢 84% | 🟢 138% | 🟢 62% | 🔴 -32% | 🟢 92% | 🟢 45% | 🟢 33% |

> [!code]- Click to view: cc3_108.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_108.py"
> ```


---

## Strategy-108
### Triple-AND ROC+Aroon+D200 (cc3_109.py)

**Description:** A trend-following strategy that requires three independent indicators to agree before holding the leveraged Nasdaq ETF: positive short-term momentum, an Aroon oscillator confirming the uptrend with the up line dominant, and price above the long-term range midpoint. All three must align simultaneously; otherwise the portfolio holds cash.

*Overfit 3/10 — Three components gated by a triple-AND: ROC(20) > 0, Aroon(25) up > 70 and up > down, and D200 midpoint. The Aroon(25) period and 70 threshold are specific parameter choices.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(20) > 0 AND Aroon(25) up > 70 AND Aroon up > Aroon down
- **Entry:** All three conditions true → 100% TQQQ
- **Exit:** Any condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 28% | -41% | 0.789 | 190 | 169 | 1.12 | 2.39 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 13% | 🔴 -19% | 🟢 7% | 🟢 53% | 🔴 -23% | 🟢 71% | 🟢 82% | 🟢 50% | 🔴 -19% | 🟢 138% | 🟢 36% | 🟢 39% |

> [!code]- Click to view: cc3_109.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_109.py"
> ```


---

## Strategy-109
### ROC+D100 + 5% Trail (cc3_110.py)

**Description:** A trend-following strategy on QQQ that uses a shorter 100-day price range midpoint as the regime filter instead of the more common 200-day window. Positive momentum, price above the midpoint of the 100-day range, and a 5% trailing stop from the 20-day high must all hold to stay invested in the leveraged Nasdaq ETF.

*Overfit 3/10 — Three tuned parameters: ROC(20), D100 midpoint (non-standard period), and 5% trailing stop from the 20-day high. The 100-day window is less canonical than the 200-day.*

- **Trend gate:** QQQ price > midpoint of 100-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry:** ROC(20) > 0 AND price > D100 mid AND drawdown from 20d high > -5% → 100% TQQQ
- **Exit:** Any condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -45% | 0.806 | 199 | 254 | 0.78 | 3.10 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 19% | 🔴 -14% | 🔴 -5% | 🟢 85% | 🔴 -15% | 🟢 66% | 🟢 188% | 🟢 39% | 🔴 -32% | 🟢 114% | 🟢 23% | 🟢 42% |

> [!code]- Click to view: cc3_110.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_110.py"
> ```


---

## Strategy-110
### Top-5 50% + 50% TQQQ Overlay (cc3_111.py)

**Description:** A hybrid rotator that combines an equal-weighted basket of the five largest US mega-cap stocks with a TQQQ trend overlay. Half the portfolio is always allocated equally across the top-five market-cap names; the other half is in TQQQ when QQQ is above the midpoint of its 200-day range, or in BIL when below. Both legs rebalance daily on regime change.

*Overfit 3/10 — Two standard components: top-5 market-cap universe selection and D200 midpoint regime. The fixed 50/50 split between mega-caps and TQQQ is a tuned allocation choice.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Universe:** Top 5 stocks by market cap from the top 100 by dollar volume
- **Allocation:** 50% equally across top-5 mega-caps (always); 50% TQQQ in bull / 50% BIL in bear
- **Symbols:** Signal: QQQ. Execution: top-5 mega-caps + TQQQ / BIL
- **Rebalance:** Daily on regime change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -49% | 0.779 | 180 | 48 | 3.75 | 1.69 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 37% | 🟢 17% | 🟢 2% | 🟢 79% | 🔴 -10% | 🟢 65% | 🟢 83% | 🟢 74% | 🔴 -44% | 🟢 78% | 🟢 51% | 🟢 23% |

> [!code]- Click to view: cc3_111.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_111.py"
> ```


---

## Strategy-115
### QQQ Range Position (cc3_116.py)

**Description:** A statistical mean-reversion/trend strategy that measures where QQQ's current price sits within its 200-day high-to-low range, expressed as a normalized position from 0 to 1. When price is in the upper half of the range the portfolio holds TQQQ; when in the lower half it holds BIL.

*Overfit 2/10 — Single textbook indicator: price position within a 200-day range with a 0.5 (midpoint) threshold. This is an essentially canonical range-position filter. Rated 2/10 as a single standard component at a natural threshold.*

- **Entry:** (price − 200d low) / (200d high − 200d low) > 0.5 → 100% TQQQ
- **Exit:** Range position ≤ 0.5 → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -57% | 0.796 | 34 | 51 | 0.67 | 9.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 22% | 🔴 -5% | 🟢 118% | 🔴 -19% | 🟢 80% | 🟢 97% | 🟢 88% | 🔴 -47% | 🟢 93% | 🟢 62% | 🟢 20% |

> [!code]- Click to view: cc3_116.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_116.py"
> ```


---

## Strategy-117
### Mega-Cap Dispersion Regime (cc3_118.py)

**Description:** A breadth-based trend follower that adds a cohesion filter to the standard D200 regime: it only holds TQQQ when both QQQ is in an uptrend and the five largest US stocks are moving together, as measured by the standard deviation of their 20-day returns being below a threshold. High dispersion among mega-caps signals stress and triggers a shift to cash.

*Overfit 4/10 — Three parameters: D200 midpoint regime, the top-5 market-cap universe, and a 5% cross-sectional standard deviation threshold on 20-day returns. The 5% dispersion cutoff is a specific tuned value.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** Std dev of 20-day returns across top-5 mega-caps < 5%
- **Entry:** In trend AND dispersion < 5% → 100% TQQQ
- **Exit:** Trend breaks OR dispersion ≥ 5% → 100% BIL
- **Symbols:** Signal: QQQ + top-5 mega-cap dispersion. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -46% | 0.892 | 290 | 247 | 1.17 | 2.06 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 37% | 🟢 38% | 🔴 -6% | 🟢 118% | 🔴 -6% | 🟢 110% | 🟢 15% | 🟢 158% | 🔴 -40% | 🟢 106% | 🟢 60% | 🟢 18% |

> [!code]- Click to view: cc3_118.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_118.py"
> ```


---

## Strategy-126
### Top-5 50% + 50% TQQQ Always-In (cc3_127.py)

**Description:** A hybrid rotator that is always invested and never holds cash. Half the portfolio is allocated equally across the five largest US mega-cap stocks. The other half is in TQQQ during a bull regime and is added to the equal-weight mega-cap allocation during a bear regime, meaning the entire portfolio moves to the top-5 stocks when QQQ is below the D200 midpoint.

*Overfit 3/10 — Two standard components: top-5 market-cap universe and D200 midpoint regime. The always-invested structure and 50/50 split with TQQQ overlay are design choices rather than specific numeric thresholds.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Universe:** Top 5 stocks by market cap from the top 100 by dollar volume
- **Allocation:** Bull: 50% equally across top-5 + 50% TQQQ; Bear: 100% equally across top-5 (no TQQQ, no cash)
- **Symbols:** Signal: QQQ. Execution: top-5 mega-caps + TQQQ
- **Rebalance:** Daily on regime change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -56% | 0.777 | 181 | 81 | 2.23 | 2.36 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 37% | 🟢 17% | 🟢 4% | 🟢 79% | 🔴 -9% | 🟢 72% | 🟢 93% | 🟢 74% | 🔴 -52% | 🟢 95% | 🟢 51% | 🟢 26% |

> [!code]- Click to view: cc3_127.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_127.py"
> ```


---

## Strategy-136
### 3-State ROC(15)+D200 (cc3_137.py)

**Description:** A three-state trend follower on QQQ that uses a 15-day rate-of-change indicator and a 200-day price range midpoint. When both signals are positive the portfolio is 100% in TQQQ; when exactly one is positive it holds a partial TQQQ/BIL split; when both are negative it moves fully to BIL. This is the shortest ROC variant in the three-state family.

*Overfit 3/10 — Two standard components in a three-state structure: ROC(15) and D200 midpoint. The 15-day ROC period is shorter than canonical and the 50/50 mixed allocation is a design choice.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(15) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 50% TQQQ / 50% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -50% | 0.714 | 362 | 309 | 1.17 | 2.01 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 36% | 🔴 -20% | 🟢 10% | 🟢 86% | 🔴 -31% | 🟢 99% | 🟢 112% | 🟢 77% | 🔴 -43% | 🟢 84% | 🟢 37% | 🟢 28% |

> [!code]- Click to view: cc3_137.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_137.py"
> ```


---

## Strategy-137
### 3-State ROC(25)+D200 (cc3_138.py)

**Description:** A three-state trend follower that uses a 25-day rate-of-change indicator paired with a 200-day price range midpoint to classify the market into three regimes: fully bullish, mixed, and bearish. Allocations cascade from 100% TQQQ to a 50/50 blend to 100% BIL based on how many signals agree.

*Overfit 3/10 — Two standard components in a three-state structure: ROC(25) and D200 midpoint. The 25-day ROC period and 50/50 mixed split are tuned choices.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(25) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 50% TQQQ / 50% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -57% | 0.718 | 289 | 236 | 1.22 | 2.16 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 30% | 🟢 14% | 🔴 -1% | 🟢 89% | 🔴 -13% | 🟢 51% | 🟢 105% | 🟢 49% | 🔴 -48% | 🟢 91% | 🟢 56% | 🟢 29% |

> [!code]- Click to view: cc3_138.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_138.py"
> ```


---

## Strategy-138
### 3-State ROC(45)+D200 (cc3_139.py)

**Description:** A three-state trend follower that uses a 45-day rate-of-change indicator and a 200-day price range midpoint to determine market regime. The three-state structure cascades from full TQQQ exposure to a partial blend to full BIL depending on signal agreement. The 45-day ROC gives a medium-term momentum read.

*Overfit 3/10 — Two standard components: ROC(45) and D200 midpoint. The 45-day period is a moderately non-standard lookback; the 50/50 mixed allocation is a design choice.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(45) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 50% TQQQ / 50% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -50% | 0.761 | 209 | 152 | 1.38 | 2.37 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 19% | 🔴 -3% | 🟢 3% | 🟢 102% | 🟢 6% | 🟢 58% | 🟢 85% | 🟢 67% | 🔴 -44% | 🟢 102% | 🟢 46% | 🟢 42% |

> [!code]- Click to view: cc3_139.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_139.py"
> ```


---

## Strategy-142
### 3-State ROC(50)+D200 (cc3_143.py)

**Description:** A three-state trend follower on QQQ using a 50-day rate-of-change and a 200-day price range midpoint. The medium-long ROC captures roughly a quarter-year of price momentum. The three-state structure produces a 50/50 blend in ambiguous regimes.

*Overfit 3/10 — Two standard components: ROC(50) and D200 midpoint. The 50-day period is a conventional intermediate-term momentum window; this is the most standard ROC choice in the family.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(50) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 50% TQQQ / 50% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -58% | 0.705 | 192 | 163 | 1.18 | 2.61 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🔴 -7% | 🔴 -2% | 🟢 118% | 🔴 -19% | 🟢 68% | 🟢 79% | 🟢 75% | 🔴 -55% | 🟢 116% | 🟢 53% | 🟢 36% |

> [!code]- Click to view: cc3_143.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_143.py"
> ```


---

## Strategy-143
### 3-State Dual-ROC(20,45)+D200 (cc3_144.py)

**Description:** A three-state trend follower that strengthens the momentum gate by requiring both a 20-day and a 45-day rate-of-change to be positive simultaneously, in addition to the 200-day price range midpoint. The momentum condition is the logical AND of the two ROC readings. This tighter joint condition reduces false positives relative to single-ROC variants.

*Overfit 3/10 — Three components: dual ROC(20) AND ROC(45) and D200 midpoint. The dual-ROC AND condition and the 45-day period are specific choices that reduce trade frequency. Rated 3/10 for the extra component.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** ROC(20) > 0 AND ROC(45) > 0
- **Entry (trend):** Both ROCs positive AND price > D200 mid → 100% TQQQ
- **Entry (MR):** Exactly one of (dual-ROC, D200) true → 50% TQQQ / 50% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -48% | 0.813 | 292 | 229 | 1.28 | 2.49 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 35% | 🔴 -8% | ⚪ 0% | 🟢 93% | 🔴 -8% | 🟢 70% | 🟢 115% | 🟢 58% | 🔴 -34% | 🟢 91% | 🟢 47% | 🟢 27% |

> [!code]- Click to view: cc3_144.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_144.py"
> ```


---

## Strategy-144
### 3-State ROC(20)+D175 (cc3_145.py)

**Description:** A three-state trend follower that uses a 20-day rate-of-change paired with a shorter-than-usual 175-day price range midpoint instead of the canonical 200-day window. The three-state structure allocates 100% TQQQ, a 50/50 blend, or 100% BIL based on signal agreement.

*Overfit 3/10 — Two components: ROC(20) and D175 midpoint. The 175-day window is a non-standard, tuned alternative to the conventional 200-day range.*

- **Trend gate:** QQQ price > midpoint of 175-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 50% TQQQ / 50% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -48% | 0.881 | 318 | 261 | 1.22 | 2.47 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | 🟢 6% | ⚪ 0% | 🟢 101% | 🔴 -20% | 🟢 84% | 🟢 161% | 🟢 62% | 🔴 -31% | 🟢 94% | 🟢 38% | 🟢 33% |

> [!code]- Click to view: cc3_145.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_145.py"
> ```


---

## Strategy-145
### 3-State ROC(20)+D250 (cc3_146.py)

**Description:** A three-state trend follower that uses a 20-day rate-of-change paired with a longer 250-day price range midpoint — approximately one trading year. The extended range window makes the regime filter slower to respond to trend changes. The three-state structure otherwise follows the same 100%/50%/0% TQQQ cascade.

*Overfit 3/10 — Two components: ROC(20) and D250 midpoint. The 250-day window is a longer-than-standard choice that smooths the regime signal.*

- **Trend gate:** QQQ price > midpoint of 250-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 50% TQQQ / 50% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -53% | 0.846 | 313 | 256 | 1.22 | 2.40 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | ⚪ 0% | 🟢 2% | 🟢 101% | 🔴 -10% | 🟢 84% | 🟢 138% | 🟢 62% | 🔴 -38% | 🟢 90% | 🟢 44% | 🟢 24% |

> [!code]- Click to view: cc3_146.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_146.py"
> ```


---

## Strategy-146
### 3-State ROC20+D175 70/30 (cc3_147.py)

**Description:** A three-state trend follower using ROC(20) and a 175-day range midpoint that varies the mixed-state allocation: instead of the canonical 50/50 split the ambiguous regime holds 70% TQQQ and 30% BIL. This gives a more aggressive posture in uncertain markets compared to the 50/50 baseline.

*Overfit 3/10 — Three tuned elements: ROC(20), D175 midpoint (non-standard window), and a 70/30 mixed-state allocation. The combination of a non-standard range period and a specific mixed-state split adds overfit specificity.*

- **Trend gate:** QQQ price > midpoint of 175-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 70% TQQQ / 30% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -53% | 0.881 | 365 | 214 | 1.71 | 1.83 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 12% | 🔴 -1% | 🟢 108% | 🔴 -23% | 🟢 91% | 🟢 159% | 🟢 72% | 🔴 -36% | 🟢 109% | 🟢 43% | 🟢 28% |

> [!code]- Click to view: cc3_147.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_147.py"
> ```


---

## Strategy-147
### 3-State ROC20+D250 60/40 (cc3_148.py)

**Description:** A three-state trend follower using ROC(20) and a 250-day range midpoint with a 60/40 TQQQ/BIL split in the mixed state. The longer range window slows regime detection and the intermediate mixed allocation sits between the 50/50 and 70/30 variants.

*Overfit 3/10 — Three tuned elements: ROC(20), D250 midpoint (longer window), and a 60/40 mixed-state allocation. The choice of 60/40 versus the standard 50/50 or other splits is a specific design decision.*

- **Trend gate:** QQQ price > midpoint of 250-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 60% TQQQ / 40% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -56% | 0.84 | 336 | 233 | 1.44 | 2.05 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 44% | 🟢 2% | 🟢 2% | 🟢 104% | 🔴 -9% | 🟢 87% | 🟢 132% | 🟢 67% | 🔴 -41% | 🟢 96% | 🟢 48% | 🟢 20% |

> [!code]- Click to view: cc3_148.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_148.py"
> ```


---

## Strategy-148
### 3-State ROC20+D125 50/50 (cc3_149.py)

**Description:** A three-state trend follower using ROC(20) and a shorter 125-day price range midpoint. The half-year range window makes the regime filter more responsive than the 200-day or 250-day variants. The mixed state holds a 50/50 TQQQ/BIL split.

*Overfit 3/10 — Two components: ROC(20) and D125 midpoint. The 125-day window (roughly a half-year) is a specific non-canonical period choice that sits shorter than the conventional 200-day range.*

- **Trend gate:** QQQ price > midpoint of 125-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 50% TQQQ / 50% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -49% | 0.85 | 327 | 290 | 1.13 | 2.46 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 35% | 🟢 13% | 🔴 -9% | 🟢 101% | 🔴 -31% | 🟢 77% | 🟢 147% | 🟢 62% | 🔴 -27% | 🟢 98% | 🟢 30% | 🟢 52% |

> [!code]- Click to view: cc3_149.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_149.py"
> ```


---

## Strategy-149
### 3-State ROC20+D175 80/20 (cc3_150.py)

**Description:** A three-state trend follower using ROC(20) and a 175-day range midpoint with a notably aggressive 80/20 TQQQ/BIL split in the mixed state. This configuration maintains substantial leveraged exposure even in ambiguous regimes, making it the most aggressive of the mixed-state variants.

*Overfit 3/10 — Three tuned elements: ROC(20), D175 midpoint (non-standard), and an 80/20 mixed-state allocation that is more aggressive than canonical. The 80% TQQQ in the mixed state is a specific tuned choice.*

- **Trend gate:** QQQ price > midpoint of 175-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 80% TQQQ / 20% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -56% | 0.877 | 371 | 208 | 1.78 | 1.78 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 50% | 🟢 16% | 🔴 -2% | 🟢 111% | 🔴 -25% | 🟢 94% | 🟢 158% | 🟢 77% | 🔴 -39% | 🟢 116% | 🟢 45% | 🟢 26% |

> [!code]- Click to view: cc3_150.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_150.py"
> ```


---

## Strategy-150
### 3-State ROC20+D225 70/30 (cc3_151.py)

**Description:** A three-state trend follower using ROC(20) and a 225-day price range midpoint with a 70/30 TQQQ/BIL allocation in the mixed state. The 225-day window sits between the standard 200-day and the longer 250-day variants, offering a slightly smoother regime signal. The 70/30 mixed allocation matches the 70/30 D175 variant in aggressiveness.

*Overfit 3/10 — Three tuned elements: ROC(20), D225 midpoint (non-standard window), and a 70/30 mixed-state allocation. The 225-day period is a specific, non-canonical selection between standard periods.*

- **Trend gate:** QQQ price > midpoint of 225-day high/low range
- **Strength filter:** ROC(20) > 0
- **Entry (trend):** Both true → 100% TQQQ
- **Entry (MR):** Exactly one true → 70% TQQQ / 30% BIL
- **Exit:** Both false → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -58% | 0.87 | 361 | 212 | 1.70 | 1.85 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 4% | 🟢 2% | 🟢 108% | 🔴 -9% | 🟢 91% | 🟢 126% | 🟢 72% | 🔴 -42% | 🟢 110% | 🟢 51% | 🟢 29% |

> [!code]- Click to view: cc3_151.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_151.py"
> ```


---
