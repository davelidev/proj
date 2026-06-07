from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class DonchianFiveVoteSub(BaseSubAlgo):
    """TQQQ weight = n/5 over Donchian midlines (50, 100, 150, 200, 250) — proportional to # of midlines exceeded."""

    PERIODS = [50, 100, 150, 200, 250]

    def initialize(self):
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.highs = [self.algo.MAX(self.qqq, p, Resolution.Daily) for p in self.PERIODS]
        self.lows  = [self.algo.MIN(self.qqq, p, Resolution.Daily) for p in self.PERIODS]

    def update_targets(self):
        if not self.highs[-1].IsReady:
            return False
        price = self.algo.Securities[self.qqq].Price
        # Midline of each Donchian channel = (period high + period low) / 2
        n_bullish = sum(
            1 for i in range(len(self.PERIODS))
            if self.highs[i].IsReady
            and price > (self.highs[i].Current.Value + self.lows[i].Current.Value) / 2.0
        )
        # Weighted: pure proportional n/N
        weight = n_bullish / float(len(self.PERIODS))

        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev


DonchianFiveVoteAlgo = _make_standalone(DonchianFiveVoteSub)
