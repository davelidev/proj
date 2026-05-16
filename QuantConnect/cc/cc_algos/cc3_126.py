from AlgorithmImports import *

class VolumeSpikeUp(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.hi10=self.MAX(self.qqq,10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.hi200.IsReady and self.lo200.IsReady and self.hi10.IsReady): return
        h=self.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h)<21: return
        vols=[float(v) for v in h["volume"].values[:-1]]
        last_v=float(h["volume"].iloc[-1])
        last_o=float(h["open"].iloc[-1]); last_c=float(h["close"].iloc[-1])
        avg_v=sum(vols)/len(vols)
        spike_up = last_v > 1.5*avg_v and last_c > last_o
        mid=(self.hi200.Current.Value+self.lo200.Current.Value)/2.0
        in_trend=self.Securities[self.qqq].Price>mid
        if not self.Portfolio[self.tqqq].Invested:
            if spike_up and in_trend:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if (not in_trend) or self.Securities[self.qqq].Price>=self.hi10.Current.Value*0.999:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
