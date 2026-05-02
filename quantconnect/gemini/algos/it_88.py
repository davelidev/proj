from AlgorithmImports import *

class KeltnerReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.kc = self.KCH(self.tqqq, 20, 2, MovingAverageType.Exponential, Resolution.Daily)
        self.rsi = self.RSI(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(30)

    def OnData(self, data):
        if not (self.kc.IsReady and self.rsi.IsReady): return
        
        price = float(self.Securities[self.tqqq].Price)
        lower = float(self.kc.LowerBand.Current.Value)
        middle = float(self.kc.MiddleBand.Current.Value)
        rsi_val = float(self.rsi.Current.Value)
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Price < Lower Keltner AND RSI < 30
            if price <= lower and rsi_val < 30:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Price returns to Middle Band
            if price >= middle:
                self.Liquidate(self.tqqq)
