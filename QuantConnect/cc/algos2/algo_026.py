from AlgorithmImports import *


class Algo026(QCAlgorithm):
    """TQQQ position scaled inversely to QQQ Bollinger %B (mean-reversion sizing)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.bb = self.BB(self.qqq, 20, 2, MovingAverageType.Simple, Resolution.Daily)

        self.last_w = -1.0

        self.SetWarmUp(40, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.bb.IsReady:
            return

        upper = self.bb.UpperBand.Current.Value
        lower = self.bb.LowerBand.Current.Value
        price = self.Securities[self.qqq].Price

        if upper == lower:
            return

        pct_b = (price - lower) / (upper - lower)
        w = 1.0 - pct_b
        if w < 0.0:
            w = 0.0
        if w > 1.0:
            w = 1.0

        if abs(w - self.last_w) < 0.05:
            return

        self.SetHoldings(self.tqqq, w)
        self.last_w = w
