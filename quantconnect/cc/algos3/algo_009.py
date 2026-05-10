from QuantConnect import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar
from datetime import datetime

class Algo009(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Always add TQQQ
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        # Dictionary to store BollingerBand indicators keyed by Symbol
        self.basket = {}

        # Indicator for TQQQ
        bb_tqqq = BollingerBands(20, 2, MovingAverageType.Simple)
        self.basket[self.tqqq] = bb_tqqq
        self.RegisterIndicator(self.tqqq, bb_tqqq, Resolution.Daily)

        # Dynamic universe: top 10 by market cap
        self.AddUniverse(self.CoarseSelectionFunction)
        self._universe_symbols = set()

    def CoarseSelectionFunction(self, coarse):
        # Filter and sort by market cap descending, take top 10
        sorted_by_cap = sorted(
            [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        top_symbols = [c.Symbol for c in sorted_by_cap[:10]]

        # Add indicators for new symbols
        for symbol in top_symbols:
            if symbol not in self.basket:
                bb = BollingerBands(20, 2, MovingAverageType.Simple)
                self.basket[symbol] = bb
                self.RegisterIndicator(symbol, bb, Resolution.Daily)

        # Keep track of current universe symbols for later use
        self._universe_symbols = set(top_symbols)
        return top_symbols

    def OnData(self, data):
        # Active symbols: TQQQ always + current universe
        active = self._universe_symbols | {self.tqqq}

        # Liquidate and remove symbols no longer in active set
        for symbol in list(self.basket.keys()):
            if symbol not in active:
                self.SetHoldings(symbol, 0)
                del self.basket[symbol]

        # Number of active symbols for equal weight calculation
        n = len(active)
        if n == 0:
            return

        # Process each active symbol
        for symbol in active:
            if symbol not in self.basket:
                continue
            bb = self.basket[symbol]
            if not bb.IsReady or not data.ContainsKey(symbol):
                continue
            price = data[symbol].Close
            lower = bb.LowerBand.Current.Value
            upper = bb.UpperBand.Current.Value

            # Weight per symbol: equal absolute weight
            weight = 0.0
            if price <= lower:
                weight = 1.0 / n
            elif price >= upper:
                weight = -1.0 / n

            self.SetHoldings(symbol, weight)
