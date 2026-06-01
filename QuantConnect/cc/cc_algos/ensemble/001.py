from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class StaticTQQQ60Sub(BaseSubAlgo):
    """Static 60% allocation split equally across SYMBOLS. Rebalances once per year."""

    SYMBOLS = ["TQQQ"]

    def initialize(self):
        self.basket    = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in self.SYMBOLS]
        self.last_year = None

    def update_targets(self):
        if self.algo.Time.year == self.last_year:
            return False
        self.last_year = self.algo.Time.year
        weight_per_sym = 0.6 / len(self.basket)
        self.targets = {sym: weight_per_sym for sym in self.basket}
        return True


StaticTQQQ60Algo = _make_standalone(StaticTQQQ60Sub)
