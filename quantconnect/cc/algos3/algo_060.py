from AlgorithmImports import *

class Algo060(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add hardcoded TQQQ (not used in trading)
        self.AddEquity("TQQQ", Resolution.Daily)

        # Universe selection for top-10 by market cap across all sectors
        self.AddUniverse(self.CoarseSelectionFunction)

        # Internal storage
        self.basket = {}        # current universe symbols
        self.roc = {}           # ROC(5) indicators per symbol

    def CoarseSelectionFunction(self, coarse):
        # Filter for top-10 by market cap
        sorted_by_mc = sorted([c for c in coarse if c.HasFundamentalData and c.MarketCap is not None],
                               key=lambda x: x.MarketCap, reverse=True)
        selected = [s.Symbol for s in sorted_by_mc[:10]]

        # Remove symbols no longer in universe
        for symbol in list(self.basket.keys()):
            if symbol not in selected:
                # Remove indicator and liquidate any position
                if symbol in self.roc:
                    self.roc.pop(symbol, None)
                if self.Portfolio[symbol].Invested:
                    self.Liquidate(symbol)
                self.basket.pop(symbol, None)

        # Add new symbols
        for symbol in selected:
            if symbol not in self.basket:
                self.AddEquity(symbol, Resolution.Daily)
                self.basket[symbol] = symbol
                self.roc[symbol] = self.ROC(symbol, 5, Resolution.Daily)

        return selected

    def OnData(self, data):
        # Collect current ROC values for all basket symbols that are ready
        roc_values = {}
        for symbol in self.basket:
            if symbol in self.roc and self.roc[symbol].IsReady:
                value = self.roc[symbol].Current.Value
                roc_values[symbol] = value

        if len(roc_values) == 0:
            return

        # Compute percentile rank (0..1) across the basket
        import pandas as pd
        series = pd.Series(roc_values).rank(pct=True)

        # Select symbols in the lowest 20th percentile (oversold mean-reversion)
        selected = [symbol for symbol, rank in series.items() if rank < 0.2]

        if len(selected) == 0:
            # No signals today → hold cash
            self.SetHoldings(self.basket, [0.0] * len(self.basket))
            return

        # Allocate equal weight, total <= 1.0
        weight = 1.0 / len(selected)
        # Build target weights dict for all basket symbols (0 for non-selected)
        targets = {sym: weight if sym in selected else 0.0 for sym in self.basket}
        # Ensure TQQQ is always 0
        tqqq = Symbol.Create("TQQQ", SecurityType.Equity, Market.USA)
        if tqqq in self.Portfolio:
            targets[tqqq] = 0.0

        # Set holdings
        self.SetHoldings(targets)

        # Plot for verification
        self.Plot("BasketSize", "Count", len(self.basket))
        self.Plot("SelectedCount", "Count", len(selected))
