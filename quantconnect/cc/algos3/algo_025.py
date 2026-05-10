class Algo025(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        
        self.AddEquity("TQQQ", Resolution.Daily)
        self.AddUniverse(self.CoarseFilter)
        
        self.basket = {}          # Symbol -> target weight (maintained daily)
        self.indicators = {}       # Symbol -> MFI
        self._all_traded = set()   # Symbols currently in basket (including TQQQ)
        
        # Initialize TQQQ
        tqqq = self.Symbol("TQQQ")
        self._all_traded.add(tqqq)
        self._create_and_warm_indicator(tqqq)
        
        self.mfi_period = 14
        self.oversold = 30
        self.overbought = 70
    
    def CoarseFilter(self, coarse):
        selected = [c for c in coarse if c.HasFundamentalData and c.Symbol.Value != "TQQQ"]
        sorted_by_mcap = sorted(selected, key=lambda c: c.MarketCap, reverse=True)
        return [c.Symbol for c in sorted_by_mcap[:10]]
    
    def _create_and_warm_indicator(self, symbol):
        mfi = MoneyFlowIndex(self.mfi_period)
        self.indicators[symbol] = mfi
        history = self.History(symbol, self.mfi_period, Resolution.Daily)
        if not history.empty:
            for index, row in history.iterrows():
                bar = TradeBar(symbol, row["close"], row["high"], row["low"], row["open"], row["volume"], row["close"])
                mfi.Update(bar)
    
    def OnSecuritiesChanged(self, changes):
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self._all_traded:
                self._all_traded.add(symbol)
                self._create_and_warm_indicator(symbol)
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self._all_traded:
                self._all_traded.remove(symbol)
            if symbol in self.indicators:
                del self.indicators[symbol]
    
    def OnData(self, data):
        self._rebalance()
    
    def _rebalance(self):
        # Compute signals for all symbols we want to trade
        buy_signals = []
        for symbol in self._all_traded:
            mfi = self.indicators.get(symbol)
            if mfi is not None and mfi.IsReady:
                value = mfi.Current.Value
                if value < self.oversold:
                    buy_signals.append(symbol)
        
        # Equal weight among signals
        if len(buy_signals) > 0:
            weight = 1.0 / len(buy_signals)
        else:
            weight = 0.0
        
        # Build target dictionary for all symbols: signals get weight, others get 0
        targets = {}
        for symbol in self._all_traded:
            if symbol in buy_signals:
                targets[symbol] = weight
            else:
                targets[symbol] = 0.0
        
        # Also liquidate any holdings that are no longer in _all_traded
        for symbol in self.Portfolio.Keys:
            if symbol not in self._all_traded:
                targets[symbol] = 0.0
        
        # Execute SetHoldings for all targets
        for symbol, target in targets.items():
            self.SetHoldings(symbol, target)
        
        # Update basket for logging/tracking (not strictly necessary)
        self.basket = {symbol: target for symbol, target in targets.items() if symbol in self._all_traded}