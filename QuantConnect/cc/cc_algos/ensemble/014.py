from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone
import math


class VolRegime20Sub(BaseSubAlgo):
    """20-day realized vol regime (20%/30% thresholds): vol<20% → 100% TQQQ, 20-30% → 50%, vol>30% → cash."""

    LOW_VOL  = 0.20
    HIGH_VOL = 0.30

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        hist = self.algo.History(self.qqq, 21, Resolution.Daily)
        if hist.empty or len(hist) < 21:
            return False
        closes = [float(x) for x in hist["close"].values]
        rets   = [(closes[i] / closes[i-1]) - 1 for i in range(1, len(closes))]
        mean   = sum(rets) / len(rets)
        var    = sum((r - mean)**2 for r in rets) / (len(rets) - 1)
        ann_vol = math.sqrt(var) * math.sqrt(252)

        if ann_vol < self.LOW_VOL:
            weight = 1.0
        elif ann_vol < self.HIGH_VOL:
            weight = 0.5
        else:
            weight = 0.0

        prev = dict(self.targets)
        if weight > 0:
            self.targets = {self.tqqq: weight}
        else:
            self.targets = {}
        return self.targets != prev


VolRegime20Algo = _make_standalone(VolRegime20Sub)
