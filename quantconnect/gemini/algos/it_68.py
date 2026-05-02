from AlgorithmImports import *

class AsymmetricTrend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma50 = self.SMA(self.tqqq, 50, Resolution.Daily)
        self.sma200 = self.SMA(self.tqqq, 200, Resolution.Daily)
        
        self.SetWarmUp(200)

    def OnData(self, data):
        if not (self.sma50.IsReady and self.sma200.IsReady): return
        
        price = float(self.Securities[self.tqqq].Price)
        s50 = self.sma50.Current.Value
        s200 = self.sma200.Current.Value
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: FAST (50 SMA)
            if price > s50:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: SLOW (200 SMA)
            if price < s200:
                self.Liquidate(self.tqqq)
