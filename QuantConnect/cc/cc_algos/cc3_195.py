from AlgorithmImports import *

class RealizedVolContraction(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.aroon=self.AROON(self.qqq, 25, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(40, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.aroon.IsReady: return
        h=self.History(self.qqq, 30, Resolution.Daily)
        if h.empty or len(h)<30: return
        c=[float(x) for x in h["close"].values]
        r=[c[i]/c[i-1]-1.0 for i in range(1,len(c))]
        recent=r[-5:]; prior=r[5:10]
        sd_rec=(sum((x-sum(recent)/5)**2 for x in recent)/5)**0.5
        sd_pri=(sum((x-sum(prior)/5)**2 for x in prior)/5)**0.5
        vol_falling = sd_rec < sd_pri
        regime = self.aroon.AroonUp.Current.Value > self.aroon.AroonDown.Current.Value
        if not self.Portfolio[self.tqqq].Invested:
            if vol_falling and regime:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if not regime:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
