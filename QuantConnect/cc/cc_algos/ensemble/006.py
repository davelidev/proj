from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TQQQSMA150Sub(BaseSubAlgo):
    """#006 — TQQQ trend on QQQ 150d SMA."""

    def initialize(self):
        self.sym  = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma  = self.algo.SMA(self.qqq, 150, Resolution.Daily)

    def update_targets(self):
        if not self.sma.IsReady: return False
        prev = dict(self.targets)
        in_trend = self.algo.Securities[self.qqq].Price > self.sma.Current.Value
        if in_trend:
            self.targets[self.sym] = 1.0
        else:
            self.targets.pop(self.sym, None)
        return self.targets != prev


TQQQSMA150Algo = _make_standalone(TQQQSMA150Sub)
