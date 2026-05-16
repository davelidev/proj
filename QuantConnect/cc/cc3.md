# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [3](#strategy-3)     | ✅    | Trend           | 30%  | -55%  | 0.74   | 99    | 78    | 1.27     | 2.68         | 2/10   |
| [19](#strategy-19)   | ✅    | Trend           | 37%  | -57%  | 0.796  | 34    | 51    | 0.67     | 9.51         | 2/10   |
| [21](#strategy-21)   | ✅    | Trend           | 31%  | -52%  | 0.715  | 80    | 97    | 0.82     | 4.60         | 2/10   |
| [28](#strategy-28)   | ✅    | Trend           | 37%  | -57%  | 0.796  | 34    | 51    | 0.67     | 9.51         | 3/10   |
| [43](#strategy-43)   | ✅    | Trend           | 32%  | -49%  | 0.798  | 250   | 153   | 1.63     | 1.82         | 3/10   |
| [45](#strategy-45)   | ✅    | Rotation        | 32%  | -57%  | 0.772  | 209   | 122   | 1.71     | 1.23         | 3/10   |
| [46](#strategy-46)   | ✅    | Trend           | 34%  | -55%  | 0.79   | 270   | 133   | 2.03     | 1.55         | 3/10   |
| [47](#strategy-47)   | ✅    | Trend           | 30%  | -43%  | 0.787  | 222   | 181   | 1.23     | 2.30         | 3/10   |
| [48](#strategy-48)   | ✅    | Rotation        | 37%  | -58%  | 0.836  | 259   | 146   | 1.77     | 1.47         | 4/10   |
| [49](#strategy-49)   | ✅    | Trend           | 29%  | -50%  | 0.749  | 279   | 210   | 1.33     | 1.92         | 3/10   |


---
## Strategy-3
### Aroon(25) Trend (cc3_003.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -55% | 0.74 | 99 | 78 | 1.27 | 2.68 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 15% | 🟢 17% | 🔴 -6% | 🟢 76% | 🟢 14% | 🟢 56% | 🟢 87% | 🟢 52% | 🔴 -40% | 🟢 80% | 🟢 32% | 🟢 49% |

> [!code]- Click to view: cc3_003.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_003.py"
> ```


---

## Strategy-19
### Donchian-200 Midline (cc3_019.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -57% | 0.796 | 34 | 51 | 0.67 | 9.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 22% | 🔴 -5% | 🟢 118% | 🔴 -19% | 🟢 80% | 🟢 97% | 🟢 88% | 🔴 -47% | 🟢 93% | 🟢 62% | 🟢 20% |

> [!code]- Click to view: cc3_019.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_019.py"
> ```


---

## Strategy-21
### Donchian-100 Midline (cc3_021.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -52% | 0.715 | 80 | 97 | 0.82 | 4.60 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 2% | 🟢 32% | 🔴 -15% | 🟢 118% | 🔴 -28% | 🟢 64% | 🟢 131% | 🟢 54% | 🔴 -50% | 🟢 137% | 🟢 26% | 🟢 59% |

> [!code]- Click to view: cc3_021.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_021.py"
> ```


---

## Strategy-28
### Donchian-200 + Drawdown Stop (cc3_029.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -57% | 0.796 | 34 | 51 | 0.67 | 9.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 22% | 🔴 -5% | 🟢 118% | 🔴 -19% | 🟢 80% | 🟢 97% | 🟢 88% | 🔴 -47% | 🟢 93% | 🟢 62% | 🟢 20% |

> [!code]- Click to view: cc3_029.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_029.py"
> ```


---

## Strategy-43
### 3-State TQQQ Sizing (cc3_044.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -49% | 0.798 | 250 | 153 | 1.63 | 1.82 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🔴 -1% | 🔴 -1% | 🟢 89% | 🔴 -19% | 🟢 68% | 🟢 101% | 🟢 63% | 🔴 -44% | 🟢 126% | 🟢 50% | 🟢 33% |

> [!code]- Click to view: cc3_044.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_044.py"
> ```


---

## Strategy-45
### Aroon-TQQQ / Top-1 Defense (cc3_046.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -57% | 0.772 | 209 | 122 | 1.71 | 1.23 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 39% | 🔴 -11% | 🟢 10% | 🟢 87% | 🔴 -25% | 🟢 90% | 🟢 134% | 🟢 56% | 🔴 -53% | 🟢 181% | 🟢 47% | 🟢 13% |

> [!code]- Click to view: cc3_046.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_046.py"
> ```


---

## Strategy-46
### 3-State 70/30 Middle (cc3_047.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -55% | 0.79 | 270 | 133 | 2.03 | 1.55 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 42% | 🟢 8% | 🔴 -2% | 🟢 100% | 🔴 -18% | 🟢 77% | 🟢 101% | 🟢 73% | 🔴 -51% | 🟢 123% | 🟢 55% | 🟢 28% |

> [!code]- Click to view: cc3_047.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_047.py"
> ```


---

## Strategy-47
### 3-State 30/70 Middle (cc3_048.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -43% | 0.787 | 222 | 181 | 1.23 | 2.30 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 24% | 🔴 -10% | 🔴 -1% | 🟢 79% | 🔴 -19% | 🟢 59% | 🟢 100% | 🟢 54% | 🔴 -36% | 🟢 128% | 🟢 45% | 🟢 38% |

> [!code]- Click to view: cc3_048.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_048.py"
> ```


---

## Strategy-48
### Graceful TQQQ/Top-1 Step-Down (cc3_049.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -58% | 0.836 | 259 | 146 | 1.77 | 1.47 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 57% | 🟢 8% | 🟢 5% | 🟢 102% | 🔴 -24% | 🟢 93% | 🟢 147% | 🟢 71% | 🔴 -54% | 🟢 151% | 🟢 52% | 🟢 13% |

> [!code]- Click to view: cc3_049.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_049.py"
> ```


---

## Strategy-49
### 3-State Aroon-25 + Donchian-100 (cc3_050.py)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -50% | 0.749 | 279 | 210 | 1.33 | 1.92 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 8% | 🟢 3% | 🔴 -7% | 🟢 89% | 🔴 -23% | 🟢 61% | 🟢 115% | 🟢 50% | 🔴 -45% | 🟢 150% | 🟢 34% | 🟢 52% |

> [!code]- Click to view: cc3_050.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_050.py"
> ```


---
