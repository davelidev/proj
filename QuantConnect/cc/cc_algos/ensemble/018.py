from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class MFI14HystSub(BaseSubAlgo):
    """MFI(14) > 60 → 100% TQQQ; MFI < 40 → cash; 40–60 hold (hysteresis)."""
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._mfi = self.algo.MFI("QQQ", 14, Resolution.Daily)

    def update_targets(self):
        if not self._mfi.IsReady: return False
        v    = self._mfi.Current.Value
        prev = dict(self.targets)
        if v > 60:
            self.targets = {self.tqqq: 1.0}
        elif v < 40:
            self.targets = {}
        return self.targets != prev


MFI14HystAlgo = _make_standalone(MFI14HystSub)
