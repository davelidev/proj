class Algo104(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.AddEquity("TQQQ", Resolution.Daily)
        self.symbol = self.Symbol("TQQQ")
        self.sma = self.SMA(self.symbol, 5, Resolution.Daily)
        self.prev_close = None
        self.prev_sma = None
        self.hold = False

    def OnData(self, data):
        if not data.ContainsKey(self.symbol):
            return

        bar = data[self.symbol]
        if not self.sma.IsReady:
            self.prev_close = bar.Close
            return

        sma_val = self.sma.Current.Value
        close = bar.Close

        # Entry: price crosses below SMA (pullback)
        if self.prev_close is not None and self.prev_sma is not None:
            if self.prev_close >= self.prev_sma and close < sma_val and not self.hold:
                self.SetHoldings(self.symbol, 1.0)
                self.hold = True
                self.Debug(f"Long entry at {close:.2f}, SMA5: {sma_val:.2f}")
            # Exit: price crosses above SMA (recovery)
            elif self.prev_close <= self.prev_sma and close > sma_val and self.hold:
                self.SetHoldings(self.symbol, 0.0)
                self.hold = False
                self.Debug(f"Exit at {close:.2f}, SMA5: {sma_val:.2f}")

        self.prev_close = close
        self.prev_sma = sma_val
