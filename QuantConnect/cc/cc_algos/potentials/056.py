from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class Price126DSub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 126, Resolution.Daily)
        if h.empty or len(h) < 126: return False
        closes = [float(x) for x in h["close"].values]
        lo, hi = min(closes), max(closes)
        if hi == lo: return False
        pct = (closes[-1] - lo) / (hi - lo)
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if pct > 0.5 else {}
        return self.targets != prev


Price126DAlgo = _make_standalone(Price126DSub)
