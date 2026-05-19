from AlgorithmImports import *
class CC18_010(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.symbols=[]; self._st=None; self.SetWarmUp(40,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,coarse):
        return [x.Symbol for x in sorted(coarse,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,fine):
        self.symbols=[x.Symbol for x in sorted(fine,key=lambda x:x.MarketCap,reverse=True)[:5]]
        return self.symbols
    def _slope(self,n):
        h=self.History(self.q,n,Resolution.Daily)
        if h.empty or len(h)<n: return None
        c=[float(x) for x in h["close"].values]
        xm=(n-1)/2; ym=sum(c)/n
        num=sum((i-xm)*(c[i]-ym) for i in range(n))
        den=sum((i-xm)**2 for i in range(n))
        return num/den if den else 0
    def R(self):
        if self.IsWarmingUp or not self.symbols: return
        s=self._slope(30)
        if s is None: return
        st=1 if s>0 else 0
        if st==self._st: return
        self._st=st
        if st==1:
            self.SetHoldings(self.b,0)
            per=1.0/len(self.symbols)
            for sym in self.symbols: self.SetHoldings(sym,per)
        else:
            for sym in self.symbols: self.SetHoldings(sym,0)
            self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
