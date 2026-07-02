from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SMA200RSITiersSub(BaseSubAlgo):
    """SMA(200) regime + RSI tiers on TQQQ. Rebalance 10 mins before close using intraday minute data."""

    def initialize(self):
        # Subscribe to Minute resolution for intraday tracking
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        
        # Create manual indicators
        self.rsi2 = RelativeStrengthIndex(2, MovingAverageType.Wilders)
        self.rsi14 = RelativeStrengthIndex(14, MovingAverageType.Wilders)
        self.sma200 = SimpleMovingAverage(200)
        

    def update_targets(self):
        # Feed manual indicators every day (incl. warmup) for a contiguous window
        price = self.algo.Securities[self.tqqq].Price
        self.rsi2.Update(self.algo.Time, price)
        self.rsi14.Update(self.algo.Time, price)
        self.sma200.Update(self.algo.Time, price)

        if self.algo.IsWarmingUp or not (self.rsi14.IsReady and self.rsi2.IsReady and self.sma200.IsReady):
            return False

        in_uptrend = price > self.sma200.Current.Value
        current_w = self.targets.get(self.tqqq, 0)

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


SMA200RSITiersAlgo = _make_standalone(SMA200RSITiersSub)
