from AlgorithmImports import *

class ThreeStateVIXAroon(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.vix=self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.aroon=self.AROON(self.qqq, 25, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(35, Resolution.Daily)
        self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not self.aroon.IsReady or not self.Securities.ContainsKey(self.vix): return
        v=self.Securities[self.vix].Price
        if v<=0: return
        a_bull = self.aroon.AroonUp.Current.Value > self.aroon.AroonDown.Current.Value and self.aroon.AroonUp.Current.Value > 70
        v_low = v < 20
        if a_bull and v_low: ns,wt,wb="BULL",1.0,0.0
        elif a_bull or v_low: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns != self.state:
            self.SetHoldings(self.tqqq, wt); self.SetHoldings(self.bil, wb); self.state=ns

    def OnData(self, data): pass
