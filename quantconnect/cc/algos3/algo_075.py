class Algo075(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        
        # Sector ETFs: Select a representative set (original 9 sectors before 2018)
        self.sectors = [
            "XLY",  # Consumer Discretionary
            "XLP",  # Consumer Staples
            "XLE",  # Energy
            "XLF",  # Financials
            "XLV",  # Health Care
            "XLI",  # Industrials
            "XLB",  # Materials
            "XLK",  # Technology
            "XLU"   # Utilities
        ]
        # Real Estate (XLRE) and Communication Services (XLC) started later, omitted for simplicity.
        
        self.lookback = 90  # Days for rolling Sharpe calculation
        self.top_k = 3      # Number of top sectors to hold
        
        # Add sector ETFs to the universe
        self.symbols = []
        for sector in self.sectors:
            symbol = self.AddEquity(sector, Resolution.Daily).Symbol
            self.symbols.append(symbol)
        
        self.SetWarmUp(self.lookback)  # Request warmup period equal to lookback
        
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Collect daily returns for each sector over the lookback period
        hist = self.History(self.symbols, self.lookback, Resolution.Daily)
        if hist.empty:
            return
        
        # Compute Sharpe ratios
        sharpe_ratios = {}
        for symbol in self.symbols:
            if symbol not in hist.index.levels[0]:
                continue
            prices = hist.loc[symbol]["close"].dropna()
            if len(prices) < self.lookback:
                continue
            returns = prices.pct_change().dropna()
            if len(returns) < 2:
                continue
            mean_return = returns.mean()
            std_return = returns.std()
            if std_return == 0:
                continue
            sharpe = mean_return / std_return  # Raw daily Sharpe, no annualization needed for ranking
            sharpe_ratios[symbol] = sharpe
        
        if not sharpe_ratios:
            return
        
        # Rank by Sharpe (highest first)
        sorted_sectors = sorted(sharpe_ratios.items(), key=lambda x: x[1], reverse=True)
        top_sectors = [sym for sym, _ in sorted_sectors[:self.top_k]]
        
        # Equal weight allocation
        weight = 1.0 / len(top_sectors) if top_sectors else 0
        
        # Liquidate sectors not in top selection
        for symbol in self.Portfolio.Keys:
            if symbol in self.symbols and symbol not in top_sectors:
                self.SetHoldings(symbol, 0)
        
        # Invest in top sectors
        for symbol in top_sectors:
            self.SetHoldings(symbol, weight)