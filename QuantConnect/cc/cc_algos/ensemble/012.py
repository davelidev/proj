from AlgorithmImports import *

class Price126D(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq, 45), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h = self.History(self.qqq, 126, Resolution.Daily)
        if h.empty or len(h) < 126: return
        closes = [float(x) for x in h["close"].values]
        lo, hi = min(closes), max(closes)
        if hi == lo: return
        pct = (closes[-1] - lo) / (hi - lo)
        if pct > 0.5: self.SetHoldings(self.tqqq, 1.0)
        elif self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
