from AlgorithmImports import *


class Algo016(QCAlgorithm):
    """TQQQ gap-up continuation: enter next-day after bullish gap-and-go; exit on 3-day hold or close < entry-day low."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.in_position = False
        self.entry_day_low = None
        self.days_held = 0
        self.max_hold = 3
        self.pending_entry = False

        self.SetWarmUp(5, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not data.ContainsKey(self.tqqq) or data[self.tqqq] is None:
            return

        bar = data[self.tqqq]
        today_open = bar.Open
        today_high = bar.High
        today_low = bar.Low
        today_close = bar.Close

        # Execute pending entry on this bar's open conceptually -- enter at this bar's close (start of next day's bar)
        if self.pending_entry and not self.in_position:
            self.SetHoldings(self.tqqq, 1.0)
            self.in_position = True
            self.days_held = 0
            self.pending_entry = False
            return

        if self.in_position:
            self.days_held += 1
            if self.entry_day_low is not None and today_close < self.entry_day_low:
                self.Liquidate()
                self.in_position = False
                self.days_held = 0
                self.entry_day_low = None
                return
            if self.days_held >= self.max_hold:
                self.Liquidate()
                self.in_position = False
                self.days_held = 0
                self.entry_day_low = None
                return

        # Detect gap-up signal using yesterday from history
        if not self.in_position and not self.pending_entry:
            hist = self.History(self.tqqq, 2, Resolution.Daily)
            if hist is None or hist.empty:
                return
            try:
                highs = hist["high"]
            except Exception:
                return
            if len(highs) < 1:
                return
            prev_high = highs.iloc[-1]

            if today_open > prev_high and today_close > today_open:
                # gap-and-go fired today; queue entry next bar
                self.pending_entry = True
                self.entry_day_low = today_low
