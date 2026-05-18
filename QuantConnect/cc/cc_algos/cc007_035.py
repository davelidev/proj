from AlgorithmImports import *

class CleanYearRegime(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(280, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 252, Resolution.Daily)
        if h.empty or len(h)<252: return
        c=[float(x) for x in h["close"].values]
        # count days where drawdown > 10%
        peak=c[0]; bad_days=0
        for v in c:
            peak=max(peak,v)
            if v/peak-1 < -0.10: bad_days += 1
        clean = bad_days/len(c) < 0.20
        cur_dd = self.Securities[self.qqq].Price / max(c) - 1
        in_trend = cur_dd > -0.05
        if clean and in_trend:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
