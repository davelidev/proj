from AlgorithmImports import *
class U006(QCAlgorithm):
    """UPRO IBS < 0.1 entry + 3×ATR stop. UPRO generalization of ensemble/006."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.upro        = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.atr         = self.ATR(self.upro, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.entry_price = None
        self.SetWarmUp(20, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.upro),
                         self.TimeRules.AfterMarketOpen(self.upro, 45), self.R)
    def R(self):
        if self.IsWarmingUp or not self.atr.IsReady: return
        bar = self.Securities[self.upro]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return
        ibs      = (c - l) / (h - l)
        invested = self.Portfolio[self.upro].Invested
        if not invested and ibs < 0.1:
            self.SetHoldings(self.upro, 1.0)
            self.entry_price = c
        elif invested:
            stop = self.entry_price - 3.0 * self.atr.Current.Value if self.entry_price else 0
            if ibs > 0.9 or c < stop:
                self.Liquidate(self.upro)
                self.entry_price = None
    def OnData(self, d): pass
