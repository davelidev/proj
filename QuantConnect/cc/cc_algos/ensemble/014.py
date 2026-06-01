from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class MFI14HystSub(BaseSubAlgo):
    """MFI(14) hysteresis: enter at >60, exit at <40; between 40-60 hold current position."""

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.mfi  = self.algo.MFI("QQQ", 14, Resolution.Daily)

    def update_targets(self):
        if not self.mfi.IsReady:
            return False
        mfi_value = self.mfi.Current.Value
        prev = dict(self.targets)
        if mfi_value > 60:
            self.targets = {self.tqqq: 1.0}
        elif mfi_value < 40:
            self.targets = {}
        # else: 40 ≤ MFI ≤ 60 → hold current position
        return self.targets != prev


MFI14HystAlgo = _make_standalone(MFI14HystSub)
