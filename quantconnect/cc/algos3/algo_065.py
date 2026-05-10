class Algo065(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        # Add TQQQ (allowed hardcoded ticker)
        self.AddEquity('TQQQ', Resolution.Daily)
        
        # Basket for all tradable symbols (TQQQ + universe)
        self.basket = {}
        
        # Initialize TQQQ indicator and state
        tqqq = Symbol.Create('TQQQ', SecurityType.Equity, Market.USA)
        self.basket['TQQQ'] = {
            'indicator': self.WilliamsPercentR(tqqq, 14),
            'previous': None,
            'holding': False
        }
        
        # Warmup for indicators
        self.SetWarmup(100, Resolution.Daily)
        
        # Universe settings and selection
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Track current universe symbols for removal handling
        self.current_universe_symbols = set()
    
    def CoarseSelectionFunction(self, coarse):
        # Exclude TQQQ from universe, select top 10 by market cap (all sectors)
        filtered = [c for c in coarse if c.HasFundamentalData and c.Symbol.Value != 'TQQQ']
        sorted_by_marketcap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = [c.Symbol for c in sorted_by_marketcap[:10]]
        self.current_universe_symbols = set(top10)
        return top10
    
    def OnSecuritiesChanged(self, changes):
        # Add new universe symbols to basket
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol.Value == 'TQQQ':
                continue
            if symbol not in self.basket:
                self.basket[symbol] = {
                    'indicator': self.WilliamsPercentR(symbol, 14),
                    'previous': None,
                    'holding': False
                }
        
        # Remove symbols that left the universe
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol.Value == 'TQQQ':
                continue
            if symbol in self.basket:
                self.Liquidate(symbol)
                del self.basket[symbol]
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Update indicators and detect cross signals
        for symbol, info in list(self.basket.items()):
            # Ensure we have data for this symbol
            if not data.ContainsKey(symbol):
                continue
            
            indicator = info['indicator']
            if not indicator.IsReady:
                continue
            
            current = indicator.Current.Value
            previous = info['previous']
            
            # Crossing logic (Williams %R oversold/overbought)
            if previous is not None:
                # Entry: cross below -80 (oversold)
                if previous > -80 and current <= -80:
                    info['holding'] = True
                # Exit: cross above -20 (overbought)
                elif previous < -20 and current >= -20:
                    info['holding'] = False
            
            # Store current value for next day
            info['previous'] = current
        
        # Rebalance: equal weight among symbols with 'holding' = True
        holdings = [sym for sym, info in self.basket.items() if info['holding']]
        
        if len(holdings) > 0:
            target = 1.0 / len(holdings)
            for sym in holdings:
                self.SetHoldings(sym, target)
            # Liquidate all others
            for sym in self.basket:
                if sym not in holdings:
                    self.SetHoldings(sym, 0)
        else:
            # No signals – liquidate everything
            for sym in self.basket:
                self.Liquidate(sym)
