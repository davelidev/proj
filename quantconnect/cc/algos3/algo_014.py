from AlgorithmImports import *

class Algo014(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Main signal asset
        self.tqqq = self.AddEquity('TQQQ', Resolution.Daily).Symbol

        # Keltner Channel indicator on TQQQ
        period = 20
        multiplier = 1.5
        self.kc = KeltnerChannels(period, multiplier)
        self.RegisterIndicator(self.tqqq, self.kc, Resolution.Daily)

        # Dynamic universe – top 10 by market cap
        self.AddUniverse(self.FundamentalFunction)
        self.basket = {}  # Dictionary to track current holdings
        self.selection_flag = False

    def FundamentalFunction(self, fundamental):
        # Sort by market cap descending, take top 10
        if fundamental is None:
            return []
        sorted_by_mc = sorted(fundamental,
                             key=lambda x: x.MarketCap if x.MarketCap else 0,
                             reverse=True)
        top10 = sorted_by_mc[:10]
        # Return list of symbols; ignore if no stocks
        return [f.Symbol for f in top10 if f.Symbol is not None]

    def OnSecuritiesChanged(self, changes):
        # Update basket: add new symbols, remove old
        for added in changes.AddedSecurities:
            symbol = added.Symbol
            if symbol not in self.basket:
                self.basket[symbol] = symbol
        for removed in changes.RemovedSecurities:
            symbol = removed.Symbol
            if symbol in self.basket:
                del self.basket[symbol]
        self.selection_flag = True

    def OnData(self, data):
        # Wait for indicators to be ready
        if not self.kc.IsReady:
            return
        if not self.selection_flag:
            return  # Wait for universe selection to populate basket

        # Get current price and Keltner bands
        if not data.Bars.ContainsKey(self.tqqq):
            return
        price = data.Bars[self.tqqq].Close
        upper_band = self.kc.UpperBand.Current.Value

        # Decide signal
        if price > upper_band:
            target_weight = 1.0 / max(len(self.basket), 1)
        else:
            target_weight = 0.0

        # Apply to all basket holdings
        for symbol in self.basket:
            if data.ContainsKey(symbol) and data[symbol] is not None and data[symbol].Price != 0:
                self.SetHoldings(symbol, target_weight)
            else:
                self.SetHoldings(symbol, 0.0)

        # Reset selection flag to avoid repeated rebalance
        self.selection_flag = False
