from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class IBSATRStopSub(BaseSubAlgo):
    """IBS extreme + ATR-based stop loss on equal-weight TQQQ/SOXL/TECL basket.

    Uses update_targets (scheduled at +DAILY_OPEN_MIN after market open) rather
    than on_data: the standalone factory's on_data path delivered systematically
    worse fills. With Resolution.Daily, Securities[syms[0]] at +45 min after open
    already reflects the previous trading day's complete bar, so IBS/ATR can be
    computed cleanly here. Signal and ATR derived from TQQQ; position spread equally
    across TQQQ, SOXL, TECL.
    """

    def initialize(self):
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        self.atr  = self.algo.ATR(self.syms[0], 14, MovingAverageType.Wilders, Resolution.Daily)
        self.entry_price = None

    def update_targets(self):
        if not self.atr.IsReady: return False
        bar = self.algo.Securities[self.syms[0]]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return False
        ibs = (c - l) / (h - l)
        invested = self.syms[0] in self.targets
        atr_val = self.atr.Current.Value

        prev = dict(self.targets)
        w = 1.0 / len(self.syms)

        if not invested and ibs < 0.1:
            self.targets = {s: w for s in self.syms}
            self.entry_price = c
        elif invested:
            stop = self.entry_price - 3.0 * atr_val if self.entry_price else 0
            if ibs > 0.9 or c < stop:
                self.targets = {}
                self.entry_price = None

        return self.targets != prev


IBSATRStopAlgo = _make_standalone(IBSATRStopSub)
