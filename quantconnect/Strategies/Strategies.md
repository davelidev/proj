# QuantConnect Trading Strategies

| #               | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :-------------- | :--- | :---- | :----- | :--- | :--- | :--- | :--- |
| [1](#strategy1) | 42%  | -44%  | 0.983  | 172 | 900 | 0.19 | 9.98 |
| [2](#strategy2) | 31%  | -49%  | 0.883  | 37 | 34 | 1.09 | 3.43 |
| [3](#strategy3) | 31%  | -52%  | 0.748  | 35 | 0 | ∞ | 0 |
| [4](#strategy4) | 95%  | -57%  | 1.520  | 100 | 85 | 1.18 | 4.51 |
| [5](#strategy5) | 42%  | -50%  | 0.858  | 159 | 230 | 0.69 | 3.40 |
| [6](#strategy6) | 47%  | -37%  | 1.034  | 1426 | 611 | 2.33 | 0.81 |
| [7](#strategy7) | 31%  | -49%  | 0.738  | 100 | 47 | 2.13 | 1.44 |
| [8](#strategy8) | 92%  | -47%  | 1.548  | 283 | 232 | 1.22 | 2.56 |

| #               | 14         | 15        | 16         | 17         | 18        | 19         | 20          | 21         | 22         | 23          | 24         | 25         |
| :-------------- | :--------- | :-------- | :--------- | :--------- | :-------- | :--------- | :---------- | :--------- | :--------- | :---------- | :--------- | :--------- |
| [1](#strategy1) | 🟢 27%     | 🟢 12%    | 🟢 19%     | 🟢 98%     | 🟢 21%    | 🟢 80%     | 🟢 144%     | 🟢 52%     | 🔴 -21%    | 🟢 77%      | 🟢 61%     | 🟢 8%      |
| [2](#strategy2) | 🟢 18%     | ⚪ 0%      | 🟢 5%      | 🟢 37%     | 🟢 6%     | 🟢 50%     | 🟢 62%      | 🟢 55%     | 🔴 -43%    | 🟢 115%     | 🟢 126%    | 🟢 39%     |
| [3](#strategy3) | 🟢 46%     | 🟢 1%     | 🟢 32%     | 🟢 76%     | 🔴 -15%   | 🟢 107%    | 🟢 51%      | 🟢 65%     | 🔴 -47%    | 🟢 127%     | 🟢 16%     | 🟢 24%     |
| [4](#strategy4) | 🟢 49%     | 🔴 -2%    | 🟢 59%     | 🟢 118%    | 🟢 26%    | 🟢 95%     | 🟢 1020%    | 🟢 88%     | 🟢 77%     | 🟢 142%     | 🟢 62%     | 🟢 68%     |
| [5](#strategy5) | 🟢 36%     | 🟢 3%     | 🟢 6%      | 🟢 118%    | 🔴 -9%    | 🟢 35%     | 🟢 234%     | 🟢 69%     | 🟢 17%     | 🟢 59%      | 🟢 49%     | 🟢 9%      |
| [6](#strategy6) | 🟢 31%     | 🔴 -8%    | 🔴 -20%    | 🟢 50%     | 🟢 19%    | 🟢 37%     | 🟢 215%     | 🟢 142%    | 🟢 22%     | 🟢 76%      | 🟢 74%     | 🟢 51%     |
| [7](#strategy7) | 🟢 35%     | 🟢 4%     | 🔴 -15%    | 🟢 133%    | 🟢 7%     | 🟢 29%     | 🟢 69%      | 🟢 83%     | 🔴 -21%    | 🟢 70%      | 🟢 29%     | 🟢 25%     |
| [8](#strategy8) | 🟢 53%     | 🟢 7%     | 🔴 -6%     | 🟢 113%    | 🟢 17%    | 🟢 91%     | 🟢 604%     | 🟢 88%     | 🟢 139%    | 🟢 224%     | 🟢 62%     | 🟢 107%    |
| **AVG**         | **🟢 37%** | **🟢 2%** | **🟢 10%** | **🟢 93%** | **🟢 9%** | **🟢 66%** | **🟢 300%** | **🟢 80%** | **🟢 15%** | **🟢 111%** | **🟢 60%** | **🟢 41%** |


---

## Strategy1
### Volatility Breakout (vol_breakout.py)

**Description:** Captures momentum by entering trades during low volatility breakouts and exiting on high volatility spikes.

*   **Entry:** Price near 240-minute high (>= 98% of high) AND intra-bar volatility < 0.1.
*   **Exit:** Intra-bar volatility > 0.15 OR 1% trailing stop loss.
*   **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :---- | :----- | :---- | :----- | :-------- | :----------- |
| 42%  | -44%  | 0.983  | 172   | 900    | 0.19      | 9.98         |

| 14     | 15     | 16     | 17     | 18     | 19     | 20      | 21     | 22      | 23     | 24     | 25    |
| :----- | :----- | :----- | :----- | :----- | :----- | :------ | :----- | :------ | :----- | :----- | :---- |
| 🟢 27% | 🟢 12% | 🟢 19% | 🟢 98% | 🟢 21% | 🟢 80% | 🟢 144% | 🟢 52% | 🔴 -21% | 🟢 77% | 🟢 61% | 🟢 8% |

> [!code]- Click to view: vol_breakout.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/vol_breakout.py"
> ```

---

## Strategy2
### Tech Dip Buy (dip_buy_tech.py)

**Description:** Mean-reversion strategy targeting top 5 tech stocks when RSI(2) < 30 and Price > SMA(50).

*   **Entry:** RSI(2) < 30 AND Price > SMA(50) on top 5 market cap tech stocks.
*   **Exit:** 15% hard stop OR price >= 1-year high (ATH proxy).
*   **Symbols:** Dynamic Top 5 Tech (e.g., AAPL, MSFT, NVDA, AVGO, ORCL)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :---- | :----- | :---- | :----- | :-------- | :----------- |
| 31%  | -49%  | 0.883  | 37    | 34     | 1.09      | 3.43         |

| 14     | 15    | 16    | 17     | 18    | 19     | 20     | 21     | 22      | 23      | 24      | 25     |
| :----- | :---- | :---- | :----- | :---- | :----- | :----- | :----- | :------ | :------ | :------ | :----- |
| 🟢 18% | ⚪ 0% | 🟢 5% | 🟢 37% | 🟢 6% | 🟢 50% | 🟢 62% | 🟢 55% | 🔴 -43% | 🟢 115% | 🟢 126% | 🟢 39% |

> [!code]- Click to view: dip_buy_tech.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/dip_buy_tech.py"
> ```

---

## Strategy3
### Leveraged Rebalance (leveraged_rebalance.py)

**Description:** Annual rebalancing of leveraged ETFs (TQQQ, SOXL, TECL) to harvest volatility premium.

*   **Entry:** Annual rebalance at year-start into target weights.
*   **Exit:** N/A (Dynamic weight adjustment).
*   **Symbols:** TQQQ (20%), SOXL (20%), TECL (20%), Cash (40%)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31%  | -52%  | 0.748  | 35 | 0 | ∞ | 0 |

| 14     | 15    | 16     | 17     | 18      | 19      | 20     | 21     | 22      | 23      | 24     | 25     |
| :----- | :---- | :----- | :----- | :------ | :------ | :----- | :----- | :------ | :------ | :----- | :----- |
| 🟢 46% | 🟢 1% | 🟢 32% | 🟢 76% | 🔴 -15% | 🟢 107% | 🟢 51% | 🟢 65% | 🔴 -47% | 🟢 127% | 🟢 16% | 🟢 24% |

> [!code]- Click to view: leveraged_rebalance.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/leveraged_rebalance.py"
> ```

---

## Strategy4
### Conservative Rotation (conservative_rotation.py)

**Description:** Multi-asset momentum rotation strategy switching between leveraged growth and short protection.

*   **Entry:** Default entry is TQQQ (Bullish regime).
*   **Exit:** Rotate to SQQQ (Short) when SPY < SMA(200) AND TQQQ < SMA(20) (unless RSI < 30).
*   **Symbols:** TQQQ, SQQQ, SPY, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 95%  | -57%  | 1.520  | 100 | 85 | 1.18 | 4.51 |

| 14     | 15     | 16     | 17      | 18     | 19     | 20      | 21     | 22     | 23      | 24     | 25     |
| :----- | :----- | :----- | :------ | :----- | :----- | :------ | :----- | :----- | :------ | :----- | :----- |
| 🟢 49% | 🔴 -2% | 🟢 59% | 🟢 118% | 🟢 26% | 🟢 95% | 🟢 1020% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% |

> [!code]- Click to view: conservative_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/conservative_rotation.py"
> ```

---

## Strategy5
### Defensive Rotation (defensive_rotation.py)

**Description:** Macro rotation with multi-layered defensive gates (Bonds and Cash) for crash protection.

*   **Entry:** TQQQ in Bull Markets (SPY > SMA200).
*   **Exit:** Rotate to BIL (RSI < 30), IEF (Bear market rally), or SQQQ (Active bear downtrend).
*   **Symbols:** TQQQ, SQQQ, BIL, IEF, SPY, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 42%  | -50%  | 0.858  | 159 | 230 | 0.69 | 3.40 |

| 14     | 15    | 16    | 17      | 18     | 19     | 20      | 21     | 22     | 23     | 24     | 25     |
| :----- | :---- | :---- | :------ | :----- | :----- | :------ | :----- | :----- | :----- | :----- | :----- |
| 🟢 36% | 🟢 3% | 🟢 6% | 🟢 118% | 🔴 -9% | 🟢 35% | 🟢 234% | 🟢 69% | 🟢 17% | 🟢 59% | 🟢 49% | 🟢 9%  |

> [!code]- Click to view: defensive_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/defensive_rotation.py"
> ```

---

## Strategy6
### RSI Champion (rsi_champion.py)

**Description:** Aggressive RSI-based oscillator swinging between leveraged growth and cash on extreme oversold signals.

*   **Entry:** QQQ RSI(2) < 25 (Extreme daily oversold).
*   **Exit:** Liquidate to cash when QQQ RSI(2) >= 25.
*   **Symbols:** TQQQ, SOXL, TECL, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 47%  | -37%  | 1.034  | 1426 | 611 | 2.33 | 0.81 |

| 14     | 15     | 16      | 17     | 18     | 19     | 20      | 21      | 22     | 23     | 24     | 25     |
| :----- | :----- | :------ | :----- | :----- | :----- | :------ | :------ | :----- | :----- | :----- | :----- |
| 🟢 31% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 51% |

> [!code]- Click to view: rsi_champion.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/rsi_champion.py"
> ```

---

## Strategy7
### TQQQ Dynamic Compounding (dip_buy_tqqq.py)

**Description:** Bull trend strategy that varies TQQQ leverage based on RSI-driven dips and exhaustion.

*   **Entry:** Bull Market (Price > SMA200) AND RSI(2) < 30 (100% leverage).
*   **Exit:** De-leverage to 20% on RSI(10) > 80; Exit to cash if Bear Market (Price < SMA200).
*   **Symbols:** TQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31%  | -49%  | 0.738  | 100 | 47 | 2.13 | 1.44 |

| 14     | 15    | 16      | 17      | 18    | 19     | 20     | 21     | 22      | 23     | 24     | 25     |
| :----- | :---- | :------ | :------ | :---- | :----- | :----- | :----- | :------ | :----- | :----- | :----- |
| 🟢 35% | 🟢 4% | 🔴 -15% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 69% | 🟢 83% | 🔴 -21% | 🟢 70% | 🟢 29% | 🟢 25% |

> [!code]- Click to view: dip_buy_tqqq.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/dip_buy_tqqq.py"
> ```

---

## Strategy8
### Holy Grail Refined (holy_grail_refined.py)

**Description:** Multi-regime rotation optimizing for crash protection and opportunistic bear-market bounces.

*   **Entry:** Bull Market (TQQQ > SMA200) -> Hold TQQQ; Bear Market -> Dip buy TECL/SOXL on RSI pullbacks.
*   **Exit:** Rotate to BIL (Cash) if RSI(10) > 79 (Bull) or based on relative momentum (Bear).
*   **Symbols:** TQQQ, TECL, SOXL, SQQQ, BIL

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 92%  | -47%  | 1.548  | 283 | 232 | 1.22 | 2.56 |

| 14     | 15    | 16     | 17      | 18     | 19     | 20      | 21     | 22      | 23      | 24     | 25      |
| :----- | :---- | :----- | :------ | :----- | :----- | :------ | :----- | :------ | :------ | :----- | :------ |
| 🟢 53% | 🟢 7% | 🔴 -6% | 🟢 113% | 🟢 17% | 🟢 91% | 🟢 604% | 🟢 88% | 🟢 139% | 🟢 224% | 🟢 62% | 🟢 107% |

> [!code]- Click to view: holy_grail_refined.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/holy_grail_refined.py"
> ```
