from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class LeveragedRebalanceSub(BaseSubAlgo):
    def initialize(self):
        syms = ["TQQQ"]
        self.syms       = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in syms]
        self.targets    = {s: 1 / len(syms) for s in self.syms}
        self._last_year = None

    def update_targets(self):
        if self.algo.Time.year == self._last_year: return
        self._last_year = self.algo.Time.year
        self.targets    = {s: 1 / len(self.syms) for s in self.syms}


LeveragedRebalanceAlgo = _make_standalone(LeveragedRebalanceSub)
