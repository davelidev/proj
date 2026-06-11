from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SMA200RSITiersSub(BaseSubAlgo):
    """SMA(200) regime + RSI tiers on TQQQ. Above SMA: 100% on RSI(2)<30 dip, 20% on RSI(14)>70 overbought, 50% on first entry from cash, else hold current weight (sticky). Below SMA: cash."""

    def initialize(self):
        self.tqqq   = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2   = self.algo.RSI(self.tqqq,  2, MovingAverageType.Wilders, Resolution.Daily)
        self.rsi14  = self.algo.RSI(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.algo.SMA(self.tqqq, 200, Resolution.Daily)

    def update_targets(self):
        if not (self.rsi14.IsReady and self.sma200.IsReady):
            return False
        price       = self.algo.Securities[self.tqqq].Price
        in_uptrend  = price > self.sma200.Current.Value
        current_w   = self.targets.get(self.tqqq, 0)

        prev = dict(self.targets)
        if in_uptrend:
            if self.rsi14.Current.Value > 70:
                self.targets[self.tqqq] = 0.2  # overbought trim
            elif self.rsi2.Current.Value < 30:
                self.targets[self.tqqq] = 1.0  # dip buy
            elif current_w == 0:
                self.targets[self.tqqq] = 0.5  # default entry
            # else: hold current weight
        else:
            self.targets = {}
        return self.targets != prev


SMA200RSITiersAlgo = _make_standalone(SMA200RSITiersSub)
