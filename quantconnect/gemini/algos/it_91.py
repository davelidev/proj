from AlgorithmImports import *

class IntradayRSIScalp(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.rsi = self.RSI(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Minute)
        
        self.SetWarmUp(30)

    def OnData(self, data):
        if self.IsWarmingUp or not self.rsi.IsReady: return
        if not data.Bars.ContainsKey(self.tqqq): return
        
        rsi_val = self.rsi.Current.Value
        
        # 1. Trading Logic
        if not self.Portfolio[self.tqqq].Invested:
            # Entry: Intraday Oversold (RSI < 20)
            if rsi_val < 20:
                # Only trade between 10 AM and 3 PM (avoid open/close volatility)
                if 10 <= self.Time.hour < 15:
                    self.SetHoldings(self.tqqq, 1.0)
        else:
            # Exit: RSI Reverts to 50 OR End of Day Approach
            if rsi_val > 50 or (self.Time.hour == 15 and self.Time.minute >= 50):
                self.Liquidate(self.tqqq)
