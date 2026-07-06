from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class DonchianFourVoteSub(BaseSubAlgo):
    """TQQQ position = n/4 where n = # of Donchian midlines (50,100,150,200) that QQQ price is above."""

    PERIODS = [50, 100, 150, 200]

    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.hi  = [self.algo.MAX(self.qqq, n, Resolution.Daily) for n in self.PERIODS]
        self.lo  = [self.algo.MIN(self.qqq, n, Resolution.Daily) for n in self.PERIODS]

    def update_targets(self):
        if not self.hi[-1].IsReady: return False
        prev  = dict(self.targets)
        price = self.algo.Securities[self.qqq].Price
        n = sum(
            price > (self.hi[i].Current.Value + self.lo[i].Current.Value) / 2.0
            for i in range(len(self.PERIODS))
            if self.hi[i].IsReady
        )
        weight = n / float(len(self.PERIODS))
        if weight > 0:
            self.targets[self.sym] = weight
        else:
            self.targets.pop(self.sym, None)
        return self.targets != prev


DonchianFourVoteAlgo = _make_standalone(DonchianFourVoteSub)
