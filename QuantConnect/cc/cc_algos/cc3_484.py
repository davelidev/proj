from AlgorithmImports import *

class LR_Tenkan_Top3(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.h9=self.MAX(self.qqq,9,Resolution.Daily); self.l9=self.MIN(self.qqq,9,Resolution.Daily)
        self.h26=self.MAX(self.qqq,26,Resolution.Daily); self.l26=self.MIN(self.qqq,26,Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily); self.symbols=[]; self.state=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:3]]
        return self.symbols
    def Rebalance(self):
        if self.IsWarmingUp or not (self.h9.IsReady and self.l9.IsReady and self.h26.IsReady and self.l26.IsReady) or not self.symbols: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        ys=c[-50:]; nL=50; xs=list(range(nL))
        mx=sum(xs)/nL; my=sum(ys)/nL
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(nL))
        den=sum((xs[i]-mx)**2 for i in range(nL))
        slope=num/den if den>0 else 0
        lr_b = slope > 0
        tenkan=(self.h9.Current.Value+self.l9.Current.Value)/2.0
        kijun=(self.h26.Current.Value+self.l26.Current.Value)/2.0
        ich_b = tenkan > kijun
        n = int(in_trend)+int(lr_b)+int(ich_b)
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
