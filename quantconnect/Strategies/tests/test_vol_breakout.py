from datetime import datetime
from fixtures import make_algo, make_indicator, make_security
from algos.vol_breakout import VolatilityBreakoutSub


def _make_sub(price=100.0, volatility=0.05, high=101.0,
              hour=10, is_warming_up=False):
    algo = make_algo(
        time=datetime(2020, 1, 6, hour, 5),
        is_warming_up=is_warming_up,
    )
    algo.MAX.return_value = make_indicator(high)
    sub = VolatilityBreakoutSub(algo, "VolatilityBreakoutSub")
    sub.initialize()

    algo.Securities["TQQQ"] = make_security(price=price)
    # Directly set the volatility indicator value
    sub.volatility.Current.Value = volatility
    sub.high = make_indicator(high)
    return sub


def test_entry_when_all_conditions_met():
    # price (99) >= high (100) * 0.98 (98), volatility (0.05) < 0.1
    sub = _make_sub(price=99.0, volatility=0.05, high=100.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 1.0


def test_no_entry_when_volatility_too_high():
    sub = _make_sub(price=99.0, volatility=0.12, high=100.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ", 0) == 0


def test_no_entry_when_price_too_far_from_high():
    sub = _make_sub(price=90.0, volatility=0.05, high=100.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ", 0) == 0


def test_exit_when_volatility_spikes():
    sub = _make_sub(price=99.0, volatility=0.05, high=100.0)
    sub.update_targets()  # enter
    assert sub.targets.get("TQQQ") == 1.0

    sub.volatility.Current.Value = 0.20
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 0


def test_exit_when_stop_hit():
    sub = _make_sub(price=99.0, volatility=0.05, high=100.0)
    sub.update_targets()  # enter at 99
    entry = sub.entry_price
    assert entry == 99.0

    algo_sec = sub.algo.Securities["TQQQ"]
    algo_sec.Price = entry * 0.96  # below 3% stop
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 0


def test_no_action_before_market_hours():
    sub = _make_sub(price=99.0, volatility=0.05, high=100.0, hour=9)
    sub.update_targets()
    assert sub.targets.get("TQQQ", 0) == 0


def test_no_action_during_warmup():
    sub = _make_sub(price=99.0, volatility=0.05, high=100.0, is_warming_up=True)
    sub.update_targets()
    assert sub.targets.get("TQQQ", 0) == 0


def test_volatility_exactly_at_threshold_no_entry():
    # Condition is < 0.1; exactly 0.1 must NOT trigger entry
    sub = _make_sub(price=99.0, volatility=0.1, high=100.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ", 0) == 0


def test_price_exactly_at_98pct_high_enters():
    # Condition is >=; price == high * 0.98 must enter
    sub = _make_sub(price=98.0, volatility=0.05, high=100.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 1.0


def test_exit_volatility_exactly_at_threshold_no_exit():
    # Condition is > 0.15; exactly 0.15 must NOT exit
    sub = _make_sub(price=99.0, volatility=0.05, high=100.0)
    sub.update_targets()  # enter
    sub.volatility.Current.Value = 0.15
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 1.0


def test_stop_exactly_at_97pct_exits():
    # Condition is <=; price == entry_price * 0.97 must exit
    sub = _make_sub(price=100.0, volatility=0.05, high=100.0)
    sub.update_targets()  # enter at 100
    assert sub.entry_price == 100.0
    sub.algo.Securities["TQQQ"].Price = 97.0  # == 100 * 0.97
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 0


def test_re_entry_after_volatility_exit():
    sub = _make_sub(price=99.0, volatility=0.05, high=100.0)
    sub.update_targets()  # enter
    sub.volatility.Current.Value = 0.20
    sub.update_targets()  # exit via vol spike
    assert sub.targets.get("TQQQ") == 0

    sub.volatility.Current.Value = 0.05  # normalizes
    sub.update_targets()  # re-entry
    assert sub.targets.get("TQQQ") == 1.0


def test_stays_invested_when_no_exit_signal():
    sub = _make_sub(price=99.0, volatility=0.05, high=100.0)
    sub.update_targets()  # enter
    assert sub.targets.get("TQQQ") == 1.0
    sub.update_targets()  # no change in conditions
    assert sub.targets.get("TQQQ") == 1.0
