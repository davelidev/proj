class Algo076(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Resolution for data and trading
        self.UniverseSettings.Resolution = Resolution.Daily
        self.UniverseSettings.DataNormalizationMode = DataNormalizationMode.Adjusted

        # No leverage - force leverage 1 on all securities
        self.SetSecurityInitializer(lambda x: x.SetLeverage(1.0))

        # Use fundamental universe to select liquid stocks
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)

        # Number of stocks to hold
        self.NumberStocks = 10

        # Rebalance every Monday
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("SPY", 30),
                         Action(self.Rebalance))

        # Store current target weights
        self.targets = dict()
        self.lastRebalance = datetime.min

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with price > $5 and sufficient volume
        if self.Time < self.lastRebalance + timedelta(days=5):
            return Universe.Unchanged
        sorted_by_dollar_volume = sorted([x for x in coarse if x.HasFundamentalData and x.Price > 5],
                                         key=lambda x: x.DollarVolume, reverse=True)
        return [x.Symbol for x in sorted_by_dollar_volume[:200]]

    def FineSelectionFunction(self, fine):
        # Further filter for market cap and earnings data
        sorted_by_market_cap = sorted([x for x in fine if x.EarningReports.BasicAverageShares>0],
                                      key=lambda x: x.MarketCap, reverse=True)
        top = [x.Symbol for x in sorted_by_market_cap[:self.NumberStocks]]
        return top

    def Rebalance(self):
        self.lastRebalance = self.Time

        # Get currently selected symbols from universe
        selected_symbols = [x.Symbol for x in self.CurrentSlice.Fundamental]
        if len(selected_symbols) == 0:
            return

        # Calculate weights: equal weight, then zero for stocks near earnings
        raw_weight = 1.0 / len(selected_symbols)
        weights = {}

        for symbol in selected_symbols:
            # Get next earnings date
            next_eps_date = self.get_next_earnings_date(symbol)
            if next_eps_date is not None:
                # Check if earnings is within 5 days (before or after)
                days_before = 5
                days_after = 5
                if abs((next_eps_date - self.Time).days) <= days_before or \
                   (next_eps_date - self.Time).days < 0 and abs((next_eps_date - self.Time).days) <= days_after:
                    # Avoid holding this stock near earnings
                    weights[symbol] = 0.0
                else:
                    weights[symbol] = raw_weight
            else:
                # No earnings data, assume safe
                weights[symbol] = raw_weight

        # Normalize weights to sum to 1 (cash gets remainder)
        total_weight = sum(weights.values())
        if total_weight > 0:
            for symbol in weights:
                weights[symbol] = min(weights[symbol] / total_weight, 1.0)

        # Apply target weights
        for symbol, weight in weights.items():
            self.SetHoldings(symbol, weight)

        # Liquidate symbols no longer in universe or with zero weight
        for symbol, weight in list(self.Securities.Keys):
            if symbol not in weights:
                self.Liquidate(symbol)

    def OnData(self, data):
        # Trading done in scheduled event; just handle splits/dividends if needed
        pass

    def get_next_earnings_date(self, symbol):
        # Try to fetch next earnings date from fundamental data
        # Use the underlying Symbol object to get fundamental data from current slice
        fundamental = self.CurrentSlice.Fundamental
        for x in fundamental:
            if x.Symbol == symbol:
                try:
                    # EarningReports object contains next earnings date
                    next_date = x.EarningReports.EarningsDate
                    if next_date:
                        return next_date
                except:
                    pass
        return None
