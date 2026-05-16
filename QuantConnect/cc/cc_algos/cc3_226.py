from AlgorithmImports import *

class CMF20Pure(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        h2=h.tail(20)
        mfv=0.0; v_sum=0.0
        for i in range(len(h2)):
            hi=float(h2["high"].iloc[i]); lo=float(h2["low"].iloc[i]); cl=float(h2["close"].iloc[i]); vl=float(h2["volume"].iloc[i])
            if hi==lo: m=0
            else: m=((cl-lo)-(hi-cl))/(hi-lo)
            mfv += m*vl; v_sum += vl
        if v_sum<=0: return
        cmf = mfv/v_sum
        c_bull = cmf > 0
        if in_trend and c_bull: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or c_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
