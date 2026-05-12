from AlgorithmImports import *


class Algo021(QCAlgorithm):
    """#21 — Most market capital company, monthly rebal, no leverage."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Select)
        self.SetWarmUp(20, Resolution.Daily)
        self.top1 = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0),
                         self.Rebalance)

    def Select(self, fundamental):
        elig = [f for f in fundamental if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top1 = [f.Symbol for f in elig[:1]]
        return self.top1

    def Rebalance(self):
        if self.IsWarmingUp or not self.top1: return
        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in self.top1:
                self.Liquidate(sym)
        for sym in self.top1:
            self.SetHoldings(sym, 1.0)
