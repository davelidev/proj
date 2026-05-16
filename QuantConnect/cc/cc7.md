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
