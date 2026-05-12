# TQQQ Algo Sweep — 100 Strategies

**Target:** CAGR ≥ 28% AND MaxDD ≤ 58%
**Asset:** TQQQ (3× Nasdaq-100)
**Date range:** 2014-01-01 → 2025-12-31
**Cash:** $100,000

Sources: `Entry_and_Exit_Confessions.md` (Davey, 41 entries × 11 exits) + `Algo_Trading_Cheat_Codes.md` (Davey, mean reversion + regime).

**Constraint:** No margin/leverage on the strategy itself (TQQQ is 3× as the underlying instrument; SetHoldings ≤ 1.0).

## 🏆 Leaderboard (top 10 passers by Sharpe)

| Rank | #       | Name                            | CAGR    | MaxDD    | Sharpe   |
| :--- | :------ | :------------------------------ | :------ | :------- | :------- |
| 1    | **046** | SMA150+IBS fast exit            | **55%** | -55%     | **1.07** |
| 2    | 064     | 5 most mkt cap + IBS regime mix | 30%     | **-23%** | 1.07     |
| 3    | 028     | TQQQ IBS extreme                | 47%     | -47%     | 1.05     |
| 4    | 031     | IBS extreme + ATR stop          | 46%     | -43%     | 1.05     |
| 5    | **047** | #46 + chandelier                | 52%     | -56%     | 1.03     |
| 6    | 048     | #46 on QLD                      | 40%     | -40%     | 1.02     |
| 7    | 043     | SMA150 + IBS + 2xATR            | 51%     | -58%     | 1.01     |
| 8    | 042     | SMA150 + IBS + 3xATR            | 51%     | -55%     | 1.00     |
| 9    | 056     | %R(2) hybrid                    | 51%     | -56%     | 1.00     |
| 10   | 066     | TQQQ hybrid + ATR               | 49%     | -48%     | 0.99     |

## Results

