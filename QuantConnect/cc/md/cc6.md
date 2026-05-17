# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [151](#strategy-151) | ✅    | —               | 37%  | -50%  | 0.862  | 303   | 238   | 1.27     | 2.48         | 3/10   |
| [152](#strategy-152) | ✅    | —               | 41%  | -51%  | 0.916  | 374   | 219   | 1.71     | 1.90         | 3/10   |
| [153](#strategy-153) | ✅    | —               | 30%  | -40%  | 0.78   | 191   | 254   | 0.75     | 3.36         | 3/10   |
| [154](#strategy-154) | ✅    | —               | 31%  | -43%  | 0.794  | 193   | 256   | 0.75     | 3.27         | 3/10   |
| [155](#strategy-155) | ✅    | —               | 32%  | -46%  | 0.826  | 215   | 286   | 0.75     | 3.09         | 3/10   |
| [157](#strategy-157) | ✅    | —               | 35%  | -50%  | 0.843  | 218   | 267   | 0.82     | 3.13         | 3/10   |
| [164](#strategy-164) | ✅    | —               | 37%  | -49%  | 0.87   | 312   | 255   | 1.22     | 2.56         | 4/10   |
| [165](#strategy-165) | ✅    | —               | 31%  | -44%  | 0.798  | 396   | 351   | 1.13     | 2.26         | 4/10   |
| [166](#strategy-166) | ✅    | —               | 31%  | -47%  | 0.782  | 411   | 336   | 1.22     | 1.96         | 4/10   |
| [169](#strategy-169) | ✅    | —               | 38%  | -50%  | 0.886  | 292   | 239   | 1.22     | 2.67         | 3/10   |
| [171](#strategy-171) | ✅    | —               | 36%  | -55%  | 0.808  | 267   | 228   | 1.17     | 1.79         | 4/10   |
| [175](#strategy-175) | ✅    | —               | 30%  | -44%  | 0.766  | 335   | 322   | 1.04     | 2.48         | 4/10   |


---
## Strategy-151
### 3-State ROC20+D300 (cc3_152.py)

**Description:** A three-state trend follower on QQQ using two concurrent signals: a 20-day rate-of-change and whether price is above the midpoint of the 300-day high/low channel. When both signals agree bullish the full portfolio goes into leveraged tech ETF; when they disagree the portfolio splits evenly; when both are bearish it holds cash-equivalent. Execution uses TQQQ for risk-on and BIL for risk-off.

*Overfit 3/10 — 3/10. Two standard momentum components (ROC20 and 300-day channel midpoint) with canonical 50/50 mixed-state allocation. The 300-day channel window and the 50/50 split are the main free parameters.*

- **Trend gate:** Price > midpoint of 300-day high/low channel (D300)
- **Entry (trend):** ROC(20) > 0 AND price > D300 midpoint → 100% TQQQ
- **Entry (MR):** Either condition true → 50% TQQQ / 50% BIL
- **Exit:** Both signals bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open; trades only on state change

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -50% | 0.862 | 303 | 238 | 1.27 | 2.48 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 41% | ⚪ 0% | 🟢 2% | 🟢 101% | 🔴 -11% | 🟢 84% | 🟢 128% | 🟢 62% | 🔴 -33% | 🟢 91% | 🟢 44% | 🟢 32% |

> [!code]- Click to view: cc3_152.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_152.py"
> ```


---

## Strategy-152
### 3-State ROC20+D150 70/30 (cc3_153.py)

**Description:** A three-state trend follower identical in structure to the D300 variant but using a 150-day high/low channel and a 70/30 mixed-state allocation instead of 50/50. When both ROC and channel signals agree bullish it goes fully into TQQQ; when only one is bullish it holds 70% TQQQ and 30% BIL; when both are bearish it moves fully to BIL.

*Overfit 3/10 — 3/10. Two standard components (ROC20, 150-day channel) plus one moderately tuned mixed-state weight (70/30 vs canonical 50/50). The 150-day window and 70/30 split are the primary free parameters.*

- **Trend gate:** Price > midpoint of 150-day high/low channel (D150)
- **Entry (trend):** ROC(20) > 0 AND price > D150 midpoint → 100% TQQQ
- **Entry (MR):** Either condition true → 70% TQQQ / 30% BIL
- **Exit:** Both signals bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open; trades only on state change

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 41% | -51% | 0.916 | 374 | 219 | 1.71 | 1.90 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 47% | 🟢 12% | 🔴 -1% | 🟢 108% | 🔴 -33% | 🟢 91% | 🟢 159% | 🟢 72% | 🔴 -23% | 🟢 102% | 🟢 49% | 🟢 41% |

> [!code]- Click to view: cc3_153.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_153.py"
> ```


---

## Strategy-153
### ROC+D100+D250 Consensus (cc3_154.py)

**Description:** A trend follower that requires consensus among three signals before buying TQQQ: a positive 20-day rate-of-change and price above both the 100-day and 250-day high/low channel midpoints. An additional trailing drawdown gate checks that the current price has not fallen more than a negligible fraction from its 20-day high. Any failure exits to BIL.

*Overfit 3/10 — 3/10. Three standard trend components (ROC20, D100 midpoint, D250 midpoint) with a near-trivial 20-day high drawdown filter (threshold effectively zero at -1.0). The dual-channel window choice is the main free parameter.*

- **Trend gate:** Price > D100 midpoint AND price > D250 midpoint
- **Entry:** ROC(20) > 0 AND both channel gates pass AND price ≤ 1.0 drawdown from 20-day high → 100% TQQQ
- **Exit:** Any condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -40% | 0.78 | 191 | 254 | 0.75 | 3.36 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 19% | 🔴 -11% | 🔴 -5% | 🟢 85% | 🔴 -15% | 🟢 66% | 🟢 161% | 🟢 39% | 🔴 -19% | 🟢 74% | 🟢 20% | 🟢 42% |

> [!code]- Click to view: cc3_154.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_154.py"
> ```


---

## Strategy-154
### ROC+D200 + 7% Trail Binary (cc3_155.py)

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

> [!code]- Click to view: cc3_155.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_155.py"
> ```


---

## Strategy-155
### ROC+D200 + 4% Trail Binary (cc3_156.py)

**Description:** Identical in structure to the 7% trailing drawdown variant but tightens the trailing stop to 4%. This makes the strategy more reactive to short-term pullbacks, exiting to BIL as soon as QQQ drops more than 4% from its 20-day high even if the broader 200-day channel and ROC signals remain bullish.

*Overfit 3/10 — 3/10. Same two-component structure as the 7% variant with the trailing drawdown threshold tightened to 4%. The tighter threshold adds a slightly more tuned parameter.*

- **Trend gate:** Price > midpoint of 200-day high/low channel
- **Entry:** ROC(20) > 0 AND price > D200 midpoint AND drawdown from 20-day high > -4% → 100% TQQQ
- **Exit:** Any condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -46% | 0.826 | 215 | 286 | 0.75 | 3.09 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 26% | 🔴 -22% | 🔴 -2% | 🟢 85% | 🔴 -9% | 🟢 66% | 🟢 208% | 🟢 28% | 🔴 -19% | 🟢 68% | 🟢 38% | 🟢 34% |

> [!code]- Click to view: cc3_156.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_156.py"
> ```


---

## Strategy-157
### CMO(20) Momentum (cc3_158.py)

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

> [!code]- Click to view: cc3_158.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_158.py"
> ```


---

## Strategy-164
### 3-State CMO+Median200 (cc3_165.py)

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

> [!code]- Click to view: cc3_165.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_165.py"
> ```


---

## Strategy-165
### 3-State Aroon+CMO (cc3_166.py)

**Description:** A three-state momentum system that votes between the Aroon(25) indicator and CMO(20) on QQQ. The Aroon is considered bullish when Aroon Up exceeds 70 and is above Aroon Down; CMO is bullish when positive. Full TQQQ allocation requires both conditions; one bullish signal yields a 50/50 split; neither triggers a BIL allocation.

*Overfit 4/10 — 4/10. Two standard momentum indicators (Aroon-25 and CMO-20) with a non-canonical Aroon threshold of 70 (slightly tuned vs the standard 50) and a 50/50 mixed-state weight.*

- **Strength filter:** Aroon Up(25) > 70 AND Aroon Up > Aroon Down
- **Entry (trend):** Aroon bullish AND CMO(20) > 0 → 100% TQQQ
- **Entry (MR):** Either signal bullish → 50% TQQQ / 50% BIL
- **Exit:** Both signals bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open; trades only on state change

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -44% | 0.798 | 396 | 351 | 1.13 | 2.26 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 20% | 🔴 -16% | 🔴 -2% | 🟢 75% | 🔴 -14% | 🟢 70% | 🟢 133% | 🟢 41% | 🔴 -30% | 🟢 123% | 🟢 33% | 🟢 44% |

> [!code]- Click to view: cc3_166.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_166.py"
> ```


---

## Strategy-166
### 3-State Aroon+CMO 70/30 (cc3_167.py)

**Description:** A three-state momentum system identical to the 50/50 Aroon+CMO variant, but with the mixed-state allocation set to 70% TQQQ and 30% BIL instead of 50/50. This tilts the partial-conviction state toward risk, giving more exposure when only one of the two signals is bullish.

*Overfit 4/10 — 4/10. Same two-indicator structure as the 50/50 variant with a moderately tuned mixed-state weight of 70/30. The Aroon Up threshold of 70 and the 70/30 split are the primary non-canonical parameters.*

- **Strength filter:** Aroon Up(25) > 70 AND Aroon Up > Aroon Down
- **Entry (trend):** Aroon bullish AND CMO(20) > 0 → 100% TQQQ
- **Entry (MR):** Either signal bullish → 70% TQQQ / 30% BIL
- **Exit:** Both signals bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open; trades only on state change

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -47% | 0.782 | 411 | 336 | 1.22 | 1.96 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 22% | 🔴 -16% | 🔴 -5% | 🟢 85% | 🔴 -10% | 🟢 66% | 🟢 155% | 🟢 37% | 🔴 -31% | 🟢 106% | 🟢 32% | 🟢 45% |

> [!code]- Click to view: cc3_167.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_167.py"
> ```


---

## Strategy-169
### 3-State CMO+52w-High Gate (cc3_170.py)

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

> [!code]- Click to view: cc3_170.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_170.py"
> ```


---

## Strategy-171
### CMO + Top-1 Mega-Cap Defense (cc3_172.py)

**Description:** A rotator that uses CMO(20) on QQQ as a regime filter. When momentum is positive it holds TQQQ fully; when momentum is negative it dynamically rotates to the single largest-market-cap stock from the top 100 by dollar volume as a defensive holding. The strategy uses a daily universe update to identify the top mega-cap equity for defensive allocation.

*Overfit 4/10 — 4/10. CMO20 at a canonical zero threshold combined with a non-standard defensive rotation to the single largest-cap stock. The mega-cap defensive choice and the CMO period are the key free parameters.*

- **Trend gate:** CMO(20) on QQQ > 0 → risk-on
- **Entry:** CMO > 0 → 100% TQQQ
- **Exit:** CMO ≤ 0 → 100% top-1 market-cap stock from top-100 dollar-volume universe
- **Universe:** Coarse: top 100 by dollar volume. Fine: largest 1 by market cap as defensive
- **Symbols:** Signal: QQQ. Execution: TQQQ (bull) / top-1 mega-cap (bear)
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 36% | -55% | 0.808 | 267 | 228 | 1.17 | 1.79 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 34% | 🟢 6% | ⚪ 0% | 🟢 94% | 🔴 -20% | 🟢 118% | 🟢 173% | 🟢 54% | 🔴 -44% | 🟢 126% | 🟢 35% | 🟢 13% |

> [!code]- Click to view: cc3_172.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_172.py"
> ```


---

## Strategy-175
### 3-State Aroon-Osc + CMO (cc3_176.py)

**Description:** A three-state momentum system that combines the Aroon oscillator with CMO(20) on QQQ. The Aroon oscillator (Up − Down) must exceed 30 for the Aroon signal to be bullish; CMO must be positive. Both bullish gives full TQQQ; one bullish gives 50/50; neither gives BIL. This uses the oscillator form of Aroon rather than the directional Up>70 form.

*Overfit 4/10 — 4/10. Two standard momentum indicators with the Aroon oscillator threshold set to 30 (non-canonical vs the 50 used in the binary version) and a standard 50/50 mixed allocation.*

- **Strength filter:** Aroon oscillator (period 25) > 30
- **Entry (trend):** Aroon oscillator > 30 AND CMO(20) > 0 → 100% TQQQ
- **Entry (MR):** Either signal bullish → 50% TQQQ / 50% BIL
- **Exit:** Both signals bearish → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open; trades only on state change

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -44% | 0.766 | 335 | 322 | 1.04 | 2.48 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 20% | 🔴 -4% | 🔴 -6% | 🟢 82% | 🔴 -2% | 🟢 71% | 🟢 116% | 🟢 40% | 🔴 -26% | 🟢 69% | 🟢 36% | 🟢 41% |

> [!code]- Click to view: cc3_176.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_176.py"
> ```


---
