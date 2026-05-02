from AlgorithmImports import *

class ClosingRangeReversion(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.window = RollingWindow[float](3)
        
        self.SetWarmUp(10)

    def OnData(self, data):
        if not data.Bars.ContainsKey(self.tqqq): return
        
        bar = data.Bars[self.tqqq]
        # Closing Range = (Close - Low) / (High - Low)
        daily_range = bar.High - bar.Low
        closing_range = (bar.Close - bar.Low) / daily_range if daily_range > 0 else 0.5
        
        self.window.Add(closing_range)
        
        if self.IsWarmingUp or not self.window.IsReady: return

        if not self.Portfolio[self.tqqq].Invested:
            # Entry: 3 consecutive days closing in the bottom 10%
            if all(x < 0.1 for x in self.window):
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: Close in the top 10%
            if closing_range > 0.9:
                self.Liquidate(self.tqqq)
