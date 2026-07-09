from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RSIThreeVoteSub(BaseSubAlgo):
    """
    Entry: QQQ RSI(2) < 30/25/20 → 33%/67%/100% split across TQQQ/SOXL/TECL (n/3 votes).
    Exit: RSI recovers above all thresholds.
    """

    THRESHOLDS = [20, 25, 30]

    def initialize(self):
        # Subscribe to Minute resolution for intraday tracking
        self.qqq = self.algo.AddEquity("QQQ", Resolution.Minute).Symbol
        self.basket = [self.algo.AddEquity(t, Resolution.Minute).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        
        self.rsi = RelativeStrengthIndex(2, MovingAverageType.Wilders)
        self.algo.IndicatorHistory(self.rsi, self.qqq, 20, Resolution.Daily)
        assert self.rsi.IsReady, "IndicatorHistory failed: rsi not ready"
        assert self.rsi.Current.Time.date() < self.algo.Time.date(), \
            f"IndicatorHistory lookahead: rsi last bar {self.rsi.Current.Time.date()} >= today {self.algo.Time.date()}"


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
