"""
Integration tests — QuantConnect backtest validation.

Runs fresh backtests on QC and compares results exactly against the baseline JSON.
Results are deterministic: same code always produces identical numbers.

Modes:
  (default)         Run backtests on QC, compare against baseline.
  --update-baseline After running, accept fresh results as the new baseline.

Run:
  python3 -m pytest strategies/tests/test_backtest_results.py -v -s
  python3 -m pytest strategies/tests/test_backtest_results.py -v -s --update-baseline
"""
import os, sys, json, shutil, subprocess
import pytest

_GIT_ROOT     = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"],
    cwd=os.path.dirname(os.path.abspath(__file__)), text=True,
).strip()
REPO_ROOT     = os.path.join(_GIT_ROOT, "quantconnect")
TESTS_DIR     = os.path.dirname(os.path.abspath(__file__))
BASELINE_JSON = os.path.join(TESTS_DIR, "strategies_results.json")
FRESH_JSON    = os.path.join(TESTS_DIR, "strategies_results_fresh.json")
BATCH_RUNNER  = os.path.join(REPO_ROOT, "api/batch_strategies_run.py")
YEARS         = [str(y) for y in range(2014, 2026)]

STRAT_IDS = [
    "vol_breakout.py",
    "tech_dip.py",
    "leveraged_rebalance.py",
    "rsi_champion.py",
    "tqqq_dynamic.py",
    "expanding_breakout.py",
]

STAT_KEYS = [
    "Compounding Annual Return",
    "Drawdown",
    "Sharpe Ratio",
    "Alpha",
    "Beta",
    "Win Rate",
    "Profit-Loss Ratio",
    "Average Win",
    "Average Loss",
    "Total Orders",
]


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _load_env():
    env, env_file = os.environ.copy(), os.path.join(REPO_ROOT, "api/.env")
    if not os.path.exists(env_file):
        return env
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


@pytest.fixture(scope="session")
def baseline():
    if not os.path.exists(BASELINE_JSON):
        pytest.skip("No baseline. Run with --rerun first to establish one.")
    with open(BASELINE_JSON) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def fresh(request):
    """Run fresh backtests on QC."""
    # Write to a separate file so baseline is untouched during the run
    env = {**_load_env(), "QC_RESULTS_JSON": FRESH_JSON}
    if os.path.exists(FRESH_JSON):
        os.remove(FRESH_JSON)
    subprocess.run([sys.executable, BATCH_RUNNER], cwd=REPO_ROOT, env=env, check=True)
    if not os.path.exists(FRESH_JSON):
        pytest.fail("Batch runner did not produce fresh results file.")
    with open(FRESH_JSON) as f:
        return json.load(f)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fmt_pct(v):
    if v is None:
        return "  —  "
    return f"{'+' if v > 0 else ''}{v:.0f}%"


def _diff_card(filename, base, new):
    """Return a formatted diff card for a strategy."""
    b_raw = base.get(filename, {}).get("metrics", {})
    n_raw = new.get(filename, {}).get("metrics", {})
    b_yr  = base.get(filename, {}).get("yearly", [])
    n_yr  = new.get(filename, {}).get("yearly", [])

    lines = ["", "─" * 60, f"  {filename}", "─" * 60,
             f"  {'Metric':<32} {'Baseline':>12}  {'Fresh':>12}  Match"]
    lines.append("  " + "─" * 56)
    for k in STAT_KEYS:
        bv = b_raw.get(k, "—")
        nv = n_raw.get(k, "—")
        ok = "✓" if bv == nv else "✗"
        lines.append(f"  {k:<32} {str(bv):>12}  {str(nv):>12}  {ok}")

    lines += ["", f"  {'Year':<6} {'Baseline':>8}  {'Fresh':>8}  Match"]
    lines.append("  " + "─" * 30)
    for y, bv, nv in zip(YEARS, b_yr, n_yr):
        ok = "✓" if bv == nv else "✗"
        lines.append(f"  {y}   {_fmt_pct(bv):>8}  {_fmt_pct(nv):>8}  {ok}")
    lines.append("─" * 60)
    return "\n".join(lines)


def _skip_if_missing(d, filename, label):
    if filename not in d:
        pytest.skip(f"{filename} not in {label}")


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("filename", STRAT_IDS)
def test_baseline_present(baseline, filename):
    """Baseline JSON must contain every strategy."""
    assert filename in baseline, \
        f"{filename} missing from baseline — run with --rerun to populate"


