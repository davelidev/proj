from fixtures import (
    make_algo, make_indicator, make_security, make_fundamental,
    make_changes, MONDAY, TUESDAY,
)
from mock_qc import MorningstarSectorCode
from algos.tech_dip import TechDipBuySub

TECH = MorningstarSectorCode.Technology
OTHER = 309  # non-tech sector code
UNIVERSE = "TechDipBuySub"


def _make_sub(time=MONDAY, portfolio_value=100_000.0):
    algo = make_algo(time=time, portfolio_value=portfolio_value)
    sub = TechDipBuySub(algo, UNIVERSE)
    sub.initialize()
    return sub


def _add_security(sub, sym, price=100.0, invested=False,
                  avg_price=100.0, holdings_value=0.0,
                  rsi=50.0, sma50=80.0, max_=120.0):
    sec = make_security(price=price, invested=invested,
                        avg_price=avg_price, holdings_value=holdings_value)
    sec.Symbol = sym
    sec.rsi   = make_indicator(rsi)
    sec.max   = make_indicator(max_)
    sec.sma50 = make_indicator(sma50)
    sub.algo.Securities[sym] = sec
    sub.universe_groups[UNIVERSE] = sub.universe_groups.get(UNIVERSE, set()) | {sym}
    return sec


# ---------------------------------------------------------------------------
# universe_selection
# ---------------------------------------------------------------------------

def test_universe_selects_top5_tech_by_market_cap():
    sub = _make_sub()
    fundamentals = [
        make_fundamental(f"T{i}", TECH, market_cap=i * 1e9)
        for i in range(1, 8)  # 7 tech stocks
    ]
    result = sub.universe_selection(fundamentals)
    caps = [f.MarketCap for f in fundamentals if f.Symbol in result]
    assert len(result) == 5
    assert min(caps) >= 3e9  # bottom 2 excluded


def test_universe_filters_non_tech():
    sub = _make_sub()
    fundamentals = [
        make_fundamental("AAPL", TECH,  market_cap=3e12),
        make_fundamental("JPM",  OTHER, market_cap=9e12),  # huge but wrong sector
    ]
    result = sub.universe_selection(fundamentals)
    assert "AAPL" in result
    assert "JPM" not in result


def test_universe_handles_fewer_than_five():
    sub = _make_sub()
    fundamentals = [make_fundamental(f"T{i}", TECH, i * 1e9) for i in range(1, 4)]
    result = sub.universe_selection(fundamentals)
    assert len(result) == 3


# ---------------------------------------------------------------------------
# on_securities_changed
# ---------------------------------------------------------------------------

def test_securities_changed_adds_indicators_to_tech_member():
    sub = _make_sub()
    sym = "AAPL"
    sub.universe_groups[UNIVERSE] = {sym}
    sec = make_security()
    sec.Symbol = sym
    sub.algo.Securities[sym] = sec

    sub.on_securities_changed(make_changes(added=[sec]))

    assert hasattr(sec, "rsi")
    assert hasattr(sec, "max")
    assert hasattr(sec, "sma50")


def test_securities_changed_skips_non_universe_member():
    sub = _make_sub()
    sub.universe_groups[UNIVERSE] = {"MSFT"}  # AAPL NOT in group
    sec = make_security()
    sec.Symbol = "AAPL"

    sub.on_securities_changed(make_changes(added=[sec]))

    sub.algo.RSI.assert_not_called()


def test_securities_changed_liquidates_removed():
    sub = _make_sub()
    sym = "NVDA"
    sub.targets[sym] = 0.2
    sec = make_security()
    sec.Symbol = sym

    sub.on_securities_changed(make_changes(removed=[sec]))

    assert sym not in sub.targets
    sub.algo.Liquidate.assert_called_with(sym)


# ---------------------------------------------------------------------------
# update_targets — timing gate
# ---------------------------------------------------------------------------

def test_no_action_on_non_monday():
    sub = _make_sub(time=TUESDAY)
    _add_security(sub, "AAPL", rsi=20.0)
    sub.update_targets()
    assert "AAPL" not in sub.targets


# ---------------------------------------------------------------------------
# update_targets — entry
# ---------------------------------------------------------------------------

def test_entry_on_valid_signal():
    sub = _make_sub()
    _add_security(sub, "AAPL", price=105.0, rsi=20.0, sma50=80.0, max_=120.0)
    sub.update_targets()
    assert "AAPL" in sub.targets
    assert sub.targets["AAPL"] > 0


def test_no_entry_when_rsi_too_high():
    sub = _make_sub()
    _add_security(sub, "AAPL", price=105.0, rsi=35.0, sma50=80.0)
    sub.update_targets()
    assert "AAPL" not in sub.targets


def test_no_entry_when_price_below_sma():
    sub = _make_sub()
    _add_security(sub, "AAPL", price=70.0, rsi=20.0, sma50=80.0)
    sub.update_targets()
    assert "AAPL" not in sub.targets


# ---------------------------------------------------------------------------
# update_targets — exit
# ---------------------------------------------------------------------------

def test_stop_loss_exit():
    sub = _make_sub()
    sec = _add_security(sub, "AAPL", price=84.0, invested=True,
                        avg_price=100.0, holdings_value=20_000.0, max_=90.0)
    sub.targets["AAPL"] = 0.2

    sub.update_targets()

    assert "AAPL" not in sub.targets


def test_ath_exit():
    sub = _make_sub()
    sec = _add_security(sub, "AAPL", price=120.0, invested=True,
                        avg_price=80.0, holdings_value=24_000.0, max_=120.0)
    sub.targets["AAPL"] = 0.24

    sub.update_targets()

    assert "AAPL" not in sub.targets


