from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class ROCD200TrailSub(BaseSubAlgo):
    """ROC(20)>0 AND QQQ > D200 midline AND within 7% of 20d high → 100% TQQQ."""
    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._roc   = self.algo.ROC("QQQ", 20,  Resolution.Daily)
        self._hi200 = self.algo.MAX("QQQ", 200, Resolution.Daily)
        self._lo200 = self.algo.MIN("QQQ", 200, Resolution.Daily)
        self._hi20  = self.algo.MAX("QQQ", 20,  Resolution.Daily)

    def update_targets(self):
        if not (self._roc.IsReady and self._hi200.IsReady
                and self._lo200.IsReady and self._hi20.IsReady):
            return False
        price = self.algo.Securities[self.qqq].Price
        mid   = (self._hi200.Current.Value + self._lo200.Current.Value) / 2.0
        dd_20 = price / self._hi20.Current.Value - 1.0
        bull  = self._roc.Current.Value > 0 and price > mid
        prev  = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if (bull and dd_20 > -0.07) else {}
        return self.targets != prev


ROCD200TrailAlgo = _make_standalone(ROCD200TrailSub)
