from AlgorithmImports import *

class Algo027(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Fixed TQQQ position
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        # Dynamic universe of top 10 mega-cap stocks
        self.AddUniverse(self.CoarseSelectionFunction)

        # Indicator storage
        self.indicators = {}

        # Basket for holdings tracking (symbol -> signal)
        self.basket = {}

        # Warmup period for indicators
        self.SetWarmup(20, Resolution.Daily)

        # Register indicator for TQQQ
        self.indicators[self.tqqq] = self.BB(self.tqqq, 20, 2, MovingAverageType.Simple, Resolution.Daily)

    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and positive market cap
        filtered = [x for x in coarse if x.HasFundamentalData and x.MarketCap > 0]
        # Sort by market cap descending and take top 10
        sorted_by_cap = sorted(filtered, key=lambda x: x.MarketCap, reverse=True)
        top10 = sorted_by_cap[:10]
        return [x.Symbol for x in top10]

    def OnSecuritiesChanged(self, changes):
        # Remove indicators for deleted securities
        for removed in changes.RemovedSecurities:
            sym = removed.Symbol
            if sym in self.indicators:
                del self.indicators[sym]
            if sym in self.basket:
                del self.basket[sym]

        # Add indicators for new securities
        for added in changes.AddedSecurities:
            sym = added.Symbol
            if sym not in self.indicators:
                self.indicators[sym] = self.BB(sym, 20, 2, MovingAverageType.Simple, Resolution.Daily)

    def OnData(self, data):
        # Skip during warmup
        if self.IsWarmingUp:
            return

        # Clear previous basket signals
        self.basket.clear()

        # Collect all symbols we care about: TQQQ + current universe symbols
        symbols = [self.tqqq] + [added.Symbol for added in self.Securities.Values
                                 if added.Symbol != self.tqqq and added.Symbol in self.indicators]

        # Compute signals for each symbol
        for sym in symbols:
            indicator = self.indicators.get(sym)
            if indicator is not None and indicator.IsReady:
                percent_b = indicator.PercentB.Current.Value
                if percent_b < 0:
                    signal = 1  # Long
                elif percent_b > 1:
                    signal = -1  # Short
                else:
                    signal = 0
            else:
                signal = 0
            self.basket[sym] = signal

        # Count active signals
        long_count = sum(1 for s in self.basket.values() if s == 1)
        short_count = sum(1 for s in self.basket.values() if s == -1)
        total_active = long_count + short_count

        # If no active signals, liquidate all
        if total_active == 0:
            for sym in symbols:
                self.SetHoldings(sym, 0)
            # Also liquidate any symbols that were previously held but are no longer in universe
            for sym in self.Portfolio.Keys:
                if sym not in symbols:
                    self.SetHoldings(sym, 0)
            return

        # Allocate equally among active positions (long positive, short negative)
        weight_per_position = 1.0 / total_active

        # Set target weights
        for sym in symbols:
            signal = self.basket.get(sym, 0)
            target = weight_per_position * signal
            self.SetHoldings(sym, target)

        # Liquidate any symbols not in current basket (e.g., dropped from universe)
        for sym in self.Portfolio.Keys:
            if sym not in symbols:
                self.SetHoldings(sym, 0)