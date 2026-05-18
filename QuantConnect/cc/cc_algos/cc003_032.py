from AlgorithmImports import *

class Top5MegaCapMomentumWeighted(QCAlgorithm):
    """Top-5 mega-cap selected by market cap, weighted by 60-day return rank."""
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
        # Compute 60-day return per name
        rets = {}
        for s in self.symbols:
            hist = self.History(s, 60, Resolution.Daily)
            if hist.empty or len(hist) < 60:
                rets[s] = 0.0
                continue
            try:
                rets[s] = float(hist["close"].iloc[-1]) / float(hist["close"].iloc[0]) - 1.0
            except Exception:
                rets[s] = 0.0
        # Rank-weighted: best name gets weight 5, worst 1, normalize
        ranked = sorted(self.symbols, key=lambda s: rets[s], reverse=True)
        n = len(ranked)
        raw = {ranked[i]: (n - i) for i in range(n)}  # 5,4,3,2,1
        total = sum(raw.values())
        weights = {s: v / total for s, v in raw.items()}

        target = set(self.symbols)
        for sym in list(self.Securities.Keys):
            if sym != self.spy and self.Portfolio[sym].Invested and sym not in target:
                self.Liquidate(sym)
        for s, w in weights.items():
            self.SetHoldings(s, w)

    def OnData(self, data): pass
