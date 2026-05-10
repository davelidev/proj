from QuantConnect import *
from QuantConnect.Data import *
from QuantConnect.Data.UniverseSelection import *
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.Market import TradeBar

class Algo004(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Always add TQQQ
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        
        # Basket dictionary to track holdings (symbol -> placeholder)
        self.basket = {}
        # Manually add TQQQ to basket
        self.basket[self.tqqq] = None
        
        # Rolling windows for each symbol (size 2 to have current and previous bar)
        self.windows = {}
        # Initialize window for TQQQ
        self.windows[self.tqqq] = RollingWindow[TradeBar](2)
        
        # Add universe for top 10 stocks by market cap
        self.AddUniverse(self.CoarseSelectionFunction)
    
    def CoarseSelectionFunction(self, coarse):
        # Filter out stocks with no fundamental data
        sorted_coarse = [c for c in coarse if c.HasFundamentalData]
        # Take top 10 by market cap
        sorted_coarse = sorted(sorted_coarse, key=lambda c: c.MarketCap, reverse=True)[:10]
        return [c.Symbol for c in sorted_coarse]
    
    def OnSecuritiesChanged(self, changes):
        # Update basket and rolling windows for new symbols
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = None
                self.windows[symbol] = RollingWindow[TradeBar](2)
        
        # Remove symbols that left the universe (but keep TQQQ)
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol != self.tqqq and symbol in self.basket:
                del self.basket[symbol]
                if symbol in self.windows:
                    del self.windows[symbol]
    
    def OnData(self, data):
        # Update rolling windows with current bars
        for symbol in list(self.basket.keys()):
            if symbol in data.Bars:
                bar = data.Bars[symbol]
                if symbol in self.windows:
                    self.windows[symbol].Add(bar)
        
        # Compute signals and target weights
        targets = {}
        basket_symbols = list(self.basket.keys())
        if len(basket_symbols) == 0:
            return
        
        # Equal weight per symbol (absolute sum of weights = 1)
        weight_per_symbol = 1.0 / len(basket_symbols)
        
        for symbol in basket_symbols:
            window = self.windows.get(symbol)
            if window is None or not window.IsReady:
                continue
            # Get current and previous bar
            current = window[0]
            previous = window[1]
            
            # Inside-outside pattern: previous high > current high, previous low < current low, current close > previous close
            if (previous.High > current.High and 
                previous.Low < current.Low and 
                current.Close > previous.Close):
                # Long signal
                targets[symbol] = weight_per_symbol
            else:
                # Short signal
                targets[symbol] = -weight_per_symbol
        
        # Apply targets using SetHoldings
        for symbol, weight in targets.items():
            self.SetHoldings(symbol, weight)
