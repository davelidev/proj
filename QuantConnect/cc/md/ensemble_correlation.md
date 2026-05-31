# Ensemble Correlation Analysis

*Based on yearly returns 2014–2025. 17 sub-algos.*

## Correlation Matrix

> `**` >= 0.95  |  `*` >= 0.90  |  `~` >= 0.75  |  blank < 0.75

| ID  | Label      | S01 |  S02 |  S03 |  S04 |   S05 |  S06 |   S08 |   S09 |  S10 |   S11 |   S12 |      S13 |      S14 |      S15 |   S16 |      S17 |   S18 |
| :-- | :--------- | --: | ---: | ---: | ---: | ----: | ---: | ----: | ----: | ---: | ----: | ----: | -------: | -------: | -------: | ----: | -------: | ----: |
| S01 | BuyHold    |  -- | 0.47 | 0.74 | 0.48 | 0.92* | 0.47 | 0.77~ |  0.70 | 0.04 | 0.85~ | 0.85~ |    0.85~ |    0.92* |     0.66 |  0.68 |    0.94* |  0.68 |
| S02 | RSI2Dip    |     |   -- | 0.62 | 0.41 |  0.62 | 0.51 |  0.55 |  0.46 | 0.13 |  0.58 |  0.68 |     0.69 |     0.61 |     0.55 |  0.61 |     0.58 |  0.38 |
| S03 | SMA+RSI    |     |      |   -- | 0.60 | 0.92* | 0.45 |  0.68 |  0.55 | 0.21 | 0.88~ | 0.80~ |    0.94* |    0.89~ |     0.66 |  0.57 |    0.83~ |  0.52 |
| S04 | RngBrk     |     |      |      |   -- |  0.61 | 0.32 |  0.47 |  0.41 | 0.24 |  0.56 |  0.60 |     0.60 |     0.57 |     0.47 |  0.41 |     0.53 |  0.16 |
| S05 | SMA150     |     |      |      |      |    -- | 0.56 | 0.79~ |  0.70 | 0.12 | 0.93* | 0.90~ | **0.96** | **0.95** |     0.72 |  0.68 | **0.96** |  0.60 |
| S06 | IBS+ATR    |     |      |      |      |       |   -- | 0.86~ | 0.79~ | 0.55 |  0.70 |  0.44 |     0.53 |     0.52 |    0.91* | 0.84~ |     0.61 |  0.68 |
| S08 | ROC20      |     |      |      |      |       |      |    -- | 0.90~ | 0.54 | 0.88~ |  0.66 |     0.74 |    0.79~ | **0.98** | 0.95* |    0.85~ | 0.88~ |
| S09 | UpDay20    |     |      |      |      |       |      |       |    -- | 0.26 |  0.75 |  0.57 |     0.63 |     0.70 |    0.87~ | 0.79~ |    0.77~ |  0.72 |
| S10 | TII20      |     |      |      |      |       |      |       |       |   -- |  0.32 |  0.07 |     0.17 |     0.16 |     0.62 |  0.63 |     0.17 |  0.60 |
| S11 | Pr126D     |     |      |      |      |       |      |       |       |      |    -- | 0.79~ |    0.88~ |    0.94* |    0.86~ | 0.80~ |    0.88~ |  0.72 |
| S12 | TrnStretch |     |      |      |      |       |      |       |       |      |       |    -- |    0.93* |    0.90* |     0.60 |  0.67 |    0.89~ |  0.49 |
| S13 | AntiMart   |     |      |      |      |       |      |       |       |      |       |       |       -- |    0.95* |     0.70 |  0.68 |    0.93* |  0.58 |
| S14 | Dnch200    |     |      |      |      |       |      |       |       |      |       |       |          |       -- |     0.74 |  0.74 |    0.91* |  0.69 |
| S15 | ROC+D200   |     |      |      |      |       |      |       |       |      |       |       |          |          |       -- | 0.95* |    0.76~ | 0.85~ |
| S16 | Pyramid    |     |      |      |      |       |      |       |       |      |       |       |          |          |          |    -- |    0.75~ | 0.88~ |
| S17 | RngExp110  |     |      |      |      |       |      |       |       |      |       |       |          |          |          |       |       -- |  0.69 |
| S18 | MFI14Hyst  |     |      |      |      |       |      |       |       |      |       |       |          |          |          |       |          |    -- |

