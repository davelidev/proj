# QuantConnect High-Alpha Master Ledger

This document provides a consolidated, deep analysis of all trading strategies in this repository that met the primary performance criteria: **CAGR >= 28% and MaxDD <= 58%** (Backtest: 2014-2025).

## Summary Table

| # | Strategy Name | Source | Category | CAGR | MaxDD | Sharpe | Win % | Overfit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ [C1](#core-1-volatility-breakout) | Volatility Breakout | Core | Breakout | 42.8% | -37.4% | 0.986 | 36% | 6/10 |
| ✅ [C2](#core-2-tech-dip-buy) | Tech Dip Buy | Core | Dip Buy | 28.7% | -41.5% | 0.869 | 58% | 2/10 |
| ✅ [C3](#core-3-leveraged-rebalance) | Leveraged Rebalance | Core | Rebalance | 28.3% | -51.4% | 0.728 | 100% | 4/10 |
| ✅ [C4](#core-4-rsi-champion) | RSI Champion | Core | Mean Rev | 46.8% | -36.9% | 1.031 | 70% | 2/10 |
| ✅ [C5](#core-5-tqqq-dynamic-compounding) | TQQQ Dynamic Comp | Core | Trend/Mom | 30.9% | -49.0% | 0.738 | 53% | 4/10 |
| ✅ [C6](#core-6-expanding-breakout) | Expanding Breakout | Core | Breakout | 38.2% | -49.2% | 0.886 | 55% | 4/10 |
| ✅ [F3](#forum-3-tqqq-sma-trend) | TQQQ SMA Trend | Forum | Trend | 33.6% | -56.4% | 0.757 | 32% | 2/10 |
| ✅ [F23](#forum-23-trend-vol-hybrid) | Trend Vol Hybrid | Forum | Trend/Vol | 28.0% | -56.4% | 0.670 | 35% | 3/10 |
| ✅ [F35](#forum-35-vol-ratio-trend) | Vol Ratio Trend | Forum | Vol/Trend | 32.6% | -56.7% | 0.741 | 39% | 4/10 |
| ✅ [F41](#forum-41-trend-stretch-exit) | Trend Stretch Exit | Forum | Trend/Rev | 36.1% | -56.4% | 0.820 | 35% | 3/10 |
| ✅ [F101](#forum-101-letf-simple-rotation) | LETF Simple Rotation | Forum | Rotation | 124.5% | -46.8% | 1.869 | 54% | 7/10 |

## Yearly Performance Grid (2014-2025)

| # | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **C1** | 🟢 43% | 🟢 8% | 🟢 26% | 🟢 101% | 🟢 23% | 🟢 105% | 🟢 149% | 🟢 23% | 🔴 -32% | 🟢 107% | 🟢 52% | 🟢 18% |
| **C2** | 🟢 20% | ⚪ 0% | 🟢 9% | 🟢 35% | 🟢 6% | 🟢 46% | 🟢 55% | 🟢 48% | 🔴 -36% | 🟢 88% | 🟢 107% | 🟢 37% |
| **C3** | 🟢 34% | 🟢 13% | 🟢 7% | 🟢 71% | 🔴 -13% | 🟢 79% | 🟢 65% | 🟢 52% | 🔴 -47% | 🟢 118% | 🟢 37% | 🟢 21% |
| **C4** | 🟢 30% | 🔴 -8% | 🔴 -20% | 🟢 50% | 🟢 19% | 🟢 37% | 🟢 215% | 🟢 142% | 🟢 22% | 🟢 76% | 🟢 74% | 🟢 55% |
| **C5** | 🟢 35% | 🟢 4% | 🔴 -13% | 🟢 133% | 🟢 7% | 🟢 29% | 🟢 67% | 🟢 82% | 🔴 -20% | 🟢 70% | 🟢 29% | 🟢 28% |
| **C6** | 🟢 137% | 🔴 -3% | 🔴 -2% | 🟢 76% | 🟢 54% | 🟢 14% | 🟢 83% | 🟢 47% | 🔴 -14% | 🟢 72% | 🟢 39% | 🟢 32% |
| **F3** | 🟢 56% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 105% | 🟢 88% | 🔴 -44% | 🟢 113% | 🟢 62% | 🟢 24% |
| **F23** | 🟢 56% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -32% | 🟢 50% | 🟢 59% | 🟢 68% | 🔴 -44% | 🟢 113% | 🟢 58% | 🟢 24% |
| **F35** | 🟢 53% | ⚪ 0% | 🔴 -22% | 🟢 118% | 🔴 -24% | 🟢 50% | 🟢 105% | 🟢 88% | 🔴 -44% | 🟢 118% | 🟢 55% | 🟢 34% |
| **F41** | 🟢 60% | 🟢 1% | 🔴 -12% | 🟢 118% | 🔴 -23% | 🟢 50% | 🟢 136% | 🟢 77% | 🔴 -44% | 🟢 108% | 🟢 86% | 🟢 24% |
| **F101** | 🟢 64% | 🔴 -11% | 🟢 64% | 🟢 139% | 🟢 20% | 🟢 136% | 🟢 1021% | 🟢 256% | 🟢 18% | 🟢 66% | 🟢 187% | 🟢 382% |

---

## Core Portfolio

### Core-1: Volatility Breakout (vol_breakout.py)
**Description:** Waits for TQQQ to quietly compress near a recent high, then enters expecting a breakout. Exits on volatility spikes or stop loss.
- **Rules:** Price >= 98% of 240-min high AND avg intra-bar volatility < 0.1
- **Overfit:** 6/10 (Multiple tuned intra-day parameters)

### Core-2: Tech Dip Buy (tech_dip.py)
**Description:** Buys the biggest tech names when they pull back during an uptrend. Universe rotates by market cap.
- **Rules:** RSI(2) < 30 AND price > SMA(50)
- **Overfit:** 2/10 (Robust, standard indicators)

### Core-3: Leveraged Rebalance (leveraged_rebalance.py)
**Description:** Annual rebalancing of 3x leveraged ETFs (TQQQ, SOXL, TECL) and cash.
- **Rules:** Fixed target weights restored yearly.
- **Overfit:** 4/10 (Hindsight asset selection bias)

### Core-4: RSI Champion (rsi_champion.py)
**Description:** Decisive entries into leveraged tech ETFs during extreme oversold conditions.
- **Rules:** QQQ RSI(2) < 25
- **Overfit:** 2/10 (High trade count, single trigger)

### Core-5: TQQQ Dynamic Compounding (tqqq_dynamic.py)
**Description:** Trend-following with dynamic position sizing based on RSI momentum.
- **Rules:** Enter on TQQQ > SMA(200); De-lever on RSI(10) > 80.
- **Overfit:** 4/10 (Specific tiered allocation logic)

### Core-6: Expanding Breakout (expanding_breakout.py)
**Description:** Momentum burst entries when today's range expands beyond yesterday's.
- **Rules:** Expanding Range AND ADX(10) > 25; Exit on 20-day high.
- **Overfit:** 4/10 (Logical range expansion rule)

---

## Forum Alpha Discoveries

### Forum-3: TQQQ SMA Trend (it_3.py)
**Description:** Baseline 200-day SMA filter on QQQ to manage TQQQ exposure.
- **Rules:** QQQ > SMA(200)
- **Overfit:** 2/10 (Industry standard parameter)

### Forum-23: Trend Vol Hybrid (it_23.py)
**Description:** Combines SMA trend following with a VIX panic filter.
- **Rules:** QQQ > SMA(200) AND VIX < 30
- **Overfit:** 3/10 (Adds one macro volatility filter)

### Forum-35: Vol Ratio Trend (it_35.py)
**Description:** SMA trend following with a short/long-term volatility ratio filter.
- **Rules:** QQQ > SMA(200) AND VolRatio(10/60) < 1.2
- **Overfit:** 4/10 (Adds volatility lookback ratios)

### Forum-41: Trend Stretch Exit (it_41.py)
**Description:** Trend following with mean-reversion "stretch" thresholds for exits.
- **Rules:** QQQ > SMA(200) AND Stretch < 15%; Exit on Stretch > 20%.
- **Overfit:** 3/10 (Specific stretch thresholds)

### Forum-101: LETF Simple Rotation (it_101.py)
**Description:** Advanced 3-of-4 regime vote (SPY, QQQ, SMH, SOXL) with overbought hedges.
- **Rules:** Bull if 3/4 over SMA(202); Hedged via UVIX if RSI(15) > 72.
- **Overfit:** 7/10 (High complexity, multiple tickers and states)
