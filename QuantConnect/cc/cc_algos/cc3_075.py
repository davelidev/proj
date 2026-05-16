from AlgorithmImports import *

class Top5PlusTQQQOverlay(QCAlgorithm):
    """Always 70% in top-5 mega-cap basket; add 30% TQQQ overlay only when QQQ > 200d Donchian midline."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)

        self.symbols = []
        self.state = None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not (self.hi200.IsReady and self.lo200.IsReady):
            return
        if not self.symbols: return
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        bull = self.Securities[self.qqq].Price > mid
        ns = "BULL" if bull else "BEAR"
        if ns == self.state: return

        target = set(self.symbols) | {self.tqqq}
        for sym in list(self.Securities.Keys):
            if sym == self.qqq: continue
            if self.Portfolio[sym].Invested and sym not in target:
                self.Liquidate(sym)

        w_mega = 0.7 / len(self.symbols)
        for s in self.symbols:
            self.SetHoldings(s, w_mega)
        if bull:
            self.SetHoldings(self.tqqq, 0.3)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
        self.state = ns

    def OnData(self, data): pass
