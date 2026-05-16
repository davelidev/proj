from AlgorithmImports import *

class OutsideBarExpansion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.hi10=self.MAX(self.qqq,10,Resolution.Daily)
        self.bars=RollingWindow[TradeBar](3)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def OnData(self, data):
        if self.qqq in data.Bars: self.bars.Add(data.Bars[self.qqq])

    def Rebalance(self):
        if self.IsWarmingUp or not(self.bars.IsReady and self.hi200.IsReady and self.lo200.IsReady and self.hi10.IsReady): return
        b0=self.bars[0]; b1=self.bars[1]
        outside_up = b0.High > b1.High and b0.Low < b1.Low and b0.Close > b0.Open
        mid=(self.hi200.Current.Value+self.lo200.Current.Value)/2.0
        in_trend=self.Securities[self.qqq].Price>mid
        if not self.Portfolio[self.tqqq].Invested:
            if outside_up and in_trend:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if (not in_trend) or self.Securities[self.qqq].Price>=self.hi10.Current.Value*0.999:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
