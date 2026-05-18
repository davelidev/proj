from AlgorithmImports import *
class CC17_067(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=["AAPL","MSFT","AMZN","NVDA","GOOGL"]
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._aroon={t:self.AROON(self.syms[t],14,Resolution.Daily) for t in self.tix}
        self._thresh=10; self.SetWarmUp(19,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[t for t in self.tix if self._aroon[t].IsReady and self._aroon[t].Current.Value>self._thresh]
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
