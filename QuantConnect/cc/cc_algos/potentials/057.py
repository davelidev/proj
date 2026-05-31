from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class ROC20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._roc = self.algo.ROC("QQQ", 20, Resolution.Daily)

    def update_targets(self):
        if not self._roc.IsReady: return False
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if self._roc.Current.Value > 0 else {}
        return self.targets != prev


ROC20Algo = _make_standalone(ROC20Sub)
