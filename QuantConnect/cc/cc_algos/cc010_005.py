from AlgorithmImports import *

class TripleMom_Top3(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
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
        m20 = c[-1] > c[-21]; m60=c[-1]>c[-61]; m120=c[-1]>c[-121]
        n = int(in_trend)+int(m20)+int(m60)+int(m120)
        plan={4:(1.0,0.0),3:(0.5,0.5),2:(0.0,1.0),1:(0.0,1.0),0:(0.0,0.0)}  # last = all out
        wt,wm=plan[n]
        if n!=self.state:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq): continue
                if sym in self.symbols: continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            if n==0:
                if self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
                for s in self.symbols:
                    if self.Portfolio[s].Invested: self.Liquidate(s)
            else:
                self.SetHoldings(self.tqqq, wt)
                per = wm / len(self.symbols) if wm>0 else 0
                for s in self.symbols: self.SetHoldings(s, per)
            self.state=n

    def OnData(self, data): pass
