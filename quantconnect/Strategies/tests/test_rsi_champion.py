from fixtures import make_algo, make_indicator
from algos.rsi_champion import RSIDipChampionSub


def _make_sub(rsi_value=50.0, is_ready=True):
    algo = make_algo()
    algo.RSI.return_value = make_indicator(rsi_value, is_ready)
    sub = RSIDipChampionSub(algo, "RSIDipChampionSub")
    sub.initialize()
    return sub


def test_entry_when_rsi_below_25():
    sub = _make_sub(rsi_value=20.0)
    sub.update_targets()
    assert len(sub.targets) == 3
    assert all(abs(w - 1 / 3) < 0.001 for w in sub.targets.values())


def test_no_entry_when_rsi_above_25():
    sub = _make_sub(rsi_value=30.0)
    sub.update_targets()
    assert sub.targets == {}


def test_exit_when_rsi_recovers():
    sub = _make_sub(rsi_value=20.0)
    sub.update_targets()
    assert len(sub.targets) == 3

    sub.rsi2.Current.Value = 30.0
    sub.update_targets()
    assert sub.targets == {}


def test_no_action_when_indicator_not_ready():
    sub = _make_sub(rsi_value=10.0, is_ready=False)
    sub.update_targets()
    assert sub.targets == {}


def test_three_distinct_symbols_in_targets():
    sub = _make_sub(rsi_value=20.0)
    sub.update_targets()
    syms = set(sub.targets.keys())
    assert syms == {"TQQQ", "SOXL", "TECL"}


def test_rsi_exactly_at_25_no_entry():
    # Threshold is < 25, so 25 itself must NOT trigger
    sub = _make_sub(rsi_value=25.0)
    sub.update_targets()
    assert sub.targets == {}


def test_weights_sum_to_one():
    sub = _make_sub(rsi_value=10.0)
    sub.update_targets()
    assert abs(sum(sub.targets.values()) - 1.0) < 1e-9


def test_stays_invested_while_rsi_stays_below_25():
    sub = _make_sub(rsi_value=20.0)
    sub.update_targets()
    assert len(sub.targets) == 3
    sub.rsi2.Current.Value = 15.0  # still below 25
    sub.update_targets()
    assert len(sub.targets) == 3


def test_rsi_oscillates_enter_exit_enter():
    sub = _make_sub(rsi_value=20.0)
    sub.update_targets()
    assert len(sub.targets) == 3

    sub.rsi2.Current.Value = 30.0
    sub.update_targets()
    assert sub.targets == {}

    sub.rsi2.Current.Value = 10.0
    sub.update_targets()
    assert len(sub.targets) == 3


def test_all_weights_equal():
    sub = _make_sub(rsi_value=20.0)
    sub.update_targets()
    weights = list(sub.targets.values())
    assert max(weights) - min(weights) < 1e-9