@pytest.mark.parametrize("filename", STRAT_IDS)
def test_metrics_match(baseline, fresh, filename):
    """Every raw stat must match baseline exactly."""
    _skip_if_missing(baseline, filename, "baseline")
    _skip_if_missing(fresh,    filename, "fresh run")

    b_raw = baseline[filename]["metrics"]
    f_raw = fresh[filename]["metrics"]
    diffs = {k: (b_raw.get(k), f_raw.get(k))
             for k in STAT_KEYS if b_raw.get(k) != f_raw.get(k)}

    assert not diffs, (
        f"{filename}: {len(diffs)} stat(s) changed\n"
        + _diff_card(filename, baseline, fresh)
    )


@pytest.mark.parametrize("filename", STRAT_IDS)
def test_yearly_returns_match(baseline, fresh, filename):
    """Every yearly return must match baseline exactly."""
    _skip_if_missing(baseline, filename, "baseline")
    _skip_if_missing(fresh,    filename, "fresh run")

    b_yr = baseline[filename].get("yearly", [])
    f_yr = fresh[filename].get("yearly", [])
    diffs = {y: (bv, fv)
             for y, bv, fv in zip(YEARS, b_yr, f_yr)
             if bv != fv}

    assert not diffs, (
        f"{filename}: yearly returns changed in {sorted(diffs.keys())}\n"
        + _diff_card(filename, baseline, fresh)
    )


# ── Update baseline after confirmed-good run ──────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def maybe_update_baseline(request, fresh):
    yield
    if not request.config.getoption("--update-baseline"):
        print("\n  Tip: run with --update-baseline to accept these as the new baseline.")
        return
    shutil.copy(FRESH_JSON, BASELINE_JSON)
    print(f"\n  ✓ Baseline updated → {BASELINE_JSON}")


# ── Session summary ───────────────────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def print_summary(baseline, fresh):
    yield
    W = 23
    print("\n\n" + "═" * 72)
    print("  FRESH RUN vs BASELINE")
    print("═" * 72)
    hdr = f"  {'Strategy':<{W}}  {'CAGR':>6}  {'MaxDD':>6}  {'Sharpe':>6}  {'Alpha':>5}  {'Beta':>5}  {'WR':>5}  {'PF':>5}"
    print(hdr)
    print("  " + "─" * 68)
    for fname in STRAT_IDS:
        r   = fresh.get(fname, {})
        s   = r.get("stats", {})
        raw = r.get("metrics", {})
        cagr   = f"{s['CAGR']:.0f}%"    if s.get("CAGR")   is not None else "—"
        maxdd  = f"-{s['MaxDD']:.0f}%"  if s.get("MaxDD")  is not None else "—"
        sharpe = f"{s['Sharpe']:.2f}"   if s.get("Sharpe") is not None else "—"
        alpha  = f"{float(raw['Alpha']):.2f}" if raw.get("Alpha") else "—"
        beta   = f"{float(raw['Beta']):.2f}"  if raw.get("Beta")  else "—"
        wr     = raw.get("Win Rate", "—")
        pf     = f"{s['PL']:.2f}"       if s.get("PL") is not None else "—"
        b_raw  = baseline.get(fname, {}).get("metrics", {})
        changed = sum(1 for k in STAT_KEYS if b_raw.get(k) != raw.get(k))
        match  = "  ✓" if changed == 0 else f"  ✗ {changed} changed"
        print(f"  {fname:<{W}}  {cagr:>6}  {maxdd:>6}  {sharpe:>6}  {alpha:>5}  {beta:>5}  {str(wr):>5}  {pf:>5}{match}")

    print("\n  YEARLY RETURNS (%)")
    print("  " + "─" * 68)
    print("  " + f"{'Strategy':<{W}}" + "".join(f" {y[2:]:>5}" for y in YEARS))
    print("  " + "─" * 68)
    for fname in STRAT_IDS:
        yr    = fresh.get(fname, {}).get("yearly", [])
        cells = "".join(f" {_fmt_pct(v):>5}" for v in yr)
        print(f"  {fname:<{W}}{cells}")
    print("  " + "─" * 68)
    print("═" * 72 + "\n")
