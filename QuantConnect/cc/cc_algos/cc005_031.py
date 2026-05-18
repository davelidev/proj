from AlgorithmImports import *

class Top5RiskParity(QCAlgorithm):
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
        invvol={}
        for s in self.symbols:
            h=self.History(s, 30, Resolution.Daily)
            if h.empty or len(h)<30:
                invvol[s]=1.0; continue
            try:
                p=[float(x) for x in h["close"].values]
                r=[p[i]/p[i-1]-1.0 for i in range(1,len(p))]
                m=sum(r)/len(r); v=sum((x-m)**2 for x in r)/len(r); sd=v**0.5
                invvol[s]= 1.0/sd if sd>0 else 1.0
            except Exception: invvol[s]=1.0
        total=sum(invvol.values())
        weights={s: v/total for s,v in invvol.items()}
        tgt=set(self.symbols)
        for sym in list(self.Securities.Keys):
            if sym!=self.spy and self.Portfolio[sym].Invested and sym not in tgt: self.Liquidate(sym)
        for s,w in weights.items(): self.SetHoldings(s,w)

    def OnData(self, data): pass
