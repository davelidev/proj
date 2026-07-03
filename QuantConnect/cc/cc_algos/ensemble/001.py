from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class LeveragedRebalanceSub(BaseSubAlgo):
    """
    Entry: 100% TQQQ on first trading day of each year.
    Exit: hold all year, no intra-year exit.
    """

    SYMBOLS = ["TQQQ"]

    def initialize(self):
        self.basket    = [self.algo.AddEquity(t, Resolution.Minute).Symbol for t in self.SYMBOLS]
        self.last_year = None

    def update_targets(self):
        if self.algo.Time.year == self.last_year:
            return False
        self.last_year = self.algo.Time.year
        weight_per_sym = 1 / len(self.basket)
        self.targets = {sym: weight_per_sym for sym in self.basket}
        return True


LeveragedRebalanceAlgo = _make_standalone(LeveragedRebalanceSub)
