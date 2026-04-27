# Strategy Development Runbook

This document outlines the standard workflow for backtesting strategies on QuantConnect and updating the project documentation.

## 1. Prerequisites
Ensure your `api/.env` file is configured with your QuantConnect API credentials:
*   `QC_USER_ID`: Your QuantConnect User ID.
*   `QC_API_TOKEN`: Your API Token.
*   `QC_PROJECT_ID`: The ID of the project where `main.py` will be updated and executed.

## 2. Triggering a Backtest
To start a new backtest, use the `run_qc_backtest.py` script. This script uploads your local strategy file to QuantConnect as `main.py`, compiles it, and starts the test.

```bash
# Usage: python3 api/run_qc_backtest.py <strategy_file_path> "<test_name>"
python3 api/run_qc_backtest.py strategies/dip_buy_tech.py "Tech Dip Baseline"
```

The script will return a **Backtest ID** (e.g., `d8015ac9...`). Copy this ID for the next steps.

## 3. Monitoring Progress
Use the `poll_backtest.py` script to watch the progress and retrieve final CAGR, Drawdown, and Sharpe stats.

```bash
# Usage: python3 api/poll_backtest.py <backtest_id>
python3 api/poll_backtest.py d8015ac983b4c946e765b9cc03223bb5
```

## 4. Extracting Yearly Stats
Once the backtest is "Completed", use `get_yearly_stats.py` to get the breakdown of performance for each year.

```bash
# Usage: python3 api/get_yearly_stats.py <backtest_id>
python3 api/get_yearly_stats.py d8015ac983b4c946e765b9cc03223bb5
```

## 5. Updating Documentation
> [!IMPORTANT]
> Do not update documentation (`Strategies.md` or `research_log.md`) unless explicitly told to do so by the user. When updating, ensure both the individual strategy section and the aggregated summary tables (Summary Table and Yearly Returns Grid) are updated to remain in sync.

Update `strategies/Strategies.md` with the new data:

### Summary Table
Update the CAGR, MaxDD, and Sharpe columns.
Update the yearly returns grid. Use 🟢 for positive years and 🔴 for negative years.

### Strategy Details
Add a detailed section for the strategy including:
*   **Description:** High-level goals.
*   **Entry Logic:** Technical triggers.
*   **Exit Logic:** Profit targets and stop losses.
*   **Symbols:** Active tickers.
*   **Source Link:** Use the `vault://` pattern to link to the `.py` file.

## 6. Pro-Tips
*   **Wait for previous:** When running scripts in a chain, ensure the backtest has fully completed before running `get_yearly_stats.py`.
*   **Warm-up:** Always ensure your strategy uses `self.SetWarmUp()` to avoid "lazy initialization" bias in the first month of the test.
*   **Daily vs Weekly:** For mean-reversion (dips), daily rebalancing (`EveryDay`) is significantly more efficient than weekly.
