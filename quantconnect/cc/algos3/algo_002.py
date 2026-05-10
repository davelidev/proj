from AlgorithmImports import *

class Algo002(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Add TQQQ for stochastic indicator
        self.AddEquity("TQQQ", Resolution.Daily)
        # Fast Stochastic: 14-period %K, 3-period smoothing
        self.stoch = self.STO("TQQQ", 14, 3, 3, Resolution.Daily)
        self.signalState = 0  # 0: flat, 1: long
        self.basket = {}  # dict to track current universe symbols

        # Universe selection: top-10 by market cap (daily)
        self.AddUniverse(self.CoarseSelectionFunction)
        self.SetWarmUp(20)  # warm up stochastic

    def CoarseSelectionFunction(self, coarse):
        # Filter stocks with fundamental data and positive market cap
        filtered = [c for c in coarse if c.HasFundamentalData and c.MarketCap > 0]
        # Sort descending by market cap and take top 10
        sorted_by_mcap = sorted(filtered, key=lambda c: c.MarketCap, reverse=True)
        top10 = sorted_by_mcap[:10]
        # Exclude TQQQ if it appears (it shouldn't be in the basket)
        return [c.Symbol for c in top10 if c.Symbol.Value != "TQQQ"]

    def OnSecuritiesChanged(self, changes):
        # Liquidate removed securities that are not TQQQ
        for security in changes.RemovedSecurities:
            if security.Symbol.Value != "TQQQ" and security.Symbol in self.basket:
                self.Liquidate(security.Symbol)
                del self.basket[security.Symbol]
        # Add new securities to basket
        for security in changes.AddedSecurities:
            if security.Symbol.Value != "TQQQ":
                self.basket[security.Symbol] = 0

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        # Get current %K value of stochastic
        if not self.stoch.IsReady:
            return
        k = self.stoch.Current.Value

        basket_count = len(self.basket)
        if basket_count == 0:
            return

        # Determine target weight per symbol
        if k < 30 and self.signalState != 1:
            # Oversold: go long mega-cap equally
            weight = 1.0 / basket_count
            for symbol in self.basket:
                self.SetHoldings(symbol, weight)
            self.signalState = 1
        elif k > 70 and self.signalState != 0:
            # Overbought: go flat (sell all basket positions)
            for symbol in self.basket:
                self.SetHoldings(symbol, 0)
            self.signalState = 0
