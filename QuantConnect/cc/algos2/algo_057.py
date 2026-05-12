from AlgorithmImports import *


class Algo057(QCAlgorithm):
    """#57 — 5 most market capital companies, equal-weight, monthly."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Sel)
        self.SetWarmUp(20, Resolution.Daily)
        self.top5 = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0), self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top5 = [f.Symbol for f in elig[:5]]
        return self.top5

    def R(self):
        if self.IsWarmingUp or not self.top5: return
        w = 1.0 / len(self.top5)
        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in self.top5:
                self.Liquidate(sym)
        for s in self.top5:
            self.SetHoldings(s, w)
