from AlgorithmImports import *
class CC18_025(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.syms=[]
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(150,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("BIL"),self.TimeRules.AfterMarketOpen("BIL",30),self.R)
    def _zscore(self,sym,p):
        h=self.History(sym,p,Resolution.Daily)
        if h.empty or len(h)<p: return None
        c=[float(x) for x in h["close"].values]
        mean=sum(c)/len(c); std=(sum((x-mean)**2 for x in c)/len(c))**0.5
        return (c[-1]-mean)/std if std else 0
    def R(self):
        if self.IsWarmingUp or not self.syms: return
        bulls=[]
        for sym in self.syms:
            z20=self._zscore(sym,20); z60=self._zscore(sym,60)
            if z20 is not None and z60 is not None and z20>0 and z60>0:
                bulls.append(sym)
        n=len(bulls)
        for sym in self.syms: self.SetHoldings(sym,1.0/n if sym in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def OnData(self,d): pass
