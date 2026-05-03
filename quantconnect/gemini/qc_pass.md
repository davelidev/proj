# QuantConnect Forum "Pass" Strategies Analysis

This document provides a deeper analysis of strategies discovered on the QuantConnect Community Forum that met the pass criteria: **CAGR >= 28% and MaxDD <= 58%**.

| # | Strategy Name | Category | CAGR | MaxDD | Sharpe | Win % | P/L Ratio | Overfit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ [3](#strategy-3) | TQQQ SMA Trend | Trend | 33.6% | -56.4% | 0.757 | 32% | 13.25 | 2/10 |
| ✅ [35](#strategy-35) | Vol Ratio Trend | Vol/Trend | 32.6% | -56.7% | 0.741 | 39% | 7.28 | 4/10 |
| ✅ [101](#strategy-101) | LETF Simple Rotation | Rotation | 124.5% | -46.8% | 1.869 | 54% | 2.55 | 7/10 |

| # | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [3](#strategy-3) | 🟢 56% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 105% | 🟢 88% | 🔴 -44% | 🟢 113% | 🟢 62% | 🟢 24% |
| [35](#strategy-35) | 🟢 53% | ⚪ 0% | 🔴 -22% | 🟢 118% | 🔴 -24% | 🟢 50% | 🟢 105% | 🟢 88% | 🔴 -44% | 🟢 118% | 🟢 55% | 🟢 34% |
| [101](#strategy-101) | 🟢 64% | 🔴 -11% | 🟢 64% | 🟢 139% | 🟢 20% | 🟢 136% | 🟢 1021% | 🟢 256% | 🟢 18% | 🟢 66% | 🟢 187% | 🟢 382% |

---

## Strategy-3
### TQQQ SMA Trend (it_3.py)

**Description:** A baseline trend-following strategy that applies a 200-day Simple Moving Average (SMA) filter to the underlying index (QQQ) to decide when to hold the 3x leveraged ETF (TQQQ). It seeks to capture long-term equity growth while avoiding major bear markets.

*Overfit 2/10 — Uses a single, industry-standard 200-day SMA parameter on the underlying index. Highly robust and simple.*

- **Entry:** QQQ Price > SMA(200)
- **Exit:** QQQ Price < SMA(200) (Switch to cash proxy BIL)
- **Symbols:** TQQQ, QQQ, BIL
- **Resolution:** Daily

| Pass? | CAGR | MaxDD | Sharpe | Win % | Loss % | P/L Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 33.594% | -56.400% | 0.757 | 32% | 68% | 13.25 |

> [!code]- Click to view: it_3.py
> ```embed-python
> PATH: "vault://QuantConnect/gemini/algos/it_3.py"
> ```

---

## Strategy-35
### Vol Ratio Trend (it_35.py)

**Description:** Enhances the standard SMA trend-following logic by adding a "volatility spike" filter. It only enters TQQQ if the trend is up AND the short-term volatility (10-day) relative to long-term volatility (60-day) is stable. This aims to avoid entering during high-volatility environments that lead to leverage decay.

*Overfit 4/10 — Adds two volatility lookbacks (10, 60) and a threshold (1.2). While logical, these extra parameters increase the risk of curve-fitting.*

- **Entry:** QQQ > SMA(200) AND VolRatio(10/60) < 1.2
- **Exit:** QQQ < SMA(200) OR VolRatio(10/60) >= 1.2
- **Symbols:** TQQQ, QQQ, BIL
- **Resolution:** Daily

| Pass? | CAGR | MaxDD | Sharpe | Win % | Loss % | P/L Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 32.556% | -56.700% | 0.741 | 39% | 61% | 7.28 |

> [!code]- Click to view: it_35.py
> ```embed-python
> PATH: "vault://QuantConnect/gemini/algos/it_35.py"
> ```

---

## Strategy-101
### LETF Simple Rotation (it_101.py)

**Description:** A sophisticated multi-state rotation model using leveraged ETFs (TQQQ, SOXL) and a volatility hedge (UVIX). It uses a 3-of-4 voting mechanism across SPY, QQQ, SMH, and SOXL moving averages to determine the market regime. Includes specific rules for overbought conditions (hedging) and bear market oversold bounces.

*Overfit 7/10 — High complexity with 4 regime tickers, multiple RSI lookbacks and thresholds, and a custom IPO proxy for UVIX. Exceptional performance, but requires careful monitoring for regime changes.*

- **Entry:** BULL Regime (3/4 SMA votes) -> 50/50 TQQQ+SOXL; BULL + Overbought -> 100% UVIX; BEAR + Oversold -> 100% SOXL.
- **Exit:** Regime shift or indicator reversal.
- **Symbols:** SPY, QQQ, SMH, TQQQ, SOXL, UVIX, UVXY
- **Resolution:** Daily (MOC signals)

| Metric | Value |
| :--- | :--- |
| Compounding Annual Return | 124.510% |
| Drawdown | 46.800% |
| Net Profit | 1649526.299% |
| Sharpe Ratio | 1.869 |
| Win Rate | 54% |
| Profit-Loss Ratio | 2.55 |
| Total Orders | 4576 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 64% | 🔴 -11% | 🟢 64% | 🟢 139% | 🟢 20% | 🟢 136% | 🟢 1021% | 🟢 256% | 🟢 18% | 🟢 66% | 🟢 187% | 🟢 382% |

> [!code]- Click to view: it_101.py
> ```embed-python
> PATH: "vault://QuantConnect/gemini/algos/it_101.py"
> ```
