from AlgorithmImports import *

class MonthlyPivot(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.pivot=None; self.r1=None; self.s1=None
        self.Schedule.On(self.DateRules.MonthStart(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.SetMonthlyLevels)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)

    def SetMonthlyLevels(self):
        h=self.History(self.qqq, 22, Resolution.Daily)
        if h.empty or len(h)<22: return
        # prior month: take ~22 bars; use last 22's H/L/C
        hi=float(h["high"].max()); lo=float(h["low"].min()); cl=float(h["close"].iloc[-1])
        self.pivot=(hi+lo+cl)/3.0
        self.r1=2*self.pivot - lo
        self.s1=2*self.pivot - hi

    def Rebalance(self):
        if self.IsWarmingUp or self.pivot is None: return
        price=self.Securities[self.qqq].Price
        bull = price > self.pivot
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
