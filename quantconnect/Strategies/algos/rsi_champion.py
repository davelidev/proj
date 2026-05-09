from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RSIDipChampionSub(BaseSubAlgo):
    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]

    def update_targets(self):
        if not self.rsi2.IsReady: return False

        prev = dict(self.targets)
        if self.rsi2.Current.Value < 25:
            self.targets = {s: 1 / len(self.syms) for s in self.syms}
        else:
            self.targets = {}
        return self.targets != prev


RSIDipChampionAlgo = _make_standalone(RSIDipChampionSub)
