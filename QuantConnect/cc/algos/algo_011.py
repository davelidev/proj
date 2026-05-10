from AlgorithmImports import *


class Algo011(QCAlgorithm):
    """#11 — 200d SMA trend + 75% TQQQ position cap (de-risked)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma  = self.SMA(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        invested = self.Portfolio[self.tqqq].Invested
        if in_trend and not invested: self.SetHoldings(self.tqqq, 0.75)
        elif not in_trend and invested: self.Liquidate(self.tqqq)