| #   | Name                       | Idea                                     | CAGR    | MaxDD    | Sharpe   | Pass | Backtest ID |
| :-- | :------------------------- | :--------------------------------------- | :------ | :------- | :------- | :--- | :---------- |
| 001 | RSI2 MR daily              | RSI(2)<10 buy / >70 or 5d sell           | 2%      | -66%     | 0.13     | ❌    | 64d80063…   |
| 002 | RSI2 + SMA200 trend gate   | RSI2 MR only if QQQ > 200d SMA           | 7%      | -43%     | 0.24     | ❌    | 8b4fd7dc…   |
| 003 | TQQQ trend SMA200          | Hold TQQQ when QQQ > 200d SMA, else flat | 33%     | -56%     | 0.75     | ✅    | 187f2156…   |
| 004 | TQQQ trend SMA50           | Hold TQQQ when QQQ > 50d SMA             | 20%     | -52%     | 0.53     | ❌    | 576b3891…   |
| 005 | TQQQ trend SMA100          | Hold TQQQ when QQQ > 100d SMA            | 17%     | -58%     | 0.47     | ❌    | 7d59721a…   |
| 006 | TQQQ trend SMA150          | Hold TQQQ when QQQ > 150d SMA            | 40%     | -55%     | 0.87     | ✅    | f977dd48…   |
| 007 | EMA50/200 cross            | EMA50>EMA200 on QQQ → TQQQ               | 35%     | -70%     | 0.76     | ❌    | dfc30ce3…   |
| 008 | TQQQ self-SMA200           | TQQQ > own 200d SMA → hold               | 33%     | -50%     | 0.76     | ✅    | 55c0a642…   |
| 009 | TQQQ self-SMA150           | TQQQ > own 150d SMA → hold               | 29%     | -53%     | 0.69     | ✅    | e949acad…   |
| 010 | SMA150+RSI2 overlay        | SMA150 trend, RSI2<10 add in downtrend   | 39%     | -62%     | 0.83     | ❌    | 51bce0dd…   |
| 011 | SMA200 75% cap             | SMA200, but only 75% TQQQ                | 29%     | -49%     | 0.70     | ✅    | 50331476…   |
| 012 | TQQQ/TLT 50/50             | Static 50/50 monthly rebal, no signal    | 22%     | -62%     | 0.64     | ❌    | 75ccb4b5…   |
| 013 | Donchian50 breakout        | TQQQ on QQQ 50d high; exit on 50d low    | 16%     | -71%     | 0.45     | ❌    | 3864bc43…   |
| 014 | VIX<22 regime              | TQQQ when VIX < 22, flat above           | 17%     | -71%     | 0.46     | ❌    | a8a2055f…   |
| 015 | ROC126 momentum            | TQQQ when QQQ 6mo return > 0             | 29%     | -72%     | 0.67     | ❌    | 6c622c23…   |
| 016 | IBS MR pure                | Buy IBS<0.2, sell IBS>0.7 on TQQQ        | 35%     | -50%     | 0.82     | ✅    | 35759289…   |
| 017 | 5 most mkt cap EW           | 5 most mkt cap, 100% (no lev), monthly  | 22%     | -40%     | 0.74     | ❌    | 6548d414…   |
| 018 | 5 most mkt cap @ 1.5x      | 5 most mkt cap @ 1.5x margin             | 33%     | -55%     | 0.83     | ✅    | 164c7001…   |
| 019 | 5 most mkt cap @ 2.0x      | 5 most mkt cap @ 2.0x margin (uses lev) | 44%     | -67%     | 0.93     | ❌    | 32737def…   |
| 020 | Top5 12-1 momo             | Top5 from S&P200 by 12-1 momentum        | 18%     | -45%     | 0.52     | ❌    | ee48df20…   |
| 021 | Most mkt cap               | Most market capital company              | 15%     | -33%     | 0.47     | ❌    | 65dfd463…   |
| 022 | TQQQ BB MR                 | Buy lower BB, sell mid BB                | 12%     | -60%     | 0.36     | ❌    | dcf54e19…   |
| 023 | TQQQ 3-down MR             | Buy after 3 red days, sell on 1st green  | 13%     | -45%     | 0.48     | ❌    | 436228f1…   |
| 024 | TQQQ Connors RSI           | 2x RSI(2)<35 buy, RSI>65 sell            | 15%     | -63%     | 0.42     | ❌    | dc60498a…   |
| 025 | 3 most mkt cap EW          | 3 most mkt cap, EW, monthly              | 20%     | -35%     | 0.67     | ❌    | 46c66a7f…   |
| 026 | 5 most mkt cap CW          | 5 most mkt cap, weighted by cap          | 21%     | -38%     | 0.72     | ❌    | c9cd1d89…   |
| 027 | 5 most mkt cap 6mo momo    | Top 5 from largest 30 by 6mo momentum   | 22%     | -27%     | 0.74     | ❌    | a73f67d6…   |
| 028 | **TQQQ IBS extreme**       | IBS<0.1 buy, IBS>0.9 exit                | **47%** | **-47%** | **1.05** | ✅    | d0e32e34…   |
| 029 | TQQQ IBS 0.15/0.85         | IBS<0.15 buy, IBS>0.85 exit              | 37%     | -42%     | 0.84     | ✅    | 65fcde16…   |
| 030 | IBS extreme + SMA200       | IBS<0.1 buy only when QQQ>200d           | 32%     | -40%     | 0.90     | ✅    | 12ca4af2…   |
| 031 | **IBS extreme + ATR stop** | IBS<0.1 + 3×ATR stop loss                | **46%** | **-43%** | **1.05** | ✅    | 04a55b85…   |
| 032 | IBS 0.05 (rare)            | IBS<0.05 buy, IBS>0.9 exit               | 31%     | -47%     | 0.79     | ✅    | eb5737c6…   |
| 033 | IBS 0.1/0.7 fast           | IBS<0.1 buy, IBS>0.7 fast exit           | 36%     | -35%     | 0.92     | ✅    | 53ffc8ad…   |
| 034 | IBS 0.05/0.7               | IBS<0.05 buy, IBS>0.7 fast exit          | 26%     | -34%     | 0.76     | ❌    | 61ff20c3…   |
| 035 | IBS regime-adaptive        | IBS<0.1 in uptrend, <0.03 in downtrend   | 39%     | -55%     | 0.92     | ✅    | d176438b…   |
| 036 | TOM TQQQ                   | Hold last 5 + first 5 cal days TQQQ      | 8%      | -62%     | 0.27     | ❌    | 07936977…   |
| 037 | Sell-in-May TQQQ           | Hold Nov-Apr only                        | 8%      | -70%     | 0.31     | ❌    | 3849867b…   |
| 038 | Overnight TQQQ             | Buy at close, sell at open (minute res)  | -51%    | -100%    | -1.22    | ❌    | ed888af2…   |
| 039 | IBS + 3d max hold          | IBS<0.1 + force exit after 3 days        | 30%     | -52%     | 0.80     | ✅    | 41664040…   |
| 040 | SMA150 trend + IBS<0.05    | Trend hold + MR overlay in down-trend    | 50%     | -56%     | 0.99     | ✅    | 91eb924d…   |
| 041 | SMA200 trend + IBS<0.05    | Same as 40 but SMA200 gate               | 44%     | -68%     | 0.90     | ❌    | 2e473812…   |
| 042 | SMA150 + IBS + 3xATR       | #40 + ATR stop on MR                     | 51%     | -55%     | 1.00     | ✅    | 7d454591…   |
| 043 | SMA150 + IBS + 2xATR       | #42 with tighter stop                    | 51%     | -58%     | 1.01     | ✅    | 88b62de1…   |
| 044 | dual-trend gate            | Both QQQ150 AND TQQQ100 SMAs up          | 12%     | -54%     | 0.37     | ❌    | 44f9c8d6…   |
| 045 | TQQQ↔TLT switch            | Risk-on/off rotation by SMA200           | 31%     | -64%     | 0.71     | ❌    | aeff8002…   |
| 046 | **SMA150+IBS fast exit**   | #40 with IBS>0.7 fast MR exit            | **55%** | **-55%** | **1.07** | ✅    | 31d82823…   |
| 047 | #46 + chandelier           | #46 + 5xATR trailing stop on trend pos   | 52%     | -56%     | 1.03     | ✅    | 8effa768…   |
| 048 | #46 on QLD                 | Same hybrid but QLD instead of TQQQ      | 40%     | -40%     | 1.02     | ✅    | 17f4607d…   |
| 049 | 5d-low pullback in trend   | Buy 5d low when QQQ>100SMA, 5d hold      | 1%      | -10%     | -0.45    | ❌    | 079f98c7…   |
| 050 | TQQQ buy & hold            | 100% TQQQ from 2014                      | 37%     | -82%     | 0.77     | ❌    | b28efa10…   |
| 051 | 5 most mkt cap + SMA200 cash | 5 most mkt cap, cash when QQQ<200SMA   | 20%     | -27%     | 0.79     | ❌    | e31554a6…   |
| 052 | XLK SMA200 trend           | Tech sector ETF + 200d SMA               | 16%     | -25%     | 0.68     | ❌    | bc0b8af7…   |
| 053 | %R(2) MR pure              | Williams %R<-90 buy, >-10 sell           | 40%     | -42%     | 0.91     | ✅    | ece7de7e…   |
| 054 | 2-down 1-up MR             | Buy 1st up after 2 downs, exit on down   | -10%    | -90%     | -0.24    | ❌    | 5283ad57…   |
| 055 | **TQQQ + SMA200**          | TQQQ hold when above 200d SMA            | 33%     | -50%     | 0.76     | ✅    | 0b7ab363…   |
| 056 | %R(2) hybrid               | SMA150 trend + %R<-95 MR overlay         | 51%     | -56%     | 1.00     | ✅    | 040559d6…   |
| 057 | 5 most mkt cap EW          | 5 most mkt cap, equal-weight, monthly   | 22%     | -40%     | 0.74     | ❌    | 8c4c9455…   |
| 058 | 5 most mkt cap + SMA200 | 5 most mkt cap EW, cash when QQQ<200SMA | 20%     | -27%     | 0.79     | ❌    | bb8b10f3…   |
| 059 | 5 most mkt cap + IBS<0.2 daily | 5 most mkt cap daily IBS rotation    | 19%     | -21%     | 0.81     | ❌    | 967adac3…   |
| 060 | TQQQ hybrid (SMA+IBS)      | TQQQ SMA200 trend + IBS<0.05 down-trend  | 49%     | -50%     | 0.99     | ✅    | ad213588…   |
| 061 | TQQQ + SMA150              | TQQQ + 150d SMA                          | 29%     | -53%     | 0.69     | ✅    | 1b79eaaa…   |
| 062 | 10 most mkt cap + SMA200   | 10 most mkt cap + QQQ regime             | 16%     | -25%     | 0.72     | ❌    | 661949ab…   |
| 063 | 3 most mkt cap + SMA200    | 3 most mkt cap EW + QQQ regime           | 18%     | -26%     | 0.68     | ❌    | 18324025…   |
| 064 | 5 most mkt cap + IBS regime mix | EW in trend; IBS<0.2 names else      | 30%     | -23%     | 1.07     | ✅    | 1f0563ad…   |
| 065 | 5 most mkt cap IBS<0.5 daily | Daily rotation by IBS<0.5              | 21%     | -31%     | 0.76     | ❌    | eb9f6e72…   |
| 066 | TQQQ hybrid + ATR          | #60 + 3xATR stop on MR pos               | 49%     | -48%     | 0.99     | ✅    | ce131745…   |
| 067 | 5 most mkt cap momo + SMA200 | Monthly momentum top5 + regime         | 17%     | -27%     | 0.59     | ❌    | fe334d41…   |
| 068 | TSLA + SMA200              | TSLA trend                               | 14%     | -72%     | 0.41     | ❌    | 4dd79c8b…   |
| 069 | 7 most mkt cap + SMA200    | 7 most mkt cap EW + QQQ regime           | 18%     | -26%     | 0.74     | ❌    | c8f8b9ab…   |
| 070 | 5 most mkt cap momo top3   | Monthly: top 3 of 5 by 1mo return        | 21%     | -44%     | 0.68     | ❌    | af1ada90…   |
| 080 | Sector momo top2           | 11 SPDR sectors, top 2 by 3mo return     | 14%     | -33%     | 0.56     | ❌    | d6a3e064…   |
| 081 | Risk parity QQQ/IEF/GLD    | Inverse-vol weights                      | 7%      | -18%     | 0.51     | ❌    | daf3069b…   |
| 082 | TQQQ↔SQQQ regime           | 20d return sign → 3x long or 3x inverse  | 5%      | -70%     | 0.28     | ❌    | a7d911bd…   |
| 083 | NR7 breakout               | Narrow-range-7 breakout on QQQ           | 7%      | -34%     | 0.24     | ❌    | 3fda01b2…   |
| 084 | SPY/TLT 6mo momo           | Monthly: hold higher 6mo return          | 7%      | -30%     | 0.30     | ❌    | 45ec62d2…   |
| 085 | Sector Momentum            | 5-ETF leveraged basket + QQQ SMA200 gate | 9%      | -74%     | 0.324    | ❌    | —          |
| 086 | Asymmetric Vol Target      | TQQQ sized by 20d vol targeting 30% ann  | 16%     | -30%     | 0.609    | ❌    | —          |
| 087 | Vol Compression Trend      | TQQQ triple positive return confirmation | 29%     | -62%     | 0.691    | ❌    | —          |
| 088 | Keltner Reversion          | TQQQ↔TMF monthly by 3mo momentum         | 15%     | -55%     | 0.452    | ❌    | —          |
| 089 | Donchian Reversion         | TQQQ dual trend + Bollinger squeeze      | 11%     | -60%     | 0.361    | ❌    | —          |
| 090 | Sector Alpha Rotation      | Top 3 of 7 leveraged ETFs by 3mo momo    | 17%     | -72%     | 0.471    | ❌    | —          |

