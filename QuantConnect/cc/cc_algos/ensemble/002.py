from datetime import time, timedelta
from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class IBSATRStopSub(BaseSubAlgo):
    """TQQQ/SOXL/TECL basket. Rebalance 10 mins before close using intraday minute data and daily history."""

    def initialize(self):
        # Subscribe to Minute resolution for intraday tracking
        self.basket = [self.algo.AddEquity(t, Resolution.Minute).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        self.entry_price = None

    def update_targets(self):
        if self.algo.IsWarmingUp:
            return False

        # 1. Aggregate today's minute bars up to 3:50 PM
        today = self.get_daily_bar(self.basket[0])
        if today is None:
            return False

        # 2. Fetch last 14 daily bars (excluding today)
        history_daily = self.algo.History(self.basket[0], 14, Resolution.Daily)
        if len(history_daily) < 14:
            return False

        # 3. Calculate today's IBS
        if today.High <= today.Low:
            return False
        ibs = (today.Close - today.Low) / (today.High - today.Low)

        # 4. ATR(14): mean True Range over the 14 daily bars + today's 3:50 PM bar
        hl     = list(zip(history_daily['high'], history_daily['low'])) + [(today.High, today.Low)]
        closes = list(history_daily['close']) + [today.Close]

        tr = [max(h - l, abs(h - pc), abs(l - pc))
              for (h, l), pc in zip(hl[1:], closes[:-1])]
        atr_val = sum(tr) / len(tr)

        # 5. Trading Logic
        prev = dict(self.targets)
        invested = self.basket[0] in self.targets
        weight = 1.0 / len(self.basket)

        if not invested and ibs < 0.1:
            self.targets = {sym: weight for sym in self.basket}
            self.entry_price = today.Close
        elif invested:
            stop_price = (self.entry_price - 3.0 * atr_val) if self.entry_price else 0
            if ibs > 0.9 or today.Close < stop_price:
                self.targets = {}
                self.entry_price = None

        return self.targets != prev


IBSATRStopAlgo = _make_standalone(IBSATRStopSub)
