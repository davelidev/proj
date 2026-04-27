# 🧪 Algorithmic Trading Research Log (Elite Strategies Only)

This file tracks the testing of strategies derived from Kevin Davey's research that met the strict performance criteria.

## Performance Criteria
*   **CAGR:** > 30%
*   **Max Drawdown:** < 57%

---

## Strategy 38 (`research/strategy_38.py`)

**Core Concept:** Expanding Volatility + SOXL/TQQQ Momentum Rotation + VIX/VIX3M Structural Shield.

*   **CAGR / Max Drawdown:** 44.621% / -50.200%
*   **Sharpe Ratio:** 0.977

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 66% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 13% | 🟢 16% | 🟢 184% | 🟢 95% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% | 🟢 75% |

> [!code]- Click to view: strategy_38.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_38.py"
> ```

---

## Strategy Iteration 69 (`research/strategy_template.py`)

**Core Concept:** Automated optimization of RSI and VIX parameters on TQQQ/SOXL rotator.

*   **CAGR / Max Drawdown:** 44.557% / -52.600%
*   **Sharpe Ratio:** 0.976
*   **Parameters:** {
  "sma200_len": "200",
  "rsi_trigger": "25.52",
  "rsi_exit": "70.64",
  "vix_limit": "32.95",
  "vix_ratio_limit": "1.073",
  "use_soxl": "false",
  "atr_stop_mult": "2.63"
}

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 82% | 🟢 19% | 🔴 -29% | 🟢 140% | 🔴 -8% | 🟢 112% | 🟢 144% | 🟢 76% | 🔴 -23% | 🟢 139% | 🟢 45% | 🟢 3% | 🔴 -4% |

> [!code]- Click to view: strategy_template.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_template.py"
> ```

---

## Strategy Iteration 60 (`research/strategy_template.py`)

**Core Concept:** TQQQ-focused automated dip-buy optimization with tight VIX shield.

*   **CAGR / Max Drawdown:** 42.730% / -52.000%
*   **Sharpe Ratio:** 0.946
*   **Parameters:** {
  "sma200_len": "200",
  "rsi_trigger": "24.55",
  "rsi_exit": "87.57",
  "vix_limit": "25.51",
  "vix_ratio_limit": "1.018",
  "use_soxl": "false",
  "atr_stop_mult": "2.58"
}

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 76% | 🟢 19% | 🔴 -29% | 🟢 128% | 🔴 -15% | 🟢 109% | 🟢 144% | 🟢 76% | 🔴 -23% | 🟢 137% | 🟢 44% | 🟢 8% | 🔴 -4% |

> [!code]- Click to view: strategy_template.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_template.py"
> ```

---

## Strategy 36 (`research/strategy_36.py`)

**Core Concept:** Triple-LETF Rotator (TQQQ/SOXL/TECL) with Expanding Range momentum logic.

*   **CAGR / Max Drawdown:** 42.448% / -50.600%
*   **Sharpe Ratio:** 0.920

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 86% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 27% | 🟢 17% | 🟢 71% | 🟢 115% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% | 🟢 75% |

> [!code]- Click to view: strategy_36.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_36.py"
> ```

---

## Strategy 35 (`research/strategy_35.py`)

**Core Concept:** Expanding Strong Trend logic with dynamic SOXL rotation and ADX filters.

*   **CAGR / Max Drawdown:** 42.226% / -50.200%
*   **Sharpe Ratio:** 0.917

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 86% | 🔴 -22% | ⚪ 0% | 🟢 54% | 🟢 28% | 🟢 16% | 🟢 83% | 🟢 95% | 🔴 -14% | 🟢 63% | 🟢 83% | 🟢 28% | 🟢 75% |

> [!code]- Click to view: strategy_35.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_35.py"
> ```

---

## Strategy Iteration 192 (`research/strategy_template.py`)

**Core Concept:** Aggressive automated RSI pullback optimizer for bull market compounding.

*   **CAGR / Max Drawdown:** 37.926% / -54.000%
*   **Sharpe Ratio:** 0.849
*   **Parameters:** {
  "sma200_len": "200",
  "rsi_trigger": "21.09",
  "rsi_exit": "89.35",
  "vix_limit": "33.68",
  "vix_ratio_limit": "0.988",
  "use_soxl": "false",
  "atr_stop_mult": "2.69"
}

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 71% | 🟢 5% | 🔴 -30% | 🟢 102% | 🔴 -29% | 🟢 113% | 🟢 145% | 🟢 76% | 🔴 -23% | 🟢 139% | 🟢 39% | 🟢 4% | 🟢 8% |

> [!code]- Click to view: strategy_template.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_template.py"
> ```

