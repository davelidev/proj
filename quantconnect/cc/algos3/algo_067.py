from AlgorithmImports import *

class Algo067(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Hardcoded TQQQ (must be added)
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # Universe selection: top 10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Basket dictionary for selected symbols and their indicators
        self.basket = {}
        
        # Parameters for pullback pattern
        self.pullback_threshold = 0.95  # 5% below 20-day high
        self.lookback_high = 20
        self.sma_period = 200
        
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and positive market cap
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        # Sort by market cap descending, take top 10
        sorted_by_cap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = [c.Symbol for c in sorted_by_cap[:10]]
        return top10
    
    def OnSecuritiesChanged(self, changes):
        # Remove old symbols not in universe anymore
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                # Remove indicators and symbol from basket
                self.basket.pop(symbol, None)
        
        # Add new symbols and create indicators
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # Create indicators
                sma = SimpleMovingAverage(self.sma_period)
                max_high = Maximum(self.lookback_high)
                # Register indicators
                self.RegisterIndicator(symbol, sma, Resolution.Daily)
                self.RegisterIndicator(symbol, max_high, Resolution.Daily)
                
                # Warm up indicators with historical data
                history = self.History(symbol, max(self.sma_period, self.lookback_high) + 1, Resolution.Daily)
                if not history.empty:
                    for index, row in history.loc[symbol].iterrows():
                        sma.Update(index, row["close"])
                        max_high.Update(index, row["high"])
                
                self.basket[symbol] = (sma, max_high)
    
    def OnData(self, data):
        # Skip if no data or no basket
        if not data.Bars and not data.QuoteBars:
            return
        
        # Build target weights dictionary
        targets = {}
        num_qualified = 0
        
        for symbol, (sma, max_high) in self.basket.items():
            if symbol not in data or symbol not in self.Securities:
                continue
            # Check if indicators are ready
            if not sma.IsReady or not max_high.IsReady:
                continue
            
            # Get current price
            price = self.Securities[symbol].Close
            if price == 0:
                continue
            
            # Pullback condition: price below 95% of 20-day high AND above 200-day SMA
            high_twenty = max_high.Current.Value
            sma_two_hundred = sma.Current.Value
            
            if price <= high_twenty * self.pullback_threshold and price > sma_two_hundred:
                num_qualified += 1
                # Store symbol for later weight assignment
                targets[symbol] = 0  # placeholder, will set equal weight later
        
        # Assign equal weight to all qualified symbols
        if num_qualified > 0:
            weight = 1.0 / num_qualified
            for symbol in targets:
                targets[symbol] = weight
        
        # Execute rebalance: SetHoldings for all symbols (including zero weight for those not qualified)
        # This will also liquidate any positions not in targets
        for symbol in self.basket:
            if symbol in targets:
                self.SetHoldings(symbol, targets[symbol])
            else:
                self.SetHoldings(symbol, 0)
