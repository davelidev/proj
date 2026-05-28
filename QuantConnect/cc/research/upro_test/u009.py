from AlgorithmImports import *
class U009(QCAlgorithm):
    """QQQ up-day count(20) > 10 → 100% UPRO; else cash. UPRO generalization of ensemble/009."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q    = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.upro = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.SetWarmUp(25, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q, 30), self.R)
    def R(self):
        if self.IsWarmingUp: return
        h = self.History(self.q, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return
        c       = [float(x) for x in h["close"].values]
        up_days = sum(1 for i in range(1, len(c)) if c[i] > c[i-1])
        if up_days > 10:
            self.SetHoldings(self.upro, 1.0)
        else:
            self.Liquidate(self.upro)
    def OnData(self, d): pass
