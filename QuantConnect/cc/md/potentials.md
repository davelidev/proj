# potentials

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [1](#strategy-1)     | ✅    | Dip Buy         | 32%  | -50%  | 0.772  | 57    | 24    | 2.38     | 1.45         | 3/10   |
| [2](#strategy-2)     | ❌    | Mean Reversion  | 27%  | -44%  | 0.835  | 452   | 254   | 1.78     | 1.22         | 2/10   |
| [3](#strategy-3)     | ✅    | Rotation        | 38%  | -54%  | 0.818  | 220   | 228   | 0.96     | 1.98         | 6/10   |
| [4](#strategy-4)     | ✅    | Mean Reversion  | 39%  | -55%  | 0.917  | 237   | 92    | 2.58     | 0.98         | 4/10   |
| [7](#strategy-7)     | ✅    | Dip Buy         | 30%  | -39%  | 0.864  | 54    | 10    | 5.40     | 5.11         | 4/10   |
| [8](#strategy-8)     | ❌    | Rotation        | 27%  | -43%  | 0.709  | 219   | 166   | 1.32     | 2.50         | 4/10   |
| [10](#strategy-10)   | ✅    | Trend/MR Hybrid | 49%  | -48%  | 0.991  | 71    | 58    | 1.22     | 4.32         | 5/10   |
| [11](#strategy-11)   | ✅    | Trend/MR Hybrid | 30%  | -23%  | 1.073  | 827   | 650   | 1.27     | 2.06         | 3/10   |
| [12](#strategy-12)   | ✅    | Rotation        | 29%  | -48%  | 0.7    | 69    | 66    | 1.05     | 3.15         | 5/10   |
| [14](#strategy-14)   | ✅    | Trend           | 38%  | -49%  | 0.885  | 309   | 252   | 1.23     | 2.65         | 3/10   |
| [17](#strategy-17)   | ✅    | Trend           | 33%  | -44%  | 0.81   | 294   | 231   | 1.27     | 2.47         | 3/10   |
| [18](#strategy-18)   | ✅    | Trend           | 31%  | -40%  | 0.806  | 204   | 249   | 0.82     | 3.01         | 3/10   |
| [19](#strategy-19)   | ✅    | Trend           | 32%  | -43%  | 0.846  | 386   | 492   | 0.78     | 3.88         | 3/10   |
| [20](#strategy-20)   | ✅    | Regime          | 39%  | -46%  | 0.892  | 290   | 247   | 1.17     | 2.06         | 4/10   |
| [21](#strategy-21)   | ✅    | Trend           | 31%  | -43%  | 0.794  | 193   | 256   | 0.75     | 3.27         | 3/10   |
| [22](#strategy-22)   | ✅    | Momentum        | 35%  | -50%  | 0.843  | 218   | 267   | 0.82     | 3.13         | 3/10   |
| [23](#strategy-23)   | ✅    | Momentum        | 37%  | -49%  | 0.87   | 312   | 255   | 1.22     | 2.56         | 4/10   |
| [24](#strategy-24)   | ✅    | Momentum        | 38%  | -50%  | 0.886  | 292   | 239   | 1.22     | 2.67         | 3/10   |
| [26](#strategy-26)   | ✅    | Hybrid          | 31%  | -44%  | 0.754  | 914   | 661   | 1.38     | 1.48         | 4/10   |
| [27](#strategy-27)   | ✅    | Hybrid          | 33%  | -45%  | 0.802  | 850   | 615   | 1.38     | 1.57         | 4/10   |
| [28](#strategy-28)   | ✅    | Hybrid          | 31%  | -50%  | 0.752  | 1055  | 733   | 1.44     | 1.39         | 4/10   |
| [29](#strategy-29)   | ✅    | Momentum        | 35%  | -50%  | 0.843  | 218   | 267   | 0.82     | 3.13         | 2/10   |
| [30](#strategy-30)   | ✅    | Hybrid          | 31%  | -29%  | 0.831  | 744   | 745   | 1.00     | 2.10         | 4/10   |
| [31](#strategy-31)   | ✅    | Hybrid          | 31%  | -33%  | 0.864  | 817   | 642   | 1.27     | 1.73         | 4/10   |
| [33](#strategy-33)   | ✅    | Hybrid          | 29%  | -42%  | 0.772  | 238   | 303   | 0.79     | 3.03         | 4/10   |
| [35](#strategy-35)   | ✅    | Price Position  | 30%  | -55%  | 0.697  | 40    | 65    | 0.62     | 8.15         | 1/10   |
| [36](#strategy-36)   | ✅    | Breadth         | 33%  | -53%  | 0.803  | 209   | 246   | 0.85     | 2.96         | 2/10   |
| [37](#strategy-37)   | ✅    | Price Position  | 35%  | -54%  | 0.785  | 70    | 83    | 0.84     | 4.80         | 2/10   |
| [38](#strategy-38)   | ✅    | Breadth         | 33%  | -53%  | 0.803  | 209   | 246   | 0.85     | 2.96         | 2/10   |
| [39](#strategy-39)   | ✅    | TII             | 30%  | -44%  | 0.711  | 545   | 446   | 1.22     | 1.44         | 2/10   |
| [41](#strategy-41)   | ✅    | Breakout        | 43%  | -37%  | 0.986  | 192   | 341   | 0.56     | 3.45         | 3/10   |
| [42](#strategy-42)   | ❌    | Dip Buy         | 28%  | -40%  | 0.856  | 32    | 26    | 1.23     | 3.20         | 2/10   |
| [43](#strategy-43)   | ❌    | Momentum        | 27%  | -26%  | 0.981  | 3552  | 888   | 4.00     | 0.59         | 2/10   |
| [49](#strategy-49)   | ✅    | Momentum        | 33%  | -40%  | 0.837  | 194   | 247   | 0.79     | 3.46         | 2/10   |


---
## Strategy-1
### Research S11 - Cheat Code Rotator TQQQ (001.py)

**Description:** Kevin Davey's 'cheat code' formula: enter a leveraged Nasdaq ETF on dips when both the long-term trend and short-term volatility are favorable. Three gates must hold simultaneously — QQQ above its 200-day SMA, VIX below 28, and QQQ RSI(2) below 30. Exits on either short-term overbought readings, a trend break, or a VIX spike above 32.

*Overfit 3/10 — Four indicators, all at conventional thresholds (SMA200, RSI<30/>80, VIX 28/32 — within the standard 25-35 'fear' band). The 28/32 asymmetry between entry-shield and exit-panic is a tuned magic-number pair, but the underlying logic is mainstream technical analysis.*

- **Trend gate:** QQQ > SMA(200)
- **Volatility shield:** VIX < 28
- **Entry:** QQQ RSI(2) < 30 (with both gates passing) → 100% TQQQ
- **Exit:** QQQ RSI(10) > 80 OR QQQ < SMA(200) OR VIX > 32
- **Symbols:** TQQQ (execution); QQQ, VIX (signals)
- **Rebalance:** Daily, 35 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -50% | 0.772 | 57 | 24 | 2.38 | 1.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 68% | 🟢 8% | 🔴 -25% | 🟢 137% | 🔴 -16% | 🟢 20% | 🟢 69% | 🟢 61% | 🔴 -27% | 🟢 104% | 🟢 64% | 🟢 32% |

> [!code]- Click to view: 001.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/001.py"
> ```


---

## Strategy-2
### Giant Sniper Mean-Reversion (002.py)

**Description:** Same shape as Strategy 11 — top-5 mega-caps + RSI(2) dip entry — but with two structural differences. (1) Universe is the top 5 by market cap *across all sectors*, not tech-only, so the basket can include non-tech leaders. (2) Has an explicit bear-market shield: when QQQ falls below its 200-day SMA, the strategy liquidates everything regardless of individual-name signals. Exits are per-name on RSI(2) > 70 instead of price highs.

*Overfit 2/10 — Two textbook indicators (RSI(2) and SMA(200)) with standard thresholds (<20 / >70 / 200d). Dynamic top-5 universe removes name-selection bias. The bear-market shield is the only added complexity and uses the canonical 200d cutoff. A clean, replicable design.*

- **Universe:** Top 5 US stocks by market cap (all sectors, dynamic)
- **Trend shield:** QQQ > SMA(200) required to hold anything
- **Entry:** Bull regime + per-name RSI(2) < 20 → buy at equal weight
- **Exit:** Per-name RSI(2) > 70; OR QQQ < SMA(200) → liquidate all
- **Rebalance:** Daily, 30 min after market open
- **Symbols:** Dynamic — typically AAPL/MSFT/NVDA/GOOG/AMZN etc.

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27% | -44% | 0.835 | 452 | 254 | 1.78 | 1.22 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 15% | 🟢 49% | 🔴 -13% | 🟢 48% | 🔴 -16% | 🟢 7% | 🟢 34% | 🟢 80% | 🔴 -10% | 🟢 43% | 🟢 40% | 🟢 94% |

> [!code]- Click to view: 002.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/002.py"
> ```


---

## Strategy-3
### Defensive Rotation (003.py)

**Description:** A four-state regime rotation. The state machine: (1) any RSI(10) crash signal → all cash; (2) bull market (TQQQ > SMA200) + uptrend or short-term dip → TQQQ; (3) bear market (TQQQ ≤ SMA200) + downtrend or overbought bounce → SQQQ; (4) anything else → all cash. The crash gate at the top sidesteps the dangerous mid-crash zones where mean-reversion entries blow up.

*Overfit 6/10 — Five tuned thresholds: SMA200, SMA20, RSI(2) at 20/80, RSI(10) at 30. The state-machine is clean conceptually but each branch's cutoff is hand-picked. Source file has duplicate Initialize blocks (indicators registered twice) suggesting copy-paste from another file — minor code smell that hints at hasty iteration.*

- **Crash gate:** RSI(QQQ,10) < 30 OR RSI(SPY,10) < 30 → all cash (no other rules evaluated)
- **Bull entry:** TQQQ > SMA(200) AND (TQQQ > SMA(20) OR RSI(TQQQ,2) < 20) → 100% TQQQ
- **Bear entry:** TQQQ ≤ SMA(200) AND (TQQQ < SMA(20) OR RSI(TQQQ,2) > 80) → 100% SQQQ
- **Else:** All cash
- **Symbols:** TQQQ, SQQQ (executions); SPY, QQQ (signals)
- **Rebalance:** Daily, 35 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -54% | 0.818 | 220 | 228 | 0.96 | 1.98 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 25% | 🔴 -25% | 🔴 -28% | 🟢 99% | 🟢 5% | 🟢 11% | 🟢 225% | 🟢 82% | 🟢 119% | 🟢 30% | 🟢 41% | 🟢 25% |

> [!code]- Click to view: 003.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/003.py"
> ```


---

## Strategy-4
### IBS regime-adaptive (004.py)

**Description:** Regime-adaptive IBS strategy. Standard IBS < 0.1 entry in uptrends (QQQ > 200d SMA), but tightens to IBS < 0.03 in downtrends — only buying extreme panic closes when the broader market is bearish. Exit is unchanged at IBS > 0.9 regardless of regime.

*Overfit 4/10 — Regime-adaptive design is conceptually sound, but the 0.03 downtrend threshold is extreme — implies essentially never entering in bear markets except on capitulation days. Such a rare threshold can only be back-fit to specific days that existed in the backtest decade.*

- **Trend gate:** QQQ > SMA(200) → 'uptrend' regime; else → 'downtrend' regime
- **Entry (uptrend):** IBS < 0.1 → 100% TQQQ
- **Entry (downtrend):** IBS < 0.03 → 100% TQQQ (very rare)
- **Exit:** IBS > 0.9 → liquidate
- **Symbols:** TQQQ (execution); QQQ (signal)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -55% | 0.917 | 237 | 92 | 2.58 | 0.98 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 12% | 🟢 1% | 🟢 26% | 🟢 71% | 🔴 -31% | 🟢 35% | 🟢 303% | 🟢 75% | 🔴 -23% | 🟢 84% | 🟢 17% | 🟢 92% |

> [!code]- Click to view: 004.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/004.py"
> ```


---

## Strategy-7
### Mega-Cap Value Averaging (007.py)

**Description:** Universe-driven dip-buy on the five largest-cap U.S. stocks (selected from the top 100 by dollar volume, then ranked by market cap each universe refresh). Whenever a name pulls back more than 5% from its 20-day high it gets a 20% portfolio allocation, and the position is liquidated the moment price prints a new 20-day high. The construction sidesteps single-stock bets by spreading 100% nominal exposure across five mega-caps, and only sells into strength — never on weakness — so a position can sit in drawdown indefinitely until a fresh high releases it.

*Overfit 4/10 — Two tuned numbers (5% dip threshold, 20-day high lookback) and a hindsight-driven universe — 'top 5 by market cap' over 2014–2025 maps directly onto the mega-cap tech complex (AAPL/MSFT/AMZN/GOOGL/META/NVDA), which is the regime the backtest favors. The rule itself (buy weakness in an uptrend, exit on new highs) is a standard value-averaging template; no exotic indicators or per-asset tuning.*

- **Universe:** Top 100 stocks by dollar volume → top 5 by market cap (daily refresh)
- **Entry:** Price < 20-day high × 0.95 → buy 20% allocation
- **Exit:** Price ≥ 20-day high → liquidate
- **Sizing:** Fixed 20% per name (5 names → 100% gross when fully loaded)
- **Resolution:** Daily bars

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -39% | 0.864 | 54 | 10 | 5.40 | 5.11 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 22% | 🟢 16% | 🟢 14% | 🟢 49% | 🔴 -4% | 🟢 61% | 🟢 57% | 🟢 50% | 🔴 -34% | 🟢 76% | 🟢 75% | 🟢 28% |

> [!code]- Click to view: 007.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/007.py"
> ```


---

## Strategy-8
### 5x 3x-Leveraged ETF Basket + QQQ Vol Gate (008.py)

**Description:** Equal-weight basket of 5 3x-leveraged ETFs (TQQQ, TECL, SOXL, UPRO, FAS), held only when QQQ's 20-day annualized log-return volatility is below 20%. Tight vol gate — flips entirely in or entirely out based on a single threshold check daily. Re-enters as soon as vol returns under threshold.

*Overfit 4/10 — Two tuned parameters — the 20-day vol lookback and the 20% threshold — applied to a fixed 5-name basket. The threshold is round-numbered but a tight binary gate on a single vol number is exactly the kind of cliff-edge rule that fits a specific regime; in the 2020 vol spike a 20% threshold would have caused multiple whipsaws.*

- **Universe:** Fixed 5-name 3x-leveraged basket: TQQQ, TECL, SOXL, UPRO, FAS
- **Vol gate:** QQQ 20d annualized log-return vol < 20% → in market; else → cash
- **Allocation:** Equal weight (20% per name) when in market
- **Entry:** Vol gate flips on → set all 5 names to 20%
- **Exit:** Vol gate flips off → liquidate entire portfolio
- **Rebalance:** Daily, 30 min after market open (checks gate only)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27% | -43% | 0.709 | 219 | 166 | 1.32 | 2.50 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 28% | 🔴 -1% | 🟢 21% | 🟢 106% | 🔴 -7% | 🟢 59% | 🟢 7% | 🟢 49% | 🟢 5% | 🟢 62% | 🟢 44% | ⚪ 0% |

> [!code]- Click to view: 008.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/008.py"
> ```


---

## Strategy-10
### TQQQ hybrid + ATR (010.py)

**Description:** TQQQ self-SMA(200) trend + IBS<0.05 dip-buy hybrid with an added 3× ATR stop-loss on the MR sleeve. Same shape as Strategy 47 but with risk management on the bear-market dips — if the dip extends another 3× ATR below the entry, the trade is cut.

*Overfit 5/10 — Strategy 47 + an ATR stop on MR positions. Four tuned parameters total (SMA200, IBS 0.05/0.7, ATR 3×). The TQQQ self-SMA introduces noise (Strategy 25 concern); the IBS<0.05 is rare-trigger fitting (Strategy 34 concern); the ATR stop is canonical (Strategy 33 concern). Inherits every concern from its parents.*

- **Trend gate:** TQQQ > SMA(200) of TQQQ → 'trend' mode; else → 'MR' mode
- **Entry (trend):** Trend mode active AND not invested → 100% TQQQ
- **Entry (MR):** MR mode active AND IBS < 0.05 → 100% TQQQ; entry price recorded
- **Exit (trend):** Trend flips off → liquidate
- **Exit (MR signal):** MR position held AND IBS > 0.7 → liquidate
- **Stop-loss (MR only):** MR position close < entry - 3.0 × ATR(14) → liquidate
- **Symbols:** TQQQ (signal and execution)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 49% | -48% | 0.991 | 71 | 58 | 1.22 | 4.32 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 52% | 🟢 9% | 🔴 -2% | 🟢 118% | 🔴 -1% | 🟢 36% | 🟢 259% | 🟢 88% | 🔴 -11% | 🟢 75% | 🟢 59% | 🟢 48% |

> [!code]- Click to view: 010.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/010.py"
> ```


---

## Strategy-11
### 5 most mkt cap + IBS regime mix (011.py)

**Description:** Two-regime rotation on the top 5 US stocks by market cap. **Uptrend** (QQQ > 200d SMA): hold all 5 mega-caps equal-weight (20% each). **Downtrend** (QQQ ≤ 200d SMA): rotate into only those names whose IBS < 0.2 (close near day's low — buying weakness in mega-caps only when the broader market is bearish). Position weights adjust daily based on how many names meet the bear-mode filter.

*Overfit 3/10 — Dynamic universe removes name-selection bias. SMA(200) and IBS<0.2 are both canonical thresholds. The 5% rebalance drift tolerance is a minor magic number but isn't outcome-shaping. One of the cleanest hybrid designs — mirrors Strategies.md Strategy-9 (active production version) at the same rating.*

- **Universe:** Top 5 US stocks by market cap (all sectors, dynamic)
- **Trend gate:** QQQ > SMA(200) → 'trend' mode; else → 'MR' mode
- **Allocation (trend):** Equal weight all 5 names (20% each); rebalance only when drift > 5%
- **Allocation (MR):** Equal weight names with IBS < 0.2 (variable subset, 0-5 names)
- **Exit:** Per-name: liquidated when no longer in target set (universe change or filter exit)
- **Symbols:** Dynamic — typically AAPL/MSFT/NVDA/GOOG/AMZN etc.; QQQ for signal
- **Rebalance:** Daily at 10:30 ET

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -23% | 1.073 | 827 | 650 | 1.27 | 2.06 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 11% | 🟢 5% | 🟢 4% | 🟢 38% | 🟢 15% | 🟢 47% | 🟢 95% | 🟢 46% | 🔴 -11% | 🟢 51% | 🟢 38% | 🟢 50% |

> [!code]- Click to view: 011.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/011.py"
> ```


---

## Strategy-12
### Nasdaq-100 Breadth Rotation (012.py)

**Description:** Uses participation across the 10 largest-cap U.S. stocks (drawn from the top 100 by dollar volume) as a breadth regime gate for TQQQ. Each constituent runs a 50-day EMA, and the strategy measures the fraction trading above its EMA: above 60% it goes 100% long TQQQ, below 40% it liquidates, and in the 40–60% no-man's-land it holds whatever it had. The mega-cap basket acts as a proxy for Nasdaq leadership health — when participation is broad the engine ramps full 3× exposure, and when it deteriorates it steps fully aside.

*Overfit 5/10 — Three tuned thresholds (50-day EMA period, 60% bull cutoff, 40% bear cutoff) and a regime-defining universe choice. The 60/40 asymmetric hysteresis is a reasonable design choice (prevents whipsaws around 50%) but the specific levels are unverified. The 'top 10 by market cap' basket suffers the same hindsight asset-selection bias as #14 — over 2014–2025 it locks in the mega-cap tech leadership that the strategy then leverages 3× into.*

- **Universe:** Top 100 stocks by dollar volume → top 10 by market cap (signal basket)
- **Indicator:** 50-day EMA per constituent; breadth = fraction trading above EMA
- **Bull entry:** Breadth > 60% → 100% TQQQ
- **Bear exit:** Breadth < 40% → liquidate TQQQ
- **Symbols:** Signal: top-10 mega-cap basket. Execution: TQQQ
- **Resolution:** Daily bars

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -48% | 0.7 | 69 | 66 | 1.05 | 3.15 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 11% | 🟢 2% | 🔴 -7% | 🟢 118% | 🔴 -29% | 🟢 33% | 🟢 108% | 🟢 53% | 🔴 -34% | 🟢 73% | 🟢 46% | 🟢 95% |

> [!code]- Click to view: 012.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/012.py"
> ```


---

## Strategy-14
### 3-State ROC(20) + Donchian-200 (014.py)

**Description:** A three-state trend follower that replaces the Aroon oscillator with a 20-day rate-of-change indicator on QQQ alongside the standard Donchian-200 midline. When both momentum and the channel position are bullish it holds TQQQ fully; partial confirmation yields a 50/50 blend; both bearish yields full cash.

*Overfit 3/10 — ROC(20)>0 is a canonical momentum threshold. Donchian-200 midline is standard. Two-indicator, textbook-level design.*

- **Trend gate:** ROC(20)>0 on QQQ; QQQ price > Donchian-200 midline
- **Entry:** Both bull → 100% TQQQ; one bull → 50% TQQQ/50% BIL; both bear → 100% BIL
- **Exit:** Rebalance on state change
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -49% | 0.885 | 309 | 252 | 1.23 | 2.65 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | 🟢 6% | ⚪ 0% | 🟢 101% | 🔴 -12% | 🟢 84% | 🟢 138% | 🟢 62% | 🔴 -32% | 🟢 92% | 🟢 44% | 🟢 33% |

> [!code]- Click to view: 014.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/014.py"
> ```


---

## Strategy-17
### 3-State Dual-ROC + D200 (017.py)

**Description:** A three-state trend follower that requires consensus from both short-term ROC(20) and medium-term ROC(60) for the momentum leg, paired with a Donchian-200 midline. The dual-ROC requirement means both timeframes must agree for the strategy to treat momentum as bullish, reducing false positives.

*Overfit 3/10 — ROC(20)>0 AND ROC(60)>0 as a consensus gate are both standard zero-crossing tests. Donchian-200 midline is standard. Two standard components with a straightforward AND logic.*

- **Trend gate:** ROC(20)>0 AND ROC(60)>0 on QQQ (dual-timeframe consensus); QQQ > Donchian-200 midline
- **Entry:** Both filters bull → 100% TQQQ; one bull → 50% TQQQ/50% BIL; both bear → 100% BIL
- **Exit:** Rebalance on state change
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -44% | 0.81 | 294 | 231 | 1.27 | 2.47 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 32% | 🟢 1% | 🔴 -3% | 🟢 101% | 🔴 -8% | 🟢 82% | 🟢 96% | 🟢 62% | 🔴 -33% | 🟢 99% | 🟢 38% | 🟢 17% |

> [!code]- Click to view: 017.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/017.py"
> ```


---

## Strategy-18
### ROC+D200 + 5% Trail Exit (018.py)

**Description:** A trend follower identical in structure to the 7%-trail variant but using a tighter 5% trailing drawdown from the 20-day high as the exit trigger. The tighter stop provides faster downside protection at the cost of more frequent exits during normal pullbacks.

*Overfit 3/10 — Standard ROC(20)>0 and Donchian-200 entry. The 5% trailing drawdown threshold from 20-day high is a tighter, non-canonical tuned value.*

- **Trend gate:** ROC(20)>0 on QQQ AND QQQ > Donchian-200 midline
- **Entry:** Both conditions true AND QQQ within 5% of 20-day high → 100% TQQQ
- **Exit:** Trend signal off OR QQQ drops >5% below 20-day high → 100% BIL
- **Stop-loss:** Trailing: exit if QQQ falls >5% from its 20-day high
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -40% | 0.806 | 204 | 249 | 0.82 | 3.01 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -14% | 🔴 -2% | 🟢 85% | 🔴 -15% | 🟢 66% | 🟢 188% | 🟢 39% | 🔴 -19% | 🟢 64% | 🟢 23% | 🟢 42% |

> [!code]- Click to view: 018.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/018.py"
> ```


---

## Strategy-19
### TQQQ Pyramid 30%/day (019.py)

**Description:** The fastest pyramiding variant, adding 30% TQQQ exposure per day while trend conditions hold, reaching full exposure in roughly four consecutive bull days. A single bear day triggers a complete exit to cash. The same ROC(20) and Donchian-200 trend conditions govern entry and exit.

*Overfit 3/10 — The 30% daily step rate (approximately 4 days to full exposure) is non-canonical. Entry conditions (ROC(20)>0 and Donchian-200) are standard. One non-canonical tuned parameter on top of standard signals.*

- **Trend gate:** ROC(20)>0 on QQQ AND QQQ > Donchian-200 midline
- **Entry:** Bull: +30% TQQQ per day (up to 100%); remainder in BIL
- **Exit:** Bear signal → TQQQ to 0%, 100% BIL immediately
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -43% | 0.846 | 386 | 492 | 0.78 | 3.88 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 28% | 🔴 -7% | 🟢 2% | 🟢 70% | 🔴 -4% | 🟢 70% | 🟢 128% | 🟢 41% | 🔴 -16% | 🟢 50% | 🟢 44% | 🟢 43% |

> [!code]- Click to view: 019.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/019.py"
> ```


---

## Strategy-20
### Mega-Cap Dispersion Regime (020.py)

**Description:** A breadth-based trend follower that adds a cohesion filter to the standard D200 regime: it only holds TQQQ when both QQQ is in an uptrend and the five largest US stocks are moving together, as measured by the standard deviation of their 20-day returns being below a threshold. High dispersion among mega-caps signals stress and triggers a shift to cash.

*Overfit 4/10 — Three parameters: D200 midpoint regime, the top-5 market-cap universe, and a 5% cross-sectional standard deviation threshold on 20-day returns. The 5% dispersion cutoff is a specific tuned value.*

- **Trend gate:** QQQ price > midpoint of 200-day high/low range
- **Strength filter:** Std dev of 20-day returns across top-5 mega-caps < 5%
- **Entry:** In trend AND dispersion < 5% → 100% TQQQ
- **Exit:** Trend breaks OR dispersion ≥ 5% → 100% BIL
- **Symbols:** Signal: QQQ + top-5 mega-cap dispersion. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 39% | -46% | 0.892 | 290 | 247 | 1.17 | 2.06 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 37% | 🟢 38% | 🔴 -6% | 🟢 118% | 🔴 -6% | 🟢 110% | 🟢 15% | 🟢 158% | 🔴 -40% | 🟢 106% | 🟢 60% | 🟢 18% |

> [!code]- Click to view: 020.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/020.py"
> ```


---

## Strategy-21
### ROC+D200 + 7% Trail Binary (021.py)

**Description:** A trend follower on QQQ that requires a positive 20-day rate-of-change, price above the 200-day high/low channel midpoint, and that the current price is no more than 7% below its 20-day high before buying TQQQ. The 7% trailing drawdown acts as an exit trigger as well, keeping the strategy out when a meaningful pullback from a recent peak occurs.

*Overfit 3/10 — 3/10. Two standard trend components (ROC20, D200 channel) plus a trailing drawdown filter at a moderately tuned 7% threshold. The 7% threshold is non-trivial but not extreme.*

- **Trend gate:** Price > midpoint of 200-day high/low channel
- **Entry:** ROC(20) > 0 AND price > D200 midpoint AND drawdown from 20-day high > -7% → 100% TQQQ
- **Exit:** Any condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -43% | 0.794 | 193 | 256 | 0.75 | 3.27 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -11% | 🔴 -2% | 🟢 85% | 🔴 -15% | 🟢 66% | 🟢 185% | 🟢 39% | 🔴 -19% | 🟢 56% | 🟢 23% | 🟢 42% |

> [!code]- Click to view: 021.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/021.py"
> ```


---

## Strategy-22
### CMO(20) Momentum (022.py)

**Description:** A momentum trend follower that uses the Chande Momentum Oscillator computed over 20 days on QQQ. A positive CMO value indicates that upward daily moves have dominated downward moves over the period, triggering a full allocation to TQQQ. When CMO turns negative the strategy exits to BIL.

*Overfit 3/10 — 2/10. Single CMO indicator with a canonical zero-crossover threshold. The only free parameter is the 20-day lookback window.*

- **Entry:** CMO(20) > 0 → 100% TQQQ
- **Exit:** CMO(20) ≤ 0 → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -50% | 0.843 | 218 | 267 | 0.82 | 3.13 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -11% | 🔴 -2% | 🟢 85% | 🔴 -8% | 🟢 86% | 🟢 170% | 🟢 39% | 🔴 -18% | 🟢 88% | 🟢 28% | 🟢 42% |

> [!code]- Click to view: 022.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/022.py"
> ```


---

## Strategy-23
### 3-State CMO+Median200 (023.py)

**Description:** A three-state trend follower that combines CMO(20) momentum with a 200-day median price filter on QQQ. When both signals are bullish the portfolio goes fully into TQQQ; when one is bullish the portfolio splits 50/50; when both are bearish it exits to BIL. Trading only occurs on state changes.

*Overfit 4/10 — 4/10. Two standard components (CMO20, 200-day median) with a canonical 50/50 mixed-state split. The 200-day median window and the three-state structure add moderate complexity.*

- **Trend gate:** Price > 200-day median close
- **Entry (trend):** CMO(20) > 0 AND price > 200-day median → 100% TQQQ
- **Entry (MR):** Either signal bullish → 50% TQQQ / 50% BIL
- **Exit:** Both signals bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open; trades only on state change

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -49% | 0.87 | 312 | 255 | 1.22 | 2.56 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | 🟢 6% | 🔴 -4% | 🟢 101% | 🔴 -11% | 🟢 75% | 🟢 139% | 🟢 62% | 🔴 -32% | 🟢 101% | 🟢 40% | 🟢 27% |

> [!code]- Click to view: 023.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/023.py"
> ```


---

## Strategy-24
### 3-State CMO+52w-High Gate (024.py)

**Description:** A three-state trend follower that combines CMO(20) momentum with a 52-week high drawdown gate. When CMO is positive and QQQ is within 15% of its 52-week high both signals agree and the portfolio goes fully into TQQQ. One bullish signal yields a 50/50 split; neither exits to BIL.

*Overfit 3/10 — 3/10. Two standard components (CMO20, 52-week proximity) with a moderately tuned 15% drawdown threshold and a canonical 50/50 mixed allocation.*

- **Trend gate:** Price drawdown from 52-week high > -15%
- **Entry (trend):** CMO(20) > 0 AND within 15% of 52-week high → 100% TQQQ
- **Entry (MR):** Either signal bullish → 50% TQQQ / 50% BIL
- **Exit:** Both signals bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open; trades only on state change

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 38% | -50% | 0.886 | 292 | 239 | 1.22 | 2.67 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | 🟢 6% | ⚪ 0% | 🟢 101% | 🔴 -13% | 🟢 99% | 🟢 138% | 🟢 62% | 🔴 -33% | 🟢 90% | 🟢 44% | 🟢 30% |

> [!code]- Click to view: 024.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/024.py"
> ```


---

## Strategy-26
### UpDnVol+52w+Top3 (026.py)

**Description:** A volume-breadth rotator that measures whether buying pressure (up-day volume) exceeds selling pressure (down-day volume) over 20 days, combined with a 52-week proximity filter (price within 7% of the one-year high). Both signals assess market health from different angles — participation from the volume side and strength from the drawdown side — alongside the 200-bar median regime gate.

*Overfit 4/10 — Up-volume vs down-volume over 20 bars; drawdown threshold of 93% of 252-day high; median-of-200 regime. The 93% threshold and 252-day window are specific tuned parameters. Rated 4/10.*

- **Trend gate:** QQQ price > median of last 200 closes
- **Strength filter:** 20-day up-day volume > 20-day down-day volume; price > 93% of 252-day rolling high
- **Entry:** Score 3 → 100% TQQQ; score 2 → 50% TQQQ + 50% Top 3; score 1 → 100% Top 3; score 0 → 50% Top 3 + 50% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / large-cap Top 3 / BIL
- **Universe:** Top 100 by dollar volume → Top 3 by market cap
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -44% | 0.754 | 914 | 661 | 1.38 | 1.48 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🟢 10% | 🔴 -8% | 🟢 93% | 🔴 -22% | 🟢 72% | 🟢 96% | 🟢 50% | 🔴 -26% | 🟢 117% | 🟢 37% | 🟢 10% |

> [!code]- Click to view: 026.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/026.py"
> ```


---

## Strategy-27
### Mom20+52w+Top3 (027.py)

**Description:** Combines a 20-day momentum signal with a 52-week high proximity filter and a 200-bar median regime gate. Being near the 52-week high is a well-known indicator of trend strength. The short-term momentum adds a recency confirmation. Together they construct a three-signal score that governs allocation between the leveraged ETF, large-cap stocks, and cash.

*Overfit 4/10 — 20-day momentum, 52-week proximity at 93% of 252-day max, median-of-200. The 93% threshold for 52w proximity is tuned. Rated 4/10.*

- **Trend gate:** QQQ price > median of last 200 closes
- **Strength filter:** 20-day price momentum positive; price > 93% of 252-day rolling high
- **Entry:** Score 3 → 100% TQQQ; score 2 → 50% TQQQ + 50% Top 3; score 1 → 100% Top 3; score 0 → 50% Top 3 + 50% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / large-cap Top 3 / BIL
- **Universe:** Top 100 by dollar volume → Top 3 by market cap
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -45% | 0.802 | 850 | 615 | 1.38 | 1.57 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 39% | 🟢 7% | 🔴 -7% | 🟢 106% | 🔴 -22% | 🟢 72% | 🟢 133% | 🟢 60% | 🔴 -36% | 🟢 103% | 🟢 47% | 🟢 17% |

> [!code]- Click to view: 027.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/027.py"
> ```


---

## Strategy-28
### M252_NEAR60_VOLCONT+Top3 (028.py)

**Description:** A trend-following rotator combining a full-year momentum check with near-60-day-high strength confirmation and a volatility contraction condition. The yearly lookback selects for macro uptrends, while the shorter-term filters ensure the current price action is both strong and calm before adding risk. Allocations are spread across TQQQ, the top three large-cap stocks, and BIL on the standard five-level ladder.

*Overfit 4/10 — Momentum compares close[-1] vs close[0] over 252 bars; near-60 threshold is 95%; volatility contraction compares 10-bar and 60-bar stddev windows; median trend gate uses the 101st value of 200 closes. The combination of a long-term momentum lookback with short-term vol filters is a specific structural choice.*

- **Trend gate:** QQQ price > median close of last 200 days (f0)
- **Entry (trend):** f1: QQQ close[-1] > close[0] (~252-day momentum, current vs. year-ago)
- **Entry (trend):** f2: QQQ price ≥ 95% of 60-day high
- **Entry (trend):** f3: 10-bar realized vol < 60-bar realized vol (volatility contraction)
- **Allocation:** n=4 → 100% TQQQ; n=3 → 70% TQQQ + 30% Top-3; n=2 → 30% TQQQ + 70% Top-3; n=1 → 50% Top-3 + 50% BIL; n=0 → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / top-3 large-cap stocks by market cap / BIL
- **Universe:** Top 100 by dollar volume → top 3 by market cap (fine selection), refreshed daily
- **Rebalance:** Daily, 30 min after market open; only trades when score n changes

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -50% | 0.752 | 1055 | 733 | 1.44 | 1.39 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 38% | 🟢 11% | 🔴 -15% | 🟢 102% | 🔴 -4% | 🟢 49% | 🟢 151% | 🟢 60% | 🔴 -46% | 🟢 105% | 🟢 41% | 🟢 11% |

> [!code]- Click to view: 028.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/028.py"
> ```


---

## Strategy-29
### ROC20_Zero (029.py)

**Description:** Applies a 20-day rate-of-change momentum signal on QQQ with a zero-line crossover. Holds leveraged Nasdaq while trailing momentum is positive and shifts entirely to T-bills when rate of change turns negative.

*Overfit 2/10 — Single textbook momentum indicator at a common period (20) with a zero-line threshold — minimal tuning*

- **Entry:** ROC(20) > 0: 100% TQQQ
- **Exit:** ROC(20) ≤ 0: 100% BIL
- **Symbols:** Signal & Execution: QQQ / TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -50% | 0.843 | 218 | 267 | 0.82 | 3.13 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -11% | 🔴 -2% | 🟢 85% | 🔴 -8% | 🟢 86% | 🟢 170% | 🟢 39% | 🔴 -18% | 🟢 88% | 🟢 28% | 🟢 42% |

> [!code]- Click to view: 029.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/029.py"
> ```


---

## Strategy-30
### OBV20_CCI20 (030.py)

**Description:** Pairs monthly OBV momentum with CCI on QQQ. Requires OBV rising over 20 days plus CCI > 0 for leveraged Nasdaq, and rotates to T-bills on either OBV weakness or deeply oversold CCI.

*Overfit 4/10 — Three tuned levers: OBV(20)-up, CCI(20)>0, and CCI<-100 with AND/OR logic*

- **Entry (trend):** OBV(20)-up AND CCI(20) > 0: 100% TQQQ
- **Entry (neutral):** Mixed: equal-weight top-5 large-caps
- **Exit:** OBV(20)-down OR CCI < -100: 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / top-5 fundamental large-caps / BIL
- **Universe:** Top 100 by dollar volume, then top 5 by market cap
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -29% | 0.831 | 744 | 745 | 1.00 | 2.10 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 2% | 🔴 -4% | 🔴 -2% | 🟢 37% | 🔴 -4% | 🟢 95% | 🟢 156% | 🟢 25% | 🟢 14% | 🟢 116% | 🟢 7% | 🟢 23% |

> [!code]- Click to view: 030.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/030.py"
> ```


---

## Strategy-31
### OBV20_ADX14 (031.py)

**Description:** Combines monthly OBV momentum with ADX directional bias on QQQ. Requires OBV rising plus +DI > -DI for leveraged Nasdaq, and exits to T-bills on either OBV weakness or a confirmed bearish ADX regime.

*Overfit 4/10 — Four tuned components: OBV(20)-up, +DI vs -DI direction, ADX(14)>25 bearish floor, and AND/OR combination*

- **Strength filter:** Bearish trigger requires ADX(14) > 25 AND -DI > +DI
- **Entry (trend):** OBV(20)-up AND +DI > -DI: 100% TQQQ
- **Entry (neutral):** Mixed: equal-weight top-5 large-caps
- **Exit:** OBV(20)-down OR (ADX > 25 AND -DI > +DI): 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / top-5 fundamental large-caps / BIL
- **Universe:** Top 100 by dollar volume, then top 5 by market cap
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -33% | 0.864 | 817 | 642 | 1.27 | 1.73 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 11% | 🔴 -15% | 🔴 -7% | 🟢 43% | 🟢 5% | 🟢 78% | 🟢 209% | 🟢 22% | 🟢 12% | 🟢 98% | 🟢 5% | 🟢 31% |

> [!code]- Click to view: 031.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/031.py"
> ```


---

## Strategy-33
### CCI20+ROC20+ATR (033.py)

**Description:** Extends the CCI+ROC momentum stack with an ATR-based volatility gate on QQQ. Holds leveraged Nasdaq only when both momentum indicators are positive and short-term volatility is contained below 1.3× the 63-day average range; exits to T-bills if any condition breaks.

*Overfit 4/10 — Three combined filters (CCI(20), ROC(20), ATR(14)/ATR(63) < 1.3) with a non-standard multiplier threshold — moderate tuning*

- **Entry:** CCI(20) > 0 AND ROC(20) > 0 AND ATR(14) < 1.3×ATR(63): 100% TQQQ
- **Exit:** Any condition breaks: 100% BIL
- **Symbols:** Signal & Execution: QQQ / TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -42% | 0.772 | 238 | 303 | 0.79 | 3.03 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🔴 -8% | 🔴 -16% | 🔴 -10% | 🟢 45% | 🔴 -3% | 🟢 97% | 🟢 227% | 🟢 58% | 🔴 -19% | 🟢 140% | 🔴 -1% | 🟢 12% |

> [!code]- Click to view: 033.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/033.py"
> ```


---

## Strategy-35
### Price52W_Percentile (035.py)

**Description:** Measures QQQ's current price as a percentile within its 52-week (252-day) high-low range. Holds leveraged Nasdaq when price sits in the upper half of the annual range and exits to T-bills when it falls into the lower half.

*Overfit 1/10 — Single price-position metric at a textbook lookback (252 days = 1 year) with a natural midpoint threshold — very minimal tuning*

- **Entry:** QQQ price percentile in 252-day range > 50%: 100% TQQQ
- **Exit:** Percentile ≤ 50%: 100% BIL
- **Symbols:** Signal & Execution: QQQ / TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -55% | 0.697 | 40 | 65 | 0.62 | 8.15 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🔴 -9% | 🔴 -5% | 🟢 118% | 🔴 -15% | 🟢 73% | 🟢 97% | 🟢 88% | 🔴 -51% | 🟢 92% | 🟢 62% | 🔴 -2% |

> [!code]- Click to view: 035.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/035.py"
> ```


---

## Strategy-36
### UpDay_Count20 (036.py)

**Description:** Counts the number of positive-close days in the trailing 20 trading sessions on QQQ as a simple market breadth proxy. Holds leveraged Nasdaq when more than half the recent sessions are up-days and exits to T-bills when down-days dominate.

*Overfit 2/10 — Single breadth metric at a common lookback (20 days) with a natural majority threshold (>10 out of 20) — minimal tuning*

- **Entry:** Up-day count in last 20 sessions > 10: 100% TQQQ
- **Exit:** Up-day count ≤ 10: 100% BIL
- **Symbols:** Signal & Execution: QQQ / TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -53% | 0.803 | 209 | 246 | 0.85 | 2.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 43% | 🟢 6% | 🟢 3% | 🟢 58% | 🔴 -26% | 🟢 81% | 🟢 147% | 🟢 41% | 🟢 28% | 🟢 94% | 🟢 8% | 🔴 -1% |

> [!code]- Click to view: 036.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/036.py"
> ```


---

## Strategy-37
### Price126D_Percentile (037.py)

**Description:** Applies the same range-percentile logic as the 52-week variant (698) but over a 6-month (126-day) lookback. Holds leveraged Nasdaq when QQQ is in the upper half of its recent 6-month range and exits to T-bills when it falls below the midpoint.

*Overfit 2/10 — Single price-position metric at a sensible shorter lookback (126 days ≈ 6 months) with a natural midpoint threshold — minimal tuning*

- **Entry:** QQQ price percentile in 126-day range > 50%: 100% TQQQ
- **Exit:** Percentile ≤ 50%: 100% BIL
- **Symbols:** Signal & Execution: QQQ / TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 35% | -54% | 0.785 | 70 | 83 | 0.84 | 4.80 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 46% | 🟢 25% | 🔴 -5% | 🟢 118% | 🔴 -25% | 🟢 59% | 🟢 119% | 🟢 68% | 🔴 -40% | 🟢 87% | 🟢 26% | 🟢 53% |

> [!code]- Click to view: 037.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/037.py"
> ```


---

## Strategy-38
### UpDay_Count55pct (038.py)

**Description:** Near-identical to UpDay_Count20 (705) but raises the threshold to a strict 55% majority. Holds leveraged Nasdaq when at least 11 of the last 20 sessions close up and switches to T-bills when down-days match or outnumber up-days.

*Overfit 2/10 — Same breadth metric as 705 with a marginally stricter threshold (≥11 vs >10); effectively the same trigger — minimal tuning*

- **Entry:** Up-day count in last 20 sessions ≥ 11 (≥55%): 100% TQQQ
- **Exit:** Up-day count < 11: 100% BIL
- **Symbols:** Signal & Execution: QQQ / TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -53% | 0.803 | 209 | 246 | 0.85 | 2.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 43% | 🟢 6% | 🟢 3% | 🟢 58% | 🔴 -26% | 🟢 81% | 🟢 147% | 🟢 41% | 🟢 28% | 🟢 94% | 🟢 8% | 🔴 -1% |

> [!code]- Click to view: 038.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/038.py"
> ```


---

## Strategy-39
### TII(20) >50.0 Bull (039.py)

**Description:** Uses the Trend Intensity Index to gauge whether QQQ closes above its 20-day SMA on a majority of recent sessions. Holds leveraged Nasdaq when more than half of the past 20 bars close above the SMA, switching to T-bills otherwise.

*Overfit 2/10 — Single indicator (TII, n=20) with canonical 50% threshold — minimal tuning*

- **Entry:** TII(20) > 50% (majority of last 20 closes above SMA(20)): 100% TQQQ
- **Exit:** TII(20) ≤ 50%: 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on regime change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -44% | 0.711 | 545 | 446 | 1.22 | 1.44 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 21% | 🔴 -6% | 🟢 29% | 🟢 55% | 🟢 49% | 🟢 40% | 🟢 84% | 🟢 2% | 🟢 15% | ⚪ 0% | 🟢 37% | 🟢 63% |

> [!code]- Click to view: 039.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/039.py"
> ```


---

## Strategy-41
### TQQQ Intrabar Vol Breakout (041.py)

**Description:** Uses a 240-bar average intrabar volatility (|open−close|/open) on TQQQ minute bars to identify low-vol regimes, entering 100% when vol < 0.1 and price is within 2% of the 240-minute high. Exits on vol spike > 0.15 or a 3% hard stop from entry.

*Overfit 3/10 — Three thresholds: vol entry 0.1, vol exit 0.15, proximity to high 98%, 3% stop. The vol entry/exit pair is calibrated to a specific breakout pattern and is somewhat arbitrary; the proximity filter is reasonable.*

- **Entry:** Avg intrabar vol (240-bar) < 0.1 AND price ≥ 240-min high × 0.98: 100% TQQQ
- **Exit vol:** Avg intrabar vol > 0.15: liquidate
- **Stop loss:** Price ≤ entry × 0.97: liquidate
- **Resolution:** Minute bars; active only after 10:00 AM ET

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 43% | -37% | 0.986 | 192 | 341 | 0.56 | 3.45 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 43% | 🟢 5% | 🟢 22% | 🟢 101% | 🟢 23% | 🟢 105% | 🟢 151% | 🟢 24% | 🔴 -33% | 🟢 107% | 🟢 52% | 🟢 18% |

> [!code]- Click to view: 041.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/041.py"
> ```


---

## Strategy-42
### Tech Dip Buy (042.py)

**Description:** Buys the top 5 US technology stocks by market cap when they pull back hard during an uptrend, then holds until they recover to new highs or the loss gets too large. Universe rotates automatically as market caps shift. Equal-weight across held positions up to 20% per slot.

*Overfit 2/10 — Textbook RSI(2)/SMA(50) entry with a clean 15% hard stop; dynamic universe removes hindsight symbol selection. Only mild concern is the small trade count (~80 trades over 11 years).*

- **Universe:** Top 5 US tech stocks by market cap (Morningstar Technology sector)
- **Entry:** RSI(2) < 30 AND price > SMA(50): up to 20% per name
- **Stop loss:** Price ≤ avg cost × 0.85: liquidate
- **Take profit:** Price ≥ 252-day high: liquidate
- **Rebalance:** Weekly (Mondays), 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 28% | -40% | 0.856 | 32 | 26 | 1.23 | 3.20 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 19% | ⚪ 0% | 🟢 7% | 🟢 37% | 🟢 6% | 🟢 40% | 🟢 39% | 🟢 52% | 🔴 -34% | 🟢 98% | 🟢 100% | 🟢 32% |

> [!code]- Click to view: 042.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/042.py"
> ```


---

## Strategy-43
### Top-5 MarketCap IBS Regime (043.py)

**Description:** Dynamically selects the top 5 US equities by market capitalization as the universe. In a bull regime (QQQ above its 200-day SMA), holds an equal-weight basket of all 5. In a bear regime, applies an IBS < 0.2 filter and holds only the stocks closing near their day's low (capitulation dips); exits the rest.

*Overfit 2/10 — Two parameters: SMA(200) regime filter and IBS threshold 0.2. Both are standard values. The top-5 market cap selection is deterministic. Low overfit.*

- **Universe:** Top 5 US stocks by market cap, daily resolution
- **Bull regime:** QQQ > SMA(200) → equal-weight all 5 positions
- **Bear regime:** QQQ ≤ SMA(200) → equal-weight only stocks with IBS < 0.2
- **IBS:** (close−low) / (high−low)
- **Rebalance:** Daily, 45 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27% | -26% | 0.981 | 3552 | 888 | 4.00 | 0.59 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 10% | 🟢 6% | ⚪ 0% | 🟢 37% | 🟢 10% | 🟢 44% | 🟢 89% | 🟢 44% | 🔴 -14% | 🟢 52% | 🟢 39% | 🟢 41% |

> [!code]- Click to view: 043.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/043.py"
> ```


---

## Strategy-49
### 2-State CMO+52w-High Gate (049.py)

**Description:** Two-state simplification of the 3-State CMO+52w-High Gate: requires BOTH CMO(20) positive AND QQQ within 15% of its 52-week high to hold TQQQ; exits entirely to BIL if either condition fails. Removes the mixed 50/50 state, making it a clean binary in-or-out signal.

*Overfit 2/10 — Same two parameters as the 3-state parent (CMO20 zero-cross, 15% drawdown from 52w high) — no additional tuning introduced by collapsing the mixed state.*

- **Entry:** CMO(20) > 0 AND drawdown from 52-week high > -15% → 100% TQQQ
- **Exit:** Either condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open (only on state change)

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 33% | -40% | 0.837 | 194 | 247 | 0.79 | 3.46 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -11% | 🔴 -2% | 🟢 85% | 🔴 -8% | 🟢 86% | 🟢 161% | 🟢 39% | 🔴 -19% | 🟢 63% | 🟢 28% | 🟢 42% |

> [!code]- Click to view: 049.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/potentials/049.py"
> ```


---
