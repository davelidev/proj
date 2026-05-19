from AlgorithmImports import *
class CC18_068(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._ema={t:self.EMA(self.syms[t],20,Resolution.Daily) for t in self.tix}
        self.SetWarmUp(35,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            if not self._ema[t].IsReady: continue
            h=self.History(self.syms[t],2,Resolution.Daily)
            if h.empty: continue
            hi=float(h["high"].values[-1])
            if hi>self._ema[t].Current.Value: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
