from AlgorithmImports import *

class Algo062(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Add TQQQ as a fixed symbol
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol
        
        # Universe for top-10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Storage for ADX indicators and basket
        self.adx = {}
        self.basket = {}
        self._universe_symbols = []
        
        # Warm-up period
        self.SetWarmUp(14, Resolution.Daily)
        
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data, sort by market cap descending, take top 10
        sorted_by_market_cap = sorted([c for c in coarse if c.HasFundamentalData],
                                      key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_market_cap[:10]
        self._universe_symbols = [c.Symbol for c in top10]
        return self._universe_symbols
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Candidates: universe symbols + TQQQ
        candidates = set(self._universe_symbols) | {self.tqqq}
        
        # Clear basket for current day
        self.basket.clear()
        
        # Evaluate each candidate
        for symbol in candidates:
            # Ensure we have data for this symbol
            if symbol not in data or not data.ContainsKey(symbol):
                continue
            bar = data[symbol]
            if bar is None:
                continue
            
            # Create ADX indicator if not exists
            if symbol not in self.adx:
                self.adx[symbol] = self.ADX(symbol, 14, Resolution.Daily)
            
            # Check if ADX is ready and above 25
            if self.adx[symbol].IsReady and self.adx[symbol].Current.Value > 25:
                self.basket[symbol] = True
        
        # Rebalance portfolio
        basket_count = len(self.basket)
        if basket_count > 0:
            target_weight = 1.0 / basket_count
            for symbol in self.basket:
                self.SetHoldings(symbol, target_weight)
        else:
            # No positions
            pass
        
        # Liquidate positions not in basket
        for holding in self.Portfolio.Values:
            if holding.Invested and holding.Symbol not in self.basket:
                self.Liquidate(holding.Symbol)
