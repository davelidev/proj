from AlgorithmImports import *


class Algo039(QCAlgorithm):
    """8 Leveraged ETF EW Permanent + Monthly Rebalance.

    Basket: TQQQ, UPRO, SOXL, TECL, QLD, SSO, DDM, FAS.
    Equal-weight (1/8 each). Pure cross-sectional rebalance harvesting,
    no timing signal. Rebalance back to EW monthly.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        basket = ["TQQQ", "UPRO", "SOXL", "TECL", "QLD", "SSO", "DDM", "FAS"]
        self.basket_symbols = []
        for t in basket:
            eq = self.AddEquity(t, Resolution.Daily)
            self.basket_symbols.append(eq.Symbol)

        self.SetWarmUp(5, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.MonthStart(self.basket_symbols[0]),
            self.TimeRules.AfterMarketOpen(self.basket_symbols[0], 30),
            self.RebalanceEW,
        )


    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe

    def RebalanceEW(self):
        if self.IsWarmingUp:
            return
        w = 1.0 / len(self.basket_symbols)
        for sym in self.basket_symbols:
            self.SetHoldings(sym, w)
