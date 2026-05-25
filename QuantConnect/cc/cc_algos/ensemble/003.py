from AlgorithmImports import *

class TQQQDynamic(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.sym    = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi2   = self.RSI(self.sym, 2,   MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10  = self.RSI(self.sym, 10,  MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.sym), self.TimeRules.AfterMarketOpen(self.sym, 45), self.Rebalance)
        self._w = 0

    def Rebalance(self):
        if self.IsWarmingUp or not (self.rsi2.IsReady and self.sma200.IsReady): return
        price = self.Securities[self.sym].Price
        prev = self._w
        if price > self.sma200.Current.Value:
            if self.rsi10.Current.Value > 80:   self._w = 0.2
            elif self.rsi2.Current.Value < 30:  self._w = 1.0
            elif self._w == 0:                  self._w = 0.5
        else:
            self._w = 0
        if self._w != prev:
            if self._w == 0: self.Liquidate(self.sym)
            else: self.SetHoldings(self.sym, self._w)
