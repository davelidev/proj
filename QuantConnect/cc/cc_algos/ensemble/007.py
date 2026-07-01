from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SMAFiveVoteSub(BaseSubAlgo):
    """TQQQ weight = n/8 over SMA periods (20, 50, 100, 150×4, 200) — proportional to # of SMAs exceeded. SMA(150) quadrupled since it tested best individually. Rebalanced daily 10 mins before close."""

    PERIODS = [20, 50, 100, 150, 150, 150, 150, 200]

    def initialize(self):
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        
        # Create manual SMAs
        unique_periods = sorted(list(set(self.PERIODS)))
        self.sma_map = {p: SimpleMovingAverage(p) for p in unique_periods}

        # Warm up the manual indicators
        history = self.algo.History(self.qqq, 250, Resolution.Daily)
        for index, row in history.iterrows():
            for p, sma in self.sma_map.items():
                sma.Update(index[1], row.close)

    def update_targets(self):
        # Feed manual SMAs every day (incl. warmup) for a contiguous window
        close = self.algo.Securities[self.qqq].Price
        for sma in self.sma_map.values():
            sma.Update(self.algo.Time, close)

        if self.algo.IsWarmingUp:
            return False

        if not all(sma.IsReady for sma in self.sma_map.values()):
            return False

        price     = close
        n_bullish = sum(1 for p in self.PERIODS if price > self.sma_map[p].Current.Value)
        # Weighted: pure proportional n/N
        weight    = n_bullish / float(len(self.PERIODS))

        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev


SMAFiveVoteAlgo = _make_standalone(SMAFiveVoteSub)
