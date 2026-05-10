from AlgorithmImports import *


class Algo013(QCAlgorithm):
    """TQQQ 5-day cumulative drawdown mean-reversion: buy after -8% 5d drop, exit on positive 5d or 7-day max hold."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.lookback = 5
        self.entry_threshold = -0.08
        self.max_hold = 7
        self.days_held = 0
        self.in_position = False

        self.SetWarmUp(15, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not data.ContainsKey(self.tqqq):
            return

        hist = self.History(self.tqqq, self.lookback + 2, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            closes = hist["close"]
        except Exception:
            return
        if len(closes) < self.lookback + 1:
            return

        cum_ret = (closes.iloc[-1] / closes.iloc[-self.lookback - 1]) - 1.0

        if self.in_position:
            self.days_held += 1
            if cum_ret > 0 or self.days_held >= self.max_hold:
                self.Liquidate()
                self.in_position = False
                self.days_held = 0
        else:
            if cum_ret < self.entry_threshold:
                self.SetHoldings(self.tqqq, 1.0)
                self.in_position = True
                self.days_held = 0
