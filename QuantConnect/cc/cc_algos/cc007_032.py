from AlgorithmImports import *

class ThreeStateDDLevels(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi60=self.MAX(self.qqq, 60, Resolution.Daily)
        self.hi200=self.MAX(self.qqq, 200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.hi60.IsReady and self.hi200.IsReady): return
        price=self.Securities[self.qqq].Price
        dd60=price/self.hi60.Current.Value-1.0
        dd200=price/self.hi200.Current.Value-1.0
        if dd60 > -0.03 and dd200 > -0.05: ns,wt,wb="BULL",1.0,0.0
        elif dd60 > -0.10 or dd200 > -0.10: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
