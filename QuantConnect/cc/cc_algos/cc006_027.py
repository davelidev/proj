from AlgorithmImports import *

class Top5InverseBeta(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.spy=self.AddEquity("SPY",Resolution.Daily).Symbol
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.symbols=[]
        self.Schedule.On(self.DateRules.MonthStart(self.spy), self.TimeRules.AfterMarketOpen(self.spy,30), self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:5]]
        return self.symbols

    def Rebalance(self):
        if not self.symbols: return
        h_q=self.History(self.qqq, 60, Resolution.Daily)
        if h_q.empty or len(h_q)<60: return
        q_c=[float(x) for x in h_q["close"].values]
        q_r=[q_c[i]/q_c[i-1]-1.0 for i in range(1,len(q_c))]
        q_var=sum((x-sum(q_r)/len(q_r))**2 for x in q_r)/len(q_r)
        inv={}
        for s in self.symbols:
            h=self.History(s, 60, Resolution.Daily)
            if h.empty or len(h)<60: inv[s]=1.0; continue
            try:
                p=[float(x) for x in h["close"].values]
                r=[p[i]/p[i-1]-1.0 for i in range(1,len(p))]
                qm=sum(q_r)/len(q_r); sm=sum(r)/len(r)
                cov=sum((r[i]-sm)*(q_r[i]-qm) for i in range(min(len(r),len(q_r))))/min(len(r),len(q_r))
                beta=cov/q_var if q_var>0 else 1.0
                inv[s] = 1.0/max(abs(beta), 0.1)
            except Exception: inv[s]=1.0
        total=sum(inv.values()); weights={s: v/total for s,v in inv.items()}
        tgt=set(self.symbols)
        for sym in list(self.Securities.Keys):
            if sym not in (self.spy, self.qqq) and self.Portfolio[sym].Invested and sym not in tgt:
                self.Liquidate(sym)
        for s,w in weights.items(): self.SetHoldings(s,w)

    def OnData(self, data): pass
