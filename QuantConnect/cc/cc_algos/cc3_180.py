from AlgorithmImports import *

class QQQOutperformSPY(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.spy=self.AddEquity("SPY",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        hq=self.History(self.qqq, 60, Resolution.Daily); hs=self.History(self.spy, 60, Resolution.Daily)
        if hq.empty or hs.empty or len(hq)<60 or len(hs)<60: return
        q_ret=float(hq["close"].iloc[-1])/float(hq["close"].iloc[0])-1.0
        s_ret=float(hs["close"].iloc[-1])/float(hs["close"].iloc[0])-1.0
        bull = q_ret > s_ret and q_ret > 0
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
