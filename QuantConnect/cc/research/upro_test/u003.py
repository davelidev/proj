from AlgorithmImports import *
class U003(QCAlgorithm):
    """UPRO Dynamic Sizing: SMA200 + RSI tiers on UPRO. UPRO generalization of ensemble/003."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.upro   = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.rsi2   = self.RSI(self.upro, 2,  MovingAverageType.Wilders, Resolution.Daily)
        self.rsi10  = self.RSI(self.upro, 10, MovingAverageType.Wilders, Resolution.Daily)
        self.sma200 = self.SMA(self.upro, 200, Resolution.Daily)
        self.SetWarmUp(210, Resolution.Daily)
        self._cur_w = 0.0
        self.Schedule.On(self.DateRules.EveryDay(self.upro),
                         self.TimeRules.AfterMarketOpen(self.upro, 30), self.R)
    def R(self):
        if self.IsWarmingUp or not (self.rsi2.IsReady and self.sma200.IsReady): return
        price = self.Securities[self.upro].Price
        if price > self.sma200.Current.Value:
            if self.rsi10.Current.Value > 80:
                w = 0.2
            elif self.rsi2.Current.Value < 30:
                w = 1.0
            elif self._cur_w == 0:
                w = 0.5
            else:
                w = self._cur_w
        else:
            w = 0.0
        if abs(w - self._cur_w) > 0.01:
            self._cur_w = w
            self.SetHoldings(self.upro, w)
    def OnData(self, d): pass
