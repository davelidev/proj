from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class IBSATRStopSub(BaseSubAlgo):
    """TQQQ/SOXL/TECL basket. Enter on TQQQ IBS<0.1, exit on IBS>0.9 or 3×ATR(14) stop."""

    def initialize(self):
        self.basket      = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        self.atr         = self.algo.ATR(self.basket[0], 14, MovingAverageType.Wilders, Resolution.Daily)
        self.entry_price = None

    def update_targets(self):
        if not self.atr.IsReady:
            return False

        # IBS computed on TQQQ's previous-day bar (Daily resolution).
        bar = self.algo.Securities[self.basket[0]]
        if bar.High <= bar.Low:
            return False
        ibs   = (bar.Close - bar.Low) / (bar.High - bar.Low)
        close = bar.Close

        prev     = dict(self.targets)
        invested = self.basket[0] in self.targets
        weight   = 1.0 / len(self.basket)

        if not invested and ibs < 0.1:
            self.targets = {sym: weight for sym in self.basket}
            self.entry_price = close
        elif invested:
            stop_price = (self.entry_price - 3.0 * self.atr.Current.Value) if self.entry_price else 0
            if ibs > 0.9 or close < stop_price:
                self.targets = {}
                self.entry_price = None
        return self.targets != prev


IBSATRStopAlgo = _make_standalone(IBSATRStopSub)
