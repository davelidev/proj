from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SMA200PyramidSub(BaseSubAlgo):
    """
    Entry: QQQ>SMA(200) → 50% TQQQ; +15% per 5% gain above entry, cap 100%; de-pyramids on pullback.
    Exit: QQQ<SMA(200).
    """

    def initialize(self):
        self.qqq         = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        self.tqqq        = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.sma200      = SimpleMovingAverage(200)
        self.algo.IndicatorHistory(self.sma200, self.qqq, 250, Resolution.Daily)
        assert self.sma200.IsReady, "IndicatorHistory failed: sma200 not ready"
        assert self.sma200.Current.Time.date() < self.algo.Time.date(), \
            f"IndicatorHistory lookahead: sma200 last bar {self.sma200.Current.Time.date()} >= today {self.algo.Time.date()}"
        self.entry_price = None
        self.current_w   = 0.0


    def update_targets(self):
        # Feed manual SMA every day (incl. warmup) for a contiguous window
        price = self.algo.Securities[self.qqq].Price
        self.sma200.Update(self.algo.Time, price)

        if self.algo.IsWarmingUp or not self.sma200.IsReady:
            return False

        in_uptrend = price > self.sma200.Current.Value
        if not in_uptrend:
            self.targets     = {}
            self.entry_price = None
            self.current_w   = 0.0
        elif not self.targets:
            # Initial entry at 50%
            self.targets     = {self.tqqq: 0.5}
            self.entry_price = price
            self.current_w   = 0.5
        else:
            # Pyramid: +15% size per 5% price gain above entry
            steps    = int((price / self.entry_price - 1) / 0.05) if self.entry_price else 0
            target_w = min(1.0, 0.5 + max(0, steps) * 0.15)
            if abs(target_w - self.current_w) > 0.05:
                self.targets = {self.tqqq: target_w}
                self.current_w = target_w


SMA200PyramidAlgo = _make_standalone(SMA200PyramidSub)
