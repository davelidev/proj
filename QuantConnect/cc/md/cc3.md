# Archived Strategy Backtests

*Strategies removed from active tracking if: CAGR < 28%, MaxDD > 58%, or Overfit ≥ 8/10.*

| #                    | Pass | Category        | CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio | Overfit |
| :------------------- | :--- | :-------------- | :--- | :---- | :----- | :---- | :----- | :-------- | :----------- | :------ |
| [3](#strategy-3)     | ✅    | Trend           | 30%  | -55%  | 0.74   | 99    | 78    | 1.27     | 2.68         | 2/10   |
| [19](#strategy-19)   | ✅    | Trend           | 37%  | -57%  | 0.796  | 34    | 51    | 0.67     | 9.51         | 2/10   |
| [21](#strategy-21)   | ✅    | Trend           | 31%  | -52%  | 0.715  | 80    | 97    | 0.82     | 4.60         | 2/10   |
| [28](#strategy-28)   | ✅    | Trend           | 37%  | -57%  | 0.796  | 34    | 51    | 0.67     | 9.51         | 3/10   |
| [43](#strategy-43)   | ✅    | Trend           | 32%  | -49%  | 0.798  | 250   | 153   | 1.63     | 1.82         | 3/10   |
| [45](#strategy-45)   | ✅    | Rotation        | 32%  | -57%  | 0.772  | 209   | 122   | 1.71     | 1.23         | 3/10   |
| [46](#strategy-46)   | ✅    | Trend           | 34%  | -55%  | 0.79   | 270   | 133   | 2.03     | 1.55         | 3/10   |
| [47](#strategy-47)   | ✅    | Trend           | 30%  | -43%  | 0.787  | 222   | 181   | 1.23     | 2.30         | 3/10   |
| [48](#strategy-48)   | ✅    | Rotation        | 37%  | -58%  | 0.836  | 259   | 146   | 1.77     | 1.47         | 4/10   |
| [49](#strategy-49)   | ✅    | Trend           | 29%  | -50%  | 0.749  | 279   | 210   | 1.33     | 1.92         | 3/10   |


---
## Strategy-3
### Aroon(25) Trend (cc3_003.py)

**Description:** A trend follower using the Aroon indicator with a 25-day period applied to the Nasdaq ETF. It buys a leveraged Nasdaq ETF when AroonUp exceeds 70 and leads AroonDown, indicating a recent high has been set within the window. It exits to a short-term bond ETF when AroonDown exceeds 70 and leads AroonUp.

*Overfit 2/10 — Single Aroon indicator at the textbook 25-period with the textbook 70 threshold. Very low overfit.*

- **Entry:** AroonUp(25) > 70 AND AroonUp > AroonDown → 100% TQQQ
- **Exit:** AroonDown(25) > 70 AND AroonDown > AroonUp → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -55% | 0.74 | 99 | 78 | 1.27 | 2.68 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 15% | 🟢 17% | 🔴 -6% | 🟢 76% | 🟢 14% | 🟢 56% | 🟢 87% | 🟢 52% | 🔴 -40% | 🟢 80% | 🟢 32% | 🟢 49% |

> [!code]- Click to view: cc3_003.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_003.py"
> ```


---

## Strategy-19
### Donchian-200 Midline (cc3_019.py)

**Description:** A trend follower using the midpoint of the 200-day Donchian channel (average of the 200-day high and 200-day low) as a dynamic trend filter. When the Nasdaq ETF price is above this midline it holds a leveraged Nasdaq ETF; below it holds a short-term bond ETF. The midline serves as a slow, price-extremes-anchored moving average.

*Overfit 2/10 — Single Donchian midline at 200 days — a textbook period applied to the midpoint instead of the breakout levels. Very low overfit.*

- **Trend gate:** QQQ price > (200d high + 200d low) / 2
- **Entry:** QQQ > Donchian-200 midline → 100% TQQQ
- **Exit:** QQQ ≤ Donchian-200 midline → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -57% | 0.796 | 34 | 51 | 0.67 | 9.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 22% | 🔴 -5% | 🟢 118% | 🔴 -19% | 🟢 80% | 🟢 97% | 🟢 88% | 🔴 -47% | 🟢 93% | 🟢 62% | 🟢 20% |

> [!code]- Click to view: cc3_019.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_019.py"
> ```


---

## Strategy-21
### Donchian-100 Midline (cc3_021.py)

**Description:** A trend follower using the midpoint of the 100-day Donchian channel as the regime signal. When the Nasdaq ETF price is above the 100-day high/low midline the strategy holds a leveraged Nasdaq ETF, otherwise a short-term bond ETF. The 100-day window is faster than the 200-day variant, producing more frequent signal changes.

*Overfit 2/10 — Single Donchian midline at 100 days. The 100-day period is a standard alternative to 200; very low overfit.*

- **Trend gate:** QQQ price > (100d high + 100d low) / 2
- **Entry:** QQQ > Donchian-100 midline → 100% TQQQ
- **Exit:** QQQ ≤ Donchian-100 midline → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 31% | -52% | 0.715 | 80 | 97 | 0.82 | 4.60 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 2% | 🟢 32% | 🔴 -15% | 🟢 118% | 🔴 -28% | 🟢 64% | 🟢 131% | 🟢 54% | 🔴 -50% | 🟢 137% | 🟢 26% | 🟢 59% |

> [!code]- Click to view: cc3_021.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_021.py"
> ```


---

## Strategy-28
### Donchian-200 + Drawdown Stop (cc3_029.py)

**Description:** A trend follower combining the 200-day Donchian midline with an emergency drawdown stop. Both conditions must hold — price above the midline and less than 15% below its 20-day high — to remain in a leveraged Nasdaq ETF. If either fails, the strategy moves to a short-term bond ETF. The drawdown stop provides faster protection during sharp declines.

*Overfit 3/10 — Donchian-200 midline plus a 15% drawdown-from-20d-high stop. The 15% threshold and 20-day high lookback are the non-canonical tuned parameters; the Donchian midline component is standard.*

- **Trend gate:** QQQ price > Donchian-200 midline
- **Stop-loss:** QQQ price < 20-day high × 0.85 (−15% drawdown trigger)
- **Entry:** Trend gate holds AND no drawdown breach → 100% TQQQ
- **Exit:** Either condition fails → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -57% | 0.796 | 34 | 51 | 0.67 | 9.51 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 56% | 🟢 22% | 🔴 -5% | 🟢 118% | 🔴 -19% | 🟢 80% | 🟢 97% | 🟢 88% | 🔴 -47% | 🟢 93% | 🟢 62% | 🟢 20% |

> [!code]- Click to view: cc3_029.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_029.py"
> ```


---

## Strategy-43
### 3-State TQQQ Sizing (cc3_044.py)

**Description:** A three-state trend follower that sizes its leveraged Nasdaq ETF position based on how many of two indicators agree. When both Aroon(25) and the Donchian-200 midline are bullish the strategy goes fully into the leveraged ETF; when only one agrees it holds a 50/50 split between the leveraged ETF and a short-term bond ETF; and when both are bearish it holds only the bond ETF.

*Overfit 3/10 — Aroon(25) and Donchian-200 midline with a 50% intermediate TQQQ allocation. The 50/50 mixed-state weight is a simple round number; both filter parameters are textbook.*

- **Trend gate:** Aroon(25) bullish: AroonUp > 70 AND AroonUp > AroonDown; Donchian bullish: QQQ > 200d midline
- **Entry:** Both bullish → 100% TQQQ; one bullish → 50% TQQQ + 50% BIL; neither → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -49% | 0.798 | 250 | 153 | 1.63 | 1.82 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 33% | 🔴 -1% | 🔴 -1% | 🟢 89% | 🔴 -19% | 🟢 68% | 🟢 101% | 🟢 63% | 🔴 -44% | 🟢 126% | 🟢 50% | 🟢 33% |

> [!code]- Click to view: cc3_044.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_044.py"
> ```


---

## Strategy-45
### Aroon-TQQQ / Top-1 Defense (cc3_046.py)

**Description:** A two-regime rotator using Aroon(25) on the Nasdaq ETF to alternate between a leveraged Nasdaq ETF and the single largest US stock by market cap as the defensive position. By concentrating the defensive leg in one mega-cap instead of a diversified basket, this variant accepts higher single-name concentration risk outside of bull markets.

*Overfit 3/10 — Aroon(25) at threshold 70 combined with a top-1 market-cap defensive single stock. The Aroon parameters are canonical; the N=1 defensive concentration adds overfit risk.*

- **Trend gate:** AroonUp(25) > 70 AND AroonUp > AroonDown
- **Entry (trend):** Aroon bullish → 100% TQQQ
- **Entry (MR):** Not bullish → 100% top-1 mega-cap by market cap
- **Universe:** Top 100 by dollar volume → top 1 by market cap
- **Symbols:** Signal: QQQ. Execution: TQQQ / top-1 mega-cap
- **Rebalance:** Daily, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 32% | -57% | 0.772 | 209 | 122 | 1.71 | 1.23 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 39% | 🔴 -11% | 🟢 10% | 🟢 87% | 🔴 -25% | 🟢 90% | 🟢 134% | 🟢 56% | 🔴 -53% | 🟢 181% | 🟢 47% | 🟢 13% |

> [!code]- Click to view: cc3_046.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_046.py"
> ```


---

## Strategy-46
### 3-State 70/30 Middle (cc3_047.py)

**Description:** A three-state trend follower using Aroon(25) and the 200-day Donchian midline, but with a risk-on tilt in the mixed state: 70% in the leveraged Nasdaq ETF and 30% in bonds when only one indicator is bullish. This biases the intermediate regime toward equities, increasing expected returns at the cost of more risk during uncertain periods.

*Overfit 3/10 — Same Aroon(25) + Donchian-200 midline framework as strategy 43, with the mixed-state weight shifted to 70/30 TQQQ/BIL. The 70/30 split is a tuned non-round alternative to 50/50.*

- **Trend gate:** Aroon(25) bullish AND/OR QQQ > Donchian-200 midline
- **Entry:** Both bullish → 100% TQQQ; one bullish → 70% TQQQ + 30% BIL; neither → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 34% | -55% | 0.79 | 270 | 133 | 2.03 | 1.55 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 42% | 🟢 8% | 🔴 -2% | 🟢 100% | 🔴 -18% | 🟢 77% | 🟢 101% | 🟢 73% | 🔴 -51% | 🟢 123% | 🟢 55% | 🟢 28% |

> [!code]- Click to view: cc3_047.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_047.py"
> ```


---

## Strategy-47
### 3-State 30/70 Middle (cc3_048.py)

**Description:** A three-state trend follower using Aroon(25) and the 200-day Donchian midline, with a risk-off tilt in the mixed state: only 30% in the leveraged Nasdaq ETF and 70% in bonds when only one indicator is bullish. This biases the intermediate regime toward capital preservation, reducing drawdowns at the cost of lower participation in ambiguous trends.

*Overfit 3/10 — Same Aroon(25) + Donchian-200 midline framework as strategy 43, with the mixed-state weight shifted to 30/70 TQQQ/BIL. The 30/70 split is a tuned non-round alternative to 50/50.*

- **Trend gate:** Aroon(25) bullish AND/OR QQQ > Donchian-200 midline
- **Entry:** Both bullish → 100% TQQQ; one bullish → 30% TQQQ + 70% BIL; neither → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 30% | -43% | 0.787 | 222 | 181 | 1.23 | 2.30 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 24% | 🔴 -10% | 🔴 -1% | 🟢 79% | 🔴 -19% | 🟢 59% | 🟢 100% | 🟢 54% | 🔴 -36% | 🟢 128% | 🟢 45% | 🟢 38% |

> [!code]- Click to view: cc3_048.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_048.py"
> ```


---

## Strategy-48
### Graceful TQQQ/Top-1 Step-Down (cc3_049.py)

**Description:** A three-state rotator that gracefully steps down from a leveraged Nasdaq ETF to the largest single mega-cap stock as market conditions deteriorate. In the bull state it holds 100% TQQQ; in the mixed state it blends 50% TQQQ with 50% of the top-1 mega-cap; and in the bear state it holds 100% of the top-1 mega-cap. This avoids pure bond exposure by using a large-cap equity as the defensive anchor.

*Overfit 4/10 — Aroon(25) + Donchian-200 midline three-state framework with a top-1 mega-cap as the defensive leg. The 50/50 mixed weight is a round number; the N=1 mega-cap defensive adds overfit. The combination of 4+ design choices elevates overfit.*

- **Trend gate:** Aroon(25) bullish AND/OR QQQ > Donchian-200 midline
- **Entry:** Both bullish → 100% TQQQ; one bullish → 50% TQQQ + 50% top-1 mega-cap; neither → 100% top-1 mega-cap
- **Universe:** Top 100 by dollar volume → top 1 by market cap
- **Symbols:** Signal: QQQ. Execution: TQQQ / top-1 mega-cap
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 37% | -58% | 0.836 | 259 | 146 | 1.77 | 1.47 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 57% | 🟢 8% | 🟢 5% | 🟢 102% | 🔴 -24% | 🟢 93% | 🟢 147% | 🟢 71% | 🔴 -54% | 🟢 151% | 🟢 52% | 🟢 13% |

> [!code]- Click to view: cc3_049.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_049.py"
> ```


---

## Strategy-49
### 3-State Aroon-25 + Donchian-100 (cc3_050.py)

**Description:** A three-state trend follower pairing the faster Aroon(25) with the intermediate 100-day Donchian midline, producing a quicker-reacting variant of the standard three-state system. Both indicators must be bullish for full TQQQ exposure; one bullish gives a 50/50 blend; neither sends the portfolio to bonds.

*Overfit 3/10 — Aroon(25) at threshold 70 combined with a Donchian-100 midline. The 100-day Donchian is faster than the 200-day, increasing signal frequency; the 50/50 mixed weight is a round number. Modest overfit from two-indicator combination.*

- **Trend gate:** Aroon(25) bullish AND/OR QQQ > Donchian-100 midline
- **Entry:** Both bullish → 100% TQQQ; one bullish → 50% TQQQ + 50% BIL; neither → 100% BIL
- **Symbols:** Signal: QQQ. Execution: TQQQ / BIL
- **Rebalance:** Daily on state change, 30 min after market open

| CAGR | MaxDD | Sharpe | Win # | Loss # | W/L Ratio | Profit Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 29% | -50% | 0.749 | 279 | 210 | 1.33 | 1.92 |

| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 8% | 🟢 3% | 🔴 -7% | 🟢 89% | 🔴 -23% | 🟢 61% | 🟢 115% | 🟢 50% | 🔴 -45% | 🟢 150% | 🟢 34% | 🟢 52% |

> [!code]- Click to view: cc3_050.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/cc_algos/cc3_050.py"
> ```


---
