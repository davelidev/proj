from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TrendStretchExitSub(BaseSubAlgo):
    """QQQ > SMA(200) AND stretch < 5% entry; exit on SMA breach or stretch > 20%."""
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._sma = self.algo.SMA("QQQ", 200, Resolution.Daily)

    def update_targets(self):
        if not self._sma.IsReady: return False
        price   = self.algo.Securities[self.qqq].Price
        sma_val = self._sma.Current.Value
        stretch = (price - sma_val) / sma_val if sma_val > 0 else 0
        prev     = dict(self.targets)
        invested = bool(self.targets)
        if not invested:
            if price > sma_val and stretch < 0.05:
                self.targets = {self.tqqq: 1.0}
        else:
            if price < sma_val or stretch > 0.20:
                self.targets = {}
        return self.targets != prev


TrendStretchExitAlgo = _make_standalone(TrendStretchExitSub)
