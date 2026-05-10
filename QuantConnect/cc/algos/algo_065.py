from AlgorithmImports import *


class Algo065(QCAlgorithm):
    """#65 — 5 most market capital companies, IBS<0.5 daily rotation."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Sel)
        self.SetWarmUp(20, Resolution.Daily)
        self.top5 = []
        self.Schedule.On(self.DateRules.EveryDay(),
                         self.TimeRules.At(10, 30), self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top5 = [f.Symbol for f in elig[:5]]
        return self.top5

    def R(self):
        if self.IsWarmingUp or not self.top5: return
        targets = []
        for s in self.top5:
            bar = self.Securities[s]
            h, l, c = bar.High, bar.Low, bar.Close
            if h <= l: continue
            ibs = (c - l) / (h - l)
            if ibs < 0.5: targets.append(s)
        for s in self.Portfolio.Keys:
            if self.Portfolio[s].Invested and s not in targets:
                self.Liquidate(s)
        if targets:
            w = 1.0 / len(targets)
            for s in targets: self.SetHoldings(s, w)
