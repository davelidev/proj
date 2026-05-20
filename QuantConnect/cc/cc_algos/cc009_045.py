from AlgorithmImports import *

class WVF_Median_CalmEntry(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi22=self.MAX(self.qqq, 22, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.hi22.IsReady: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        price=self.Securities[self.qqq].Price
        wvf=(self.hi22.Current.Value - price)/self.hi22.Current.Value*100
        # Low VIX-fix = calm; long when calm AND trend
        if in_trend and wvf < 3:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        elif wvf > 8 or not in_trend:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
