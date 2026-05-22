from AlgorithmImports import *
class CC18_014(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.syms=[]
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=15; self.SetWarmUp(150,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("BIL"),self.TimeRules.AfterMarketOpen("BIL",30),self.R)
    def _trix(self,sym):
        n=self._p*3+5
        h=self.History(sym,n,Resolution.Daily)
        if h.empty or len(h)<n: return None
        c=[float(x) for x in h["close"].values]
        k=2.0/(self._p+1)
        e1=[c[0]]
        for v in c[1:]: e1.append(v*k+e1[-1]*(1-k))
        e2=[e1[0]]
        for v in e1[1:]: e2.append(v*k+e2[-1]*(1-k))
        e3=[e2[0]]
        for v in e2[1:]: e3.append(v*k+e3[-1]*(1-k))
        if len(e3)<2 or e3[-2]==0: return None
        return (e3[-1]-e3[-2])/e3[-2]*100
    def R(self):
        if self.IsWarmingUp or not self.syms: return
        bulls=[]
        for sym in self.syms:
            v=self._trix(sym)
            price=self.Securities[sym].Price
            if v is not None and v>0:
                bulls.append(sym)
        n=len(bulls)
        for sym in self.syms: self.SetHoldings(sym,1.0/n if sym in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def OnData(self,d): pass
