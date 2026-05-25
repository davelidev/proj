from AlgorithmImports import *

class ROC20(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.roc  = self.ROC(self.qqq, 20, Resolution.Daily)
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq, 45), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.roc.IsReady: return
        if self.roc.Current.Value > 0: self.SetHoldings(self.tqqq, 1.0)
        elif self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
