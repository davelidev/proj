from AlgorithmImports import *


class Algo028(QCAlgorithm):
    """100% TQQQ in uptrend, else 67% TQQQ + 33% SH inverse hedge."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sh = self.AddEquity("SH", Resolution.Daily).Symbol

        self.qqq_sma200 = self.SMA(self.qqq, 200, Resolution.Daily)

        self.last_state = None  # "up" or "down"

        self.SetWarmUp(220, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.qqq_sma200.IsReady:
            return

        price = self.Securities[self.qqq].Price
        sma = self.qqq_sma200.Current.Value
        state = "up" if price > sma else "down"

        if state == self.last_state:
            return

        if state == "up":
            self.SetHoldings(self.sh, 0.0)
            self.SetHoldings(self.tqqq, 1.0)
        else:
            self.SetHoldings(self.tqqq, 0.67)
            self.SetHoldings(self.sh, 0.33)

        self.last_state = state
