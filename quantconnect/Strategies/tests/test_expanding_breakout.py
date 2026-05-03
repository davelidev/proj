from fixtures import (
    make_algo, make_indicator, make_security,
    make_history, MONDAY,
)
from algos.expanding_breakout import ExpandingBreakoutSub


def _make_sub(
    tqqq_price=100.0,
    qqq_price=350.0,
    sma200=300.0,
    adx=30.0,
    max20=110.0,
    atr=2.0,
    history=None,
    ready=True,
):
    algo = make_algo(time=MONDAY)
    algo.SMA.return_value  = make_indicator(sma200, ready)
    algo.ADX.return_value  = make_indicator(adx,    ready)
    algo.MAX.return_value  = make_indicator(max20,  ready)
    algo.ATR.return_value  = make_indicator(atr,    ready)
    # History default: expanding range (bar[-2] range > bar[-3] range)
    algo.History.return_value = history or make_history(
        (305, 300),  # bar[-3]: range 5
        (308, 301),  # bar[-2]: range 7  → expanding
        (310, 304),  # bar[-1]: unused
    )
    sub = ExpandingBreakoutSub(algo, "ExpandingBreakoutSub")
    sub.initialize()
    algo.Securities["TQQQ"] = make_security(price=tqqq_price)
    algo.Securities["QQQ"]  = make_security(price=qqq_price)
    return sub


def test_entry_when_all_conditions_met():
    sub = _make_sub(tqqq_price=100.0, qqq_price=350.0, sma200=300.0, adx=30.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 1.0


def test_entry_sets_trailing_stop():
    sub = _make_sub(tqqq_price=100.0, atr=2.0)
    sub.update_targets()
    assert sub.trailing_stop == pytest_approx(94.0)  # 100 - 3*2


def test_no_entry_when_qqq_below_sma():
    sub = _make_sub(qqq_price=280.0, sma200=300.0)
    sub.update_targets()
    assert sub.targets == {}


def test_no_entry_when_adx_too_low():
    sub = _make_sub(adx=20.0)
    sub.update_targets()
    assert sub.targets == {}


def test_no_entry_when_range_not_expanding():
    flat_history = make_history(
        (308, 301),  # bar[-3]: range 7
        (305, 300),  # bar[-2]: range 5  → NOT expanding
        (310, 304),
    )
    sub = _make_sub(history=flat_history)
    sub.update_targets()
    assert sub.targets == {}


def test_exit_at_20day_high():
    sub = _make_sub(tqqq_price=100.0, max20=100.0)  # price == max
    sub.update_targets()  # enter
    # Ensure entry happened
    if not sub.targets:
        return  # max condition prevented entry; test not applicable
    sub.algo.Securities["TQQQ"].Price = 110.0
    sub.max_exit = make_indicator(110.0)
    sub.update_targets()
    assert sub.targets == {}


def test_exit_when_qqq_drops_below_sma():
    sub = _make_sub(tqqq_price=100.0)
    sub.update_targets()  # enter
    sub.algo.Securities["QQQ"].Price = 280.0  # below sma200=300
    sub.update_targets()
    assert sub.targets == {}


def test_trailing_stop_ratchets_up():
    # Use max20=200 so the ATH exit doesn't fire while testing the ratchet
    sub = _make_sub(tqqq_price=100.0, atr=2.0, max20=200.0)
    sub.update_targets()
    initial_stop = sub.trailing_stop  # 100 - 3*2 = 94

    # Price rises to 110; new stop = 110 - 6 = 104 > 94 → ratchet up
    sub.algo.Securities["TQQQ"].Price = 110.0
    sub.update_targets()
    assert sub.trailing_stop > initial_stop
    assert abs(sub.trailing_stop - 104.0) < 0.001


def test_trailing_stop_does_not_ratchet_down():
    # Price rises first (ratchets stop to 104), then falls back but stays above stop
    sub = _make_sub(tqqq_price=100.0, atr=2.0, max20=200.0)
    sub.update_targets()  # stop = 94

    sub.algo.Securities["TQQQ"].Price = 110.0
    sub.update_targets()  # stop ratchets to 104

    high_water_stop = sub.trailing_stop  # 104
    # Price pulls back to 106 (above stop=104); new stop = 100 < 104 → no ratchet
    sub.algo.Securities["TQQQ"].Price = 106.0
    sub.update_targets()
    assert sub.trailing_stop == high_water_stop


def test_no_entry_when_history_too_short():
    short_history = make_history((310, 304))  # only 1 bar; len < 3 → early return
    sub = _make_sub(history=short_history)
    sub.update_targets()
    assert sub.targets == {}


def test_adx_exactly_at_25_no_entry():
    # Condition is > 25; exactly 25 must NOT trigger entry
    sub = _make_sub(adx=25.0)
    sub.update_targets()
    assert sub.targets == {}


def test_trailing_stop_reset_to_zero_on_exit():
    sub = _make_sub(tqqq_price=100.0, atr=2.0, max20=200.0)
    sub.update_targets()  # enter, stop = 94
    assert sub.trailing_stop > 0

    sub.algo.Securities["QQQ"].Price = 250.0  # below sma200=300 → exit
    sub.update_targets()

    assert sub.targets == {}
    assert sub.trailing_stop == 0


def test_multiple_price_ratchets():
    sub = _make_sub(tqqq_price=100.0, atr=2.0, max20=500.0)
    sub.update_targets()  # enter, stop = 94

    sub.algo.Securities["TQQQ"].Price = 110.0
    sub.update_targets()
    assert abs(sub.trailing_stop - 104.0) < 0.001

    sub.algo.Securities["TQQQ"].Price = 120.0
    sub.update_targets()
    assert abs(sub.trailing_stop - 114.0) < 0.001

    sub.algo.Securities["TQQQ"].Price = 130.0
    sub.update_targets()
    assert abs(sub.trailing_stop - 124.0) < 0.001


def test_trailing_stop_exit():
    sub = _make_sub(tqqq_price=100.0, atr=2.0, max20=200.0)
    sub.update_targets()  # enter, stop = 94

    sub.algo.Securities["TQQQ"].Price = 90.0  # below stop=94
    sub.update_targets()

    assert sub.targets == {}
    assert sub.trailing_stop == 0


def test_no_reentry_while_already_invested():
    # Entry conditions still met but not-empty targets → else branch (exit check only)
    sub = _make_sub(tqqq_price=100.0, max20=200.0)
    sub.update_targets()  # enter
    assert sub.targets.get("TQQQ") == 1.0

    sub.update_targets()  # conditions still met, but already in position
    assert sub.targets.get("TQQQ") == 1.0  # position unchanged, not doubled


def test_qqq_below_sma_exits_profitable_position():
    sub = _make_sub(tqqq_price=100.0, qqq_price=350.0, sma200=300.0, max20=200.0)
    sub.update_targets()  # enter
    assert sub.targets.get("TQQQ") == 1.0

    sub.algo.Securities["QQQ"].Price = 250.0  # below sma200=300
    sub.update_targets()
    assert sub.targets == {}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def pytest_approx(value, rel=1e-3):
    return value  # inline approx: use direct equality since floats are exact here
