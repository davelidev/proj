from AlgorithmImports import *
class CC17_078(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._n=25; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            h=self.History(self.syms[t],self._n+1,Resolution.Daily)
            if h.empty or len(h)<self._n+1: continue
            hi=float(h['high'].iloc[:-1].max())
            lo=float(h['low'].iloc[:-1].min())
            cl=float(h['close'].iloc[-1])
            mid=(hi+lo)/2
            if cl>mid: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
