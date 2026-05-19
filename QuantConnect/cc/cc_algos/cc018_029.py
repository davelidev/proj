from AlgorithmImports import *
class CC18_029(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(110,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _coppock(self,sym,lo,sh,sm):
        n=lo+sm+2
        h=self.History(sym,n,Resolution.Daily)
        if h.empty or len(h)<n: return None
        c=[float(x) for x in h["close"].values]
        roc_vals=[]
        for i in range(sm):
            idx=len(c)-sm+i
            if c[idx-lo]!=0 and c[idx-sh]!=0:
                roc_vals.append((c[idx]-c[idx-lo])/c[idx-lo]*100+(c[idx]-c[idx-sh])/c[idx-sh]*100)
            else: roc_vals.append(0)
        w=list(range(1,sm+1)); denom=sum(w)
        return sum(w[i]*roc_vals[i] for i in range(sm))/denom
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            v_slow=self._coppock(self.syms[t],55,43,40)
            v_fast=self._coppock(self.syms[t],20,15,15)
            if v_slow is not None and v_fast is not None and v_slow>0 and v_fast>0:
                bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
