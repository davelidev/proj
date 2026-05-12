from AlgorithmImports import *


class Algo063(QCAlgorithm):
    """#63 — 3 most market capital companies + SMA200 gate."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Sel)
        self.SetWarmUp(220, Resolution.Daily)
        self.top3 = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0), self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top3 = [f.Symbol for f in elig[:3]]
        return self.top3

    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.top3: return
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        if in_trend:
            w = 1.0 / len(self.top3)
            for sym in list(self.Portfolio.Keys):
                if self.Portfolio[sym].Invested and sym not in self.top3:
                    self.Liquidate(sym)
            for s in self.top3: self.SetHoldings(s, w)
        else:
            for sym in list(self.Portfolio.Keys):
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
