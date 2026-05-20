from AlgorithmImports import *
class CC18_100(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.syms=[]
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=20; self.SetWarmUp(150,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("BIL"),self.TimeRules.AfterMarketOpen("BIL",30),self.R)
    def _cci(self,sym):
        h=self.History(sym,self._p+1,Resolution.Daily)
        if h.empty or len(h)<self._p: return None
        hi=[float(x) for x in h["high"].values[-self._p:]]
        lo=[float(x) for x in h["low"].values[-self._p:]]
        cl=[float(x) for x in h["close"].values[-self._p:]]
        tp=[(hi[i]+lo[i]+cl[i])/3 for i in range(self._p)]
        ma=sum(tp)/self._p
        md=sum(abs(t-ma) for t in tp)/self._p
        return (tp[-1]-ma)/(0.015*md) if md else 0
    def R(self):
        if self.IsWarmingUp or not self.syms: return
        bulls=[]
        for sym in self.syms:
            v=self._cci(sym)
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
