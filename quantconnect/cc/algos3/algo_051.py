import numpy as np
from QuantConnect import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Market import TradeBar

class Algo051(QCAlgorithm):
    """Daily trading algorithm using RSI(5) and 20d volatility on top-10 market cap universe to trade TQQQ."""

    class SymbolData:
        def __init__(self, rsi, std):
            self.RSI = rsi
            self.StdDev = std

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ as the trading target
        self.AddEquity('TQQQ', Resolution.Daily)

        # Universe selection: top-10 by market cap across all sectors
        self.AddUniverse(self.CoarseSelectionFunction)

        # Container for basket symbols and their indicators
        self.basket = {}

        # Warm up indicators (enough for RSI(5) and STD(20))
        self.SetWarmUp(21)

    def CoarseSelectionFunction(self, coarse):
        """Select top 10 stocks by market cap from all sectors."""
        # Filter for stocks with fundamental data and a valid market cap
        coarse = [c for c in coarse if c.HasFundamentalData and c.MarketCap is not None]
        # Sort descending by market cap
        sorted_coarse = sorted(coarse, key=lambda c: c.MarketCap, reverse=True)
        # Return the top 10 symbols
        return [c.Symbol for c in sorted_coarse[:10]]

    def OnSecuritiesChanged(self, changes):
        """Update basket when universe changes."""
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # Create indicators for the new symbol
                rsi = self.RSI(symbol, 5, Resolution.Daily)
                std = self.STD(symbol, 20, Resolution.Daily)
                self.basket[symbol] = self.SymbolData(rsi, std)

        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                del self.basket[symbol]

    def OnData(self, data):
        """Main trading logic: enter TQQQ when any basket stock meets entry criteria."""
        if self.IsWarmingUp:
            return

        entry = False
        for symbol, sd in self.basket.items():
            if sd.RSI.IsReady and sd.StdDev.IsReady:
                if data.ContainsKey(symbol) and data[symbol] is not None:
                    price = data[symbol].Close
                    if price > 0:
                        # Annualized volatility = StdDev(20) * sqrt(252) / price
                        annualized_vol = sd.StdDev.Current.Value * np.sqrt(252) / price
                        # Entry condition: RSI(5) < 30 AND annualized vol < 25%
                        if sd.RSI.Current.Value < 30 and annualized_vol < 0.25:
                            entry = True
                            break

        # Manage TQQQ position (100% allocation on signal, 0% otherwise)
        if entry:
            self.SetHoldings('TQQQ', 1.0)
        else:
            self.SetHoldings('TQQQ', 0.0)
