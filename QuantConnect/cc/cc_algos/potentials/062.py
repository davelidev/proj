from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SMA150TrendSub(BaseSubAlgo):
    """100% TQQQ when QQQ > SMA(150); cash otherwise."""

    def initialize(self):
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma150 = self.algo.SMA(self.qqq, 150, Resolution.Daily)

    def update_targets(self):
        if not self.sma150.IsReady:
            return False
        in_uptrend = self.algo.Securities[self.qqq].Price > self.sma150.Current.Value

        prev = dict(self.targets)
        if in_uptrend:
            self.targets[self.tqqq] = 1.0
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev


SMA150TrendAlgo = _make_standalone(SMA150TrendSub)
