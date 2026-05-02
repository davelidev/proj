from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TQQQDynamicSub(BaseSubAlgo):
    def initialize(self):
        self.sym    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2   = self.algo.RSI(self.sym, 2,   MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10  = self.algo.RSI(self.sym, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.sym, 200, Resolution.Daily)
        self.current_weight = 0

    def update_targets(self) -> bool:
        if not (self.rsi2.IsReady and self.sma200.IsReady): return False
        price = self.algo.Securities[self.sym].Price
        if price > self.sma200.Current.Value:
            if self.rsi10.Current.Value > 80:
                new_w = 0.2
            elif self.rsi2.Current.Value < 30:
                new_w = 1.0
            elif self.current_weight == 0:
                new_w = 0.5
            else:
                new_w = self.current_weight
        else:
            new_w = 0
        changed             = (self.current_weight != new_w)
        self.current_weight = new_w
        self.targets        = {self.sym: self.current_weight}
        return changed


TQQQDynamicAlgo = _make_standalone(TQQQDynamicSub)
