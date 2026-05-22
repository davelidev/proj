from AlgorithmImports import *


class Algo053(QCAlgorithm):
    """#53 — Williams %R(2) MR on TQQQ. Buy %R<-90, sell %R>-10."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.t = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.wpr = self.WILR(self.t, 2, Resolution.Daily)
        self.SetWarmUp(10, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.t),
                         self.TimeRules.AfterMarketOpen(self.t, 30),
                         self.R)

    def R(self):
        if self.IsWarmingUp or not self.wpr.IsReady: return
        v = self.wpr.Current.Value
        invested = self.Portfolio[self.t].Invested
        if not invested and v < -90: self.SetHoldings(self.t, 1.0)
        elif invested and v > -10: self.Liquidate(self.t)
