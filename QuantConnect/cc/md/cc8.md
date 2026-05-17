# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [251](#strategy-251) | ✅    | Volume          | 29%  | -49%  | 0.732  | 450   | 339   | 1.33     | 1.77         | 3/10   |
| [254](#strategy-254) | ✅    | Volume          | 33%  | -58%  | 0.774  | 282   | 213   | 1.32     | 1.97         | 3/10   |
| [258](#strategy-258) | ✅    | Oscillator      | 33%  | -54%  | 0.798  | 336   | 287   | 1.17     | 2.18         | 3/10   |
| [266](#strategy-266) | ✅    | Ichimoku        | 34%  | -51%  | 0.823  | 195   | 142   | 1.37     | 2.68         | 3/10   |
| [269](#strategy-269) | ✅    | Oscillator      | 30%  | -50%  | 0.714  | 163   | 108   | 1.51     | 2.62         | 3/10   |
| [270](#strategy-270) | ✅    | Volume          | 31%  | -56%  | 0.778  | 360   | 272   | 1.32     | 1.86         | 3/10   |
| [283](#strategy-283) | ✅    | Range           | 34%  | -41%  | 0.824  | 136   | 91    | 1.49     | 3.23         | 3/10   |
| [284](#strategy-284) | ✅    | Range           | 34%  | -49%  | 0.805  | 126   | 95    | 1.33     | 3.80         | 3/10   |
| [293](#strategy-293) | ✅    | Momentum        | 32%  | -44%  | 0.772  | 428   | 323   | 1.33     | 2.26         | 3/10   |
| [295](#strategy-295) | ✅    | Volatility      | 35%  | -53%  | 0.809  | 57    | 48    | 1.19     | 6.54         | 3/10   |
| [297](#strategy-297) | ✅    | Momentum        | 30%  | -52%  | 0.709  | 350   | 275   | 1.27     | 2.27         | 3/10   |
| [298](#strategy-298) | ✅    | Momentum        | 29%  | -52%  | 0.719  | 704   | 553   | 1.27     | 1.78         | 4/10   |
| [299](#strategy-299) | ✅    | Hybrid          | 38%  | -56%  | 0.833  | 341   | 228   | 1.50     | 1.64         | 3/10   |
| [300](#strategy-300) | ✅    | Hybrid          | 30%  | -44%  | 0.734  | 428   | 336   | 1.27     | 1.67         | 4/10   |


---
## Strategy-251
### MFI(10) >50 + Median (cc3_252.py)

**Description:** A trend-following strategy that combines a long-term price median filter with a short-period Money Flow Index. QQQ is used as the signal asset and TQQQ/BIL as execution vehicles. When both the median filter and MFI agree, the strategy goes fully long TQQQ; partial disagreement yields a 50/50 split.

*Overfit 3/10 — MFI period of 10 and threshold of 50 are both relatively standard; the 200-day median split (index 100 of sorted closes) is a slightly unusual trend gate but not aggressively tuned. Overfit risk is low.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** MFI(10) > 50
- **Entry:** Both conditions true → 100% TQQQ
- **Exit (MR):** One condition true → 50% TQQQ / 50% BIL; neither true → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -49% | 0.732 | 450 | 339 | 1.33 | 1.77 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 34% | 🟢 2% | 🔴 -8% | 🟢 51% | 🔴 -7% | 🟢 81% | 🟢 154% | 🟢 45% | 🔴 -44% | 🟢 115% | 🟢 21% | 🟢 22% |

> [!code]- Click to view: cc3_252.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_252.py"
> ```


---

## Strategy-254
### MFI(14) >40 (loose) (cc3_255.py)

**Description:** A loosened variant of the MFI median trend-follower, using a below-neutral MFI threshold of 40 to allow entry under weaker money-flow conditions. This makes the strategy more permissive: it enters TQQQ whenever the price is above its median and even modest positive flow is present.

*Overfit 3/10 — MFI(14) threshold of 40 is deliberately loose and below the neutral 50 midline, reducing the strength filter's selectivity. The 50/50 mixed allocation is standard. One slightly tuned threshold.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** MFI(14) > 40 (loose threshold)
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% BIL; neither true → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -58% | 0.774 | 282 | 213 | 1.32 | 1.97 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 24% | 🟢 9% | 🟢 5% | 🟢 113% | 🔴 -18% | 🟢 91% | 🟢 140% | 🟢 65% | 🔴 -52% | 🟢 92% | 🟢 49% | 🟢 22% |

> [!code]- Click to view: cc3_255.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_255.py"
> ```


---

## Strategy-258
### CCI + Median (cc3_259.py)

**Description:** A trend-following strategy combining a 20-period Commodity Channel Index with a 200-day price median filter on QQQ. CCI above zero indicates bullish momentum; paired with the median trend gate, this drives a three-state TQQQ/BIL allocation.

*Overfit 3/10 — CCI(20) is a standard period; the threshold of zero (neutral line) rather than the conventional ±100 overbought/oversold levels is a slight but reasonable deviation. Two components, one lightly non-canonical threshold.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** CCI(20) > 0
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% BIL; neither true → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -54% | 0.798 | 336 | 287 | 1.17 | 2.18 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 31% | 🔴 -5% | 🟢 2% | 🟢 79% | 🔴 -15% | 🟢 86% | 🟢 146% | 🟢 73% | 🔴 -50% | 🟢 135% | 🟢 33% | 🟢 24% |

> [!code]- Click to view: cc3_259.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_259.py"
> ```


---

## Strategy-266
### Tenkan/Kijun Cross + Median (cc3_267.py)

**Description:** A trend-following strategy using the Ichimoku Tenkan-sen (9-period midpoint) versus Kijun-sen (26-period midpoint) relationship as a momentum signal, combined with a 200-day price median filter. When Tenkan is above Kijun (a standard bullish Ichimoku signal) and the median gate passes, the strategy holds TQQQ.

*Overfit 3/10 — Tenkan (9) and Kijun (26) periods are the textbook Ichimoku defaults; the 200-day median is standard. All components at canonical settings.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** Tenkan (9-period midpoint) > Kijun (26-period midpoint)
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% BIL; neither true → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -51% | 0.823 | 195 | 142 | 1.37 | 2.68 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 36% | 🟢 5% | 🔴 -8% | 🟢 100% | 🔴 -11% | 🟢 65% | 🟢 126% | 🟢 78% | 🔴 -43% | 🟢 88% | 🟢 52% | 🟢 38% |

> [!code]- Click to view: cc3_267.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_267.py"
> ```


---

## Strategy-269
### Stochastic(50,5,5) + Median (cc3_270.py)

**Description:** A trend-following strategy using a slow, wide 50-period Stochastic oscillator above its midline (50) as a momentum filter, combined with a 200-day price median filter on QQQ. The extra-long Stochastic period dampens noise and provides a slower-turning momentum signal.

*Overfit 3/10 — Stochastic period of 50 with smoothing (5,5) is significantly non-standard versus the canonical (14,3,3); threshold of %K > 50 is the midline, which is standard. One notably non-canonical period choice.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** Stochastic(50,5,5) %K > 50
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% BIL; neither true → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -50% | 0.714 | 163 | 108 | 1.51 | 2.62 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🟢 17% | 🔴 -9% | 🟢 110% | 🔴 -21% | 🟢 61% | 🟢 90% | 🟢 63% | 🔴 -46% | 🟢 112% | 🟢 35% | 🟢 27% |

> [!code]- Click to view: cc3_270.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_270.py"
> ```


---

## Strategy-270
### Up/Down Vol Ratio + Median (cc3_271.py)

**Description:** A trend-following strategy using an up/down volume ratio as a market breadth filter: summing volume on up-days versus down-days over the past 20 sessions and requiring buyers to dominate. Combined with a 200-day price median filter on QQQ, it drives a three-state TQQQ/BIL allocation.

*Overfit 3/10 — The 20-day lookback window and the ratio threshold of 1.0 are both round numbers and reasonable defaults. Two standard-feeling components, though the up/down volume ratio is less common than MFI.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** Sum of volume on up-days / sum of volume on down-days (last 20 days) > 1.0
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% BIL; neither true → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -56% | 0.778 | 360 | 272 | 1.32 | 1.86 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 35% | 🟢 13% | 🔴 -4% | 🟢 81% | 🔴 -17% | 🟢 70% | 🟢 77% | 🟢 58% | 🔴 -17% | 🟢 114% | 🟢 29% | 🟢 12% |

> [!code]- Click to view: cc3_271.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_271.py"
> ```


---

## Strategy-283
### Range Expanded 110% (cc3_284.py)

**Description:** A volatility-expansion trend follower that enters TQQQ when QQQ's recent 25-day average range exceeds 110% of the 200-day average, indicating elevated volatility, combined with a median trend gate. This tests whether periods of rising volatility in an uptrend produce strong forward returns.

*Overfit 3/10 — The 110% threshold inverts the compression logic; it is one step in a family of threshold sweeps. Elevated volatility entry is a non-standard signal direction compared to breakout compression strategies. Moderate tuning.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** Avg daily range (last 25 days) > 110% of avg daily range (last 200 days)
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% BIL; neither true → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -41% | 0.824 | 136 | 91 | 1.49 | 3.23 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 23% | 🟢 6% | 🔴 -10% | 🟢 99% | 🟢 1% | 🟢 63% | 🟢 109% | 🟢 62% | 🔴 -34% | 🟢 135% | 🟢 56% | 🟢 8% |

> [!code]- Click to view: cc3_284.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_284.py"
> ```


---

## Strategy-284
### Range Expanded 120% (cc3_285.py)

**Description:** A variant of the range-expansion trend follower with a tighter expansion requirement: the recent 25-day average range must exceed 120% of the 200-day historical average. This fires less frequently than the 110% variant and targets more pronounced volatility expansions.

*Overfit 3/10 — The 120% threshold is a step in the same family of range-expansion threshold sweeps. The concept is the same as the 110% variant with one adjusted parameter.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** Avg daily range (last 25 days) > 120% of avg daily range (last 200 days)
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% BIL; neither true → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -49% | 0.805 | 126 | 95 | 1.33 | 3.80 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 34% | 🟢 6% | 🔴 -4% | 🟢 102% | 🟢 4% | 🟢 67% | 🟢 92% | 🟢 65% | 🔴 -44% | 🟢 147% | 🟢 42% | 🟢 13% |

> [!code]- Click to view: cc3_285.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_285.py"
> ```


---

## Strategy-293
### Dual Mom 20+60 4-state (cc3_294.py)

**Description:** A four-state momentum trend follower combining the 200-day price median with two separate lookback momentum measures (20-day and 60-day). All three votes drive a graduated TQQQ/BIL allocation. This tests whether multi-timeframe momentum agreement (1-month and 3-month) improves timing.

*Overfit 3/10 — 20-day and 60-day momentum lookbacks are both standard timeframes; positive-return thresholds need no tuning. The 4-state allocation table is a parameterized design choice. Three components at near-canonical settings.*

- **Trend gate:** QQQ close > median of last 200 daily closes (1 vote)
- **Strength filter:** QQQ 20-day return > 0 (1 vote); QQQ 60-day return > 0 (1 vote)
- **Allocation:** 3 votes → 100% TQQQ; 2 votes → 70% TQQQ / 30% BIL; 1 vote → 30% TQQQ / 70% BIL; 0 votes → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -44% | 0.772 | 428 | 323 | 1.33 | 2.26 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 23% | 🟢 5% | 🔴 -9% | 🟢 104% | 🔴 -8% | 🟢 62% | 🟢 106% | 🟢 55% | 🔴 -33% | 🟢 121% | 🟢 25% | 🟢 30% |

> [!code]- Click to view: cc3_294.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_294.py"
> ```


---

## Strategy-295
### VIX-Fix Calm Entry + Median (cc3_296.py)

**Description:** A volatility-filtered trend follower using the Williams VIX-Fix (a synthetic volatility measure computed from price relative to a 22-day high) as a calm/stress indicator. Entry requires low synthetic VIX (below 3%) during an uptrend; exit triggers when the VIX-Fix spikes above 8% or the trend fails.

*Overfit 3/10 — The 22-day high window for VIX-Fix is a standard Williams parameter; the calm threshold of 3% and exit threshold of 8% are specific tuned values with no canonical basis. Two thresholds introducing moderate overfit risk.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** VIX-Fix = (22-day high − close) / 22-day high × 100 < 3%
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** VIX-Fix > 8% OR trend gate fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -53% | 0.809 | 57 | 48 | 1.19 | 6.54 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 31% | 🟢 23% | 🔴 -4% | 🟢 118% | 🔴 -31% | 🟢 40% | 🟢 145% | 🟢 78% | 🔴 -31% | 🟢 103% | 🟢 50% | 🟢 19% |

> [!code]- Click to view: cc3_296.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_296.py"
> ```


---

## Strategy-297
### Dual Mom 30+90 4-state (cc3_298.py)

**Description:** A four-state momentum trend follower using medium and longer-term 30-day and 90-day momentum lookbacks alongside the 200-day median filter. The three votes drive a graduated TQQQ/BIL allocation, testing whether intermediate and quarterly momentum agreement improves timing.

*Overfit 3/10 — 30-day and 90-day momentum lookbacks are standard timeframes; positive-return thresholds need no tuning. The 4-state table is a design parameter. Three components at near-canonical settings.*

- **Trend gate:** QQQ close > median of last 200 daily closes (1 vote)
- **Strength filter:** QQQ 30-day return > 0 (1 vote); QQQ 90-day return > 0 (1 vote)
- **Allocation:** 3 votes → 100% TQQQ; 2 votes → 70% TQQQ / 30% BIL; 1 vote → 30% TQQQ / 70% BIL; 0 votes → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -52% | 0.709 | 350 | 275 | 1.27 | 2.27 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 35% | 🔴 -4% | 🔴 -11% | 🟢 101% | 🔴 -3% | 🟢 49% | 🟢 97% | 🟢 56% | 🔴 -46% | 🟢 118% | 🟢 48% | 🟢 25% |

> [!code]- Click to view: cc3_298.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_298.py"
> ```


---

## Strategy-298
### Triple Mom 5-state (cc3_299.py)

**Description:** A five-state momentum trend follower that counts four independent positive-return signals: the 200-day median filter, 10-day, 30-day, and 90-day momentum. The count (0–4) maps to five graduated TQQQ/BIL allocations in 25% increments. This is the most complex pure-momentum variant in this series.

*Overfit 4/10 — Four components (median + three momentum periods), all at near-standard settings. The 5-state allocation table with 25% steps (1.0/0.75/0.5/0.25/0.0) is a parameterized design. The specific three momentum lookbacks (10/30/90) introduce mild selection overfit.*

- **Trend gate:** QQQ close > median of last 200 daily closes (1 vote)
- **Strength filter:** QQQ 10-day return > 0 (1 vote); 30-day return > 0 (1 vote); 90-day return > 0 (1 vote)
- **Allocation:** 4 votes → 100% TQQQ; 3 → 75%; 2 → 50%; 1 → 25%; 0 → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -52% | 0.719 | 704 | 553 | 1.27 | 1.78 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 29% | 🔴 -6% | 🔴 -10% | 🟢 79% | 🔴 -6% | 🟢 69% | 🟢 105% | 🟢 50% | 🔴 -46% | 🟢 130% | 🟢 33% | 🟢 35% |

> [!code]- Click to view: cc3_299.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_299.py"
> ```


---

## Strategy-299
### Mom20+Median+Top1 (cc3_300.py)

**Description:** A hybrid trend follower that pairs the standard 20-day momentum and 200-day median timing signals with a universe selection component: the single largest-cap stock from the top 100 by dollar volume is used as the cash-alternative exposure in mixed states. When both signals are bullish, 100% goes to TQQQ; in mixed states, 50% goes to TQQQ and 50% to the top market-cap stock.

*Overfit 3/10 — The 20-day momentum and 200-day median are both standard. Using the top-1 market-cap stock as the non-leveraged allocation (instead of BIL) is a non-canonical design that benefits from large-cap bias in the backtest period. Mild overfit from this vehicle selection.*

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** QQQ 20-day return > 0
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% top-cap stock; neither true → 100% top-cap stock
- **Universe:** Top 1 stock by market cap from top 100 by dollar volume
- **Symbols:** Signal: QQQ. Execution: TQQQ / largest-cap stock
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -56% | 0.833 | 341 | 228 | 1.50 | 1.64 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 50% | 🟢 15% | 🔴 -1% | 🟢 106% | 🔴 -22% | 🟢 97% | 🟢 170% | 🟢 70% | 🔴 -49% | 🟢 132% | 🟢 43% | 🟢 10% |

> [!code]- Click to view: cc3_300.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_300.py"
> ```


---

## Strategy-300
### Dual Mom Top-1 Step-Down (cc3_301.py)

**Description:** A four-state hybrid that combines the 200-day median, 20-day momentum, and 60-day momentum to drive a step-down allocation across TQQQ, the largest-cap stock, and BIL. As the vote count drops from 3 to 0, the strategy steps down from pure TQQQ through mixed TQQQ/top-cap, to pure top-cap, and finally to a 50/50 top-cap/BIL split.

*Overfit 4/10 — Three components (median + two momentum periods) at near-standard settings; the specific 4-state allocation plan mixing TQQQ, top-cap stock, and BIL in an asymmetric step-down is a highly specific design choice. The universe selection (top market cap stock) adds vehicle-selection risk.*

- **Trend gate:** QQQ close > median of last 200 daily closes (1 vote)
- **Strength filter:** QQQ 20-day return > 0 (1 vote); QQQ 60-day return > 0 (1 vote)
- **Allocation:** 3 votes → 100% TQQQ; 2 votes → 50% TQQQ / 50% top-cap; 1 vote → 100% top-cap; 0 votes → 50% top-cap / 50% BIL
- **Universe:** Top 1 stock by market cap from top 100 by dollar volume
- **Symbols:** Signal: QQQ. Execution: TQQQ / largest-cap stock / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -44% | 0.734 | 428 | 336 | 1.27 | 1.67 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 19% | 🟢 9% | 🔴 -10% | 🟢 102% | 🔴 -10% | 🟢 66% | 🟢 123% | 🟢 55% | 🔴 -34% | 🟢 128% | 🟢 23% | 🟢 7% |

> [!code]- Click to view: cc3_301.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_301.py"
> ```


---