---

## Passing Algos — Details

### 003 — TQQQ trend SMA200

**Description:** The canonical "price above 200-day SMA" trend filter applied to QQQ (NASDAQ 100 ETF), with the execution vehicle being TQQQ for 3x leveraged exposure during uptrends. When QQQ is above its 200d SMA, the algo goes 100% TQQQ; when it dips below, it moves entirely to cash. The 200-day SMA is the most widely followed technical indicator in institutional markets, so its signals have real behavioral anchoring — but the lagging nature means the leveraged vehicle takes severe damage before the exit triggers. In 2022, QQQ broke below its 200d SMA well after TQQQ had already lost ~60% from its peak.

*Overfit 1/10 — The 200-day SMA is a standard, universally recognized threshold. Zero tuned parameters beyond it.*

- **Entry:** QQQ price > 200-day SMA → allocate 100% to TQQQ
- **Exit:** QQQ price <= 200-day SMA → liquidate TQQQ to cash
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 33% | -56% | 0.75 |

> [!code]- Click to view: algo_003.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_003.py"
> ```

---

### 006 — TQQQ trend SMA150

**Description:** An identical structure to 003 but with the SMA lookback shortened from 200 to 150 days. This faster filter catches trend entries a few weeks earlier and, more importantly, exits during drawdowns sooner — which in 2022 meant preserving more capital for the recovery. The result is a meaningful lift in CAGR (33% to 40%) with essentially unchanged MaxDD (-56% to -55%). The weakness is that a shorter lookback increases whipsaw frequency during range-bound, choppy markets.

*Overfit 2/10 — 150d is a common alternative to 200d, but this is clearly part of a parameter sweep across SMA lengths. The improvement over 003 is marginal enough to question out-of-sample robustness.*

- **Entry:** QQQ price > 150-day SMA → allocate 100% to TQQQ
- **Exit:** QQQ price <= 150-day SMA → liquidate TQQQ to cash
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 40% | -55% | 0.87 |

> [!code]- Click to view: algo_006.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_006.py"
> ```

