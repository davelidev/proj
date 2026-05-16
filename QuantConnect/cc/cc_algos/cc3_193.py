from AlgorithmImports import *

class VIXPercentile60d(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.vix=self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)

    def Rebalance(self):
        if not self.Securities.ContainsKey(self.vix): return
        h=self.History(self.vix, 60, Resolution.Daily)
        if h.empty or len(h)<60: return
        vals=sorted(float(x) for x in h["value"].values)
        cur=self.Securities[self.vix].Price
        if cur<=0: return
        pct=sum(1 for v in vals if v <= cur)/len(vals)
        bull = pct < 0.20  # VIX in bottom 20%
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        elif pct > 0.80:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
