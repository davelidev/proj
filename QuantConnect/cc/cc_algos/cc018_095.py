from AlgorithmImports import *
class CC18_095(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(75,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _roc(self,sym,p):
        h=self.History(sym,p+1,Resolution.Daily)
        if h.empty or len(h)<p+1: return None
        c=[float(x) for x in h["close"].values]
        return (c[-1]/c[0]-1)*100 if c[0] else None
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            r1=self._roc(self.syms[t],20); r3=self._roc(self.syms[t],63)
            if r1 is not None and r3 is not None and r1>0 and r1>r3: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
