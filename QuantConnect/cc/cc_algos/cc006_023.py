from AlgorithmImports import *

class DaysSince52wHigh(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(270, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 252, Resolution.Daily)
        if h.empty or len(h)<252: return
        closes=[float(x) for x in h["close"].values]
        hi_idx=max(range(len(closes)), key=lambda i: closes[i])
        days_since = len(closes) - 1 - hi_idx
        bull = days_since <= 30
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
