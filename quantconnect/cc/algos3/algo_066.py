from AlgorithmImports import *

class Algo066(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.AddEquity('TQQQ', Resolution.Daily)

        # Basket dictionary: symbol -> SMA(volume, 20)
        self.basket = {}

        # Universe selection: top 10 by market cap, all sectors
        self.AddUniverse(self.CoarseSelectionFunction)

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with fundamental data and positive market cap
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        # Sort descending by market cap and take top 10
        selected = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)[:10]
        return [c.Symbol for c in selected]

    def OnSecuritiesChanged(self, changes):
        # Handle added symbols
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                # Create and register a 20-period SMA of volume
                sma = self.SMA(symbol, 20, Resolution.Daily)
                self.basket[symbol] = sma

        # Handle removed symbols
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                # Remove from basket and liquidate if held
                self.Liquidate(symbol)
                del self.basket[symbol]

    def OnData(self, data):
        # Determine which symbols in the basket have valid data today
        symbols_with_data = [s for s in self.basket if data.ContainsKey(s) and data[s] is not None]

        signals = []
        for symbol in symbols_with_data:
            sma = self.basket[symbol]
            if not sma.IsReady:
                continue

            bar = data[symbol]
            close = bar.Close
            open_price = bar.Open
            volume = bar.Volume

            # Entry condition: Close > Open AND volume > 1.5 * average volume (SMA)
            if close > open_price and volume > 1.5 * sma.Current.Value:
                signals.append(symbol)

        # Equal weight allocation among signals (total <= 1.0)
        if signals:
            weight = 1.0 / len(signals)
            for symbol in signals:
                self.SetHoldings(symbol, weight)
            # Liquidate any holdings not in signals
            for symbol in self.basket:
                if symbol not in signals:
                    self.Liquidate(symbol)
        else:
            # No signals: liquidate everything
            for symbol in self.basket:
                self.Liquidate(symbol)
