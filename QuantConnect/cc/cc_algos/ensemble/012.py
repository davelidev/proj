from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RangeCompressedSub(BaseSubAlgo):
    """Trend (price > 200d median) AND compressed range (25d avg < 110% of 200d avg) → 100%; only one true → 50%; else cash."""

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        hist = self.algo.History(self.qqq, 200, Resolution.Daily)
        if hist.empty or len(hist) < 200:
            return False
        closes      = [float(x) for x in hist["close"].values]
        median_200d = sorted(closes)[100]
        in_trend    = self.algo.Securities[self.qqq].Price > median_200d

        # Range = high-low for each daily bar
        ranges_25d  = [float(hist["high"].iloc[i]) - float(hist["low"].iloc[i]) for i in range(-25, 0)]
        ranges_200d = [float(hist["high"].iloc[i]) - float(hist["low"].iloc[i]) for i in range(-200, 0)]
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