---

## Strategy 34 (`research/strategy_34.py`)

**Core Concept:** Expanding Trend logic replacing trailing stops with 20-day high profit targets.

*   **CAGR / Max Drawdown:** 37.972% / -49.500%
*   **Sharpe Ratio:** 0.880

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 85% | 🔴 -3% | 🔴 -6% | 🟢 76% | 🟢 54% | 🟢 14% | 🟢 85% | 🟢 49% | 🔴 -14% | 🟢 81% | 🟢 36% | 🟢 28% | 🟢 21% |

> [!code]- Click to view: strategy_34.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_34.py"
> ```

---

## Strategy 22 (`research/strategy_22.py`)

**Core Concept:** High-Octane RSI Swing. Entry on leader dips (NVDA/AMD/TSLA) -> 100% TQQQ.

*   **CAGR / Max Drawdown:** 37.376% / -51.500%
*   **Sharpe Ratio:** 0.827

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 66% | 🟢 5% | 🔴 -17% | 🟢 118% | 🔴 -5% | 🟢 25% | 🟢 123% | 🟢 88% | 🔴 -27% | 🟢 80% | 🟢 62% | 🟢 27% | 🟢 6% |

> [!code]- Click to view: strategy_22.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_22.py"
> ```

---

## Strategy 31 (`research/strategy_31.py`)

**Core Concept:** Expanding Breakout with tightened ADX trend filters and 3.0 ATR protection.

*   **CAGR / Max Drawdown:** 35.641% / -49.500%
*   **Sharpe Ratio:** 0.834

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 86% | 🔴 -3% | 🔴 -6% | 🟢 78% | 🟢 28% | 🟢 11% | 🟢 84% | 🟢 49% | 🔴 -14% | 🟢 81% | 🟢 36% | 🟢 28% | 🟢 21% |

> [!code]- Click to view: strategy_31.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_31.py"
> ```

---

## Strategy 16 (`research/strategy_16.py`)

**Core Concept:** Classic Expanding Breakout (Yest Range > Prev Range) with 2.5 ATR trailing stop.

*   **CAGR / Max Drawdown:** 30.904% / -56.600%
*   **Sharpe Ratio:** 0.726

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 85% | 🔴 -24% | 🔴 -19% | 🟢 92% | 🔴 -1% | 🟢 50% | 🟢 135% | 🟢 43% | 🔴 -25% | 🟢 42% | 🟢 87% | 🟢 10% | 🟢 7% |

> [!code]- Click to view: strategy_16.py
> ```embed-python
> PATH: "vault://QuantConnect/research/strategy_16.py"
> ```

---

## Strategy 8 (`dip_buy_tqqq.py`)

**Core Concept:** Dynamic Compounding. Varies TQQQ leverage based on RSI2 dip/RSI10 exhaustion.

*   **CAGR / Max Drawdown:** 30.695% / -49.000%
*   **Sharpe Ratio:** 0.731

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 39% | 🟢 4% | 🔴 -15% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 69% | 🟢 83% | 🔴 -21% | 🟢 70% | 🟢 29% | 🟢 25% | 🔴 -6% |

> [!code]- Click to view: dip_buy_tqqq.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/dip_buy_tqqq.py"
> ```

---

## Strategy 11 (`research/cheat_code_rotator_tqqq.py`)

**Core Concept:** Pure Cheat Code logic. 200 SMA Bull Filter + VIX Shield + RSI2 Dip entry.

*   **CAGR / Max Drawdown:** 30.102% / -50.200%
*   **Sharpe Ratio:** 0.728

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 69% | 🟢 8% | 🔴 -25% | 🟢 137% | 🔴 -16% | 🟢 20% | 🟢 69% | 🟢 61% | 🔴 -27% | 🟢 104% | 🟢 64% | 🟢 32% | 🔴 -18% |

> [!code]- Click to view: cheat_code_rotator_tqqq.py
> ```embed-python
> PATH: "vault://QuantConnect/research/cheat_code_rotator_tqqq.py"
> ```

---
