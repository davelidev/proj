from AlgorithmImports import *

class RSIDipChampion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.soxl = self.AddEquity("SOXL", Resolution.Daily).Symbol
        self.tecl = self.AddEquity("TECL", Resolution.Daily).Symbol
        self.rsi2 = self.RSI(self.qqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self._syms = [self.tqqq, self.soxl, self.tecl]
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq, 45), self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.rsi2.IsReady: return
        if self.rsi2.Current.Value < 20:
            for s in self._syms: self.SetHoldings(s, 1/3)
        else:
            for s in self._syms:
                if self.Portfolio[s].Invested: self.Liquidate(s)
