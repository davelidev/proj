from AlgorithmImports import *

class MFI_WilliamsR_4State(QCAlgorithm):
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
        m_bull=self.mfi.Current.Value>50
        w_bull=self.wilr.Current.Value>-50
        if in_trend and m_bull and w_bull: ns,wt,wb="BULL",1.0,0.0
        elif (in_trend and m_bull) or (in_trend and w_bull): ns,wt,wb="MIXED",0.7,0.3
        elif in_trend or m_bull or w_bull: ns,wt,wb="MIXED2",0.4,0.6
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
