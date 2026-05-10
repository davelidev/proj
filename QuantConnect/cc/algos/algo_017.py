from AlgorithmImports import *


class Algo017(QCAlgorithm):
    """#17 — 5 most market capital companies, equal-weight, monthly."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.SelectTop5)
        self.SetWarmUp(20, Resolution.Daily)
        self.top5 = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0),
                         self.Rebalance)

    def SelectTop5(self, fundamental):
        # Filter: tradable, has fundamentals, equity
        eligible = [f for f in fundamental
                    if f.HasFundamentalData
                    and f.MarketCap > 0
                    and f.Price > 5]
        eligible.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top5 = [f.Symbol for f in eligible[:5]]
        return self.top5

    def Rebalance(self):
        if self.IsWarmingUp: return
        if not self.top5: return
        weight = 1.0 / len(self.top5)
        # Liquidate anything not in top5
        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in self.top5:
                self.Liquidate(sym)
        for sym in self.top5:
            self.SetHoldings(sym, weight)
