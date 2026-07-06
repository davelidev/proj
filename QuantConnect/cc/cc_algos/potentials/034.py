from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class Donchian200MidlineSub(BaseSubAlgo):
    """QQQ > midpoint of 200-day Donchian channel → 100% TQQQ; else cash."""
    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._hi200 = self.algo.MAX("QQQ", 200, Resolution.Daily)
        self._lo200 = self.algo.MIN("QQQ", 200, Resolution.Daily)

    def update_targets(self):
        if not (self._hi200.IsReady and self._lo200.IsReady): return False
        price   = self.algo.Securities[self.qqq].Price
        midline = (self._hi200.Current.Value + self._lo200.Current.Value) / 2.0
        prev    = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if price > midline else {}
        return self.targets != prev


Donchian200MidlineAlgo = _make_standalone(Donchian200MidlineSub)