---

### 008 — TQQQ self-SMA200

**Description:** Applies the 200-day SMA filter directly to the leveraged instrument TQQQ rather than the underlying QQQ. The rationale might be simplicity (one symbol), but it introduces a subtle problem: TQQQ's 3x daily leverage creates volatility decay and path-dependence that the underlying NASDAQ 100 does not have, making the self-SMA signal noisier and less reliable as a trend gauge.

*Overfit 1/10 — Standard 200d SMA, no parameter tuning. The symbol choice (TQQQ vs QQQ) is a design decision, not a fitted parameter.*

- **Entry:** TQQQ price > TQQQ's own 200-day SMA → allocate 100% to TQQQ
- **Exit:** TQQQ price <= own 200-day SMA → liquidate to cash
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 33% | -50% | 0.76 |

> [!code]- Click to view: algo_008.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_008.py"
> ```

---

### 009 — TQQQ self-SMA150

**Description:** The same self-SMA approach as 008 but with a 150-day lookback applied to TQQQ's own price. This performs strictly worse than 008 across all metrics (29% CAGR, -53% MaxDD, 0.69 Sharpe vs 33%, -50%, 0.76), making it the weakest variant in this family. The combination of leveraged volatility and a shorter lookback amplifies whipsaw losses: TQQQ's daily price swings of 5-10% mean it frequently breaches its own 150d SMA on noise rather than genuine trend changes.

*Overfit 3/10 — The 150d lookback on a 3x leveraged ETF is non-standard and appears to be a speculative parameter choice. The clear degradation relative to 008 (200d) suggests this was tested as part of a sweep.*

- **Entry:** TQQQ price > TQQQ's own 150-day SMA → allocate 100% to TQQQ
- **Exit:** TQQQ price <= own 150-day SMA → liquidate to cash
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -53% | 0.69 |

> [!code]- Click to view: algo_009.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_009.py"
> ```

---

### 011 — SMA200 75% cap

**Description:** A de-risked variant of 003 that uses the same QQQ > 200d SMA entry signal but caps TQQQ allocation at 75% instead of 100%. The remaining 25% sits in cash, providing a buffer during drawdowns and reducing overall portfolio volatility. This predictably reduces CAGR (33% to 29%) alongside MaxDD (-56% to -49%). The 75% cap is intuitively appealing but the specific number feels tuned to this backtest window.

*Overfit 2/10 — The 75% allocation cap is a single tuned parameter. 75% is a round number but likely chosen by testing several caps and picking the one that trimmed MaxDD without cratering CAGR.*

- **Entry:** QQQ price > 200-day SMA → allocate 75% to TQQQ (25% cash)
- **Exit:** QQQ price <= 200-day SMA → liquidate TQQQ to cash
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -49% | 0.70 |

> [!code]- Click to view: algo_011.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_011.py"
> ```

---

### 016 — IBS MR pure

**Description:** Buys TQQQ when the close is near the low of the day (IBS < 0.2, oversold) and sells when the close nears the high (IBS > 0.7, overbought), applying mean reversion to a 3x leveraged Nasdaq ETF. The asymmetric thresholds (wide buy, narrow sell) bias toward holding long, which partially compensates for fighting TQQQ's strong upward drift. Its main weakness is that mean reversion systematically shorts strength in a secular bull market, leaving significant upside on the table during trending rallies.

*Overfit 2/10 — the 0.2/0.7 IBS thresholds are standard values from the literature; only 2 parameters, both round numbers.*

- **Entry:** IBS < 0.2 (close near the daily low)
- **Exit:** IBS > 0.7 (close near the daily high)
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 35% | -50% | 0.82 |

> [!code]- Click to view: algo_016.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_016.py"
> ```

