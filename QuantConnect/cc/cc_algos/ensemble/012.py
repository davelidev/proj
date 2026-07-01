from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RangeCompressedSub(BaseSubAlgo):
    """Trend (price > 200d median) AND compressed range (25d avg < 110% of 200d avg) → 100%; only one true → 50%; else cash. Rebalanced daily 10 mins before close."""

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol

    def update_targets(self):
        if self.algo.IsWarmingUp:
            return False

        # Get today's aggregated bar up to 3:50 PM
        today = self.get_daily_bar(self.qqq)
        if today is None:
            return False

        # Fetch last 199 daily bars
        hist = self.algo.History(self.qqq, 199, Resolution.Daily)
        if hist.empty or len(hist) < 199:
            return False

        closes = [float(x) for x in hist["close"].values] + [today.Close]
        highs = [float(x) for x in hist["high"].values] + [today.High]
        lows = [float(x) for x in hist["low"].values] + [today.Low]

        median_200d = sorted(closes)[100]
        in_trend    = today.Close > median_200d

        # Range = high-low for each daily bar
        ranges_200d = [highs[i] - lows[i] for i in range(200)]
        ranges_25d  = ranges_200d[-25:]
        avg_25      = sum(ranges_25d)  / 25
        avg_200     = sum(ranges_200d) / 200
        compressed  = avg_25 < avg_200 * 1.1

        if in_trend and compressed:
            weight = 1.0
        elif in_trend or compressed:
            weight = 0.5
        else:
            weight = 0.0

        prev = dict(self.targets)
        self.targets = {self.tqqq: weight} if weight > 0 else {}
        return self.targets != prev


RangeCompressedAlgo = _make_standalone(RangeCompressedSub)
