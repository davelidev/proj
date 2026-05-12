from AlgorithmImports import *


class Algo006(QCAlgorithm):
    """Defensive vs Aggressive Sector Pair Switch: aggressive basket if outperforming, else defensive."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.aggressive_t = ["XLK", "XLY", "XLC"]
        self.defensive_t = ["XLP", "XLU", "XLV"]

        self.aggressive = []
        for t in self.aggressive_t:
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.aggressive.append(sym)

        self.defensive = []
        for t in self.defensive_t:
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.defensive.append(sym)

        self.lookback = 63

        self.Schedule.On(
            self.DateRules.MonthStart(self.aggressive[0]),
            self.TimeRules.AfterMarketOpen(self.aggressive[0], 30),
            self.Rebalance,
        )

    def basket_return(self, syms):
        rets = []
        for sym in syms:
            hist = self.History(sym, self.lookback + 1, Resolution.Daily)
            if hist.empty or "close" not in hist.columns:
                continue
            closes = hist["close"].values
            if len(closes) < self.lookback + 1:
                continue
            rets.append((closes[-1] / closes[0]) - 1.0)
        if not rets:
            return None
        return sum(rets) / len(rets)

    def Rebalance(self):
        agg_r = self.basket_return(self.aggressive)
        def_r = self.basket_return(self.defensive)
        if agg_r is None or def_r is None:
            return
        spread = agg_r - def_r

        if spread >= 0:
            target = self.aggressive
            other = self.defensive
        else:
            target = self.defensive
            other = self.aggressive

        for sym in other:
            if self.Portfolio[sym].Invested:
                self.Liquidate(sym)

        weight = 1.0 / 3.0
        for sym in target:
            self.SetHoldings(sym, weight)