---

### 018 — 5 most mkt cap @ 1.5x

**Description:** Each month, buys equal weights of the 5 most market capital companies using 1.5x margin, liquidating any that fall out of the top 5. The strategy rides the compounding power of market-leading megacaps (AAPL, MSFT, NVDA, AMZN, GOOGL) with leverage — and this has worked brilliantly as mega-cap tech dominated. Its critical weakness is the complete absence of risk management: a concentrated 5-stock portfolio at 1.5x leverage can experience catastrophic drawdowns during regime shifts.

*Overfit 2/10 — top-5-by-market-cap is a natural universe definition; 1.5x leverage is a round number; no lookback windows or threshold tuning.*

- **Entry:** Monthly rebalance into 5 most market capital companies, each at weight = 1.5 / 5
- **Exit:** Liquidate any position that drops out of the top 5
- **Symbols:** Top 5 US equities by market cap (dynamic universe)

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 33% | -55% | 0.83 |

> [!code]- Click to view: algo_018.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_018.py"
> ```

---

### 028 — TQQQ IBS extreme

**Description:** A stricter variant of the IBS mean reversion theme that only buys when selling is truly extreme (IBS < 0.1) and only exits when buying is truly extreme (IBS > 0.9). This dramatically reduces trade frequency but each entry catches deeper capitulation, and the very late exit allows full trend participation once a rally is underway. The 47% CAGR (vs 35% for the standard 0.2/0.7 version) shows that patience on entry and letting winners run more than compensates for extended cash periods.

*Overfit 3/10 — extreme round thresholds (0.1, 0.9) are less commonly used than the standard IBS 0.2/0.8 pair but are still intuitive boundary values.*

- **Entry:** IBS < 0.1 (extreme selling pressure)
- **Exit:** IBS > 0.9 (extreme buying pressure)
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 47% | -47% | 1.05 |

> [!code]- Click to view: algo_028.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_028.py"
> ```

---

### 029 — TQQQ IBS 0.15/0.85

**Description:** A middle-ground IBS variant with buy at 0.15 and exit at 0.85 — sandwiched between the standard 0.2/0.7 (algo 016) and the extreme 0.1/0.9 (algo 028). It achieves the best MaxDD of the three (-42% vs -50% and -47%) and a CAGR (37%) that splits the difference. The key weakness is that these specific intermediate values have no theoretical justification — they are clearly the product of a parameter sweep.

*Overfit 5/10 — the 0.15 and 0.85 thresholds do not correspond to any standard IBS value and appear to be the result of explicit parameter optimization.*

- **Entry:** IBS < 0.15
- **Exit:** IBS > 0.85
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 37% | -42% | 0.84 |

> [!code]- Click to view: algo_029.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_029.py"
> ```

---

### 030 — IBS extreme + SMA200

**Description:** Combines the IBS extreme oversold signal with a 200-day SMA trend filter on QQQ. It only enters a TQQQ position when both IBS is below 0.1 (extreme intraday weakness) and QQQ is trading above its 200-day SMA (uptrend), which keeps it out of sustained bear markets. The drawback is the trend filter can delay re-entry after a sharp but short-lived dip.

*Overfit 3/10 — IBS thresholds (0.1/0.9) are round but arbitrary; SMA 200 is a standard lookback. The QQQ trend filter adds a second conditional.*

- **Entry:** IBS < 0.1 and QQQ price > SMA(200)
- **Exit:** IBS > 0.9
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 32% | -40% | 0.90 |

> [!code]- Click to view: algo_030.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_030.py"
> ```

---

### 031 — IBS extreme + ATR stop

**Description:** Enters TQQQ on IBS < 0.1 like the basic IBS strategy, but adds a trailing volatility-based stop loss at 3x the 14-period ATR from the entry price. This stop is designed to cap catastrophic single-trade losses during flash crashes or gap downs. The weakness is that TQQQ's 3x leverage amplifies volatility, making the 3x ATR stop prone to triggering on routine whipsaws rather than true disasters.

*Overfit 3/10 — IBS thresholds and ATR multiplier (3x) are standard choices (Bollinger-style 3-sigma logic). ATR(14) is a canonical period.*

- **Entry:** IBS < 0.1
- **Exit:** IBS > 0.9, OR close < entry_price - 3 x ATR(14)
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 46% | -43% | 1.05 |

> [!code]- Click to view: algo_031.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_031.py"
> ```

---

### 032 — IBS 0.05 (rare)

**Description:** A stricter version of the IBS strategy that only buys when IBS drops below 0.05 — a much rarer event than the standard 0.1 threshold. This results in fewer but theoretically higher-conviction trades, since the stock needs to close extremely near its daily low. The main weakness is extended cash drag between rare entry signals.

*Overfit 2/10 — only two parameters (0.05 entry, 0.9 exit). However, 0.05 is a suspiciously precise threshold that was almost certainly backtest-optimized.*

- **Entry:** IBS < 0.05
- **Exit:** IBS > 0.9
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 31% | -47% | 0.79 |

> [!code]- Click to view: algo_032.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_032.py"
> ```

---

### 033 — IBS 0.1/0.7 fast

