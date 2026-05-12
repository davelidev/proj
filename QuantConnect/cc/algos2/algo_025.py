from AlgorithmImports import *


class Algo025(QCAlgorithm):
    """#25 — 3 most market capital companies, equal weight, monthly."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Select)
        self.SetWarmUp(20, Resolution.Daily)
        self.top = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0),
                         self.Rebalance)

    def Select(self, fundamental):
        elig = [f for f in fundamental if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top = [f.Symbol for f in elig[:3]]
        return self.top

    def Rebalance(self):
        if self.IsWarmingUp or not self.top: return
        w = 1.0 / len(self.top)
        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in self.top:
                self.Liquidate(sym)
        for sym in self.top:
            self.SetHoldings(sym, w)
