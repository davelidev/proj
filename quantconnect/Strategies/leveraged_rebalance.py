from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class LeveragedRebalanceSub(BaseSubAlgo):
    def initialize(self):
        self.syms       = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        self.targets    = {s: 0.20 for s in self.syms}
        self._last_year = None

    def update_targets(self) -> bool:
        if self.algo.Time.year == self._last_year: return False
        self._last_year = self.algo.Time.year
        self.targets    = {s: 0.20 for s in self.syms}
        return True


LeveragedRebalanceAlgo = _make_standalone(LeveragedRebalanceSub)
