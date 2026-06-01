from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class GoldenCrossATRSub(BaseSubAlgo):
    """Enter on EMA(50) > EMA(200) of QQQ. Exit on crossback or 3×ATR(14) trailing stop on TQQQ."""

    ATR_MULT = 3.0

    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.ema50  = self.algo.EMA(self.qqq, 50,  Resolution.Daily)
        self.ema200 = self.algo.EMA(self.qqq, 200, Resolution.Daily)
        self.atr    = self.algo.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.trail  = 0.0

    def on_data(self, data):
        return self.update_targets()

    def update_targets(self):
        if not (self.ema50.IsReady and self.ema200.IsReady and self.atr.IsReady):
            return False
        price    = self.algo.Securities[self.tqqq].Price
        in_trend = self.ema50.Current.Value > self.ema200.Current.Value

        prev = dict(self.targets)
        if not self.targets:
            if in_trend:
                self.targets = {self.tqqq: 1.0}
                self.trail   = price - self.ATR_MULT * self.atr.Current.Value
        else:
            # Trail ratchets up only
            new_trail = price - self.ATR_MULT * self.atr.Current.Value
            if new_trail > self.trail:
                self.trail = new_trail
            if price < self.trail or not in_trend:
                self.targets = {}
                self.trail   = 0.0
        return self.targets != prev


GoldenCrossATRAlgo = _make_standalone(GoldenCrossATRSub)
