from System import *
from QuantConnect import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Securities import Resolution
from QuantConnect.Data.UniverseSelection import *
from datetime import datetime, timedelta

class Algo054(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Add TQQQ (required by hard rules)
        self.AddEquity("TQQQ", Resolution.Daily)

        # Universe selection: top 10 by market cap (all sectors)
        self.AddUniverse(self.CoarseFilterFunction)

        # Basket to hold current universe symbols (NOT self.universe)
        self.basket = set()

        # For tracking patterns we need at least 3 bars of history
        self.min_bars = 3

    def CoarseFilterFunction(self, coarse):
        # Filter out stocks with no fundamental data or price
        filtered = [x for x in coarse if x.HasFundamentalData and x.Price > 0]
        # Sort by market cap descending, take top 10
        sorted_by_market_cap = sorted(filtered, key=lambda x: x.MarketCap, reverse=True)
        top10 = sorted_by_market_cap[:10]
        return [x.Symbol for x in top10]

    def OnSecuritiesChanged(self, changes):
        # Update basket with the current universe members
        for added in changes.AddedSecurities:
            self.basket.add(added.Symbol)
        for removed in changes.RemovedSecurities:
            self.basket.discard(removed.Symbol)

    def OnData(self, data):
        # Liquidate any symbols that are no longer in the basket
        for symbol in list(self.Portfolio.Keys):
            if symbol not in self.basket and symbol != "TQQQ":
                if self.Portfolio[symbol].Invested:
                    self.SetHoldings(symbol, 0)

        # Collect signals for basket symbols
        signals = []
        for symbol in self.basket:
            if not self.Securities.ContainsKey(symbol):
                continue
            # Need at least 3 daily bars to detect pattern
            bars = self.History(symbol, self.min_bars, Resolution.Daily)
            if bars.empty or len(bars) < self.min_bars:
                continue

            # Extract the three most recent completed daily bars (today, yesterday, day before yesterday)
            bar0 = bars.iloc[-3]   # day-3
            bar1 = bars.iloc[-2]   # day-2
            bar2 = bars.iloc[-1]   # day-1 (yesterday)

            # Define inside bar: bar1's range inside bar0's range
            inside_bar = bar1.High <= bar0.High and bar1.Low >= bar0.Low
            # Define outside bar: bar2's range engulfs bar1's range
            outside_bar = bar2.High > bar1.High and bar2.Low < bar1.Low

            # 3‑bar inside‑outside pattern: inside bar followed by outside bar
            if inside_bar and outside_bar:
                signals.append(symbol)

        # If no signals, go all cash
        if len(signals) == 0:
            for symbol in self.basket:
                if self.Portfolio[symbol].Invested:
                    self.SetHoldings(symbol, 0)
            return

        # Equal weight among all symbols with a signal
        weight = 1.0 / len(signals)
        for symbol in signals:
            self.SetHoldings(symbol, weight)

        # Liquidate any basket symbols that did not signal
        for symbol in self.basket:
            if symbol not in signals and self.Portfolio[symbol].Invested:
                self.SetHoldings(symbol, 0)
