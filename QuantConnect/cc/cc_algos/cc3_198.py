from AlgorithmImports import *

class QQQvsGLD60(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.gld=self.AddEquity("GLD",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        hq=self.History(self.qqq, 60, Resolution.Daily); hg=self.History(self.gld, 60, Resolution.Daily)
        if hq.empty or hg.empty or len(hq)<60 or len(hg)<60: return
        q_r=float(hq["close"].iloc[-1])/float(hq["close"].iloc[0])-1.0
        g_r=float(hg["close"].iloc[-1])/float(hg["close"].iloc[0])-1.0
        risk_on = q_r > g_r and q_r > 0
        if risk_on:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
