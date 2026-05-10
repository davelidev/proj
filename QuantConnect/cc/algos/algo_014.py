from AlgorithmImports import *


class Algo014(QCAlgorithm):
    """#14 — VIX regime: long TQQQ when VIX < 22, flat when above."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        # VIX is a CBOE index — add via AddIndex
        self.vix  = self.AddIndex("VIX", Resolution.Daily).Symbol
        self.SetWarmUp(20, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp: return
        if not self.Securities.ContainsKey(self.vix): return
        v = self.Securities[self.vix].Price
        if v <= 0: return
        invested = self.Portfolio[self.tqqq].Invested
        if v < 22 and not invested: self.SetHoldings(self.tqqq, 1.0)
        elif v >= 22 and invested: self.Liquidate(self.tqqq)
