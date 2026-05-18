from AlgorithmImports import *

class MegaCapBreakout20d(QCAlgorithm):
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
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:10]]
        return self.symbols

    def Rebalance(self):
        if not self.symbols: return
        breakouts=[]
        for s in self.symbols:
            hist=self.History(s, 20, Resolution.Daily)
            if hist.empty or len(hist)<20: continue
            try:
                hi20=float(hist["high"].iloc[:-1].max()); last=float(hist["close"].iloc[-1])
                if last >= hi20: breakouts.append(s)
            except Exception: continue
        breakouts=breakouts[:5]
        tgt=set(breakouts)
        for sym in list(self.Securities.Keys):
            if sym!=self.spy and self.Portfolio[sym].Invested and sym not in tgt:
                self.Liquidate(sym)
        if not breakouts: return
        w=1.0/len(breakouts)
        for s in breakouts: self.SetHoldings(s,w)

    def OnData(self, data): pass
