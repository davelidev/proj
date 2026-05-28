from AlgorithmImports import *
class U007(QCAlgorithm):
    """QQQ CMO(20) > 0 → 100% UPRO; else cash. UPRO generalization of ensemble/007."""
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
        changes = [c[i] - c[i-1] for i in range(1, len(c))]
        up  = sum(x for x in changes if x > 0)
        dn  = sum(-x for x in changes if x < 0)
        tot = up + dn
        cmo = 0 if tot == 0 else 100 * (up - dn) / tot
        if cmo > 0:
            self.SetHoldings(self.upro, 1.0)
        else:
            self.Liquidate(self.upro)
    def OnData(self, d): pass
