from AlgorithmImports import *

class UpDownRatio50(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(70, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 51, Resolution.Daily)
        if h.empty or len(h)<51: return
        c=[float(x) for x in h["close"].values]
        up_n=sum(1 for i in range(1,len(c)) if c[i]>c[i-1])
        ratio=up_n/50.0
        bull = ratio > 0.55
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        elif ratio < 0.45:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
