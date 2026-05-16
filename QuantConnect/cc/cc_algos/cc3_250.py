from AlgorithmImports import *

class Top3OfTop5_Median(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(220, Resolution.Daily); self.symbols=[]
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not self.symbols: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        # rank top-5 by 20-day return; hold top 3 only when in_trend
        if not in_trend:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.bil): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            if not self.Portfolio[self.bil].Invested:
                self.SetHoldings(self.bil, 1.0)
            return
        if self.Portfolio[self.bil].Invested: self.Liquidate(self.bil)
        rets={}
        for s in self.symbols:
            hs=self.History(s, 20, Resolution.Daily)
            if hs.empty or len(hs)<20: rets[s]=-1e9; continue
            try: rets[s]=float(hs["close"].iloc[-1])/float(hs["close"].iloc[0])-1.0
            except Exception: rets[s]=-1e9
        top3=sorted(self.symbols, key=lambda s: rets[s], reverse=True)[:3]
        tgt=set(top3)
        for sym in list(self.Securities.Keys):
            if sym in (self.qqq, self.bil): continue
            if self.Portfolio[sym].Invested and sym not in tgt: self.Liquidate(sym)
        w=1.0/len(top3)
        for s in top3: self.SetHoldings(s,w)

    def OnData(self, data): pass
