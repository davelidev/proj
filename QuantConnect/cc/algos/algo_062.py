from AlgorithmImports import *


class Algo062(QCAlgorithm):
    """#62 — 10 most mkt cap + SMA200 trend gate."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Sel)
        self.SetWarmUp(220, Resolution.Daily)
        self.top = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0), self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top = [f.Symbol for f in elig[:10]]
        return self.top

    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.top: return
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        if in_trend:
            w = 1.0 / len(self.top)
            for s in list(self.Portfolio.Keys):
                if self.Portfolio[s].Invested and s not in self.top: self.Liquidate(s)
            for s in self.top: self.SetHoldings(s, w)
        else:
            for s in list(self.Portfolio.Keys):
                if self.Portfolio[s].Invested: self.Liquidate(s)
