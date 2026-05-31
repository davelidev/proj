from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RangeExpandedSub(BaseSubAlgo):
    """Trend (price > 200d median) + range compressed (<110% avg) → 100%; mixed → 50%; else cash."""
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h) < 200: return False
        closes    = [float(x) for x in h["close"].values]
        med       = sorted(closes)[100]
        in_trend  = self.algo.Securities[self.qqq].Price > med
        recent_r  = [float(h["high"].iloc[i]) - float(h["low"].iloc[i]) for i in range(-25, 0)]
        all_r     = [float(h["high"].iloc[i]) - float(h["low"].iloc[i]) for i in range(-200, 0)]
        compressed = (sum(recent_r) / 25) < (sum(all_r) / 200) * 1.1
        if in_trend and compressed:
            wt = 1.0
        elif in_trend or compressed:
            wt = 0.5
        else:
            wt = 0.0
        prev         = dict(self.targets)
        self.targets = {self.tqqq: wt} if wt > 0 else {}
        return self.targets != prev


RangeExpandedAlgo = _make_standalone(RangeExpandedSub)
