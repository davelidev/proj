from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class LeveragedRebalanceSub(BaseSubAlgo):
    def initialize(self):
        syms = ["TQQQ"]
        self.syms       = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in syms]
        self._last_year = None

    def update_targets(self):
        # Annual rebalance: always returns True on year-change so the ensemble
        # rebalances to correct positional drift, even though weights are static.
        if self.algo.Time.year == self._last_year: return False
        self._last_year = self.algo.Time.year
        self.targets = {s: 1 / len(self.syms) * .6 for s in self.syms}
        return True


LeveragedRebalanceAlgo = _make_standalone(LeveragedRebalanceSub)
