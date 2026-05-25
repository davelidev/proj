from AlgorithmImports import *

class CMO20(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq, 45), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h = self.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return
        c = [float(x) for x in h["close"].values]
        changes = [c[i] - c[i-1] for i in range(1, len(c))]
        up  = sum(x for x in changes if x > 0)
        dn  = sum(-x for x in changes if x < 0)
        tot = up + dn
        cmo = 0 if tot == 0 else 100 * (up - dn) / tot
        if cmo > 0: self.SetHoldings(self.tqqq, 1.0)
        elif self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
