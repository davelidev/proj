from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class RangeCompressedSub(BaseSubAlgo):
    """
    Entry: QQQ>200d median AND 25d range avg<110% of 200d range avg → 100% TQQQ; one condition → 50%.
    Exit: both false.
    """

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

        sc = sorted(closes)
        median_200d = (sc[99] + sc[100]) / 2
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

        self.targets = {self.tqqq: weight} if weight > 0 else {}


RangeCompressedAlgo = _make_standalone(RangeCompressedSub)
