from AlgorithmImports import *
class CC19_092(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._atr=self.ATR(self.q,14,Resolution.Daily)
        self._sma=self.SMA(self.q,50,Resolution.Daily)
        self.thr=2.0; self.st=None; self.SetWarmUp(max(14,50)+5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self._atr.IsReady or not self._sma.IsReady: return
        close=self.Securities[self.q].Price
        if close==0: return
        natr=self._atr.Current.Value/close*100
        s=1 if natr<self.thr and close>self._sma.Current.Value else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
