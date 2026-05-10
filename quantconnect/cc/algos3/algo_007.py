from System import *
from QuantConnect import *
from QuantConnect.Data import *
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import QCAlgorithm
from datetime import datetime, timedelta

class Algo007(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Always add TQQQ
        self.AddEquity('TQQQ', Resolution.Daily)

        # Dictionary to track holdings (symbol -> placeholder)
        self.basket = {}

        # Dictionary for 21-day momentum indicators
        self.momentum = {}

        # Universe selection – top 10 by market cap
        self.AddUniverse(self.CoarseSelectionFunction)

        # Store current universe symbols (avoid using self.universe)
        self._current_universe = []

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with fundamental data and positive market cap
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        # Sort descending by market cap and take top 10
        sorted_coarse = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = [c.Symbol for c in sorted_coarse[:10]]
        self._current_universe = top10
        return top10

    def OnData(self, data):
        tqqq = self.Symbol("TQQQ")
        # Build basket from TQQQ and current universe symbols that have data
        current_basket = {tqqq: 0}
        for symbol in self._current_universe:
            if data.ContainsKey(symbol) and data[symbol] is not None:
                current_basket[symbol] = 0
        self.basket = current_basket

        # Liquidate any holdings not in current basket
        for holding in self.Portfolio.Values:
            if holding.Invested and holding.Symbol not in self.basket:
                self.Liquidate(holding.Symbol)

        # Update/create indicators for symbols in basket
        for symbol in self.basket:
            if symbol not in self.momentum:
                self.momentum[symbol] = Momentum(21)
                # Warm up indicator with historical data (21 bars before today)
                history = self.History(symbol, 21, Resolution.Daily)
                if not history.empty:
                    for time, row in history.loc[symbol].iterrows():
                        self.momentum[symbol].Update(time, row['close'])
            # Update with current bar
            if data.ContainsKey(symbol) and data[symbol] is not None:
                bar = data[symbol]
                self.momentum[symbol].Update(bar.EndTime, bar.Close)

        # Compute weights per symbol
        weights = {}
        n = len(self.basket)
        if n == 0:
            return
        for symbol in self.basket:
            if self.momentum[symbol].IsReady:
                mom_value = self.momentum[symbol].Current.Value
                weekday = self.Time.DayOfWeek
                if (weekday == DayOfWeek.Wednesday or weekday == DayOfWeek.Thursday) and mom_value > 0:
                    weight = 1.0 / n
                else:
                    weight = -1.0 / n
                weights[symbol] = weight
            else:
                weights[symbol] = 0.0

        # Set holdings for all symbols in basket
        for symbol, weight in weights.items():
            self.SetHoldings(symbol, weight)
