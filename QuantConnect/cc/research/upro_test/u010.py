from AlgorithmImports import *
class U010(QCAlgorithm):
    """QQQ TII(20) > 10 → 100% UPRO; else cash. UPRO generalization of ensemble/010."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q    = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.upro = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.sma  = self.SMA("QQQ", 20, Resolution.Daily)
        self.wins = RollingWindow[float](20)
        self.SetWarmUp(25, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q, 30), self.R)
    def OnData(self, d):
        if d.Bars.ContainsKey(self.q):
            self.wins.Add(d.Bars[self.q].Close)
    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.wins.IsReady: return
        sma = self.sma.Current.Value
        tii = sum(1 for i in range(20) if self.wins[i] > sma)
        if tii > 10:
            self.SetHoldings(self.upro, 1.0)
        else:
            self.Liquidate(self.upro)
