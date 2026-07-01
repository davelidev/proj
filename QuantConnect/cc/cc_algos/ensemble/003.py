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
        
        # Warm up the manual indicator with historical daily data
        history = self.algo.History(self.qqq, 30, Resolution.Daily)
        for index, row in history.iterrows():
            self.rsi.Update(index[1], row.close)

    def update_targets(self):
        # Feed the manual RSI every day (incl. warmup) so its window stays contiguous
        close = self.algo.Securities[self.qqq].Price
        self.rsi.Update(self.algo.Time, close)

        if self.algo.IsWarmingUp:
            return False

        if not self.rsi.IsReady:
            return False
        
        rsi_value = self.rsi.Current.Value
        n_bullish = sum(1 for thr in self.THRESHOLDS if rsi_value < thr)
        total_w = n_bullish / float(len(self.THRESHOLDS))

        prev = dict(self.targets)
        if total_w > 0:
            per_sym = total_w / len(self.basket)
            self.targets = {sym: per_sym for sym in self.basket}
        else:
            self.targets = {}

        return self.targets != prev


RSIThreeVoteAlgo = _make_standalone(RSIThreeVoteSub)
