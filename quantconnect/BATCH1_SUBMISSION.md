# Batch 1 Submission Guide

## Status

**Phase 1-2 Complete:** All 10 strategies (001-010) have been generated and validated.

**Phase 3 Pending:** QC cluster was at capacity during initial submission attempt. All strategies are ready to submit.

## File Locations

All strategies are in: `cc/algos3/algo_001.py` through `algo_010.py`

## To Submit All 10 Strategies

Use the provided script:

```bash
cd /Users/daveli/Desktop/proj/QuantConnect
bash /tmp/submit_batch1_sequential.sh
```

This script will:
1. Submit each algo sequentially
2. Poll and wait for each backtest to complete (20-40 min each)
3. Extract CAGR, MaxDD, Sharpe from results
4. Append results to `/tmp/batch1_results.txt`

Total time: ~4-6 hours (10 algos × 25-40 min per backtest)

## Manual Submission (One at a Time)

If you prefer to submit manually:

```bash
cd /Users/daveli/Desktop/proj/QuantConnect

# Submit algo 001
python3 api/run_qc_backtest.py cc/algos3/algo_001.py "Algo001-Davey-Mega-Cap"
# Output: BACKTEST_ID=...

# Poll result (replace with actual ID)
python3 api/poll_backtest.py <BACKTEST_ID>

# Repeat for 002-010
```

## Results Processing

After all 10 complete, process results:

```bash
cd /Users/daveli/Desktop/proj/QuantConnect

# Parse results from /tmp/batch1_results.txt
# Update cc3.log and cc3.md with entries
# Example row for cc3.log:
# 001,Algo001-Davey-Mega-Cap,1,RSI(5) < 30 + vol,mega-cap,XX.X,-YY.Y,Z.ZZ,✅,<backtest-id>

git add cc3.log cc3.md
git commit -m "batch1: results 001-010 processed"
```

## Strategy Descriptions

| # | Name | Signal |
| :- | :--- | :--- |
| 001 | RSI | RSI(5) < 30 AND 20d vol < 25% → long; > 70 AND vol < 25% → short |
| 002 | Stochastic | %K < 30 → long; > 70 → short |
| 003 | ATR-Breakout | price > 20d high + 1.5×ATR → long; < 20d low - 1.5×ATR → short |
| 004 | Inside-Outside | 3-bar pattern + momentum filter |
| 005 | MA Crossover | SMA(5) cross SMA(20) with price gate |
| 006 | Range Contraction | ATR ratio < 0.6 + breakout entry |
| 007 | Day-of-Week | Wed/Thu + 21d momentum > 0 |
| 008 | CCI | CCI > 100 → short; < -100 → long |
| 009 | Bollinger Band | Lower band touch → long; upper band → short |
| 010 | Percentile | Close < 25th pct → long; > 75th pct → short |

## Universe

All strategies use: **TQQQ + dynamic top-10 by market cap** (via AddUniverse CoarseSelectionFunction)

## Parameters

- Start Date: 2014-01-01
- End Date: 2025-12-31
- Cash: $100,000
- Resolution: Daily only
- Warmup: 20-100 bars (strategy-specific)

## Pass Criteria

CAGR ≥ 28% AND |MaxDD| ≤ 58%

---

Created: 2025-05-10
Status: Generated + Validated, awaiting submission
