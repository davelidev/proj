from AlgorithmImports import *

class VR_MFI_Combined(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.mfi=self.MFI(self.qqq, 14, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not self.mfi.IsReady: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]
        med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        m_bull=self.mfi.Current.Value>50
        # Variance ratio (5d returns vs 1d returns)
        r=[c[i]/c[i-1]-1.0 for i in range(1,len(c))]
        m=sum(r)/len(r); var1=sum((x-m)**2 for x in r)/len(r)
        r5=[c[i]/c[i-5]-1.0 for i in range(5,len(c))]
        m5=sum(r5)/len(r5); var5=sum((x-m5)**2 for x in r5)/len(r5)
        vr_bull = var1>0 and (var5/(5*var1)) > 1.0
        if in_trend and m_bull and vr_bull: ns,wt,wb="BULL",1.0,0.0
        elif in_trend and (m_bull or vr_bull): ns,wt,wb="MIXED",0.6,0.4
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
