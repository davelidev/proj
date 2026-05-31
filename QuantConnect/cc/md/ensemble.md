# ensemble

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [1](#strategy-1)     | ✅    | Buy & Hold      | 28%  | -51%  | 0.727  | 12    | 0     | —        | —            |        |
| [2](#strategy-2)     | ✅    | Mean Reversion  | 46%  | -43%  | 1.049  | 271   | 106   | 2.56     | 0.96         |        |
| [3](#strategy-3)     | ✅    | Mean Reversion  | 45%  | -35%  | 1.019  | —     | —     | —        | 0.96         |        |
| [4](#strategy-4)     | ✅    | Breakout        | 38%  | -49%  | 0.886  | 94    | 76    | 1.24     | 2.19         |        |
| [5](#strategy-5)     | ✅    | Trend Following | 29%  | -45%  | 0.705  | —     | —     | —        | 1.45         |        |
| [6](#strategy-6)     | ✅    | Trend Following | 40%  | -55%  | 0.871  | 22    | 36    | 0.61     | 13.35        |        |
| [7](#strategy-7)     | ✅    | Trend           | 30%  | -51%  | 0.715  | 120   | 70    | 1.71     | 4.25         |        |
| [8](#strategy-8)     | ✅    | Trend Following | 29%  | -45%  | 0.709  | 368   | 255   | 1.44     | 1.66         |        |
| [9](#strategy-9)     | ✅    | Trend           | 32%  | -52%  | 0.738  | 166   | 126   | 1.32     | 2.20         |        |
| [10](#strategy-10)   | ✅    | Trend           | 35%  | -36%  | 0.927  | —     | —     | —        | 1.34         |        |
| [11](#strategy-11)   | ✅    | Mean Reversion  | 40%  | -56%  | 0.925  | 49    | 80    | 0.61     | 8.62         |        |
| [12](#strategy-12)   | ✅    | Trend           | 43%  | -56%  | 0.891  | —     | —     | —        | 2.34         |        |
| [13](#strategy-13)   | ✅    | Range           | 34%  | -41%  | 0.824  | 136   | 91    | 1.49     | 3.23         |        |
| [14](#strategy-14)   | ✅    | Volume          | 31%  | -44%  | 0.783  | 110   | 73    | 1.51     | 2.44         |        |
| [15](#strategy-15)   | ✅    | Ensemble        | 38%  | -39%  | 0.973  | —     | —     | —        | 1.57         |        |


---
## Strategy-1
### TQQQ 60% Annual Rebalance (001.py)

- **Allocation:** 60% TQQQ at all times
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
### TQQQ/SOXL/TECL Basket IBS Extreme + ATR Stop (002.py)

- **Entry:** TQQQ IBS = (close−low)/(high−low) < 0.1: equal-weight 33% TQQQ + 33% SOXL + 33% TECL
- **IBS exit:** TQQQ IBS > 0.9: liquidate basket
- **Stop loss:** TQQQ close < entry price − 3 × ATR(14, Wilder): liquidate basket
- **Symbols:** Signal & ATR: TQQQ. Execution: TQQQ / SOXL / TECL

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 46% | -43% | 1.049 | 271 | 106 | 2.56 | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 7% | 🟢 6% | 🟢 39% | 🟢 71% | 🔴 -29% | 🟢 33% | 🟢 344% | 🟢 75% | 🔴 -1% | 🟢 101% | 🟢 29% | 🟢 82% |

> [!code]- Click to view: 002.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/002.py"
> ```

---
## Strategy-3
### RSI(2) 3-Vote Dip → Basket (003.py)

- **Signal:** Count n = # of RSI(2, Wilder) thresholds breached: <20, <25, <30
- **Position:** Total weight = n / 3 split equally across TQQQ / SOXL / TECL
- **Symbols:** Signal: QQQ. Execution: TQQQ / SOXL / TECL

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 45% | -35% | 1.019 | — | — | — | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 32% | 🟢 2% | 🔴 -18% | 🟢 51% | 🟢 8% | 🟢 52% | 🟢 138% | 🟢 131% | 🟢 27% | 🟢 66% | 🟢 74% | 🟢 54% |

> [!code]- Click to view: 003.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/003.py"
> ```

---
## Strategy-4
### TQQQ Expanding Range Breakout + ATR Trailing Stop (004.py)

- **Entry:** All three must hold: QQQ above SMA(200), yesterday's range wider than the day before, ADX(10) > 25 → 100% TQQQ
- **Trailing stop:** Stop = Price − 3 × ATR(14, Wilder); only ratchets up
- **Take profit:** TQQQ hits new 20-day high → exit
- **Trend exit:** QQQ breaks below SMA(200) → exit

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
### TQQQ Dynamic Sizing: SMA200 + RSI Tiers (005.py)

- **Regime gate:** TQQQ > SMA(200): active; else 0% (cash)
- **Dip entry:** RSI(2, Wilder) < 30: 100% TQQQ
- **Overbought trim:** RSI(14, Wilder) > 70: 20% TQQQ
- **Default:** 50% TQQQ when in regime with no RSI signal

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -45% | 0.705 | — | — | — | 1.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 31% | 🟢 2% | 🔴 -15% | 🟢 111% | 🟢 5% | 🟢 21% | 🟢 55% | 🟢 87% | 🔴 -21% | 🟢 64% | 🟢 38% | 🟢 33% |

> [!code]- Click to view: 005.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/005.py"
> ```

---
## Strategy-6
### QQQ SMA(150) Trend → TQQQ (006.py)

- **Entry:** QQQ > SMA(150): 100% TQQQ
- **Exit:** QQQ ≤ SMA(150): cash
- **Symbols:** Signal: QQQ. Execution: TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -55% | 0.871 | 22 | 36 | 0.61 | 13.35 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 18% | 🔴 -5% | 🟢 118% | 🟢 1% | 🟢 53% | 🟢 97% | 🟢 88% | 🔴 -34% | 🟢 125% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: 006.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/006.py"
> ```

---
## Strategy-7
### TQQQ Anti-Martingale Pyramid (007.py)

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

> [!code]- Click to view: 007.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/007.py"
> ```

---
## Strategy-8
### QQQ 5-SMA Vote → TQQQ (008.py)

- **Position:** n/5 TQQQ where n = # of SMA(20,50,100,150,200) that QQQ price exceeds
- **Exit:** Partial or full exit as SMAs are lost on the way down
- **Symbols:** Signal: QQQ. Execution: TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -45% | 0.709 | 368 | 255 | 1.44 | 1.66 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 23% | 🔴 -6% | 🔴 -7% | 🟢 95% | 🔴 -7% | 🟢 44% | 🟢 100% | 🟢 48% | 🔴 -39% | 🟢 122% | 🟢 35% | 🟢 35% |

> [!code]- Click to view: 008.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/008.py"
> ```

---
## Strategy-9
### QQQ Donchian 4-Vote → TQQQ (009.py)

- **Signal:** Count n = # of Donchian midlines (50d, 100d, 150d, 200d) that QQQ price exceeds
- **Position:** TQQQ weight = n / 4 (0%, 25%, 50%, 75%, or 100%)
- **Midline:** Donchian midline = (N-day high + N-day low) / 2
- **Symbols:** Signal: QQQ. Execution: TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -52% | 0.738 | 166 | 126 | 1.32 | 2.20 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 23% | 🟢 16% | 🔴 -10% | 🟢 114% | 🔴 -27% | 🟢 63% | 🟢 116% | 🟢 60% | 🔴 -45% | 🟢 112% | 🟢 45% | 🟢 44% |

> [!code]- Click to view: 009.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/009.py"
> ```

---
## Strategy-10
### QQQ 3-Vote → TQQQ (010.py)

- **Signal 1:** ROC(20) > 0: today close > close 20 days ago
- **Signal 2:** UpDay(20): >10 of last 20 day-to-day changes are positive
- **Signal 3:** TII(20): >10 of last 20 closes are above SMA(20)
- **Position:** TQQQ weight = n / 3 (0%, 33%, 67%, or 100%)
- **Symbols:** Signal: QQQ. Execution: TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -36% | 0.927 | — | — | — | 1.34 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 32% | 🔴 -2% | 🟢 12% | 🟢 67% | 🟢 3% | 🟢 69% | 🟢 139% | 🟢 29% | 🟢 12% | 🟢 55% | 🟢 24% | 🟢 32% |

> [!code]- Click to view: 010.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/010.py"
> ```

---
## Strategy-11
### Trend Stretch Exit (011.py)

- **Trend gate:** QQQ close > SMA(200)
- **Entry:** QQQ > SMA(200) AND stretch = (price - SMA)/SMA < 5% → 100% TQQQ
- **Exit:** QQQ < SMA(200) OR stretch > 20% → 100% cash
- **Symbols:** Signal: QQQ. Execution: TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -56% | 0.925 | 49 | 80 | 0.61 | 8.62 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 70% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 96% | 🟢 92% | 🔴 -44% | 🟢 142% | 🟢 135% | 🟢 24% |

> [!code]- Click to view: 011.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/011.py"
> ```

---
## Strategy-12
### QQQ Golden Cross + 3×ATR Trail → TQQQ (012.py)

- **Entry:** EMA(50) of QQQ > EMA(200) of QQQ → 100% TQQQ
- **Trailing stop:** Stop = TQQQ price − 3 × ATR(14, Wilder); only ratchets up
- **Exit:** Stop hit OR EMA(50) ≤ EMA(200)
- **Symbols:** Signal: QQQ. Execution: TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 43% | -56% | 0.891 | — | — | — | 2.34 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 44% | 🟢 28% | 🟢 1% | 🟢 96% | 🟢 9% | 🟢 68% | 🟢 204% | 🟢 62% | 🔴 -25% | 🟢 97% | 🟢 61% | 🔴 -7% |

> [!code]- Click to view: 012.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/012.py"
> ```

---
## Strategy-13
### Range Expanded 110% (013.py)

- **Trend gate:** QQQ close > median of last 200 daily closes
- **Strength filter:** Avg daily range (last 25 days) > 110% of avg daily range (last 200 days)
- **Entry:** Both conditions true → 100% TQQQ
- **Exit:** One condition true → 50% TQQQ / 50% cash; neither true → 100% cash
- **Symbols:** Signal: QQQ. Execution: TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -41% | 0.824 | 136 | 91 | 1.49 | 3.23 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 23% | 🟢 6% | 🔴 -10% | 🟢 99% | 🟢 1% | 🟢 63% | 🟢 109% | 🟢 62% | 🔴 -34% | 🟢 135% | 🟢 56% | 🟢 8% |

> [!code]- Click to view: 013.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/013.py"
> ```

---
## Strategy-14
### MFI14_Hyst (014.py)

- **Entry:** MFI(14) > 60: 100% TQQQ
- **Exit:** MFI(14) < 40: 100% cash
- **Hold:** 40 ≤ MFI(14) ≤ 60 — no change
- **Symbols:** Signal & Execution: QQQ / TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -44% | 0.783 | 110 | 73 | 1.51 | 2.44 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -11% | 🟢 2% | 🟢 11% | 🟢 71% | 🟢 8% | 🟢 120% | 🟢 121% | 🟢 29% | 🔴 -20% | 🟢 41% | 🟢 36% | 🟢 40% |

> [!code]- Click to view: 014.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/014.py"
> ```

---
## Strategy-15
### Full Ensemble (ultAlgo) (ultAlgo.py)

- **Components:** LeveragedRebalance, IBSATRStop, RSIThreeVote, ExpandingBreakout, TQQQDynamic, TQQQSMA150, AntiMartingale, SMAFiveVote, DonchianFourVote, ThreeVote, TrendStretchExit, GoldenCrossATR, RangeExpanded, MFI14Hyst (14 sub-algos)
- **Weighting:** Equal virtual equity split at start; aggregated proportionally each day, reset annually

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -39% | 0.973 | — | — | — | 1.57 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 38% | 🟢 5% | 🔴 -1% | 🟢 93% | 🔴 -3% | 🟢 57% | 🟢 119% | 🟢 73% | 🔴 -25% | 🟢 99% | 🟢 52% | 🟢 34% |

> [!code]- Click to view: ultAlgo.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/utils/ultAlgo.py"
> ```

---