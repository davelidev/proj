from AlgorithmImports import *

class Algo064(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.SetWarmUp(20)

        # Add TQQQ separately (hardcoded ticker)
        self.AddEquity('TQQQ', Resolution.Daily)

        # Universe for top-10 by market cap (all sectors)
        self.AddUniverse(self.CoarseSelectionFunction)

        # Basket to hold dynamic symbols and their Keltner Channel indicators
        self.basket = {}

        # Strategy parameters
        self.entry_weight = 0.1  # 10% per position, max 10 stocks = 100%
        self.keltner_period = 20
        self.keltner_multiplier = 1.5
        self.moving_average_type = MovingAverageType.Simple

    def CoarseSelectionFunction(self, coarse):
        # Filter for fundamental data, price > $5, and non-zero volume
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5 and c.Volume > 0]
        # Sort by market cap descending and take top 10
        sorted_by_cap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        return [c.Symbol for c in sorted_by_cap[:10]]

    def OnSecuritiesChanged(self, changes):
        # Remove old symbols
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                self.Liquidate(symbol)
                del self.basket[symbol]

        # Add new symbols
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # Create Keltner Channel indicator
                keltner = KeltnerChannels(self.keltner_period, self.keltner_multiplier, self.moving_average_type)
                self.RegisterIndicator(symbol, keltner, Resolution.Daily)
                self.basket[symbol] = keltner

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        for symbol, keltner in self.basket.items():
            # Ensure we have data for this symbol
            if not (data.Bars.ContainsKey(symbol) or data.QuoteBars.ContainsKey(symbol)):
                continue
            if not keltner.IsReady:
                continue

            # Get current price
            if data.Bars.ContainsKey(symbol):
                close = data.Bars[symbol].Close
            else:
                close = data.QuoteBars[symbol].Close

            upper_band = keltner.UpperBand.Current.Value
            lower_band = keltner.LowerBand.Current.Value

            holdings = self.Portfolio[symbol]
            invested = holdings.Invested

            # Entry: close above upper band
            if not invested and close > upper_band:
                self.SetHoldings(symbol, self.entry_weight)

            # Exit: close below lower band
            elif invested and close < lower_band:
                self.SetHoldings(symbol, 0)
