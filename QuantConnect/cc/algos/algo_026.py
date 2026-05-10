from AlgorithmImports import *


class Algo026(QCAlgorithm):
    """#26 — 5 most market capital companies, cap-weighted, monthly."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Select)
        self.SetWarmUp(20, Resolution.Daily)
        self.top_data = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0),
                         self.Rebalance)

    def Select(self, fundamental):
        elig = [f for f in fundamental if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top_data = [(f.Symbol, f.MarketCap) for f in elig[:5]]
        return [s for s, _ in self.top_data]

    def Rebalance(self):
        if self.IsWarmingUp or not self.top_data: return
        total_mc = sum(mc for _, mc in self.top_data)
        if total_mc <= 0: return
        weights = {s: mc / total_mc for s, mc in self.top_data}
        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in weights:
                self.Liquidate(sym)
        for sym, w in weights.items():
            self.SetHoldings(sym, w)
