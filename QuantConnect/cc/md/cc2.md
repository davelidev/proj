# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [1](#strategy-1)     | ✅    | Trend           | 34%  | -56%  | 0.757  | 36    | 77    | 0.47     | 13.25        | 2/10   |
| [2](#strategy-2)     | ✅    | Trend/MR Hybrid | 28%  | -56%  | 0.67   | 55    | 102   | 0.54     | 6.85         | 3/10   |
| [3](#strategy-3)     | ✅    | Trend/MR Hybrid | 33%  | -57%  | 0.741  | 57    | 88    | 0.65     | 7.28         | 4/10   |
| [4](#strategy-4)     | ✅    | Mean Reversion  | 36%  | -56%  | 0.82   | 48    | 89    | 0.54     | 7.88         | 3/10   |
| [5](#strategy-5)     | ✅    | Rotation        | 125% | -47%  | 1.869  | 2471  | 2105  | 1.17     | 2.55         | 7/10   |
| [6](#strategy-6)     | ✅    | Mean Reversion  | 30%  | -39%  | 0.757  | 334   | 137   | 2.44     | 0.77         | 3/10   |
| [7](#strategy-7)     | ✅    | Trend           | 30%  | -51%  | 0.715  | 120   | 70    | 1.71     | 4.25         | 3/10   |
| [8](#strategy-8)     | ✅    | Dip Buy         | 30%  | -39%  | 0.864  | 384   | 68    | 5.65     | 5.11         | 4/10   |
| [9](#strategy-9)     | ✅    | Rotation        | 29%  | -48%  | 0.692  | 127   | 109   | 1.17     | 3.15         | 5/10   |


---
## Strategy-1
### TQQQ SMA Trend (it_3.py)

**Description:** Baseline 200-day SMA filter on QQQ to manage TQQQ exposure.

*Overfit 2/10 — Industry standard parameter*

- **Trend gate:** QQQ close > SMA(200)
- **Entry:** QQQ > SMA(200) → 100% TQQQ
- **Exit:** QQQ ≤ SMA(200) → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -56% | 0.757 | 36 | 77 | 0.47 | 13.25 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 105% | 🟢 88% | 🔴 -44% | 🟢 113% | 🟢 62% | 🟢 24% |

> [!code]- Click to view: it_3.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/it_3.py"
> ```


---

## Strategy-2
### Trend Vol Hybrid (it_23.py)

**Description:** Combines SMA trend following with a VIX panic filter.

*Overfit 3/10 — Adds one macro volatility filter*

- **Trend gate:** QQQ close > SMA(200)
- **Entry:** QQQ > SMA(200) AND VIX < 30 → 100% TQQQ
- **Exit:** QQQ ≤ SMA(200) OR VIX ≥ 30 → 100% BIL
- **Symbols:** Signal: QQQ + VIX. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 28% | -56% | 0.67 | 55 | 102 | 0.54 | 6.85 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -32% | 🟢 50% | 🟢 59% | 🟢 68% | 🔴 -44% | 🟢 113% | 🟢 58% | 🟢 24% |

> [!code]- Click to view: it_23.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/it_23.py"
> ```


---

## Strategy-3
### Vol Ratio Trend (it_35.py)

**Description:** SMA trend following with a short/long-term volatility ratio filter.

*Overfit 4/10 — Adds volatility lookback ratios*

- **Trend gate:** QQQ close > SMA(200)
- **Entry:** QQQ > SMA(200) AND STD(10)/STD(60) < 1.2 → 100% TQQQ
- **Exit:** QQQ ≤ SMA(200) OR vol ratio ≥ 1.2 → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -57% | 0.741 | 57 | 88 | 0.65 | 7.28 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 53% | ⚪ 0% | 🔴 -22% | 🟢 118% | 🔴 -24% | 🟢 50% | 🟢 105% | 🟢 88% | 🔴 -44% | 🟢 118% | 🟢 55% | 🟢 34% |

> [!code]- Click to view: it_35.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/it_35.py"
> ```


---

## Strategy-4
### Trend Stretch Exit (it_41.py)

**Description:** Trend following with mean-reversion "stretch" thresholds for exits.

*Overfit 3/10 — Specific stretch thresholds*

- **Trend gate:** QQQ close > SMA(200)
- **Entry:** QQQ > SMA(200) AND stretch = (price - SMA)/SMA < 15% → 100% TQQQ
- **Exit:** QQQ < SMA(200) OR stretch > 20% → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -56% | 0.82 | 48 | 89 | 0.54 | 7.88 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 60% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 136% | 🟢 77% | 🔴 -44% | 🟢 108% | 🟢 86% | 🟢 24% |

> [!code]- Click to view: it_41.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/it_41.py"
> ```


---

## Strategy-5
### LETF Simple Rotation (it_101.py)

**Description:** Advanced 3-of-4 regime vote (SPY, QQQ, SMH, SOXL) with overbought hedges.

*Overfit 7/10 — High complexity, multiple tickers and states*

- **Regime gate:** 3-of-4 vote: SPY, QQQ, SMH, SOXL each > SMA(202) → BULL if ≥ 3 votes
- **Bull overbought (R1):** BULL AND any RSI(15) on {SPY, QQQ, SMH, SOXL} > 72 → 100% UVIX (UVXY proxy pre-2022-03-30)
- **Bull default (R3):** BULL AND not overbought → 50% TQQQ + 50% SOXL
- **Bear bounce (R4):** BEAR AND (QQQ RSI(8) < 29 OR SMH RSI(8) < 31) → 100% SOXL
- **Bear default (R5):** BEAR otherwise → 100% cash
- **Symbols:** Signal: SPY, QQQ, SMH, SOXL. Execution: TQQQ, SOXL, UVIX/UVXY
- **Rebalance:** Daily, 15 min before market close

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 125% | -47% | 1.869 | 2471 | 2105 | 1.17 | 2.55 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 64% | 🔴 -11% | 🟢 58% | 🟢 139% | 🟢 20% | 🟢 136% | 🟢 1028% | 🟢 260% | 🟢 17% | 🟢 66% | 🟢 187% | 🟢 370% |

> [!code]- Click to view: it_101.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/it_101.py"
> ```


---

## Strategy-6
### TQQQ IBS Dip (0.25/0.90, SMA200)

**Description:** Internal Bar Strength (close position within high-low range) on the QQQ index triggers entry into leveraged Nasdaq exposure when IBS drops below 0.25 and the index is above its 200-day average. Exits when bars close near their highs (IBS > 0.90) or the long-term trend breaks down.

*Overfit 3/10 — IBS<0.25 is a standard published threshold; SMA(200) is canonical. Two tuned parameters total.*

- **Trend gate:** QQQ close > SMA(200)
- **Entry:** IBS(QQQ) < 0.25 → buy 100% TQQQ
- **Exit:** IBS > 0.90 OR trend break
- **Symbols:** Signal: QQQ. Execution: TQQQ
- **Rebalance:** Daily at -10 min before close (uses today's full bar)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -39% | 0.757 | 334 | 137 | 2.44 | 0.77 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 13% | 🔴 -23% | 🟢 10% | 🟢 88% | 🔴 -22% | 🟢 22% | 🟢 175% | 🟢 91% | 🔴 -8% | 🟢 73% | 🟢 16% | 🟢 37% |

> [!code]- Click to view: cc2_014.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc2_014.py"
> ```


---

## Strategy-7
### TQQQ Anti-Martingale Pyramid (base 50%, +15% per 5% gain, cap 100%)

**Description:** Starts at 50% TQQQ when QQQ > SMA(200). For every 5% gain above the entry price, adds another 15% allocation until reaching 100%. Liquidates on trend break. Implements the 'let winners run / cut losers' principle discussed in the 'Antifragile / 2025 best year' thread — pyramiding into strength rather than averaging into weakness.

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

> [!code]- Click to view: cc3_022.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_022.py"
> ```


---

## Strategy-8
### Mega-Cap Value Averaging (cc4_007.py)

**Description:** Universe-driven dip-buy on the five largest-cap U.S. stocks (selected from the top 100 by dollar volume, then ranked by market cap each universe refresh). Whenever a name pulls back more than 5% from its 20-day high it gets a 20% portfolio allocation, and the position is liquidated the moment price prints a new 20-day high. The construction sidesteps single-stock bets by spreading 100% nominal exposure across five mega-caps, and only sells into strength — never on weakness — so a position can sit in drawdown indefinitely until a fresh high releases it.

*Overfit 4/10 — Two tuned numbers (5% dip threshold, 20-day high lookback) and a hindsight-driven universe — 'top 5 by market cap' over 2014–2025 maps directly onto the mega-cap tech complex (AAPL/MSFT/AMZN/GOOGL/META/NVDA), which is the regime the backtest favors. The rule itself (buy weakness in an uptrend, exit on new highs) is a standard value-averaging template; no exotic indicators or per-asset tuning.*

- **Universe:** Top 100 stocks by dollar volume → top 5 by market cap (daily refresh)
- **Entry:** Price < 20-day high × 0.95 → buy 20% allocation
- **Exit:** Price ≥ 20-day high → liquidate
- **Sizing:** Fixed 20% per name (5 names → 100% gross when fully loaded)
- **Resolution:** Daily bars

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -39% | 0.864 | 384 | 68 | 5.65 | 5.11 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 22% | 🟢 16% | 🟢 14% | 🟢 49% | 🔴 -4% | 🟢 61% | 🟢 57% | 🟢 50% | 🔴 -34% | 🟢 76% | 🟢 75% | 🟢 28% |

> [!code]- Click to view: cc4_007.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc4_007.py"
> ```


---

## Strategy-9
### Nasdaq-100 Breadth Rotation (cc4_010.py)

**Description:** Uses participation across the 10 largest-cap U.S. stocks (drawn from the top 100 by dollar volume) as a breadth regime gate for TQQQ. Each constituent runs a 50-day EMA, and the strategy measures the fraction trading above its EMA: above 60% it goes 100% long TQQQ, below 40% it liquidates, and in the 40–60% no-man's-land it holds whatever it had. The mega-cap basket acts as a proxy for Nasdaq leadership health — when participation is broad the engine ramps full 3× exposure, and when it deteriorates it steps fully aside.

*Overfit 5/10 — Three tuned thresholds (50-day EMA period, 60% bull cutoff, 40% bear cutoff) and a regime-defining universe choice. The 60/40 asymmetric hysteresis is a reasonable design choice (prevents whipsaws around 50%) but the specific levels are unverified. The 'top 10 by market cap' basket suffers the same hindsight asset-selection bias as #14 — over 2014–2025 it locks in the mega-cap tech leadership that the strategy then leverages 3× into.*

- **Universe:** Top 100 stocks by dollar volume → top 10 by market cap (signal basket)
- **Indicator:** 50-day EMA per constituent; breadth = fraction trading above EMA
- **Bull entry:** Breadth > 60% → 100% TQQQ
- **Bear exit:** Breadth < 40% → liquidate TQQQ
- **Symbols:** Signal: top-10 mega-cap basket. Execution: TQQQ
- **Resolution:** Daily bars

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -48% | 0.692 | 127 | 109 | 1.17 | 3.15 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 11% | 🟢 2% | 🔴 -7% | 🟢 118% | 🔴 -29% | 🟢 33% | 🟢 127% | 🟢 41% | 🔴 -34% | 🟢 73% | 🟢 46% | 🟢 82% |

> [!code]- Click to view: cc4_010.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc4_010.py"
> ```


---
