from AlgorithmImports import *

class WideRangeUpEntry(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.armed=0; self.entry=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        h2=self.History(self.qqq, 11, Resolution.Daily)
        if h2.empty or len(h2)<11: return
        prior_r=[float(h2["high"].iloc[i])-float(h2["low"].iloc[i]) for i in range(10)]
        last_r=float(h2["high"].iloc[-1])-float(h2["low"].iloc[-1])
        last_c=float(h2["close"].iloc[-1]); last_o=float(h2["open"].iloc[-1])
        wide_up = last_r > 1.5 * (sum(prior_r)/10) and last_c > last_o
        if not self.Portfolio[self.tqqq].Invested:
            if wide_up and in_trend:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
                self.armed=10
        else:
            if not in_trend or self.armed<=0:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)
        self.armed = max(0, self.armed-1)

    def OnData(self, data): pass
