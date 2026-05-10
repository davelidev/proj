from AlgorithmImports import *


class Algo015(QCAlgorithm):
    """#15 — ROC(126) momentum on QQQ. Long TQQQ when 6mo return > 0."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.roc  = self.ROC(self.qqq, 126, Resolution.Daily)
        self.SetWarmUp(140, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.roc.IsReady: return
        bullish = self.roc.Current.Value > 0
        invested = self.Portfolio[self.tqqq].Invested
        if bullish and not invested: self.SetHoldings(self.tqqq, 1.0)
        elif not bullish and invested: self.Liquidate(self.tqqq)
