from AlgorithmImports import *

class Top5MegaCapAroonWeighted(QCAlgorithm):
    """Top-5 mega-cap, weight = AroonUp(25) per name, normalized."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.symbols = []
        self.aroon = {}  # symbol -> aroon indicator
        self.Schedule.On(self.DateRules.MonthStart(self.spy),
                         self.TimeRules.AfterMarketOpen(self.spy, 30),
                         self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]

    def FineSelection(self, fine):
        self.symbols = [x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def OnSecuritiesChanged(self, changes):
        for s in changes.AddedSecurities:
            sym = s.Symbol
            if sym in self.aroon: continue
            self.aroon[sym] = self.AROON(sym, 25, Resolution.Daily)
        for s in changes.RemovedSecurities:
            sym = s.Symbol
            if sym in self.aroon:
                self.aroon.pop(sym, None)

    def Rebalance(self):
        if not self.symbols: return
        scores = {}
        for s in self.symbols:
            ar = self.aroon.get(s)
            if ar is None or not ar.IsReady:
                scores[s] = 50.0  # neutral
            else:
                scores[s] = max(ar.AroonUp.Current.Value - ar.AroonDown.Current.Value, 0.0) + 1.0
        total = sum(scores.values())
        if total <= 0: return
        weights = {s: v / total for s, v in scores.items()}

        target = set(self.symbols)
        for sym in list(self.Securities.Keys):
            if sym != self.spy and self.Portfolio[sym].Invested and sym not in target:
                self.Liquidate(sym)
        for s, w in weights.items():
            self.SetHoldings(s, w)

    def OnData(self, data): pass
