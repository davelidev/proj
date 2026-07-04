# Ensemble Overview

## 1. Leveraged Rebalance
**Type:** Rebalance
**Backtest:** 37% / -82% / 1
**Description:** Buy and hold TQQQ, reset allocation once a year
**Entry:** 100% TQQQ on first trading day of each year
**Exit:** Hold all year, no intra-year exit

---

## 2. IBS ATR Stop
**Type:** Reversion
**Backtest:** 30% / -41% / 921
**Description:** Buy when TQQQ closes near its daily low, sell near daily high or on stop
**Entry:** TQQQ IBS < 0.1 while QQQ > SMA(200) → 33% each TQQQ / SOXL / TECL
**Exit:** IBS > 0.9 or 2×ATR(14) trailing stop

---

## 3. RSI Three Vote
**Type:** Reversion
**Backtest:** 37% / -42% / 2742
**Description:** Scale into QQQ oversold dips, exit on RSI recovery
**Entry:** TQQQ / SOXL / TECL weight = n/3 RSI(2) thresholds QQQ is below (30 / 25 / 20)
**Exit:** RSI recovers above all thresholds

---

## 4. SMA200 RSI Tiers
**Type:** Trend
**Backtest:** 33% / -50% / 168
**Description:** Hold TQQQ above trend, scale up on dips and trim on overbought
**Entry:** TQQQ weight tiers while above SMA(200): base 50% / RSI(2) < 30 → 100% / RSI(14) > 70 → 20%
**Exit:** TQQQ < SMA(200)

---

## 5. SMA200 Pyramid
**Type:** Trend
**Backtest:** 32% / -49% / 214
**Description:** Enter on trend, add size as price rises, exit on trend break
**Entry:** TQQQ weight = 50% + 15% per 5% gain above entry (cap 100%) while QQQ > SMA(200)
**Exit:** QQQ < SMA(200)

---

## 6. SMA Five Vote
**Type:** Trend
**Backtest:** 35% / -43% / 590
**Description:** Weight position by how many timeframes agree on uptrend
**Entry:** TQQQ weight = n/8 SMAs QQQ is above (20 / 50 / 100 / 150×4 / 200)
**Exit:** Weight falls to 0 as price drops below each SMA

---

## 7. Donchian Five Vote
**Type:** Trend
**Backtest:** 35% / -55% / 301
**Description:** Weight position by how many channel midlines are cleared
**Entry:** TQQQ weight = n/5 Donchian midlines QQQ is above (50 / 100 / 150 / 200 / 250d)
**Exit:** Weight falls to 0 as price drops below midlines

---

## 8. Momentum Vote
**Type:** Momentum
**Backtest:** 36% / -37% / 855
**Description:** Weight position by how many momentum signals are bullish
**Entry:** TQQQ weight = n/3 momentum signals bullish on QQQ (ROC(20) > 0 / up-days > 10 / TII(20) > 10)
**Exit:** All 3 bearish

---

## 9. Trend Stretch Exit
**Type:** Trend
**Backtest:** 43% / -54% / 65
**Description:** Enter trend early when not yet stretched, exit when overstretched
**Entry:** 100% TQQQ when QQQ > SMA(200) and price stretch < 5%
**Exit:** QQQ < SMA(200) or stretch > 20% above SMA

---

## 10. Golden Cross ATR
**Type:** Trend
**Backtest:** 37% / -52% / 179
**Description:** Ride golden cross in calm markets, exit on cross flip or vol spike
**Entry:** 100% TQQQ when QQQ EMA(50) > EMA(200) and 20d vol < 30%
**Exit:** Death cross, vol > 30%, or 3×ATR(14) trailing stop

---

## 11. Range Compressed
**Type:** Range
**Backtest:** 33% / -43% / 130
**Description:** Hold during quiet trending markets, avoid volatile expansions
**Entry:** QQQ > 200d median AND recent daily swings not expanded beyond 10% above 200d baseline → 100%; one condition → 50%
**Exit:** Both false

---

## 12. MFI14 Hysteresis
**Type:** Volume
**Backtest:** 38% / -46% / 94
**Description:** Hold through strong money inflow, sit out on outflow
**Entry:** 100% TQQQ when QQQ MFI(14) > 60; hold when 40–60
**Exit:** MFI < 40

---

## 13. Vol Regime 20
**Type:** Volatility
**Backtest:** 34% / -46% / 135
**Description:** Scale position inversely with realized volatility
**Entry:** TQQQ weight tiers by 20d vol: (< 20% → 100%), (20–30% → 50%), (> 30% → 0%)
**Exit:** vol > 30%

---

## Ensemble (UltimateAlgo)
**Backtest:** 38% / -34%

---

## Yearly Returns

| # | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 🟢 64% | 🟢 22% | 🟢 11% | 🟢 118% | 🔴 -19% | 🟢 132% | 🟢 108% | 🟢 86% | 🔴 -79% | 🟢 198% | 🟢 61% | 🟢 34% |
| 2 | ⚪ 0% | 🔴 -24% | 🟢 26% | 🟢 52% | 🟢 26% | 🟢 90% | 🟢 195% | 🟢 9% | 🔴 -19% | 🟢 44% | 🟢 58% | 🟢 15% |
| 3 | 🟢 30% | 🔴 -11% | 🔴 -23% | 🟢 50% | 🔴 -6% | 🟢 52% | 🟢 90% | 🟢 114% | 🟢 26% | 🟢 81% | 🟢 41% | 🟢 70% |
| 4 | 🟢 29% | 🟢 17% | 🔴 -6% | 🟢 113% | 🟢 10% | 🟢 23% | 🟢 59% | 🟢 104% | 🔴 -20% | 🟢 65% | 🟢 30% | 🟢 43% |
| 5 | 🟢 36% | 🔴 -7% | 🔴 -4% | 🟢 111% | 🟢 2% | 🟢 33% | 🟢 101% | 🟢 87% | 🔴 -36% | 🟢 88% | 🟢 61% | 🟢 9% |
| 6 | 🟢 40% | 🟢 3% | 🔴 -5% | 🟢 103% | 🔴 -2% | 🟢 42% | 🟢 128% | 🟢 62% | 🔴 -37% | 🟢 119% | 🟢 42% | 🟢 35% |
| 7 | 🟢 37% | 🟢 14% | 🔴 -10% | 🟢 113% | 🔴 -14% | 🟢 70% | 🟢 132% | 🟢 68% | 🔴 -47% | 🟢 105% | 🟢 51% | 🟢 33% |
| 8 | 🟢 38% | 🔴 -1% | 🟢 15% | 🟢 67% | 🟢 6% | 🟢 77% | 🟢 122% | 🟢 31% | 🟢 8% | 🟢 50% | 🟢 31% | 🟢 31% |
| 9 | 🟢 76% | 🟢 1% | 🔴 -7% | 🟢 118% | 🔴 -11% | 🟢 45% | 🟢 112% | 🟢 91% | 🔴 -45% | 🟢 137% | 🟢 135% | 🟢 23% |
| 10 | 🟢 68% | 🟢 26% | 🔴 -11% | 🟢 100% | 🟢 7% | 🟢 87% | 🟢 110% | 🟢 45% | 🔴 -22% | 🟢 110% | 🟢 43% | 🔴 -12% |
| 11 | 🟢 33% | 🔴 -5% | 🔴 -2% | 🟢 96% | ⚪ 0% | 🟢 62% | 🟢 99% | 🟢 67% | 🔴 -34% | 🟢 132% | 🟢 40% | 🟢 10% |
| 12 | 🟢 25% | 🔴 -15% | 🟢 28% | 🟢 90% | 🔴 -2% | 🟢 107% | 🟢 136% | 🟢 21% | 🔴 -14% | 🟢 64% | 🟢 53% | 🟢 47% |
| 13 | 🟢 41% | 🟢 9% | 🟢 4% | 🟢 118% | 🟢 2% | 🟢 62% | 🟢 65% | 🟢 66% | 🔴 -36% | 🟢 107% | 🟢 52% | 🟢 5% |
| **E** | 🟢 42% | 🟢 5% | 🟢 2% | 🟢 95% | 🟢 1% | 🟢 69% | 🟢 112% | 🟢 65% | 🔴 -26% | 🟢 102% | 🟢 56% | 🟢 29% |

---

## vs QQQ / QLD

| Year | QQQ (orig) | QQQ | QLD | TQQQ | Δ QQQ | Δ QLD | Δ TQQQ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2010 | 🟢 19% | 🟢 9% | 🟢 13% | 🟢 28% | -10% | -6% | +9% |
| 2011 | 🟢 3% | 🔴 -9% | 🔴 -18% | 🔴 -25% | -12% | -21% | -28% |
| 2012 | 🟢 18% | 🟢 6% | 🟢 9% | 🟢 15% | -12% | -9% | -3% |
| 2013 | 🟢 37% | 🟢 28% | 🟢 57% | 🟢 89% | -9% | +20% | +52% |
| 2014 | 🟢 19% | 🟢 17% | 🟢 28% | 🟢 39% | -2% | +9% | +20% |
| 2015 | 🟢 9% | 🟢 2% | 🟢 3% | 🟢 5% | -7% | -6% | -4% |
| 2016 | 🟢 7% | 🟢 2% | 🟢 3% | 🟢 2% | -5% | -4% | -5% |
| 2017 | 🟢 33% | 🟢 32% | 🟢 62% | 🟢 95% | -1% | +29% | +62% |
| 2018 | ⚪ 0% | 🟢 4% | 🟢 3% | 🟢 1% | +4% | +3% | +1% |
| 2019 | 🟢 39% | 🟢 27% | 🟢 47% | 🟢 69% | -12% | +8% | +30% |
| 2020 | 🟢 48% | 🟢 47% | 🟢 85% | 🟢 112% | -1% | +37% | +64% |
| 2021 | 🟢 27% | 🟢 27% | 🟢 46% | 🟢 65% | 0% | +19% | +38% |
| 2022 | 🔴 -33% | 🔴 -9% | 🔴 -18% | 🔴 -26% | +24% | +15% | +7% |
| 2023 | 🟢 55% | 🟢 38% | 🟢 68% | 🟢 102% | -17% | +13% | +47% |
| 2024 | 🟢 26% | 🟢 28% | 🟢 40% | 🟢 57% | +2% | +14% | +31% |
| 2025 | 🟢 21% | 🟢 19% | 🟢 25% | 🟢 32% | -2% | +4% | +11% |
| **CAGR** | **19%** | **16%** | **25%** | **35%** | **-3%** | **+6%** | **+16%** |
| **MaxDD** | **-35%** | **-16%** | **-29%** | **-38%** | **+19%** | **+6%** | **-3%** |
