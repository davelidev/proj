from AlgorithmImports import *


class Algo064(QCAlgorithm):
    """#64 — 5 most market capital companies + IBS regime mix (IBS<0.2 when QQQ < SMA200)."""

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
        self.Schedule.On(self.DateRules.EveryDay(),
                         self.TimeRules.At(10, 30), self.R)

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
            for s in self.top5:
                cur_w = self.Portfolio[s].HoldingsValue / self.Portfolio.TotalPortfolioValue if self.Portfolio.TotalPortfolioValue > 0 else 0
                if abs(cur_w - w) > 0.05:
                    self.SetHoldings(s, w)
        else:
            targets = []
            for s in self.top5:
                bar = self.Securities[s]
                h, l, c = bar.High, bar.Low, bar.Close
                if h <= l: continue
                ibs = (c - l) / (h - l)
                if ibs < 0.2: targets.append(s)
            for s in self.Portfolio.Keys:
                if self.Portfolio[s].Invested and s not in targets:
                    self.Liquidate(s)
            if targets:
                w = 1.0 / len(targets)
                for s in targets: self.SetHoldings(s, w)
