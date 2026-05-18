from AlgorithmImports import *

class Top5MomentumRotation(QCAlgorithm):
    """Top-5 mega-cap (by market cap), monthly hold the 3 best by 60-day return."""
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
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if not self.symbols: return
        rets = {}
        for s in self.symbols:
            hist = self.History(s, 60, Resolution.Daily)
            if hist.empty or len(hist) < 60:
                rets[s] = -1e9
                continue
            try:
                rets[s] = float(hist["close"].iloc[-1]) / float(hist["close"].iloc[0]) - 1.0
            except Exception:
                rets[s] = -1e9
        top3 = sorted(self.symbols, key=lambda s: rets[s], reverse=True)[:3]
        target = set(top3)
        for sym in list(self.Securities.Keys):
            if sym != self.spy and self.Portfolio[sym].Invested and sym not in target:
                self.Liquidate(sym)
        w = 1.0 / len(top3)
        for s in top3:
            self.SetHoldings(s, w)

    def OnData(self, data): pass
