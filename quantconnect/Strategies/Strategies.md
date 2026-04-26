# QuantConnect Trading Strategies

## Portfolio Summary

| # | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| [1](#strategy-1) | 46.32% | -43.70% | 1.075 |
| [2](#strategy-2) | 32.02% | -46.60% | 0.899 |
| [3](#strategy-3) | 34.74% | -52.00% | 0.812 |
| [4](#strategy-4) | 104.48% | -56.50% | 1.626 |
| [5](#strategy-5) | 41.76% | -49.80% | 0.847 |
| [6](#strategy-6) | 50.11% | -36.90% | 1.081 |
| [7](#strategy-7) | 30.70% | -49.00% | 0.731 |
| [8](#strategy-8) | 96.93% | -46.60% | 1.606 |

---

## Strategy 1
### Volatility Breakout (`vol_breakout.py`)

**Core Concept:** Capture momentum by entering trades during low volatility breakouts and exiting on high volatility spikes.

*   **CAGR / MaxDD:** 46.320% / -43.700%
*   **Sharpe Ratio:** 1.075
*   **Yearly Returns:**

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 87% | 🟢 12% | 🟢 19% | 🟢 98% | 🟢 21% | 🟢 80% | 🟢 144% | 🟢 52% | 🔴 -21% | 🟢 77% | 🟢 61% | 🟢 10% | 🔴 -4% |

> [!code]- Click to view: vol_breakout.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/vol_breakout.py"
> ```

---

## Strategy 2
### Tech Dip Buy (`dip_buy_tech.py`)

**Core Concept:** Mean-reversion strategy targeting top 5 tech stocks when RSI(2) < 25 and Price > SMA(20).

*   **CAGR / MaxDD:** 32.021% / -46.600%
*   **Sharpe Ratio:** 0.899
*   **Yearly Returns:**

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 10% | ⚪ 0% | 🟢 8% | 🟢 34% | 🟢 5% | 🟢 49% | 🟢 61% | 🟢 55% | 🔴 -39% | 🟢 109% | 🟢 122% | 🟢 39% | 🟢 14% |

> [!code]- Click to view: dip_buy_tech.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/dip_buy_tech.py"
> ```

---

## Strategy 3
### Leveraged Rebalance (`leveraged_rebalance.py`)

**Core Concept:** Annual rebalancing of leveraged ETFs (TQQQ, SOXL, TECL) to harvest volatility premium.

*   **CAGR / MaxDD:** 34.743% / -52.000%
*   **Sharpe Ratio:** 0.812
*   **Yearly Returns:**

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 38% | 🟢 1% | 🟢 32% | 🟢 76% | 🔴 -15% | 🟢 107% | 🟢 51% | 🟢 65% | 🔴 -47% | 🟢 127% | 🟢 16% | 🟢 26% | 🟢 46% |

> [!code]- Click to view: leveraged_rebalance.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/leveraged_rebalance.py"
> ```

---

## Strategy 4
### Conservative Rotation (`conservative_rotation.py`)

**Core Concept:** Multi-asset momentum rotation with trend filters.

*   **CAGR / MaxDD:** 104.477% / -56.500%
*   **Sharpe Ratio:** 1.626
*   **Yearly Returns:**

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 58% | 🔴 -2% | 🟢 128% | 🟢 118% | 🟢 25% | 🟢 94% | 🟢 1022% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% | 🟢 16% |

> [!code]- Click to view: conservative_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/conservative_rotation.py"
> ```

---

## Strategy 5
### Defensive Rotation (`defensive_rotation.py`)

**Core Concept:** Macro rotation with defensive gates for crash protection.

*   **CAGR / MaxDD:** 41.763% / -49.800%
*   **Sharpe Ratio:** 0.847
*   **Yearly Returns:**

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 50% | 🔴 -4% | 🟢 6% | 🟢 118% | 🔴 -9% | 🟢 34% | 🟢 234% | 🟢 69% | 🟢 17% | 🟢 59% | 🟢 49% | 🟢 9% | 🔴 -5% |

> [!code]- Click to view: defensive_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/defensive_rotation.py"
> ```

---

## Strategy 6
### RSI Champion (`rsi_champion.py`)

**Core Concept:** Aggressive RSI-based oscillation between Nasdaq growth and cash.

*   **CAGR / MaxDD:** 50.112% / -36.900%
*   **Sharpe Ratio:** 1.081
*   **Yearly Returns:**

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 23% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 🟢 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 51% | 🟢 37% |

> [!code]- Click to view: rsi_champion.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/rsi_champion.py"
> ```

---

## Strategy 7
### TQQQ Dynamic Compounding (`dip_buy_tqqq.py`)

**Core Concept:** Bull trend exposure with dynamic RSI-based de-leveraging.

*   **CAGR / MaxDD:** 30.695% / -49.000%
*   **Sharpe Ratio:** 0.731
*   **Yearly Returns:**

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 39% | 🟢 4% | 🔴 -15% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 69% | 🟢 83% | 🔴 -21% | 🟢 70% | 🟢 29% | 🟢 25% | 🔴 -6% |

> [!code]- Click to view: dip_buy_tqqq.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/dip_buy_tqqq.py"
> ```

---

## Strategy 8
### Holy Grail Refined (`holy_grail_refined.py`)

**Core Concept:** Multi-regime rotation with shorting and dip-buying capabilities.

*   **CAGR / MaxDD:** 96.930% / -46.600%
*   **Sharpe Ratio:** 1.606
*   **Yearly Returns:**

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 62% | 🟢 8% | ⚪ 0% | 🟢 113% | 🟢 16% | 🟢 92% | 🟢 604% | 🟢 88% | 🟢 139% | 🟢 224% | 🟢 62% | 🟢 107% | 🟢 18% |

> [!code]- Click to view: holy_grail_refined.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/holy_grail_refined.py"
> ```
