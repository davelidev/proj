# QuantConnect Trading Strategies

## Portfolio Summary

| # | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| [1](#strategy1) | 42% | -44% | 0.983 |
| [2](#strategy2) | 32% | -47% | 0.900 |
| [3](#strategy3) | 31% | -52% | 0.748 |
| [4](#strategy4) | 95% | -57% | 1.520 |
| [5](#strategy5) | 42% | -50% | 0.858 |
| [6](#strategy6) | 47% | -37% | 1.034 |
| [7](#strategy7) | 31% | -49% | 0.738 |
| [8](#strategy8) | 92% | -47% | 1.548 |

## Yearly Returns Summary

| # | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [1](#strategy1) | 🟢 27% | 🟢 12% | 🟢 19% | 🟢 98% | 🟢 21% | 🟢 80% | 🟢 144% | 🟢 52% | 🔴 -21% | 🟢 77% | 🟢 61% | 🟢 8% |
| [2](#strategy2) | 🟢 17% | 🟢 3% | 🟢 8% | 🟢 35% | 🟢 6% | 🟢 49% | 🟢 61% | 🟢 55% | 🔴 -39% | 🟢 109% | 🟢 123% | 🟢 39% |
| [3](#strategy3) | 🟢 46% | 🟢 1% | 🟢 32% | 🟢 76% | 🔴 -15% | 🟢 107% | 🟢 51% | 🟢 65% | 🔴 -47% | 🟢 127% | 🟢 16% | 🟢 24% |
| [4](#strategy4) | 🟢 49% | 🔴 -2% | 🟢 59% | 🟢 118% | 🟢 26% | 🟢 95% | 🟢 1020% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% |
| [5](#strategy5) | 🟢 36% | 🟢 3% | 🟢 6% | 🟢 118% | 🔴 -9% | 🟢 35% | 🟢 234% | 🟢 69% | 🟢 17% | 🟢 59% | 🟢 49% | 🟢 9% |
| [6](#strategy6) | 🟢 31% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 🟢 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 51% |
| [7](#strategy7) | 🟢 35% | 🟢 4% | 🔴 -15% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 69% | 🟢 83% | 🔴 -21% | 🟢 70% | 🟢 29% | 🟢 25% |
| [8](#strategy8) | 🟢 53% | 🟢 7% | 🔴 -6% | 🟢 113% | 🟢 17% | 🟢 91% | 🟢 604% | 🟢 88% | 🟢 139% | 🟢 224% | 🟢 62% | 🟢 107% |
| **AVG** | **🟢 37%** | **🟢 3%** | **🟢 10%** | **🟢 93%** | **🟢 9%** | **🟢 67%** | **🟢 300%** | **🟢 80%** | **🟢 16%** | **🟢 111%** | **🟢 60%** | **🟢 41%** |

---

## Strategy1
### Volatility Breakout (vol_breakout.py)

**Core Concept:** Capture momentum by entering trades during low volatility breakouts and exiting on high volatility spikes.

| CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- |
| 42% | -44% | 0.983 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 27% | 🟢 12% | 🟢 19% | 🟢 98% | 🟢 21% | 🟢 80% | 🟢 144% | 🟢 52% | 🔴 -21% | 🟢 77% | 🟢 61% | 🟢 8% |

> [!code]- Click to view: vol_breakout.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/vol_breakout.py"
> ```

---

## Strategy2
### Tech Dip Buy (dip_buy_tech.py)

**Core Concept:** Mean-reversion strategy targeting top 5 tech stocks when RSI(2) < 25 and Price > SMA(20).

| CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- |
| 32% | -47% | 0.900 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 17% | 🟢 3% | 🟢 8% | 🟢 35% | 🟢 6% | 🟢 49% | 🟢 61% | 🟢 55% | 🔴 -39% | 🟢 109% | 🟢 123% | 🟢 39% |

> [!code]- Click to view: dip_buy_tech.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/dip_buy_tech.py"
> ```

---

## Strategy3
### Leveraged Rebalance (leveraged_rebalance.py)

**Core Concept:** Annual rebalancing of leveraged ETFs (TQQQ, SOXL, TECL) to harvest volatility premium.

| CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- |
| 31% | -52% | 0.748 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 46% | 🟢 1% | 🟢 32% | 🟢 76% | 🔴 -15% | 🟢 107% | 🟢 51% | 🟢 65% | 🔴 -47% | 🟢 127% | 🟢 16% | 🟢 24% |

> [!code]- Click to view: leveraged_rebalance.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/leveraged_rebalance.py"
> ```

---

## Strategy4
### Conservative Rotation (conservative_rotation.py)

**Core Concept:** Multi-asset momentum rotation with trend filters.

| CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- |
| 95% | -57% | 1.520 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 49% | 🔴 -2% | 🟢 59% | 🟢 118% | 🟢 26% | 🟢 95% | 🟢 1020% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% |

> [!code]- Click to view: conservative_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/conservative_rotation.py"
> ```

---

## Strategy5
### Defensive Rotation (defensive_rotation.py)

**Core Concept:** Macro rotation with defensive gates for crash protection.

| CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- |
| 42% | -50% | 0.858 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 36% | 🟢 3% | 🟢 6% | 🟢 118% | 🔴 -9% | 🟢 35% | 🟢 234% | 🟢 69% | 🟢 17% | 🟢 59% | 🟢 49% | 🟢 9% |

> [!code]- Click to view: defensive_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/defensive_rotation.py"
> ```

---

## Strategy6
### RSI Champion (rsi_champion.py)

**Core Concept:** Aggressive RSI-based oscillation between Nasdaq growth and cash.

| CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- |
| 47% | -37% | 1.034 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 31% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 🟢 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 51% |

> [!code]- Click to view: rsi_champion.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/rsi_champion.py"
> ```

---

## Strategy7
### TQQQ Dynamic Compounding (dip_buy_tqqq.py)

**Core Concept:** Bull trend exposure with dynamic RSI-based de-leveraging.

| CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- |
| 31% | -49% | 0.738 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 35% | 🟢 4% | 🔴 -15% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 69% | 🟢 83% | 🔴 -21% | 🟢 70% | 🟢 29% | 🟢 25% |

> [!code]- Click to view: dip_buy_tqqq.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/dip_buy_tqqq.py"
> ```

---

## Strategy8
### Holy Grail Refined (holy_grail_refined.py)

**Core Concept:** Multi-regime rotation with shorting and dip-buying capabilities.

| CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- |
| 92% | -47% | 1.548 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 53% | 🟢 7% | 🔴 -6% | 🟢 113% | 🟢 17% | 🟢 91% | 🟢 604% | 🟢 88% | 🟢 139% | 🟢 224% | 🟢 62% | 🟢 107% |

> [!code]- Click to view: holy_grail_refined.py
> ```embed-python
> PATH: "vault://QuantConnect/Strategies/holy_grail_refined.py"
> ```
