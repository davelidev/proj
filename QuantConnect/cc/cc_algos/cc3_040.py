from AlgorithmImports import *

class TQQQMegaCap5050Blend(QCAlgorithm):
    """Always invested: 50% TQQQ + 50% top-5 mega-cap equal weight, monthly rebalance."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.symbols = []
        self.Schedule.On(self.DateRules.MonthStart(self.spy),
                         self.TimeRules.AfterMarketOpen(self.spy, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if not self.symbols: return
        per_mega = 0.5 / len(self.symbols)
        target = set(self.symbols) | {self.tqqq}
        for sym in list(self.Securities.Keys):
            if sym in (self.spy,): continue
            if self.Portfolio[sym].Invested and sym not in target:
                self.Liquidate(sym)
        self.SetHoldings(self.tqqq, 0.5)
        for s in self.symbols:
            self.SetHoldings(s, per_mega)

    def OnData(self, data): pass
