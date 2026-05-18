from AlgorithmImports import *

class Mom30_MFI14_Top3_w30_9(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.ind=self.MFI(self.qqq, 14, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily); self.symbols=[]; self.state=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)

    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:3]]
        return self.symbols

    def Rebalance(self):
        if self.IsWarmingUp or not self.ind.IsReady or not self.symbols: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        m = c[-1] > c[-30-1]
        i_b = self.ind.Current.Value > 50
        n = int(in_trend)+int(m)+int(i_b)
        # adjust middle weight: w_full TQQQ when 3, w_mix in mid
        if n==3: plan=(1.0,0.0,0.0)
        elif n==2: plan=(0.3,0.70,0.0)
        elif n==1: plan=(0.0,1.0,0.0)
        else: plan=(0.0,0.5,0.5)
        wt,wm,wc=plan
        if n!=self.state:
            for sym in list(self.Securities.Keys):
                if sym in (self.qqq, self.tqqq, self.bil) or sym in self.symbols: continue
                if self.Portfolio[sym].Invested: self.Liquidate(sym)
            self.SetHoldings(self.tqqq,wt)
            per = wm/len(self.symbols) if wm>0 else 0
            for s in self.symbols: self.SetHoldings(s, per)
            self.SetHoldings(self.bil,wc); self.state=n

    def OnData(self, data): pass
