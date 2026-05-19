from AlgorithmImports import *
class CC18_022(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=30; self.SetWarmUp(40,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _zscore(self,sym):
        h=self.History(sym,self._p,Resolution.Daily)
        if h.empty or len(h)<self._p: return None
        c=[float(x) for x in h["close"].values]
        mean=sum(c)/len(c)
        std=(sum((x-mean)**2 for x in c)/len(c))**0.5
        if std==0: return 0
        return (c[-1]-mean)/std
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            z=self._zscore(self.syms[t])
            if z is not None and z>0: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
