from AlgorithmImports import *

class VIXPercentile(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.vix=self.AddData(CBOE,"VIX",Resolution.Daily).Symbol
        self.vix_win=RollingWindow[float](252)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)

    def OnData(self, data):
        if self.vix in data and data[self.vix] is not None:
            self.vix_win.Add(data[self.vix].Price)

    def Rebalance(self):
        if not self.vix_win.IsReady: return
        cur=self.vix_win[0]
        vals=[self.vix_win[i] for i in range(252)]
        srt=sorted(vals)
        pct=srt.index(cur)/252.0 if cur in srt else sum(1 for v in vals if v<=cur)/252.0
        bull = pct < 0.3
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
