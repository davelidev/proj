from AlgorithmImports import *


class Algo009(QCAlgorithm):
    """Region-Rotation: Top-2 of US/EU/JP/EM/CN by 90d return at 50/50."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["SPY", "EFA", "EWJ", "EEM", "FXI"]
        self.symbols = []
        for t in self.tickers:
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.symbols.append(sym)

        self.lookback = 90
        self.top_n = 2

        self.Schedule.On(
            self.DateRules.MonthStart(self.symbols[0]),
            self.TimeRules.AfterMarketOpen(self.symbols[0], 30),
            self.Rebalance,
        )

    def Rebalance(self):
        scores = {}
        for sym in self.symbols:
            hist = self.History(sym, self.lookback + 1, Resolution.Daily)
            if hist.empty or "close" not in hist.columns:
                continue
            closes = hist["close"].values
            if len(closes) < self.lookback + 1:
                continue
            scores[sym] = (closes[-1] / closes[0]) - 1.0

        if not scores:
            return
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        winners = [s for s, _ in ranked[: self.top_n]]

        for sym in self.symbols:
            if sym not in winners and self.Portfolio[sym].Invested:
                self.Liquidate(sym)

        weight = 0.5
        for sym in winners:
            self.SetHoldings(sym, weight)
