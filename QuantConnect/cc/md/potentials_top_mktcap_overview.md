# Top Market Cap Strategies — Overview

## 1. Giant Sniper Mean-Reversion
**Type:** Reversion
**Backtest:** 27% / -44% / 0.835
**Description:** Dip-buy each top-5 mega-cap on RSI(2) oversold, exit on RSI recovery or trend break
**Entry:** QQQ > SMA(200) AND per-name RSI(2) < 20 → equal-weight entry (all sectors top-5)
**Exit:** Per-name RSI(2) > 70 OR QQQ < SMA(200) → liquidate all

---

## 2. Mega-Cap Value Averaging
**Type:** Dip Buy
**Backtest:** 30% / -39% / 0.864
**Description:** Buy each mega-cap on 5% pullback from 20d high, sell into new high
**Entry:** Price < 20d high × 0.95 → 20% allocation per name (up to 5 names, 100% gross)
**Exit:** Price ≥ 20d high → liquidate

---

## 3. MktCap IBS Regime (drift)
**Type:** Hybrid
**Backtest:** 30% / -23% / 1.073
**Description:** Hold all top-5 mega-caps in uptrend, rotate into low-IBS dips only in downtrend
**Entry:** QQQ > SMA(200) → equal-weight top-5 (rebalance only on >5% drift); else → equal-weight IBS < 0.2 names
**Exit:** Name exits regime filter or universe

---

## 4. Nasdaq Breadth Rotation
**Type:** Breadth
**Backtest:** 29% / -48% / 0.700
**Description:** Hold TQQQ when majority of top-10 mega-caps trade above their EMA(50)
**Entry:** Fraction of top-10 above EMA(50) > 60% → 100% TQQQ
**Exit:** Fraction < 40% → liquidate

---

## 5. Mega-Cap Dispersion Regime
**Type:** Regime
**Backtest:** 39% / -46% / 0.892
**Description:** Hold top-5 mega-caps only when they trend in sync with low return dispersion
**Entry:** QQQ > D200 midline AND 20d return std dev across top-5 < 5% → equal-weight top-5
**Exit:** Trend breaks OR std dev ≥ 5% → cash

---

## 6. UpDnVol + 52w + Top3
**Type:** Multi-factor
**Backtest:** 31% / -44% / 0.754
**Description:** Score up/down vol ratio, 52w-high proximity, and trend for TQQQ/Top3/cash ladder
**Entry:** Score 3 → 100% TQQQ; 2 → 50% TQQQ + 50% Top3; 1 → 100% Top3; 0 → 50% Top3 + 50% cash
**Exit:** Score decreases on next daily check

---

## 7. Mom20 + 52w + Top3
**Type:** Multi-factor
**Backtest:** 33% / -45% / 0.802
**Description:** Score trend median, ROC(20) momentum, and 52w-high proximity for TQQQ/Top3/cash ladder
**Entry:** Score 3 → 100% TQQQ; 2 → 50% TQQQ + 50% Top3; 1 → 100% Top3; 0 → 50% Top3 + 50% cash
**Exit:** Score decreases on next daily check

---

## 8. M252 + NEAR60 + VolContr + Top3
**Type:** Multi-factor
**Backtest:** 31% / -50% / 0.752
**Description:** 252d momentum + 60d-high proximity + vol contraction for 5-level TQQQ/Top3/cash ladder
**Entry:** n=4 → 100% TQQQ; n=3 → 70% TQQQ/30% Top3; n=2 → 30%/70%; n=1 → 50% Top3/cash; n=0 → cash
**Exit:** Score n drops on next daily check

---

## 9. OBV + CCI
**Type:** Volume
**Backtest:** 31% / -29% / 0.831
**Description:** OBV trend + CCI gate routes between TQQQ, top-5 mega-caps, and cash
**Entry:** OBV(20)-up AND CCI(20) > 0 → 100% TQQQ; one signal → equal-weight top-5; neither → cash
**Exit:** OBV-down OR CCI < -100 → cash

---

## 10. OBV + ADX
**Type:** Volume
**Backtest:** 31% / -33% / 0.864
**Description:** OBV trend + ADX directional strength routes between TQQQ, top-5 mega-caps, and cash
**Entry:** OBV(20)-up AND +DI > -DI → 100% TQQQ; one signal → equal-weight top-5; ADX bear → cash
**Exit:** OBV-down OR (ADX(14) > 25 AND -DI > +DI) → cash

