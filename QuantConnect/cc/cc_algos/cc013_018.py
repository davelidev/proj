from AlgorithmImports import *

class D_Mom20_RNG_T3_2(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        
        self.SetWarmUp(280, Resolution.Daily); self.symbols=[]; self.state=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
    def CoarseSelection(self, coarse):
        return [x.Symbol for x in sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)[:100]]
    def FineSelection(self, fine):
        self.symbols=[x.Symbol for x in sorted(fine, key=lambda x: x.MarketCap, reverse=True)[:3]]
        return self.symbols
    def Rebalance(self):
        if self.IsWarmingUp or not self.symbols: return
        h=self.History(self.qqq, 252, Resolution.Daily)
        if h.empty or len(h)<252: return
        c=[float(x) for x in h["close"].values]
        v=[float(x) for x in h["volume"].values]
        med=sorted(c[-200:])[100]
        in_trend=self.Securities[self.qqq].Price>med
        try:
            f1 = c[-1] > c[-21]
            f2 = sum(float(h["high"].iloc[i])-float(h["low"].iloc[i]) for i in range(-25,0))/25 > sum(float(h["high"].iloc[i])-float(h["low"].iloc[i]) for i in range(-200,0))/200 * 1.1
        except Exception: return
        n = int(in_trend)+int(f1)+int(f2)
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
