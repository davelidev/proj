from AlgorithmImports import *
class U002(QCAlgorithm):
    """QQQ RSI(2,Wilder) < 20 → 100% UPRO; else cash. UPRO generalization of ensemble/002."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q    = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.upro = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.rsi2 = self.RSI("QQQ", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.SetWarmUp(10, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q, 30), self.R)
    def R(self):
        if self.IsWarmingUp or not self.rsi2.IsReady: return
        if self.rsi2.Current.Value < 20:
            self.SetHoldings(self.upro, 1.0)
        else:
            self.Liquidate(self.upro)
    def OnData(self, d): pass
