from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SMAFiveVoteSub(BaseSubAlgo):
    """TQQQ weight = n/5 where n = # of SMA periods (20,50,100,150,200) that QQQ price exceeds."""

    PERIODS = [20, 50, 100, 150, 200]

    def initialize(self):
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.smas = [self.algo.SMA(self.qqq, p, Resolution.Daily) for p in self.PERIODS]

    def update_targets(self):
        if not self.smas[-1].IsReady:
            return False
        price     = self.algo.Securities[self.qqq].Price
        n_bullish = sum(1 for sma in self.smas if price > sma.Current.Value)
        weight    = n_bullish / float(len(self.PERIODS))

        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev


SMAFiveVoteAlgo = _make_standalone(SMAFiveVoteSub)
