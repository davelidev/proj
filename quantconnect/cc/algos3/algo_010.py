from AlgorithmImports import *

class Algo010(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ and set up its indicators
        tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.basket = {}
        self.basket[tqqq] = {
            "p25": Percentile(20, 0.25),
            "p75": Percentile(20, 0.75)
        }
        self.RegisterIndicator(tqqq, self.basket[tqqq]["p25"], Resolution.Daily)
        self.RegisterIndicator(tqqq, self.basket[tqqq]["p75"], Resolution.Daily)

        # Universe selection: top 10 by market cap
        self.AddUniverse(self.CoarseFilter, self.FineFilter)

    def CoarseFilter(self, coarse):
        # Return symbols that have fundamental data and price > 0
        return [c.Symbol for c in coarse if c.HasFundamentalData and c.Price > 0]

    def FineFilter(self, fine):
        # Get top 10 by market cap
        sorted_fine = sorted(fine, key=lambda f: f.MarketCap, reverse=True)
        top10 = [f.Symbol for f in sorted_fine[:10]]

        # Always include TQQQ
        tqqq = self.Symbol("TQQQ")
        if tqqq not in top10:
            top10.append(tqqq)

        # Remove symbols that are no longer in the universe
        current_symbols = set(self.basket.keys())
        new_symbols = set(top10)
        symbols_to_remove = current_symbols - new_symbols
        for sym in symbols_to_remove:
            if sym in self.basket:  # but never remove TQQQ
                del self.basket[sym]

        # Add new symbols and their indicators
        for sym in new_symbols - current_symbols:
            if sym not in self.basket:
                self.basket[sym] = {
                    "p25": Percentile(20, 0.25),
                    "p75": Percentile(20, 0.75)
                }
                self.RegisterIndicator(sym, self.basket[sym]["p25"], Resolution.Daily)
                self.RegisterIndicator(sym, self.basket[sym]["p75"], Resolution.Daily)

        return top10

    def OnData(self, data):
        basket_count = len(self.basket)
        if basket_count == 0:
            return

        for symbol, indicators in self.basket.items():
            if not data.ContainsKey(symbol) or data[symbol] is None:
                continue

            close = data[symbol].Close
            p25 = indicators["p25"].Current.Value
            p75 = indicators["p75"].Current.Value

            if not indicators["p25"].IsReady or not indicators["p75"].IsReady:
                continue

            weight = 0.0
            if close < p25:
                weight = 1.0 / basket_count   # long
            elif close > p75:
                weight = -1.0 / basket_count  # short

            self.SetHoldings(symbol, weight)
