from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TrendStretchExitSub(BaseSubAlgo):
    """Enter on QQQ > SMA(200) with stretch < 5%; exit when below SMA or stretch > 20%. Rebalanced daily 10 mins before close."""

    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.sma200 = SimpleMovingAverage(200)

        # Warm up manual SMA
        history = self.algo.History(self.qqq, 220, Resolution.Daily)
        for index, row in history.iterrows():
            self.sma200.Update(index[1], row.close)

    def update_targets(self):
        if self.algo.IsWarmingUp:
            return False

        price = self.algo.Securities[self.qqq].Price
        self.sma200.Update(self.algo.Time, price)

        if not self.sma200.IsReady:
            return False

        sma     = self.sma200.Current.Value
        stretch = (price - sma) / sma if sma > 0 else 0

        prev     = dict(self.targets)
        invested = bool(self.targets)
        if not invested:
            # Enter only at a low-stretch entry above the trend
            if price > sma and stretch < 0.05:
                self.targets = {self.tqqq: 1.0}
        else:
            # Exit on trend break or extreme overbought stretch
            if price < sma or stretch > 0.20:
                self.targets = {}
        return self.targets != prev


TrendStretchExitAlgo = _make_standalone(TrendStretchExitSub)
