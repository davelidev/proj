from AlgorithmImports import *

class Algo030(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.AddEquity("TQQQ", Resolution.Daily)
        self.symbol = self.Symbol("TQQQ")

        # Linear regression slope over 20 days
        self.lr = LinearRegression(20)

        # Warm up the indicator with 20 daily bars
        self.SetWarmUp(20, Resolution.Daily)

        # Universe for top-10 mega-cap stocks (by market cap)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseFilter, self.FineFilter)

        # Dictionary to track universe constituents (NOT used for trading)
        self.basket = {}

    def CoarseFilter(self, coarse):
        # Basic liquidity and price filter
        filtered = [c for c in coarse if c.Price > 5 and c.HasFundamentalData]
        sorted_by_dollar_vol = sorted(filtered, key=lambda c: c.DollarVolume, reverse=True)
        # Take top 100 by dollar volume for fine selection
        return [c.Symbol for c in sorted_by_dollar_vol[:100]]

    def FineFilter(self, fine):
        # Sort by market cap descending and pick top 10
        sorted_by_marketcap = sorted(fine, key=lambda f: f.MarketCap, reverse=True)
        top10 = [f.Symbol for f in sorted_by_marketcap[:10]]
        self.basket = {sym: None for sym in top10}
        return top10

    def OnData(self, data):
        # Wait until warmup is complete
        if self.IsWarmingUp:
            return

        # Update linear regression indicator
        price = self.Securities[self.symbol].Close
        self.lr.Update(self.Time, price)

        if not self.lr.IsReady:
            return

        slope = self.lr.Slope.Current.Value

        # Determine position: long if slope > 0, short if slope < 0, flat otherwise
        if slope > 0:
            self.SetHoldings(self.symbol, 1.0)
        elif slope < 0:
            self.SetHoldings(self.symbol, -1.0)
        else:
            self.SetHoldings(self.symbol, 0.0)