from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class DonchianFiveVoteSub(BaseSubAlgo):
    """TQQQ weight = n/5 over Donchian midlines (50, 100, 150, 200, 250) — proportional to # of midlines exceeded. Rebalanced daily 10 mins before close."""

    PERIODS = [50, 100, 150, 200, 250]

    def initialize(self):
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        
        # Create manual highs/lows
        unique_periods = sorted(list(set(self.PERIODS)))
        self.high_map = {p: Maximum(p) for p in unique_periods}
        self.low_map = {p: Minimum(p) for p in unique_periods}

        # Warm up the indicators
        history = self.algo.History(self.qqq, 260, Resolution.Daily)
        for index, row in history.iterrows():
            for p in unique_periods:
                self.high_map[p].Update(index[1], row.high)
                self.low_map[p].Update(index[1], row.low)

    def update_targets(self):
        # Get today's high/low up to 3:50 PM
        bar = self.get_daily_bar(self.qqq)
        if bar is None:
            return False
        today_high = bar.High
        today_low = bar.Low
        today_close = bar.Close

        # Update the indicators
        for p in self.high_map:
            self.high_map[p].Update(self.algo.Time, today_high)
            self.low_map[p].Update(self.algo.Time, today_low)

        if self.algo.IsWarmingUp:
            return False

        if not all(self.high_map[p].IsReady and self.low_map[p].IsReady for p in self.high_map):
            return False

        price = today_close
        # Midline of each Donchian channel = (period high + period low) / 2
        n_bullish = sum(
            1 for p in self.PERIODS
            if price > (self.high_map[p].Current.Value + self.low_map[p].Current.Value) / 2.0
        )
        # Weighted: pure proportional n/N
        weight = n_bullish / float(len(self.PERIODS))

        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev


DonchianFiveVoteAlgo = _make_standalone(DonchianFiveVoteSub)
