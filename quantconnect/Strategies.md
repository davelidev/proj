# QuantConnect Trading Strategies

---

## Volatility Breakout (`vol_breakout.py`)

**Core Concept:** Capture momentum by entering trades during low volatility breakouts and exiting on high volatility spikes.

*   **Total Return:** 7726.292%
*   **CAGR / Max Drawdown:** 43.769% / -43.700%
*   **Sharpe Ratio:** 1.021
*   **Overfit Risk:** Low-Moderate (Uses standard volatility breakout concepts)

> [!code]- Click to view: vol_breakout.py
> ```embed-python
> PATH: "vault://QuantConnect/vol_breakout.py"
> ```

---

## Tech Dip Buy (`dip_buy_tech.py`)

**Core Concept:** Mean-reversion strategy targeting top 5 tech stocks when RSI(2) < 25.

*   **Total Return:** 2652.285%
*   **CAGR / Max Drawdown:** 31.785% / -49.700%
*   **Sharpe Ratio:** 0.879
*   **Overfit Risk:** Low (Standard RSI mean-reversion)

> [!code]- Click to view: dip_buy_tech.py
> ```embed-python
> PATH: "vault://QuantConnect/dip_buy_tech.py"
> ```

---

## Leveraged Rebalance (`leveraged_rebalance.py`)

**Core Concept:** Annual rebalancing of leveraged ETFs (TQQQ, SOXL, TECL) to harvest volatility premium.

*   **Total Return:** 2954.582%
*   **CAGR / Max Drawdown:** 32.936% / -52.000%
*   **Sharpe Ratio:** 0.779
*   **Overfit Risk:** Low (Static allocation with periodic rebalancing)

> [!code]- Click to view: leveraged_rebalance.py
> ```embed-python
> PATH: "vault://QuantConnect/leveraged_rebalance.py"
> ```

---

## Conservative Rotation (`conservative_rotation.py`)

**Core Concept:** Simplified and more conservative version of the macro rotation strategy (formerly v2).

*   **Total Return:** 486251.023%
*   **CAGR / Max Drawdown:** 102.763% / -56.500%
*   **Sharpe Ratio:** 1.605
*   **Overfit Risk:** Moderate (High sensitivity to TQQQ/SQQQ timing)

> [!code]- Click to view: conservative_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/conservative_rotation.py"
> ```

---

## Defensive Rotation (`defensive_rotation.py`)

**Core Concept:** Enhanced macro rotation with defensive gates. Rotates to BIL (Cash) during sharp crashes (RSI < 30) and IEF (Bonds) during sideways bear markets (SPY < SMA200, TQQQ > SMA20) (formerly v3).

*   **Total Return:** 6488.188%
*   **CAGR / Max Drawdown:** 41.767% / -49.800%
*   **Sharpe Ratio:** 0.849
*   **Overfit Risk:** Low-Moderate (Structural hedging reduces volatility/performance but improves robustness)

> [!code]- Click to view: defensive_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/defensive_rotation.py"
> ```

---

## RSI Champion (`rsi_champion.py`)

**Core Concept:** **Champion Strategy.** Oscillates between aggressive growth and cash based on short-term RSI signals on QQQ.

*   **Total Return:** 12960.470%
*   **CAGR / Max Drawdown:** 50.031% / -36.900%
*   **Sharpe Ratio:** 1.08
*   **Overfit Risk:** Moderate (Optimized RSI thresholds for current market regime)

> [!code]- Click to view: rsi_champion.py
> ```embed-python
> PATH: "vault://QuantConnect/rsi_champion.py"
> ```

---

## Holy Grail Refined (`holy_grail_refined.py`)

**Core Concept:** A robust enhancement of the legacy `a_5.py` logic. In a bull market (TQQQ > 200 SMA), holds TQQQ but rotates to Cash (BIL) when RSI(10) > 79 to avoid pullbacks. In a bear market, executes targeted dip-buys on tech/semis (RSI < 31), shorts via SQQQ if momentum is negative, or holds Cash (formerly v18).

*   **Total Return:** 305886.994%
*   **CAGR / Max Drawdown:** 96.182% / -46.600%
*   **Sharpe Ratio:** 1.600
*   **Overfit Risk:** Moderate (Relies on specific RSI thresholds for bear market bounce entries, but fundamentally sound structure).

> [!code]- Click to view: holy_grail_refined.py
> ```embed-python
> PATH: "vault://QuantConnect/holy_grail_refined.py"
> ```
