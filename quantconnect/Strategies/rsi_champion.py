from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RSIDipChampionSub(BaseSubAlgo):
    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.syms = [self.algo.AddEquity(t, Resolution.Daily).Symbol for t in ["TQQQ", "SOXL", "TECL"]]

    def update_targets(self) -> bool:
        if not self.rsi2.IsReady: return False
        weight  = 1/3 if self.rsi2.Current.Value < 25 else 0
        changed = (self.targets.get(self.syms[0], -1) != weight)
        self.targets = {s: weight for s in self.syms}
        return changed


RSIDipChampionAlgo = _make_standalone(RSIDipChampionSub)
