from AlgorithmImports import *

class CMO20(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h)<21: return
        c=[float(x) for x in h["close"].values]
        changes=[c[i]-c[i-1] for i in range(1,len(c))]
        sum_up=sum(x for x in changes if x>0)
        sum_dn=sum(-x for x in changes if x<0)
        total = sum_up + sum_dn
        if total<=0: return
        cmo = 100.0 * (sum_up - sum_dn) / total
        if cmo > 0:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
