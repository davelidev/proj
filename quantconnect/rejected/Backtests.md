# Rejected Strategies Findings

This document explains why various strategies were rejected for failing to meet the strict requirements: **CAGR > 30%** and **Max Drawdown < 57%** over a 12-year simulation.

## Summary Table

| Strategy | CAGR | Max DD | Primary Reason for Rejection |
| :--- | :--- | :--- | :--- |
| **VAA Leveraged** | 26.3% | 37.3% | **CAGR Ceiling:** Too conservative to hit 30%. |
| **BAA Leveraged** | 23.9% | 37.4% | **CAGR Ceiling:** Defensive rotation capped returns. |
| **Vol Targeting** | 17.5% | 33.5% | **Growth Drag:** De-leveraging during high-vol recovery. |
| **VAA Aggressive**| 20.5% | 78.0% | **Risk Leak:** Relaxed entry rules caused 2022 failure. |
| **VAA Max** | 11.4% | 73.6% | **Beta Decay:** FNGU/TECL volatility destroyed capital. |
| **Sector Rotation**| 20.4% | 75.7% | **Signal Lag:** Monthly rebalancing is too slow for LETFs. |
| **Hybrid LETF** | 42.2% | 73.3% | **High Beta DD:** SMA filter failed to stop 2022 decay. |
| **TQQQ SMA (48/49)**| 13.8% | 68.1% | **Whipsaws:** Ineffective in non-trending volatile markets. |
| **VIX Term Structure**| 22.3% | 58.3% | **Marginal Failure:** Failed both metrics slightly. |
| **LS Mean Reversion**| 4.3% | 65.9% | **Signal Noise:** Short-term RSI on LETFs is unreliable. |
| **Weekly Rebalance**| 5.6% | 86.9% | **Over-trading:** Destroyed by weekly whipsaws. |
| **Vol Spike Reversion**| 1.9% | 67.6% | **Bad Entries:** "Falling knife" entries in bear markets. |
| **Commodity-Equity**| 20.6% | 63.8% | **Uncorrelated DD:** GUSH volatility was too extreme. |
| **VIX Sector RSI** | 9.7% | 42.9% | **Over-filtering:** Missed too many high-alpha periods. |
| **ML Regression** | 5.7% | 73.2% | **Overfitting:** Daily regression failed to capture trends. |
| **Pair Switching** | 5.2% | 75.7% | **Small-Cap Drag:** TNA performance was fatal in 2022. |
| **TQQQ SVXY Alpha** | 17.5% | 39.8% | **Slow Recovery:** Short vol drag during spike regimes. |
| **TQQQ SOXL Mom** | 26.2% | 69.0% | **Concentration Risk:** SOXL drawdown exceeded limits. |
| **TQQQ TECL Alpha** | 23.5% | 69.6% | **Tech Correlation:** No hedging during tech crashes. |
| **TQQQ SQQQ Macro** | 5.1% | 79.0% | **Shorting Risk:** SQQQ squeezed during bear rallies. |
| **TQQQ SOXL MR** | 20.8% | 48.0% | **Opportunity Cost:** Too selective, missed bull meat. |
| **TQQQ BULZ Rot** | 1.8% | 95.1% | **Inception Risk:** BULZ launched at the market peak. |
| **TQQQ Golden Cross**| 19.3% | 69.9% | **Lag:** 50/200 SMA is too slow for 3x instruments. |
| **TQQQ TECL Trend** | 16.4% | 53.5% | **CAGR Ceiling:** Trend following capped growth. |

---

## Key Lessons Learned

### 1. The Leveraged Decay Paradox
Leveraged ETFs (3x) like TQQQ and SOXL suffer from "volatility decay" in sideways markets. Any strategy that uses monthly rebalancing or slow moving averages (like the Golden Cross) is mathematically destined to fail during extended volatile periods like 2022 because they stay invested while the asset "chops" downward.

### 2. The Defense vs. Growth Trade-off
Strategies like VAA and BAA that provide excellent drawdown protection (keeping DD < 40%) consistently fail the >30% CAGR requirement. This is because the "Risk-Off" state (moving to TLT/IEF/BIL) misses the initial explosive "V-shaped" recovery of high-beta assets.

### 3. Machine Learning Complexity
Simple linear regression on daily returns (`ml_momentum_regression.py`) proved ineffective. Market noise at the daily level is too high for a basic ML model to distinguish between a "dip" and the "start of a crash."

### 4. Mean Reversion Selectivity
The only strategy that consistently hit the target was `rsi_rebalance.py` because it combined **daily** checks with **aggressive dip buying**. The rejected mean reversion versions failed because they were either too selective (missing the trade) or not selective enough (catching falling knives).
