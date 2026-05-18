from AlgorithmImports import *

class Top5MegaCapWithDonchianGate(QCAlgorithm):
    """Top-5 mega-cap equal weight when QQQ > 200-day Donchian midline; else 100% BIL."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol

        self.high200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.low200  = self.MIN(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)

        self.symbols = []
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.high200.IsReady and self.low200.IsReady):
            return
        midline = (self.high200.Current.Value + self.low200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        in_trend = price > midline

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

    def OnData(self, data):
        pass
