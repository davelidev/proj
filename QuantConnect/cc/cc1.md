# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [1](#strategy-1)     | ❌    | Breakout        | 26%  | -36%  | 0.754  | 1009  | 1645  | 0.61     | 2.14         | 4/10   |
| [2](#strategy-2)     | ✅    | Breakout        | 41%  | -50%  | 0.916  | 119   | 93    | 1.28     | 2.49         | 6/10   |
| [3](#strategy-3)     | ✅    | Breakout        | 39%  | -51%  | 0.862  | 78    | 69    | 1.13     | 2.45         | 6/10   |
| [4](#strategy-4)     | ✅    | Breakout        | 39%  | -50%  | 0.859  | 81    | 66    | 1.23     | 2.34         | 5/10   |
| [5](#strategy-5)     | ✅    | Breakout        | 36%  | -50%  | 0.851  | 81    | 67    | 1.21     | 2.32         | 5/10   |
| [6](#strategy-6)     | ✅    | Breakout        | 31%  | -57%  | 0.723  | 92    | 109   | 0.84     | 2.41         | 3/10   |
| [7](#strategy-7)     | ✅    | Dip Buy         | 39%  | -28%  | 1.335  | 1160  | 681   | 1.70     | 1.30         | 7/10   |
| [8](#strategy-8)     | ✅    | Dip Buy         | 36%  | -52%  | 0.817  | 10    | 25    | 0.40     | 23.67        | 6/10   |
| [9](#strategy-9)     | ✅    | Dip Buy         | 32%  | -50%  | 0.772  | 57    | 24    | 2.38     | 1.45         | 5/10   |
| [10](#strategy-10)   | ✅    | Rotation        | 95%  | -56%  | 1.52   | 100   | 85    | 1.18     | 4.51         | 7/10   |
| [11](#strategy-11)   | ✅    | Mean Reversion  | 31%  | -55%  | 0.844  | 39    | 34    | 1.15     | 2.59         | 3/10   |
| [12](#strategy-12)   | ❌    | Mean Reversion  | 27%  | -44%  | 0.835  | 452   | 254   | 1.78     | 1.22         | 2/10   |
| [13](#strategy-13)   | ❌    | Momentum        | 27%  | -37%  | 0.788  | 98    | 51    | 1.92     | 3.35         | 4/10   |
| [14](#strategy-14)   | ✅    | Rotation        | 54%  | -24%  | 1.339  | 305   | 172   | 1.77     | 2.74         | 7/10   |
| [15](#strategy-15)   | ✅    | Rotation        | 54%  | -24%  | 1.339  | 305   | 172   | 1.77     | 2.74         | 7/10   |
| [16](#strategy-16)   | ✅    | Rotation        | 95%  | -56%  | 1.52   | 100   | 85    | 1.18     | 4.51         | 6/10   |
| [17](#strategy-17)   | ✅    | Rotation        | 38%  | -54%  | 0.818  | 220   | 228   | 0.96     | 1.98         | 6/10   |
| [18](#strategy-18)   | ✅    | Dip Buy         | 50%  | -37%  | 1.076  | 1440  | 588   | 2.45     | 0.81         | 3/10   |
| [19](#strategy-19)   | ✅    | Trend           | 158% | -56%  | 2.224  | 276   | 119   | 2.32     | 1.67         | 7/10   |
| [20](#strategy-20)   | ✅    | Trend           | 28%  | -50%  | 0.825  | 37    | 20    | 1.85     | 2.45         | 2/10   |
| [21](#strategy-21)   | ✅    | Trend           | 31%  | -49%  | 0.738  | 100   | 47    | 2.13     | 1.44         | 4/10   |
| [22](#strategy-22)   | ✅    | Rebalance       | 37%  | -52%  | 0.848  | 38    | 0     | —        | —            | 4/10   |
| [23](#strategy-23)   | ✅    | Trend           | 33%  | -56%  | 0.753  | 10    | 47    | 0.21     | 28.85        | 1/10   |
| [24](#strategy-24)   | ✅    | Trend           | 40%  | -55%  | 0.871  | 21    | 36    | 0.58     | 14.75        | 2/10   |
| [25](#strategy-25)   | ✅    | Trend           | 33%  | -50%  | 0.76   | 18    | 41    | 0.44     | 16.03        | 1/10   |
| [26](#strategy-26)   | ✅    | Trend           | 29%  | -53%  | 0.692  | 24    | 59    | 0.41     | 10.03        | 3/10   |
| [27](#strategy-27)   | ✅    | Trend           | 29%  | -49%  | 0.703  | 10    | 47    | 0.21     | 28.86        | 2/10   |
| [28](#strategy-28)   | ✅    | Mean Reversion  | 35%  | -50%  | 0.817  | 498   | 245   | 2.03     | 0.85         | 2/10   |
| [29](#strategy-29)   | ✅    | Rotation        | 33%  | -55%  | 0.829  | 569   | 49    | 11.61    | 1.89         | 2/10   |
| [30](#strategy-30)   | ✅    | Mean Reversion  | 47%  | -47%  | 1.05   | 269   | 100   | 2.69     | 1.00         | 3/10   |
| [31](#strategy-31)   | ✅    | Mean Reversion  | 37%  | -42%  | 0.843  | 361   | 162   | 2.23     | 0.88         | 5/10   |
| [32](#strategy-32)   | ✅    | Mean Reversion  | 32%  | -40%  | 0.903  | 214   | 79    | 2.71     | 0.97         | 3/10   |
| [33](#strategy-33)   | ✅    | Mean Reversion  | 46%  | -43%  | 1.049  | 271   | 106   | 2.56     | 0.96         | 3/10   |
| [34](#strategy-34)   | ✅    | Mean Reversion  | 31%  | -47%  | 0.791  | 170   | 60    | 2.83     | 0.96         | 2/10   |
| [35](#strategy-35)   | ✅    | Mean Reversion  | 36%  | -35%  | 0.915  | 328   | 141   | 2.33     | 0.96         | 2/10   |
| [36](#strategy-36)   | ✅    | Mean Reversion  | 39%  | -55%  | 0.917  | 237   | 92    | 2.58     | 0.98         | 4/10   |
| [37](#strategy-37)   | ✅    | Mean Reversion  | 30%  | -52%  | 0.799  | 295   | 166   | 1.78     | 1.04         | 5/10   |
| [38](#strategy-38)   | ✅    | Trend/MR Hybrid | 50%  | -56%  | 0.986  | 52    | 45    | 1.16     | 5.27         | 5/10   |
| [39](#strategy-39)   | ✅    | Trend/MR Hybrid | 51%  | -55%  | 1.002  | 57    | 44    | 1.30     | 4.54         | 7/10   |
| [40](#strategy-40)   | ✅    | Trend/MR Hybrid | 51%  | -58%  | 1.01   | 57    | 44    | 1.30     | 4.53         | 3/10   |
| [41](#strategy-41)   | ✅    | Mean Reversion  | 55%  | -55%  | 1.068  | 62    | 49    | 1.27     | 4.76         | 2/10   |
| [42](#strategy-42)   | ✅    | Trend/MR Hybrid | 52%  | -56%  | 1.027  | 77    | 60    | 1.28     | 2.77         | 4/10   |
| [43](#strategy-43)   | ✅    | Trend/MR Hybrid | 40%  | -40%  | 1.018  | 69    | 46    | 1.50     | 3.88         | 1/10   |
| [44](#strategy-44)   | ✅    | Mean Reversion  | 40%  | -42%  | 0.912  | 242   | 90    | 2.69     | 0.95         | 7/10   |
| [45](#strategy-45)   | ✅    | Trend           | 33%  | -50%  | 0.76   | 18    | 41    | 0.44     | 16.03        | 4/10   |
| [46](#strategy-46)   | ✅    | Trend/MR Hybrid | 51%  | -56%  | 0.996  | 55    | 50    | 1.10     | 5.92         | 8/10   |
| [47](#strategy-47)   | ✅    | Trend/MR Hybrid | 49%  | -50%  | 0.988  | 69    | 58    | 1.19     | 4.69         | 6/10   |
| [48](#strategy-48)   | ✅    | Trend           | 29%  | -53%  | 0.692  | 24    | 59    | 0.41     | 10.03        | 6/10   |
| [49](#strategy-49)   | ✅    | Trend/MR Hybrid | 30%  | -23%  | 1.073  | 828   | 650   | 1.27     | 2.07         | 3/10   |
| [50](#strategy-50)   | ✅    | Trend/MR Hybrid | 49%  | -48%  | 0.991  | 71    | 58    | 1.22     | 4.32         | 4/10   |
| [51](#strategy-51)   | ✅    | Rotation        | 30%  | -52%  | 0.799  | 295   | 166   | 1.78     | 1.04         | 5/10   |
| [52](#strategy-52)   | ✅    | Rotation        | 40%  | -40%  | 1.018  | 69    | 46    | 1.50     | 3.88         | 6/10   |
| [53](#strategy-53)   | ❌    | Mean Reversion  | 22%  | -40%  | 0.74   | 520   | 27    | 19.26    | 1.50         | 2/10   |
| [54](#strategy-54)   | ✅    | Momentum        | 49%  | -50%  | 0.988  | 69    | 58    | 1.19     | 4.69         | 5/10   |


---
## Strategy-1
### Volatility Squeeze Alpha (z_gold_oil_breakout.py)

**Description:** Volatility squeeze breakout strategy applied to Gold and Oil CFDs. Uses Bollinger Bands and Keltner Channels to identify "squeezes" before explosive moves.

*Overfit 4/10 — BB/KC squeeze is a documented and widely-used pattern; four indicators each with clear roles; ATR trailing stop uses a standard multiplier; primary concern is the non-standard asset pairing (Gold + Oil CFDs) which limits historical depth.*

- **Squeeze:** BB inside KC
- **Entry:** Squeeze breakout AND Price > EMA
- **Exit:** ATR-based trailing stop or time-based
- **Symbols:** XAUUSD (Gold), WTICOUSD (Oil)
- **Resolution:** Hour

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 26% | -36% | 0.754 | 1009 | 1645 | 0.61 | 2.14 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -15% | 🔴 -13% | 🟢 1% | 🟢 19% | 🟢 15% | 🔴 -8% | 🟢 108% | 🟢 10% | 🟢 51% | 🟢 55% | 🟢 56% | 🟢 97% |

> [!code]- Click to view: z_gold_oil_breakout.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/z_gold_oil_breakout.py"
> ```


---

## Strategy-2
### Research S38 - Vol Expansion + SOXL/TQQQ + VIX Shield (strategy_38.py)

**Description:** Expanding Volatility + SOXL/TQQQ Momentum Rotation + VIX/VIX3M Structural Shield.

*Overfit 6/10 — three stacked components (vol expansion, LETF momentum rotation, VIX/VIX3M ratio filter) each with separate thresholds; the VIX3M/VIX ratio is a non-standard metric; LETF asset selection (SOXL/TQQQ) carries hindsight bias.*

- **Gate:** QQQ > SMA(200) AND VIX/VIX3M < 1.10
- **Entry:** Expanding Range AND ADX(10) > 25 → TQQQ; ADX > 30 AND SOXL momentum > TQQQ → SOXL
- **Exit:** 3.0 ATR trailing stop OR QQQ < SMA(200) OR VIX/VIX3M > 1.10
- **Symbols:** TQQQ, SOXL (signal from QQQ, VIX, VIX3M)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 41% | -50% | 0.916 | 119 | 93 | 1.28 | 2.49 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 115% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 13% | 🟢 16% | 🟢 184% | 🟢 95% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% |

> [!code]- Click to view: strategy_38.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/strategy_38.py"
> ```


---

## Strategy-3
### Research S36 - Triple-LETF Rotator + Expanding Range (strategy_36.py)

**Description:** Triple-LETF Rotator (TQQQ/SOXL/TECL) with Expanding Range momentum logic.

*Overfit 6/10 — LETF trio selection (TQQQ/SOXL/TECL) carries hindsight bias as these were the decade's top performers; expanding range momentum adds non-standard breakout width parameters; this is a refined iteration of S38, indicating active tuning.*

- **Gate:** QQQ > SMA(200)
- **Entry:** Expanding Range AND ADX(10) > 25 → TQQQ; ADX > 30 → highest momentum of TQQQ/SOXL/TECL
- **Exit:** 3.0 ATR trailing stop OR QQQ < SMA(200)
- **Symbols:** TQQQ, SOXL, TECL (signal from QQQ)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -51% | 0.862 | 78 | 69 | 1.13 | 2.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 141% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 27% | 🟢 17% | 🟢 71% | 🟢 115% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% |

> [!code]- Click to view: strategy_36.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/strategy_36.py"
> ```


---

## Strategy-4
### Research S35 - Expanding Strong Trend + SOXL + ADX (strategy_35.py)

**Description:** Expanding Strong Trend logic with dynamic SOXL rotation and ADX filters.

*Overfit 5/10 — the expanding trend base is well-defined but the specific ADX threshold and SOXL rotation trigger condition look iteratively fitted; ADX itself is a standard indicator, keeping the score moderate.*

- **Gate:** QQQ > SMA(200)
- **Entry:** Expanding Range AND ADX(10) > 25 → TQQQ; ADX > 30 AND SOXL momentum > TQQQ → SOXL
- **Exit:** 3.0 ATR trailing stop OR QQQ < SMA(200)
- **Symbols:** TQQQ, SOXL (signal from QQQ)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -50% | 0.859 | 81 | 66 | 1.23 | 2.34 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 141% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 28% | 🟢 16% | 🟢 83% | 🟢 95% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% |

> [!code]- Click to view: strategy_35.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/strategy_35.py"
> ```


---

## Strategy-5
### Research S31 - Expanding Breakout + ADX + 3.0 ATR (strategy_31.py)

**Description:** Expanding Breakout with tightened ADX trend filters and 3.0 ATR protection.

*Overfit 5/10 — 3.0 ATR is above the typical 2.0 default; combining expanding breakout with tightened ADX and an elevated ATR multiplier suggests multiple rounds of iterative refinement from the S16 baseline.*

- **Gate:** QQQ > SMA(200)
- **Entry:** Expanding Range AND ADX(10) > 25 → 100% TQQQ
- **Exit:** 3.0 ATR trailing stop OR QQQ < SMA(200)
- **Symbols:** TQQQ (signal from QQQ)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -50% | 0.851 | 81 | 67 | 1.21 | 2.32 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 141% | 🔴 -3% | 🔴 -6% | 🟢 78% | 🟢 28% | 🟢 11% | 🟢 84% | 🟢 49% | 🔴 -14% | 🟢 81% | 🟢 36% | 🟢 28% |

> [!code]- Click to view: strategy_31.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/strategy_31.py"
> ```


---

## Strategy-6
### Research S16 - Classic Expanding Breakout + 2.5 ATR (strategy_16.py)

**Description:** Classic Expanding Breakout (Yest Range > Prev Range) with 2.5 ATR trailing stop.

*Overfit 3/10 — classic breakout with a standard ATR multiplier; lowest parameter count in the breakout series; no exotic filters; the unmodified baseline from which S31–S38 were derived.*

- **Gate:** QQQ > SMA(200)
- **Entry:** Expanding Range AND ADX(10) > 20 → 100% TQQQ
- **Exit:** 2.5 ATR trailing stop OR QQQ < SMA(200)
- **Symbols:** TQQQ (signal from QQQ)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -57% | 0.723 | 92 | 109 | 0.84 | 2.41 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 93% | 🔴 -24% | 🔴 -19% | 🟢 92% | 🔴 -1% | 🟢 50% | 🟢 135% | 🟢 43% | 🔴 -25% | 🟢 42% | 🟢 87% | 🟢 10% |

> [!code]- Click to view: strategy_16.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/strategy_16.py"
> ```


---

## Strategy-7
### RSI Frankenfest v1.5 (a_10.py)

**Description:** Multi-layered strategy using a QQQ EMA(200) top gate. Bullish regime uses RSI(TQQQ,2) for dip buying, while bearish regime uses a defensive selection from bonds and defensive ETFs.

*Overfit 7/10 — large defensive ETF pool (10+ symbols), complex ranking logic, and multiple regime gates; the name reflects iterative layering; only 5 years of data (2020 start) gives a short history relative to the parameter count.*

- **Gate:** QQQ > EMA(200)
- **Bull Entry:** RSI(TQQQ, 2) < 20
- **Defensive:** Bottom 1 by RSI(10) from defensive list
- **Symbols:** TQQQ, QLD, BSV, TLT, LQD, VBF, XLP, UGE, XLU, XLV, SPAB, ANGL, etc.
- **Rebalance:** Daily

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -28% | 1.335 | 1160 | 681 | 1.70 | 1.30 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ⚪ 0% | ⚪ 0% | ⚪ 0% | ⚪ 0% | ⚪ 0% | ⚪ 0% | 🟢 4% | 🟢 228% | 🟢 4% | 🟢 118% | 🟢 244% | 🟢 95% |

> [!code]- Click to view: a_10.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/a_10.py"
> ```


---

## Strategy-8
### Research S22 - High-Octane RSI Swing TQQQ (strategy_22.py)

**Description:** High-Octane RSI Swing. Entry on leader dips (NVDA/AMD/TSLA) → 100% TQQQ.

*Overfit 6/10 — only 35 total trades (10 wins, 25 losses), far too few for statistical confidence; using individual stock RSI signals as triggers for a TQQQ position creates a cross-asset dependency unlikely to hold out-of-sample; the NVDA/AMD/TSLA universe reflects hindsight selection.*

- **Gate:** QQQ > SMA(200)
- **Entry:** Any of NVDA/AMD/TSLA RSI(2) < 20 → 100% TQQQ
- **Exit:** QQQ RSI(2) > 70 OR QQQ < SMA(200)
- **Symbols:** TQQQ (trigger from NVDA, AMD, TSLA; signal from QQQ)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -52% | 0.817 | 10 | 25 | 0.40 | 23.67 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 64% | 🟢 5% | 🔴 -17% | 🟢 118% | 🔴 -5% | 🟢 25% | 🟢 123% | 🟢 88% | 🔴 -27% | 🟢 80% | 🟢 62% | 🟢 27% |

> [!code]- Click to view: strategy_22.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/strategy_22.py"
> ```


---

## Strategy-9
### Research S11 - Cheat Code Rotator TQQQ (cheat_code_rotator_tqqq.py)

**Description:** Pure Cheat Code logic. 200 SMA Bull Filter + VIX Shield + RSI2 Dip entry.

*Overfit 5/10 — three stacked filters (SMA(200) + VIX ceiling + RSI(2)) with 81 trades; the VIX ceiling is an additional non-standard fitted threshold; "cheat code" framing suggests the entry conditions were identified retrospectively rather than from first principles.*

- **Gate:** QQQ > SMA(200) AND VIX < 28
- **Entry:** QQQ RSI(2) < 30 → 100% TQQQ
- **Exit:** QQQ RSI(10) > 80 OR QQQ < SMA(200) OR VIX > 32
- **Symbols:** TQQQ (signal from QQQ, VIX)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -50% | 0.772 | 57 | 24 | 2.38 | 1.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 68% | 🟢 8% | 🔴 -25% | 🟢 137% | 🔴 -16% | 🟢 20% | 🟢 69% | 🟢 61% | 🔴 -27% | 🟢 104% | 🟢 64% | 🟢 32% |

> [!code]- Click to view: cheat_code_rotator_tqqq.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/cheat_code_rotator_tqqq.py"
> ```


---

## Strategy-10
### Conservative Rotation (conservative_rotation.py)

**Description:** Always either long or short — never in cash. Rides TQQQ in bull markets and flips to SQQQ during sustained downtrends, but stays long during sharp crashes rather than shorting into panic. Aggressive on both sides of the market. The 1020% return in 2020 is a red flag suggesting the logic was calibrated to the specific shape of the COVID crash and recovery.

*Overfit 7/10 — the crash gate (RSI(10) < 30 prevents shorting into panic drops) appears specifically calibrated to avoid shorting the COVID crash; the 1020% 2020 return is an extreme outlier; always-invested design amplifies the effect of any misfired bear signal.*

- **Entry:** Default TQQQ; rotate to SQQQ when SPY < SMA(200) AND TQQQ < SMA(20) AND no crash
- **Exit:** Rotate back to TQQQ when trend or crash conditions clear
- **Crash Gate:** RSI(10) on QQQ or SPY < 30 → stay long TQQQ (prevents shorting sharp drops)
- **Symbols:** TQQQ, SQQQ, SPY, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 95% | -56% | 1.52 | 100 | 85 | 1.18 | 4.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 49% | 🔴 -2% | 🟢 59% | 🟢 118% | 🟢 26% | 🟢 95% | 🟢 1020% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% |

> [!code]- Click to view: conservative_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/conservative_rotation.py"
> ```


---

## Strategy-11
### Large Cap Dip Buy (large_cap_dip_buy.py)

**Description:** Targets the top 5 largest technology companies by market cap. Waits for a short-term pullback (RSI < 25) within a broad tech universe. Exits when individual positions reach new 1-year highs.

*Overfit 3/10 — standard RSI(2)/ATH-exit logic with a dynamic market cap universe that prevents hindsight symbol selection; RSI threshold of 25 is a minor variation from the common 30; the main concern is the small trade count (80 trades).*

- **Entry:** Top 5 Tech Market Cap AND RSI(2) < 25
- **Exit:** Price >= 252-day High (ATH)
- **Symbols:** Dynamic top 5 tech (AAPL, MSFT, NVDA, AVGO, ORCL)
- **Rebalance:** Weekly

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -55% | 0.844 | 39 | 34 | 1.15 | 2.59 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 9% | 🔴 -1% | 🟢 8% | 🟢 35% | 🟢 8% | 🟢 41% | 🟢 40% | 🟢 62% | 🔴 -42% | 🟢 118% | 🟢 131% | 🟢 39% |

> [!code]- Click to view: large_cap_dip_buy.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/large_cap_dip_buy.py"
> ```


---

## Strategy-12
### Giant Sniper Mean-Reversion (giant_sniper_mean_rev.py)

**Description:** High-conviction mean reversion in global leaders. Selects Top 5 by Market Cap monthly and enters on deep RSI(2) dips.

*Overfit 2/10 — minimal parameters (RSI(2) < 20 entry, RSI(2) > 70 exit, SMA(200) shield); dynamic market cap universe eliminates hindsight symbol selection; 706 trades provides strong statistical backing; close to textbook RSI mean-reversion.*

- **Universe:** Top 5 Market Cap
- **Entry:** RSI(2) < 20
- **Exit:** RSI(2) > 70 OR QQQ < SMA(200)
- **Shield:** QQQ > SMA(200)
- **Rebalance:** Daily

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27% | -44% | 0.835 | 452 | 254 | 1.78 | 1.22 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 15% | 🟢 49% | 🔴 -13% | 🟢 48% | 🔴 -16% | 🟢 7% | 🟢 34% | 🟢 80% | 🔴 -10% | 🟢 43% | 🟢 40% | 🟢 94% |

> [!code]- Click to view: giant_sniper_mean_rev.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/giant_sniper_mean_rev.py"
> ```


---

## Strategy-13
### VAA Leveraged (vaa_leveraged.py)

**Description:** VAA-G (Global) strategy modified for leveraged ETFs. Rotates between high-momentum offensive assets (TQQQ, EFA, EEM, AGG) when all are positive, or defensive assets (LQD, IEF, SHY) otherwise. Monthly rebalancing.

*Overfit 4/10 — the VAA momentum formula (12/4/2/1 weights) is published and non-fitted; replacing the original broad ETFs with TQQQ as the sole offensive asset introduces LETF hindsight selection risk; defensive basket (LQD/IEF/SHY) is standard.*

- **Logic:** Momentum Score = (12 * r1) + (4 * r3) + (2 * r6) + (1 * r12)
- **Risk-On:** ALL offensive scores > 0
- **Assets (Offensive):** TQQQ, EFA, EEM, AGG
- **Assets (Defensive):** LQD, IEF, SHY
- **Rebalance:** Monthly

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27% | -37% | 0.788 | 98 | 51 | 1.92 | 3.35 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 28% | 🟢 5% | 🟢 10% | 🟢 66% | 🟢 53% | 🟢 49% | 🟢 61% | 🟢 9% | 🔴 -11% | 🟢 15% | 🔴 -2% | 🟢 37% |

> [!code]- Click to view: vaa_leveraged.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/vaa_leveraged.py"
> ```


---

## Strategy-14
### SOXL.SOXS SeeSaw (a_6.py)

**Description:** Binary rotation between SOXL and SOXS based on RSI thresholds and cumulative returns. Includes a cash (BIL) default and UVXY for hedging.

*Overfit 7/10 — non-standard RSI periods (25 and 32) not found in reference literature; dual cumulative return lookbacks (6-month and 1-month) with a custom drift rebalance threshold are all hand-fitted; 477 trades is borderline for this parameter count.*

- **Indicators:** RSI(SOXS, 25), RSI(SOXL, 32), CumRet(6), CumRet(1)
- **Default:** BIL
- **Symbols:** SOXL, SOXS, UVXY, BIL
- **Rebalance:** Drift-based (10%)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 54% | -24% | 1.339 | 305 | 172 | 1.77 | 2.74 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 1% | 🟢 3% | 🟢 6% | ⚪ 0% | 🟢 118% | 🟢 23% | 🟢 142% | 🟢 74% | 🟢 265% | 🟢 22% | 🟢 36% | 🟢 132% |

> [!code]- Click to view: a_6.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/a_6.py"
> ```


---

## Strategy-15
### SOXL.SOXS SeeSaw Duplicate (a_7.py)

**Description:** Duplicate of Strategy 8. Uses binary rotation between SOXL and SOXS based on RSI and cumulative return logic.

*Overfit 7/10 — identical to Strategy-14; the presence of a near-identical variant implies active parameter search rather than independent derivation; both should be treated as a single research branch.*

- **Indicators:** RSI(SOXS, 25), RSI(SOXL, 32), CumRet(6), CumRet(1)
- **Symbols:** SOXL, SOXS, UVXY, BIL
- **Rebalance:** Drift-based (10%)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 54% | -24% | 1.339 | 305 | 172 | 1.77 | 2.74 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 1% | 🟢 3% | 🟢 6% | ⚪ 0% | 🟢 118% | 🟢 23% | 🟢 142% | 🟢 74% | 🟢 265% | 🟢 22% | 🟢 36% | 🟢 132% |

> [!code]- Click to view: a_7.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/a_7.py"
> ```


---

## Strategy-16
### Rotation Strategy V1 (rotation_v1.py)

**Description:** Trend-following rotation between TQQQ and SPY. Uses SPY SMA(200) as a global regime filter.

*Overfit 6/10 — the 1020% 2020 return is a major outlier suggesting the rotation timing was calibrated to the COVID crash and recovery; commented-out bear logic and multiple candidate assets (TQQQ/SPXL/TECL) indicate iterative asset selection.*

- **Regime:** SPY > SMA(200) → TQQQ
- **Bear Logic:** Stay in cash or SQQQ (original code commented out)
- **Symbols:** SPY, QQQ, TQQQ, SPXL, UVXY, TECL, UPRO, SQQQ, TLT
- **Rebalance:** Daily

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 95% | -56% | 1.52 | 100 | 85 | 1.18 | 4.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 49% | 🔴 -2% | 🟢 59% | 🟢 118% | 🟢 26% | 🟢 95% | 🟢 1020% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% |

> [!code]- Click to view: rotation_v1.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/rotation_v1.py"
> ```


---

## Strategy-17
### Defensive Rotation (defensive_rotation.py)

**Description:** Rotates between TQQQ, SQQQ, and cash depending on the trend and momentum regime. More conservative than S19 — defaults to cash when conditions are ambiguous rather than forcing a position. A duplicate initialization block in the code indicates this strategy was tuned in place over time.

*Overfit 6/10 — SMA(200) and SMA(20) are standard, but RSI(2) < 20 bull entry and RSI(2) > 80 bear entry are tighter than the typical 30/70; the duplicate initialization block confirms iterative in-place tuning.*

- **Entry (Bull):** TQQQ > SMA(200) AND (price > SMA(20) OR RSI(2) < 20) → TQQQ
- **Entry (Bear):** TQQQ ≤ SMA(200) AND (price < SMA(20) OR RSI(2) > 80) → SQQQ
- **Cash Gate:** RSI(10) on QQQ or SPY < 30 → cash regardless of regime
- **Default:** Cash
- **Symbols:** TQQQ, SQQQ, SPY, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -54% | 0.818 | 220 | 228 | 0.96 | 1.98 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 25% | 🔴 -25% | 🔴 -28% | 🟢 99% | 🟢 5% | 🟢 11% | 🟢 225% | 🟢 82% | 🟢 119% | 🟢 30% | 🟢 41% | 🟢 25% |

> [!code]- Click to view: defensive_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/defensive_rotation.py"
> ```


---

## Strategy-18
### RSI Rebalance (rsi_rebalance.py)

**Description:** An advanced version of the RSI Champion. Monitors QQQ for extreme oversold conditions and rotates into an aggressive growth basket. Includes a defensive ranking system for rotation during neutral periods.

*Overfit 3/10 — single oversold trigger with 2910 trades gives strong statistical confidence; RSI(2) < 25 and the LETF basket are the only minor non-standard choices; the defensive ranking fallback adds parameters but does not change the dominant core signal.*

- **Entry:** QQQ RSI(2) < 25 → equal-weight TQQQ / SOXL / TECL
- **Exit:** QQQ RSI(2) >= 25 → 100% Cash/Defensive
- **Symbols:** TQQQ, SOXL, TECL, TLT, GLD, IEF, AGG, BND, SGOV, BSV

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 50% | -37% | 1.076 | 1440 | 588 | 2.45 | 0.81 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 21% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 🟢 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 51% |

> [!code]- Click to view: rsi_rebalance.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/rsi_rebalance.py"
> ```


---

## Strategy-19
### TQQQ Simple Long Term (a_2.py)

**Description:** A trend-following strategy for TQQQ using SPY SMA(200) as a regime filter and TQQQ SMA(20) for local trend. Includes RSI(10) filters for timing.

*Overfit 7/10 — 158% CAGR and 4720% in 2020 are extreme outliers; the triple-filter stack (SPY SMA(200) + TQQQ SMA(20) + RSI(10)) appears calibrated to catch the exact shape of the COVID recovery; the implausibly high CAGR is the primary concern.*

- **Entry:** SPY > SMA(200) AND (TQQQ > SMA(20) OR RSI(10) < 30)
- **Exit:** SPY <= SMA(200) OR (TQQQ < SMA(20) AND RSI(10) > 70)
- **Symbols:** TQQQ, SQQQ, SPY, UVXY, SPXL, UPRO, TLT
- **Rebalance:** Daily

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 158% | -56% | 2.224 | 276 | 119 | 2.32 | 1.67 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | ⚪ 0% | 🟢 65% | 🟢 138% | 🟢 70% | 🟢 186% | 🟢 4720% | 🟢 163% | 🟢 186% | 🟢 195% | 🟢 75% | 🟢 76% |

> [!code]- Click to view: a_2.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/a_2.py"
> ```


---

## Strategy-20
### Large Cap Tech Strategy (large_cap_ema.py)

**Description:** A simple trend-following strategy for top tech leaders. Buys when price pulls below the 100-day EMA and exits when it recovers to a new 1-year high.

*Overfit 2/10 — clean two-rule design (EMA(100) entry, 252-day high exit); dynamic market cap universe prevents hindsight symbol selection; EMA(100) is less standard than SMA(200) but not exotic; 47 trades is small but the logic is straightforward.*

- **Entry:** Top 5 Tech Market Cap AND Price < EMA(100)
- **Exit:** Price >= 252-day High
- **Symbols:** Dynamic Top 5 Tech
- **Rebalance:** Weekly

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 28% | -50% | 0.825 | 37 | 20 | 1.85 | 2.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 17% | 🟢 1% | 🟢 6% | 🟢 33% | 🟢 10% | 🟢 43% | 🟢 30% | 🟢 53% | 🔴 -36% | 🟢 92% | 🟢 120% | 🟢 42% |

> [!code]- Click to view: large_cap_ema.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/large_cap_ema.py"
> ```


---

## Strategy-21
### Research S8 - TQQQ Dynamic Compounding (dip_buy_tqqq.py)

**Description:** Dynamic Compounding. Varies TQQQ leverage based on RSI2 dip/RSI10 exhaustion.

*Overfit 4/10 — RSI thresholds (30, 80) are textbook oversold/overbought levels and SMA(200) is canonical, but the three-tier allocation (20%/50%/100%) and the RSI(10) > 80 de-lever trigger look hand-fitted; single-ticker focus on TQQQ keeps the parameter space small. Restored from git history (commit cba62e9^); identical in spirit to the active tqqq_dynamic.py.*

- **Entry (Bull, full):** TQQQ > SMA(200) AND RSI(2) < 30 → 100%
- **Entry (Bull, default):** TQQQ > SMA(200), not overbought → 50%
- **De-lever:** TQQQ > SMA(200) AND RSI(10) > 80 → 20%
- **Exit:** TQQQ ≤ SMA(200) → 100% cash
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -49% | 0.738 | 100 | 47 | 2.13 | 1.44 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 35% | 🟢 4% | 🔴 -15% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 69% | 🟢 83% | 🔴 -21% | 🟢 70% | 🟢 29% | 🟢 25% |

> [!code]- Click to view: dip_buy_tqqq.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/dip_buy_tqqq.py"
> ```


---

## Strategy-22
### Equal-Weight LETF Rebalance (rebalance.py)

**Description:** Simple periodic rebalancer for TQQQ/SOXL/TECL. Holds 20% in each ETF (60% total) and 40% cash, rebalancing once per year after 11am.

*Overfit 4/10 — zero mechanical parameter tuning, but the TQQQ/SOXL/TECL choice is hindsight bias — these three were among the best-performing leveraged ETFs of the backtest decade, knowable only after the fact. 40% cash dampens drawdowns but doesn't address the selection issue.*

- **Allocation:** TQQQ 20%, SOXL 20%, TECL 20%, Cash 40%
- **Rebalance:** Yearly
- **Symbols:** TQQQ, SOXL, TECL

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -52% | 0.848 | 38 | 0 | — | — |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 37% | 🟢 1% | 🟢 32% | 🟢 76% | 🔴 -15% | 🟢 107% | 🟢 51% | 🟢 65% | 🔴 -47% | 🟢 127% | 🟢 16% | 🟢 26% |

> [!code]- Click to view: rebalance.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos1/rebalance.py"
> ```


---

## Strategy-23
### TQQQ trend SMA200 (algo_003.py)

**Description:** The canonical "price above 200-day SMA" trend filter applied to QQQ (NASDAQ 100 ETF), with the execution vehicle being TQQQ for 3x leveraged exposure during uptrends. When QQQ is above its 200d SMA, the algo goes 100% TQQQ; when it dips below, it moves entirely to cash. The 200-day SMA is the most widely followed technical indicator in institutional markets, so its signals have real behavioral anchoring — but the lagging nature means the leveraged vehicle takes severe damage before the exit triggers. In 2022, QQQ broke below its 200d SMA well after TQQQ had already lost ~60% from its peak.

*Overfit 1/10 — The 200-day SMA is a standard, universally recognized threshold. Zero tuned parameters beyond it.*

- **Entry:** QQQ price > 200-day SMA → allocate 100% to TQQQ
- **Exit:** QQQ price <= 200-day SMA → liquidate TQQQ to cash
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -56% | 0.753 | 10 | 47 | 0.21 | 28.85 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 2% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 105% | 🟢 88% | 🔴 -44% | 🟢 112% | 🟢 62% | 🟢 23% |

> [!code]- Click to view: algo_003.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_003.py"
> ```


---

## Strategy-24
### TQQQ trend SMA150 (algo_006.py)

**Description:** An identical structure to 003 but with the SMA lookback shortened from 200 to 150 days. This faster filter catches trend entries a few weeks earlier and, more importantly, exits during drawdowns sooner — which in 2022 meant preserving more capital for the recovery. The result is a meaningful lift in CAGR (33% to 40%) with essentially unchanged MaxDD (-56% to -55%). The weakness is that a shorter lookback increases whipsaw frequency during range-bound, choppy markets.

*Overfit 2/10 — 150d is a common alternative to 200d, but this is clearly part of a parameter sweep across SMA lengths. The improvement over 003 is marginal enough to question out-of-sample robustness.*

- **Entry:** QQQ price > 150-day SMA → allocate 100% to TQQQ
- **Exit:** QQQ price <= 150-day SMA → liquidate TQQQ to cash
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -55% | 0.871 | 21 | 36 | 0.58 | 14.75 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 18% | 🔴 -5% | 🟢 118% | 🟢 1% | 🟢 53% | 🟢 97% | 🟢 88% | 🔴 -34% | 🟢 125% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: algo_006.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_006.py"
> ```


---

## Strategy-25
### TQQQ self-SMA200 (algo_008.py)

**Description:** Applies the 200-day SMA filter directly to the leveraged instrument TQQQ rather than the underlying QQQ. The rationale might be simplicity (one symbol), but it introduces a subtle problem: TQQQ's 3x daily leverage creates volatility decay and path-dependence that the underlying NASDAQ 100 does not have, making the self-SMA signal noisier and less reliable as a trend gauge.

*Overfit 1/10 — Standard 200d SMA, no parameter tuning. The symbol choice (TQQQ vs QQQ) is a design decision, not a fitted parameter.*

- **Entry:** TQQQ price > TQQQ's own 200-day SMA → allocate 100% to TQQQ
- **Exit:** TQQQ price <= own 200-day SMA → liquidate to cash
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -50% | 0.76 | 18 | 41 | 0.44 | 16.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 11% | 🔴 -20% | 🟢 118% | 🟢 8% | 🟢 40% | 🟢 69% | 🟢 88% | 🔴 -21% | 🟢 68% | 🟢 41% | 🟢 16% |

> [!code]- Click to view: algo_008.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_008.py"
> ```


---

## Strategy-26
### TQQQ self-SMA150 (algo_009.py)

**Description:** The same self-SMA approach as 008 but with a 150-day lookback applied to TQQQ's own price. This performs strictly worse than 008 across all metrics (29% CAGR, -53% MaxDD, 0.69 Sharpe vs 33%, -50%, 0.76), making it the weakest variant in this family. The combination of leveraged volatility and a shorter lookback amplifies whipsaw losses: TQQQ's daily price swings of 5-10% mean it frequently breaches its own 150d SMA on noise rather than genuine trend changes.

*Overfit 3/10 — The 150d lookback on a 3x leveraged ETF is non-standard and appears to be a speculative parameter choice. The clear degradation relative to 008 (200d) suggests this was tested as part of a sweep.*

- **Entry:** TQQQ price > TQQQ's own 150-day SMA → allocate 100% to TQQQ
- **Exit:** TQQQ price <= own 150-day SMA → liquidate to cash
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -53% | 0.692 | 24 | 59 | 0.41 | 10.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 42% | 🟢 1% | 🔴 -5% | 🟢 118% | 🔴 -23% | 🟢 16% | 🟢 93% | 🟢 64% | 🔴 -22% | 🟢 76% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: algo_009.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_009.py"
> ```


---

## Strategy-27
### SMA200 75% cap (algo_011.py)

**Description:** A de-risked variant of 003 that uses the same QQQ > 200d SMA entry signal but caps TQQQ allocation at 75% instead of 100%. The remaining 25% sits in cash, providing a buffer during drawdowns and reducing overall portfolio volatility. This predictably reduces CAGR (33% to 29%) alongside MaxDD (-56% to -49%). The 75% cap is intuitively appealing but the specific number feels tuned to this backtest window.

*Overfit 2/10 — The 75% allocation cap is a single tuned parameter. 75% is a round number but likely chosen by testing several caps and picking the one that trimmed MaxDD without cratering CAGR.*

- **Entry:** QQQ price > 200-day SMA → allocate 75% to TQQQ (25% cash)
- **Exit:** QQQ price <= 200-day SMA → liquidate TQQQ to cash
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -49% | 0.703 | 10 | 47 | 0.21 | 28.86 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 42% | 🟢 1% | 🔴 -9% | 🟢 94% | 🔴 -16% | 🟢 39% | 🟢 87% | 🟢 80% | 🔴 -39% | 🟢 87% | 🟢 55% | 🟢 15% |

> [!code]- Click to view: algo_011.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_011.py"
> ```


---

## Strategy-28
### IBS MR pure (algo_016.py)

**Description:** Buys TQQQ when the close is near the low of the day (IBS < 0.2, oversold) and sells when the close nears the high (IBS > 0.7, overbought), applying mean reversion to a 3x leveraged Nasdaq ETF. The asymmetric thresholds (wide buy, narrow sell) bias toward holding long, which partially compensates for fighting TQQQ's strong upward drift. Its main weakness is that mean reversion systematically shorts strength in a secular bull market, leaving significant upside on the table during trending rallies.

*Overfit 2/10 — the 0.2/0.7 IBS thresholds are standard values from the literature; only 2 parameters, both round numbers.*

- **Entry:** IBS < 0.2 (close near the daily low)
- **Exit:** IBS > 0.7 (close near the daily high)
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -50% | 0.817 | 498 | 245 | 2.03 | 0.85 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -11% | 🔴 -18% | 🟢 18% | 🟢 41% | 🔴 -12% | 🟢 18% | 🟢 384% | 🟢 51% | 🟢 24% | 🟢 125% | ⚪ 0% | 🟢 43% |

> [!code]- Click to view: algo_016.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_016.py"
> ```


---

## Strategy-29
### 5 most mkt cap @ 1.5x (algo_018.py)

**Description:** Each month, buys equal weights of the 5 most market capital companies using 1.5x margin, liquidating any that fall out of the top 5. The strategy rides the compounding power of market-leading megacaps (AAPL, MSFT, NVDA, AMZN, GOOGL) with leverage — and this has worked brilliantly as mega-cap tech dominated. Its critical weakness is the complete absence of risk management: a concentrated 5-stock portfolio at 1.5x leverage can experience catastrophic drawdowns during regime shifts.

*Overfit 2/10 — top-5-by-market-cap is a natural universe definition; 1.5x leverage is a round number; no lookback windows or threshold tuning.*

- **Entry:** Monthly rebalance into 5 most market capital companies, each at weight = 1.5 / 5
- **Exit:** Liquidate any position that drops out of the top 5
- **Symbols:** Top 5 US equities by market cap (dynamic universe)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -55% | 0.829 | 569 | 49 | 11.61 | 1.89 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 19% | 🟢 14% | 🟢 10% | 🟢 53% | 🟢 12% | 🟢 70% | 🟢 84% | 🟢 71% | 🔴 -51% | 🟢 102% | 🟢 50% | 🟢 50% |

> [!code]- Click to view: algo_018.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_018.py"
> ```


---

## Strategy-30
### TQQQ IBS extreme (algo_028.py)

**Description:** A stricter variant of the IBS mean reversion theme that only buys when selling is truly extreme (IBS < 0.1) and only exits when buying is truly extreme (IBS > 0.9). This dramatically reduces trade frequency but each entry catches deeper capitulation, and the very late exit allows full trend participation once a rally is underway. The 47% CAGR (vs 35% for the standard 0.2/0.7 version) shows that patience on entry and letting winners run more than compensates for extended cash periods.

*Overfit 3/10 — extreme round thresholds (0.1, 0.9) are less commonly used than the standard IBS 0.2/0.8 pair but are still intuitive boundary values.*

- **Entry:** IBS < 0.1 (extreme selling pressure)
- **Exit:** IBS > 0.9 (extreme buying pressure)
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 47% | -47% | 1.05 | 269 | 100 | 2.69 | 1.00 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 12% | 🟢 5% | 🟢 39% | 🟢 71% | 🔴 -18% | 🟢 35% | 🟢 344% | 🟢 75% | 🔴 -1% | 🟢 101% | 🟢 17% | 🟢 82% |

> [!code]- Click to view: algo_028.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_028.py"
> ```


---

## Strategy-31
### TQQQ IBS 0.15/0.85 (algo_029.py)

**Description:** A middle-ground IBS variant with buy at 0.15 and exit at 0.85 — sandwiched between the standard 0.2/0.7 (algo 016) and the extreme 0.1/0.9 (algo 028). It achieves the best MaxDD of the three (-42% vs -50% and -47%) and a CAGR (37%) that splits the difference. The key weakness is that these specific intermediate values have no theoretical justification — they are clearly the product of a parameter sweep.

*Overfit 5/10 — the 0.15 and 0.85 thresholds do not correspond to any standard IBS value and appear to be the result of explicit parameter optimization.*

- **Entry:** IBS < 0.15
- **Exit:** IBS > 0.85
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -42% | 0.843 | 361 | 162 | 2.23 | 0.88 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -3% | ⚪ 0% | 🟢 5% | 🟢 50% | 🔴 -22% | 🟢 63% | 🟢 361% | 🟢 74% | 🟢 9% | 🟢 74% | 🟢 1% | 🟢 42% |

> [!code]- Click to view: algo_029.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_029.py"
> ```


---

## Strategy-32
### IBS extreme + SMA200 (algo_030.py)

**Description:** Combines the IBS extreme oversold signal with a 200-day SMA trend filter on QQQ. It only enters a TQQQ position when both IBS is below 0.1 (extreme intraday weakness) and QQQ is trading above its 200-day SMA (uptrend), which keeps it out of sustained bear markets. The drawback is the trend filter can delay re-entry after a sharp but short-lived dip.

*Overfit 3/10 — IBS thresholds (0.1/0.9) are round but arbitrary; SMA 200 is a standard lookback. The QQQ trend filter adds a second conditional.*

- **Entry:** IBS < 0.1 and QQQ price > SMA(200)
- **Exit:** IBS > 0.9
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -40% | 0.903 | 214 | 79 | 2.71 | 0.97 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 12% | 🟢 1% | 🟢 8% | 🟢 71% | 🔴 -10% | 🟢 34% | 🟢 136% | 🟢 75% | 🔴 -14% | 🟢 84% | 🟢 17% | 🟢 50% |

> [!code]- Click to view: algo_030.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_030.py"
> ```


---

## Strategy-33
### IBS extreme + ATR stop (algo_031.py)

**Description:** Enters TQQQ on IBS < 0.1 like the basic IBS strategy, but adds a trailing volatility-based stop loss at 3x the 14-period ATR from the entry price. This stop is designed to cap catastrophic single-trade losses during flash crashes or gap downs. The weakness is that TQQQ's 3x leverage amplifies volatility, making the 3x ATR stop prone to triggering on routine whipsaws rather than true disasters.

*Overfit 3/10 — IBS thresholds and ATR multiplier (3x) are standard choices (Bollinger-style 3-sigma logic). ATR(14) is a canonical period.*

- **Entry:** IBS < 0.1
- **Exit:** IBS > 0.9, OR close < entry_price - 3 x ATR(14)
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 46% | -43% | 1.049 | 271 | 106 | 2.56 | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 7% | 🟢 6% | 🟢 39% | 🟢 71% | 🔴 -29% | 🟢 33% | 🟢 344% | 🟢 75% | 🔴 -1% | 🟢 101% | 🟢 29% | 🟢 82% |

> [!code]- Click to view: algo_031.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_031.py"
> ```


---

## Strategy-34
### IBS 0.05 (rare) (algo_032.py)

**Description:** A stricter version of the IBS strategy that only buys when IBS drops below 0.05 — a much rarer event than the standard 0.1 threshold. This results in fewer but theoretically higher-conviction trades, since the stock needs to close extremely near its daily low. The main weakness is extended cash drag between rare entry signals.

*Overfit 2/10 — only two parameters (0.05 entry, 0.9 exit). However, 0.05 is a suspiciously precise threshold that was almost certainly backtest-optimized.*

- **Entry:** IBS < 0.05
- **Exit:** IBS > 0.9
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -47% | 0.791 | 170 | 60 | 2.83 | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 9% | 🟢 8% | 🟢 43% | 🟢 37% | 🔴 -12% | 🟢 24% | 🟢 216% | 🟢 28% | 🟢 6% | 🟢 45% | 🔴 -6% | 🟢 77% |

> [!code]- Click to view: algo_032.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_032.py"
> ```


---

## Strategy-35
### IBS 0.1/0.7 fast (algo_033.py)

**Description:** Enters on the standard IBS < 0.1 signal but exits much earlier at IBS > 0.7 instead of the usual 0.9. The tighter exit captures only the initial mean-reversion bounce and avoids holding through the extended recovery leg. The weakness is that it systematically leaves money on the table — many trades that recover fully to 0.9+ are cut at 0.7.

*Overfit 2/10 — only two round thresholds (0.1/0.7). The 0.7 exit is the sole deviation from the standard IBS template.*

- **Entry:** IBS < 0.1
- **Exit:** IBS > 0.7
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -35% | 0.915 | 328 | 141 | 2.33 | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -7% | 🔴 -4% | 🟢 23% | 🟢 34% | 🔴 -1% | 🟢 18% | 🟢 273% | 🟢 20% | 🟢 26% | 🟢 89% | 🟢 75% | 🟢 22% |

> [!code]- Click to view: algo_033.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_033.py"
> ```


---

## Strategy-36
### IBS regime-adaptive (algo_035.py)

**Description:** Uses a 200-day SMA on QQQ to switch between two regimes: in uptrends it buys TQQQ on moderate pullbacks (IBS < 0.1), but in downtrends it only enters on extremely rare capitulation events (IBS < 0.03). Exits when IBS crosses above 0.9 regardless of regime. The regime-awareness prevents catching falling knives during bear markets, but the 0.03 downtrend threshold is so extreme that the algo sits in cash for entire bear-market rallies.

*Overfit 4/10 — two regime-specific IBS entry thresholds (0.1 vs 0.03), one exit (0.9), and a SMA(200) lookback; the 0.03 value is especially vulnerable to hindsight tuning.*

- **Entry:** IBS < 0.1 if QQQ > SMA(200); IBS < 0.03 if QQQ < SMA(200)
- **Exit:** IBS > 0.9
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -55% | 0.917 | 237 | 92 | 2.58 | 0.98 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 12% | 🟢 1% | 🟢 26% | 🟢 71% | 🔴 -31% | 🟢 35% | 🟢 303% | 🟢 75% | 🔴 -23% | 🟢 84% | 🟢 17% | 🟢 92% |

> [!code]- Click to view: algo_035.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_035.py"
> ```


---

## Strategy-37
### IBS + 3d max hold (algo_039.py)

**Description:** A pure mean-reversion strategy that buys TQQQ whenever IBS drops below 0.1 and forces an exit after three trading days regardless of price, in addition to the standard IBS > 0.9 exit. The time-capped hold prevents a failed reversion trade from decaying into a large loss. However, the arbitrary 3-day exit can cut short a reversion that is still developing.

*Overfit 5/10 — two IBS thresholds (0.1 entry, 0.9 exit) and a 3-bar max-hold parameter; changing the hold to 2, 4, or 5 days would materially alter results.*

- **Entry:** IBS < 0.1
- **Exit:** IBS > 0.9 OR held >= 3 bars
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -52% | 0.799 | 295 | 166 | 1.78 | 1.04 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -4% | 🔴 -18% | 🟢 15% | 🟢 47% | 🟢 46% | 🟢 9% | 🟢 205% | 🟢 58% | 🔴 -34% | 🟢 90% | 🟢 61% | 🟢 8% |

> [!code]- Click to view: algo_039.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_039.py"
> ```


---

## Strategy-38
### SMA150 trend + IBS<0.05 (algo_040.py)

**Description:** A hybrid strategy that holds TQQQ during uptrends (QQQ > SMA150) and switches to a mean-reversion overlay in downtrends, buying only when IBS drops below 0.05 and selling at IBS > 0.9. This captures full bull-market exposure while deploying a defensive dip-buying approach during drawdowns. The sequential transition (liquidate trend, then wait for MR entry) means a sharp reversal off the trend line leaves the algo fully in cash.

*Overfit 5/10 — SMA lookback (150 vs the more standard 200), two-mode architecture, MR entry threshold (0.05), and IBS exit (0.9).*

- **Entry:** QQQ > SMA(150) → buy TQQQ; QQQ < SMA(150) AND IBS < 0.05 → buy TQQQ
- **Exit:** Trend mode → exit on trend flip; MR mode → IBS > 0.9
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 50% | -56% | 0.986 | 52 | 45 | 1.16 | 5.27 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 7% | 🟢 26% | 🟢 118% | 🔴 -22% | 🟢 55% | 🟢 222% | 🟢 88% | 🔴 -31% | 🟢 135% | 🟢 64% | 🟢 57% |

> [!code]- Click to view: algo_040.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_040.py"
> ```


---

## Strategy-39
### SMA150 + IBS + 3xATR (algo_042.py)

**Description:** Extends algo 040 by adding a 3x ATR(14) trailing stop on mean-reversion positions only, exiting MR trades when price drops below entry_price - 3 * ATR in addition to the IBS > 0.9 exit. Trend-mode positions are not stopped at all. The ATR stop provides theoretical downside protection, but on TQQQ (extremely high volatility) the 3xATR distance is so wide that it rarely triggers, making the practical difference from algo 040 marginal.

*Overfit 7/10 — all of 040's parameters plus ATR period (14), ATR multiplier (3), and entry-price tracking; the combination outperforms 040 by only 1% CAGR, suggesting the extra complexity is not justified.*

- **Entry:** QQQ > SMA(150) → buy TQQQ; QQQ < SMA(150) AND IBS < 0.05 → buy TQQQ
- **Exit:** Trend mode → exit on trend flip; MR mode → IBS > 0.9 OR price < entry_price - 3x ATR(14)
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 51% | -55% | 1.002 | 57 | 44 | 1.30 | 4.54 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 8% | 🟢 26% | 🟢 118% | 🔴 -16% | 🟢 55% | 🟢 222% | 🟢 88% | 🔴 -31% | 🟢 135% | 🟢 64% | 🟢 57% |

> [!code]- Click to view: algo_042.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_042.py"
> ```


---

## Strategy-40
### SMA150 + IBS + 2xATR (algo_043.py)

**Description:** A hybrid trend/mean-reversion strategy on TQQQ that goes long in an uptrend (QQQ above its 150-day SMA) and fades deeply oversold conditions via mean reversion when the trend is flat or down. The "tighter stop" from #42 is a 2x ATR hard stop below the MR entry price, intended to cap losses when oversold bounces fail. The weakness is that 2x ATR on TQQQ is very tight for a 3x leveraged ETF — normal daily volatility can trigger the stop before the mean reversion materializes.

*Overfit 3/10 — standard lookbacks (SMA 150, ATR 14) and extreme IBS thresholds (0.05/0.9) are common choices. The 2x ATR multiplier is the only tuned parameter.*

- **Entry (Trend):** QQQ > SMA(150) and not invested → go long TQQQ at 100%
- **Entry (MR):** QQQ <= SMA(150), not invested, and IBS < 0.05 → go long TQQQ at 100%
- **Exit (Trend):** QQQ drops below SMA(150) → liquidate
- **Exit (MR):** IBS > 0.9 or price < entry_price - 2 * ATR(14) → liquidate
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 51% | -58% | 1.01 | 57 | 44 | 1.30 | 4.53 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 23% | 🟢 19% | 🟢 118% | 🔴 -3% | 🟢 55% | 🟢 222% | 🟢 88% | 🔴 -43% | 🟢 135% | 🟢 64% | 🟢 57% |

> [!code]- Click to view: algo_043.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_043.py"
> ```


---

## Strategy-41
### SMA150+IBS fast exit (algo_046.py)

**Description:** A simplified hybrid that removes the ATR stop entirely and exits mean-reversion positions as soon as IBS crosses above 0.7 (versus the typical 0.9). Ride TQQQ long when QQQ is above its 150-day SMA, and buy deep oversold IBS (< 0.05) bounces when it is not, cashing out quickly at 0.7 for higher turnover. Dropping the hard stop reduces parameter count but leaves MR positions exposed to gap-down or sustained selling.

*Overfit 2/10 — IBS take-profit at 0.7 instead of 0.9 is a single threshold tweak. All other parameters are standard.*

- **Entry (Trend):** QQQ > SMA(150) → go long TQQQ at 100%
- **Entry (MR):** QQQ <= SMA(150) and IBS < 0.05 → go long TQQQ at 100%
- **Exit (Trend):** QQQ drops below SMA(150) → liquidate
- **Exit (MR):** IBS > 0.7 → liquidate
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 55% | -55% | 1.068 | 62 | 49 | 1.27 | 4.76 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 7% | 🟢 17% | 🟢 118% | 🔴 -14% | 🟢 57% | 🟢 276% | 🟢 88% | 🔴 -26% | 🟢 135% | 🟢 64% | 🟢 70% |

> [!code]- Click to view: algo_046.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_046.py"
> ```


---

## Strategy-42
### #46 + chandelier (algo_047.py)

**Description:** Builds on #46 by adding a trailing chandelier stop on trend positions (5x ATR from the peak) and a hard stop on mean-reversion positions (3x ATR below entry). The trailing stop is meant to lock in trend gains during sharp reversals. In practice, the 5x ATR trail on a 3x leveraged ETF may be wide enough that it only triggers during crash events.

*Overfit 4/10 — two added ATR multipliers (5x for trend trail, 3x for MR stop) tuned against past data. These interact with the existing IBS thresholds.*

- **Entry (Trend):** QQQ > SMA(150) → go long at 100%; record peak at entry
- **Entry (MR):** QQQ <= SMA(150) and IBS < 0.05 → go long TQQQ at 100%
- **Exit (Trend via SMA):** QQQ drops below SMA(150) → liquidate
- **Exit (Trend via Chandelier):** Close < peak_price - 5 * ATR(14) → liquidate
- **Exit (MR via IBS):** IBS > 0.7 → liquidate
- **Exit (MR via Stop):** Close < entry_price - 3 * ATR(14) → liquidate
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 52% | -56% | 1.027 | 77 | 60 | 1.28 | 2.77 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 46% | 🟢 8% | 🟢 9% | 🟢 118% | 🔴 -23% | 🟢 60% | 🟢 266% | 🟢 81% | 🔴 -26% | 🟢 136% | 🟢 64% | 🟢 70% |

> [!code]- Click to view: algo_047.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_047.py"
> ```


---

## Strategy-43
### #46 on QLD (algo_048.py)

**Description:** An exact replica of #46's logic applied to QLD (2x Nasdaq-100) instead of TQQQ (3x). The intent is to test whether the #46 edge survives deleveraging — lower CAGR is expected (40% vs. 55%), but the commensurately lower drawdown (-40% vs. -55%) suggests the underlying timing signal, not leverage, drives most of the risk-adjusted return.

*Overfit 1/10 — no new parameters versus #46. The only change is the traded symbol, a straightforward robustness check.*

- **Entry (Trend):** QQQ > SMA(150) → go long QLD at 100%
- **Entry (MR):** QQQ <= SMA(150) and IBS < 0.05 → go long QLD at 100%
- **Exit (Trend):** QQQ drops below SMA(150) → liquidate
- **Exit (MR):** IBS > 0.7 → liquidate
- **Symbols:** QLD, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -40% | 1.018 | 69 | 46 | 1.50 | 3.88 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🟢 11% | 🟢 3% | 🟢 70% | 🔴 -4% | 🟢 36% | 🟢 158% | 🟢 57% | 🟢 2% | 🟢 93% | 🟢 46% | 🟢 49% |

> [!code]- Click to view: algo_048.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_048.py"
> ```


---

## Strategy-44
### %R(2) MR pure (algo_053.py)

**Description:** Buys TQQQ when the 2-period Williams %R dips below -90, betting on an immediate bounce from extreme oversold conditions, then sells when %R crosses above -10. The ultra-short 2-bar window makes this a high-frequency mean-reversion gambit that catches sharp intra-week reversals but gets crushed in sustained downtrends where oversold keeps getting more oversold.

*Overfit 7/10 — %R(2) is a non-standard period far from the conventional 14, thresholds of -90/-10 are aggressively tuned.*

- **Entry:** Williams %R(2) < -90 (oversold)
- **Exit:** Williams %R(2) > -10 (overbought)
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -42% | 0.912 | 242 | 90 | 2.69 | 0.95 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 9% | 🟢 18% | 🟢 41% | 🟢 49% | 🔴 -19% | 🟢 64% | 🟢 347% | 🟢 17% | 🔴 -3% | 🟢 110% | 🟢 37% | 🟢 10% |

> [!code]- Click to view: algo_053.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_053.py"
> ```


---

## Strategy-45
### TQQQ + SMA200 (algo_055.py)

**Description:** Applies the classic 200-day SMA trend filter to TQQQ (3× Nasdaq-100), holding when TQQQ's close is above its own 200-day SMA and liquidating to cash when it falls below. Replacing NVDA with TQQQ dramatically changes the character: TQQQ's 3× daily leverage means the SMA breaches earlier and more frequently in downtrends, reducing drawdown (-50% vs -42% for NVDA) but also cutting CAGR sharply (33% vs 64%). The strategy is essentially identical to #008 (TQQQ self-SMA200) and the 33% CAGR with 0.76 Sharpe confirms the performance is comparable.

*Overfit 4/10 — the SMA(200) is a standard, widely-used lookback with no tuning, but cherry-picking the single best-performing large-cap strategy and applying it to a 3× leveraged ETF introduces hindsight bias.*

- **Entry:** TQQQ price > SMA(200)
- **Exit:** TQQQ price < SMA(200)
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -50% | 0.76 | 18 | 41 | 0.44 | 16.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 11% | 🔴 -20% | 🟢 118% | 🟢 8% | 🟢 40% | 🟢 69% | 🟢 88% | 🔴 -21% | 🟢 68% | 🟢 41% | 🟢 16% |

> [!code]- Click to view: algo_055.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_055.py"
> ```


---

## Strategy-46
### %R(2) hybrid (algo_056.py)

**Description:** Two-regime strategy on TQQQ using QQQ's 150-day SMA as a market health filter. When QQQ is above its SMA (bull trend), it buys TQQQ and holds continuously. When QQQ is below the SMA, it switches to mean-reversion: only buying on extreme %R(2) < -95 oversold prints and selling on %R(2) > -10.

*Overfit 8/10 — %R(2) with a -95/-10 threshold pair is more aggressively tuned than even algo 053, SMA(150) is a non-standard departure from the conventional 200.*

- **Entry:** QQQ > SMA(150) = buy TQQQ; QQQ < SMA(150) and %R(2) < -95 = buy TQQQ
- **Exit:** QQQ < SMA(150) while in trend mode = liquidate; in MR mode and %R(2) > -10 = liquidate
- **Symbols:** TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 51% | -56% | 0.996 | 55 | 50 | 1.10 | 5.92 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 17% | 🟢 9% | 🟢 118% | 🔴 -21% | 🟢 53% | 🟢 191% | 🟢 88% | 🔴 -4% | 🟢 164% | 🟢 64% | 🟢 28% |

> [!code]- Click to view: algo_056.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_056.py"
> ```


---

## Strategy-47
### TQQQ hybrid (SMA+IBS) (algo_060.py)

**Description:** A dual-regime strategy on TQQQ that combines trend-following with extreme dip-buying. In trend mode (TQQQ above SMA200), it holds TQQQ continuously. In down-trend mode, it switches to mean-reversion: entering only when IBS drops below 0.05 (extreme selling pressure within the day) and exiting when IBS recovers above 0.70. Replacing NVDA with TQQQ preserves the hybrid structure but reduces CAGR from 68% to 49% and Sharpe from 1.44 to 0.99, as TQQQ's leverage amplifies whipsaw losses when the SMA gate flips.

*Overfit 6/10 — both IBS thresholds (0.05, 0.70) are clearly tuned; applying NVDA-specific parameters to TQQQ adds another degree of specification bias.*

- **Entry:** If TQQQ > SMA200 → hold TQQQ. If below SMA200 and IBS < 0.05 → buy TQQQ
- **Exit:** Trend mode and price < SMA200 → liquidate. MR mode and IBS > 0.70 → liquidate
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 49% | -50% | 0.988 | 69 | 58 | 1.19 | 4.69 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 9% | 🟢 4% | 🟢 118% | 🔴 -8% | 🟢 36% | 🟢 259% | 🟢 88% | 🔴 -11% | 🟢 75% | 🟢 59% | 🟢 48% |

> [!code]- Click to view: algo_060.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_060.py"
> ```


---

## Strategy-48
### TQQQ + SMA150 (algo_061.py)

**Description:** A pure trend-following strategy on TQQQ using a 150-day SMA as the regime filter — invested when TQQQ closes above its 150-day moving average, flat when below. This is essentially a re-run of #009 (TQQQ self-SMA150) with identical parameters. The results confirm the match: 29% CAGR / -53% MaxDD / 0.69 Sharpe vs #009's 29% / -53% / 0.69. The shorter SMA150 lookback exits trends more quickly than SMA200 but also generates more whipsaw on TQQQ's volatile daily swings.

*Overfit 6/10 — SMA150 is non-standard and appears to be a tuned middle-ground between common values (100, 200); applying a single-stock parameter to a leveraged ETF adds bias.*

- **Entry:** TQQQ > SMA(150) → go all-in
- **Exit:** TQQQ <= SMA(150) → liquidate to cash
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -53% | 0.692 | 24 | 59 | 0.41 | 10.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 42% | 🟢 1% | 🔴 -5% | 🟢 118% | 🔴 -23% | 🟢 16% | 🟢 93% | 🟢 64% | 🔴 -22% | 🟢 76% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: algo_061.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_061.py"
> ```


---

## Strategy-49
### 5 most mkt cap + IBS regime mix (algo_064.py)

**Description:** Switches between two regimes based on QQQ relative to its 200-day SMA. In trend mode (QQQ above SMA200), it holds all five most market capital companies equal-weight. In non-trend mode, it only holds names where IBS is below 0.2, acting as an oversold mean-reversion filter. The regime mix gives it the best MaxDD in the set (-23%) — the IBS filter successfully sidesteps the worst of bear markets.

*Overfit 3/10 — SMA200 is a standard lookback. The IBS<0.2 threshold is the single tuned parameter; it is reasonable but untested against alternatives.*

- **Entry:** Trend mode (QQQ > SMA200): equal weight all 5. No-trend mode: only names with IBS < 0.2, equal-weighted
- **Exit:** When QQQ < SMA200 and a held name no longer has IBS < 0.2, liquidate
- **Symbols:** QQQ (signal), Top 5 US equities by market cap (dynamic universe)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -23% | 1.073 | 828 | 650 | 1.27 | 2.07 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 11% | 🟢 5% | 🟢 4% | 🟢 38% | 🟢 15% | 🟢 47% | 🟢 95% | 🟢 46% | 🔴 -11% | 🟢 51% | 🟢 38% | 🟢 50% |

> [!code]- Click to view: algo_064.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_064.py"
> ```


---

## Strategy-50
### TQQQ hybrid + ATR (algo_066.py)

**Description:** A two-mode TQQQ strategy gated by SMA200. When TQQQ trades above the 200-day SMA, it takes a full long position. When below, it switches to mean-reversion: entering only when IBS drops below 0.05 and exiting when IBS recovers above 0.70 or price hits a 3x ATR stop-loss from entry. Replacing NVDA with TQQQ yields a near-identical result to #060 (49% CAGR / -48% MaxDD vs 49% / -50%), confirming that the ATR stop on TQQQ adds negligible marginal benefit since TQQQ's 3× volatility makes the 3× ATR distance so wide it rarely triggers.

*Overfit 4/10 — SMA(200) and ATR(14) are standard, but both IBS thresholds (0.05 entry, 0.7 exit) and the 3× ATR stop multiplier are tuned values, now applied to a leveraged ETF rather than a single stock.*

- **Entry:** If TQQQ > SMA200 → full position. If below SMA200 and IBS < 0.05 → full MR position
- **Exit:** Trend mode and price < SMA200 → liquidate. MR mode: IBS > 0.70 or price < entry - 3× ATR → liquidate
- **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 49% | -48% | 0.991 | 71 | 58 | 1.22 | 4.32 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 9% | 🔴 -2% | 🟢 118% | 🔴 -1% | 🟢 36% | 🟢 259% | 🟢 88% | 🔴 -11% | 🟢 75% | 🟢 59% | 🟢 48% |

> [!code]- Click to view: algo_066.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_066.py"
> ```


---

## Strategy-51
### 8 Leveraged ETF EW Permanent + Monthly Rebalance (algo_039.py — algos3)

**Description:** Equal-weight basket of 8 leveraged ETFs (TQQQ, UPRO, SOXL, TECL, QLD, SSO, DDM, FAS) with monthly rebalance. Pure cross-sectional rebalancing with no timing signal. This strategy was not converted to the dynamic top-5 universe — the leveraged ETF basket remained intact.

*Overfit 5/10 — zero mechanical parameter tuning, but the 8-ETF basket (TQQQ/UPRO/SOXL/TECL/QLD/SSO/DDM/FAS) is heavy hindsight selection — every name is a tech/financial leveraged ETF that benefited from the 2014–2025 bull run; the same basket pre-2010 would have been catastrophic (leveraged ETFs barely existed). More hindsight-loaded than Strategy 3's 3-ETF version.*

- **Entry:** Monthly rebalance to equal weight (1/8 each)
- **Exit:** None (permanent hold, rebalanced monthly)
- **Symbols:** TQQQ, UPRO, SOXL, TECL, QLD, SSO, DDM, FAS
- **Resolution:** Daily

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -52% | 0.799 | 295 | 166 | 1.78 | 1.04 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -4% | 🔴 -18% | 🟢 15% | 🟢 47% | 🟢 46% | 🟢 9% | 🟢 205% | 🟢 58% | 🔴 -34% | 🟢 90% | 🟢 61% | 🟢 8% |

> [!code]- Click to view: algo_039.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_039.py"
> ```


---

## Strategy-52
### 5x 3x-Leveraged ETF Basket + QQQ Vol Gate (algo_048.py — algos3)

**Description:** Equal-weight basket of 5 leveraged tech ETFs (TQQQ, TECL, SOXL, UPRO, FAS) gated by QQQ 20-day annualized volatility. Invested only when vol < 20%, otherwise flat. The tight vol gate (20% vs typical 30%) makes this a fair-weather strategy that sits out high-volatility periods entirely.

*Overfit 6/10 — two compounding sources: same hindsight ETF basket as Strategy 51, plus a custom 20% QQQ vol gate (the strategy's own description flags this as tight vs the typical 30% threshold). The fair-weather behavior sitting out every high-vol period is the kind of rule that back-fits cleanly to bull-market data and underperforms out-of-sample.*

- **Entry:** QQQ 20d vol < 20% → equal-weight all 5 ETFs
- **Exit:** QQQ 20d vol >= 20% → liquidate
- **Symbols:** TQQQ, TECL, SOXL, UPRO, FAS, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -40% | 1.018 | 69 | 46 | 1.50 | 3.88 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🟢 11% | 🟢 3% | 🟢 70% | 🔴 -4% | 🟢 36% | 🟢 158% | 🟢 57% | 🟢 2% | 🟢 93% | 🟢 46% | 🟢 49% |

> [!code]- Click to view: algo_048.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_048.py"
> ```


---

## Strategy-53
### Dynamic Top-5 EW + Adaptive Vol Gate (algo_057.py — algos3)

**Description:** Holds the top-5 market-cap stocks equal-weight when the basket's recent 20-day volatility is below its longer-term 252-day volatility (calm regime). When short-term vol exceeds the long-term average, it goes to cash. This adaptive gate naturally sidesteps volatility spikes (2020 COVID crash, 2022 rate hikes) while capturing most of the upside in calm bull markets.

*Overfit 2/10 — dynamic top-5 universe removes name-selection bias; the gate compares short-term (20d) to long-term (252d) volatility with no magic threshold — adaptive by construction, essentially zero tuned parameters. One of the cleanest designs in the set.*

- **Entry:** Basket 20d vol < basket 252d vol → equal-weight top-5
- **Exit:** 20d vol >= 252d vol → liquidate
- **Symbols:** Top 5 US equities by market cap (dynamic universe), QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 22% | -40% | 0.74 | 520 | 27 | 19.26 | 1.50 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 11% | 🟢 12% | 🟢 6% | 🟢 33% | 🟢 8% | 🟢 45% | 🟢 53% | 🟢 44% | 🔴 -37% | 🟢 62% | 🟢 32% | 🟢 32% |

> [!code]- Click to view: algo_057.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_057.py"
> ```


---

## Strategy-54
### Dynamic Top-5 Momentum + TQQQ Sleeve + Vol Gate (algo_060.py — algos3)

**Description:** A two-sleeve allocation: 80% in top-5 market-cap stocks weighted by 3-month momentum, 20% in TQQQ. The entire portfolio is gated by TQQQ's 21-day annualized volatility — invested only when vol < 60%. The momentum weighting concentrates exposure in the strongest-performing mega-caps, while the TQQQ sleeve adds a small leverage kick. Monthly momentum recomputation.

*Overfit 5/10 — dynamic universe helps, but four hand-picked parameters stack up: 80/20 split between sleeves, 3-month momentum lookback, 21-day vol window, and 60% vol cutoff. The 60% threshold is unusually loose for TQQQ (typical regime gates use 30–50%) and the 21-day window is on the short side — both smell like they were tuned to keep the strategy engaged through 2020–2021.*

- **Entry:** TQQQ 21d vol < 60% → allocate (80% top-5 momo-weighted, 20% TQQQ)
- **Exit:** TQQQ 21d vol >= 60% → liquidate all
- **Symbols:** Top 5 US equities by market cap (dynamic universe), TQQQ, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 49% | -50% | 0.988 | 69 | 58 | 1.19 | 4.69 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 9% | 🟢 4% | 🟢 118% | 🔴 -8% | 🟢 36% | 🟢 259% | 🟢 88% | 🔴 -11% | 🟢 75% | 🟢 59% | 🟢 48% |

> [!code]- Click to view: algo_060.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_060.py"
> ```


---
