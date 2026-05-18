from AlgorithmImports import *

class MFI_WilliamsR_Median_4state(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.mfi=self.MFI(self.qqq, 14, Resolution.Daily)
        self.wilr=self.WILR(self.qqq, 14, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.mfi.IsReady and self.wilr.IsReady): return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        m_b=self.mfi.Current.Value>50
        w_b=self.wilr.Current.Value>-50
        n=int(in_trend)+int(m_b)+int(w_b)
        plan={3:(1.0,0.0),2:(0.7,0.3),1:(0.3,0.7),0:(0.0,1.0)}
        wt,wb=plan[n]
        if n!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=n

    def OnData(self, data): pass
