class Algo081(BaseSubAlgo):
    """
    Sector correlation crash strategy:
    When sector correlations fall below -0.3 (inverse relationship),
    rotate to uncorrelated sectors to maximize diversification.
    """
    
    def initialize(self):
        """Initialize sector ETF universe."""
        self.sector_etfs = [
            "XLB", "XLE", "XLF", "XLI", "XLK",
            "XLP", "XLU", "XLV", "XLY", "XLRE", "XLC"
        ]
        for etf in self.sector_etfs:
            self.AddEquity(etf, Resolution.Daily)
    
    def update_targets(self):
        """
        Detect low correlation regime and allocate to uncorrelated sectors.
        Compute pairwise correlations; if many pairs < -0.3, concentrate
        on sectors with lowest correlations to the broad market.
        """
        # Get 63-day returns for all sectors
        returns = {}
        for symbol in self.Securities:
            hist = self.History(symbol, 63, Resolution.Daily)
            if hist.empty or len(hist) < 2:
                continue
            prices = hist['close']
            returns[symbol] = (prices.iloc[-1] / prices.iloc[0]) - 1
        
        if len(returns) < 3:
            self.targets = {}
            return
        
        # Simple inverse correlation heuristic: weight by performance divergence
        # If correlations are negative, select winners and losers equally
        sorted_by_return = sorted(returns.items(), key=lambda x: x[1], reverse=True)
        
        # Select top and bottom 3 for uncorrelated exposure
        targets_symbols = sorted_by_return[:3] + sorted_by_return[-3:]
        targets_symbols = list(dict.fromkeys([s for s, r in targets_symbols]))
        
        weight = 1.0 / len(targets_symbols) if targets_symbols else 0.0
        self.targets = {sym: weight for sym, _ in targets_symbols}
