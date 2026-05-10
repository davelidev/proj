class Algo076(BaseSubAlgo):
    """
    Daily sector rotation strategy with earnings season adjustments.
    Inherits from BaseSubAlgo and implements initialize() and update_targets().
    
    Strategy:
        - Holds an equally-weighted portfolio of major sector ETFs.
        - During earnings season (months January, April, July, October), 
          reduces exposure by a factor (e.g., 50%) to limit gap risk.
        - Outside earnings season, returns to full target weights.
    
    This version uses a simple calendar rule for earnings season months.
    """
    
    def initialize(self):
        """Initialize algorithm: set symbols, add securities, and create targets dict."""
        self.targets = {}
        
        # Define sector ETFs (US sector SPDRs)
        self.sector_tickers = [
            "XLF",  # Financials
            "XLK",  # Technology
            "XLV",  # Health Care
            "XLE",  # Energy
            "XLI",  # Industrials
            "XLB",  # Materials
            "XLP",  # Consumer Staples
            "XLY",  # Consumer Discretionary
            "XLU",  # Utilities
            "XLRE", # Real Estate
            "XLC"   # Communication Services
        ]
        
        # Add each sector ETF with daily resolution
        for ticker in self.sector_tickers:
            self.AddEquity(ticker, Resolution.Daily)
        
        # Store symbols for later use
        self.symbols = [self.Symbol(t) for t in self.sector_tickers]
        
        # Earnings season months (January, April, July, October)
        self.earnings_months = [1, 4, 7, 10]
        
        # Reduction factor during earnings season (0.5 means 50% exposure)
        self.reduction_factor = 0.5
    
    def update_targets(self):
        """
        Update the target weights dictionary based on the current date.
        Called each trading day by the base class; must set self.targets dict.
        """
        current_time = self.Time
        current_month = current_time.month
        
        # Determine if we are in an earnings season month
        in_earnings_season = current_month in self.earnings_months
        
        # Equal weight per sector (1 / number of sectors)
        base_weight = 1.0 / len(self.symbols)
        
        # Apply reduction if in earnings season
        weight_multiplier = self.reduction_factor if in_earnings_season else 1.0
        target_weight = base_weight * weight_multiplier
        
        # Build the targets dict for all sector symbols
        self.targets.clear()
        for symbol in self.symbols:
            self.targets[symbol] = target_weight
        
        # Note: remaining cash is not explicitly targeted; base class will 
        # allocate the weight and leave the rest in cash automatically.
