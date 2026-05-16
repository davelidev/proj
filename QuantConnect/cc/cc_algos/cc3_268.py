from AlgorithmImports import *

class PriceAboveBoth_4state(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.h9=self.MAX(self.qqq, 9, Resolution.Daily); self.l9=self.MIN(self.qqq, 9, Resolution.Daily)
        self.h26=self.MAX(self.qqq, 26, Resolution.Daily); self.l26=self.MIN(self.qqq, 26, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.h9.IsReady and self.l9.IsReady and self.h26.IsReady and self.l26.IsReady): return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        tenkan=(self.h9.Current.Value+self.l9.Current.Value)/2.0
        kijun=(self.h26.Current.Value+self.l26.Current.Value)/2.0
        price=self.Securities[self.qqq].Price
        bulls = int(in_trend) + int(price > tenkan) + int(price > kijun)
        plan={3:(1.0,0.0),2:(0.7,0.3),1:(0.3,0.7),0:(0.0,1.0)}
        wt,wb = plan[bulls]
        if bulls != self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=bulls

    def OnData(self, data): pass
