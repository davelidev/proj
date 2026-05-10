from datetime import datetime
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import Maximum, Minimum
from System.Collections.Generic import List

class Algo094(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.AddEquity("TQQQ", Resolution.Daily)
        self.symbol = self.Symbol("TQQQ")
        
        # Rolling window to store last 20 daily highs and lows (excluding today)
        self.highs = RollingWindow[float](20)
        self.lows = RollingWindow[float](20)
        
        # Warm up by filling the rolling windows with history
        history = self.History(self.symbol, 20, Resolution.Daily)
        for index, row in history.iterrows():
            self.highs.Add(row['high'])
            self.lows.Add(row['low'])
        
        self.SetWarmUp(20, Resolution.Daily)  # Ensure indicators are ready
        
    def OnData(self, data: TradeBar):
        if self.IsWarmingUp:
            return
        
        # Update rolling windows with current bar's high/low (will be used for next day's breakout)
        # But for today's signal we need previous 20 days only, which are already in windows.
        if not self.highs.IsReady:
            return
        
        current_close = data[self.symbol].Close
        
        # Compute 20-day high and low from the rolling windows (previous 20 bars)
        prev_20d_high = max(self.highs)
        prev_20d_low = min(self.lows)
        
        # Determine signal
        long_signal = current_close > prev_20d_high
        short_signal = current_close < prev_20d_low
        
        if long_signal:
            # Enter long
            self.SetHoldings(self.symbol, 1.0)
            self.Debug(f"{self.Time} - LONG signal: Close={current_close} > High={prev_20d_high}")
        elif short_signal:
            # Enter short
            self.SetHoldings(self.symbol, -1.0)
            self.Debug(f"{self.Time} - SHORT signal: Close={current_close} < Low={prev_20d_low}")
        else:
            # No signal, stay flat (could also hold previous position, but for pure breakout we exit)
            self.Liquidate(self.symbol)
        
        # Update rolling windows with today's bar for future calculations
        self.highs.Add(data[self.symbol].High)
        self.lows.Add(data[self.symbol].Low)