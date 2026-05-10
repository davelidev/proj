from AlgorithmImports import *

class Algo092(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.AddEquity("TQQQ", Resolution.Daily)
        self.previous_close = None

    def OnData(self, data: Slice):
        if not data.Bars.ContainsKey("TQQQ"):
            return
        bar = data.Bars["TQQQ"]
        
        # First day: store close and return
        if self.previous_close is None:
            self.previous_close = bar.Close
            return
        
        open_price = bar.Open
        prev_close = self.previous_close
        gap = (open_price - prev_close) / prev_close
        
        # Buy on large gap down (>1%), only if not already invested
        if gap < -0.01 and not self.Portfolio["TQQQ"].Invested:
            self.SetHoldings("TQQQ", 1.0)
            self.Debug(f"Bought TQQQ on gap down: open {open_price:.2f}, prev close {prev_close:.2f}, gap {gap:.4f}")
        
        # Update previous close for next day
        self.previous_close = bar.Close