# ---------------------------------------------------------------------------
# update_targets — drift-lock & budget
# ---------------------------------------------------------------------------

def test_drift_lock_preserves_grown_position():
    sub = _make_sub(portfolio_value=100_000.0)
    # Position grown to 40% of portfolio (from initial 20%)
    _add_security(sub, "AAPL", price=110.0, invested=True,
                  avg_price=80.0, holdings_value=40_000.0,
                  rsi=50.0, max_=120.0)
    sub.targets["AAPL"] = 0.2  # stale target

    sub.update_targets()

    assert abs(sub.targets["AAPL"] - 0.4) < 0.001  # locked to current weight


def test_budget_caps_entry_when_portfolio_full():
    sub = _make_sub(portfolio_value=100_000.0)
    # Two invested positions consuming 90% of portfolio
    _add_security(sub, "MSFT", price=110.0, invested=True,
                  avg_price=80.0, holdings_value=50_000.0, max_=130.0)
    _add_security(sub, "NVDA", price=110.0, invested=True,
                  avg_price=80.0, holdings_value=40_000.0, max_=130.0)
    sub.targets = {"MSFT": 0.5, "NVDA": 0.4}

    # New entry trigger: only 10% cash remaining
    _add_security(sub, "AAPL", price=105.0, rsi=20.0, sma50=80.0, max_=130.0)

    sub.update_targets()

    if "AAPL" in sub.targets:
        # Entry weight must not exceed remaining budget
        total = sum(sub.targets.values())
        assert total <= 1.001  # scale never drops below 1


# ---------------------------------------------------------------------------
# boundary conditions
# ---------------------------------------------------------------------------

def test_rsi_exactly_at_30_no_entry():
    # Entry condition is rsi < 30; exactly 30 must NOT enter
    sub = _make_sub()
    _add_security(sub, "AAPL", price=105.0, rsi=30.0, sma50=80.0)
    sub.update_targets()
    assert "AAPL" not in sub.targets


def test_price_exactly_at_sma50_no_entry():
    # Entry condition is price > sma50; equality must NOT enter
    sub = _make_sub()
    _add_security(sub, "AAPL", price=80.0, rsi=20.0, sma50=80.0)
    sub.update_targets()
    assert "AAPL" not in sub.targets


def test_stop_loss_at_exactly_85pct_avg():
    # Exit condition is price <= avg * 0.85; equality must trigger exit
    sub = _make_sub()
    _add_security(sub, "AAPL", price=85.0, invested=True,
                  avg_price=100.0, holdings_value=17_000.0, max_=120.0)
    sub.targets["AAPL"] = 0.17
    sub.update_targets()
    assert "AAPL" not in sub.targets


def test_indicators_not_ready_skips_invested_stock():
    # Invested stock with stop-loss trigger is NOT exited when indicators unready
    sub = _make_sub()
    sec = _add_security(sub, "AAPL", price=50.0, invested=True,
                        avg_price=100.0, holdings_value=10_000.0, max_=120.0)
    sec.max.IsReady = False
    sub.targets["AAPL"] = 0.1
    sub.update_targets()
    assert "AAPL" in sub.targets  # guard skipped → no exit


def test_indicators_not_ready_skips_entry():
    # Uninvested stock with valid RSI/price is NOT entered when indicators unready
    sub = _make_sub()
    sec = _add_security(sub, "AAPL", price=105.0, rsi=20.0, sma50=80.0, max_=130.0)
    sec.max.IsReady = False
    sub.update_targets()
    assert "AAPL" not in sub.targets


def test_exit_frees_budget_for_new_entry():
    # AAPL triggers stop loss → exits; budget freed → MSFT enters in same call
    sub = _make_sub(portfolio_value=100_000.0)
    _add_security(sub, "AAPL", price=84.0, invested=True,
                  avg_price=100.0, holdings_value=20_000.0, max_=120.0)
    sub.targets["AAPL"] = 0.2

    _add_security(sub, "MSFT", price=105.0, rsi=20.0, sma50=80.0, max_=130.0)

    sub.update_targets()

    assert "AAPL" not in sub.targets
    assert "MSFT" in sub.targets
    assert sub.targets["MSFT"] > 0


def test_multiple_entries_respect_budget():
    # 3 qualifying stocks, no existing positions → each gets 0.2 (= 1/5)
    sub = _make_sub(portfolio_value=100_000.0)
    for sym in ["AAPL", "MSFT", "NVDA"]:
        _add_security(sub, sym, price=105.0, rsi=20.0, sma50=80.0, max_=130.0)
    sub.update_targets()

    assert len(sub.targets) == 3
    assert all(abs(w - 0.2) < 0.001 for w in sub.targets.values())


def test_budget_too_small_prevents_entry():
    # Invested positions consume ~99.7%, budget = 0.003 < 0.005 → no new entry
    sub = _make_sub(portfolio_value=100_000.0)
    _add_security(sub, "MSFT", price=110.0, invested=True,
                  avg_price=80.0, holdings_value=49_900.0, max_=130.0)
    _add_security(sub, "NVDA", price=110.0, invested=True,
                  avg_price=80.0, holdings_value=49_900.0, max_=130.0)
    sub.targets = {"MSFT": 0.499, "NVDA": 0.499}

    _add_security(sub, "AAPL", price=105.0, rsi=20.0, sma50=80.0, max_=130.0)
    sub.update_targets()

    # budget = 1.0 - 0.499 - 0.499 = 0.002 < 0.005 → no entry
    assert "AAPL" not in sub.targets
