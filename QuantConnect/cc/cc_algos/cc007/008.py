from AlgorithmImports import *

class ThreeState_Aroon_CMO(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.aroon=self.AROON(self.qqq, 25, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(60, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not self.aroon.IsReady: return
        h=self.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h)<21: return
        c=[float(x) for x in h["close"].values]
        ch=[c[i]-c[i-1] for i in range(1,len(c))]
        up=sum(x for x in ch if x>0); dn=sum(-x for x in ch if x<0); tot=up+dn
        if tot<=0: return
        cmo=100.0*(up-dn)/tot
        ar_up=self.aroon.AroonUp.Current.Value; ar_dn=self.aroon.AroonDown.Current.Value
        a_bull = ar_up>70 and ar_up>ar_dn
        c_bull = cmo>0
        if a_bull and c_bull: ns,wt,wb="BULL",1.0,0.0
        elif a_bull or c_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
