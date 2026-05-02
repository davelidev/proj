from AlgorithmImports import *

class DualMomentumTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.roc3 = self.ROC(self.qqq, 63, Resolution.Daily)
        self.roc6 = self.ROC(self.qqq, 126, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), 
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(126)

    def Rebalance(self):
        if not (self.roc3.IsReady and self.roc6.IsReady): return
        
        m3 = self.roc3.Current.Value
        m6 = self.roc6.Current.Value
        
        # Signal: Dual Momentum UP
        if m3 > 0 and m6 > 0:
            if not self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] DUAL MOMENTUM ON. Entering TQQQ.")
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Log(f"[{self.Time}] MOMENTUM STALL. Exiting to Cash.")
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
