from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RSIThreeVoteSub(BaseSubAlgo):
    """Equal-weight TQQQ/SOXL/TECL basket; position = n/3 where n = # of RSI(2) thresholds breached (<20, <25, <30)."""

    THRESHOLDS = [20, 25, 30]

    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi    = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.basket = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]

    def update_targets(self):
        if not self.rsi.IsReady:
            return False
        rsi_value = self.rsi.Current.Value
        n_bullish = sum(1 for thr in self.THRESHOLDS if rsi_value < thr)
        total_w   = n_bullish / float(len(self.THRESHOLDS))

        prev = dict(self.targets)
        if total_w > 0:
            per_sym = total_w / len(self.basket)
            self.targets = {sym: per_sym for sym in self.basket}
            self.force_rebalance = True
        else:
            self.targets = {}
        return self.targets != prev


RSIThreeVoteAlgo = _make_standalone(RSIThreeVoteSub)
