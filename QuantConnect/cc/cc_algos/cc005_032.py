from AlgorithmImports import *

class Top5_HighestROC60(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.spy=self.AddEquity("SPY",Resolution.Daily).Symbol
        self.symbols=[]
        self.Schedule.On(self.DateRules.MonthStart(self.spy), self.TimeRules.AfterMarketOpen(self.spy,30), self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if not self.symbols: return
        rets={}
        for s in self.symbols:
            h=self.History(s, 60, Resolution.Daily)
            if h.empty or len(h)<60: rets[s]=-1e9; continue
            try: rets[s]=float(h["close"].iloc[-1])/float(h["close"].iloc[0])-1.0
            except Exception: rets[s]=-1e9
        best=max(self.symbols, key=lambda s: rets[s])
        for sym in list(self.Securities.Keys):
            if sym!=self.spy and self.Portfolio[sym].Invested and sym!=best: self.Liquidate(sym)
        self.SetHoldings(best, 1.0)

    def OnData(self, data): pass
