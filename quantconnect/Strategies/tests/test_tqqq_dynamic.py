from fixtures import make_algo, make_indicator, make_security
from algos.tqqq_dynamic import TQQQDynamicSub


def _make_sub(price=150.0, sma200=100.0, rsi2=50.0, rsi10=50.0, ready=True):
    algo = make_algo()
    algo.SMA.return_value = make_indicator(sma200, ready)
    # RSI calls: first call → rsi2, second call → rsi10
    algo.RSI.side_effect = [make_indicator(rsi2, ready), make_indicator(rsi10, ready)]
    sub = TQQQDynamicSub(algo, "TQQQDynamicSub")
    sub.initialize()
    algo.Securities["TQQQ"] = make_security(price=price)
    return sub


def test_full_position_on_dip_above_sma():
    sub = _make_sub(price=150.0, sma200=100.0, rsi2=20.0, rsi10=50.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 1.0


def test_delever_when_rsi10_overbought():
    sub = _make_sub(price=150.0, sma200=100.0, rsi2=50.0, rsi10=85.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 0.2


def test_default_half_position_above_sma():
    sub = _make_sub(price=150.0, sma200=100.0, rsi2=50.0, rsi10=50.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 0.5


def test_exit_when_below_sma():
    sub = _make_sub(price=90.0, sma200=100.0, rsi2=20.0, rsi10=50.0)
    sub.targets["TQQQ"] = 1.0  # simulate existing position
    sub.update_targets()
    assert sub.targets == {}


def test_no_action_when_not_ready():
    sub = _make_sub(ready=False)
    sub.update_targets()
    assert "TQQQ" not in sub.targets


def test_delever_wins_over_dip_when_both_triggered():
    # RSI10 > 80 AND RSI2 < 30 simultaneously — de-lever is checked first
    sub = _make_sub(price=150.0, sma200=100.0, rsi2=20.0, rsi10=85.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 0.2


def test_rsi2_exactly_at_30_no_full_position():
    # Threshold is < 30; exactly 30 falls into the default branch
    sub = _make_sub(price=150.0, sma200=100.0, rsi2=30.0, rsi10=50.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 0.5


def test_price_exactly_at_sma200_exits():
    # Condition is price > sma200; equality means no bull regime → exit
    sub = _make_sub(price=100.0, sma200=100.0)
    sub.targets["TQQQ"] = 1.0
    sub.update_targets()
    assert sub.targets == {}


def test_stays_full_after_dip_signal_clears():
    # After full entry on dip, RSI recovers but no extreme → holds full (current_w != 0)
    sub = _make_sub(price=150.0, sma200=100.0, rsi2=20.0, rsi10=50.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 1.0

    sub.rsi2.Current.Value = 50.0  # dip signal gone, but not overbought
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 1.0  # stays full


def test_default_position_not_set_when_already_invested():
    # "elif current_w == 0" means default 50% is only set from zero
    sub = _make_sub(price=150.0, sma200=100.0, rsi2=50.0, rsi10=50.0)
    sub.targets["TQQQ"] = 0.3  # some existing weight
    sub.update_targets()
    # current_w = 0.3 ≠ 0, so default branch is skipped — targets[TQQQ] unchanged
    assert sub.targets.get("TQQQ") == 0.3


def test_transition_full_to_delever():
    sub = _make_sub(price=150.0, sma200=100.0, rsi2=20.0, rsi10=50.0)
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 1.0

    sub.rsi10.Current.Value = 85.0  # goes overbought
    sub.update_targets()
    assert sub.targets.get("TQQQ") == 0.2
