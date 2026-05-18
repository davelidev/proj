from AlgorithmImports import *

class Top1MegaCapMonthly(QCAlgorithm):
    """Single-name maximum concentration: hold the #1 mega-cap by market cap, refresh monthly."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.symbols = []
        self.Schedule.On(self.DateRules.MonthStart(self.spy),
                         self.TimeRules.AfterMarketOpen(self.spy, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:1]]
        return self.symbols

    def Rebalance(self):
        if not self.symbols: return
        s = self.symbols[0]
        for sym in list(self.Securities.Keys):
            if sym != self.spy and self.Portfolio[sym].Invested and sym != s:
                self.Liquidate(sym)
        self.SetHoldings(s, 1.0)

    def OnData(self, data): pass
