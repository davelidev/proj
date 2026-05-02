from AlgorithmImports import *

class DeepRSIDip(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(10)

    def OnData(self, data):
        if not self.rsi.IsReady: return
        
        rsi_val = float(self.rsi.Current.Value)
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Extreme Deep Dip (RSI < 10)
            if rsi_val < 10:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Full Recovery (RSI > 90)
            if rsi_val > 90:
                self.Liquidate(self.tqqq)
