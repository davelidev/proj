from AlgorithmImports import *

class VR_Skew_Top3(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(220, Resolution.Daily); self.symbols=[]; self.state=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:3]]
        return self.symbols
    def Rebalance(self):
        if self.IsWarmingUp or not self.symbols: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        r=[c[i]/c[i-1]-1.0 for i in range(1,len(c))]
        mn=sum(r)/len(r); var1=sum((x-mn)**2 for x in r)/len(r)
        r5=[c[i]/c[i-5]-1.0 for i in range(5,len(c))]
        m5=sum(r5)/len(r5); var5=sum((x-m5)**2 for x in r5)/len(r5)
        vr_b = var1>0 and var5/(5*var1) > 1.0
        # skewness over last 60 returns
        r60=r[-60:]; mn60=sum(r60)/len(r60); sd60=(sum((x-mn60)**2 for x in r60)/len(r60))**0.5
        sk_b = sd60>0 and sum((x-mn60)**3 for x in r60)/len(r60)/(sd60**3) > 0
        n = int(in_trend)+int(vr_b)+int(sk_b)
        if n==3: plan=(1.0,0.0,0.0)
        elif n==2: plan=(0.5,0.5,0.0)
        elif n==1: plan=(0.0,1.0,0.0)
        else: plan=(0.0,0.5,0.5)
        wt,wm,wc=plan
        if n!=self.state:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, self.bil) or sym in self.symbols: continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            self.SetHoldings(self.tqqq,wt); per=wm/len(self.symbols) if wm>0 else 0
            for s in self.symbols: self.SetHoldings(s, per)
            self.SetHoldings(self.bil,wc); self.state=n

    def OnData(self, data): pass
