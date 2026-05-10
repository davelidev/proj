from QuantConnect import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import WilliamsPercentile, WilliamsR
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Algorithm.Framework.Selection import CoarseFundamentalUniverseSelectionModel
from System.Collections.Generic import List

class Algo015(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ for signal generation only
        self.AddEquity('TQQQ', Resolution.Daily)
        # Williams %R indicator with period 14
        self.wr = self.WR('TQQQ', 14, Resolution.Daily)

        # Universe selection for top 10 market cap stocks
        self.AddUniverse(self.CoarseSelectionFunction)
        self.basket = {}  # will hold the current universe symbols (as keys)

    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and market cap
        sorted_by_cap = sorted(
            [x for x in coarse if x.HasFundamentalData],
            key=lambda x: x.MarketCap,
            reverse=True
        )
        # Take top 10
        top10 = sorted_by_cap[:10]
        # Update basket dictionary
        self.basket = {x.Symbol: 0 for x in top10}
        # Return symbols for universe addition
        return [x.Symbol for x in top10]

    def OnData(self, data):
        # Ensure indicator is ready
        if not self.wr.IsReady:
            return

        wr_value = self.wr.Current.Value

        # Determine signal (long or short) or neutral
        if wr_value > -20:
            signal = -1  # short (overbought)
        elif wr_value < -80:
            signal = 1   # long (oversold)
        else:
            signal = 0   # neutral

        # Symbols to trade: TQQQ is kept flat, basket symbols get signal
        TQQQ = self.Symbol("TQQQ")
        basket_symbols = list(self.basket.keys())

        # First, liquidate any positions not in current basket and TQQQ
        for symbol in list(self.Portfolio.Keys):
            if symbol == TQQQ:
                continue
            if symbol not in basket_symbols:
                self.SetHoldings(symbol, 0)

        # Always liquidate TQQQ (we never hold it)
        self.SetHoldings(TQQQ, 0)

        # If neutral signal, all remaining basket positions set to 0
        if signal == 0:
            for symbol in basket_symbols:
                self.SetHoldings(symbol, 0)
            return

        # Apply equal weight among basket symbols
        weight = signal * (1.0 / len(basket_symbols)) if len(basket_symbols) > 0 else 0
        for symbol in basket_symbols:
            self.SetHoldings(symbol, weight)
