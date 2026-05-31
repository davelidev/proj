from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SMAFiveVoteSub(BaseSubAlgo):
    """TQQQ position = n/5 where n = # of (SMA20, SMA50, SMA100, SMA150, SMA200) that QQQ price is above."""

    PERIODS = [20, 50, 100, 150, 200]

    def initialize(self):
        self.sym  = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.smas = [self.algo.SMA(self.qqq, n, Resolution.Daily) for n in self.PERIODS]

    def update_targets(self):
        if not self.smas[-1].IsReady: return False
        prev  = dict(self.targets)
        price = self.algo.Securities[self.qqq].Price
        n     = sum(price > sma.Current.Value for sma in self.smas)
        weight = n / float(len(self.PERIODS))
        if weight > 0:
            self.targets[self.sym] = weight
        else:
            self.targets.pop(self.sym, None)
        return self.targets != prev


SMAFiveVoteAlgo = _make_standalone(SMAFiveVoteSub)