## High-Correlation Pairs

|         r | A   | B   | Strategy A                              | Strategy B                   |
| --------: | :-- | :-- | :-------------------------------------- | :--------------------------- |
| **0.981** | S08 | S15 | ROC(20) Zero Cross                      | ROC+D200 + 7% Trail Exit     |
| **0.963** | S05 | S13 | QQQ SMA(150) Trend → TQQQ               | TQQQ Anti-Martingale Pyramid |
| **0.962** | S05 | S17 | QQQ SMA(150) Trend → TQQQ               | Range Expanded 110%          |
| **0.953** | S05 | S14 | QQQ SMA(150) Trend → TQQQ               | Donchian-200 Midline         |
|    0.948* | S08 | S16 | ROC(20) Zero Cross                      | TQQQ Pyramid                 |
|    0.948* | S15 | S16 | ROC+D200 + 7% Trail Exit                | TQQQ Pyramid                 |
|    0.948* | S13 | S14 | TQQQ Anti-Martingale Pyramid            | Donchian-200 Midline         |
|    0.936* | S03 | S13 | TQQQ Dynamic Sizing: SMA200 + RSI Tiers | TQQQ Anti-Martingale Pyramid |
|    0.936* | S11 | S14 | Price 126D Percentile                   | Donchian-200 Midline         |
|    0.936* | S01 | S17 | TQQQ 60% Annual Rebalance               | Range Expanded 110%          |
|    0.932* | S12 | S13 | Trend Stretch Exit                      | TQQQ Anti-Martingale Pyramid |
|    0.930* | S05 | S11 | QQQ SMA(150) Trend → TQQQ               | Price 126D Percentile        |
|    0.926* | S13 | S17 | TQQQ Anti-Martingale Pyramid            | Range Expanded 110%          |
|    0.924* | S03 | S05 | TQQQ Dynamic Sizing: SMA200 + RSI Tiers | QQQ SMA(150) Trend → TQQQ    |
|    0.921* | S01 | S05 | TQQQ 60% Annual Rebalance               | QQQ SMA(150) Trend → TQQQ    |
|    0.916* | S01 | S14 | TQQQ 60% Annual Rebalance               | Donchian-200 Midline         |
|    0.915* | S06 | S15 | TQQQ IBS Extreme + ATR Stop             | ROC+D200 + 7% Trail Exit     |
|    0.914* | S14 | S17 | Donchian-200 Midline                    | Range Expanded 110%          |
|    0.903* | S12 | S14 | Trend Stretch Exit                      | Donchian-200 Midline         |
|    0.900~ | S08 | S09 | ROC(20) Zero Cross                      | Up-Day Count(20)             |
|    0.896~ | S05 | S12 | QQQ SMA(150) Trend → TQQQ               | Trend Stretch Exit           |
|    0.891~ | S12 | S17 | Trend Stretch Exit                      | Range Expanded 110%          |
|    0.888~ | S03 | S14 | TQQQ Dynamic Sizing: SMA200 + RSI Tiers | Donchian-200 Midline         |
|    0.883~ | S16 | S18 | TQQQ Pyramid                            | MFI14_Hyst                   |
|    0.881~ | S08 | S18 | ROC(20) Zero Cross                      | MFI14_Hyst                   |
|    0.880~ | S03 | S11 | TQQQ Dynamic Sizing: SMA200 + RSI Tiers | Price 126D Percentile        |
|    0.878~ | S08 | S11 | ROC(20) Zero Cross                      | Price 126D Percentile        |
|    0.877~ | S11 | S13 | Price 126D Percentile                   | TQQQ Anti-Martingale Pyramid |
|    0.876~ | S11 | S17 | Price 126D Percentile                   | Range Expanded 110%          |
|    0.867~ | S09 | S15 | Up-Day Count(20)                        | ROC+D200 + 7% Trail Exit     |
|    0.864~ | S06 | S08 | TQQQ IBS Extreme + ATR Stop             | ROC(20) Zero Cross           |
|    0.858~ | S11 | S15 | Price 126D Percentile                   | ROC+D200 + 7% Trail Exit     |
|    0.853~ | S01 | S11 | TQQQ 60% Annual Rebalance               | Price 126D Percentile        |
|    0.849~ | S15 | S18 | ROC+D200 + 7% Trail Exit                | MFI14_Hyst                   |
|    0.847~ | S01 | S12 | TQQQ 60% Annual Rebalance               | Trend Stretch Exit           |
|    0.847~ | S01 | S13 | TQQQ 60% Annual Rebalance               | TQQQ Anti-Martingale Pyramid |
|    0.846~ | S08 | S17 | ROC(20) Zero Cross                      | Range Expanded 110%          |
|    0.837~ | S06 | S16 | TQQQ IBS Extreme + ATR Stop             | TQQQ Pyramid                 |
|    0.827~ | S03 | S17 | TQQQ Dynamic Sizing: SMA200 + RSI Tiers | Range Expanded 110%          |
|    0.801~ | S11 | S16 | Price 126D Percentile                   | TQQQ Pyramid                 |
|    0.795~ | S03 | S12 | TQQQ Dynamic Sizing: SMA200 + RSI Tiers | Trend Stretch Exit           |
|    0.794~ | S08 | S14 | ROC(20) Zero Cross                      | Donchian-200 Midline         |
|    0.792~ | S11 | S12 | Price 126D Percentile                   | Trend Stretch Exit           |
|    0.791~ | S06 | S09 | TQQQ IBS Extreme + ATR Stop             | Up-Day Count(20)             |
|    0.790~ | S09 | S16 | Up-Day Count(20)                        | TQQQ Pyramid                 |
|    0.790~ | S05 | S08 | QQQ SMA(150) Trend → TQQQ               | ROC(20) Zero Cross           |
|    0.772~ | S09 | S17 | Up-Day Count(20)                        | Range Expanded 110%          |
|    0.768~ | S01 | S08 | TQQQ 60% Annual Rebalance               | ROC(20) Zero Cross           |
|    0.764~ | S15 | S17 | ROC+D200 + 7% Trail Exit                | Range Expanded 110%          |
|    0.753~ | S16 | S17 | TQQQ Pyramid                            | Range Expanded 110%          |

