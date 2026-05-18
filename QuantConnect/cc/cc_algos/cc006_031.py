from AlgorithmImports import *

class NR7Break(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(30, Resolution.Daily)
        self.nr7_high=None
        self.armed_days=0

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 7, Resolution.Daily)
        if h.empty or len(h)<7: return
        ranges=[float(h["high"].iloc[i])-float(h["low"].iloc[i]) for i in range(7)]
        # yesterday's range smallest of last 7
        if ranges[-1] == min(ranges):
            self.nr7_high = float(h["high"].iloc[-1])
            self.nr7_low = float(h["low"].iloc[-1])
            self.armed_days = 3
        if self.nr7_high is None: return
        price = self.Securities[self.qqq].Price
        if not self.Portfolio[self.tqqq].Invested:
            if price > self.nr7_high and self.armed_days > 0:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if price < self.nr7_low:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)
        self.armed_days = max(0, self.armed_days - 1)

    def OnData(self, data): pass
