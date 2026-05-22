# ensemble

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [1](#strategy-1)     | ✅    | Buy & Hold      | 28%  | -51%  | 0.727  | 12    | 0     | —        | —            | 1/10   |
| [2](#strategy-2)     | ✅    | Mean Reversion  | 40%  | -32%  | 0.952  | 1276  | 687   | 1.86     | 1.08         | 2/10   |
| [3](#strategy-3)     | ✅    | Trend Following | 31%  | -49%  | 0.738  | 65    | 57    | 1.14     | 2.69         | 4/10   |
| [4](#strategy-4)     | ✅    | Breakout        | 38%  | -49%  | 0.886  | 94    | 76    | 1.24     | 2.19         | 4/10   |
| [5](#strategy-5)     | ✅    | Trend Following | 40%  | -55%  | 0.871  | 21    | 36    | 0.58     | 14.75        | 2/10   |
| [6](#strategy-6)     | ✅    | Mean Reversion  | 46%  | -43%  | 1.049  | 271   | 106   | 2.56     | 0.96         | 3/10   |
| [7](#strategy-7)     | ✅    | Ensemble        | 40%  | -35%  | 1.034  | 1580  | 677   | 2.33     | 1.20         | N/A    |


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
| 40% | -32% | 0.952 | 1276 | 687 | 1.86 | 1.08 |

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
| 40% | -55% | 0.871 | 21 | 36 | 0.58 | 14.75 |

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
### Mini Ensemble (cc000_003–008) (007.py)

**Description:** Equal-weight ensemble of the six core strategies: LeveragedRebalance, RSIDipChampion, TQQQDynamic, ExpandingBreakout, TQQQSMA150, and IBSATRStop. Sub-algo equities start equal and drift with performance; reset annually.

*Overfit N/A — Ensemble of independently-designed strategies. No combined parameter tuning.*

- **Components:** cc000_003 LeveragedRebalance, cc000_004 RSIDipChampion, cc000_005 TQQQDynamic, cc000_006 ExpandingBreakout, cc000_007 TQQQSMA150, cc000_008 IBSATRStop
- **Weighting:** Equal virtual equity split at start; aggregated proportionally each day
- **Rebalance:** Daily, 45 min after market open (SPY)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40% | -35% | 1.034 | 1580 | 677 | 2.33 | 1.20 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 46% | 🟢 9% | 🔴 -1% | 🟢 85% | 🟢 2% | 🟢 41% | 🟢 115% | 🟢 81% | 🔴 -18% | 🟢 94% | 🟢 45% | 🟢 45% |

> [!code]- Click to view: 007.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/ensemble/007.py"
> ```


---
