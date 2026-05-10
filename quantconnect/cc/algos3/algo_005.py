from AlgorithmImports import *

class Algo005(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Always add TQQQ
        tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.basket = {}  # dict tracking indicators per symbol

        # Initialize TQQQ indicators
        sma5 = self.SMA(tqqq, 5, Resolution.Daily)
        sma20 = self.SMA(tqqq, 20, Resolution.Daily)
        self.basket[tqqq] = {
            'sma5': sma5,
            'sma20': sma20,
            'prev_sma5': None,
            'prev_sma20': None
        }

        # Add universe for top 10 by market cap
        self.AddUniverse(self.CoarseSelectionFunction)
        self._tqqq_symbol = tqqq  # store for exclusion in universe

    def CoarseSelectionFunction(self, coarse):
        # Filter out TQQQ (already added) and select top 10 by market cap
        sorted_coarse = sorted(
            [c for c in coarse if c.HasFundamentalData and c.Symbol != self._tqqq_symbol],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        return [c.Symbol for c in sorted_coarse[:10]]

    def OnSecuritiesChanged(self, changes):
        # Handle added securities: add indicators
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket and symbol != self._tqqq_symbol:
                sma5 = self.SMA(symbol, 5, Resolution.Daily)
                sma20 = self.SMA(symbol, 20, Resolution.Daily)
                # Register indicators with daily bar data
                self.RegisterIndicator(symbol, sma5, Resolution.Daily)
                self.RegisterIndicator(symbol, sma20, Resolution.Daily)
                self.basket[symbol] = {
                    'sma5': sma5,
                    'sma20': sma20,
                    'prev_sma5': None,
                    'prev_sma20': None
                }

        # Handle removed securities: liquidate and remove from basket
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                self.SetHoldings(symbol, 0.0)  # close position
                del self.basket[symbol]

    def OnData(self, data):
        # Compute signals for all symbols in basket
        signals = {}
        for symbol, info in self.basket.items():
            sma5 = info['sma5']
            sma20 = info['sma20']
            if not (sma5.IsReady and sma20.IsReady):
                continue

            price = self.Securities[symbol].Price
            curr_sma5 = sma5.Current.Value
            curr_sma20 = sma20.Current.Value
            prev_sma5 = info['prev_sma5']
            prev_sma20 = info['prev_sma20']

            # Determine crossover
            cross_above = False
            cross_below = False
            if prev_sma5 is not None and prev_sma20 is not None:
                if prev_sma5 <= prev_sma20 and curr_sma5 > curr_sma20:
                    cross_above = True
                if prev_sma5 >= prev_sma20 and curr_sma5 < curr_sma20:
                    cross_below = True

            # Signal: 1 for long, -1 for short, 0 otherwise
            signal = 0
            if cross_above and price > curr_sma5:
                signal = 1
            elif cross_below and price < curr_sma5:
                signal = -1

            signals[symbol] = signal

            # Update previous values
            info['prev_sma5'] = curr_sma5
            info['prev_sma20'] = curr_sma20

        # Determine equal weight per active signal
        active_symbols = [s for s, sig in signals.items() if sig != 0]
        if active_symbols:
            weight_per = 1.0 / len(active_symbols)
            for symbol in self.basket:
                target = signals.get(symbol, 0) * weight_per
                self.SetHoldings(symbol, target)
        else:
            # No active signals: liquidate all positions
            for symbol in self.basket:
                self.SetHoldings(symbol, 0.0)
