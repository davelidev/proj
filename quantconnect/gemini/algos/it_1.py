from AlgorithmImports import *

class AlphaRebalancingAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Universe of 20 liquid stocks
        self.Equities = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", 
            "META", "NVDA", "BRK.B", "JNJ", "V", 
            "WMT", "PG", "MA", "UNH", "HD", 
            "DIS", "PYPL", "BAC", "VZ", "ADBE"
        ]
        
        self.symbol_objs = {}
        self.close_window = {}
        self.low_window = {}
        
        for ticker in self.Equities:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbol_objs[ticker] = symbol
            # 16-day rolling windows for the alpha calculation
            self.close_window[ticker] = RollingWindow[float](16)
            self.low_window[ticker] = RollingWindow[float](16)
            
        # Schedule rebalancing at the end of each quarter
        self.Schedule.On(
            self.DateRules.MonthEnd("SPY"), 
            self.TimeRules.BeforeMarketClose("SPY", 10), 
            self.Rebalance
        )
        
        self.SetWarmUp(16)

    def OnData(self, data):
        # Update rolling windows with daily data
        for ticker, symbol in self.symbol_objs.items():
            if data.Bars.ContainsKey(symbol):
                self.close_window[ticker].Add(data.Bars[symbol].Close)
                self.low_window[ticker].Add(data.Bars[symbol].Low)

    def Rebalance(self):
        # Only rebalance at the end of March, June, September, and December
        if self.Time.month not in [3, 6, 9, 12]:
            return

        alpha_rankings = {}
        
        for ticker, symbol in self.symbol_objs.items():
            if self.close_window[ticker].IsReady and self.low_window[ticker].IsReady:
                # Alpha Formula: inv(prod(div(close, low), 16))
                product = 1.0
                for i in range(16):
                    product *= (self.close_window[ticker][i] / self.low_window[ticker][i])
                
                alpha = -1.0 * product
                alpha_rankings[symbol] = alpha
        
        if not alpha_rankings:
            return
            
        # Sort symbols by alpha value in descending order (highest alpha = stocks closing near lows)
        sorted_alpha = sorted(alpha_rankings.items(), key=lambda x: x[1], reverse=True)
        
        # Determine quartile size (5 stocks for a 20-stock universe)
        num_stocks = len(sorted_alpha)
        quartile_size = num_stocks // 4
        
        if quartile_size == 0:
            return
            
        long_stocks = [x[0] for x in sorted_alpha[:quartile_size]]
        short_stocks = [x[0] for x in sorted_alpha[-quartile_size:]]
        
        # Liquidate positions no longer in the top or bottom quartile
        for symbol in self.Portfolio.Keys:
            if symbol not in long_stocks and symbol not in short_stocks:
                if self.Portfolio[symbol].Invested:
                    self.Liquidate(symbol)
                
        # Allocate equal weight (e.g., 10% each for 5 longs and 5 shorts)
        weight = 1.0 / (2 * quartile_size)
        
        for symbol in long_stocks:
            self.SetHoldings(symbol, weight)
            
        for symbol in short_stocks:
            self.SetHoldings(symbol, -weight)
