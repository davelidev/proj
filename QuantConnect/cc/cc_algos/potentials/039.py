from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TII20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 20, Resolution.Daily)
        if h.empty or len(h) < 20: return False
        c = [float(x) for x in h["close"].values]
        sma = sum(c) / len(c)
        tii = sum(1 for x in c if x > sma)
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if tii > 10 else {}
        return self.targets != prev


TII20Algo = _make_standalone(TII20Sub)
