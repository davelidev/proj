from AlgorithmImports import *

class Algo080(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Sector ETFs (SPDR)
        self.sectors = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]
        for ticker in self.sectors:
            self.AddEquity(ticker, Resolution.Daily)
        
        # Strategy parameters
        self.lookback = 63  # ~3 months of trading days
        self.divergence_threshold = 0.15  # 15% difference to trigger concentration
        
        # Warm up for historical data
        self.SetWarmUp(self.lookback, Resolution.Daily)
        self.warming_up = True
        
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Get historical close prices for all sectors
        history = self.History(self.sectors, self.lookback + 1, Resolution.Daily)
        if history.empty:
            return
        
        # Extract closing prices
        closes = history.close.unstack(level=0)
        
        # Compute total return over lookback period
        # Use first and last close in the history
        returns = {}
        for ticker in self.sectors:
            if ticker in closes.columns:
                series = closes[ticker].dropna()
                if len(series) >= self.lookback + 1:
                    ret = series.iloc[-1] / series.iloc[0] - 1
                    returns[ticker] = ret
        
        if not returns:
            return
        
        # Find leader (max return) and spread
        max_ret = max(returns.values())
        min_ret = min(returns.values())
        leader = max(returns, key=returns.get)
        spread = max_ret - min_ret
        
        # Determine target weights
        targets = {}
        if spread > self.divergence_threshold:
            # Concentrate on leader
            targets[leader] = 1.0
        else:
            # Equal weight all sectors
            equal_weight = 1.0 / len(self.sectors)
            for ticker in self.sectors:
                targets[ticker] = equal_weight
        
        # Execute orders (no leverage, weights sum to 1.0)
        self.SetHoldings(targets, liquidateExistingHoldings=True)