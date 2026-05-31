from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TQQQPyramidSub(BaseSubAlgo):
    """Bull: +10% TQQQ per day up to 100%; bear signal → 0% immediately."""
    def initialize(self):
        self.qqq      = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq     = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._roc     = self.algo.ROC("QQQ", 20,  Resolution.Daily)
        self._hi200   = self.algo.MAX("QQQ", 200, Resolution.Daily)
        self._lo200   = self.algo.MIN("QQQ", 200, Resolution.Daily)
        self._exposure = 0.0

    def update_targets(self):
        if not (self._roc.IsReady and self._hi200.IsReady and self._lo200.IsReady):
            return False
        mid     = (self._hi200.Current.Value + self._lo200.Current.Value) / 2.0
        bull    = self._roc.Current.Value > 0 and self.algo.Securities[self.qqq].Price > mid
        new_exp = min(1.0, self._exposure + 0.1) if bull else 0.0
        prev    = dict(self.targets)
        if abs(new_exp - self._exposure) > 0.005:
            self._exposure = new_exp
            self.targets   = {self.tqqq: new_exp} if new_exp > 0 else {}
        return self.targets != prev


TQQQPyramidAlgo = _make_standalone(TQQQPyramidSub)
