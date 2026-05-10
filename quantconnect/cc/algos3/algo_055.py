from QuantConnect.Data.UniverseSelection import *
from QuantConnect.Indicators import *

class Algo055(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Add TQQQ as a required fixed equity (not part of universe selection)
        self.AddEquity('TQQQ', Resolution.Daily)
        
        # Universe selection: all sectors, top 10 by market cap
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Basket dictionary: symbol -> { 'sma5': SMA, 'sma20': SMA }
        self.basket = {}
        
        # Warm up period for indicators
        self.SetWarmUp(20)
    
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and positive market cap
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        # Sort descending by market cap, take top 10
        sorted_by_market_cap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        return [c.Symbol for c in sorted_by_market_cap[:10]]
    
    def OnSecuritiesChanged(self, changes):
        # Handle added securities
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # Create SMA(5) and SMA(20) indicators
                sma5 = self.SMA(symbol, 5, Resolution.Daily)
                sma20 = self.SMA(symbol, 20, Resolution.Daily)
                # Register them (automatically updated with daily bars)
                self.RegisterIndicator(symbol, sma5, Resolution.Daily)
                self.RegisterIndicator(symbol, sma20, Resolution.Daily)
                self.basket[symbol] = {'sma5': sma5, 'sma20': sma20}
        
        # Handle removed securities (universe changes)
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                # Liquidate any position and remove from basket
                self.Liquidate(symbol)
                del self.basket[symbol]
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Current number of securities in basket
        basket_size = len(self.basket)
        if basket_size == 0:
            return
        
        # Target weight per position (equal weight)
        target_weight = 1.0 / basket_size
        
        # Check each symbol in basket
        for symbol, indicators in self.basket.items():
            sma5 = indicators['sma5']
            sma20 = indicators['sma20']
            
            if not (sma5.IsReady and sma20.IsReady):
                continue
            
            # Current and previous indicator values
            curr_sma5 = sma5.Current.Value
            prev_sma5 = sma5.Previous.Value if sma5.Previous is not None else curr_sma5
            curr_sma20 = sma20.Current.Value
            prev_sma20 = sma20.Previous.Value if sma20.Previous is not None else curr_sma20
            
            # MA5 crosses above MA20 -> enter / add
            if prev_sma5 <= prev_sma20 and curr_sma5 > curr_sma20:
                self.SetHoldings(symbol, target_weight)
            
            # MA5 crosses below MA20 -> exit
            elif prev_sma5 >= prev_sma20 and curr_sma5 < curr_sma20:
                self.SetHoldings(symbol, 0)
