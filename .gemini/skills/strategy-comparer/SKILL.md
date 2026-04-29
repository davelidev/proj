---
name: strategy-comparer
description: Automates the backtesting and side-by-side comparison of specific strategies. Use when the user triggers /compare [args] or asks to "compare strategy X and Y."
---

# Strategy Comparer Workflow

This skill provides an agent-driven workflow to compare specific strategies provided as arguments (e.g., `/compare compare strategy x with x with resolution 10m`).

## Step 1: Resolve Strategies from Arguments
Identify the strategy numbers or names provided in the user's request. Read `QuantConnect/strategies/Strategies.md` to find the corresponding `.py` filenames for those specific strategies (e.g., "Strategy 1" maps to `vol_breakout.py`).

## Step 2: Trigger Backtests
For each strategy identified, run the following command:
```bash
python3 QuantConnect/api/run_qc_backtest.py QuantConnect/strategies/<filename>.py "<Strategy Name> Comparison"
```
Capture the **Backtest ID** for each run.

## Step 3: Poll and Gather Statistics
For each Backtest ID:
1.  **Poll for completion:** `python3 QuantConnect/api/poll_backtest.py <backtest_id>`
2.  **Retrieve performance stats:** Note CAGR, Max Drawdown, and Sharpe Ratio.
3.  **Retrieve yearly returns:** `python3 QuantConnect/api/get_yearly_stats.py <backtest_id>`

## Step 4: Generate Comparison Table
Create a consolidated Markdown table displaying the requested strategies side-by-side.

### Table Format:
| Strategy | CAGR | MaxDD | Sharpe | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Strat Name | XX% | -XX% | X.XXX | 🟢 XX% | 🔴 -XX% | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Note:** Round percentages to the nearest whole number. Use 🟢 for positive years and 🔴 for negative years.
