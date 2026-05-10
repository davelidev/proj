from AlgorithmImports import *

class Algo102(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Keltner Channel parameters
        self.ema_period = 20
        self.atr_period = 20
        self.multiplier = 2.0
        
        # Create Keltner Channel indicator
        self.kc = self.KC(self.symbol, self.ema_period, self.multiplier, self.atr_period, MovingAverageType.Exponential, Resolution.Daily)
        self.kc.Updated += self.OnKCUpdated
        
        # Warmup period
        self.SetWarmUp(self.ema_period + self.atr_period)
        
        self.prev_kc_ready = False
        
    def OnKCUpdated(self, sender, updated):
        # This event is triggered when the indicator updates
        pass
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        if not self.kc.IsReady:
            return
        
        # Current values
        close = self.Securities[self.symbol].Close
        middle = self.kc.MiddleBand.Current.Value
        upper = self.kc.UpperBand.Current.Value
        lower = self.kc.LowerBand.Current.Value
        
        # Entry/Exit logic
        if not self.Portfolio.Invested:
            # Buy when close crosses below lower band (reversal from oversold)
            if close < lower and close < middle:
                self.SetHoldings(self.symbol, 1.0)  # Full allocation, no leverage
                self.Debug(f"BUY {self.Time} - Close: {close:.2f}, Lower: {lower:.2f}")
        else:
            # Sell when close crosses above middle band (revert to mean)
            if close > middle:
                self.Liquidate(self.symbol)
                self.Debug(f"SELL {self.Time} - Close: {close:.2f}, Middle: {middle:.2f}")