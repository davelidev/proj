from AlgorithmImports import *

class Algo112(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.previous_close = None
        
        # Schedule liquidation at 1 minute after market open each day
        self.Schedule.On(
            self.DateRules.EveryDay(self.symbol),
            self.TimeRules.AfterMarketOpen(self.symbol, 1),
            self.liquidate_position
        )
    
    def liquidate_position(self):
        # Sell any existing position at the open
        if self.Portfolio[self.symbol].Invested:
            self.SetHoldings(self.symbol, 0)
    
    def OnData(self, data):
        if not data.ContainsKey(self.symbol):
            return
        
        bar = data[self.symbol]
        current_close = bar.Close
        
        if self.previous_close is not None and current_close < self.previous_close:
            # Buy TQQQ at the close with full portfolio (weight <= 1.0)
            self.SetHoldings(self.symbol, 1.0)
        
        self.previous_close = current_close
