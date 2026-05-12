from AlgorithmImports import *


class Algo070(QCAlgorithm):
    """#70 — 5 most market capital companies, monthly momentum top 3."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Sel)
        self.SetWarmUp(220, Resolution.Daily)
        self.top5 = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 30), self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top5 = [f.Symbol for f in elig[:5]]
        return self.top5

    def R(self):
        if self.IsWarmingUp or not self.top5: return
        hist = self.History(self.top5, 25, Resolution.Daily)
        if hist.empty or len(hist.index.levels[0]) < len(self.top5):
            return

        def momentum(sym):
            df = hist.loc[sym]
            if len(df) < 22:
                return -1e9
            recent = df["close"].iloc[-1]
            past = df["close"].iloc[-22]
            return recent / past - 1.0

        ranked = sorted(self.top5, key=momentum, reverse=True)
        top3 = ranked[:3]

        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in top3:
                self.Liquidate(sym)
        for sym in top3:
            self.SetHoldings(sym, 1.0 / 3.0)
