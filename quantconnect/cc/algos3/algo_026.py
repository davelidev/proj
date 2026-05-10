from AlgorithmImports import *

class Algo026(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Add TQQQ as a fixed ticker
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # Dictionary to hold symbols and their ROC indicators
        self.basket = {}
        
        # Add universe selection for top 10 by market cap
        self.AddUniverse(self.UniverseFilter)
        
        # Set warmup period for indicators
        self.SetWarmUp(5, Resolution.Daily)
    
    def UniverseFilter(self, fundamental):
        # Filter to get top 10 stocks by market cap
        sorted_by_cap = sorted(fundamental, key=lambda f: f.MarketCap, reverse=True)
        top10 = [f.Symbol for f in sorted_by_cap[:10]]
        return top10
    
    def OnSecuritiesChanged(self, changes):
        # Add new securities to basket with ROC indicator
        for security in changes.AddedSecurities:
            symbol = security.Symbol
            if symbol not in self.basket:
                roc = self.ROC(symbol, 5, Resolution.Daily)
                self.basket[symbol] = roc
        
        # Remove securities that left the universe
        for security in changes.RemovedSecurities:
            symbol = security.Symbol
            if symbol in self.basket:
                del self.basket[symbol]
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Ensure TQQQ is always in basket (in case it wasn't added by universe)
        if "TQQQ" not in self.basket:
            tqqq = Symbol.Create("TQQQ", SecurityType.Equity, Market.USA)
            if tqqq not in self.basket:
                roc = self.ROC(tqqq, 5, Resolution.Daily)
                self.basket[tqqq] = roc
        
        # Compute signals for all symbols in basket
        targets = []
        for symbol, roc in self.basket.items():
            if not roc.IsReady:
                continue
            roc_value = roc.Current.Value
            if roc_value > 5.0:
                targets.append((symbol, 1.0))  # Long
            elif roc_value < -5.0:
                targets.append((symbol, -1.0)) # Short
            else:
                targets.append((symbol, 0.0))
        
        # Apply weight allocation: equal weight per non-flat signal, sum abs <= 1
        active = [t for t in targets if t[1] != 0]
        if active:
            num_active = len(active)
            # Ensure total absolute weight <= 1.0
            weight_per = 1.0 / num_active
            for symbol, direction in active:
                target_weight = direction * weight_per
                self.SetHoldings(symbol, target_weight)
        else:
            # Flatten all positions
            for symbol, _ in targets:
                self.SetHoldings(symbol, 0)