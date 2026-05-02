from AlgorithmImports import *

class VolAdaptiveRSI(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.vix = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol
        
        self.rsi = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        
        self.SetWarmUp(30)

    def OnData(self, data):
        if not (self.rsi.IsReady and self.Securities.ContainsKey(self.vix)): return
        
        vix_val = self.Securities[self.vix].Price
        rsi_val = self.rsi.Current.Value
        
        # Dynamic Threshold calculation
        # If VIX is high (panic), wait for deeper dip.
        # Threshold = 40 - (VIX / 2) 
        # e.g. VIX 20 -> 40 - 10 = 30
        # e.g. VIX 40 -> 40 - 20 = 20
        entry_threshold = max(15, 40 - (vix_val / 2.0))
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            if rsi_val < entry_threshold:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if rsi_val > 70:
                self.Liquidate(self.tqqq)
