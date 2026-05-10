from AlgorithmImports import *

class Algo008(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.AddEquity('TQQQ', Resolution.Daily)
        
        # Dictionary to track holdings by symbol
        self.basket = {}
        # Dictionary to store CCI indicators for each symbol
        self.cci_indicators = {}
        
        # Universe selection: top 10 stocks by market cap
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        
        self.SetWarmUp(14)
    
    def CoarseSelectionFunction(self, coarse):
        # Return all symbols that have fundamental data (for fine selection)
        # Filter to avoid TQQQ duplication (it's already added separately)
        return [c.Symbol for c in coarse if c.HasFundamentalData and c.Symbol.Value != 'TQQQ']
    
    def FineSelectionFunction(self, fine):
        # Sort by market cap descending, take top 10
        sorted_fine = sorted(fine, key=lambda f: f.MarketCap, reverse=True)
        return [f.Symbol for f in sorted_fine[:10]]
    
    def OnSecuritiesChanged(self, changes):
        # Handle removed securities
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                del self.basket[symbol]
            if symbol in self.cci_indicators:
                del self.cci_indicators[symbol]
            # Liquidate any remaining position
            self.Liquidate(symbol)
        
        # Handle added securities
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = None  # placeholder
                # Create and register CCI indicator
                cci = self.CCI(symbol, 14, Resolution.Daily)
                self.cci_indicators[symbol] = cci
                # Warm up indicator using historical data
                self.WarmUpIndicator(symbol, cci, Resolution.Daily)
        
        # Ensure TQQQ is always in basket (it's added via AddEquity and may not appear in universe changes)
        tqqq_symbol = self.Symbol('TQQQ')
        if tqqq_symbol not in self.basket:
            self.basket[tqqq_symbol] = None
            cci = self.CCI(tqqq_symbol, 14, Resolution.Daily)
            self.cci_indicators[tqqq_symbol] = cci
            self.WarmUpIndicator(tqqq_symbol, cci, Resolution.Daily)
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Compute signals for each symbol in basket
        signals = {}
        for symbol in self.basket:
            if symbol in self.cci_indicators and self.cci_indicators[symbol].IsReady:
                cci_value = self.cci_indicators[symbol].Current.Value
                if cci_value > 100:
                    signals[symbol] = -1  # short
                elif cci_value < -100:
                    signals[symbol] = 1   # long
                else:
                    signals[symbol] = 0   # flat
        
        # Count non-zero signals
        active_symbols = [s for s, sig in signals.items() if sig != 0]
        if len(active_symbols) == 0:
            # No signal – liquidate all
            for symbol in self.basket:
                self.SetHoldings(symbol, 0)
            return
        
        # Allocate equal weight among active positions, respecting direction
        weight_per = 1.0 / len(active_symbols)
        for symbol in self.basket:
            if symbol in signals:
                weight = signals[symbol] * weight_per
                self.SetHoldings(symbol, weight)
            else:
                # Symbol not ready or not in signals – liquidate
                self.SetHoldings(symbol, 0)
