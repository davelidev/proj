from AlgorithmImports import *

class Top3MegaCapDonchian200(QCAlgorithm):
    """Top-3 mega-cap when QQQ > 200d Donchian midline; else BIL."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol

        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)

        self.symbols = []
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:3]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.hi200.IsReady and self.lo200.IsReady):
            return
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        in_trend = self.Securities[self.qqq].Price > mid

        if in_trend and self.symbols:
            if self.Portfolio[self.bil].Invested:
                self.Liquidate(self.bil)
            target = set(self.symbols)
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.bil): continue
                if self.Portfolio[sym].Invested and sym not in target:
                    self.Liquidate(sym)
            w = 1.0 / len(self.symbols)
            for s in self.symbols:
                self.SetHoldings(s, w)
        else:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.bil): continue
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            if not self.Portfolio[self.bil].Invested:
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
