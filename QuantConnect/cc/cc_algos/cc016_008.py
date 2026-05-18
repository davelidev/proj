from AlgorithmImports import *
class CC16_658(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(70,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,65,Resolution.Daily)
        if h.empty or len(h)<64: return
        cl=float(h['close'].iloc[-1])
        hi63=float(h['high'].max()); lo63=float(h['low'].min())
        w63=(hi63-cl)/(hi63-lo63)*-100 if hi63>lo63 else -50
        s14=h.iloc[-14:]; hi14=float(s14['high'].max()); lo14=float(s14['low'].min())
        w14=(hi14-cl)/(hi14-lo14)*-100 if hi14>lo14 else -50
        # Dip-buy within quarterly uptrend: enter on short-term oversold, exit on overbought or trend break
        if w63>-50 and w14<-80: st=1      # trend up + short-term dip → long
        elif w63<-50 or w14>-20: st=0     # trend down or short-term overbought → cash
        else: return
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
