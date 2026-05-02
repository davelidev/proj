from AlgorithmImports import *

class IntradayBreakout(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.ticker = "TQQQ"
        self.symbol = self.AddEquity(self.ticker, Resolution.Minute).Symbol
        
        # Lookback: 48 bars of 5-min = 4 hours
        self.high = self.MAX(self.symbol, 240, Resolution.Minute)
        self.entry_price = 0
        self.trailing_stop = 0
        
        self.SetWarmUp(240)

    def OnData(self, data):
        if self.IsWarmingUp or not self.high.IsReady: return
        if not data.Bars.ContainsKey(self.symbol): return
        
        price = data.Bars[self.symbol].Close
        
        # 1. Trading Logic
        if not self.Portfolio[self.symbol].Invested:
            # Entry: Price breaks 4-hour high
            if price > self.high.Current.Value * 1.005:
                # Limit entries to middle of the day (avoid open/close volatility)
                if self.Time.hour >= 10 and self.Time.hour < 15:
                    self.SetHoldings(self.symbol, 1.0)
                    self.entry_price = price
                    self.trailing_stop = price * 0.98
        else:
            # Update Trailing Stop
            self.trailing_stop = max(self.trailing_stop, price * 0.98)
            
            # Exit conditions
            # a) Trailing Stop hit
            # b) End of day approach (3:50 PM)
            if price < self.trailing_stop or (self.Time.hour == 15 and self.Time.minute >= 50):
                self.Liquidate(self.symbol)
                self.entry_price = 0
                self.trailing_stop = 0
