from AlgorithmImports import *
class U005(QCAlgorithm):
    """QQQ > SMA(150) → 100% UPRO; else cash. UPRO generalization of ensemble/005."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q    = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.upro = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.sma  = self.SMA(self.q, 150, Resolution.Daily)
        self.SetWarmUp(160, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q, 30), self.R)
    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        if self.Securities[self.q].Price > self.sma.Current.Value:
            self.SetHoldings(self.upro, 1.0)
        else:
            self.Liquidate(self.upro)
    def OnData(self, d): pass
