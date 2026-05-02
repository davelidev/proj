from AlgorithmImports import *
import numpy as np

class AdaptiveSMACross(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma_slow = self.SMA(self.tqqq, 200, Resolution.Daily)
        
        # Indicator for volatility
        self.std = self.STD(self.tqqq, 21, Resolution.Daily)
        
        # We will manually calculate the fast SMA based on dynamic lookback
        self.window = RollingWindow[float](100) # Max possible lookback
        
        self.SetWarmUp(200)

    def OnData(self, data):
        if not data.Bars.ContainsKey(self.tqqq): return
        
        price = float(data.Bars[self.tqqq].Close)
        self.window.Add(price)
        
        if self.IsWarmingUp or not (self.sma_slow.IsReady and self.std.IsReady and self.window.IsReady): return

        # 1. Calculate Dynamic Lookback for Fast SMA
        # Logic: Volatility (as % of price) inversely proportional to lookback
        # Base lookback = 20 days
        # Min = 5, Max = 50
        vol_pct = self.std.Current.Value / price if price > 0 else 1.0
        lookback = int(20 / (vol_pct * 10)) # Heuristic scaling
        lookback = max(5, min(50, lookback))
        
        # 2. Calculate Fast SMA
        prices = [self.window[i] for i in range(lookback)]
        fast_sma = sum(prices) / len(prices)
        slow_sma = self.sma_slow.Current.Value

        # 3. Trading Logic
        if fast_sma > slow_sma:
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
