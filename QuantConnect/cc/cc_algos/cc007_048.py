from AlgorithmImports import *

class Top5RiskParityMedian(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(220, Resolution.Daily); self.symbols=[]
        self.Schedule.On(self.DateRules.MonthStart(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)

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
        for sym in list(self.Securities.Keys):
            if sym in (self.qqq, self.bil): continue
            if self.Portfolio[sym].Invested and sym not in set(self.symbols): self.Liquidate(sym)
        if not in_trend:
            for s in self.symbols:
                if self.Portfolio[s].Invested: self.Liquidate(s)
            if not self.Portfolio[self.bil].Invested:
                self.SetHoldings(self.bil, 1.0)
            return
        if self.Portfolio[self.bil].Invested: self.Liquidate(self.bil)
        invvol={}
        for s in self.symbols:
            hs=self.History(s, 30, Resolution.Daily)
            if hs.empty or len(hs)<30: invvol[s]=1.0; continue
            try:
                p=[float(x) for x in hs["close"].values]
                r=[p[i]/p[i-1]-1.0 for i in range(1,len(p))]
                m=sum(r)/len(r); v=sum((x-m)**2 for x in r)/len(r); sd=v**0.5
                invvol[s]=1.0/sd if sd>0 else 1.0
            except Exception: invvol[s]=1.0
        total=sum(invvol.values()); weights={s: v/total for s,v in invvol.items()}
        for s,w in weights.items(): self.SetHoldings(s,w)

    def OnData(self, data): pass
