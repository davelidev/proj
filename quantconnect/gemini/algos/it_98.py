from AlgorithmImports import *
import numpy as np

class VolStretchReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.tqqq, 20, Resolution.Daily)
        self.std = self.STD(self.tqqq, 21, Resolution.Daily)
        
        self.SetWarmUp(30)

    def OnData(self, data):
        if not (self.sma.IsReady and self.std.IsReady): return
        
        price = float(self.Securities[self.tqqq].Price)
        mean = float(self.sma.Current.Value)
        
        # Daily Volatility (Standard Deviation as % of price)
        daily_vol = float(self.std.Current.Value) / price if price > 0 else 0
        
        # Dynamic Stretch Threshold: 2.0 * Volatility
        # e.g. if daily vol is 3%, threshold is 6% below SMA
        threshold = 2.0 * daily_vol
        
        if self.IsWarmingUp: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Price is 'Threshold' % below 20-day SMA
            if price <= mean * (1.0 - threshold):
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Return to Mean
            if price >= mean:
                self.Liquidate(self.tqqq)
