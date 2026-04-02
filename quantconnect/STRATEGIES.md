# QuantConnect Trading Strategies

This document provides an overview and the source code for the trading strategies located in the `quantconnect/` directory.

---

## Volatility Breakout (`breakout.py`)

**Core Concept:** Capture momentum by entering trades during low volatility breakouts and exiting on high volatility spikes.

*   **Total Return:** 7726.292%
*   **CAGR / Max Drawdown:** 43.769% / -43.700%
*   **Sharpe Ratio:** 1.021
*   **Overfit Risk:** Low-Moderate (Uses standard volatility breakout concepts)

> [!code]- Click to view: breakout.py
> ```embed-python
> PATH: "vault://quantconnect/breakout.py"
> ```

---

## Large Cap Tech Dip Buy (`large_cap_dip_buy.py`)

**Core Concept:** Mean-reversion strategy targeting top 5 tech stocks when RSI(2) < 25.

*   **Total Return:** 2652.285%
*   **CAGR / Max Drawdown:** 31.785% / -49.700%
*   **Sharpe Ratio:** 0.879
*   **Overfit Risk:** Low (Standard RSI mean-reversion)

> [!code]- Click to view: large_cap_dip_buy.py
> ```embed-python
> PATH: "vault://quantconnect/large_cap_dip_buy.py"
> ```

---

## Fixed-Weight Rebalance (`rebalance.py`)

**Core Concept:** Annual rebalancing of leveraged ETFs (TQQQ, SOXL, TECL) to harvest volatility premium.

*   **Total Return:** 2954.582%
*   **CAGR / Max Drawdown:** 32.936% / -52.000%
*   **Sharpe Ratio:** 0.779
*   **Overfit Risk:** Low (Static allocation with periodic rebalancing)

> [!code]- Click to view: rebalance.py
> ```embed-python
> PATH: "vault://quantconnect/rebalance.py"
> ```

---

## Regime Rotation v2 (`rotation_v2.py`)

**Core Concept:** Simplified and more conservative version of the macro rotation strategy.

*   **Total Return:** 486251.023%
*   **CAGR / Max Drawdown:** 102.763% / -56.500%
*   **Sharpe Ratio:** 1.605
*   **Overfit Risk:** Moderate (High sensitivity to TQQQ/SQQQ timing)

> [!code]- Click to view: rotation_v2.py
> ```embed-python
> PATH: "vault://quantconnect/rotation_v2.py"
> ```

---

## Rotation Strategy v3 (rotation_v3.py)

**Core Concept:** Enhanced macro rotation with defensive gates. Rotates to BIL (Cash) during sharp crashes (RSI < 30) and IEF (Bonds) during sideways bear markets (SPY < SMA200, TQQQ > SMA20).

*   **Total Return:** 2410.518%
*   **CAGR / Max Drawdown:** 30.331% / -45.800%
*   **Sharpe Ratio:** 0.700
*   **Overfit Risk:** Low-Moderate (Structural hedging reduces volatility/performance but improves robustness)

> [!code]- Click to view: rotation_v3.py
> ```embed-python
> PATH: "vault://quantconnect/rotation_v3.py"
> ```

---

## Dual Regime RSI Rotation (`rsi_rebalance.py`)

**Core Concept:** **Champion Strategy.** Oscillates between aggressive growth and cash based on short-term RSI signals on QQQ.

*   **Total Return:** 12960.470%
*   **CAGR / Max Drawdown:** 50.031% / -36.900%
*   **Sharpe Ratio:** 1.08
*   **Overfit Risk:** Moderate (Optimized RSI thresholds for current market regime)

> [!code]- Click to view: rsi_rebalance.py
> ```embed-python
> PATH: "vault://quantconnect/rsi_rebalance.py"
> ```

---

## The Holy Grail Refined (`rotation_v18.py`)

**Core Concept:** A robust enhancement of the legacy `a_5.py` logic. In a bull market (TQQQ > 200 SMA), holds TQQQ but rotates to Cash (BIL) when RSI(10) > 79 to avoid pullbacks. In a bear market, executes targeted dip-buys on tech/semis (RSI < 31), shorts via SQQQ if momentum is negative, or holds Cash.

*   **Total Return:** 305886.994%
*   **CAGR / Max Drawdown:** 96.182% / -46.600%
*   **Sharpe Ratio:** 1.600
*   **Overfit Risk:** Moderate (Relies on specific RSI thresholds for bear market bounce entries, but fundamentally sound structure).

> [!code]- Click to view: rotation_v18.py
> ```embed-python
> PATH: "vault://quantconnect/rotation_v18.py"
> ```
