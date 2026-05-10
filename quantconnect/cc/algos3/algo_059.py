class Algo059(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ as required hardcoded ticker
        self.AddEquity("TQQQ", Resolution.Daily)

        # Universe selection: top 10 by market cap across all sectors
        self.AddUniverse(self.CoarseSelectionFunction)

        # Container for selected symbols and their Bollinger Bands indicators
        self.basket = {}
        # Track whether price was below lower band on previous day
        self.below_lower = {}

    def CoarseSelectionFunction(self, coarse):
        # Filter securities with fundamental data and sort by market cap descending
        sorted_by_market_cap = sorted(
            [c for c in coarse if c.HasFundamentalData],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        top10 = [c.Symbol for c in sorted_by_market_cap[:10]]

        # Remove symbols that are no longer in the universe
        for symbol in list(self.basket.keys()):
            if symbol not in top10:
                del self.basket[symbol]
                del self.below_lower[symbol]

        # Add new symbols
        for symbol in top10:
            if symbol not in self.basket:
                bb = BollingerBands(20, 2, MovingAverageType.Simple)
                self.RegisterIndicator(symbol, bb, Resolution.Daily)
                self.basket[symbol] = bb
                self.below_lower[symbol] = False

        return top10

    def OnData(self, data):
        # Number of symbols currently in basket (used for equal weight allocation)
        n = len(self.basket)
        if n == 0:
            return

        for symbol, bb in self.basket.items():
            if symbol not in self.Securities or not self.Securities[symbol].HasData:
                continue
            if not bb.IsReady:
                continue

            close = self.Securities[symbol].Close
            lower = bb.LowerBand.Current.Value
            upper = bb.UpperBand.Current.Value

            # Exit: price touches upper band -> sell full position
            if self.Portfolio[symbol].Invested and close >= upper:
                self.SetHoldings(symbol, 0)

            # Entry: price was below lower band yesterday and crosses back above today
            if not self.Portfolio[symbol].Invested and self.below_lower.get(symbol, False) and close >= lower:
                # Allocate equally among all basket symbols (no leverage)
                weight = 1.0 / n
                self.SetHoldings(symbol, weight)

            # Update flag for next day: was today's close below lower band?
            self.below_lower[symbol] = close < lower
