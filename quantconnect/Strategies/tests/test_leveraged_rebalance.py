from datetime import datetime
from fixtures import make_algo
from algos.leveraged_rebalance import LeveragedRebalanceSub


def _make_sub(year=2020):
    algo = make_algo(time=datetime(year, 1, 6, 10, 5))
    sub = LeveragedRebalanceSub(algo, "LeveragedRebalanceSub")
    sub.initialize()
    return sub


def test_sets_target_on_first_call():
    sub = _make_sub(2020)
    sub.update_targets()
    assert "TQQQ" in sub.targets


def test_target_weight_is_60_percent():
    sub = _make_sub(2020)
    sub.update_targets()
    assert abs(sub.targets["TQQQ"] - 0.6) < 0.001


def test_no_change_same_year():
    sub = _make_sub(2020)
    sub.update_targets()
    sub.targets["TQQQ"] = 0.99  # simulate drift
    sub.update_targets()         # should not reset since same year
    assert sub.targets["TQQQ"] == 0.99


def test_resets_on_new_year():
    sub = _make_sub(2020)
    sub.update_targets()
    sub.algo.Time = datetime(2021, 1, 4, 10, 5)
    sub.update_targets()
    assert abs(sub.targets["TQQQ"] - 0.6) < 0.001


def test_returns_true_on_first_rebalance():
    sub = _make_sub(2020)
    result = sub.update_targets()
    assert result is True


def test_returns_false_same_year():
    sub = _make_sub(2020)
    sub.update_targets()
    result = sub.update_targets()
    assert result is False


def test_consecutive_year_transitions():
    sub = _make_sub(2020)
    sub.update_targets()
    sub.targets["TQQQ"] = 0.99  # simulate drift

    sub.algo.Time = datetime(2021, 1, 4, 10, 5)
    sub.update_targets()
    assert abs(sub.targets["TQQQ"] - 0.6) < 0.001

    sub.targets["TQQQ"] = 0.99
    sub.algo.Time = datetime(2022, 1, 3, 10, 5)
    sub.update_targets()
    assert abs(sub.targets["TQQQ"] - 0.6) < 0.001


def test_only_tqqq_in_targets():
    sub = _make_sub(2020)
    sub.update_targets()
    assert set(sub.targets.keys()) == {"TQQQ"}


def test_midyear_call_does_not_rebalance():
    sub = _make_sub(2020)
    sub.update_targets()
    sub.targets["TQQQ"] = 0.99
    # Different date but same year
    sub.algo.Time = datetime(2020, 7, 6, 10, 5)
    sub.update_targets()
    assert sub.targets["TQQQ"] == 0.99
