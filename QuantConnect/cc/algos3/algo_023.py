from AlgorithmImports import *


class Algo023(QCAlgorithm):
    """Scaled TQQQ position by QQQ 63d ROC strength, rest in BIL."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol

        self.qqq_roc = self.ROC(self.qqq, 63, Resolution.Daily)

        self.last_w = -1.0

        self.SetWarmUp(80, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.qqq_roc.IsReady:
            return

        roc = self.qqq_roc.Current.Value  # decimal: 0.10 = 10%
        w = (roc + 0.05) * 5.0
        if w < 0.0:
            w = 0.0
        if w > 1.0:
            w = 1.0

        if abs(w - self.last_w) < 0.05:
            return

        self.SetHoldings(self.tqqq, w)
        self.SetHoldings(self.bil, 1.0 - w)
        self.last_w = w
