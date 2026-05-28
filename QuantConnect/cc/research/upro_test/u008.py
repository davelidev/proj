from AlgorithmImports import *
class U008(QCAlgorithm):
    """QQQ ROC(20) > 0 → 100% UPRO; else cash. UPRO generalization of ensemble/008."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q    = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.upro = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.roc  = self.ROC("QQQ", 20, Resolution.Daily)
        self.SetWarmUp(25, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q, 30), self.R)
    def R(self):
        if self.IsWarmingUp or not self.roc.IsReady: return
        if self.roc.Current.Value > 0:
            self.SetHoldings(self.upro, 1.0)
        else:
            self.Liquidate(self.upro)
    def OnData(self, d): pass
