from AlgorithmImports import *

class TII20(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma  = self.SMA(self.qqq, 20, Resolution.Daily)
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq, 45), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        h = self.History(self.qqq, 20, Resolution.Daily)
        if len(h) < 20: return
        sma = self.sma.Current.Value
        tii = sum(1 for c in h["close"] if float(c) > sma)
        if tii > 10: self.SetHoldings(self.tqqq, 1.0)
        elif self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
