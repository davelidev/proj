from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TrendStretchExitSub(BaseSubAlgo):
    """
    Entry: QQQ>SMA(200) and price within 5% of SMA → 100% TQQQ.
    Exit: QQQ<SMA(200) or stretch>20% above SMA.
    """

    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.sma200 = SimpleMovingAverage(200)


    def update_targets(self):
        # Feed manual SMA every day (incl. warmup) for a contiguous window
        price = self.algo.Securities[self.qqq].Price
        self.sma200.Update(self.algo.Time, price)

        if self.algo.IsWarmingUp or not self.sma200.IsReady:
            return False

        sma     = self.sma200.Current.Value
        stretch = (price - sma) / sma if sma > 0 else 0

        invested = bool(self.targets)
        if not invested:
            # Enter only at a low-stretch entry above the trend
            if price > sma and stretch < 0.05:
                self.targets = {self.tqqq: 1.0}
        else:
            # Exit on trend break or extreme overbought stretch
            if price < sma or stretch > 0.20:
                self.targets = {}


TrendStretchExitAlgo = _make_standalone(TrendStretchExitSub)
