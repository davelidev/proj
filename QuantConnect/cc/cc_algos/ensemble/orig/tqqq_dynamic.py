from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TQQQDynamicSub(BaseSubAlgo):
    def initialize(self):
        self.sym    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2   = self.algo.RSI(self.sym, 2,   MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10  = self.algo.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.sym, 200, Resolution.Daily)

    def update_targets(self):
        if not (self.rsi2.IsReady and self.sma200.IsReady): return False
        price = self.algo.Securities[self.sym].Price

        prev = dict(self.targets)
        current_w = self.targets.get(self.sym, 0)

        if price > self.sma200.Current.Value:
            if self.rsi10.Current.Value > 80:
                self.targets[self.sym] = 0.2
            elif self.rsi2.Current.Value < 30:
                self.targets[self.sym] = 1.0
            elif current_w == 0:
                self.targets[self.sym] = 0.5
        else:
            self.targets = {}

        return self.targets != prev


TQQQDynamicAlgo = _make_standalone(TQQQDynamicSub)
