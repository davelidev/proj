from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone
import math


class VolRegime20Sub(BaseSubAlgo):
    """20-day realized vol regime (20%/30% thresholds): vol<20% → 100% TQQQ, 20-30% → 50%, vol>30% → cash. Rebalanced daily 10 mins before close."""

    LOW_VOL  = 0.20
    HIGH_VOL = 0.30

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol

    def update_targets(self):
        if self.algo.IsWarmingUp:
            return False

        # Get today's close up to 3:50 PM
        today_close = self.algo.Securities[self.qqq].Price

        # Fetch last 20 daily bars
        hist = self.algo.History(self.qqq, 20, Resolution.Daily)
        if hist.empty or len(hist) < 20:
            return False
            
        closes = [float(x) for x in hist["close"].values] + [today_close]
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

        if weight > 0:
            self.targets = {self.tqqq: weight}
        else:
            self.targets = {}


VolRegime20Algo = _make_standalone(VolRegime20Sub)
