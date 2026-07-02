from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RSIThreeVoteSub(BaseSubAlgo):
    """Equal-weight TQQQ/SOXL/TECL basket; basket weight = n/3 (weighted) where n = # of RSI(2) thresholds breached (<20, <25, <30). Rebalance 10 mins before close using intraday minute data."""

    THRESHOLDS = [20, 25, 30]

    def initialize(self):
        # Subscribe to Minute resolution for intraday tracking
        self.qqq = self.algo.AddEquity("QQQ", Resolution.Minute).Symbol
        self.basket = [self.algo.AddEquity(t, Resolution.Minute).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        
        # Create manual RSI(2)
        self.rsi = RelativeStrengthIndex(2, MovingAverageType.Wilders)
        

    def update_targets(self):
        # Feed the manual RSI every day (incl. warmup) so its window stays contiguous
        close = self.algo.Securities[self.qqq].Price
        self.rsi.Update(self.algo.Time, close)

        if self.algo.IsWarmingUp or not self.rsi.IsReady:
            return False
        
        rsi_value = self.rsi.Current.Value
        n_bullish = sum(1 for thr in self.THRESHOLDS if rsi_value < thr)
        total_w = n_bullish / float(len(self.THRESHOLDS))

        if total_w > 0:
            per_sym = total_w / len(self.basket)
            self.targets = {sym: per_sym for sym in self.basket}
        else:
            self.targets = {}


RSIThreeVoteAlgo = _make_standalone(RSIThreeVoteSub)
