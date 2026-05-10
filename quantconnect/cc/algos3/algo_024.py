from AlgorithmImports import *

class Algo024(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        # Universe for top-10 mega cap stocks by market cap
        self.AddUniverse(self.CoarseSelectionFunction)
        self.current_universe = []

        # Holdings tracking (not the universe list)
        self.basket = {}

    def CoarseSelectionFunction(self, coarse):
        # Filter for stocks with fundamental data and positive market cap
        sorted_by_mcap = sorted(
            [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0],
            key=lambda c: c.MarketCap,
            reverse=True
        )
        # Take top 10
        top10 = sorted_by_mcap[:10]
        self.current_universe = [c.Symbol for c in top10]
        return self.current_universe

    def OnData(self, slice):
        # Build set of currently active symbols (TQQQ + universe)
        active_set = set(self.current_universe) | {self.tqqq}

        # Evaluate momentum condition for each active symbol
        for symbol in active_set:
            if slice.Bars.ContainsKey(symbol):
                bar = slice.Bars[symbol]
                # Intra-bar momentum: (close - open) > 2 * (high - low)
                condition = (bar.Close - bar.Open) > 2.0 * (bar.High - bar.Low)
                self.basket[symbol] = 1 if condition else 0

        # Identify symbols with positive signal among active set
        active_signals = [s for s in active_set if self.basket.get(s, 0) == 1]
        total_signals = len(active_signals)

        # Liquidate any symbol that is no longer in the active universe (except TQQQ)
        for symbol in list(self.Portfolio.Keys):
            if symbol not in active_set:
                self.Liquidate(symbol)

        # Rebalance: equal weight among signals, zero weight for others
        if total_signals > 0:
            weight = 1.0 / total_signals
            for symbol in active_set:
                if symbol in active_signals:
                    self.SetHoldings(symbol, weight)
                else:
                    self.SetHoldings(symbol, 0)
        else:
            # No signals: go to cash (liquidate all active positions)
            for symbol in active_set:
                self.SetHoldings(symbol, 0)