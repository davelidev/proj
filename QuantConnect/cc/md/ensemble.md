# ensemble

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [1](#strategy-1)     | ✅    | Buy & Hold      | 28%  | -51%  | 0.727  | 12    | 0     | —        | —            | 1/10   |
| [2](#strategy-2)     | ✅    | Mean Reversion  | 40%  | -32%  | 0.953  | 1281  | 928   | 1.38     | 1.47         | 2/10   |
| [3](#strategy-3)     | ✅    | Trend Following | 31%  | -49%  | 0.738  | 65    | 57    | 1.14     | 2.69         | 4/10   |
| [4](#strategy-4)     | ✅    | Breakout        | 38%  | -49%  | 0.886  | 94    | 76    | 1.24     | 2.19         | 4/10   |
| [5](#strategy-5)     | ✅    | Trend Following | 40%  | -55%  | 0.871  | 22    | 36    | 0.61     | 13.35        | 2/10   |
| [6](#strategy-6)     | ✅    | Mean Reversion  | 46%  | -43%  | 1.049  | 271   | 106   | 2.56     | 0.96         | 3/10   |
| [7](#strategy-7)     | ✅    | Momentum        | 35%  | -50%  | 0.834  | 112   | 131   | 0.85     | 3.02         | 2/10   |
| [8](#strategy-8)     | ✅    | Momentum        | 35%  | -50%  | 0.834  | 112   | 131   | 0.85     | 3.02         | 2/10   |
| [9](#strategy-9)     | ✅    | Breadth         | 32%  | -53%  | 0.792  | 98    | 129   | 0.76     | 3.31         | 2/10   |
| [10](#strategy-10)   | ✅    | Trend           | 29%  | -45%  | 0.695  | 302   | 193   | 1.56     | 1.09         | 2/10   |
| [11](#strategy-11)   | ✅    | Price Position  | 34%  | -55%  | 0.78   | 22    | 55    | 0.40     | 10.02        | 1/10   |
| [12](#strategy-12)   | ✅    | Mean Reversion  | 40%  | -56%  | 0.925  | 49    | 80    | 0.61     | 8.62         | 3/10   |
| [13](#strategy-13)   | ✅    | Trend           | 30%  | -51%  | 0.715  | 120   | 70    | 1.71     | 4.25         | 3/10   |
| [14](#strategy-14)   | ✅    | Trend           | 37%  | -57%  | 0.796  | 34    | 51    | 0.67     | 9.51         | 2/10   |
| [15](#strategy-15)   | ✅    | Trend           | 31%  | -43%  | 0.794  | 193   | 256   | 0.75     | 3.27         | 3/10   |
| [16](#strategy-16)   | ✅    | Trend           | 29%  | -43%  | 0.814  | 741   | 711   | 1.04     | 3.24         | 4/10   |
| [17](#strategy-17)   | ✅    | Range           | 34%  | -41%  | 0.824  | 136   | 91    | 1.49     | 3.23         | 3/10   |
| [18](#strategy-18)   | ✅    | Volume          | 31%  | -44%  | 0.783  | 110   | 73    | 1.51     | 2.44         | 2/10   |
| [19](#strategy-19)   | ✅    | Ensemble        | 36%  | -33%  | 0.982  | 3791  | 2324  | 1.63     | 1.83         | N/A    |


---
## Strategy-1
### TQQQ 60% Annual Rebalance (001.py)

**Description:** Holds a static 60% allocation to TQQQ, rebalancing once per year on the first trading day of each year to correct drift. Serves as a leveraged baseline — no signal logic, just a constant leveraged Nasdaq position.

*Overfit 1/10 — Single parameter: 60% allocation. The round number is a deliberate design choice, not a swept value. Minimal overfit risk.*

- **Allocation:** 60% TQQQ at all times
- **Rebalance:** Annual — first trading day of each year, resets to 60%
- **No signal:** No entry/exit logic; pure static allocation

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 28% | -51% | 0.727 | 12 | 0 | — | — |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 34% | 🟢 13% | 🟢 4% | 🟢 71% | 🔴 -13% | 🟢 81% | 🟢 66% | 🟢 53% | 🔴 -48% | 🟢 118% | 🟢 37% | 🟢 18% |

> [!code]- Click to view: 001.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/001.py"
> ```


---

## Strategy-2
### QQQ RSI(2) Dip → Equal-Weight TQQQ/SOXL/TECL (002.py)

**Description:** Enters an equal-weight basket of TQQQ, SOXL, and TECL (3× leveraged tech) when QQQ's 2-period Wilder RSI drops below 20, capturing short-term oversold bounces in leveraged Nasdaq. Exits fully when RSI recovers above 20.

*Overfit 2/10 — Two parameters: RSI period 2 and threshold 20. Both are canonical for ultra-short mean reversion. The three-name basket is a deliberate diversification, not a swept choice.*

- **Entry:** QQQ RSI(2, Wilder) < 20: 33% TQQQ + 33% SOXL + 33% TECL
- **Exit:** QQQ RSI(2) ≥ 20: liquidate all three
- **Symbols:** Signal: QQQ. Execution: TQQQ / SOXL / TECL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -32% | 0.953 | 1281 | 928 | 1.38 | 1.47 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 38% | 🟢 1% | 🔴 -18% | 🟢 46% | 🟢 12% | 🟢 34% | 🟢 81% | 🟢 110% | 🟢 32% | 🟢 60% | 🟢 72% | 🟢 62% |

> [!code]- Click to view: 002.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/002.py"
> ```


---

## Strategy-3
### TQQQ Dynamic Sizing: SMA200 + RSI Tiers (003.py)

**Description:** Three-tier TQQQ sizing gated by the 200-day SMA. Above SMA: 100% on RSI(2) < 30 dip, 50% default, 20% on RSI(10) overbought > 80. Below SMA: cash. Adapts position size to both trend regime and short-term momentum state.

*Overfit 4/10 — Five parameters: SMA 200, RSI2 period/threshold, RSI10 period/threshold, three allocation levels (100/50/20%). The allocation tiers feel calibrated; the combination of two RSI indicators on the same asset adds fitting risk.*

- **Regime gate:** TQQQ > SMA(200): active; else 0% (cash)
- **Dip entry:** RSI(2, Wilder) < 30: 100% TQQQ
- **Overbought trim:** RSI(10, Wilder) > 80: 20% TQQQ
- **Default:** 50% TQQQ when in regime with no RSI signal
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -49% | 0.738 | 65 | 57 | 1.14 | 2.69 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 35% | 🟢 4% | 🔴 -15% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 68% | 🟢 83% | 🔴 -21% | 🟢 70% | 🟢 29% | 🟢 25% |

> [!code]- Click to view: 003.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/003.py"
> ```


---

## Strategy-4
### TQQQ Expanding Range Breakout + ATR Trailing Stop (004.py)

**Description:** Enters TQQQ when QQQ is in an uptrend (above SMA 200), the previous day's bar range expanded vs. the bar before it, and ADX(10) > 25 confirming trend strength. Manages the trade with a 3×ATR(14) Wilder trailing stop and exits at the 20-day high or on QQQ falling below SMA.

*Overfit 4/10 — Five parameters: SMA 200, ADX 10/threshold 25, ATR 14/multiplier 3, 20-day exit high. The combination of range expansion + ADX is somewhat fitted; the ATR multiplier 3 is standard.*

- **Entry:** QQQ > SMA(200) AND prior bar range > bar-before range AND ADX(10) > 25: 100% TQQQ
- **Trailing stop:** Price − 3 × ATR(14, Wilder); ratchets up, never down
- **Take profit:** Price ≥ 20-day high: exit
- **Trend exit:** QQQ < SMA(200): exit
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -49% | 0.886 | 94 | 76 | 1.24 | 2.19 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 137% | 🔴 -3% | 🔴 -6% | 🟢 76% | 🟢 54% | 🟢 14% | 🟢 84% | 🟢 49% | 🔴 -14% | 🟢 72% | 🟢 39% | 🟢 28% |

> [!code]- Click to view: 004.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/004.py"
> ```


---

## Strategy-5
### QQQ SMA(150) Trend → TQQQ (005.py)

**Description:** Holds 100% TQQQ when QQQ is above its 150-day SMA, otherwise moves to cash. A slight variant of the standard 200-day trend rule — uses 150 days for a faster regime signal on the underlying index.

*Overfit 2/10 — Single parameter: SMA 150. Slightly shorter than the canonical 200 but still a widely-used period. The period choice could be a minor fit to history.*

- **Entry:** QQQ > SMA(150): 100% TQQQ
- **Exit:** QQQ ≤ SMA(150): cash
- **Symbols:** Signal: QQQ. Execution: TQQQ
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -55% | 0.871 | 22 | 36 | 0.61 | 13.35 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 18% | 🔴 -5% | 🟢 118% | 🟢 1% | 🟢 53% | 🟢 97% | 🟢 88% | 🔴 -34% | 🟢 125% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: 005.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/005.py"
> ```


---

## Strategy-6
### TQQQ IBS Extreme + ATR Stop (006.py)

**Description:** Buys TQQQ when the Internal Bar Strength (IBS = (close−low)/(high−low)) is below 0.1, signaling a close near the day's low (capitulation). Exits when IBS exceeds 0.9 (close near day's high) or price falls below entry minus 3×ATR(14).

*Overfit 3/10 — Three parameters: IBS entry 0.1, IBS exit 0.9, ATR multiplier 3. IBS thresholds 0.1/0.9 are at the extreme ends of [0,1] and are standard for this type of reversal strategy. ATR multiplier 3 is conventional.*

- **Entry:** IBS = (close−low)/(high−low) < 0.1: 100% TQQQ
- **IBS exit:** IBS > 0.9: liquidate
- **Stop loss:** Close < entry price − 3 × ATR(14, Wilder): liquidate
- **Rebalance:** Daily, 45 min after market open (previous day's completed bar)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 46% | -43% | 1.049 | 271 | 106 | 2.56 | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 7% | 🟢 6% | 🟢 39% | 🟢 71% | 🔴 -29% | 🟢 33% | 🟢 344% | 🟢 75% | 🔴 -1% | 🟢 101% | 🟢 29% | 🟢 82% |

> [!code]- Click to view: 006.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/006.py"
> ```


---

## Strategy-7
### CMO(20) Momentum (008.py)

**Description:** Holds TQQQ when the 20-day Chande Momentum Oscillator on QQQ is positive (net up-moves exceed net down-moves) and switches to BIL otherwise. Only trades on regime change.

*Overfit 2/10 — Single momentum indicator at a standard period (20) with a zero-line threshold — minimal tuning.*

- **Entry:** CMO(20) > 0: 100% TQQQ
- **Exit:** CMO(20) ≤ 0: 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -50% | 0.834 | 112 | 131 | 0.85 | 3.02 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -10% | 🔴 -2% | 🟢 85% | 🔴 -8% | 🟢 85% | 🟢 169% | 🟢 40% | 🔴 -18% | 🟢 85% | 🟢 27% | 🟢 40% |

> [!code]- Click to view: 008.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/008.py"
> ```


---

## Strategy-8
### ROC(20) Zero Cross (009.py)

**Description:** Holds TQQQ when QQQ's 20-day rate of change is positive (today's close above close 20 days ago) and switches to BIL otherwise. Only trades on regime change.

*Overfit 2/10 — Single momentum indicator at a standard period (20) with a zero-line threshold — minimal tuning.*

- **Entry:** ROC(20) > 0: 100% TQQQ
- **Exit:** ROC(20) ≤ 0: 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -50% | 0.834 | 112 | 131 | 0.85 | 3.02 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -10% | 🔴 -2% | 🟢 85% | 🔴 -8% | 🟢 85% | 🟢 169% | 🟢 40% | 🔴 -18% | 🟢 85% | 🟢 27% | 🟢 40% |

> [!code]- Click to view: 009.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/009.py"
> ```


---

## Strategy-9
### Up-Day Count(20) (010.py)

**Description:** Holds TQQQ when more than half of the last 20 trading sessions closed higher than the previous day, and switches to BIL when down-days dominate. Only trades on regime change.

*Overfit 2/10 — Single breadth metric at a common lookback (20 days) with a natural majority threshold — minimal tuning.*

- **Entry:** Up-day count in last 20 sessions > 10: 100% TQQQ
- **Exit:** Up-day count ≤ 10: 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -53% | 0.792 | 98 | 129 | 0.76 | 3.31 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 43% | 🟢 6% | 🟢 3% | 🟢 58% | 🔴 -26% | 🟢 80% | 🟢 147% | 🟢 41% | 🟢 27% | 🟢 92% | 🟢 8% | 🔴 -3% |

> [!code]- Click to view: 010.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/010.py"
> ```


---

## Strategy-10
### TII(20) Trend Intensity (011.py)

**Description:** Holds TQQQ when more than half of the last 20 daily closes are above the 20-day SMA, indicating sustained trend participation, and switches to BIL otherwise. Only trades on regime change.

*Overfit 2/10 — Single indicator (TII, n=20) with canonical 50% threshold — minimal tuning.*

- **Entry:** TII(20) > 50%: 100% TQQQ
- **Exit:** TII(20) ≤ 50%: 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -45% | 0.695 | 302 | 193 | 1.56 | 1.09 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 21% | 🔴 -6% | 🟢 30% | 🟢 55% | 🟢 48% | 🟢 39% | 🟢 84% | 🟢 2% | 🟢 14% | 🔴 -2% | 🟢 34% | 🟢 59% |

> [!code]- Click to view: 011.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/011.py"
> ```


---

## Strategy-11
### Price 126D Percentile (012.py)

**Description:** Holds TQQQ when QQQ's current price is in the upper half of its 126-day (6-month) high-low range and switches to BIL otherwise. Only trades on regime change.

*Overfit 1/10 — Single price-position metric at a sensible lookback (126 days) with a natural midpoint threshold — minimal tuning.*

- **Entry:** Price percentile in 126-day range > 50%: 100% TQQQ
- **Exit:** Percentile ≤ 50%: 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -55% | 0.78 | 22 | 55 | 0.40 | 10.02 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 46% | 🟢 25% | 🔴 -5% | 🟢 118% | 🔴 -25% | 🟢 59% | 🟢 119% | 🟢 68% | 🔴 -41% | 🟢 86% | 🟢 26% | 🟢 52% |

> [!code]- Click to view: 012.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/012.py"
> ```


---

## Strategy-12
### Trend Stretch Exit (005.py)

**Description:** Trend following with mean-reversion "stretch" thresholds for exits.

*Overfit 3/10 — Specific stretch thresholds*

- **Trend gate:** QQQ close > SMA(200)
- **Entry:** QQQ > SMA(200) AND stretch = (price - SMA)/SMA < 5% → 100% TQQQ
- **Exit:** QQQ < SMA(200) OR stretch > 20% → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -56% | 0.925 | 49 | 80 | 0.61 | 8.62 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 70% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 96% | 🟢 92% | 🔴 -44% | 🟢 142% | 🟢 135% | 🟢 24% |

> [!code]- Click to view: 005.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/005.py"
> ```


---

## Strategy-13
### TQQQ Anti-Martingale Pyramid (006.py)

**Description:** Starts at 50% TQQQ when QQQ > SMA(200). For every 5% gain above the entry price, adds another 15% allocation until reaching 100%. Implements the 'let winners run / cut losers' principle — pyramiding into strength.

*Overfit 3/10 — Anti-Martingale is a textbook position-sizing scheme; tuned step (5% gain → +15% size).*

- **Trend gate:** QQQ > SMA(200)
- **Initial entry:** 50% TQQQ
- **Pyramid:** Each 5% gain above entry → +15% allocation, capped at 100%
- **Exit:** Trend break → liquidate all
- **Symbols:** Signal: QQQ. Execution: TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -51% | 0.715 | 120 | 70 | 1.71 | 4.25 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🔴 -6% | 🔴 -6% | 🟢 111% | 🔴 -5% | 🟢 35% | 🟢 83% | 🟢 88% | 🔴 -36% | 🟢 90% | 🟢 62% | 🟢 7% |

> [!code]- Click to view: 006.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/006.py"
> ```


---

## Strategy-14
### Donchian-200 Midline (013.py)

**Description:** A trend follower using the midpoint of the 200-day Donchian channel (average of the 200-day high and 200-day low) as a dynamic trend filter. When QQQ price is above this midline it holds TQQQ; below it holds BIL.

*Overfit 2/10 — Single Donchian midline at 200 days — a textbook period applied to the midpoint instead of the breakout levels. Very low overfit.*

- **Trend gate:** QQQ price > (200d high + 200d low) / 2
- **Entry:** QQQ > Donchian-200 midline → 100% TQQQ
- **Exit:** QQQ ≤ Donchian-200 midline → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -57% | 0.796 | 34 | 51 | 0.67 | 9.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 22% | 🔴 -5% | 🟢 118% | 🔴 -19% | 🟢 80% | 🟢 97% | 🟢 88% | 🔴 -47% | 🟢 93% | 🟢 62% | 🟢 20% |

> [!code]- Click to view: 013.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/013.py"
> ```


---

## Strategy-15
### ROC+D200 + 7% Trail Exit (015.py)

**Description:** Enters TQQQ when both ROC(20) and Donchian-200 are bullish, with a trailing drawdown exit: closes if QQQ falls more than 7% below its 20-day high, even if the longer-term trend signal remains intact.

*Overfit 3/10 — Standard ROC(20)>0 and Donchian-200 entry conditions. The 7% trailing drawdown from 20-day high is a non-canonical threshold — the specific percentage is tuned.*

- **Trend gate:** ROC(20)>0 on QQQ AND QQQ > Donchian-200 midline
- **Entry:** Both conditions true AND QQQ within 7% of 20-day high → 100% TQQQ
- **Exit:** Trend signal turns off OR QQQ drops >7% below 20-day high → 100% BIL
- **Stop-loss:** Trailing: exit if QQQ falls >7% from its 20-day high
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -43% | 0.794 | 193 | 256 | 0.75 | 3.27 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -11% | 🔴 -2% | 🟢 85% | 🔴 -15% | 🟢 66% | 🟢 185% | 🟢 39% | 🔴 -19% | 🟢 56% | 🟢 23% | 🟢 42% |

> [!code]- Click to view: 015.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/015.py"
> ```


---

## Strategy-16
### TQQQ Pyramid (10%/day) (016.py)

**Description:** A pyramiding trend follower that gradually scales into TQQQ by adding 10% exposure per day while both ROC(20) and Donchian-200 remain bullish, reaching 100% after ten consecutive bull days. Exits entirely to BIL on the first bear signal.

*Overfit 4/10 — Key tuned parameter: the 10% daily increment rate (requiring 10 consecutive bull days for full exposure). Also uses standard ROC(20)>0 and Donchian-200. The pyramid step rate is non-canonical.*

- **Trend gate:** ROC(20)>0 on QQQ AND QQQ > Donchian-200 midline
- **Entry:** Bull: +10% TQQQ per day (up to 100%); remainder in BIL
- **Exit:** Bear signal → TQQQ to 0%, 100% BIL immediately
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -43% | 0.814 | 741 | 711 | 1.04 | 3.24 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 22% | 🔴 -9% | 🟢 4% | 🟢 51% | 🔴 -7% | 🟢 64% | 🟢 118% | 🟢 27% | 🔴 -9% | 🟢 45% | 🟢 52% | 🟢 46% |

> [!code]- Click to view: 016.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/016.py"
> ```


---

## Strategy-17
### Range Expanded 110% (025.py)

**Description:** A volatility-expansion trend follower that enters TQQQ when QQQ's recent 25-day average range exceeds 110% of the 200-day average, indicating elevated volatility, combined with a median trend gate.

*Overfit 3/10 — The 110% threshold inverts the compression logic; it is one step in a family of threshold sweeps. Elevated volatility entry is a non-standard signal direction. Moderate tuning.*

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

> [!code]- Click to view: 025.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/025.py"
> ```


---

## Strategy-18
### MFI14_Hyst (032.py)

**Description:** Applies a 14-period Money Flow Index on QQQ with hysteresis bands to reduce whipsaw. Enters TQQQ when buying pressure dominates (MFI > 60), exits to BIL when selling pressure takes over (MFI < 40), holds current position in the neutral zone.

*Overfit 2/10 — Single volume-price indicator at a standard period (14); 60/40 hysteresis bands are common textbook levels for MFI — minimal tuning.*

- **Entry:** MFI(14) > 60: 100% TQQQ
- **Exit:** MFI(14) < 40: 100% BIL
- **Hold:** 40 ≤ MFI(14) ≤ 60 — no change
- **Symbols:** Signal & Execution: QQQ / TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -44% | 0.783 | 110 | 73 | 1.51 | 2.44 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -11% | 🟢 2% | 🟢 11% | 🟢 71% | 🟢 8% | 🟢 120% | 🟢 121% | 🟢 29% | 🔴 -20% | 🟢 41% | 🟢 36% | 🟢 40% |

> [!code]- Click to view: 032.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/032.py"
> ```


---

## Strategy-19
### Full Ensemble (ultAlgo) (ultAlgo.py)

**Description:** Equal-weight ensemble of 19 sub-algos: LeveragedRebalance, RSIDipChampion, TQQQDynamic, ExpandingBreakout, TQQQSMA150, IBSATRStop, MktCapIBSRegime, CMO20, ROC20, UpDay20, TII20, Price126D, TrendStretchExit, AntiMartingale, Donchian200Midline, ROCD200Trail, TQQQPyramid, RangeExpanded, and MFI14Hyst. Sub-algo equities start equal and drift with performance; reset annually.

*Overfit N/A — Ensemble of independently-designed strategies. No combined parameter tuning.*

- **Components:** LeveragedRebalance, RSIDipChampion, TQQQDynamic, ExpandingBreakout, TQQQSMA150, IBSATRStop, MktCapIBSRegime, CMO20, ROC20, UpDay20, TII20, Price126D, TrendStretchExit, AntiMartingale, Donchian200Midline, ROCD200Trail, TQQQPyramid, RangeExpanded, MFI14Hyst
- **Weighting:** Equal virtual equity split at start; aggregated proportionally each day
- **Rebalance:** Daily, 45 min after market open (SPY)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -33% | 0.982 | 3791 | 2324 | 1.63 | 1.83 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 36% | 🟢 3% | 🟢 1% | 🟢 85% | 🔴 -3% | 🟢 59% | 🟢 120% | 🟢 59% | 🔴 -18% | 🟢 83% | 🟢 45% | 🟢 36% |

> [!code]- Click to view: ultAlgo.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/ultAlgo.py"
> ```


---
