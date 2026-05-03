from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RSIDipChampionSub(BaseSubAlgo):
    def initialize(self):
        self.algo.AddEquity("QQQ", Resolution.Daily)
        self.rsi2 = self.algo.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        if not self.rsi2.IsReady: return
        self.targets[self.sym] = int(self.rsi2.Current.Value < 25)


RSIDipChampionAlgo = _make_standalone(RSIDipChampionSub)
