from fixtures import make_algo
from base import BaseSubAlgo


def _make_sub(algo=None):
    return BaseSubAlgo(algo or make_algo(), "TestSub")


def test_has_changed_false_initially():
    sub = _make_sub()
    assert sub.has_changed() is False


def test_has_changed_true_after_target_set():
    sub = _make_sub()
    sub.has_changed()  # snapshot empty
    sub.targets = {"SPY": 0.5}
    assert sub.has_changed() is True


def test_has_changed_false_when_targets_stable():
    sub = _make_sub()
    sub.targets = {"SPY": 0.5}
    sub.has_changed()  # snapshot
    assert sub.has_changed() is False


def test_has_changed_true_on_weight_change():
    sub = _make_sub()
    sub.targets = {"SPY": 0.5}
    sub.has_changed()
    sub.targets = {"SPY": 0.8}
    assert sub.has_changed() is True


def test_get_universes_empty_when_no_universe():
    sub = _make_sub()
    assert sub.get_universes() == {}


def test_get_universes_returns_selection_when_flag_set():
    sub = _make_sub()
    sub.HAS_UNIVERSE = True
    universes = sub.get_universes()
    assert "TestSub" in universes
    assert callable(universes["TestSub"])


def test_targets_and_prev_targets_are_independent_copies():
    sub = _make_sub()
    sub.targets = {"SPY": 0.5}
    sub.has_changed()  # snapshots _prev_targets = {"SPY": 0.5}
    sub.targets["SPY"] = 0.9  # mutate in-place
    # _prev_targets should still be {"SPY": 0.5}
    assert sub._prev_targets == {"SPY": 0.5}


def test_has_changed_logs_message_on_change():
    algo = make_algo()
    sub = _make_sub(algo)
    sub.targets = {"QQQ": 1.0}
    sub.has_changed()
    sub.targets = {}
    sub.has_changed()
    algo.Log.assert_called()


def test_targets_initialized_empty():
    sub = _make_sub()
    assert sub.targets == {}


def test_force_rebalance_defaults_to_false():
    sub = _make_sub()
    assert sub.force_rebalance is False


def test_universe_groups_initialized_empty():
    sub = _make_sub()
    assert sub.universe_groups == {}


def test_has_changed_symbol_added():
    sub = _make_sub()
    sub.targets = {"SPY": 0.5}
    sub.has_changed()
    sub.targets["QQQ"] = 0.3
    assert sub.has_changed() is True


def test_has_changed_symbol_removed():
    sub = _make_sub()
    sub.targets = {"SPY": 0.5, "QQQ": 0.3}
    sub.has_changed()
    del sub.targets["QQQ"]
    assert sub.has_changed() is True


def test_has_changed_clears_after_snapshot():
    sub = _make_sub()
    sub.targets = {"SPY": 0.5}
    sub.has_changed()  # True — takes snapshot
    # No further change → should be False now
    assert sub.has_changed() is False
