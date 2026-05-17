# QuantConnect Trading Strategies

| #                  | Category       | CAGR    | MaxDD    | Sharpe    | Win #    | Loss #  | W/L Ratio | Profit Ratio | Overfit |     |     |
| :----------------- | :------------- | :------ | :------- | :-------- | :------- | :------ | :-------- | :----------- | :------ | --- | --- |
| [1](#strategy-1)   | Breakout       | 43%     | -37%     | 0.986     | 192      | 341     | 0.56      | 3.45         | 6/10    |     |     |
| [2](#strategy-2)   | Dip Buy        | 28%     | -42%     | 0.846     | 42       | 38      | 1.11      | 3.11         | 2/10    |     |     |
| ✅ [3](#strategy-3) | Rebalance | 28% | -51% | 0.728 | 13 | 0 | — | 0.00 | 4/10 |
| ✅ [4](#strategy-4) | Dip Buy | 47% | -37% | 1.031 | 1426 | 611 | 2.33 | 0.81 | 2/10 |
| ✅ [5](#strategy-5) | Trend | 31% | -49% | 0.738 | 65 | 57 | 1.14 | 2.69 | 4/10 |
| ✅ [6](#strategy-6) | Breakout | 38% | -49% | 0.886 | 94 | 76 | 1.24 | 2.19 | 4/10 |
| ✅ [7](#strategy-7) | Trend          | 40%     | -55%     | 0.871     | 11       | 17      | 0.65      | 8.14         | 2/10    |     |     |
| ✅ [8](#strategy-8) | Mean Reversion | 46%     | -43%     | 1.049     | 137      | 51      | 2.69      | 1.14         | 3/10    |     |     |
|  [9](#strategy-9)  | Rotation       | 30%     | -23%     | 1.073     | 390      | 327     | 1.19      | 2.12         | 3/10    |     |     |
| **ENSEMBLE**       | **Ensemble**   | **38%** | **-33%** | **1.036** | **1535** | **863** | **1.78**  | **1.51**     | **—**   |     |     |


| #                | 14         | 15        | 16       | 17         | 18        | 19         | 20          | 21         | 22          | 23         | 24         | 25         |
| :--------------- | :--------- | :-------- | :------- | :--------- | :-------- | :--------- | :---------- | :--------- | :---------- | :--------- | :--------- | :--------- |
| [1](#strategy-1) | 🟢 43%     | 🟢 8%     | 🟢 26%   | 🟢 101%    | 🟢 23%    | 🟢 105%    | 🟢 149%     | 🟢 23%     | 🔴 -32%     | 🟢 107%    | 🟢 52%     | 🟢 18%     |
| [2](#strategy-2) | 🟢 20%     | ⚪ 0%      | 🟢 8%    | 🟢 37%     | 🟢 6%     | 🟢 39%     | 🟢 38%      | 🟢 53%     | 🔴 -35%     | 🟢 87%     | 🟢 119%    | 🟢 38%     |
| [3](#strategy-3) | 🟢 34%     | 🟢 13%    | 🟢 7%    | 🟢 71%     | 🔴 -13%   | 🟢 79%     | 🟢 65%      | 🟢 52%     | 🔴 -47%     | 🟢 118%    | 🟢 37%     | 🟢 21%     |
| [4](#strategy-4) | 🟢 39%     | 🟢 1%     | 🔴 -18%  | 🟢 46%     | 🟢 12%    | 🟢 34%     | 🟢 81%      | 🟢 110%    | 🟢 33%      | 🟢 60%     | 🟢 72%     | 🟢 66%     |
| [5](#strategy-5) | 🟢 35%     | 🟢 4%     | 🔴 -13%  | 🟢 133%    | 🟢 7%     | 🟢 29%     | 🟢 67%      | 🟢 82%     | 🔴 -20%     | 🟢 70%     | 🟢 29%     | 🟢 28%     |
| [6](#strategy-6) | 🟢 144%    | 🔴 -6%    | 🔴 -6%   | 🟢 76%     | 🟢 54%    | 🟢 14%     | 🟢 84%      | 🟢 49%     | 🔴 -14%     | 🟢 72%     | 🟢 39%     | 🟢 28%     |
| [7](#strategy-7) | 🟢 47%     | 🟢 18%    | 🔴 -5%   | 🟢 118%    | 🟢 1%     | 🟢 53%     | 🟢 97%      | 🟢 88%     | 🔴 -34%     | 🟢 125%    | 🟢 45%     | 🟢 27%     |
| [8](#strategy-8) | 🟢 7%      | 🟢 6%     | 🟢 39%   | 🟢 71%     | 🔴 -29%   | 🟢 33%     | 🟢 344%     | 🟢 75%     | 🔴 -1%      | 🟢 101%    | 🟢 29%     | 🟢 82%     |
| [9](#strategy-9) | 🟢 11%     | 🟢 5%     | 🟢 4%    | 🟢 38%     | 🟢 15%    | 🟢 47%     | 🟢 95%      | 🟢 46%     | 🔴 -11%     | 🟢 51%     | 🟢 38%     | 🟢 50%     |
| **ENSEMBLE**     | **🟢 44%** | **🟢 5%** | **⚪ 0%** | **🟢 79%** | **🟢 4%** | **🟢 42%** | **🟢 113%** | **🟢 72%** | **🔴 -16%** | **🟢 88%** | **🟢 44%** | **🟢 46%** |

> Note: Checkmarked strategies (✅) are considered "selected" and contribute to the ENSEMBLE calculations. VolBreakout (strategy-1) and Tech Dip Buy (strategy-2) are disabled, so 7 sub-algos are active.*

---

## Strategy-1
### Volatility Breakout (vol_breakout.py)

**Description:** Waits for TQQQ to quietly compress near a recent high, then enters expecting a breakout. Gets out as soon as volatility spikes or the stop is hit. Operates on minute bars, so it is trying to exploit intraday momentum patterns rather than daily trends.

*Overfit 6/10 — 6 tuned parameters plus a custom volatility threshold pair (0.1/0.15) that aren't standard values; intraday minute-bar logic narrows the historical sample significantly.*

- **Entry:** Price >= 98% of 240-min high AND avg intra-bar volatility < 0.1
- **Exit:** Avg intra-bar volatility > 0.15 OR 3% stop loss
- **Symbols:** TQQQ
- **Resolution:** Minute

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 43% | -37% | 0.986 | 192 | 341 | 0.56 | 3.45 |

| 14     | 15    | 16     | 17     | 18     | 19      | 20      | 21     | 22      | 23     | 24     | 25     |
| :----- | :---- | :----- | :----- | :----- | :------ | :------ | :----- | :------ | :----- | :----- | :----- |
| 🟢 43% | 🟢 8% | 🟢 26% | 🟢 101% | 🟢 23% | 🟢 105% | 🟢 149% | 🟢 23% | 🔴 -32% | 🟢 107% | 🟢 52% | 🟢 18% |

> [!code]- Click to view: vol_breakout.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/vol_breakout.py"
> ```

---

## Strategy-2
### Tech Dip Buy (tech_dip.py)

**Description:** Buys the biggest tech names when they pull back hard during an uptrend, then holds until they recover to new highs or the loss gets too large. Universe rotates automatically as market caps shift, so it always targets the current leaders.

*Overfit 2/10 — textbook RSI(2)/SMA(50) entry with a clean 15% hard stop; dynamic universe removes hindsight symbol selection; only mild concern is the small trade count (71 trades).*

- **Entry:** RSI(2) < 30 AND price > SMA(50); equal weight across held positions
- **Exit:** Price <= avg cost × 0.85 (15% hard stop) OR price >= 252-day high (1-yr ATH)
- **Symbols:** Dynamic top 5 tech by market cap (e.g. AAPL, MSFT, NVDA, AVGO, ORCL)
- **Rebalance:** Weekly

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :----------- |
| ✅ | 28% | -41% | 0.848 | 53 | 47 | 1.13 | 2.69 |

| 14     | 15    | 16    | 17     | 18    | 19     | 20     | 21     | 22      | 23      | 24      | 25     |
| :----- | :---- | :---- | :----- | :---- | :----- | :----- | :----- | :------ | :------ | :------ | :----- |
| 🟢 20% | ⚪ 0% | 🟢 8% | 🟢 37% | 🟢 6% | 🟢 39% | 🟢 38% | 🟢 53% | 🔴 -35% | 🟢 87% | 🟢 119% | 🟢 38% |

> [!code]- Click to view: tech_dip.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/tech_dip.py"
> ```

---

## Strategy-3
### Leveraged Rebalance (leveraged_rebalance.py)

**Description:** Holds three leveraged ETFs and cash in fixed proportions, restoring those proportions once a year. No signals, no timing decisions. Returns come almost entirely from what it holds rather than how it manages positions — TQQQ, SOXL, and TECL were among the best-performing ETFs of the backtest decade, which is a hindsight advantage.

*Overfit 4/10 — zero mechanical parameter tuning, but choosing TQQQ/SOXL/TECL specifically is a form of hindsight bias; you could only know these were the best picks after seeing the decade play out.*

- **Entry:** Annual rebalance to target weights
- **Exit:** N/A — weight drift only corrected annually
- **Symbols:** TQQQ 20%, SOXL 20%, TECL 20%, Cash 40%
- **Rebalance:** Yearly

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :----------- |
| ✅ | 28% | -51% | 0.728 | 13 | 0 | — | 0.00 |

| 14     | 15    | 16     | 17     | 18      | 19      | 20     | 21     | 22      | 23      | 24     | 25     |
| :----- | :---- | :----- | :----- | :------ | :------ | :----- | :----- | :------ | :------ | :----- | :----- |
| 🟢 34% | 🟢 13% | 🟢 7% | 🟢 71% | 🔴 -13% | 🟢 79% | 🟢 65% | 🟢 52% | 🔴 -47% | 🟢 118% | 🟢 37% | 🟢 21% |

> [!code]- Click to view: leveraged_rebalance.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/leveraged_rebalance.py"
> ```

---

## Strategy-4
### RSI Champion (rsi_champion.py)

**Description:** Sits in cash most of the time, then rushes into a basket of leveraged tech ETFs the moment the market gets extremely oversold. Exits as soon as the signal clears. Patient and decisive — no trend filter, no regime switching, just one clean trigger. ~900 closed trades across 11 years give it strong statistical reliability relative to the rest of the set.

*Overfit 2/10 — single indicator, one threshold; ~900 closed trades give solid statistical confidence; RSI(2) < 20 is a textbook oversold level (alongside the <10 and <30 variants), so there is no parameter-fitting concern.*

- **Entry:** QQQ RSI(2) < 20 → equal-weight TQQQ / SOXL / TECL
- **Exit:** QQQ RSI(2) >= 20 → 100% cash
- **Symbols:** TQQQ, SOXL, TECL (signal from QQQ)

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 47% | -37% | 1.031 | 1426 | 611 | 2.33 | 0.81 |

| 14     | 15    | 16      | 17     | 18     | 19     | 20     | 21      | 22     | 23     | 24     | 25     |
| :----- | :---- | :------ | :----- | :----- | :----- | :----- | :------ | :----- | :----- | :----- | :----- |
| 🟢 30% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 🟢 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 55% |

> [!code]- Click to view: rsi_champion.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/rsi_champion.py"
> ```

---

## Strategy-5
### TQQQ Dynamic Compounding (tqqq_dynamic.py)

**Description:** Owns TQQQ in bull markets but adjusts position size based on momentum — loads up on dips, cuts back at peaks, and exits entirely when the trend turns bear. Tries to compound faster than a static buy-and-hold by being more aggressive when conditions are favorable and more cautious when overextended.

*Overfit 4/10 — RSI thresholds (30, 80) are standard, but the three-tier allocation (20%/50%/100%) and the specific RSI(10) > 80 de-lever trigger look hand-fitted; single-ticker focus keeps the parameter space small.*

- **Entry (Bull, full):** TQQQ > SMA(200) AND RSI(2) < 30 → 100%
- **Entry (Bull, default):** TQQQ > SMA(200), not overbought → 50%
- **De-lever:** TQQQ > SMA(200) AND RSI(10) > 80 → 20%
- **Exit:** TQQQ ≤ SMA(200) → 100% cash
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 31% | -49% | 0.738 | 65 | 57 | 1.14 | 2.69 |

| 14     | 15    | 16      | 17      | 18    | 19     | 20     | 21     | 22      | 23     | 24     | 25     |
| :----- | :---- | :------ | :------ | :---- | :----- | :----- | :----- | :------ | :----- | :----- | :----- |
| 🟢 35% | 🟢 4% | 🔴 -13% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 67% | 🟢 82% | 🔴 -20% | 🟢 70% | 🟢 29% | 🟢 28% |

> [!code]- Click to view: tqqq_dynamic.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/tqqq_dynamic.py"
> ```

---

## Strategy-6
### Expanding Breakout 20d Exit (expanding_breakout.py)

**Description:** Enters TQQQ when today's trading range expands beyond yesterday's in a confirmed uptrend, then closes the position the moment price tags a 20-day high. Taking profit on strength avoids giving back gains on sharp reversals — the trade opens on a momentum burst and closes at the first new short-term milestone. The defining difference from the other breakout variants in this set.

*Overfit 4/10 — 20-day high exit is a standard and defensible rule; fewer parameters than its S35/S36 siblings; only the expanding range trigger is non-standard; the cleanest design in the breakout series.*

- **Gate:** QQQ > SMA(200)
- **Entry:** Expanding Range AND ADX(10) > 25 → 100% TQQQ
- **Exit:** Price >= 20-day high OR 3.0 ATR stop OR QQQ < SMA(200)
- **Symbols:** TQQQ (signal from QQQ)

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 38% | -49% | 0.886 | 94 | 76 | 1.24 | 2.19 |

| 14     | 15     | 16     | 17     | 18     | 19     | 20     | 21     | 22      | 23     | 24     | 25     |
| :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :------ | :----- | :----- | :----- |
| 🟢 137% | 🔴 -3% | 🔴 -2% | 🟢 76% | 🟢 54% | 🟢 14% | 🟢 83% | 🟢 47% | 🔴 -14% | 🟢 72% | 🟢 39% | 🟢 32% |

[Backtest](https://www.quantconnect.com/project/31177892/backtest/42389a9eb4dbd33bfb2df9496328c3af)

> [!code]- Click to view: expanding_breakout.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/expanding_breakout.py"
> ```

---

## Strategy-7
### TQQQ Trend SMA150 (tqqq_sma150.py)

**Description:** An identical structure to the classic SMA200 trend but with the SMA lookback shortened from 200 to 150 days. This faster filter catches trend entries a few weeks earlier and, more importantly, exits during drawdowns sooner — which in 2022 meant preserving more capital for the recovery. The result is a meaningful lift in CAGR (33% to 40%) with essentially unchanged MaxDD (-56% to -55%). The weakness is that a shorter lookback increases whipsaw frequency during range-bound, choppy markets.

*Overfit 2/10 — 150d is a common alternative to 200d, but this is clearly part of a parameter sweep across SMA lengths. The improvement over the 200d variant is marginal enough to question out-of-sample robustness.*

- **Entry:** QQQ price > 150-day SMA → allocate 100% to TQQQ
- **Exit:** QQQ price <= 150-day SMA → liquidate TQQQ to cash
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 40% | -55% | 0.871 | 11 | 17 | 0.65 | 8.14 |

| 14     | 15     | 16     | 17      | 18     | 19     | 20     | 21     | 22      | 23      | 24     | 25     |
| :----- | :----- | :----- | :------ | :----- | :----- | :----- | :----- | :------ | :------ | :----- | :----- |
| 🟢 47% | 🟢 18% | 🔴 -5% | 🟢 118% | 🟢 1%  | 🟢 53% | 🟢 97% | 🟢 88% | 🔴 -34% | 🟢 125% | 🟢 45% | 🟢 27% |

> [!code]- Click to view: tqqq_sma150.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/tqqq_sma150.py"
> ```

---

## Strategy-8
### IBS Extreme + ATR Stop (ibs_atr_stop.py)

**Description:** Enters TQQQ on IBS < 0.1 like the basic IBS strategy, but adds a trailing volatility-based stop loss at 3x the 14-period ATR from the entry price. This stop is designed to cap catastrophic single-trade losses during flash crashes or gap downs. The weakness is that TQQQ's 3x leverage amplifies volatility, making the 3x ATR stop prone to triggering on routine whipsaws rather than true disasters.

*Overfit 3/10 — IBS thresholds and ATR multiplier (3x) are standard choices (Bollinger-style 3-sigma logic). ATR(14) is a canonical period.*

- **Entry:** IBS < 0.1
- **Exit:** IBS > 0.9, OR close < entry_price - 3 × ATR(14)
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 46% | -43% | 1.049 | 137 | 51 | 2.69 | 1.14 |

| 14     | 15     | 16     | 17     | 18      | 19     | 20      | 21     | 22     | 23      | 24     | 25     |
| :----- | :----- | :----- | :----- | :------ | :----- | :------ | :----- | :------ | :----- | :----- | :----- |
| 🟢 7%  | 🟢 6%  | 🟢 39% | 🟢 71% | 🔴 -29% | 🟢 33% | 🟢 344% | 🟢 75% | 🔴 -1%  | 🟢 101% | 🟢 29% | 🟢 82% |

> [!code]- Click to view: ibs_atr_stop.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/ibs_atr_stop.py"
> ```

---

## Strategy-9
### 5 Most Mkt Cap + IBS Regime Mix (mktcap_ibs_regime.py)

**Description:** Switches between two regimes based on QQQ relative to its 200-day SMA. In trend mode (QQQ above SMA200), it holds all five most market capital companies equal-weight. In non-trend mode, it only holds names where IBS is below 0.2, acting as an oversold mean-reversion filter. The regime mix gives it the best MaxDD in the set (-23%) — the IBS filter successfully sidesteps the worst of bear markets.

*Overfit 3/10 — SMA200 is a standard lookback. The IBS<0.2 threshold is the single tuned parameter; it is reasonable but untested against alternatives.*

- **Entry:** Trend mode (QQQ > SMA200): equal weight all 5. No-trend mode: only names with IBS < 0.2, equal-weighted
- **Exit:** When QQQ < SMA200 and a held name no longer has IBS < 0.2, liquidate
- **Symbols:** QQQ (signal), Top 5 US equities by market cap (dynamic universe)

| Pass? | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ | 30% | -23% | 1.073 | 390 | 327 | 1.19 | 2.12 |

| 14     | 15     | 16     | 17     | 18     | 19     | 20     | 21     | 22      | 23     | 24     | 25     |
| :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :------ | :----- | :----- | :----- |
| 🟢 11% | 🟢 5%  | 🟢 4%  | 🟢 38% | 🟢 15% | 🟢 47% | 🟢 95% | 🟢 46% | 🔴 -11% | 🟢 51% | 🟢 38% | 🟢 50% |

> [!code]- Click to view: mktcap_ibs_regime.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/algos/mktcap_ibs_regime.py"
> ```

