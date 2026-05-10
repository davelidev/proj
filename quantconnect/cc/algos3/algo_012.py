from QuantConnect import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import *
from QuantConnect.Data.UniverseSelection import *

class Algo012(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ with daily resolution
        self.AddEquity("TQQQ", Resolution.Daily)

        # Universe selection: top 10 by market cap, exclude TQQQ
        self.AddUniverse(self.CoarseSelectionFunction)

        # Basket to track indicators and holdings
        self.basket = {}

        # Initialize indicators for TQQQ
        tqqq = self.Symbol("TQQQ")
        self.basket[tqqq] = {
            "adx": self.ADX(tqqq, 14, Resolution.Daily),
            "max": self.MAX(tqqq, 5, Resolution.Daily)
        }
        # Warm up indicators
        self.WarmUpIndicator(tqqq, self.basket[tqqq]["adx"], Resolution.Daily, 14)
        self.WarmUpIndicator(tqqq, self.basket[tqqq]["max"], Resolution.Daily, 5)

        # Schedule daily rebalance at the end of each bar (OnData is called daily)
        # No scheduling needed; we handle in OnData

    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data, sort by market cap descending, take top 10, exclude TQQQ
        sorted_by_mc = sorted(
            [c for c in coarse if c.HasFundamentalData and c.Symbol.Value != "TQQQ"],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        return [c.Symbol for c in sorted_by_mc[:10]]

    def OnSecuritiesChanged(self, changes):
        # Remove symbols no longer in universe
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket and symbol.Value != "TQQQ":
                self.Liquidate(symbol)
                del self.basket[symbol]

        # Add new symbols and their indicators
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = {
                    "adx": self.ADX(symbol, 14, Resolution.Daily),
                    "max": self.MAX(symbol, 5, Resolution.Daily)
                }
                self.WarmUpIndicator(symbol, self.basket[symbol]["adx"], Resolution.Daily, 14)
                self.WarmUpIndicator(symbol, self.basket[symbol]["max"], Resolution.Daily, 5)

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        # Collect signals for each symbol in basket
        buy_signals = []
        for symbol, indicators in self.basket.items():
            # Check if indicators are ready
            if not (indicators["adx"].IsReady and indicators["max"].IsReady):
                continue
            # Get values
            adx = indicators["adx"].Current.Value
            max_5d = indicators["max"].Current.Value
            price = self.Securities[symbol].Price

            # Signal: ADX > 25 and price > 5d high → buy
            if adx > 25 and price > max_5d:
                buy_signals.append(symbol)
            # ADX < 20 → flat (liquidate later) – we'll set weight 0 for those not in buy_signals

        # Compute target weights: equal weight among buy signals, cash if none
        if len(buy_signals) > 0:
            weight_per = 1.0 / len(buy_signals)
        else:
            weight_per = 0.0

        # Set holdings for all symbols in basket (including TQQQ)
        for symbol in self.basket.Keys:
            if symbol in buy_signals:
                self.SetHoldings(symbol, weight_per)
            else:
                # Liquidate if position exists
                if self.Portfolio[symbol].Invested:
                    self.SetHoldings(symbol, 0.0)