## Correlation with Full Ensemble

| r | ID | Name |
| ---: | :-- | :-- |
| 0.952 | S11 | Price 126D Percentile |
| 0.948 | S08 | ROC(20) Zero Cross |
| 0.938 | S17 | Range Expanded 110% |
| 0.929 | S05 | QQQ SMA(150) Trend → TQQQ |
| 0.927 | S14 | Donchian-200 Midline |
| 0.917 | S15 | ROC+D200 + 7% Trail Exit |
| 0.909 | S13 | TQQQ Anti-Martingale Pyramid |
| 0.899 | S16 | TQQQ Pyramid |
| 0.868 | S01 | TQQQ 60% Annual Rebalance |
| 0.850 | S12 | Trend Stretch Exit |
| 0.837 | S03 | TQQQ Dynamic Sizing: SMA200 + RSI Tiers |
| 0.830 | S09 | Up-Day Count(20) |
| 0.786 | S18 | MFI14_Hyst |
| 0.773 | S06 | TQQQ IBS Extreme + ATR Stop |
| 0.672 | S02 | QQQ RSI(2) Dip → Equal-Weight TQQQ/SOXL/TECL |
| 0.585 | S04 | TQQQ Expanding Range Breakout + ATR Trailing Stop |
| 0.390 | S10 | TII(20) Trend Intensity |

## Yearly Returns by Sub-Algo

