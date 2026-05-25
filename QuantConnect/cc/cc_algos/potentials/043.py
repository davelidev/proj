from AlgorithmImports import *
class FourSignal50Vote(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,21,Resolution.Daily)
        if h.empty or len(h)<21: return
        closes=[float(h['close'].iloc[i]) for i in range(len(h))]
        changes=[closes[i]-closes[i-1] for i in range(1,len(closes))]
        # CMO(20) > 0
        up=sum(x for x in changes if x>0); dn=sum(-x for x in changes if x<0)
        tot=up+dn
        cmo=0 if tot==0 else 100*(up-dn)/tot
        # ROC(20) > 0
        roc=closes[-1]>closes[0]
        # UpDay count > 10
        updays=sum(1 for x in changes if x>0)>10
        # TII(20): closes above SMA(20) > 10
        sma=sum(closes[-20:])/20
        tii=sum(1 for c in closes[-20:] if c>sma)>10
        score=sum([cmo>0, roc, updays, tii])
        st=1 if score>=2 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
