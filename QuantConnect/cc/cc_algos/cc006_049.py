from AlgorithmImports import *

class ThreeAssetRS(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.spy=self.AddEquity("SPY",Resolution.Daily).Symbol
        self.iwm=self.AddEquity("IWM",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        rets = {}
        for s in (self.qqq, self.spy, self.iwm):
            h = self.History(s, 60, Resolution.Daily)
            if h.empty or len(h)<60: return
            rets[s] = float(h["close"].iloc[-1])/float(h["close"].iloc[0])-1.0
        leader = max(rets, key=rets.get)
        if leader == self.qqq and rets[leader] > 0:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
