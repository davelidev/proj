# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [1](#strategy-1)     | ❌    | Breakout        | 26%  | -36%  | 0.754  | 1009  | 1645  | 0.61     | 2.14         | 4/10   |
| [2](#strategy-2)     | ✅    | Breakout        | 41%  | -50%  | 0.916  | 119   | 93    | 1.28     | 2.49         | 5/10   |
| [3](#strategy-3)     | ✅    | Breakout        | 39%  | -51%  | 0.862  | 78    | 69    | 1.13     | 2.45         | 5/10   |
| [4](#strategy-4)     | ✅    | Breakout        | 39%  | -50%  | 0.859  | 81    | 66    | 1.23     | 2.34         | 4/10   |
| [5](#strategy-5)     | ✅    | Breakout        | 36%  | -50%  | 0.851  | 81    | 67    | 1.21     | 2.32         | 3/10   |
| [6](#strategy-6)     | ✅    | Breakout        | 31%  | -57%  | 0.723  | 92    | 109   | 0.84     | 2.41         | 3/10   |
| [7](#strategy-7)     | ✅    | Dip Buy         | 39%  | -28%  | 1.335  | 1160  | 681   | 1.70     | 1.30         | 8/10   |
| [8](#strategy-8)     | ✅    | Dip Buy         | 36%  | -52%  | 0.817  | 10    | 25    | 0.40     | 23.67        | 5/10   |
| [9](#strategy-9)     | ✅    | Dip Buy         | 32%  | -50%  | 0.772  | 57    | 24    | 2.38     | 1.45         | 3/10   |
| [10](#strategy-10)   | ✅    | Rotation        | 95%  | -56%  | 1.52   | 100   | 85    | 1.18     | 4.51         | 5/10   |
| [11](#strategy-11)   | ✅    | Mean Reversion  | 31%  | -55%  | 0.844  | 39    | 34    | 1.15     | 2.59         | 2/10   |
| [12](#strategy-12)   | ❌    | Mean Reversion  | 27%  | -44%  | 0.835  | 452   | 254   | 1.78     | 1.22         | 2/10   |
| [13](#strategy-13)   | ❌    | Momentum        | 27%  | -37%  | 0.788  | 98    | 51    | 1.92     | 3.35         | 3/10   |
| [14](#strategy-14)   | ✅    | Rotation        | 54%  | -24%  | 1.339  | 305   | 172   | 1.77     | 2.74         | 9/10   |
| [15](#strategy-15)   | ✅    | Rotation        | 54%  | -24%  | 1.339  | 305   | 172   | 1.77     | 2.74         | 9/10   |
| [16](#strategy-16)   | ✅    | Rotation        | 95%  | -56%  | 1.52   | 100   | 85    | 1.18     | 4.51         | 5/10   |
| [17](#strategy-17)   | ✅    | Rotation        | 38%  | -54%  | 0.818  | 220   | 228   | 0.96     | 1.98         | 6/10   |
| [18](#strategy-18)   | ✅    | Dip Buy         | 50%  | -37%  | 1.076  | 1440  | 588   | 2.45     | 0.81         | 4/10   |
| [19](#strategy-19)   | ✅    | Trend           | 158% | -56%  | 2.224  | 276   | 119   | 2.32     | 1.67         | 8/10   |
| [20](#strategy-20)   | ✅    | Trend           | 28%  | -50%  | 0.825  | 37    | 20    | 1.85     | 2.45         | 3/10   |
| [21](#strategy-21)   | ✅    | Trend           | 31%  | -49%  | 0.738  | 100   | 47    | 2.13     | 1.44         | 4/10   |
| [22](#strategy-22)   | ✅    | Rebalance       | 37%  | -52%  | 0.848  | 38    | 0     | —        | —            | 4/10   |
| [23](#strategy-23)   | ✅    | Trend           | 33%  | -56%  | 0.753  | 10    | 47    | 0.21     | 28.85        | 1/10   |
| [24](#strategy-24)   | ✅    | Trend           | 40%  | -55%  | 0.871  | 21    | 36    | 0.58     | 14.75        | 2/10   |
| [25](#strategy-25)   | ✅    | Trend           | 33%  | -50%  | 0.76   | 18    | 41    | 0.44     | 16.03        | 3/10   |
| [26](#strategy-26)   | ✅    | Trend           | 29%  | -53%  | 0.692  | 24    | 59    | 0.41     | 10.03        | 3/10   |
| [27](#strategy-27)   | ✅    | Trend           | 29%  | -49%  | 0.703  | 10    | 47    | 0.21     | 28.86        | 2/10   |
| [28](#strategy-28)   | ✅    | Mean Reversion  | 35%  | -50%  | 0.817  | 498   | 245   | 2.03     | 0.85         | 2/10   |
| [29](#strategy-29)   | ✅    | Rotation        | 33%  | -55%  | 0.829  | 569   | 49    | 11.61    | 1.89         | 5/10   |
| [30](#strategy-30)   | ✅    | Mean Reversion  | 47%  | -47%  | 1.05   | 269   | 100   | 2.69     | 1.00         | 3/10   |
| [31](#strategy-31)   | ✅    | Mean Reversion  | 37%  | -42%  | 0.843  | 361   | 162   | 2.23     | 0.88         | 4/10   |
| [32](#strategy-32)   | ✅    | Mean Reversion  | 32%  | -40%  | 0.903  | 214   | 79    | 2.71     | 0.97         | 3/10   |
| [33](#strategy-33)   | ✅    | Mean Reversion  | 46%  | -43%  | 1.049  | 271   | 106   | 2.56     | 0.96         | 3/10   |
| [34](#strategy-34)   | ✅    | Mean Reversion  | 31%  | -47%  | 0.791  | 170   | 60    | 2.83     | 0.96         | 4/10   |
| [35](#strategy-35)   | ✅    | Mean Reversion  | 36%  | -35%  | 0.915  | 328   | 141   | 2.33     | 0.96         | 3/10   |
| [36](#strategy-36)   | ✅    | Mean Reversion  | 39%  | -55%  | 0.917  | 237   | 92    | 2.58     | 0.98         | 4/10   |
| [37](#strategy-37)   | ✅    | Mean Reversion  | 30%  | -52%  | 0.799  | 295   | 166   | 1.78     | 1.04         | 5/10   |
| [38](#strategy-38)   | ✅    | Trend/MR Hybrid | 50%  | -56%  | 0.986  | 52    | 45    | 1.16     | 5.27         | 5/10   |
| [39](#strategy-39)   | ✅    | Trend/MR Hybrid | 51%  | -55%  | 1.002  | 57    | 44    | 1.30     | 4.54         | 5/10   |
| [40](#strategy-40)   | ✅    | Trend/MR Hybrid | 51%  | -58%  | 1.01   | 57    | 44    | 1.30     | 4.53         | 5/10   |
| [41](#strategy-41)   | ✅    | Mean Reversion  | 55%  | -55%  | 1.068  | 62    | 49    | 1.27     | 4.76         | 5/10   |
| [42](#strategy-42)   | ✅    | Trend/MR Hybrid | 52%  | -56%  | 1.027  | 77    | 60    | 1.28     | 2.77         | 6/10   |
| [43](#strategy-43)   | ✅    | Trend/MR Hybrid | 40%  | -40%  | 1.018  | 69    | 46    | 1.50     | 3.88         | 4/10   |
| [44](#strategy-44)   | ✅    | Mean Reversion  | 40%  | -42%  | 0.912  | 242   | 90    | 2.69     | 0.95         | 2/10   |
| [45](#strategy-45)   | ✅    | Trend           | 33%  | -50%  | 0.76   | 18    | 41    | 0.44     | 16.03        | 3/10   |
| [46](#strategy-46)   | ✅    | Trend/MR Hybrid | 51%  | -56%  | 0.996  | 55    | 50    | 1.10     | 5.92         | 5/10   |
| [47](#strategy-47)   | ✅    | Trend/MR Hybrid | 49%  | -50%  | 0.988  | 69    | 58    | 1.19     | 4.69         | 5/10   |
| [48](#strategy-48)   | ✅    | Trend           | 29%  | -53%  | 0.692  | 24    | 59    | 0.41     | 10.03        | 3/10   |
| [49](#strategy-49)   | ✅    | Trend/MR Hybrid | 30%  | -23%  | 1.073  | 828   | 650   | 1.27     | 2.07         | 3/10   |
| [50](#strategy-50)   | ✅    | Trend/MR Hybrid | 49%  | -48%  | 0.991  | 71    | 58    | 1.22     | 4.32         | 5/10   |
| [51](#strategy-51)   | ❌    | Rotation        | 32%  | -70%  | 0.707  | 842   | 44    | 19.14    | 3.66         | 2/10   |
| [52](#strategy-52)   | ❌    | Rotation        | 27%  | -43%  | 0.709  | 219   | 166   | 1.32     | 2.50         | 4/10   |
| [53](#strategy-53)   | ❌    | Mean Reversion  | 25%  | -17%  | 1.08   | 297   | 160   | 1.86     | 2.58         | 3/10   |
| [54](#strategy-54)   | ❌    | Momentum        | 24%  | -27%  | 0.827  | 455   | 256   | 1.78     | 2.15         | 6/10   |


---
## Strategy-1
### Volatility Squeeze Alpha (z_gold_oil_breakout.py)

**Description:** Trades volatility 'squeezes' in two commodity CFDs (Gold and Oil) on the OANDA broker. Waits for price to be above its 50-day EMA, then watches for a Bollinger Band 'squeeze' (volatility compression) followed by an upside breakout — that's the entry. Position sizes are sized by a risk-per-trade rule rather than a fixed allocation, and exits use a volatility-adaptive trailing stop that tightens as the trade goes into profit. Trades hourly bars.

*Overfit 4/10 — BB-squeeze + EMA filter is a well-documented pattern; the risk-sized position sizing is a defensible practice. Three real concerns: (1) the BB-width threshold at 1.1× rolling average is a tuned magic number, (2) the dual-multiplier ATR stop (1.5× / 2.5× based on a 2% profit threshold) introduces hand-fitted breakpoints, and (3) trading Gold/Oil CFDs is a narrow asset universe — limits the strategy's edge to commodity-specific behavior with limited historical depth.*

- **Entry:** Price > daily EMA(50) AND Bollinger Band squeeze (BB width below 1.1× rolling-100 average) AND price breaks above BB upper band
- **Position size:** (equity × 2.5%) ÷ stop_distance — halved (1.25%) when in a >15% drawdown
- **Stop-loss:** Trailing: 1.5× ATR(14) once profit > 2%, else 2.5× ATR(14)
- **Exit:** Price below trailing stop OR price below daily EMA(50); 12-hour cooldown before re-entry
- **Symbols:** XAUUSD (Gold), WTICOUSD (Oil) — CFDs on OANDA
- **Resolution:** Hourly bars (with daily EMA filter)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 26% | -36% | 0.754 | 1009 | 1645 | 0.61 | 2.14 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -15% | 🔴 -13% | 🟢 1% | 🟢 19% | 🟢 15% | 🔴 -8% | 🟢 108% | 🟢 10% | 🟢 51% | 🟢 55% | 🟢 56% | 🟢 97% |

> [!code]- Click to view: cc_001.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_001.py"
> ```


---

## Strategy-2
### Research S38 - Vol Expansion + SOXL/TQQQ + VIX Shield (strategy_38.py)

**Description:** Same shape as Strategy 4 (trend + breakout + vehicle rotation between TQQQ and SOXL) but adds a 'kill switch' on VIX-term-structure backwardation: when short-term VIX runs above 3-month VIX by more than 10%, the strategy goes fully to cash regardless of other signals. The idea is to sidestep volatility regime breaks — when near-term fear exceeds longer-dated, sharp drawdowns often follow.

*Overfit 5/10 — Inherits Strategy 4's parameter density (SMA200, ADX25, ADX30 turbo, 3×ATR stop) and adds a VIX/VIX3M > 1.10 backwardation gate. The 1.10 cutoff is a tuned threshold (typical 'backwardation' is just >1.0); the rule itself is grounded in volatility-term-structure literature but the specific level needs out-of-sample validation.*

- **Trend gate:** QQQ > SMA(200)
- **Breakout trigger:** Today's QQQ range > yesterday's range
- **Strength filter:** ADX(10) > 25
- **Kill switch:** VIX / VIX3M > 1.10 → liquidate all (backwardation = panic regime)
- **Entry:** ADX > 30 AND SOXL 21d momentum > TQQQ 21d momentum → SOXL; else → TQQQ
- **Stop-loss:** 3.0× ATR(14) trailing
- **Exit:** Stop hit OR QQQ < SMA(200) OR kill switch trips
- **Symbols:** TQQQ, SOXL (executions); QQQ, VIX, VIX3M (signals)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 41% | -50% | 0.916 | 119 | 93 | 1.28 | 2.49 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 115% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 13% | 🟢 16% | 🟢 184% | 🟢 95% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% |

> [!code]- Click to view: cc_002.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_002.py"
> ```


---

## Strategy-3
### Research S36 - Triple-LETF Rotator + Expanding Range (strategy_36.py)

**Description:** Trend-following rotator across three leveraged tech ETFs (TQQQ, SOXL, TECL). Waits for confirmed market uptrend + a breakout day, then picks whichever of the three has the strongest recent momentum. A second-tier 'turbo' filter (ADX > 30) only allows the rotation to pick SOXL or TECL when the trend is unusually strong; otherwise it defaults to TQQQ.

*Overfit 5/10 — Same parameter stack as Strategy 2/4 (SMA200, ADX25, ADX30 turbo, 3×ATR stop) but adds two more leveraged tech ETFs to rotate across — TECL added to the SOXL/TQQQ pair. The 3-way momentum rank inside the ADX>30 branch is one more degree of freedom; expands hindsight bias on instrument selection since all three ETFs are sector-specific tech bets.*

- **Trend gate:** QQQ > SMA(200)
- **Breakout trigger:** Today's QQQ range > yesterday's range
- **Strength filter:** ADX(10) > 25
- **Entry:** If ADX > 30 → pick highest of (TQQQ, SOXL, TECL) by 21d momentum; else → default TQQQ
- **Stop-loss:** 3.0× ATR(14) trailing
- **Exit:** Stop hit OR QQQ < SMA(200)
- **Symbols:** TQQQ, SOXL, TECL (executions); QQQ (signal)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -51% | 0.862 | 78 | 69 | 1.13 | 2.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 141% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 27% | 🟢 17% | 🟢 71% | 🟢 115% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% |

> [!code]- Click to view: cc_003.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_003.py"
> ```


---

## Strategy-4
### Research S35 - Expanding Strong Trend + SOXL + ADX (strategy_35.py)

**Description:** A trend-following rotator that chooses between two leveraged tech ETFs on confirmed breakout days. Waits for the market to be in a clear uptrend, then enters either the leveraged Nasdaq ETF (TQQQ) or the leveraged semiconductor ETF (SOXL) — picking semis only when the trend is unusually strong and semis have been outperforming. Exits when the price falls below a volatility-based trailing stop.

*Overfit 4/10 — Standard indicators (SMA200, ADX, ATR) at conventional thresholds; expanding-range trigger is a documented pattern. Main concern is the second-level 'Turbo' filter (ADX>30 + SOXL momentum) that adds a rotation parameter; also the source docstring claims 2.5× ATR stop but code uses 3.0× — parameter tuning happened between drafts.*

- **Trend gate:** QQQ > SMA(200)
- **Breakout trigger:** Today's QQQ range > yesterday's range
- **Strength filter:** ADX(10) > 25
- **Entry:** ADX > 30 AND SOXL 21d momentum > TQQQ 21d momentum → SOXL; else → TQQQ
- **Stop-loss:** 3.0× ATR(14) trailing
- **Exit:** Stop hit OR QQQ < SMA(200)
- **Symbols:** TQQQ, SOXL (executions); QQQ (signal)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -50% | 0.859 | 81 | 66 | 1.23 | 2.34 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 141% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 28% | 🟢 16% | 🟢 83% | 🟢 95% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% |

> [!code]- Click to view: cc_004.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_004.py"
> ```


---

## Strategy-5
### Research S31 - Expanding Breakout + ADX + 3.0 ATR (strategy_31.py)

**Description:** The simplest member of the 'expanding range' family — just TQQQ. Waits for the market to be in an uptrend, watches for a day where TQQQ's daily range expands beyond yesterday's range, confirms with an ADX trend-strength reading, and goes 100% long. Uses a generous volatility-based trailing stop to give the position room before exiting.

*Overfit 3/10 — Three standard components (SMA200, ADX, ATR) with conventional thresholds. The only tuned parameter is the ADX cutoff (>25) and ATR multiplier (3.0×); both are within the typical range. Cleanest of the expanding-range family — no rotation logic, no turbo filter.*

- **Trend gate:** QQQ > SMA(200)
- **Breakout trigger:** Today's TQQQ range > yesterday's range
- **Strength filter:** ADX(10) > 25
- **Entry:** All three gates pass → 100% TQQQ
- **Stop-loss:** 3.0× ATR(14) trailing
- **Exit:** Stop hit OR QQQ < SMA(200)
- **Symbols:** TQQQ (execution); QQQ (signal)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -50% | 0.851 | 81 | 67 | 1.21 | 2.32 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 141% | 🔴 -3% | 🔴 -6% | 🟢 78% | 🟢 28% | 🟢 11% | 🟢 84% | 🟢 49% | 🔴 -14% | 🟢 81% | 🟢 36% | 🟢 28% |

> [!code]- Click to view: cc_005.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_005.py"
> ```


---

## Strategy-6
### Research S16 - Classic Expanding Breakout + 2.5 ATR (strategy_16.py)

**Description:** The textbook expanding-range entry: when today's TQQQ range is wider than yesterday's, the market is in an uptrend, and there's enough trend strength to confirm. Identical structure to Strategy 5 but with a looser ADX gate (>20 instead of >25) and a tighter ATR stop (2.5× instead of 3.0×) — trades more often, exits sooner.

*Overfit 3/10 — Same template as Strategy 5 with two parameter shifts (ADX 20 vs 25, ATR 2.5× vs 3.0×). The pair of strategies looks like A/B testing of cutoffs which is itself a mild form of fitting — but the magnitudes are reasonable on both sides.*

- **Trend gate:** QQQ > SMA(200)
- **Breakout trigger:** Today's TQQQ range > yesterday's range
- **Strength filter:** ADX(10) > 20
- **Entry:** All three gates pass → 100% TQQQ
- **Stop-loss:** 2.5× ATR(14) trailing
- **Exit:** Stop hit OR QQQ < SMA(200)
- **Symbols:** TQQQ (execution); QQQ (signal)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -57% | 0.723 | 92 | 109 | 0.84 | 2.41 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 93% | 🔴 -24% | 🔴 -19% | 🟢 92% | 🔴 -1% | 🟢 50% | 🟢 135% | 🟢 43% | 🔴 -25% | 🟢 42% | 🟢 87% | 🟢 10% |

> [!code]- Click to view: cc_006.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_006.py"
> ```


---

## Strategy-7
### RSI Frankenfest v1.5 (a_10.py)

**Description:** A decision-tree strategy translated from a Composer 'symphony' — branches through a sequence of RSI and EMA comparisons to pick one of several baskets each day. In bull regime + extreme oversold conditions, it concentrates into 2 of 7 leveraged tech ETFs (highest-volatility pair). In bull regime with normal conditions, it routes based on RSI cross-checks between tech (XLK), trend (KMLM), credit (CORP), transports (IYT), and broad market (SPY) — landing in 100% QLD, an 80/20 QLD/defensive mix, or a single defensive bond. In bear regime, holds the lowest-RSI defensive (counterintuitive — buys the weakest bond, a form of mean reversion).

*Overfit 8/10 — Decision tree with 8+ branches, 6 RSI cutoffs at non-standard windows (RSI-2, RSI-10, RSI-15, RSI-21), and a 10-name defensive list. The 80/20 split with conditional QLD weighting is hand-engineered; the 'top 2 by 20-day stdev' selection inside the deep-dip branch is itself a tuned heuristic. Almost every leaf of this tree could be parameter-fit to the backtest decade. Composer symphonies have a reputation for severe overfitting and this conversion inherits that risk.*

- **Top gate:** QQQ > EMA(200) → bull tree; else → defensive bottom-1
- **Bull deep dip:** RSI(TQQQ, 2) < 20 → top 2 of leveraged bull list by 20d price stdev, 50/50
- **Bull default tree:** If RSI(XLK, 10) > RSI(KMLM, 10) → 80/20 with QLD weighting (see overfit notes); else → defensive bottom-1
- **Defensive selection:** Lowest-RSI(10) from defensive list (BSV/TLT/LQD/VBF/XLP/UGE/XLU/XLV/SPAB/ANGL)
- **Rebalance:** Daily, 1 minute after market open
- **Symbols (offensive):** TQQQ, TECL, SOXL, UPRO, QLD, LTL, ROM
- **Symbols (defensive):** BSV, TLT, LQD, VBF, XLP, UGE, XLU, XLV, SPAB, ANGL
- **Symbols (signals):** QQQ, XLK, KMLM, CORP, IYT, SPY

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -28% | 1.335 | 1160 | 681 | 1.70 | 1.30 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ⚪ 0% | ⚪ 0% | ⚪ 0% | ⚪ 0% | ⚪ 0% | ⚪ 0% | 🟢 4% | 🟢 228% | 🟢 4% | 🟢 118% | 🟢 244% | 🟢 95% |

> [!code]- Click to view: cc_007.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_007.py"
> ```


---

## Strategy-8
### Research S22 - High-Octane RSI Swing TQQQ (strategy_22.py)

**Description:** A high-beta dip-buy that uses signal stocks distinct from the trade vehicle. Watches three momentum leaders (NVDA, AMD, TSLA) for extreme short-term oversold readings (RSI(2) < 20) while QQQ is in an uptrend; when any one of them dips, it buys TQQQ to ride the broader Nasdaq snap-back. Exits quickly on QQQ RSI recovery or trend break.

*Overfit 5/10 — Standard SMA200 trend gate + textbook RSI(2) thresholds. The decoupling of signal symbols (NVDA/AMD/TSLA) from execution (TQQQ) is creative but introduces real hindsight bias — those three names were the top high-beta tech names *of the backtest decade*, knowable only after the fact. The strategy's edge depends on the signal-symbol selection holding up; a different decade with different leaders would fail.*

- **Trend gate:** QQQ > SMA(200)
- **Entry:** Any of NVDA/AMD/TSLA has RSI(2) < 20 → 100% TQQQ
- **Exit:** QQQ RSI(2) > 70 OR QQQ < SMA(200)
- **Symbols:** TQQQ (execution); QQQ, NVDA, AMD, TSLA (signals)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -52% | 0.817 | 10 | 25 | 0.40 | 23.67 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 64% | 🟢 5% | 🔴 -17% | 🟢 118% | 🔴 -5% | 🟢 25% | 🟢 123% | 🟢 88% | 🔴 -27% | 🟢 80% | 🟢 62% | 🟢 27% |

> [!code]- Click to view: cc_008.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_008.py"
> ```


---

## Strategy-9
### Research S11 - Cheat Code Rotator TQQQ (cheat_code_rotator_tqqq.py)

**Description:** Kevin Davey's 'cheat code' formula: enter a leveraged Nasdaq ETF on dips when both the long-term trend and short-term volatility are favorable. Three gates must hold simultaneously — QQQ above its 200-day SMA, VIX below 28, and QQQ RSI(2) below 30. Exits on either short-term overbought readings, a trend break, or a VIX spike above 32.

*Overfit 3/10 — Four indicators, all at conventional thresholds (SMA200, RSI<30/>80, VIX 28/32 — within the standard 25-35 'fear' band). The 28/32 asymmetry between entry-shield and exit-panic is a tuned magic-number pair, but the underlying logic is mainstream technical analysis.*

- **Trend gate:** QQQ > SMA(200)
- **Volatility shield:** VIX < 28
- **Entry:** QQQ RSI(2) < 30 (with both gates passing) → 100% TQQQ
- **Exit:** QQQ RSI(10) > 80 OR QQQ < SMA(200) OR VIX > 32
- **Symbols:** TQQQ (execution); QQQ, VIX (signals)
- **Rebalance:** Daily, 35 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -50% | 0.772 | 57 | 24 | 2.38 | 1.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 68% | 🟢 8% | 🔴 -25% | 🟢 137% | 🔴 -16% | 🟢 20% | 🟢 69% | 🟢 61% | 🔴 -27% | 🟢 104% | 🟢 64% | 🟢 32% |

> [!code]- Click to view: cc_009.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_009.py"
> ```


---

## Strategy-10
### Conservative Rotation (conservative_rotation.py)

**Description:** A defensive long/short rotator: defaults to long leveraged Nasdaq (TQQQ) almost always, but flips to inverse Nasdaq (SQQQ) during sustained bear markets — only when both long-term and short-term trends are negative *and* the market isn't already in a sharp crash. The sharp-crash carve-out is designed to avoid the typical inverse-ETF trap of shorting capitulation lows.

*Overfit 5/10 — Three timing rules layered: long-term trend (SPY < 200d), short-term trend (TQQQ < 20d), crash carve-out (RSI10 not extreme). The carve-out is a non-canonical rule whose specific thresholds (RSI10 < 30 on either QQQ or SPY) look back-fit. Inverse ETFs like SQQQ also suffer from decay over long holding periods, which biases this design toward fast-rotation backtests.*

- **Default:** 100% TQQQ
- **Inverse switch:** SPY < SMA(200) AND TQQQ < SMA(20) AND NOT (RSI(QQQ,10) < 30 OR RSI(SPY,10) < 30) → 100% SQQQ
- **Symbols:** TQQQ, SQQQ (executions); SPY, QQQ (signals)
- **Rebalance:** Daily, 35 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 95% | -56% | 1.52 | 100 | 85 | 1.18 | 4.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 49% | 🔴 -2% | 🟢 59% | 🟢 118% | 🟢 26% | 🟢 95% | 🟢 1020% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% |

> [!code]- Click to view: cc_010.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_010.py"
> ```


---

## Strategy-11
### Large Cap Dip Buy (large_cap_dip_buy.py)

**Description:** Buys oversold dips in the five largest US tech stocks by market cap. Universe is rebuilt automatically from QC's fundamental data, so the holdings rotate as market cap rankings shift. Each name is entered when its RSI(2) drops below 25 and held until the price tags a fresh 52-week (252-day) high.

*Overfit 2/10 — Single-indicator entry (RSI(2)<25) and single-rule exit (52-week high). Dynamic universe eliminates name-selection bias. Weekly rebalance reduces overfitting from frequent re-evaluation. One of the cleanest designs in the set — the only minor tuning is RSI<25 vs the canonical 20 or 30.*

- **Universe:** Top 5 US tech stocks by market cap (Morningstar Technology sector, dynamic)
- **Entry:** Per-name: RSI(2) < 25 AND not already held → buy at 1/5 weight
- **Exit:** Per-name: price ≥ 252-day high → liquidate
- **Rebalance:** Weekly (Monday market open + 5 min)
- **Symbols:** Dynamic — typically AAPL/MSFT/NVDA/GOOG/AVGO etc.

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -55% | 0.844 | 39 | 34 | 1.15 | 2.59 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 9% | 🔴 -1% | 🟢 8% | 🟢 35% | 🟢 8% | 🟢 41% | 🟢 40% | 🟢 62% | 🔴 -42% | 🟢 118% | 🟢 131% | 🟢 39% |

> [!code]- Click to view: cc_011.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_011.py"
> ```


---

## Strategy-12
### Giant Sniper Mean-Reversion (giant_sniper_mean_rev.py)

**Description:** Same shape as Strategy 11 — top-5 mega-caps + RSI(2) dip entry — but with two structural differences. (1) Universe is the top 5 by market cap *across all sectors*, not tech-only, so the basket can include non-tech leaders. (2) Has an explicit bear-market shield: when QQQ falls below its 200-day SMA, the strategy liquidates everything regardless of individual-name signals. Exits are per-name on RSI(2) > 70 instead of price highs.

*Overfit 2/10 — Two textbook indicators (RSI(2) and SMA(200)) with standard thresholds (<20 / >70 / 200d). Dynamic top-5 universe removes name-selection bias. The bear-market shield is the only added complexity and uses the canonical 200d cutoff. A clean, replicable design.*

- **Universe:** Top 5 US stocks by market cap (all sectors, dynamic)
- **Trend shield:** QQQ > SMA(200) required to hold anything
- **Entry:** Bull regime + per-name RSI(2) < 20 → buy at equal weight
- **Exit:** Per-name RSI(2) > 70; OR QQQ < SMA(200) → liquidate all
- **Rebalance:** Daily, 30 min after market open
- **Symbols:** Dynamic — typically AAPL/MSFT/NVDA/GOOG/AMZN etc.

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27% | -44% | 0.835 | 452 | 254 | 1.78 | 1.22 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 15% | 🟢 49% | 🔴 -13% | 🟢 48% | 🔴 -16% | 🟢 7% | 🟢 34% | 🟢 80% | 🔴 -10% | 🟢 43% | 🟢 40% | 🟢 94% |

> [!code]- Click to view: cc_012.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_012.py"
> ```


---

## Strategy-13
### VAA Leveraged (vaa_leveraged.py)

**Description:** Implementation of Wouter Keller's Vigilant Asset Allocation (VAA-G) with a leveraged twist — substitutes TQQQ into the offensive sleeve to push CAGR. Every month, scores 7 ETFs (4 offensive + 3 defensive) using the '13612W' momentum formula (weighted average of 1-, 3-, 6-, 12-month returns). If *all* offensive scores are positive, holds the single highest-scoring offensive; if any offensive score is negative, switches entirely to the highest-scoring defensive (the 'breadth' rule).

*Overfit 3/10 — VAA-G is a published academic strategy (Keller & Keuning 2017), so the core scoring framework and breadth rule are well-documented. The only deviation is swapping the original aggregate-bond offensive (AGG-style) for TQQQ — meaningful hindsight bias for the 2014–2025 leveraged-tech window. Monthly rebalance and the single-asset concentration are conservative choices.*

- **Momentum score:** 13612W = 12·r₁ + 4·r₃ + 2·r₆ + 1·r₁₂ (weighted past returns)
- **Risk-on rule:** All offensive scores > 0 → hold highest-scoring offensive (single-asset)
- **Risk-off rule:** Any offensive score ≤ 0 → hold highest-scoring defensive (single-asset)
- **Rebalance:** Monthly, first trading day, 35 min after market open
- **Symbols (offensive):** TQQQ, EFA, EEM, AGG
- **Symbols (defensive):** LQD, IEF, SHY

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27% | -37% | 0.788 | 98 | 51 | 1.92 | 3.35 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 28% | 🟢 5% | 🟢 10% | 🟢 66% | 🟢 53% | 🟢 49% | 🟢 61% | 🟢 9% | 🔴 -11% | 🟢 15% | 🔴 -2% | 🟢 37% |

> [!code]- Click to view: cc_013.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_013.py"
> ```


---

## Strategy-14
### SOXL.SOXS SeeSaw (a_6.py)

**Description:** A semiconductor seesaw converted from a Composer symphony. Routes between SOXL (3× semis long), SOXS (3× semis short), UVXY (long volatility), and BIL (cash) based on a five-layer decision tree of RSI readings and 6-day cumulative returns. The branches were tuned to capture momentum in either direction of semis while sidestepping range-bound periods (when it parks in cash). Rebalances only when current weights drift more than 10% from target.

*Overfit 9/10 — Composer symphony with 6 hand-tuned numeric thresholds (RSI windows 25/32, RSI cutoffs 62.5/66, return thresholds 34/26.5/-3) — none are standard values. The non-standard RSI windows are particularly suspicious; canonical settings would be 2, 10, or 14. The 10% drift threshold is also non-standard. Composer symphonies have a documented reputation for severe overfitting and every threshold here looks back-fit to the specific 2014-2025 semiconductor cycle.*

- **Top branch:** RSI(SOXS, 25) > 62.5 → lowest 1-day return of [SOXL, UVXY] (i.e. fade the strongest semis-short rally)
- **Second branch:** Else RSI(SOXL, 32) > 66 → lowest 1-day return of [SOXS, UVXY] (fade the strongest semis-long rally)
- **SOXL hot:** Else if SOXL 6-day return > 34% → 100% SOXS (mean-reverse the explosive rally)
- **SOXS hot:** Else if SOXS 6-day return > 26.5%: if SOXS 1-day return < -3% → SOXS; else → SOXL
- **Default:** Else → 100% BIL (cash)
- **Rebalance:** Daily check, executes only when any holding drifts >10% from target weight
- **Symbols:** SOXL, SOXS, UVXY, BIL

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 54% | -24% | 1.339 | 305 | 172 | 1.77 | 2.74 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 1% | 🟢 3% | 🟢 6% | ⚪ 0% | 🟢 118% | 🟢 23% | 🟢 142% | 🟢 74% | 🟢 265% | 🟢 22% | 🟢 36% | 🟢 132% |

> [!code]- Click to view: cc_014.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_014.py"
> ```


---

## Strategy-15
### SOXL.SOXS SeeSaw Duplicate (a_7.py)

**Description:** Byte-for-byte duplicate of Strategy 14 (same SOXL.SOXS SeeSaw symphony). Kept as a copy from the original research notes; the duplication doesn't add information and could be deleted from the catalog.

*Overfit 9/10 — Same rating and rationale as Strategy 14 since the files are literally identical.*

- **See:** Identical to Strategy 14 — same source code, same rules. Marked 'Duplicate' in the metadata name.

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 54% | -24% | 1.339 | 305 | 172 | 1.77 | 2.74 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 1% | 🟢 3% | 🟢 6% | ⚪ 0% | 🟢 118% | 🟢 23% | 🟢 142% | 🟢 74% | 🟢 265% | 🟢 22% | 🟢 36% | 🟢 132% |

> [!code]- Click to view: cc_015.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_015.py"
> ```


---

## Strategy-16
### Rotation Strategy V1 (rotation_v1.py)

**Description:** A leveraged Nasdaq trend strategy with a defensive inverse-ETF fallback. Default position is 100% TQQQ. When SPY breaks below its 200-day SMA *and* TQQQ has also rolled below its 20-day SMA, the strategy flips to 100% SQQQ to short the trend — but only when there's no sharp-crash RSI reading (which would suggest a near-term mean reversion is imminent). Subscribes to a wide symbol set but only trades TQQQ and SQQQ.

*Overfit 5/10 — Three tiered timing rules (SPY trend, TQQQ short-term, crash carve-out) with an RSI<30 cutoff that is on the boundary of conventional. The dead-code branches in the source (commented-out UVXY/TLT/SQQQ paths) suggest active parameter exploration. Trading inverse ETFs over multi-day periods incurs decay drag that the backtest may understate.*

- **Default:** 100% TQQQ
- **Crash buy:** If SPY < SMA(200) AND (RSI(QQQ,10) < 30 OR RSI(SPY,10) < 30) → 100% TQQQ (mean-reversion buy)
- **Inverse switch:** If SPY < SMA(200) AND TQQQ < SMA(20) AND no crash signal → 100% SQQQ
- **Symbols (traded):** TQQQ, SQQQ
- **Symbols (subscribed but unused):** SPY, QQQ, SPXL, UVXY, TECL, UPRO, TLT (legacy from earlier draft branches that are commented out)
- **Rebalance:** Daily, 35 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 95% | -56% | 1.52 | 100 | 85 | 1.18 | 4.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 49% | 🔴 -2% | 🟢 59% | 🟢 118% | 🟢 26% | 🟢 95% | 🟢 1020% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% |

> [!code]- Click to view: cc_016.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_016.py"
> ```


---

## Strategy-17
### Defensive Rotation (defensive_rotation.py)

**Description:** A four-state regime rotation. The state machine: (1) any RSI(10) crash signal → all cash; (2) bull market (TQQQ > SMA200) + uptrend or short-term dip → TQQQ; (3) bear market (TQQQ ≤ SMA200) + downtrend or overbought bounce → SQQQ; (4) anything else → all cash. The crash gate at the top sidesteps the dangerous mid-crash zones where mean-reversion entries blow up.

*Overfit 6/10 — Five tuned thresholds: SMA200, SMA20, RSI(2) at 20/80, RSI(10) at 30. The state-machine is clean conceptually but each branch's cutoff is hand-picked. Source file has duplicate Initialize blocks (indicators registered twice) suggesting copy-paste from another file — minor code smell that hints at hasty iteration.*

- **Crash gate:** RSI(QQQ,10) < 30 OR RSI(SPY,10) < 30 → all cash (no other rules evaluated)
- **Bull entry:** TQQQ > SMA(200) AND (TQQQ > SMA(20) OR RSI(TQQQ,2) < 20) → 100% TQQQ
- **Bear entry:** TQQQ ≤ SMA(200) AND (TQQQ < SMA(20) OR RSI(TQQQ,2) > 80) → 100% SQQQ
- **Else:** All cash
- **Symbols:** TQQQ, SQQQ (executions); SPY, QQQ (signals)
- **Rebalance:** Daily, 35 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -54% | 0.818 | 220 | 228 | 0.96 | 1.98 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 25% | 🔴 -25% | 🔴 -28% | 🟢 99% | 🟢 5% | 🟢 11% | 🟢 225% | 🟢 82% | 🟢 119% | 🟢 30% | 🟢 41% | 🟢 25% |

> [!code]- Click to view: cc_017.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_017.py"
> ```


---

## Strategy-18
### RSI Rebalance (rsi_rebalance.py)

**Description:** A simple regime-flip on QQQ short-term oversold. When QQQ's RSI(2) drops below 25, goes equal-weight long the three leveraged tech ETFs (TQQQ/SOXL/TECL). When the regime flips back (RSI ≥ 25), liquidates to cash. Note: the source contains a defensive-bond fallback branch but it's unreachable due to an early `return` statement — effectively the strategy is binary long-or-cash.

*Overfit 4/10 — Single-indicator regime (RSI(2)<25) is textbook. Equal-weight aggressive basket is reasonable. Two concerns: (1) the start_date computed from `datetime.now() - 12*365 days` is non-deterministic across runs (deprecated pattern); (2) the dead-code defensive branch suggests the strategy was originally more complex and got simplified, but the unreachable code muddies the audit trail.*

- **Regime signal:** QQQ RSI(2) < 25 → 'long' regime; else → 'cash' regime
- **On flip to long:** Liquidate, then equal-weight TQQQ/SOXL/TECL (1/3 each)
- **On flip to cash:** Liquidate everything (defensive bond rotation in source is dead code)
- **Symbols (active):** TQQQ, SOXL, TECL
- **Symbols (dead branch):** TLT, GLD, IEF, AGG, BND, SGOV, BSV
- **Rebalance:** Daily, 35 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 50% | -37% | 1.076 | 1440 | 588 | 2.45 | 0.81 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 21% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 🟢 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 51% |

> [!code]- Click to view: cc_018.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_018.py"
> ```


---

## Strategy-19
### TQQQ Simple Long Term (a_2.py)

**Description:** Another Composer-converted decision tree with two regime arms. **Bull arm** (SPY > SMA200): if any leveraged ETF (TQQQ or SPXL) is in extreme overbought territory (RSI(10) > 79-80), the strategy switches to long UVXY (volatility); otherwise default 100% TQQQ. **Bear arm** (SPY ≤ SMA200): cascading checks — first try a TQQQ oversold-bounce, then SPY oversold-bounce via UPRO, then a defensive rotation between SQQQ and TLT, with a final fallback to SQQQ shorts or TQQQ longs based on more RSI readings.

*Overfit 8/10 — Composer symphony with 7+ decision branches and 5 distinct RSI cutoffs (31, 30, 79, 80, 80) — none rounded to standard values like 30 or 80. The fact that 79 vs 80 is treated as different is a clear sign of threshold-tuning. The bear arm's branching to UVXY (which decays brutally over multi-day holds) suggests the backtest contains specific volatility-spike days that the threshold catches; out-of-sample this would likely fail.*

- **Bull: vol spike:** If RSI(TQQQ,10) > 79 OR RSI(SPXL,10) > 80 → 100% UVXY
- **Bull default:** Else → 100% TQQQ
- **Bear: TQQQ dip:** If RSI(TQQQ,10) < 31 → 100% TQQQ
- **Bear: SPY dip:** Else if RSI(SPY,10) < 30 → 100% UPRO
- **Bear: defensive:** Else if TQQQ < SMA(20) → highest-RSI(10) of [SQQQ, TLT]
- **Bear: SQQQ short entry:** Else if RSI(SQQQ,10) < 31 → 100% SQQQ
- **Bear default:** Else → 100% TQQQ
- **Symbols:** SPY, TQQQ, SQQQ, UVXY, SPXL, UPRO, TLT
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 158% | -56% | 2.224 | 276 | 119 | 2.32 | 1.67 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | ⚪ 0% | 🟢 65% | 🟢 138% | 🟢 70% | 🟢 186% | 🟢 4720% | 🟢 163% | 🟢 186% | 🟢 195% | 🟢 75% | 🟢 76% |

> [!code]- Click to view: cc_019.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_019.py"
> ```


---

## Strategy-20
### Large Cap Tech Strategy (large_cap_ema.py)

**Description:** Same structure as Strategy 11 (top-5 US tech by market cap, weekly rebalance, 252-day high exit) but the entry trigger is different: instead of buying on RSI(2) < 25, this version enters when price drops below its 100-day EMA. So it's catching slower trend-changes rather than short-term oversold spikes.

*Overfit 3/10 — Single-indicator entry (price < EMA100) and single-rule exit (252-day high). Dynamic universe removes name-selection bias. EMA(100) is a non-canonical lookback (vs typical 50/100/200), but only one parameter is tuned. Compared to Strategy 11 (RSI dip), the EMA trigger fires more often and on slower signals — different risk profile, similar overfit floor.*

- **Universe:** Top 5 US tech stocks by market cap (Morningstar Technology sector, dynamic)
- **Entry:** Per-name: price < EMA(100) AND not already held → buy at 1/5 weight
- **Exit:** Per-name: price ≥ 252-day high → liquidate
- **Rebalance:** Weekly (Monday market open at 10:05)
- **Symbols:** Dynamic — typically AAPL/MSFT/NVDA/GOOG/AVGO etc.

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 28% | -50% | 0.825 | 37 | 20 | 1.85 | 2.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 17% | 🟢 1% | 🟢 6% | 🟢 33% | 🟢 10% | 🟢 43% | 🟢 30% | 🟢 53% | 🔴 -36% | 🟢 92% | 🟢 120% | 🟢 42% |

> [!code]- Click to view: cc_020.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_020.py"
> ```


---

## Strategy-21
### Research S8 - TQQQ Dynamic Compounding (dip_buy_tqqq.py)

**Description:** A graduated-leverage trend strategy on TQQQ. When QQQ is in an uptrend (above 200d SMA), allocates 100% on dips (RSI(2) < 30), drops to 20% when overheated (RSI(10) > 80), or holds 50% as the default. When QQQ falls below its 200d SMA, exits to cash entirely. The three-tier allocation is meant to push compounding by being maximally aggressive on dips and minimally exposed at peaks.

*Overfit 4/10 — RSI thresholds (30, 80) are textbook oversold/overbought levels and SMA(200) is canonical, but the three-tier allocation (20/50/100%) and the RSI(10) > 80 de-lever trigger look hand-fitted; single-ticker focus on TQQQ keeps the parameter space small. Restored from git history (commit cba62e9^); identical in spirit to the active strategies/algos/tqqq_dynamic.py.*

- **Trend gate:** QQQ > SMA(200) → bull mode; else → 100% cash
- **Bull: full leverage:** RSI(QQQ,2) < 30 → 100% TQQQ
- **Bull: de-lever:** RSI(QQQ,10) > 80 → 20% TQQQ
- **Bull: default:** Neither extreme AND not invested → 50% TQQQ
- **Bear exit:** QQQ ≤ SMA(200) → liquidate
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -49% | 0.738 | 100 | 47 | 2.13 | 1.44 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 35% | 🟢 4% | 🔴 -15% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 69% | 🟢 83% | 🔴 -21% | 🟢 70% | 🟢 29% | 🟢 25% |

> [!code]- Click to view: cc_021.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_021.py"
> ```


---

## Strategy-22
### Equal-Weight LETF Rebalance (rebalance.py)

**Description:** A simple yearly rebalance to a fixed weighted basket: 60% leveraged tech split equally across TQQQ/SOXL/TECL (20% each), 40% cash. No signals, no timing — just hold the basket and reset the weights once a year. The cash portion dampens the volatility of the leveraged ETF sleeve.

*Overfit 4/10 — Zero mechanical parameter tuning, but the TQQQ/SOXL/TECL choice is hindsight bias — these three were among the best-performing leveraged ETFs of the backtest decade, knowable only after the fact. 40% cash dampens drawdowns but doesn't address the selection issue. Also uses `datetime.now() - 12*365 days` for the start date — deprecated non-deterministic pattern.*

- **Allocation:** TQQQ 20% / SOXL 20% / TECL 20% / Cash 40%
- **Rebalance:** Yearly (on year-change detection in OnData), after 11:00 ET
- **Entry:** None (permanent hold)
- **Exit:** None (rebalanced only)
- **Symbols:** TQQQ, SOXL, TECL (minute resolution)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -52% | 0.848 | 38 | 0 | — | — |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 37% | 🟢 1% | 🟢 32% | 🟢 76% | 🔴 -15% | 🟢 107% | 🟢 51% | 🟢 65% | 🔴 -47% | 🟢 127% | 🟢 16% | 🟢 26% |

> [!code]- Click to view: cc_022.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_022.py"
> ```


---

## Strategy-23
### TQQQ trend SMA200 (algo_003.py)

**Description:** The canonical 'price above 200-day SMA' trend filter, applied to QQQ as a signal and TQQQ as the execution vehicle. When QQQ is above its 200-day SMA, holds 100% TQQQ for leveraged Nasdaq exposure; when it drops below, moves entirely to cash. The 200-day SMA is the most-followed long-term technical indicator in institutional markets, which gives the signal real behavioral anchoring — but the lagging nature means the leveraged vehicle takes severe damage before the exit triggers.

*Overfit 1/10 — The simplest possible trend filter — one canonical indicator (SMA200) on one canonical signal asset (QQQ). Zero tuned parameters; this is the textbook implementation of the Davey 'Cheat Code Chapter 5' regime filter. As close to a no-overfit baseline as exists in the set.*

- **Trend gate:** QQQ > SMA(200) → 100% TQQQ; else → cash
- **Entry:** Trend gate becomes true and not currently holding → buy TQQQ
- **Exit:** Trend gate becomes false → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -56% | 0.753 | 10 | 47 | 0.21 | 28.85 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 2% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 105% | 🟢 88% | 🔴 -44% | 🟢 112% | 🟢 62% | 🟢 23% |

> [!code]- Click to view: cc_023.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_023.py"
> ```


---

## Strategy-24
### TQQQ trend SMA150 (algo_006.py)

**Description:** Same structure as Strategy 23 (QQQ trend filter → TQQQ vehicle, all-or-nothing) but uses a 150-day SMA instead of 200-day. The shorter lookback catches trend entries a few weeks earlier and exits drawdowns sooner — which historically traded a small CAGR boost for slightly worse whipsaw risk in range-bound regimes.

*Overfit 2/10 — Shortens the canonical SMA(200) to SMA(150) — alternate but still widely-used value (50/100/150/200 are the standard variants). One parameter, no tuning. The choice between 150 and 200 is reasonable on either side; mild concern that this is part of a parameter sweep across SMA lengths.*

- **Trend gate:** QQQ > SMA(150) → 100% TQQQ; else → cash
- **Entry:** Trend gate flips true and not currently holding → buy TQQQ
- **Exit:** Trend gate flips false → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -55% | 0.871 | 21 | 36 | 0.58 | 14.75 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 18% | 🔴 -5% | 🟢 118% | 🟢 1% | 🟢 53% | 🟢 97% | 🟢 88% | 🔴 -34% | 🟢 125% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: cc_024.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_024.py"
> ```


---

## Strategy-25
### TQQQ self-SMA200 (algo_008.py)

**Description:** Identical to Strategy 23 (200-day SMA trend filter) except the signal asset is TQQQ itself rather than QQQ. Reads TQQQ's price against its own 200-day moving average, so the signal is driven by the leveraged ETF's path rather than the underlying index. Self-referential SMAs on leveraged ETFs tend to be noisier because the ETF's path is path-dependent (3x leverage compounds asymmetrically vs the underlying).

*Overfit 3/10 — Replaces QQQ as the signal asset with TQQQ itself. The leveraged ETF's path is path-dependent, so the self-SMA tends to be noisier than the underlying's SMA and harder to defend out-of-sample — TQQQ's day-to-day moves are amplified, making the 200-day SMA more volatile around the trend line. Adds reflexive risk vs the canonical Strategy 23.*

- **Trend gate:** TQQQ > SMA(200) of TQQQ → 100% TQQQ; else → cash
- **Entry:** Trend gate flips true and not currently holding → buy TQQQ
- **Exit:** Trend gate flips false → liquidate
- **Symbols:** TQQQ (signal and execution)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -50% | 0.76 | 18 | 41 | 0.44 | 16.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 11% | 🔴 -20% | 🟢 118% | 🟢 8% | 🟢 40% | 🟢 69% | 🟢 88% | 🔴 -21% | 🟢 68% | 🟢 41% | 🟢 16% |

> [!code]- Click to view: cc_025.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_025.py"
> ```


---

## Strategy-26
### TQQQ self-SMA150 (algo_009.py)

**Description:** TQQQ self-SMA combined with the 150-day lookback — same idea as Strategy 25 (read TQQQ's own SMA) but shorter window. Combines the two parameter shifts from Strategies 23/24/25: self-referential signal + 150d instead of 200d. The shorter window adds whipsaw risk; the self-reference adds reflexivity.

*Overfit 3/10 — Self-SMA + shorter lookback — same caveat as Strategy 25 (leveraged-ETF path-dependence makes the signal noisier) plus the parameter sweep concern from Strategy 24. The combination compounds both minor risks but each in isolation is defensible.*

- **Trend gate:** TQQQ > SMA(150) of TQQQ → 100% TQQQ; else → cash
- **Entry:** Trend gate flips true and not currently holding → buy TQQQ
- **Exit:** Trend gate flips false → liquidate
- **Symbols:** TQQQ (signal and execution)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -53% | 0.692 | 24 | 59 | 0.41 | 10.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 42% | 🟢 1% | 🔴 -5% | 🟢 118% | 🔴 -23% | 🟢 16% | 🟢 93% | 🟢 64% | 🔴 -22% | 🟢 76% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: cc_026.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_026.py"
> ```


---

## Strategy-27
### SMA200 75% cap (algo_011.py)

**Description:** Same as Strategy 23 (QQQ 200-day SMA trend filter → TQQQ vehicle) but caps the TQQQ allocation at 75% instead of 100%. The cash buffer dampens drawdowns at the cost of giving up some upside — a simple risk-budget knob applied to an otherwise textbook trend strategy.

*Overfit 2/10 — Adds one tuned magnitude parameter (75% cap) to the otherwise canonical SMA(200) trend filter. The cap value isn't a standard convention but is on the conservative side; main concern is parameter sweep (similar to 24's SMA-length tweak).*

- **Trend gate:** QQQ > SMA(200) → 75% TQQQ + 25% cash; else → cash
- **Entry:** Trend gate flips true and not currently holding → buy 75% TQQQ
- **Exit:** Trend gate flips false → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -49% | 0.703 | 10 | 47 | 0.21 | 28.86 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 42% | 🟢 1% | 🔴 -9% | 🟢 94% | 🔴 -16% | 🟢 39% | 🟢 87% | 🟢 80% | 🔴 -39% | 🟢 87% | 🟢 55% | 🟢 15% |

> [!code]- Click to view: cc_027.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_027.py"
> ```


---

## Strategy-28
### IBS MR pure (algo_016.py)

**Description:** A pure mean-reversion strategy using Internal Bar Strength (IBS), a measure of where the day's close lands within the daily range. Buys TQQQ when IBS is low (close near the day's low, suggesting a selloff close) and exits when IBS is high (close near the day's high, suggesting a strong close).

*Overfit 2/10 — Single indicator with the canonical IBS bands (0.2/0.7). Zero trend filter, zero stop. Pure MR design — the most overfit-resistant flavor of IBS strategy because there are essentially no tuned parameters beyond the well-known thresholds.*

- **Entry:** IBS = (close - low) / (high - low) < 0.2 → 100% TQQQ
- **Exit:** IBS > 0.7 → liquidate
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open (signals computed on previous bar's H/L/C)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -50% | 0.817 | 498 | 245 | 2.03 | 0.85 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -11% | 🔴 -18% | 🟢 18% | 🟢 41% | 🔴 -12% | 🟢 18% | 🟢 384% | 🟢 51% | 🟢 24% | 🟢 125% | ⚪ 0% | 🟢 43% |

> [!code]- Click to view: cc_028.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_028.py"
> ```


---

## Strategy-29
### 5 most mkt cap @ 1.5x (algo_018.py)

**Description:** Holds the five largest US stocks by market cap (rebuilt monthly), each at 30% weight — totaling 150% notional via margin. No timing signals, no trend filter, just leveraged exposure to mega-caps. Uses Interactive Brokers margin model for the 1.5× leverage.

*Overfit 5/10 — Dynamic top-5 universe removes name-selection bias, but 1.5x is a tuned leverage level (not a standard fraction like 1.0 or 2.0). No trend filter means full exposure during all drawdowns, amplified by margin — a backtest-friendly design that suppresses MaxDD only because the 2014-2025 mega-cap drawdowns were shallow.*

- **Universe:** Top 5 US stocks by market cap (all sectors, dynamic, monthly selection)
- **Allocation:** Equal weight × 1.5x = 30% per name, 150% total notional
- **Entry:** None (permanent hold)
- **Exit:** On universe change — names dropped from top 5 get liquidated
- **Rebalance:** Monthly (first trading day at 10:00 ET)
- **Symbols:** Dynamic — typically AAPL/MSFT/NVDA/GOOG/AMZN etc.
- **Brokerage:** Interactive Brokers margin account (required for 1.5x)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -55% | 0.829 | 569 | 49 | 11.61 | 1.89 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 19% | 🟢 14% | 🟢 10% | 🟢 53% | 🟢 12% | 🟢 70% | 🟢 84% | 🟢 71% | 🔴 -51% | 🟢 102% | 🟢 50% | 🟢 50% |

> [!code]- Click to view: cc_029.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_029.py"
> ```


---

## Strategy-30
### TQQQ IBS extreme (algo_028.py)

**Description:** More restrictive cousin of Strategy 28 — same IBS mean-reversion mechanic on TQQQ but with much tighter thresholds. Only enters when IBS is in extreme oversold territory (< 0.1, meaning the close was very near the day's low) and only exits at extreme overbought (> 0.9). Trades less often than Strategy 28 but each trade is meant to be higher quality.

*Overfit 3/10 — Tightens Strategy 28's IBS bands from 0.2/0.7 to 0.1/0.9. Both bands are standard 'tail' values widely used in IBS literature; the tightening reduces trade frequency but introduces no novel parameters. Slightly higher overfit floor than #28 only because the choice between 0.1/0.9 and 0.2/0.7 is itself a parameter sweep.*

- **Entry:** IBS < 0.1 → 100% TQQQ
- **Exit:** IBS > 0.9 → liquidate
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 47% | -47% | 1.05 | 269 | 100 | 2.69 | 1.00 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 12% | 🟢 5% | 🟢 39% | 🟢 71% | 🔴 -18% | 🟢 35% | 🟢 344% | 🟢 75% | 🔴 -1% | 🟢 101% | 🟢 17% | 🟢 82% |

> [!code]- Click to view: cc_030.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_030.py"
> ```


---

## Strategy-31
### TQQQ IBS 0.15/0.85 (algo_029.py)

**Description:** Splits the difference between Strategies 28 and 30 — IBS thresholds at 0.15/0.85. Trades more than #30 but less than #28; the cutoffs sit halfway between the canonical 0.1/0.9 and 0.2/0.7 pairs.

*Overfit 4/10 — IBS thresholds 0.15 / 0.85 are explicitly between the textbook 0.1/0.9 and 0.2/0.7 — exactly the kind of non-standard splitting that signals threshold-sweeping rather than principled selection. Lower overfit floor than Strategy 14's RSI windows but higher than the canonical-cutoff variants (28, 30).*

- **Entry:** IBS < 0.15 → 100% TQQQ
- **Exit:** IBS > 0.85 → liquidate
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -42% | 0.843 | 361 | 162 | 2.23 | 0.88 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -3% | ⚪ 0% | 🟢 5% | 🟢 50% | 🔴 -22% | 🟢 63% | 🟢 361% | 🟢 74% | 🟢 9% | 🟢 74% | 🟢 1% | 🟢 42% |

> [!code]- Click to view: cc_031.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_031.py"
> ```


---

## Strategy-32
### IBS extreme + SMA200 (algo_030.py)

**Description:** Combines Strategy 30's IBS extreme mean-reversion (entry IBS < 0.1, exit IBS > 0.9) with a 200-day SMA trend filter — only enters new positions when QQQ is above its 200-day SMA. Exits still trigger on IBS > 0.9 regardless of trend state. The trend filter prevents catching falling knives in confirmed bear markets.

*Overfit 3/10 — Two canonical indicators (SMA200 and IBS at standard 0.1/0.9 bands), combined in the most natural way (trend filter gates entry, mean-reversion signal exits). The asymmetric filter (trend on entry only) is a sensible design choice that doesn't add tuning.*

- **Trend gate:** QQQ > SMA(200) — required for entry only, not for hold
- **Entry:** Trend gate true AND IBS < 0.1 → 100% TQQQ
- **Exit:** IBS > 0.9 → liquidate (regardless of trend)
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -40% | 0.903 | 214 | 79 | 2.71 | 0.97 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 12% | 🟢 1% | 🟢 8% | 🟢 71% | 🔴 -10% | 🟢 34% | 🟢 136% | 🟢 75% | 🔴 -14% | 🟢 84% | 🟢 17% | 🟢 50% |

> [!code]- Click to view: cc_032.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_032.py"
> ```


---

## Strategy-33
### IBS extreme + ATR stop (algo_031.py)

**Description:** Strategy 30's IBS extreme mean-reversion (IBS < 0.1 buy, IBS > 0.9 exit) with a 3× ATR stop-loss added to limit catastrophic single-trade losses. Stop is measured from the entry close — no trailing, no recalculation. This is the strategy that matches Strategies.md Strategy-8 (the active production version).

*Overfit 3/10 — Adds a single risk-management parameter (3× ATR fixed stop) to Strategy 30's IBS extremes. The 3× multiplier matches the conventional Bollinger 3-sigma intuition and ATR(14) is the canonical window. Mirrors the active Strategies.md Strategy-8 rating.*

- **Entry:** IBS < 0.1 → 100% TQQQ; entry price recorded
- **Exit (MR):** IBS > 0.9 → liquidate
- **Stop-loss:** Close < entry_price - 3.0 × ATR(14) → liquidate (fixed from entry, not trailing)
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 46% | -43% | 1.049 | 271 | 106 | 2.56 | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 7% | 🟢 6% | 🟢 39% | 🟢 71% | 🔴 -29% | 🟢 33% | 🟢 344% | 🟢 75% | 🔴 -1% | 🟢 101% | 🟢 29% | 🟢 82% |

> [!code]- Click to view: cc_033.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_033.py"
> ```


---

## Strategy-34
### IBS 0.05 (rare) (algo_032.py)

**Description:** Even more restrictive than Strategy 30 — IBS entry threshold dropped from 0.1 to 0.05. Only fires on truly extreme close-near-the-low days (rare events, often during market panics). Exits unchanged at IBS > 0.9.

*Overfit 4/10 — IBS < 0.05 is meaningfully tighter than canonical 0.1 — these triggers are very rare events. Rarity reduces statistical confidence: a strategy with only ~30 entries over 11 years can be parameter-fit to coincide with specific panic days that happened in the backtest. Higher overfit floor than #30.*

- **Entry:** IBS < 0.05 → 100% TQQQ
- **Exit:** IBS > 0.9 → liquidate
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -47% | 0.791 | 170 | 60 | 2.83 | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 9% | 🟢 8% | 🟢 43% | 🟢 37% | 🔴 -12% | 🟢 24% | 🟢 216% | 🟢 28% | 🟢 6% | 🟢 45% | 🔴 -6% | 🟢 77% |

> [!code]- Click to view: cc_034.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_034.py"
> ```


---

## Strategy-35
### IBS 0.1/0.7 fast (algo_033.py)

**Description:** Faster-exit variant of Strategy 30 — same IBS < 0.1 entry but exits at IBS > 0.7 instead of > 0.9. Captures the early part of the mean-reversion bounce and gives up the final leg.

*Overfit 3/10 — Mixes Strategy 28's exit threshold (0.7) with Strategy 30's entry threshold (0.1). Both values are canonical individually, but the asymmetric pairing — extreme entry + moderate exit — is a parameter combination that needs out-of-sample validation.*

- **Entry:** IBS < 0.1 → 100% TQQQ
- **Exit:** IBS > 0.7 → liquidate
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -35% | 0.915 | 328 | 141 | 2.33 | 0.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -7% | 🔴 -4% | 🟢 23% | 🟢 34% | 🔴 -1% | 🟢 18% | 🟢 273% | 🟢 20% | 🟢 26% | 🟢 89% | 🟢 75% | 🟢 22% |

> [!code]- Click to view: cc_035.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_035.py"
> ```


---

## Strategy-36
### IBS regime-adaptive (algo_035.py)

**Description:** Regime-adaptive IBS strategy. Standard IBS < 0.1 entry in uptrends (QQQ > 200d SMA), but tightens to IBS < 0.03 in downtrends — only buying extreme panic closes when the broader market is bearish. Exit is unchanged at IBS > 0.9 regardless of regime.

*Overfit 4/10 — Regime-adaptive design is conceptually sound, but the 0.03 downtrend threshold is extreme — implies essentially never entering in bear markets except on capitulation days. Such a rare threshold can only be back-fit to specific days that existed in the backtest decade.*

- **Trend gate:** QQQ > SMA(200) → 'uptrend' regime; else → 'downtrend' regime
- **Entry (uptrend):** IBS < 0.1 → 100% TQQQ
- **Entry (downtrend):** IBS < 0.03 → 100% TQQQ (very rare)
- **Exit:** IBS > 0.9 → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -55% | 0.917 | 237 | 92 | 2.58 | 0.98 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 12% | 🟢 1% | 🟢 26% | 🟢 71% | 🔴 -31% | 🟢 35% | 🟢 303% | 🟢 75% | 🔴 -23% | 🟢 84% | 🟢 17% | 🟢 92% |

> [!code]- Click to view: cc_036.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_036.py"
> ```


---

## Strategy-37
### IBS + 3d max hold (algo_039.py)

**Description:** Strategy 30 with a hard time-based exit added: if you're still holding after 3 trading days, liquidate regardless of IBS reading. Prevents the strategy from bag-holding through a longer reversal when the IBS exit signal stalls.

*Overfit 5/10 — Adds a 3-day max-hold time stop to canonical IBS extremes. The 3-day window is hand-tuned and doesn't generalize across volatility regimes — in calm markets the bounce may take longer than 3 days, in panic markets shorter. The time stop is the kind of patch that fixes the backtest curve specifically.*

- **Entry:** IBS < 0.1 → 100% TQQQ; entry bar recorded
- **Exit (IBS):** IBS > 0.9 → liquidate
- **Exit (time):** Holding for ≥ 3 trading days → liquidate
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -52% | 0.799 | 295 | 166 | 1.78 | 1.04 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -4% | 🔴 -18% | 🟢 15% | 🟢 47% | 🟢 46% | 🟢 9% | 🟢 205% | 🟢 58% | 🔴 -34% | 🟢 90% | 🟢 61% | 🟢 8% |

> [!code]- Click to view: cc_037.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_037.py"
> ```


---

## Strategy-38
### SMA150 trend + IBS<0.05 (algo_040.py)

**Description:** Two-mode hybrid strategy on TQQQ. In an uptrend (QQQ > 150d SMA), holds 100% TQQQ as a pure trend follower. When trend breaks, exits the trend position but stays alert for mean-reversion opportunities — entering on extreme oversold IBS < 0.05 readings and exiting those MR positions on IBS > 0.9. Internal state tracks whether the current position is a 'trend' hold or 'MR' hold so the exits are properly attributed.

*Overfit 5/10 — Hybrid trend-plus-MR designs introduce real complexity: two entry rules, two exit rules, and stateful tracking of which sleeve owns the current position. The downtrend MR entry at IBS<0.05 is rare-threshold tuning (same concern as #34) and the SMA(150) lookback adds the parameter-sweep concern from #24.*

- **Trend gate:** QQQ > SMA(150) → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ (trend position)
- **Entry (MR):** MR mode active AND not invested AND IBS < 0.05 → 100% TQQQ (MR position)
- **Exit (trend):** Trend flips off → liquidate the trend position
- **Exit (MR):** MR position held AND IBS > 0.9 → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 50% | -56% | 0.986 | 52 | 45 | 1.16 | 5.27 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 7% | 🟢 26% | 🟢 118% | 🔴 -22% | 🟢 55% | 🟢 222% | 🟢 88% | 🔴 -31% | 🟢 135% | 🟢 64% | 🟢 57% |

> [!code]- Click to view: cc_038.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_038.py"
> ```


---

## Strategy-39
### SMA150 + IBS + 3xATR (algo_042.py)

**Description:** Strategy 38 (SMA150 trend + IBS MR hybrid) with a 3× ATR stop-loss added only on the MR-position side. Trend positions exit on the SMA flip; MR positions exit on either IBS > 0.9, the stop, or the SMA flip. Adds a fourth parameter to an already-layered design.

*Overfit 5/10 — Inherits Strategy 38's hybrid complexity plus a 3× ATR stop on the MR sleeve. Four tuned parameters total (SMA150, IBS 0.05/0.9, ATR 3×). The ATR multiplier matches Strategy 33's choice; the rest is the #38 stack. Defensible piece-by-piece but the combination is dense.*

- **Trend gate:** QQQ > SMA(150) → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ
- **Entry (MR):** MR mode active AND IBS < 0.05 → 100% TQQQ; entry price recorded
- **Exit (trend):** Trend flips off → liquidate
- **Exit (MR signal):** MR position held AND IBS > 0.9 → liquidate
- **Stop-loss (MR only):** MR position close < entry - 3.0 × ATR(14) → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 51% | -55% | 1.002 | 57 | 44 | 1.30 | 4.54 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 8% | 🟢 26% | 🟢 118% | 🔴 -16% | 🟢 55% | 🟢 222% | 🟢 88% | 🔴 -31% | 🟢 135% | 🟢 64% | 🟢 57% |

> [!code]- Click to view: cc_039.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_039.py"
> ```


---

## Strategy-40
### SMA150 + IBS + 2xATR (algo_043.py)

**Description:** Strategy 39 with a tighter stop on the MR sleeve — 2× ATR instead of 3×. Otherwise identical: SMA(150) trend hold + IBS<0.05 dip entry on the down-trend side, IBS>0.9 exit. The tighter stop reduces per-trade drawdown at the cost of more frequent stop-outs.

*Overfit 5/10 — Identical structure to Strategy 39 with a single parameter change — ATR multiplier 2× vs 3×. The fact that this exists alongside Strategy 39 confirms the multiplier was being swept; 2× and 3× are both within conventional range but the existence of paired variants raises the overfit floor.*

- **Trend gate:** QQQ > SMA(150) → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ
- **Entry (MR):** MR mode active AND IBS < 0.05 → 100% TQQQ; entry price recorded
- **Exit (trend):** Trend flips off → liquidate
- **Exit (MR signal):** MR position held AND IBS > 0.9 → liquidate
- **Stop-loss (MR only):** MR position close < entry - 2.0 × ATR(14) → liquidate (tighter than #39's 3×)
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 51% | -58% | 1.01 | 57 | 44 | 1.30 | 4.53 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 23% | 🟢 19% | 🟢 118% | 🔴 -3% | 🟢 55% | 🟢 222% | 🟢 88% | 🔴 -43% | 🟢 135% | 🟢 64% | 🟢 57% |

> [!code]- Click to view: cc_040.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_040.py"
> ```


---

## Strategy-41
### SMA150+IBS fast exit (algo_046.py)

**Description:** Faster-exit variant of Strategy 38 — same SMA(150) trend + IBS<0.05 hybrid structure, but the MR sleeve exits on IBS > 0.7 instead of > 0.9. Captures less of the bounce per trade but releases capital sooner for the next setup.

*Overfit 5/10 — Strategy 38 with the MR exit threshold dropped from 0.9 to 0.7. Same concerns: hybrid complexity + rare IBS<0.05 entry + parameter swap. The 0.7 exit is canonical but the explicit pairing with 0.05 entry (asymmetric tails) is non-standard.*

- **Trend gate:** QQQ > SMA(150) → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ
- **Entry (MR):** MR mode active AND IBS < 0.05 → 100% TQQQ
- **Exit (trend):** Trend flips off → liquidate
- **Exit (MR):** MR position held AND IBS > 0.7 → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 55% | -55% | 1.068 | 62 | 49 | 1.27 | 4.76 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 7% | 🟢 17% | 🟢 118% | 🔴 -14% | 🟢 57% | 🟢 276% | 🟢 88% | 🔴 -26% | 🟢 135% | 🟢 64% | 🟢 70% |

> [!code]- Click to view: cc_041.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_041.py"
> ```


---

## Strategy-42
### #46 + chandelier (algo_047.py)

**Description:** Strategy 41 (SMA150 + IBS<0.05 + IBS>0.7 fast exit) with a 5× ATR chandelier trailing stop added to the trend sleeve and a 3× ATR fixed stop on the MR sleeve. The trend stop tracks the peak price reached during the trade and exits when the price falls 5× ATR below that peak — much more permissive than the MR stop, which is fixed from entry.

*Overfit 6/10 — Five tuned parameters (SMA150, IBS 0.05/0.7, ATR 5× chandelier, ATR 3× MR). The 5× chandelier is unusually wide — most chandelier stops use 2-3× ATR — suggesting it was tuned to avoid stopping out the long trend rides that drive CAGR in the backtest. Highest parameter density in the hybrid family.*

- **Trend gate:** QQQ > SMA(150) → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ; peak price tracked
- **Entry (MR):** MR mode active AND IBS < 0.05 → 100% TQQQ; entry price recorded
- **Trend stop (chandelier):** Close < peak_price - 5.0 × ATR(14) → liquidate
- **MR stop:** Close < entry_price - 3.0 × ATR(14) → liquidate
- **Exit (trend signal):** Trend flips off → liquidate
- **Exit (MR signal):** MR position held AND IBS > 0.7 → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 52% | -56% | 1.027 | 77 | 60 | 1.28 | 2.77 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 46% | 🟢 8% | 🟢 9% | 🟢 118% | 🔴 -23% | 🟢 60% | 🟢 266% | 🟢 81% | 🔴 -26% | 🟢 136% | 🟢 64% | 🟢 70% |

> [!code]- Click to view: cc_042.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_042.py"
> ```


---

## Strategy-43
### #46 on QLD (algo_048.py)

**Description:** Strategy 41 (SMA150 + IBS<0.05 + IBS>0.7 hybrid) ported from TQQQ to QLD (2× Nasdaq) for lower leverage exposure. Same trend + MR mechanics, just half the daily-leverage of the TQQQ original. Trades less violently both up and down.

*Overfit 4/10 — Same structure as Strategy 41 but lower-leverage vehicle (QLD vs TQQQ). The 'swap one ETF for another to reduce DD' pattern is itself a form of post-hoc selection — picking QLD specifically (over UPRO, SSO, etc.) is a hindsight choice.*

- **Trend gate:** QQQ > SMA(150) → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% QLD
- **Entry (MR):** MR mode active AND QLD IBS < 0.05 → 100% QLD
- **Exit (trend):** Trend flips off → liquidate
- **Exit (MR):** MR position held AND QLD IBS > 0.7 → liquidate
- **Symbols:** QLD (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -40% | 1.018 | 69 | 46 | 1.50 | 3.88 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🟢 11% | 🟢 3% | 🟢 70% | 🔴 -4% | 🟢 36% | 🟢 158% | 🟢 57% | 🟢 2% | 🟢 93% | 🟢 46% | 🟢 49% |

> [!code]- Click to view: cc_043.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_043.py"
> ```


---

## Strategy-44
### %R(2) MR pure (algo_053.py)

**Description:** Pure mean-reversion strategy using Williams %R(2), an oscillator that measures where the close sits within the recent high-low range. Buys TQQQ when %R drops below -90 (deeply oversold, close near recent 2-day low) and exits when %R rises above -10 (overbought, close near recent high). Conceptually similar to IBS strategies but uses a 2-day lookback range instead of the single-day range.

*Overfit 2/10 — Williams %R with canonical -90/-10 bands and a 2-day lookback (matches the RSI(2) family in spirit — very short-term oscillators). Single indicator, single rule, no trend filter or stop. The most overfit-resistant flavor of %R-based MR.*

- **Entry:** Williams %R(2) < -90 → 100% TQQQ
- **Exit:** Williams %R(2) > -10 → liquidate
- **Symbols:** TQQQ
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -42% | 0.912 | 242 | 90 | 2.69 | 0.95 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 9% | 🟢 18% | 🟢 41% | 🟢 49% | 🔴 -19% | 🟢 64% | 🟢 347% | 🟢 17% | 🔴 -3% | 🟢 110% | 🟢 37% | 🟢 10% |

> [!code]- Click to view: cc_044.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_044.py"
> ```


---

## Strategy-45
### TQQQ + SMA200 (algo_055.py)

**Description:** TQQQ-vs-TQQQ-own-SMA(200) trend filter — identical mechanic to Strategy 25 but listed separately. Reads TQQQ's price against its own 200-day SMA, enters 100% on cross-above, exits on cross-below. The self-referential signal makes this noisier than QQQ-driven Strategy 23.

*Overfit 3/10 — Functionally identical to Strategy 25 (TQQQ self-SMA200 trend) — same code shape, same parameters. The self-SMA on leveraged ETF is the only minor concern (path-dependence makes signal noisier than QQQ-anchored Strategy 23).*

- **Trend gate:** TQQQ > SMA(200) of TQQQ → 100% TQQQ; else → cash
- **Entry:** Trend gate flips true and not currently holding → buy TQQQ
- **Exit:** Trend gate flips false → liquidate
- **Symbols:** TQQQ (signal and execution)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -50% | 0.76 | 18 | 41 | 0.44 | 16.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 11% | 🔴 -20% | 🟢 118% | 🟢 8% | 🟢 40% | 🟢 69% | 🟢 88% | 🔴 -21% | 🟢 68% | 🟢 41% | 🟢 16% |

> [!code]- Click to view: cc_045.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_045.py"
> ```


---

## Strategy-46
### %R(2) hybrid (algo_056.py)

**Description:** Trend + Williams %R hybrid: in an uptrend (QQQ > SMA(150)), holds 100% TQQQ as trend follower. When trend breaks, exits the trend position and enters MR mode — buying TQQQ on extreme %R<-95 readings and exiting on %R>-10. Combines the trend-following uptime of Strategy 24 with the bear-market dip-buys of Strategy 44.

*Overfit 5/10 — %R<-95 is tighter than the canonical -90 — the kind of parameter shift that signals back-fitting to specific 2014-2025 panic days. Hybrid complexity (two entry rules, two exit rules) plus a tuned non-standard threshold puts this near the top of the bear-market dip-buyer family.*

- **Trend gate:** QQQ > SMA(150) → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ
- **Entry (MR):** MR mode active AND Williams %R(2) < -95 → 100% TQQQ
- **Exit (trend):** Trend flips off → liquidate
- **Exit (MR):** MR position held AND Williams %R(2) > -10 → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 51% | -56% | 0.996 | 55 | 50 | 1.10 | 5.92 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 17% | 🟢 9% | 🟢 118% | 🔴 -21% | 🟢 53% | 🟢 191% | 🟢 88% | 🔴 -4% | 🟢 164% | 🟢 64% | 🟢 28% |

> [!code]- Click to view: cc_046.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_046.py"
> ```


---

## Strategy-47
### TQQQ hybrid (SMA+IBS) (algo_060.py)

**Description:** TQQQ self-SMA(200) trend filter + IBS<0.05 extreme dip-buy overlay. In an uptrend, holds 100% TQQQ. When TQQQ closes below its own 200d SMA, exits the trend position but stays alert for IBS<0.05 panic-close re-entries. Exit on MR positions at IBS>0.7.

*Overfit 5/10 — Similar to Strategy 38 (SMA150 hybrid) but uses TQQQ self-SMA200 — inherits the same noisier self-SMA concern from Strategy 25/45. The IBS<0.05 extreme threshold is the rare-trigger flag. Hybrid stack with three tuned components.*

- **Trend gate:** TQQQ > SMA(200) of TQQQ → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ
- **Entry (MR):** MR mode active AND IBS < 0.05 → 100% TQQQ
- **Exit (trend):** Trend flips off → liquidate
- **Exit (MR):** MR position held AND IBS > 0.7 → liquidate
- **Symbols:** TQQQ (signal and execution)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 49% | -50% | 0.988 | 69 | 58 | 1.19 | 4.69 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 9% | 🟢 4% | 🟢 118% | 🔴 -8% | 🟢 36% | 🟢 259% | 🟢 88% | 🔴 -11% | 🟢 75% | 🟢 59% | 🟢 48% |

> [!code]- Click to view: cc_047.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_047.py"
> ```


---

## Strategy-48
### TQQQ + SMA150 (algo_061.py)

**Description:** TQQQ-vs-TQQQ-own-SMA(150) trend filter — identical mechanic to Strategy 26. Reads TQQQ's price against its own 150-day SMA, enters 100% on cross-above, exits on cross-below. The shorter self-SMA combines the shorter-lookback concern of Strategy 24 with the self-reference concern of Strategy 25.

*Overfit 3/10 — Functionally identical to Strategy 26 (TQQQ self-SMA150 trend). The shorter window adds whipsaw risk; the self-reference adds reflexivity. Same rating.*

- **Trend gate:** TQQQ > SMA(150) of TQQQ → 100% TQQQ; else → cash
- **Entry:** Trend gate flips true and not currently holding → buy TQQQ
- **Exit:** Trend gate flips false → liquidate
- **Symbols:** TQQQ (signal and execution)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -53% | 0.692 | 24 | 59 | 0.41 | 10.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 42% | 🟢 1% | 🔴 -5% | 🟢 118% | 🔴 -23% | 🟢 16% | 🟢 93% | 🟢 64% | 🔴 -22% | 🟢 76% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: cc_048.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_048.py"
> ```


---

## Strategy-49
### 5 most mkt cap + IBS regime mix (algo_064.py)

**Description:** Two-regime rotation on the top 5 US stocks by market cap. **Uptrend** (QQQ > 200d SMA): hold all 5 mega-caps equal-weight (20% each). **Downtrend** (QQQ ≤ 200d SMA): rotate into only those names whose IBS < 0.2 (close near day's low — buying weakness in mega-caps only when the broader market is bearish). Position weights adjust daily based on how many names meet the bear-mode filter.

*Overfit 3/10 — Dynamic universe removes name-selection bias. SMA(200) and IBS<0.2 are both canonical thresholds. The 5% rebalance drift tolerance is a minor magic number but isn't outcome-shaping. One of the cleanest hybrid designs — mirrors Strategies.md Strategy-9 (active production version) at the same rating.*

- **Universe:** Top 5 US stocks by market cap (all sectors, dynamic)
- **Trend gate:** QQQ > SMA(200) → 'trend' mode; else → 'MR' mode
- **Allocation (trend):** Equal weight all 5 names (20% each); rebalance only when drift > 5%
- **Allocation (MR):** Equal weight names with IBS < 0.2 (variable subset, 0-5 names)
- **Exit:** Per-name: liquidated when no longer in target set (universe change or filter exit)
- **Symbols:** Dynamic — typically AAPL/MSFT/NVDA/GOOG/AMZN etc.; QQQ for signal
- **Rebalance:** Daily at 10:30 ET

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -23% | 1.073 | 828 | 650 | 1.27 | 2.07 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 11% | 🟢 5% | 🟢 4% | 🟢 38% | 🟢 15% | 🟢 47% | 🟢 95% | 🟢 46% | 🔴 -11% | 🟢 51% | 🟢 38% | 🟢 50% |

> [!code]- Click to view: cc_049.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_049.py"
> ```


---

## Strategy-50
### TQQQ hybrid + ATR (algo_066.py)

**Description:** TQQQ self-SMA(200) trend + IBS<0.05 dip-buy hybrid with an added 3× ATR stop-loss on the MR sleeve. Same shape as Strategy 47 but with risk management on the bear-market dips — if the dip extends another 3× ATR below the entry, the trade is cut.

*Overfit 5/10 — Strategy 47 + an ATR stop on MR positions. Four tuned parameters total (SMA200, IBS 0.05/0.7, ATR 3×). The TQQQ self-SMA introduces noise (Strategy 25 concern); the IBS<0.05 is rare-trigger fitting (Strategy 34 concern); the ATR stop is canonical (Strategy 33 concern). Inherits every concern from its parents.*

- **Trend gate:** TQQQ > SMA(200) of TQQQ → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ
- **Entry (MR):** MR mode active AND IBS < 0.05 → 100% TQQQ; entry price recorded
- **Exit (trend):** Trend flips off → liquidate
- **Exit (MR signal):** MR position held AND IBS > 0.7 → liquidate
- **Stop-loss (MR only):** MR position close < entry - 3.0 × ATR(14) → liquidate
- **Symbols:** TQQQ (signal and execution)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 49% | -48% | 0.991 | 71 | 58 | 1.22 | 4.32 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 9% | 🔴 -2% | 🟢 118% | 🔴 -1% | 🟢 36% | 🟢 259% | 🟢 88% | 🔴 -11% | 🟢 75% | 🟢 59% | 🟢 48% |

> [!code]- Click to view: cc_050.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_050.py"
> ```


---

## Strategy-51
### 8 Leveraged ETF EW Permanent + Monthly Rebalance (algo_039.py — algos3)

**Description:** Equal-weight permanent basket of 8 leveraged ETFs (TQQQ, UPRO, SOXL, TECL, QLD, SSO, DDM, FAS), rebalanced monthly back to 1/8 each. Pure cross-sectional rebalance harvesting — no timing signal, no trend gate. Captures the rebalancing premium from holding a basket of correlated but distinct leveraged exposures.

*Overfit 2/10 — Zero tuned parameters, fixed basket, fixed equal weights, fixed monthly cadence. The rebalancing premium is a well-documented effect; the basket choice (large-cap-tilt leveraged ETFs) is the only real degree of freedom and it's reasonable as a thematic group rather than an optimization.*

- **Universe:** Fixed 8-name basket: TQQQ, UPRO, SOXL, TECL, QLD, SSO, DDM, FAS
- **Allocation:** Equal weight (12.5% per name)
- **Entry:** None (permanent monthly rebalance back to EW)
- **Exit:** None — always invested
- **Rebalance:** Monthly, 30 min after market open on first trading day

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -70% | 0.707 | 842 | 44 | 19.14 | 3.66 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 45% | 🟢 4% | 🟢 33% | 🟢 87% | 🔴 -23% | 🟢 120% | 🟢 40% | 🟢 93% | 🔴 -61% | 🟢 107% | 🟢 45% | 🟢 34% |

> [!code]- Click to view: cc_051.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_051.py"
> ```


---

## Strategy-52
### 5x 3x-Leveraged ETF Basket + QQQ Vol Gate (algo_048.py — algos3)

**Description:** Equal-weight basket of 5 3x-leveraged ETFs (TQQQ, TECL, SOXL, UPRO, FAS), held only when QQQ's 20-day annualized log-return volatility is below 20%. Tight vol gate — flips entirely in or entirely out based on a single threshold check daily. Re-enters as soon as vol returns under threshold.

*Overfit 4/10 — Two tuned parameters — the 20-day vol lookback and the 20% threshold — applied to a fixed 5-name basket. The threshold is round-numbered but a tight binary gate on a single vol number is exactly the kind of cliff-edge rule that fits a specific regime; in the 2020 vol spike a 20% threshold would have caused multiple whipsaws.*

- **Universe:** Fixed 5-name 3x-leveraged basket: TQQQ, TECL, SOXL, UPRO, FAS
- **Vol gate:** QQQ 20d annualized log-return vol < 20% → in market; else → cash
- **Allocation:** Equal weight (20% per name) when in market
- **Entry:** Vol gate flips on → set all 5 names to 20%
- **Exit:** Vol gate flips off → liquidate entire portfolio
- **Rebalance:** Daily, 30 min after market open (checks gate only)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27% | -43% | 0.709 | 219 | 166 | 1.32 | 2.50 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 28% | 🔴 -1% | 🟢 21% | 🟢 106% | 🔴 -7% | 🟢 59% | 🟢 7% | 🟢 49% | 🟢 5% | 🟢 62% | 🟢 44% | ⚪ 0% |

> [!code]- Click to view: cc_052.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_052.py"
> ```


---

## Strategy-53
### Dynamic Top-5 EW + Adaptive Vol Gate (algo_057.py — algos3)

**Description:** Dynamic Top-5 by market cap, equal-weighted, held only when the basket's own short-term vol is below its long-term vol. Compares the basket's 20-day vs 252-day annualized vol of mean returns daily; in market on calm-relative-to-history, in cash when short-term vol exceeds long-term. The gate is self-adaptive — no fixed threshold — so it scales with the basket's own regime.

*Overfit 3/10 — Two lookback windows (20 and 252) — both conventional. The self-adaptive comparison (short vs long vol) removes the cliff-edge threshold concern that hurts Strategy 52. The dynamic universe (top-5 by mkt cap) avoids ticker cherry-picking. Main concern: the gate flips quickly and may whipsaw in transitional regimes.*

- **Universe:** Top 5 US stocks by market cap (HasFundamentalData, Price > 5)
- **Vol gate:** Basket 20d annualized vol of mean returns < basket 252d annualized vol → in market; else cash
- **Allocation:** Equal weight (20% per name) when gate is on
- **Entry:** Gate turns on AND not in market → set all top-5 to 20%
- **Exit:** Gate turns off → liquidate all top-5 positions
- **Rebalance:** Daily, 30 min after market open (checks gate only)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 25% | -17% | 1.08 | 297 | 160 | 1.86 | 2.58 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 6% | 🟢 10% | 🟢 13% | 🟢 25% | 🟢 15% | 🟢 30% | 🟢 54% | 🟢 45% | 🔴 -7% | 🟢 57% | 🟢 29% | 🟢 34% |

> [!code]- Click to view: cc_053.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_053.py"
> ```


---

## Strategy-54
### Dynamic Top-5 Momentum + TQQQ Sleeve + Vol Gate (algo_060.py — algos3)

**Description:** Two-sleeve strategy gated by TQQQ vol. When TQQQ's 20-day annualized vol < 60%: holds 80% in a momentum-weighted Top-5 basket (weights proportional to 63-day return, normalized) and 20% in TQQQ. When vol breaks above 60%: 100% cash. Monthly re-weight of the momentum sleeve, with a 3% drift band to avoid churn.

*Overfit 6/10 — Five tuned parameters: 63-day momo lookback, 20-day vol lookback, 60% vol threshold, 80/20 sleeve mix, 3% drift band. The 60% vol threshold is wide enough to be permissive but the combination of sleeve mix + drift band + momentum lookback is a lot of knobs for one strategy. The two-sleeve design (momentum basket + fixed TQQQ slug) is a real choice rather than a swept parameter, which keeps this from rating higher.*

- **Universe:** Top 5 US stocks by market cap (HasFundamentalData, Price > 5) + TQQQ
- **Vol gate:** TQQQ 20d annualized log-return vol < 60% → in market; else 100% cash
- **Top-5 sleeve (80%):** Weights ∝ 63-day return (negative clipped to 0); equal-weight fallback if all returns ≤ 0; re-weighted monthly
- **TQQQ sleeve (20%):** Fixed 20% allocation while gate is on
- **Drift band:** Skip rebalance for a name if |target − current| ≤ 3%
- **Exit:** Vol gate flips off → liquidate top-5 and TQQQ
- **Rebalance:** Daily gate check, monthly sleeve re-weight, both 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 24% | -27% | 0.827 | 455 | 256 | 1.78 | 2.15 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 7% | 🟢 18% | 🔴 -4% | 🟢 63% | 🟢 10% | 🟢 45% | 🟢 11% | 🟢 42% | 🔴 -12% | 🟢 47% | 🟢 64% | 🟢 22% |

> [!code]- Click to view: cc_054.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc_054.py"
> ```


---