---

## 11. Tech Dip Buy
**Type:** Dip Buy
**Backtest:** 28% / -40% / 0.856
**Description:** Weekly dip-buy on top-5 Morningstar tech mega-caps above SMA(50), exit on 52w high or stop
**Entry:** RSI(2) < 30 AND price > SMA(50) → 20% allocation per tech name
**Exit:** Price ≥ 252d high (take profit) OR price ≤ avg cost × 0.85 (stop loss)

---

## 12. MktCap IBS Regime
**Type:** Hybrid
**Backtest:** 27% / -26% / 0.981
**Description:** Hold all top-5 mega-caps in uptrend, buy only low-IBS dips in downtrend
**Entry:** QQQ > SMA(200) → equal-weight top-5; else → equal-weight IBS < 0.2 names only
**Exit:** Name exits regime filter or universe

---

## Yearly Returns

| # | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 🟢 15% | 🟢 49% | 🔴 -13% | 🟢 48% | 🔴 -16% | 🟢 7% | 🟢 34% | 🟢 80% | 🔴 -10% | 🟢 43% | 🟢 40% | 🟢 94% |
| 2 | 🟢 22% | 🟢 16% | 🟢 14% | 🟢 49% | 🔴 -4% | 🟢 61% | 🟢 57% | 🟢 50% | 🔴 -34% | 🟢 76% | 🟢 75% | 🟢 28% |
| 3 | 🟢 11% | 🟢 5% | 🟢 4% | 🟢 38% | 🟢 15% | 🟢 47% | 🟢 95% | 🟢 46% | 🔴 -11% | 🟢 51% | 🟢 38% | 🟢 50% |
| 4 | 🟢 11% | 🟢 2% | 🔴 -7% | 🟢 118% | 🔴 -29% | 🟢 33% | 🟢 108% | 🟢 53% | 🔴 -34% | 🟢 73% | 🟢 46% | 🟢 95% |
| 5 | 🟢 37% | 🟢 38% | 🔴 -6% | 🟢 118% | 🔴 -6% | 🟢 110% | 🟢 15% | 🟢 158% | 🔴 -40% | 🟢 106% | 🟢 60% | 🟢 18% |
| 6 | 🟢 33% | 🟢 10% | 🔴 -8% | 🟢 93% | 🔴 -22% | 🟢 72% | 🟢 96% | 🟢 50% | 🔴 -26% | 🟢 117% | 🟢 37% | 🟢 10% |
| 7 | 🟢 39% | 🟢 7% | 🔴 -7% | 🟢 106% | 🔴 -22% | 🟢 72% | 🟢 133% | 🟢 60% | 🔴 -36% | 🟢 103% | 🟢 47% | 🟢 17% |
| 8 | 🟢 38% | 🟢 11% | 🔴 -15% | 🟢 102% | 🔴 -4% | 🟢 49% | 🟢 151% | 🟢 60% | 🔴 -46% | 🟢 105% | 🟢 41% | 🟢 11% |
| 9 | 🟢 2% | 🔴 -4% | 🔴 -2% | 🟢 37% | 🔴 -4% | 🟢 95% | 🟢 156% | 🟢 25% | 🟢 14% | 🟢 116% | 🟢 7% | 🟢 23% |
| 10 | 🟢 11% | 🔴 -15% | 🔴 -7% | 🟢 43% | 🟢 5% | 🟢 78% | 🟢 209% | 🟢 22% | 🟢 12% | 🟢 98% | 🟢 5% | 🟢 31% |
| 11 | 🟢 19% | ⚪ 0% | 🟢 7% | 🟢 37% | 🟢 6% | 🟢 40% | 🟢 39% | 🟢 52% | 🔴 -34% | 🟢 98% | 🟢 100% | 🟢 32% |
| 12 | 🟢 10% | 🟢 6% | ⚪ 0% | 🟢 37% | 🟢 10% | 🟢 44% | 🟢 89% | 🟢 44% | 🔴 -14% | 🟢 52% | 🟢 39% | 🟢 41% |
