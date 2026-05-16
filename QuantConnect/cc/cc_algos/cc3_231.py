from AlgorithmImports import *

class GarmanKlassVol(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        import math
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        gk_sum=0.0
        for i in range(-20,0):
            hi=float(h["high"].iloc[i]); lo=float(h["low"].iloc[i]); op=float(h["open"].iloc[i]); cl=float(h["close"].iloc[i])
            if hi<=0 or lo<=0 or op<=0 or cl<=0: continue
            gk = 0.5*(math.log(hi/lo))**2 - (2*math.log(2)-1)*(math.log(cl/op))**2
            gk_sum += gk
        gk_vol = (gk_sum/20)**0.5 if gk_sum>0 else 0
        low_vol = gk_vol < 0.015
        if in_trend and low_vol: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or low_vol: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
