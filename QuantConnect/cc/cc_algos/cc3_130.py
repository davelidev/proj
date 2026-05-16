from AlgorithmImports import *

class InsideDayPattern(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.hi5=self.MAX(self.qqq,5,Resolution.Daily); self.lo5=self.MIN(self.qqq,5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.hi200.IsReady and self.lo200.IsReady and self.hi5.IsReady): return
        h=self.History(self.qqq, 2, Resolution.Daily)
        if h.empty or len(h)<2: return
        ph=float(h["high"].iloc[0]); pl=float(h["low"].iloc[0])
        ch=float(h["high"].iloc[1]); cl=float(h["low"].iloc[1])
        inside = ch<ph and cl>pl
        mid=(self.hi200.Current.Value+self.lo200.Current.Value)/2.0
        in_trend=self.Securities[self.qqq].Price>mid
        if not self.Portfolio[self.tqqq].Invested:
            if inside and in_trend:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if (not in_trend) or self.Securities[self.qqq].Price<=self.lo5.Current.Value*1.001:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
