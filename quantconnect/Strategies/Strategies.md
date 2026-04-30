# QuantConnect Trading Strategies

| #               | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :-------------- | :--- | :---- | :----- | :--- | :--- | :--- | :--- |
| ✅ [1](#strategy1) | 45%  | -38%  | 1.021 | 234 | 435 | 0.54 | 3.77 |
| ✅ [2](#strategy2) | 31%  | -49%  | 0.883  | 37 | 34 | 1.09 | 3.43 |
| ✅ [3](#strategy3) | 31%  | -52%  | 0.748  | 35 | 0 | ∞ | 0 |
| [4](#strategy4) | 95%  | -57%  | 1.520  | 100 | 85 | 1.18 | 4.51 |
| [5](#strategy5) | 42%  | -48%  | 0.859 | 82  | 123 | 0.67 | 3.68 |
| ✅ [6](#strategy6) | 47%  | -37%  | 1.034 | 1426 | 611 | 2.33 | 0.81 |
| ✅ [7](#strategy7) | 31%  | -49%  | 0.738  | 100 | 47 | 2.13 | 1.44 |
| [8](#strategy8) | 92%  | -47%  | 1.548  | 283 | 232 | 1.22 | 2.56 |
| ✅ [9](#strategy9) | 38% | -54% | 0.818 | 219 | 229 | 0.96 | 1.98 |

| #               | 14         | 15         | 16        | 17         | 18        | 19         | 20          | 21         | 22         | 23          | 24         | 25         |
| :-------------- | :--------- | :--------- | :-------- | :--------- | :-------- | :--------- | :---------- | :--------- | :--------- | :---------- | :--------- | :--------- |
| ✅ [1](#strategy1) | 🟢 53%     | 🟢 6%      | 🟢 21%    | 🟢 88%     | 🟢 19%    | 🟢 111%    | 🟢 169%     | 🟢 42%     | 🔴 -34%    | 🟢 92%      | 🟢 53%     | 🟢 20%     |
| ✅ [2](#strategy2) | 🟢 18%     | ⚪ 0%       | 🟢 5%     | 🟢 37%     | 🟢 6%     | 🟢 50%     | 🟢 62%      | 🟢 55%     | 🔴 -43%    | 🟢 115%     | 🟢 126%    | 🟢 39%     |
| ✅ [3](#strategy3) | 🟢 46%     | 🟢 1%      | 🟢 32%    | 🟢 76%     | 🔴 -15%   | 🟢 107%    | 🟢 51%      | 🟢 65%     | 🔴 -47%    | 🟢 127%     | 🟢 16%     | 🟢 24%     |
| [4](#strategy4) | 🟢 49%     | 🔴 -2%     | 🟢 59%    | 🟢 118%    | 🟢 26%    | 🟢 95%     | 🟢 1020%    | 🟢 88%     | 🟢 77%     | 🟢 142%     | 🟢 62%     | 🟢 68%     |
| [5](#strategy5) | 🟢 42%     | 🟢 6%      | 🔴 -27%   | 🟢 118%    | 🔴 -2%    | 🟢 6%      | 🟢 164%     | 🟢 69%     | 🟢 96%     | 🟢 47%      | 🟢 40%     | 🟢 48%     |
| ✅ [6](#strategy6) | 🟢 31%     | 🔴 -8%     | 🔴 -20%   | 🟢 50%     | 🟢 19%    | 🟢 37%     | 🟢 215%     | 🟢 142%    | 🟢 22%     | 🟢 76%      | 🟢 74%     | 🟢 51%     |
| ✅ [7](#strategy7) | 🟢 35%     | 🟢 4%      | 🔴 -15%   | 🟢 133%    | 🟢 7%     | 🟢 29%     | 🟢 69%      | 🟢 83%     | 🔴 -21%    | 🟢 70%      | 🟢 29%     | 🟢 25%     |
| [8](#strategy8) | 🟢 53%     | 🟢 7%      | 🔴 -6%    | 🟢 113%    | 🟢 17%    | 🟢 91%     | 🟢 604%     | 🟢 88%     | 🟢 139%    | 🟢 224%     | 🟢 62%     | 🟢 107%    |
| ✅ [9](#strategy9) | 🟢 25%     | 🔴 -25%    | 🔴 -28%   | 🟢 99%     | 🟢 5%     | 🟢 11%     | 🟢 225%     | 🟢 82%     | 🟢 119%    | 🟢 30%      | 🟢 41%     | 🟢 25%     |
| ✅ **AVG**     | **🟢 35%** | **🔴 -3%** | **🔴 -1%** | **🟢 81%** | **🟢 7%** | **🟢 58%** | **🟢 132%** | **🟢 78%** | **🔴 -1%** | **🟢 85%** | **🟢 57%** | **🟢 31%** |


---

## Strategy1
### Volatility Breakout (vol_breakout.py)

**Description:** Waits for TQQQ to quietly compress near a recent high, then enters expecting a breakout. Gets out as soon as volatility spikes or the stop is hit. Operates on minute bars, so it is trying to exploit intraday momentum patterns rather than daily trends.

**Overfitting Risk:** 6/10 (Medium) — 6 optimizer-tuned parameters; custom non-standard indicator; performance depends on the specific volatility regime of the 2014–2025 period.

- **Entry:** Price >= 98% of 240-min high AND avg intra-bar volatility < 0.1
- **Exit:** Avg intra-bar volatility > 0.15 OR 3% stop loss
- **Symbols:** TQQQ
- **Resolution:** Minute

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 45% | -38% | 1.021 | 234 | 435 | 0.54 | 3.77 |

| 14     | 15    | 16     | 17     | 18     | 19      | 20      | 21     | 22      | 23     | 24     | 25     |
| :----- | :---- | :----- | :----- | :----- | :------ | :------ | :----- | :------ | :----- | :----- | :----- |
| 🟢 53% | 🟢 6% | 🟢 21% | 🟢 88% | 🟢 19% | 🟢 111% | 🟢 169% | 🟢 42% | 🔴 -34% | 🟢 92% | 🟢 53% | 🟢 20% |

> [!code]- Click to view: vol_breakout.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/vol_breakout.py"
> ```

---

## Strategy2
### Tech Dip Buy (dip_buy_tech.py)

**Description:** Buys the biggest tech names when they pull back hard during an uptrend, then holds until they recover to new highs or the loss gets too large. Universe rotates automatically as market caps shift, so it always targets the current leaders.

**Overfitting Risk:** 2/10 (Very Low) — textbook parameters, dynamic universe, small trade count (71 total) is a minor concern but the logic is sound.

- **Entry:** RSI(2) < 30 AND price > SMA(50); equal weight across held positions
- **Exit:** Price <= avg cost × 0.85 (15% hard stop) OR price >= 252-day high (1-yr ATH)
- **Symbols:** Dynamic top 5 tech by market cap (e.g. AAPL, MSFT, NVDA, AVGO, ORCL)
- **Rebalance:** Weekly

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

**Description:** Holds three leveraged ETFs and cash in fixed proportions, restoring those proportions once a year. No signals, no timing decisions. Returns come almost entirely from what it holds rather than how it manages positions — TQQQ, SOXL, and TECL were among the best-performing ETFs of the backtest decade, which is a hindsight advantage.

**Overfitting Risk:** 4/10 (Low-Medium) — zero mechanical overfitting, but symbol selection is a meta-level hindsight bias that cannot be discovered without knowing the outcome.

- **Entry:** Annual rebalance to target weights
- **Exit:** N/A — weight drift only corrected annually
- **Symbols:** TQQQ 20%, SOXL 20%, TECL 20%, Cash 40%
- **Rebalance:** Yearly

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -52% | 0.748 | 35 | 0 | ∞ | 0 |

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

**Description:** Always either long or short — never in cash. Rides TQQQ in bull markets and flips to SQQQ during sustained downtrends, but stays long during sharp crashes rather than shorting into panic. Aggressive on both sides of the market. The 1020% return in 2020 is a red flag suggesting the logic was calibrated to the specific shape of the COVID crash and recovery.

**Overfitting Risk:** 7/10 (High) — RSI(10) crash gate on 4 tickers is highly specific; the 2020 outlier return (1020%) strongly suggests the logic was tuned to that event; never holding cash is an aggressive structural choice.

- **Entry:** Default TQQQ; rotate to SQQQ when SPY < SMA(200) AND TQQQ < SMA(20) AND no crash
- **Exit:** Rotate back to TQQQ when trend or crash conditions clear
- **Crash Gate:** RSI(10) on QQQ or SPY < 30 → stay long TQQQ (prevents shorting sharp drops)
- **Symbols:** TQQQ, SQQQ, SPY, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 95%  | -57%  | 1.520  | 100 | 85 | 1.18 | 4.51 |

| 14     | 15     | 16     | 17      | 18     | 19     | 20       | 21     | 22     | 23      | 24     | 25     |
| :----- | :----- | :----- | :------ | :----- | :----- | :------- | :----- | :----- | :------ | :----- | :----- |
| 🟢 49% | 🔴 -2% | 🟢 59% | 🟢 118% | 🟢 26% | 🟢 95% | 🟢 1020% | 🟢 88% | 🟢 77% | 🟢 142% | 🟢 62% | 🟢 68% |

> [!code]- Click to view: conservative_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/conservative_rotation.py"
> ```

---

## Strategy5
### Defensive Rotation (defensive_rotation.py)

**Description:** Rotates between TQQQ, SQQQ, and cash depending on the trend and momentum regime. More conservative than S4 — defaults to cash when conditions are ambiguous rather than forcing a position. Note: the original description did not match the actual code, meaning the logic was changed without a clean rewrite. A duplicate initialization block in the code further indicates this strategy was tuned in place over time.

**Overfitting Risk:** 6/10 (Medium) — duplicate init block reveals iterative tuning; RSI(10) crash gate on two indices is a specific multi-ticker filter; code-to-docstring mismatch means the logic was changed without a clean rewrite.

- **Entry (Bull):** TQQQ > SMA(200) AND (price > SMA(20) OR RSI(2) < 20) → TQQQ
- **Entry (Bear):** TQQQ ≤ SMA(200) AND (price < SMA(20) OR RSI(2) > 80) → SQQQ
- **Cash Gate:** RSI(10) on QQQ or SPY < 30 → cash regardless of regime
- **Default:** Cash
- **Symbols:** TQQQ, SQQQ, SPY, QQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 42% | -48% | 0.859 | 82 | 123 | 0.67 | 3.68 |

| 14     | 15    | 16      | 17      | 18     | 19    | 20      | 21     | 22     | 23     | 24     | 25     |
| :----- | :---- | :------ | :------ | :----- | :---- | :------ | :----- | :----- | :----- | :----- | :----- |
| 🟢 42% | 🟢 6% | 🔴 -27% | 🟢 118% | 🔴 -2% | 🟢 6% | 🟢 164% | 🟢 69% | 🟢 96% | 🟢 47% | 🟢 40% | 🟢 48% |

> [!code]- Click to view: defensive_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/defensive_rotation.py"
> ```

---

## Strategy6
### RSI Champion (rsi_champion.py)

**Description:** Sits in cash most of the time, then rushes into a basket of leveraged tech ETFs the moment the market gets extremely oversold. Exits as soon as the signal clears. Patient and decisive — no trend filter, no regime switching, just one clean trigger. With over 2000 trades across 11 years it is the most statistically reliable strategy in the set.

**Overfitting Risk:** 2/10 (Very Low) — single indicator, single threshold; 2000+ trades provide strong statistical confidence; the only minor concern is the 25 threshold vs the more standard 20 or 30.

- **Entry:** QQQ RSI(2) < 25 → equal-weight TQQQ / SOXL / TECL
- **Exit:** QQQ RSI(2) >= 25 → 100% cash
- **Symbols:** TQQQ, SOXL, TECL (signal from QQQ)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 47% | -37% | 1.034 | 1426 | 611 | 2.33 | 0.81 |

| 14     | 15     | 16      | 17     | 18     | 19     | 20      | 21      | 22     | 23     | 24     | 25     |
| :----- | :----- | :------ | :----- | :----- | :----- | :------ | :------ | :----- | :----- | :----- | :----- |
| 🟢 31% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 🟢 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 51% |

> [!code]- Click to view: rsi_champion.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/rsi_champion.py"
> ```

---

## Strategy7
### TQQQ Dynamic Compounding (dip_buy_tqqq.py)

**Description:** Owns TQQQ in bull markets but adjusts position size based on momentum — loads up on dips, cuts back at peaks, and exits entirely when the trend turns bear. Tries to compound faster than a static buy-and-hold by being more aggressive when conditions are favorable and more cautious when overextended.

**Overfitting Risk:** 4/10 (Low-Medium) — RSI thresholds (30, 80) are standard; the three allocation tiers (20%/50%/100%) and their trigger conditions are likely tuned; single-ticker focus limits parameter space.

- **Entry (Bull, full):** TQQQ > SMA(200) AND RSI(2) < 30 → 100%
- **Entry (Bull, default):** TQQQ > SMA(200), not overbought → 50%
- **De-lever:** TQQQ > SMA(200) AND RSI(10) > 80 → 20%
- **Exit:** TQQQ ≤ SMA(200) → 100% cash
- **Symbols:** TQQQ

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

**Description:** Tries to profit in both bull and bear markets by rotating across five assets depending on which regime is active. The result of 18 rounds of iterative refinement on top of a prior strategy. The complexity is a liability — some of the logic (particularly the BIL comparison in bear markets) has no clear economic rationale and appears to be an artifact of repeated backtesting rather than a genuine market insight.

**Overfitting Risk:** 9/10 (Very High) — 18 iterations of in-sample refinement; RSI(BIL) comparison is economically meaningless; thresholds 79/31/30 indicate single-point optimizer tuning; 604% return in 2020 suggests calibration to the COVID event.

- **Entry (Bull):** TQQQ > SMA(200) AND RSI(10) ≤ 79 → TQQQ
- **Cash (Bull overbought):** RSI(10,TQQQ) > 79 → BIL
- **Bear dip-buy:** RSI(10,TQQQ) < 31 → TECL; RSI(10,SOXL) < 30 → SOXL
- **Bear downtrend:** TQQQ < SMA(20) → SQQQ if RSI(SQQQ) > RSI(BIL), else BIL
- **Bear rally:** TQQQ ≥ SMA(20) → TQQQ
- **Symbols:** TQQQ, TECL, SOXL, SQQQ, BIL

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

---

## Strategy9
### Dual Signal Rotation (dual_signal_rotation.py)

**Description:** Goes long in uptrends, short in downtrends, and hides in cash when neither signal is clear. The cleanest rotation strategy in the set — the bull and bear logic are mirror images of each other, all signals come from a single ticker, and every threshold is a round-number standard value. What you see is what you get.

**Overfitting Risk:** 3/10 (Low) — 3 indicators on one ticker, symmetric logic, standard thresholds; the -54% max drawdown is steep but consistent with the strategy's exposure to leveraged ETFs.

- **Entry (Bull):** TQQQ > SMA(200) AND (price > SMA(20) OR RSI(2) < 20) → TQQQ
- **Entry (Bear):** TQQQ ≤ SMA(200) AND (price < SMA(20) OR RSI(2) > 80) → SQQQ
- **Default:** Cash
- **Symbols:** TQQQ, SQQQ

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -54% | 0.818 | 219 | 229 | 0.96 | 1.98 |

| 14     | 15      | 16      | 17     | 18    | 19     | 20      | 21     | 22      | 23     | 24     | 25     |
| :----- | :------ | :------ | :----- | :---- | :----- | :------ | :----- | :------ | :----- | :----- | :----- |
| 🟢 25% | 🔴 -25% | 🔴 -28% | 🟢 99% | 🟢 5% | 🟢 11% | 🟢 225% | 🟢 82% | 🟢 119% | 🟢 30% | 🟢 41% | 🟢 25% |

> [!code]- Click to view: dual_signal_rotation.py
> ```embed-python
> PATH: "vault://QuantConnect/strategies/dual_signal_rotation.py"
> ```