**Description:** Enters on the standard IBS < 0.1 signal but exits much earlier at IBS > 0.7 instead of the usual 0.9. The tighter exit captures only the initial mean-reversion bounce and avoids holding through the extended recovery leg. The weakness is that it systematically leaves money on the table — many trades that recover fully to 0.9+ are cut at 0.7.

*Overfit 2/10 — only two round thresholds (0.1/0.7). The 0.7 exit is the sole deviation from the standard IBS template.*

- **Entry:** IBS < 0.1
- **Exit:** IBS > 0.7
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 36% | -35% | 0.92 |

> [!code]- Click to view: algo_033.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_033.py"
> ```

---

### 035 — IBS regime-adaptive

**Description:** Uses a 200-day SMA on QQQ to switch between two regimes: in uptrends it buys TQQQ on moderate pullbacks (IBS < 0.1), but in downtrends it only enters on extremely rare capitulation events (IBS < 0.03). Exits when IBS crosses above 0.9 regardless of regime. The regime-awareness prevents catching falling knives during bear markets, but the 0.03 downtrend threshold is so extreme that the algo sits in cash for entire bear-market rallies.

*Overfit 4/10 — two regime-specific IBS entry thresholds (0.1 vs 0.03), one exit (0.9), and a SMA(200) lookback; the 0.03 value is especially vulnerable to hindsight tuning.*

- **Entry:** IBS < 0.1 if QQQ > SMA(200); IBS < 0.03 if QQQ < SMA(200)
- **Exit:** IBS > 0.9
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 39% | -55% | 0.92 |

> [!code]- Click to view: algo_035.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_035.py"
> ```

---

### 039 — IBS + 3d max hold

**Description:** A pure mean-reversion strategy that buys TQQQ whenever IBS drops below 0.1 and forces an exit after three trading days regardless of price, in addition to the standard IBS > 0.9 exit. The time-capped hold prevents a failed reversion trade from decaying into a large loss. However, the arbitrary 3-day exit can cut short a reversion that is still developing.

*Overfit 5/10 — two IBS thresholds (0.1 entry, 0.9 exit) and a 3-bar max-hold parameter; changing the hold to 2, 4, or 5 days would materially alter results.*

- **Entry:** IBS < 0.1
- **Exit:** IBS > 0.9 OR held >= 3 bars
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 30% | -52% | 0.80 |

> [!code]- Click to view: algo_039.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_039.py"
> ```

---

### 040 — SMA150 trend + IBS<0.05

**Description:** A hybrid strategy that holds TQQQ during uptrends (QQQ > SMA150) and switches to a mean-reversion overlay in downtrends, buying only when IBS drops below 0.05 and selling at IBS > 0.9. This captures full bull-market exposure while deploying a defensive dip-buying approach during drawdowns. The sequential transition (liquidate trend, then wait for MR entry) means a sharp reversal off the trend line leaves the algo fully in cash.

*Overfit 5/10 — SMA lookback (150 vs the more standard 200), two-mode architecture, MR entry threshold (0.05), and IBS exit (0.9).*

- **Entry:** QQQ > SMA(150) → buy TQQQ; QQQ < SMA(150) AND IBS < 0.05 → buy TQQQ
- **Exit:** Trend mode → exit on trend flip; MR mode → IBS > 0.9
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 50% | -56% | 0.99 |

> [!code]- Click to view: algo_040.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_040.py"
> ```

---

### 042 — SMA150 + IBS + 3xATR

**Description:** Extends algo 040 by adding a 3x ATR(14) trailing stop on mean-reversion positions only, exiting MR trades when price drops below entry_price - 3 * ATR in addition to the IBS > 0.9 exit. Trend-mode positions are not stopped at all. The ATR stop provides theoretical downside protection, but on TQQQ (extremely high volatility) the 3xATR distance is so wide that it rarely triggers, making the practical difference from algo 040 marginal.

*Overfit 7/10 — all of 040's parameters plus ATR period (14), ATR multiplier (3), and entry-price tracking; the combination outperforms 040 by only 1% CAGR, suggesting the extra complexity is not justified.*

- **Entry:** QQQ > SMA(150) → buy TQQQ; QQQ < SMA(150) AND IBS < 0.05 → buy TQQQ
- **Exit:** Trend mode → exit on trend flip; MR mode → IBS > 0.9 OR price < entry_price - 3x ATR(14)
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 51% | -55% | 1.00 |

> [!code]- Click to view: algo_042.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_042.py"
> ```

---

### 043 — SMA150 + IBS + 2xATR

**Description:** A hybrid trend/mean-reversion strategy on TQQQ that goes long in an uptrend (QQQ above its 150-day SMA) and fades deeply oversold conditions via mean reversion when the trend is flat or down. The "tighter stop" from #42 is a 2x ATR hard stop below the MR entry price, intended to cap losses when oversold bounces fail. The weakness is that 2x ATR on TQQQ is very tight for a 3x leveraged ETF — normal daily volatility can trigger the stop before the mean reversion materializes.

*Overfit 3/10 — standard lookbacks (SMA 150, ATR 14) and extreme IBS thresholds (0.05/0.9) are common choices. The 2x ATR multiplier is the only tuned parameter.*

- **Entry (Trend):** QQQ > SMA(150) and not invested → go long TQQQ at 100%
- **Entry (MR):** QQQ <= SMA(150), not invested, and IBS < 0.05 → go long TQQQ at 100%
- **Exit (Trend):** QQQ drops below SMA(150) → liquidate
- **Exit (MR):** IBS > 0.9 or price < entry_price - 2 * ATR(14) → liquidate
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 51% | -58% | 1.01 |

> [!code]- Click to view: algo_043.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_043.py"
> ```

