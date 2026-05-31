# Ensemble Monthly Correlation

*Pearson r on monthly returns (M1 rolling window, 2014–2025, up to 144 data points).*

## Correlation with Full Ensemble

| r | n | ID | Name |
| ---: | ---: | :-- | :-- |
| 0.949 | 144 | S05 | QQQ SMA(150) Trend → TQQQ |
| 0.946 | 144 | S11 | Price 126D Percentile |
| 0.942 | 144 | S14 | Donchian-200 Midline |
| 0.938 | 144 | S01 | TQQQ 60% Annual Rebalance |
| 0.930 | 144 | S13 | TQQQ Anti-Martingale Pyramid |
| 0.922 | 144 | S17 | Range Expanded 110% |
| 0.897 | 144 | S15 | ROC+D200 + 7% Trail Exit |
| 0.886 | 144 | S03 | TQQQ Dynamic Sizing |
| 0.878 | 144 | S08 | ROC(20) Zero Cross |
| 0.848 | 144 | S09 | Up-Day Count(20) |
| 0.837 | 144 | S16 | TQQQ Pyramid (10%/day) |
| 0.806 | 144 | S18 | MFI14_Hyst |
| 0.769 | 144 | S04 | TQQQ Expanding Range Breakout |
| 0.761 | 144 | S12 | Trend Stretch Exit |
| 0.595 | 144 | S10 | TII(20) Trend Intensity |
| 0.448 | 144 | S06 | TQQQ IBS Extreme + ATR Stop |
| 0.218 | 144 | S02 | QQQ RSI(2) Dip |

## Notes

- Monthly returns computed as month-over-month equity change from QC M1 rolling window.
- `n` = number of overlapping months used for the correlation.
- Ensemble backtest: full 17-algo portfolio.
- Each sub-algo run standalone (equal allocation, same date range).
