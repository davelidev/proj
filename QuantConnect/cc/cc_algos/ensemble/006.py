from AlgorithmImports import *

class IBSATRStop(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.sym  = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.atr  = self.ATR(self.sym, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.SetWarmUp(252, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.sym), self.TimeRules.AfterMarketOpen(self.sym, 45), self.Rebalance)
        self._entry = None

    def Rebalance(self):
        if self.IsWarmingUp or not self.atr.IsReady: return
        bar = self.Securities[self.sym]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return
        ibs = (c - l) / (h - l)
        atr = self.atr.Current.Value
        if not self._entry and ibs < 0.1:
            self.SetHoldings(self.sym, 1.0)
            self._entry = c
        elif self._entry:
            if ibs > 0.9 or c < self._entry - 3.0 * atr:
                self.Liquidate(self.sym)
                self._entry = None
