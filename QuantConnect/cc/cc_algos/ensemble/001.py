from AlgorithmImports import *

class LeveragedRebalance(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq), self.TimeRules.AfterMarketOpen(self.tqqq, 45), self.Rebalance)
        self._last_year = None

    def Rebalance(self):
        if self.IsWarmingUp: return
        if self.Time.year == self._last_year: return
        self._last_year = self.Time.year
        self.SetHoldings(self.tqqq, 0.6)
