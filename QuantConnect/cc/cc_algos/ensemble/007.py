from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class AntiMartingaleSub(BaseSubAlgo):
    """QQQ > SMA(200) → 50% TQQQ; pyramid +15% per 5% gain above entry, cap 100%."""
    def initialize(self):
        self.qqq       = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq      = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._sma      = self.algo.SMA("QQQ", 200, Resolution.Daily)
        self._entry_px = None
        self._cur_w    = 0.0

    def update_targets(self):
        if not self._sma.IsReady: return False
        price = self.algo.Securities[self.qqq].Price
        bull  = price > self._sma.Current.Value
        prev  = dict(self.targets)
        if not bull:
            self.targets   = {}
            self._entry_px = None
            self._cur_w    = 0.0
        elif not self.targets:
            self.targets   = {self.tqqq: 0.5}
            self._entry_px = price
            self._cur_w    = 0.5
        else:
            steps  = (price / self._entry_px - 1) / 0.05 if self._entry_px else 0
            target = min(1.0, 0.5 + max(0, int(steps)) * 0.15)
            if abs(target - self._cur_w) > 0.05:
                self.targets = {self.tqqq: target}
                self._cur_w  = target
        return self.targets != prev


AntiMartingaleAlgo = _make_standalone(AntiMartingaleSub)
