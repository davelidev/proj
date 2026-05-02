from AlgorithmImports import *

class GoldenButterflyRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "TMF", "GLD"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        self.smas = {}
        
        for ticker in self.assets:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.smas[symbol] = self.SMA(symbol, 200, Resolution.Daily)
            
        self.Schedule.On(self.DateRules.MonthStart("BIL"), 
                         self.TimeRules.AfterMarketOpen("BIL", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        total_w = 0
        target_weights = {}
        
        # Check trend for each asset
        for ticker, symbol in self.symbols.items():
            if not self.smas[symbol].IsReady: continue
            
            price = self.Securities[symbol].Price
            sma_val = self.smas[symbol].Current.Value
            
            if price > sma_val:
                # Trend is bullish, allocate 1/3
                target_weights[symbol] = 0.33
                total_w += 0.33
            else:
                # Trend is bearish, allocate 0
                target_weights[symbol] = 0
        
        # Allocate to BIL for remaining weight
        target_weights[self.bil] = 1.0 - total_w
        
        # Execute rebalance
        for symbol, weight in target_weights.items():
            self.SetHoldings(symbol, weight)
            
        # Liquidate removed
        for symbol in self.Portfolio.Keys:
            if symbol not in target_weights:
                self.Liquidate(symbol)

    def OnData(self, data):
        pass
