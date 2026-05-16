from AlgorithmImports import *

class Top5PosROC60Filter(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.spy=self.AddEquity("SPY",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.symbols=[]
        self.Schedule.On(self.DateRules.MonthStart(self.spy), self.TimeRules.AfterMarketOpen(self.spy,30), self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if not self.symbols: return
        good=[]
        for s in self.symbols:
            h=self.History(s, 60, Resolution.Daily)
            if h.empty or len(h)<60: continue
            try:
                r=float(h["close"].iloc[-1])/float(h["close"].iloc[0])-1.0
                if r>0: good.append(s)
            except Exception: pass
        tgt=set(good)|{self.bil}
        for sym in list(self.Securities.Keys):
            if sym!=self.spy and self.Portfolio[sym].Invested and sym not in tgt: self.Liquidate(sym)
        if good:
            w=1.0/len(good)
            for s in good: self.SetHoldings(s,w)
            if self.Portfolio[self.bil].Invested: self.Liquidate(self.bil)
        else:
            self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
