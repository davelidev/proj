from AlgorithmImports import *

class Algo023(QCAlgorithm):
    """Support/resistance strategy with dynamic mega-cap basket."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Hardcoded TQQQ
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol

        # Holdings tracking dictionary (NOT self.universe)
        self.basket = {}

        # Add TQQQ to basket with rolling windows for 21-day high/low
        self.basket[self.tqqq] = {
            'high': RollingWindow[float](22),
            'low':  RollingWindow[float](22)
        }

        # Dynamic universe: top 10 mega-cap stocks by market cap
        self.AddUniverse(self.CoarseSelection)

        # Warmup for rolling window indicators
        self.SetWarmup(22)

    def CoarseSelection(self, coarse):
        """Select top 10 stocks by market cap from coarse universe."""
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        sorted_by_cap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        return [c.Symbol for c in sorted_by_cap[:10]]

    def OnSecuritiesChanged(self, changes):
        """Add/remove symbols from basket tracking."""
        for added in changes.AddedSecurities:
            if added.Symbol == self.tqqq:
                continue
            if added.Symbol not in self.basket:
                self.basket[added.Symbol] = {
                    'high': RollingWindow[float](22),
                    'low':  RollingWindow[float](22)
                }

        for removed in changes.RemovedSecurities:
            if removed.Symbol in self.basket:
                del self.basket[removed.Symbol]

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        # Update rolling windows with current bar high/low
        for symbol, info in self.basket.items():
            if data.Bars.ContainsKey(symbol):
                bar = data.Bars[symbol]
                info['high'].Add(bar.High)
                info['low'].Add(bar.Low)

        # Compute target weights
        n = len(self.basket)
        weights = {}

        for symbol, info in self.basket.items():
            if info['high'].Count < 22 or info['low'].Count < 22:
                weights[symbol] = 0.0
                continue

            if not data.Bars.ContainsKey(symbol):
                weights[symbol] = 0.0
                continue

            bar = data.Bars[symbol]
            close = bar.Close

            # Previous 21-day high (exclude today)
            prev_high = max(info['high'][i] for i in range(1, 22))
            # Previous 21-day low (exclude today)
            prev_low  = min(info['low'][i] for i in range(1, 22))

            # Generate signal
            if close > prev_high:
                weights[symbol] = 1.0 / n
            elif close < prev_low:
                weights[symbol] = -1.0 / n
            else:
                weights[symbol] = 0.0

        # Liquidate any positions not in the current basket
        for symbol in self.Portfolio.Keys:
            if symbol not in weights and self.Securities.ContainsKey(symbol):
                weights[symbol] = 0.0

        # Set holdings (daily rebalance only)
        for symbol, weight in weights.items():
            if self.Securities.ContainsKey(symbol):
                self.SetHoldings(symbol, weight)