from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RangeBreakoutSub(BaseSubAlgo):
    """QQQ > SMA(200) + range expanding + ADX(10) > 25 → 100% TQQQ. Exits: 3×ATR trail, 20d high, or trend break."""

    def initialize(self):
        self.tqqq    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq     = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.adx     = self.algo.ADX(self.qqq, 10, Resolution.Daily)
        self.sma200  = self.algo.SMA(self.qqq, 200, Resolution.Daily)
        self.atr     = self.algo.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.hi20    = self.algo.MAX(self.tqqq, 20, Resolution.Daily)
        self.trail   = 0.0

    def on_data(self, data):
        return self.update_targets()

    def update_targets(self):
        if not (self.adx.IsReady and self.sma200.IsReady and self.hi20.IsReady):
            return False
        tqqq_price = self.algo.Securities[self.tqqq].Price
        qqq_price  = self.algo.Securities[self.qqq].Price
        sma200     = self.sma200.Current.Value
        adx        = self.adx.Current.Value
        hi20       = self.hi20.Current.Value

        # Range expansion: yesterday's QQQ range > the day before's. Skip today's
        # just-closed bar (iloc[-1]) — acts on settled prior bars only.
        hist = self.algo.History(self.qqq, 3, Resolution.Daily)
        if len(hist) < 3:
            return False
        range_of = lambda bar: bar.high - bar.low
        range_expanding = range_of(hist.iloc[-2]) > range_of(hist.iloc[-3])

        prev = dict(self.targets)
        if not self.targets:
            # Entry
            if qqq_price > sma200 and range_expanding and adx > 25:
                self.targets = {self.tqqq: 1.0}
                self.trail   = tqqq_price - 3.0 * self.atr.Current.Value
        else:
            # Trail ratchets up only
            new_trail = tqqq_price - 3.0 * self.atr.Current.Value
            if new_trail > self.trail:
                self.trail = new_trail
            # Exit on take-profit, stop, or trend break
            if tqqq_price >= hi20 or tqqq_price < self.trail or qqq_price < sma200:
                self.targets = {}
                self.trail   = 0.0
        return self.targets != prev


RangeBreakoutAlgo = _make_standalone(RangeBreakoutSub)
