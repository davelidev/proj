---
name: research-qc
description: Research and document high-performance trading strategies from the QuantConnect Community Forum and Reddit r/algotrading. Use when the user needs to identify new alpha sources with CAGR >= 28% and Max Drawdown <= 58%.
---

# Research Quantitative Strategies

This skill automates the process of scouting the QuantConnect Community Forum and Reddit r/algotrading for high-performance trading strategies and maintaining a structured research ledger.

## Workflow

1.  **Environment Setup**: Operate within the `gemini/` directory.
2.  **De-duplication**: 
    - Read `gemini/visited.txt` before searching.
    - NEVER revisit a URL already listed in this file.
    - Append any new URLs researched to `visited.txt` immediately.
3.  **Strategy Scouting**:
    - Scout both the **QuantConnect Forum** and **Reddit r/algotrading** for strategies meeting the primary criteria:
        - **CAGR**: >= 28%
        - **Max Drawdown**: <= 58%
    - **QuantConnect**: Focus on threads with attached code (Python) and validated backtest results.
    - **Reddit**: Search for "strategy", "backtest", "alpha", or "results" in r/algotrading. Look for posts sharing specific logic, code, or detailed performance metrics that can be reproduced.
4.  **Implementation & Backtesting**:
    - For each identified candidate, implement the strategy in a new file named `algos/it_{n}.py` (where n is the global iteration number).
    - Use the project's backtest API (`api/run_qc_backtest.py`) to run a validation backtest from 2014-01-01 to 2025-12-31.
5.  **Documentation & Pagination**:
    - Document results in `qc_forum_{x}.md` (or `reddit_research_{x}.md` if preferred, but keep `qc_forum_{x}.md` as the primary ledger).
    - **Pagination Rule**: Each research file MUST contain exactly 50 strategy entries.
    - Use `qc_forum_1.md` for iterations 1-50, `qc_forum_2.md` for 51-100, etc.
    - The format should match the professional structure of `Strategies.md`, including:
        - Summary performance table with internal links.
        - Horizontal yearly return grid (2014-2025).
        - Detailed breakdown per iteration with embedded code links to `gemini/algos/it_{n}.py`.
6.  **Iteration Goal**: Execute 100 iterations of this loop unless otherwise specified.

## Statistics Standardization

Always report and validate against these thresholds:
- **Success (✅ Pass)**: CAGR >= 28% AND MaxDD <= 58%.
- **Low Return (❌ Low Return)**: CAGR < 28% but MaxDD <= 58%.
- **High Drawdown (❌ High DD)**: CAGR >= 28% but MaxDD > 58%.
- **Failure (❌ Fail)**: Fails both targets.

## Critical Warnings
- **Secrets**: Never log or print QuantConnect API keys.
- **File Collisions**: Ensure `it_{n}.py` indices are unique and incrementing.
- **Context Efficiency**: Combine searches and batch backtest polling when possible.
