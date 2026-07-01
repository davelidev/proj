# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running Backtests

**Run the full ensemble (primary workflow):**
```bash
ult                          # alias for: python3 api/ult_run.py
```

**Run a standalone sub-algo:**
```bash
ult strategies/algos/tech_dip.py
```

**Manual pipeline (step-by-step):**
```bash
python3 strategies/bundle.py                          # regenerate ensemble.py
python3 api/run_qc_backtest.py <file> "<name>"        # upload + compile + start backtest; prints BACKTEST_ID=...
python3 api/poll_backtest.py <backtest_id>            # poll until complete, prints summary stats
python3 api/get_yearly_stats.py <backtest_id>         # fetch yearly returns breakdown
```

**Run unit tests:**
```bash
cd strategies && python3 -m pytest tests/             # all tests
cd strategies && python3 -m pytest tests/test_leveraged_rebalance.py  # single file
```

## Architecture

### Ensemble System

The live algo is `UltimateAlgo` in `strategies/ultAlgo.py`. It owns a list of `sub_algos`, each an instance of a `BaseSubAlgo` subclass from `strategies/algos/`. Each sub-algo maintains its own `targets` dict (`{Symbol: weight}`) and `equity` float (virtual portfolio value used for proportional allocation). The ensemble aggregates weighted targets from all subs each day and calls `SetHoldings`.

**Key design constraints:**
- Sub-algos never call `SetHoldings` directly — they only update `self.targets`.
- All order execution goes through `UltimateAlgo.ExecuteAggregation()`, which is called only from `PerformDailyUpdate` (the daily scheduler). `OnData` updates targets but does **not** trigger execution — this prevents per-minute rebalancing churn from minute-resolution sub-algos.
- Virtual equity (`sub.equity`) is updated each `OnData` call and resets to equal shares annually.
- `SetWarmUp(WARMUP_DAYS, Resolution.Daily)` must specify `Resolution.Daily` — without it, a minute-resolution data subscription (like `VolatilityBreakoutSub`) reduces warmup to ~252 minute bars (~1 day), causing immediate trading with uninitialized indicators.

### Bundling

QC requires a single `main.py`. `strategies/bundle.py` inlines all files into `strategies/embedded/ensemble.py` (or `standalone.py` for single-algo runs). Key stripping it does:
- Removes all `from X import` / `import X` lines.
- In ensemble mode (`ensemble=True`): also strips the `_make_standalone` factory function and all `XxxAlgo = _make_standalone(XxxSub)` assignments. **This is critical** — without stripping, each algo file creates an extra `QCAlgorithm` subclass at import time, and QC runs the first one found instead of `UltimateAlgo`.

### Sub-algo Pattern

Each file in `strategies/algos/` follows this pattern:
```python
class MyStrategySub(BaseSubAlgo):
    def initialize(self): ...          # called once; AddEquity, set up indicators
    def update_targets(self): ...      # called daily; set self.targets, return True if forced rebalance
    def on_data(self, data): ...       # optional; for intraday or event-driven updates

MyStrategyAlgo = _make_standalone(MyStrategySub)  # creates a runnable QCAlgorithm for solo testing
```

`_make_standalone` wraps a sub-algo in a full `QCAlgorithm` for standalone backtest — it is defined in `base.py` and stripped from ensemble bundles.

### Configuration

All backtest date range, cash, and warmup constants live in `strategies/base.py` (imported by all algo files). API credentials are in `api/.env` (not committed).

### Directories

- `strategies/algos/` — active sub-algos used by the ensemble
- `strategies/embedded/` — generated bundle output (do not edit manually)
- `research/` — one-off experimental algos, not part of the ensemble
- `archive/` — retired strategies
- `api/` — QC API scripts and `.env`
