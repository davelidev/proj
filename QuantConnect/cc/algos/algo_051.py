from AlgorithmImports import *


class Algo051(QCAlgorithm):
    """#51 — 5 most mkt cap + cash sleeve when QQQ < SMA200."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Sel)
        self.SetWarmUp(220, Resolution.Daily)
        self.top5 = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0),
                         self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top5 = [f.Symbol for f in elig[:5]]
        return self.top5

    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.top5: return
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        if in_trend:
            w = 1.0 / len(self.top5)
            for sym in list(self.Portfolio.Keys):
                if self.Portfolio[sym].Invested and sym not in self.top5:
                    self.Liquidate(sym)
            for sym in self.top5: self.SetHoldings(sym, w)
        else:
            for sym in list(self.Portfolio.Keys):
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
