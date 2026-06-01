from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SMA200PyramidSub(BaseSubAlgo):
    """QQQ > SMA(200): start at 50% TQQQ, add +15% per 5% gain above entry (cap 100%). Below SMA: cash."""

    def initialize(self):
        self.qqq         = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq        = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma200      = self.algo.SMA("QQQ", 200, Resolution.Daily)
        self.entry_price = None
        self.current_w   = 0.0

    def update_targets(self):
        if not self.sma200.IsReady:
            return False
        price      = self.algo.Securities[self.qqq].Price
        in_uptrend = price > self.sma200.Current.Value
        prev       = dict(self.targets)

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
        return self.targets != prev


SMA200PyramidAlgo = _make_standalone(SMA200PyramidSub)
