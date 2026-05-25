from AlgorithmImports import *

class RangeExpanded(QCAlgorithm):
    """Trend (price > 200d median) + range compressed (<110% avg): bull=100%, mixed=50%, bear=0%."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq, 45), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h = self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h) < 200: return
        closes    = [float(x) for x in h["close"].values]
        med       = sorted(closes)[100]
        in_trend  = self.Securities[self.qqq].Price > med
        recent_r  = [float(h["high"].iloc[i]) - float(h["low"].iloc[i]) for i in range(-25, 0)]
        all_r     = [float(h["high"].iloc[i]) - float(h["low"].iloc[i]) for i in range(-200, 0)]
        compressed = (sum(recent_r) / 25) < (sum(all_r) / 200) * 1.1
        if in_trend and compressed:   wt = 1.0
        elif in_trend or compressed:  wt = 0.5
        else:                         wt = 0.0
        if wt > 0: self.SetHoldings(self.tqqq, wt)
        elif self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
