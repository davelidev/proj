from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class LeveragedRebalanceSub(BaseSubAlgo):
    """Static 60% allocation to TQQQ. Rebalances back to 60% once per year (per-year drift harvest)."""

    SYMBOLS = ["TQQQ"]

    def initialize(self):
        self.basket    = [self.algo.AddEquity(t, Resolution.Minute).Symbol for t in self.SYMBOLS]
        self.last_year = None

    def update_targets(self):
        if self.algo.Time.year == self.last_year:
            return False
        self.last_year = self.algo.Time.year
        weight_per_sym = 0.6 / len(self.basket)
        self.targets = {sym: weight_per_sym for sym in self.basket}
        return True


LeveragedRebalanceAlgo = _make_standalone(LeveragedRebalanceSub)
