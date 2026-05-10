from AlgorithmImports import *

class Algo105(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Store previous bar's OHLC for inside bar detection
        self.previous_high = None
        self.previous_low = None
        self.inside_bar_high = None  # high of mother bar (the bar before inside bar)
        self.inside_bar_low = None   # low of mother bar
        self.in_position = False
        self.entry_price = None
        
    def OnData(self, data):
        if not data.ContainsKey(self.symbol):
            return
        
        bar = data[self.symbol]
        current_high = bar.High
        current_low = bar.Low
        current_close = bar.Close
        
        # Wait for enough data
        if self.previous_high is None or self.previous_low is None:
            # Store first bar and return
            self.previous_high = current_high
            self.previous_low = current_low
            self.previous_close = bar.Close
            return
        
        # Check for inside bar pattern:
        # Current bar is inside the previous bar's range
        if current_high < self.previous_high and current_low > self.previous_low:
            # Inside bar formed: mother bar is the previous bar
            self.inside_bar_high = self.previous_high
            self.inside_bar_low = self.previous_low
        
        # Check for breakout above mother bar high
        if self.inside_bar_high is not None and current_close > self.inside_bar_high:
            # Breakout signal
            if not self.in_position:
                # Buy as much as cash allows (weight <= 1.0, no leverage)
                self.SetHoldings(self.symbol, 1.0)
                self.in_position = True
                self.entry_price = current_close
                self.Debug(f"BUY at {current_close}")
            # If already in position, do nothing (could add trailing stop or exit)
        
        # Optional: exit if price falls below mother bar low (stop loss)
        if self.in_position and self.inside_bar_low is not None and current_close < self.inside_bar_low:
            self.Liquidate(self.symbol)
            self.in_position = False
            self.inside_bar_high = None
            self.inside_bar_low = None
            self.Debug(f"SELL (stop loss) at {current_close}")
        
        # Store current bar for next comparison
        self.previous_high = current_high
        self.previous_low = current_low
        self.previous_close = bar.Close
