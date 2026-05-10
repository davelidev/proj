class Algo095(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # Create fast and slow SMA indicators
        self.sma20 = self.SMA("TQQQ", 20, Resolution.Daily)
        self.sma50 = self.SMA("TQQQ", 50, Resolution.Daily)
        
        self.previous_signal = None  # track last known cross state

    def OnData(self, data):
        if not data.ContainsKey("TQQQ"):
            return
        
        # Ensure both SMAs are ready before trading
        if not (self.sma20.IsReady and self.sma50.IsReady):
            return
        
        fast = self.sma20.Current.Value
        slow = self.sma50.Current.Value
        
        current_signal = fast > slow
        
        # Only act when the crossover signal changes
        if self.previous_signal is not None and current_signal == self.previous_signal:
            return
        
        self.previous_signal = current_signal
        
        if current_signal:
            # Buy signal: go fully invested, weight = 1.0 (no leverage)
            self.SetHoldings("TQQQ", 1.0)
        else:
            # Sell signal: exit entirely
            self.Liquidate("TQQQ")