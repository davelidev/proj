# Ensemble Overview

## 1. Leveraged Rebalance
**Type:** Rebalance
**Backtest:** 37% / -82%
**Description:** Buy and hold TQQQ, reset allocation once a year
**Entry:** 100% TQQQ on first trading day of each year
**Exit:** Hold all year, no intra-year exit

---

## 2. IBS ATR Stop
**Type:** Reversion
**Backtest:** 30% / -41%
**Description:** Buy when TQQQ closes near its daily low, sell near daily high or on stop
**Entry:** TQQQ IBS < 0.1 while QQQ > SMA(200) → 33% each TQQQ / SOXL / TECL
**Exit:** IBS > 0.9 or 2×ATR(14) trailing stop

---

## 3. RSI Three Vote
**Type:** Reversion
**Backtest:** 37% / -42%
**Description:** Scale into QQQ oversold dips, exit on RSI recovery
**Entry:** TQQQ / SOXL / TECL weight = n/3 RSI(2) thresholds QQQ is below (30 / 25 / 20)
**Exit:** RSI recovers above all thresholds

---

## 4. SMA200 RSI Tiers
**Type:** Trend
**Backtest:** 33% / -50%
**Description:** Hold TQQQ above trend, scale up on dips and trim on overbought
**Entry:** TQQQ > SMA(200) → 50% base; RSI(2) < 30 → 100%; RSI(14) > 70 → trim to 20%
**Exit:** TQQQ < SMA(200)

---

## 5. SMA200 Pyramid
**Type:** Trend
**Backtest:** 32% / -49%
**Description:** Enter on trend, add size as price rises, exit on trend break
**Entry:** QQQ > SMA(200) → 50% TQQQ; +15% per 5% gain above entry, cap 100%; de-pyramids on pullback
**Exit:** QQQ < SMA(200)

---

## 6. SMA Five Vote
**Type:** Trend
**Backtest:** 36% / -43%
**Description:** Weight position by how many timeframes agree on uptrend
**Entry:** TQQQ weight = n/8 SMAs QQQ is above (20 / 50 / 100 / 150×4 / 200)
**Exit:** Weight falls to 0 as price drops below each SMA

---

## 7. Donchian Five Vote
**Type:** Trend
**Backtest:** 35% / -55%
**Description:** Weight position by how many channel midlines are cleared
**Entry:** TQQQ weight = n/5 Donchian midlines QQQ is above (50 / 100 / 150 / 200 / 250d)
**Exit:** Weight falls to 0 as price drops below midlines

---

## 8. Momentum Vote
**Type:** Momentum
**Backtest:** 36% / -37%
**Description:** Weight position by how many momentum signals are bullish
**Entry:** TQQQ weight = n/3 momentum signals bullish on QQQ (ROC(20) > 0 / up-days > 10 / TII(20) > 10)
**Exit:** All 3 bearish

---

## 9. Trend Stretch Exit
**Type:** Trend
**Backtest:** 43% / -54%
**Description:** Enter trend early when not yet stretched, exit when overstretched
**Entry:** QQQ > SMA(200) and price within 5% of SMA → 100% TQQQ
**Exit:** QQQ < SMA(200) or stretch > 20% above SMA

---

## 10. Golden Cross ATR
**Type:** Trend
**Backtest:** 37% / -52%
**Description:** Ride golden cross in calm markets, exit on cross flip or vol spike
**Entry:** QQQ EMA(50) > EMA(200) and 20d vol < 30% → 100% TQQQ
**Exit:** Death cross, vol > 30%, or 3×ATR(14) trailing stop

---

## 11. Range Compressed
**Type:** Range
**Backtest:** 34% / -45%
**Description:** Hold during quiet trending markets, avoid volatile expansions
**Entry:** QQQ > 200d median AND 25d range avg < 110% of 200d avg → 100%; one condition → 50%
**Exit:** Both false

---

## 12. MFI14 Hysteresis
**Type:** Volume
**Backtest:** 37% / -46%
**Description:** Hold through strong money inflow, sit out on outflow
**Entry:** QQQ MFI(14) > 60 → 100% TQQQ; hold between 40–60
**Exit:** MFI < 40

---

## 13. Vol Regime 20
**Type:** Volatility
**Backtest:** 34% / -46%
**Description:** Scale position inversely with realized volatility
**Entry:** 20d ann. vol < 20% → 100% TQQQ; vol 20–30% → 50% TQQQ
**Exit:** vol > 30%