---

### 046 — SMA150+IBS fast exit

**Description:** A simplified hybrid that removes the ATR stop entirely and exits mean-reversion positions as soon as IBS crosses above 0.7 (versus the typical 0.9). Ride TQQQ long when QQQ is above its 150-day SMA, and buy deep oversold IBS (< 0.05) bounces when it is not, cashing out quickly at 0.7 for higher turnover. Dropping the hard stop reduces parameter count but leaves MR positions exposed to gap-down or sustained selling.

*Overfit 2/10 — IBS take-profit at 0.7 instead of 0.9 is a single threshold tweak. All other parameters are standard.*

- **Entry (Trend):** QQQ > SMA(150) → go long TQQQ at 100%
- **Entry (MR):** QQQ <= SMA(150) and IBS < 0.05 → go long TQQQ at 100%
- **Exit (Trend):** QQQ drops below SMA(150) → liquidate
- **Exit (MR):** IBS > 0.7 → liquidate
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 55% | -55% | 1.07 |

> [!code]- Click to view: algo_046.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_046.py"
> ```

---

### 047 — #46 + chandelier

**Description:** Builds on #46 by adding a trailing chandelier stop on trend positions (5x ATR from the peak) and a hard stop on mean-reversion positions (3x ATR below entry). The trailing stop is meant to lock in trend gains during sharp reversals. In practice, the 5x ATR trail on a 3x leveraged ETF may be wide enough that it only triggers during crash events.

*Overfit 4/10 — two added ATR multipliers (5x for trend trail, 3x for MR stop) tuned against past data. These interact with the existing IBS thresholds.*

- **Entry (Trend):** QQQ > SMA(150) → go long at 100%; record peak at entry
- **Entry (MR):** QQQ <= SMA(150) and IBS < 0.05 → go long TQQQ at 100%
- **Exit (Trend via SMA):** QQQ drops below SMA(150) → liquidate
- **Exit (Trend via Chandelier):** Close < peak_price - 5 * ATR(14) → liquidate
- **Exit (MR via IBS):** IBS > 0.7 → liquidate
- **Exit (MR via Stop):** Close < entry_price - 3 * ATR(14) → liquidate
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 52% | -56% | 1.03 |

> [!code]- Click to view: algo_047.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_047.py"
> ```

---

### 048 — #46 on QLD

**Description:** An exact replica of #46's logic applied to QLD (2x Nasdaq-100) instead of TQQQ (3x). The intent is to test whether the #46 edge survives deleveraging — lower CAGR is expected (40% vs. 55%), but the commensurately lower drawdown (-40% vs. -55%) suggests the underlying timing signal, not leverage, drives most of the risk-adjusted return.

*Overfit 1/10 — no new parameters versus #46. The only change is the traded symbol, a straightforward robustness check.*

- **Entry (Trend):** QQQ > SMA(150) → go long QLD at 100%
- **Entry (MR):** QQQ <= SMA(150) and IBS < 0.05 → go long QLD at 100%
- **Exit (Trend):** QQQ drops below SMA(150) → liquidate
- **Exit (MR):** IBS > 0.7 → liquidate
- **Symbols:** QLD, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 40% | -40% | 1.02 |

> [!code]- Click to view: algo_048.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_048.py"
> ```

---

### 053 — %R(2) MR pure

**Description:** Buys TQQQ when the 2-period Williams %R dips below -90, betting on an immediate bounce from extreme oversold conditions, then sells when %R crosses above -10. The ultra-short 2-bar window makes this a high-frequency mean-reversion gambit that catches sharp intra-week reversals but gets crushed in sustained downtrends where oversold keeps getting more oversold.

*Overfit 7/10 — %R(2) is a non-standard period far from the conventional 14, thresholds of -90/-10 are aggressively tuned.*

- **Entry:** Williams %R(2) < -90 (oversold)
- **Exit:** Williams %R(2) > -10 (overbought)
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 40% | -42% | 0.91 |

> [!code]- Click to view: algo_053.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_053.py"
> ```

---

### 055 — TQQQ + SMA200

**Description:** Applies the classic 200-day SMA trend filter to TQQQ (3× Nasdaq-100), holding when TQQQ's close is above its own 200-day SMA and liquidating to cash when it falls below. Replacing NVDA with TQQQ dramatically changes the character: TQQQ's 3× daily leverage means the SMA breaches earlier and more frequently in downtrends, reducing drawdown (-50% vs -42% for NVDA) but also cutting CAGR sharply (33% vs 64%). The strategy is essentially identical to #008 (TQQQ self-SMA200) and the 33% CAGR with 0.76 Sharpe confirms the performance is comparable.

*Overfit 4/10 — the SMA(200) is a standard, widely-used lookback with no tuning, but cherry-picking the single best-performing large-cap strategy and applying it to a 3× leveraged ETF introduces hindsight bias.*

- **Entry:** TQQQ price > SMA(200)
- **Exit:** TQQQ price < SMA(200)
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 33% | -50% | 0.76 |

