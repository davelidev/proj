from AlgorithmImports import *

class Algo022(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.UniverseSettings.Resolution = Resolution.Daily

        # Add TQQQ
        tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol
        sma_tqqq = self.SMA(tqqq, 50, Resolution.Daily)
        self.RegisterIndicator(tqqq, sma_tqqq, Resolution.Daily)
        self.basket = {
            tqqq: {
                'sma': sma_tqqq,
                'pos_count': 0,
                'neg_count': 0
            }
        }

        # Add universe for dynamic mega-cap basket (top-10 by market cap)
        self.AddUniverse(self.CoarseSelectionFunction)

        self.SetWarmUp(50)  # for TQQQ indicator warm-up

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with fundamental data, top 10 by market cap
        sorted_by_market_cap = sorted(
            [c for c in coarse if c.HasFundamentalData and c.MarketCap is not None],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        top10 = sorted_by_market_cap[:10]
        return [c.Symbol for c in top10]

    def OnSecuritiesChanged(self, changes):
        # Process added securities
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol in self.basket:
                continue  # already handled (e.g., TQQQ)
            # Add equity with daily resolution (if not already subscribed)
            self.AddEquity(symbol, Resolution.Daily)
            # Create SMA indicator
            sma = self.SMA(symbol, 50, Resolution.Daily)
            self.RegisterIndicator(symbol, sma, Resolution.Daily)
            # Warm up the indicator with historical data
            history = self.History(symbol, 50, Resolution.Daily)
            if not history.empty:
                for index, row in history.iterrows():
                    # row has: time, open, high, low, close, volume
                    sma.Update(index, row['close'])
            # Initialize counting
            self.basket[symbol] = {
                'sma': sma,
                'pos_count': 0,
                'neg_count': 0
            }

        # Process removed securities
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                self.Liquidate(symbol)
                del self.basket[symbol]

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        # Compute signals and weights for all symbols in basket
        signals = {}
        for symbol, info in self.basket.items():
            # Get current bar
            if not data.Bars.ContainsKey(symbol):
                continue
            bar = data.Bars[symbol]
            close = bar.Close

            # Get SMA value (must be ready after warmup)
            if not info['sma'].IsReady:
                continue
            sma_value = info['sma'].Current.Value

            # Update consecutive counts
            if close > sma_value:
                info['pos_count'] += 1
                info['neg_count'] = 0
            elif close < sma_value:
                info['neg_count'] += 1
                info['pos_count'] = 0
            else:
                info['pos_count'] = 0
                info['neg_count'] = 0

            # Determine signal
            if info['pos_count'] >= 3:
                signals[symbol] = 1      # long
            elif info['neg_count'] >= 3:
                signals[symbol] = -1     # short
            else:
                signals[symbol] = 0      # flat

        # Compute total absolute signal magnitude
        total_abs_signal = sum(abs(sig) for sig in signals.values())
        if total_abs_signal == 0:
            # No trades: set all positions to zero (liquidate)
            for symbol in self.basket:
                if self.Portfolio[symbol].Invested:
                    self.Liquidate(symbol)
            return

        weight_per_unit = 1.0 / total_abs_signal

        # Set holdings for each symbol
        for symbol, sig in signals.items():
            target = sig * weight_per_unit
            self.SetHoldings(symbol, target)