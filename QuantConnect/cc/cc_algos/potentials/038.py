from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class UpDay20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return False
        c = [float(x) for x in h["close"].values]
        up_days = sum(1 for i in range(1, len(c)) if c[i] > c[i-1])
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if up_days > 10 else {}
        return self.targets != prev


UpDay20Algo = _make_standalone(UpDay20Sub)
