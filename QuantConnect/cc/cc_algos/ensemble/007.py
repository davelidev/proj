from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class DonchianFiveVoteSub(BaseSubAlgo):
    """
    Entry: TQQQ weight = n/5 Donchian midlines QQQ is above (50/100/150/200/250d).
    Exit: weight falls to 0 as price drops below midlines.
    """

    PERIODS = [50, 100, 150, 200, 250]

    def initialize(self):
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol

    def update_targets(self):
        if self.algo.IsWarmingUp:
            return False

        # p-1 complete daily bars + today's partial bar = p-bar Donchian, not persisted
        hist = self.history_daily(self.qqq, max(self.PERIODS))
        if len(hist) < max(self.PERIODS) - 1:
            return False
        today_bar = self.get_daily_bar(self.qqq)
        if today_bar is None:
            return False

        price = today_bar.Close
        n_bullish = 0
        for p in self.PERIODS:
            rows = hist.tail(p - 1)
            h = max(rows['high'].max(), today_bar.High)
            l = min(rows['low'].min(),  today_bar.Low)
            if price > (h + l) / 2.0:
                n_bullish += 1
        weight = n_bullish / float(len(self.PERIODS))

        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)


DonchianFiveVoteAlgo = _make_standalone(DonchianFiveVoteSub)
