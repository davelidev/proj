from AlgorithmImports import *

class Mom60_MFI_OBV_Top1_5state(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.mfi=self.MFI(self.qqq, 14, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily); self.symbols=[]; self.state=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:1]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not self.mfi.IsReady or not self.symbols: return
        top1=self.symbols[0]
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; v=[float(x) for x in h["volume"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        m = c[-1] > c[-60-1]
        m_b = self.mfi.Current.Value > 50
        obv=0.0; obvs=[]
        for i in range(1,len(c)):
            sign = 1 if c[i]>c[i-1] else (-1 if c[i]<c[i-1] else 0)
            obv += sign*v[i]; obvs.append(obv)
        nW=30; ys=obvs[-nW:]; xs=list(range(nW))
        mx=sum(xs)/nW; my=sum(ys)/nW
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(nW))
        den=sum((xs[i]-mx)**2 for i in range(nW))
        slope=num/den if den>0 else 0
        o_b = slope > 0
        n = int(in_trend)+int(m)+int(m_b)+int(o_b)
        # plan: TQQQ, Top1, BIL
        if n==4: plan=(1.0,0.0,0.0)
        elif n==3: plan=(0.65,0.35,0.0)
        elif n==2: plan=(0.3,0.7,0.0)
        elif n==1: plan=(0.0,0.7,0.3)
        else: plan=(0.0,0.3,0.7)
        wt,wm,wc=plan
        if n!=self.state:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, self.bil, top1): continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(top1,wm); self.SetHoldings(self.bil,wc); self.state=n

    def OnData(self, data): pass
