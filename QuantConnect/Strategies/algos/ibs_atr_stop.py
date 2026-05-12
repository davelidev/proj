from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class IBSATRStopSub(BaseSubAlgo):
    """#031 — IBS extreme + ATR-based stop loss."""

    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.atr = self.algo.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.entry_price = None

    def on_data(self, data):
        if not self.atr.IsReady: return False
        bar = self.algo.Securities[self.sym]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return False
        ibs = (c - l) / (h - l)
        invested = self.sym in self.targets
        atr_val = self.atr.Current.Value

        prev = dict(self.targets)

        if not invested and ibs < 0.1:
            self.targets[self.sym] = 1.0
            self.entry_price = c
        elif invested:
            stop = self.entry_price - 3.0 * atr_val if self.entry_price else 0
            if ibs > 0.9 or c < stop:
                self.targets.pop(self.sym, None)
                self.entry_price = None

        return self.targets != prev


IBSATRStopAlgo = _make_standalone(IBSATRStopSub)
