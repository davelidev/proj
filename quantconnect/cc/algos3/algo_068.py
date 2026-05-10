class Algo068(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.AddEquity("TQQQ", Resolution.Daily)
        
        # Universe selection: top 10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Basket of symbols we are monitoring (dictionary of -> indicators)
        self.basket = {}
        
        # Parameters for the entry pattern
        self.lookback = 20          # for highest high
        self.adx_period = 14
        
        # Warm-up period for indicators (will be applied to each new symbol)
        self.SetWarmUp(self.lookback + self.adx_period)
    
    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with price > $5 and positive market cap, sort by market cap descending
        sorted_coarse = sorted(
            [c for c in coarse if c.HasFundamentalData and c.Price > 5 and c.MarketCap > 0],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        top10 = [c.Symbol for c in sorted_coarse[:10]]
        
        # Always include TQQQ (if not already in top10)
        tqqq = self.Symbol("TQQQ")
        if tqqq not in top10:
            top10.append(tqqq)
        return top10
    
    def OnSecuritiesChanged(self, changes):
        # When new symbols are added, create indicators and warm them up
        for symbol in changes.AddedSecurities:
            if symbol not in self.basket:
                # Create indicators
                adx = self.ADX(symbol, self.adx_period, Resolution.Daily)
                max_high = self.MAX(symbol, self.lookback, Resolution.Daily)
                self.basket[symbol] = {"ADX": adx, "MAX": max_high}
                
                # Warm-up with historical data
                history = self.History[TradeBar](symbol, self.lookback + self.adx_period, Resolution.Daily)
                if not history.empty:
                    for bar in history:
                        adx.Update(bar)
                        max_high.Update(bar.High)
        
        # When symbols are removed, liquidate and remove from basket
        for symbol in changes.RemovedSecurities:
            if symbol in self.basket:
                self.Liquidate(symbol)
                del self.basket[symbol]
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        # Determine target weights for each symbol in the basket
        target_weights = {}
        for symbol, indicators in self.basket.items():
            if not data.Bars.ContainsKey(symbol):
                continue
            if not indicators["ADX"].IsReady or not indicators["MAX"].IsReady:
                continue
            
            adx = indicators["ADX"].Current.Value
            max_high = indicators["MAX"].Current.Value
            price = data[symbol].Close
            
            # Check if already invested
            invested = self.Portfolio[symbol].Invested
            
            if invested:
                # Exit if ADX falls below 20
                if adx < 20:
                    target_weights[symbol] = 0
                else:
                    target_weights[symbol] = 1  # placeholder, will be normalized
            else:
                # Entry condition: close at or above highest high of lookback period AND ADX > 30
                if price >= max_high and adx > 30:
                    target_weights[symbol] = 1
        
        # Normalize weights for long positions to sum to 1
        long_symbols = [s for s, w in target_weights.items() if w > 0]
        if long_symbols:
            weight_per = 1.0 / len(long_symbols)
            for s in long_symbols:
                target_weights[s] = weight_per
        
        # For symbols not in target_weights, set weight to 0 (sell if held)
        for symbol in self.basket:
            if symbol not in target_weights:
                target_weights[symbol] = 0
        
        # Execute trades
        for symbol, weight in target_weights.items():
            self.SetHoldings(symbol, weight)
