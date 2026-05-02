from AlgorithmImports import *
import numpy as np

class PercentRankReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.window = RollingWindow[float](252)
        
        self.SetWarmUp(252)

    def OnData(self, data):
        if not data.Bars.ContainsKey(self.tqqq): return
        
        price = float(data.Bars[self.tqqq].Close)
        self.window.Add(price)
        
        if self.IsWarmingUp or not self.window.IsReady: return

        # Calculate % Rank
        prices = [x for x in self.window]
        rank = (sum(1 for x in prices if x < price) / 252.0) * 100.0
        
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Price in bottom 5% of yearly range
            if rank < 5:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Price reverts to median (50%)
            if rank > 50:
                self.Liquidate(self.tqqq)
