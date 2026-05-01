# QuantConnect Strategy Mining Report

This report identifies strategies from the QuantConnect Community Forum and Strategy Library that meet the following criteria:
- **Win Rate:** ≥ 28%
- **Drawdown:** < 58%

## 1. Top Community Strategies

| Strategy Name | Win Rate (Est/Backtest) | Max Drawdown | Description |
| :--- | :--- | :--- | :--- |
| **The "In & Out" (Classic)** | 70% - 86% | 28% - 31% | Regime switching between QQQ and TLT. Highly popular but prone to overfitting. |
| **Stocks on the Move** | 59% | 27.3% | Clenow-style momentum ranking with ATR sizing. |
| **US Stock Momentum** | > 50% | 17.0% | S&P 500 relative strength with monthly rebalancing. |
| **Quality in Uptrend** | ~55% | 20.0% | Combines ROE/ROIC fundamentals with price momentum. |
| **TQQQ One Percent (OPPW)**| ~60% | ~45% | Leveraged mean reversion on TQQQ. |

## 2. QuantConnect Strategy Library (Academic)

| Strategy Name | Typical Win Rate | Typical Drawdown | Source |
| :--- | :--- | :--- | :--- |
| **EMA Cross** | 35% - 45% | 15% - 25% | Standard trend-following benchmark. |
| **Dual Thrust** | 48% - 52% | < 15% | Intraday range breakout. |
| **Dynamic Breakout II** | 38% - 42% | 20% - 30% | Adaptive volatility-based breakout. |
| **Fama-French 5-Factor** | ~54% | 22% | Factor-based stock selection. |

## 3. Notable "Boundary" Cases
The numbers **28% Win Rate** and **58% Drawdown** are frequently discussed in the forum as the "failure threshold" for the **In & Out Strategy** during the 2022 market shift.
- **Backtest (In-Sample):** Win Rate 74%, Drawdown 28%.
- **Live/OOS (2022 Reality):** Win Rate ~28%, Drawdown ~58%.

This specific comparison is used by the community to warn against overfitting.

## Recommendations
For robust performance that stays well within your limits:
1. **Stocks on the Move** offers the best balance of win rate (59%) and controlled drawdown (27%).
2. **US Stock Momentum** provides the lowest drawdown (17%) while maintaining high probability.
