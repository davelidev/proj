from AlgorithmImports import *
import numpy as np

class SigmaReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.tqqq, 20, Resolution.Daily)
        self.std = self.STD(self.tqqq, 20, Resolution.Daily)
        
        self.SetWarmUp(20)

    def OnData(self, data):
        if not (self.sma.IsReady and self.std.IsReady): return
        
        price = float(self.Securities[self.tqqq].Price)
        mean = float(self.sma.Current.Value)
        std_val = float(self.std.Current.Value)
        
        # 1. Trading Logic
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Extreme Outlier (3 Sigma below mean)
            if price <= (mean - 3 * std_val):
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Return to Mean
            if price >= mean:
                self.Liquidate(self.tqqq)
