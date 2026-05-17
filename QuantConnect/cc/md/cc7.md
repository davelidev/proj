# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [210](#strategy-210) | ✅    | Oscillator      | 28%  | -52%  | 0.714  | 416   | 289   | 1.44     | 1.58         | 3/10   |
| [212](#strategy-212) | ✅    | Statistical     | 28%  | -37%  | 0.754  | 160   | 116   | 1.38     | 2.75         | 3/10   |
| [223](#strategy-223) | ✅    | Volume          | 31%  | -48%  | 0.746  | 176   | 113   | 1.56     | 2.52         | 3/10   |
| [227](#strategy-227) | ✅    | Volatility      | 32%  | -56%  | 0.786  | 360   | 211   | 1.71     | 1.50         | 3/10   |
| [236](#strategy-236) | ✅    | Oscillator      | 33%  | -40%  | 0.819  | 340   | 257   | 1.32     | 2.25         | 3/10   |
| [239](#strategy-239) | ✅    | Volume          | 35%  | -54%  | 0.796  | 188   | 101   | 1.86     | 2.25         | 3/10   |
| [243](#strategy-243) | ✅    | Seasonality     | 29%  | -54%  | 0.698  | 413   | 242   | 1.71     | 1.23         | 3/10   |


---
## Strategy-210
### MFI(14) + Median-200 (cc3_211.py)

**Description:** A three-state trend-follower combining a 200-bar median price filter with the Money Flow Index on QQQ. Full TQQQ allocation requires both the trend regime and MFI to be bullish; partial allocation (50/50) when only one is positive; full BIL when both are bearish. The MFI uses the midline of 50 as the bullish threshold.

*Overfit 3/10 — MFI period is 14 (standard). Bullish threshold at MFI > 50 (canonical midline). Median-200 exact midpoint. 3/10: two standard indicators at canonical thresholds.*

- **Trend gate:** QQQ close > median of last 200 daily closes (in_trend)
- **Entry (trend):** in_trend AND MFI(14) > 50 → 100% TQQQ
- **Entry (MR):** in_trend XOR MFI > 50 → 50% TQQQ / 50% BIL
- **Exit:** Both conditions bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 28% | -52% | 0.714 | 416 | 289 | 1.44 | 1.58 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 24% | 🔴 -8% | 🟢 3% | 🟢 83% | 🔴 -16% | 🟢 86% | 🟢 109% | 🟢 48% | 🔴 -45% | 🟢 101% | 🟢 27% | 🟢 34% |

> [!code]- Click to view: cc3_211.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_211.py"
> ```


---

## Strategy-212
### Variance Ratio Test (cc3_213.py)

**Description:** A three-state trend-follower that uses the variance ratio test to detect trending versus mean-reverting price behavior in QQQ. When variance of 5-day returns exceeds 5 times the variance of 1-day returns, the series is trending (VR > 1). This signal is combined with a 200-bar median filter for a three-state allocation between TQQQ and BIL.

*Overfit 3/10 — Variance ratio threshold at 1.0 (neutral, not tuned). Lookback of 100 days for variance calculation, 200 for median. 5-day aggregation period is standard for VR tests. 3/10: econometric technique at a natural breakeven threshold.*

- **Trend gate:** QQQ close > median of last 200 daily closes (in_trend)
- **Entry (trend):** Variance ratio(100d, 5d/1d) > 1.0 (trending) AND in_trend → 100% TQQQ
- **Entry (MR):** VR > 1 XOR in_trend → 50% TQQQ / 50% BIL
- **Exit:** Both conditions bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 28% | -37% | 0.754 | 160 | 116 | 1.38 | 2.75 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | 🟢 36% | 🔴 -8% | 🟢 60% | 🔴 -14% | 🟢 27% | 🟢 85% | 🟢 65% | 🔴 -30% | 🟢 72% | 🟢 54% | 🟢 13% |

> [!code]- Click to view: cc3_213.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_213.py"
> ```


---

## Strategy-223
### OBV Slope (cc3_224.py)

**Description:** A three-state trend-follower that measures the slope of On-Balance Volume over a 30-day window on QQQ, combined with a 200-bar median price regime filter. A rising OBV slope signals increasing buying pressure and confirms the price trend. Full TQQQ when both signals are bullish; 50/50 when one is; full BIL when neither.

*Overfit 3/10 — OBV slope window is 30 days. Zero crossing threshold. Median-200 regime. 3/10: two standard volume/price components at natural thresholds.*

- **Trend gate:** QQQ close > median of last 200 daily closes (in_trend)
- **Entry (trend):** OBV linear slope (30d) > 0 AND in_trend → 100% TQQQ
- **Entry (MR):** OBV slope > 0 XOR in_trend → 50% TQQQ / 50% BIL
- **Exit:** Both conditions bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -48% | 0.746 | 176 | 113 | 1.56 | 2.52 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 31% | 🟢 20% | 🔴 -5% | 🟢 80% | 🔴 -13% | 🟢 52% | 🟢 83% | 🟢 60% | 🔴 -25% | 🟢 89% | 🟢 33% | 🟢 26% |

> [!code]- Click to view: cc3_224.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_224.py"
> ```


---

## Strategy-227
### Vol Contraction Regime (cc3_228.py)

**Description:** A three-state trend-follower that detects volatility contraction on QQQ by comparing short-term realized volatility to long-term realized volatility. When the 10-day volatility is below the 60-day volatility (vol is contracting), the market is considered calm. This condition is combined with a 200-bar median price filter for a three-state TQQQ/BIL allocation.

*Overfit 3/10 — Short vol window: 10 days; long vol window: 60 days. Threshold is zero (short < long = contraction). Median-200 regime. 3/10: two components at natural ratio threshold.*

- **Trend gate:** QQQ close > median of last 200 daily closes (in_trend)
- **Entry (trend):** 10-day realized vol < 60-day realized vol (contracting) AND in_trend → 100% TQQQ
- **Entry (MR):** Vol contraction XOR in_trend → 50% TQQQ / 50% BIL
- **Exit:** Both conditions bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -56% | 0.786 | 360 | 211 | 1.71 | 1.50 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 46% | 🟢 7% | 🔴 -11% | 🟢 74% | 🟢 3% | 🟢 78% | 🟢 173% | 🟢 60% | 🔴 -52% | 🟢 100% | 🟢 43% | 🟢 11% |

> [!code]- Click to view: cc3_228.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_228.py"
> ```


---

## Strategy-236
### MFI(20) + Median (cc3_237.py)

**Description:** A three-state trend-follower that pairs the Money Flow Index with a 20-day period alongside a 200-bar median price regime filter on QQQ. Full TQQQ when both MFI and regime are bullish; 50/50 when only one is; full BIL when both are bearish. Using a 20-day MFI is slightly slower than the standard 14-day version.

*Overfit 3/10 — MFI period is 20 (vs standard 14). Midline threshold at 50. Median-200 regime. 3/10: two standard components; the 20-day period is a slight departure from canonical 14.*

- **Trend gate:** QQQ close > median of last 200 daily closes (in_trend)
- **Entry (trend):** MFI(20) > 50 AND in_trend → 100% TQQQ
- **Entry (MR):** MFI > 50 XOR in_trend → 50% TQQQ / 50% BIL
- **Exit:** Both conditions bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -40% | 0.819 | 340 | 257 | 1.32 | 2.25 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 24% | 🟢 9% | 🟢 1% | 🟢 90% | 🔴 -12% | 🟢 82% | 🟢 153% | 🟢 23% | 🔴 -23% | 🟢 80% | 🟢 45% | 🟢 23% |

> [!code]- Click to view: cc3_237.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_237.py"
> ```


---

## Strategy-239
### OBV Slope + Median 3-state (cc3_240.py)

**Description:** A three-state trend-follower that pairs OBV slope over 30 days with a 200-bar median price filter on QQQ, using a skewed intermediate allocation. When both signals are bullish, the strategy holds 100% TQQQ; when only one is bullish, it holds 70/30 TQQQ/BIL (more aggressive than the symmetric 50/50 used in similar strategies); when both are bearish, it holds 100% BIL.

*Overfit 3/10 — OBV slope window 30 days. Intermediate allocation at 70/30 vs 50/50 in comparable algos — this is a specifically tuned weight. Median-200 regime. 3/10: two standard components with one tuned intermediate allocation.*

- **Trend gate:** QQQ close > median of last 200 daily closes (in_trend)
- **Entry (trend):** OBV slope (30d) > 0 AND in_trend → 100% TQQQ
- **Entry (MR):** OBV slope > 0 XOR in_trend → 70% TQQQ / 30% BIL
- **Exit:** Both conditions bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -54% | 0.796 | 188 | 101 | 1.86 | 2.25 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | 🟢 24% | ⚪ 0% | 🟢 94% | 🔴 -17% | 🟢 63% | 🟢 86% | 🟢 70% | 🔴 -34% | 🟢 108% | 🟢 39% | 🟢 28% |

> [!code]- Click to view: cc3_240.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_240.py"
> ```


---

## Strategy-243
### Avoid Mid-Month + Median (cc3_244.py)

**Description:** A seasonal trend-follower that avoids trading during the middle third of each month (calendar days 10–20), where equity markets have historically shown weaker performance. The avoidance window is combined with a 200-bar median regime filter. Full TQQQ outside the mid-month window in an uptrend; 50/50 otherwise; full BIL in downtrend and mid-month.

*Overfit 3/10 — Mid-month exclusion window: calendar days 10–20 (11 days). Exact day boundaries are tuned. Median-200 regime. 3/10: one tuned calendar rule plus a standard trend filter.*

- **Trend gate:** QQQ close > median of last 200 daily closes (in_trend)
- **Entry (trend):** in_trend AND calendar day NOT in 10–20 → 100% TQQQ
- **Entry (MR):** in_trend OR day not in 10–20 → 50% TQQQ / 50% BIL
- **Exit:** Both conditions bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -54% | 0.698 | 413 | 242 | 1.71 | 1.23 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 34% | 🔴 -1% | 🔴 -15% | 🟢 87% | 🔴 -8% | 🟢 49% | 🟢 111% | 🟢 94% | 🔴 -50% | 🟢 99% | 🟢 47% | 🟢 29% |

> [!code]- Click to view: cc3_244.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_244.py"
> ```


---
