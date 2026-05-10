from AlgorithmImports import *

class Algo019(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ and its indicators
        self.AddEquity('TQQQ', Resolution.Daily)
        tqqq = self.Symbol('TQQQ')
        rsi_tqqq = self.RSI(tqqq, 14, Resolution.Daily)
        max_tqqq = self.MAX(tqqq, 21, Resolution.Daily)
        self.basket = {
            tqqq: {
                'rsi': rsi_tqqq,
                'max': max_tqqq,
                'last_high_close': None,
                'last_high_rsi': None
            }
        }

        # Add dynamic universe (top-10 by market cap)
        self.AddUniverse(self.CoarseSelectionFunction)

    def CoarseSelectionFunction(self, coarse):
        # Exclude TQQQ (already added separately)
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 0 and c.Symbol != self.Symbol('TQQQ')]
        sorted_by_mc = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_mc[:10]
        return [c.Symbol for c in top10]

    def OnSecuritiesChanged(self, changes):
        # Remove stocks that left the universe (except TQQQ)
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol != self.Symbol('TQQQ') and symbol in self.basket:
                self.basket.pop(symbol)

        # Add new stocks from the universe
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol != self.Symbol('TQQQ') and symbol not in self.basket:
                rsi = self.RSI(symbol, 14, Resolution.Daily)
                mxx = self.MAX(symbol, 21, Resolution.Daily)
                self.basket[symbol] = {
                    'rsi': rsi,
                    'max': mxx,
                    'last_high_close': None,
                    'last_high_rsi': None
                }

    def OnData(self, data):
        # Prepare targets for each symbol with ready indicators
        targets = {}
        for symbol, info in self.basket.items():
            if not data.ContainsKey(symbol):
                continue
            close = data[symbol].Close
            rsi_ind = info['rsi']
            max_ind = info['max']
            if not rsi_ind.IsReady or not max_ind.IsReady:
                continue

            current_rsi = rsi_ind.Current.Value
            current_max = max_ind.Current.Value
            last_high_close = info['last_high_close']
            last_high_rsi = info['last_high_rsi']

            # Detect new 21-day high
            is_new_high = (close >= current_max) and (last_high_close is None or close > last_high_close)

            if is_new_high:
                # Check for bearish divergence
                if last_high_rsi is not None and current_rsi < last_high_rsi:
                    targets[symbol] = 0.0  # sell signal
                # Update stored high data
                info['last_high_close'] = close
                info['last_high_rsi'] = current_rsi

        # Compute equal weight for all active symbols (including those not sold)
        active_symbols = [s for s in self.basket if data.ContainsKey(s) and self.basket[s]['rsi'].IsReady and self.basket[s]['max'].IsReady]
        if not active_symbols:
            return

        equal_weight = 1.0 / len(active_symbols)
        final_targets = {}
        for s in active_symbols:
            if s in targets:
                final_targets[s] = targets[s]  # already 0 for sell signals
            else:
                final_targets[s] = equal_weight

        # Execute trades
        self.SetHoldings(final_targets)