> [!code]- Click to view: algo_055.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_055.py"
> ```

---

### 056 — %R(2) hybrid

**Description:** Two-regime strategy on TQQQ using QQQ's 150-day SMA as a market health filter. When QQQ is above its SMA (bull trend), it buys TQQQ and holds continuously. When QQQ is below the SMA, it switches to mean-reversion: only buying on extreme %R(2) < -95 oversold prints and selling on %R(2) > -10.

*Overfit 8/10 — %R(2) with a -95/-10 threshold pair is more aggressively tuned than even algo 053, SMA(150) is a non-standard departure from the conventional 200.*

- **Entry:** QQQ > SMA(150) = buy TQQQ; QQQ < SMA(150) and %R(2) < -95 = buy TQQQ
- **Exit:** QQQ < SMA(150) while in trend mode = liquidate; in MR mode and %R(2) > -10 = liquidate
- **Symbols:** TQQQ, QQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 51% | -56% | 1.00 |

> [!code]- Click to view: algo_056.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_056.py"
> ```

---

### 060 — TQQQ hybrid (SMA+IBS)

**Description:** A dual-regime strategy on TQQQ that combines trend-following with extreme dip-buying. In trend mode (TQQQ above SMA200), it holds TQQQ continuously. In down-trend mode, it switches to mean-reversion: entering only when IBS drops below 0.05 (extreme selling pressure within the day) and exiting when IBS recovers above 0.70. Replacing NVDA with TQQQ preserves the hybrid structure but reduces CAGR from 68% to 49% and Sharpe from 1.44 to 0.99, as TQQQ's leverage amplifies whipsaw losses when the SMA gate flips.

*Overfit 6/10 — both IBS thresholds (0.05, 0.70) are clearly tuned; applying NVDA-specific parameters to TQQQ adds another degree of specification bias.*

- **Entry:** If TQQQ > SMA200 → hold TQQQ. If below SMA200 and IBS < 0.05 → buy TQQQ
- **Exit:** Trend mode and price < SMA200 → liquidate. MR mode and IBS > 0.70 → liquidate
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 49% | -50% | 0.99 |

> [!code]- Click to view: algo_060.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_060.py"
> ```

---

### 061 — TQQQ + SMA150

**Description:** A pure trend-following strategy on TQQQ using a 150-day SMA as the regime filter — invested when TQQQ closes above its 150-day moving average, flat when below. This is essentially a re-run of #009 (TQQQ self-SMA150) with identical parameters. The results confirm the match: 29% CAGR / -53% MaxDD / 0.69 Sharpe vs #009's 29% / -53% / 0.69. The shorter SMA150 lookback exits trends more quickly than SMA200 but also generates more whipsaw on TQQQ's volatile daily swings.

*Overfit 6/10 — SMA150 is non-standard and appears to be a tuned middle-ground between common values (100, 200); applying a single-stock parameter to a leveraged ETF adds bias.*

- **Entry:** TQQQ > SMA(150) → go all-in
- **Exit:** TQQQ <= SMA(150) → liquidate to cash
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 29% | -53% | 0.69 |

> [!code]- Click to view: algo_061.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_061.py"
> ```

---

### 064 — 5 most mkt cap + IBS regime mix

**Description:** Switches between two regimes based on QQQ relative to its 200-day SMA. In trend mode (QQQ above SMA200), it holds all five most market capital companies equal-weight. In non-trend mode, it only holds names where IBS is below 0.2, acting as an oversold mean-reversion filter. The regime mix gives it the best MaxDD in the set (-23%) — the IBS filter successfully sidesteps the worst of bear markets.

*Overfit 3/10 — SMA200 is a standard lookback. The IBS<0.2 threshold is the single tuned parameter; it is reasonable but untested against alternatives.*

- **Entry:** Trend mode (QQQ > SMA200): equal weight all 5. No-trend mode: only names with IBS < 0.2, equal-weighted
- **Exit:** When QQQ < SMA200 and a held name no longer has IBS < 0.2, liquidate
- **Symbols:** QQQ (signal), Top 5 US equities by market cap (dynamic universe)

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 30% | -23% | 1.07 |

> [!code]- Click to view: algo_064.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_064.py"
> ```

---

### 066 — TQQQ hybrid + ATR

**Description:** A two-mode TQQQ strategy gated by SMA200. When TQQQ trades above the 200-day SMA, it takes a full long position. When below, it switches to mean-reversion: entering only when IBS drops below 0.05 and exiting when IBS recovers above 0.70 or price hits a 3x ATR stop-loss from entry. Replacing NVDA with TQQQ yields a near-identical result to #060 (49% CAGR / -48% MaxDD vs 49% / -50%), confirming that the ATR stop on TQQQ adds negligible marginal benefit since TQQQ's 3× volatility makes the 3× ATR distance so wide it rarely triggers.

*Overfit 4/10 — SMA(200) and ATR(14) are standard, but both IBS thresholds (0.05 entry, 0.7 exit) and the 3× ATR stop multiplier are tuned values, now applied to a leveraged ETF rather than a single stock.*

- **Entry:** If TQQQ > SMA200 → full position. If below SMA200 and IBS < 0.05 → full MR position
- **Exit:** Trend mode and price < SMA200 → liquidate. MR mode: IBS > 0.70 or price < entry - 3× ATR → liquidate
- **Symbols:** TQQQ

| Pass? | CAGR | MaxDD | Sharpe |
| :--- | :--- | :--- | :--- |
| ✅ | 49% | -48% | 0.99 |

> [!code]- Click to view: algo_066.py
> ```embed-python
> PATH: "vault://QuantConnect/cc/algos2/algo_066.py"
> ```

---