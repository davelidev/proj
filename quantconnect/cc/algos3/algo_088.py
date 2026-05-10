from System import *
from QuantConnect import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.Market import TradeBar
from collections import deque
import math

class MeanReversionSector(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(100000)

        # Sector ETFs
        self.sectors = {
            "XLY": "Consumer Discretionary",
            "XLP": "Consumer Staples",
            "XLE": "Energy",
            "XLF": "Financials",
            "XLV": "Health Care",
            "XLI": "Industrials",
            "XLB": "Materials",
            "XLK": "Technology",
            "XLU": "Utilities",
            "XLRE": "Real Estate"
        }

        self.symbols = []
        self.windows = {}
        for ticker in self.sectors:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols.append(symbol)
            self.windows[symbol] = deque(maxlen=252)

        # Warm-up period: we will start trading after we have 252 days
        self.trading_started = False

    def OnData(self, data):
        # Collect prices and update windows
        for symbol in self.symbols:
            if data.Bars.ContainsKey(symbol):
                price = data.Bars[symbol].Close
                self.windows[symbol].append(price)

        # We need at least 252 days of data for all symbols to compute mean and std
        # Check if all windows are full
        if not self.trading_started:
            if all(len(self.windows[sym]) == 252 for sym in self.symbols):
                self.trading_started = True
            else:
                return  # Wait until we have enough data

        # Compute signals
        qualifiers = []
        for symbol in self.symbols:
            if data.Bars.ContainsKey(symbol):
                window = self.windows[symbol]
                if len(window) == 252:
                    # Compute mean and standard deviation of the last 252 closing prices
                    prices = list(window)
                    mean = sum(prices) / 252.0
                    variance = sum((p - mean) ** 2 for p in prices) / 252.0
                    std = math.sqrt(variance)
                    current_price = data.Bars[symbol].Close
                    # Signal: price < mean - std (more than 1 std below the MA)
                    if current_price < mean - std:
                        qualifiers.append(symbol)
                # else skip if not enough data (should not happen once trading started)

        # Set holdings
        if len(qualifiers) > 0:
            weight = 1.0 / len(qualifiers)
            for symbol in self.symbols:
                if symbol in qualifiers:
                    self.SetHoldings(symbol, weight)
                else:
                    self.SetHoldings(symbol, 0)
        else:
            # No qualifiers: set all to zero (cash)
            for symbol in self.symbols:
                self.SetHoldings(symbol, 0)
