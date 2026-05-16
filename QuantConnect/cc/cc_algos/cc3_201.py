from AlgorithmImports import *

class HYGvsLQDCredit(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.hyg=self.AddEquity("HYG",Resolution.Daily).Symbol
        self.lqd=self.AddEquity("LQD",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        hh=self.History(self.hyg, 60, Resolution.Daily); hl=self.History(self.lqd, 60, Resolution.Daily)
        if hh.empty or hl.empty or len(hh)<60 or len(hl)<60: return
        h_r=float(hh["close"].iloc[-1])/float(hh["close"].iloc[0])-1.0
        l_r=float(hl["close"].iloc[-1])/float(hl["close"].iloc[0])-1.0
        # HYG outperforming LQD = credit risk-on
        risk_on = h_r > l_r
        if risk_on:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
