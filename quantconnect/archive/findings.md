# Archived Strategies Findings

This document summarizes historical, experimental, or superseded strategies located in the `quantconnect/archive/` directory.

## Summary Table

| Strategy | CAGR | Max DD | Overfit Risk | Primary Reason for Archival |
| :--- | :--- | :--- | :--- | :--- |
| **Rotation v1** | 104.1% | 56.5% | Moderate | Superseded by newer versions / Version control. |
| **Sector Hedge** | 52.8% | 25.5% | Low-Mod | Experimental; high Sharpe but complex execution. |
| **Gold/Oil Breakout** | 31.0% | 34.5% | Low | Specialized commodity; too narrow for general application. |
| **Large Cap EMA** | 29.2% | 51.5% | Low | Marginal failure of the 30% CAGR target. |
| **Large Cap Breakout** | 27.0% | 65.9% | Low | Inefficient volatility filter caused extreme 2022 DD. |
| **Scratchpad a_11** | 213.2% | 65.6% | **High** | **Optimizer Trap:** Precise thresholds (e.g. 62.1995%). |
| **Scratchpad a_9** | 169.7% | 55.0% | **High** | Extreme alpha; likely fitted to specific bull runs. |
| **Scratchpad a_5** | 169.0% | 47.0% | **High** | **Optimizer Trap:** Precise volatility/DD thresholds. |
| **Scratchpad a_2** | 162.2% | 56.5% | **High** | Prototype for high-beta rotation; high volatility. |
| **Scratchpad a_8** | 113.4% | 41.9% | Moderate | Strong risk-adjusted returns; superseded by v1. |
| **Scratchpad a_4** | 72.9% | 74.6% | **High** | **Regime Fitting:** Specifically tuned for ARKK bubble. |
| **Scratchpad a_6/7** | 53.4% | 33.0% | Low-Mod | Robust SeeSaw logic; identical versions 6 and 7. |
| **Scratchpad a_3** | 46.8% | 24.3% | Low | High-Sharpe "Frontrunner" baseline; low DD. |
| **Scratchpad a_10** | 44.4% | 27.7% | Moderate | **Logic Overfit:** Complex "Frankenfest" indicator chain. |
| **Scratchpad a_1** | 30.5% | 71.4% | Low | Extreme beta decay; failed risk requirements. |

---

## Strategic Significance

### 1. Identifying the "Optimizer Trap" (`a_11`, `a_5`)
The 200%+ CAGR in `a_11` is achieved using hyper-precise thresholds like `62.1995` and `4.9226`. This is a classic example of **overfitting to historical noise**. While it looks impressive on paper, these strategies are brittle and likely to fail in live markets where price action never matches the historical minute-by-minute data exactly.

### 2. High-Alpha Baselines (`rotation_v1.py`, `a_9`)
`rotation_v1.py` and `a_9` demonstrate that macro-regime switching (TQQQ/SQQQ) is the primary driver of 100%+ alpha. These are "Moderate" risk because while the returns are extreme, the underlying concept (trend-following on SPY) is fundamentally sound.

### 3. High-Sharpe and Defensive Logic (`a_3`, `a_10`, Sector Hedge)
`a_3` and `z_sector_rotation_hedge.py` represent the "Low Overfit" path to alpha. By focusing on volatility-adjusted returns and hedging rather than pure directional betting, they maintain a CAGR > 40% with significantly lower drawdowns.

### 4. Regime Fitting (`a_4`)
The "ARKK Machine" (`a_4`) is an example of regime fitting. It captures the 2020-2021 hyper-growth phase perfectly but collapses (74% DD) when that specific market regime ends. 

### 5. Evolution of Volatility Normalization
The transition from `large_cap_breakout.py` (27% CAGR) to the production `breakout.py` highlights why simplicity (EMA gates) is often better than complex, hand-tuned breakout rules that fail during 2022-style shifts.