| ID | Name | '14 | '15 | '16 | '17 | '18 | '19 | '20 | '21 | '22 | '23 | '24 | '25 |
| :-- | :-- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| S01 | TQQQ 60% Annual Rebalance | +34% | +13% | +4% | +71% | -13% | +81% | +66% | +53% | -48% | +118% | +37% | +18% |
| S02 | QQQ RSI(2) Dip → Equal-Weight TQQQ/SOXL/TECL | +38% | +1% | -18% | +46% | +12% | +34% | +81% | +110% | +32% | +60% | +72% | +62% |
| S03 | TQQQ Dynamic Sizing: SMA200 + RSI Tiers | +35% | +4% | -15% | +133% | +7% | +29% | +68% | +83% | -21% | +70% | +29% | +25% |
| S04 | TQQQ Expanding Range Breakout + ATR Trailing Stop | +137% | -3% | -6% | +76% | +54% | +14% | +84% | +49% | -14% | +72% | +39% | +28% |
| S05 | QQQ SMA(150) Trend → TQQQ | +47% | +18% | -5% | +118% | +1% | +53% | +97% | +88% | -34% | +125% | +45% | +27% |
| S06 | TQQQ IBS Extreme + ATR Stop | +7% | +6% | +39% | +71% | -29% | +33% | +344% | +75% | -1% | +101% | +29% | +82% |
| S08 | ROC(20) Zero Cross | +26% | -10% | -2% | +85% | -8% | +85% | +169% | +40% | -18% | +85% | +27% | +40% |
| S09 | Up-Day Count(20) | +43% | +6% | +3% | +58% | -26% | +80% | +147% | +41% | +27% | +92% | +8% | -3% |
| S10 | TII(20) Trend Intensity | +21% | -6% | +30% | +55% | +48% | +39% | +84% | +2% | +14% | -2% | +34% | +59% |
| S11 | Price 126D Percentile | +46% | +25% | -5% | +118% | -25% | +59% | +119% | +68% | -41% | +86% | +26% | +52% |
| S12 | Trend Stretch Exit | +70% | +1% | -12% | +118% | -23% | +50% | +96% | +92% | -44% | +142% | +135% | +24% |
| S13 | TQQQ Anti-Martingale Pyramid | +33% | -6% | -6% | +111% | -5% | +35% | +83% | +88% | -36% | +90% | +62% | +7% |
| S14 | Donchian-200 Midline | +56% | +22% | -5% | +118% | -19% | +80% | +97% | +88% | -47% | +93% | +62% | +20% |
| S15 | ROC+D200 + 7% Trail Exit | +26% | -11% | -2% | +85% | -15% | +66% | +185% | +39% | -19% | +56% | +23% | +42% |
| S16 | TQQQ Pyramid | +22% | -9% | +4% | +51% | -7% | +64% | +118% | +27% | -9% | +45% | +52% | +46% |
| S17 | Range Expanded 110% | +23% | +6% | -10% | +99% | +1% | +63% | +109% | +62% | -34% | +135% | +56% | +8% |
| S18 | MFI14_Hyst | -11% | +2% | +11% | +71% | +8% | +120% | +121% | +29% | -20% | +41% | +36% | +40% |

## Key Observations

**Correlated clusters (likely redundant):**

- **Trend core:** S05 SMA150, S13 AntiMartingale, S14 Donchian200, S17 RangeExp -- all r >= 0.93
- **ROC pair:** S08 ROC20 <-> S15 ROC+D200 -- r = 0.98, near-identical year-by-year
- **Price/momentum:** S11 Price126D, S12 TrendStretch, S03 SMA+RSI cluster at r >= 0.88

**Most diversifying (genuinely independent):**

- **S10 TII20** -- r < 0.65 with all other algos; most uncorrelated sub-algo
- **S04 RngBrk** -- r <= 0.61 everywhere; breakout logic is structurally different
- **S02 RSI2Dip** -- r <= 0.69; mean-reversion dip-buyer diverges from trend followers

**Ensemble drivers:**

- S11, S08, S17, S05 have r >= 0.93 with the ensemble -- ensemble behavior largely reflects these
- S10 (r = 0.39) and S04 (r = 0.59) contribute the most unique signal
