from fixtures import make_algo
from base import BaseSubAlgo


def _make_sub(algo=None):
    return BaseSubAlgo(algo or make_algo(), "TestSub")


def test_get_universes_empty_when_no_universe():
    sub = _make_sub()
    assert sub.get_universes() == {}


def test_get_universes_returns_selection_when_flag_set():
    sub = _make_sub()
    sub.HAS_UNIVERSE = True
    universes = sub.get_universes()
    assert "TestSub" in universes
    assert callable(universes["TestSub"])


def test_targets_initialized_empty():
    sub = _make_sub()
    assert sub.targets == {}


def test_force_rebalance_defaults_to_false():
    sub = _make_sub()
    assert sub.force_rebalance is False


def test_universe_groups_initialized_empty():
    sub = _make_sub()
    assert sub.universe_groups == {}
