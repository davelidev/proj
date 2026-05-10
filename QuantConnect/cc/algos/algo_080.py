from AlgorithmImports import *


class Algo080(QCAlgorithm):
    """Sector Momentum Rotation: top 2 of 11 SPDR sector ETFs by 3-month return,
    rebalanced monthly, equal-weighted (50/50)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["XLK", "XLF", "XLE", "XLV", "XLY", "XLI", "XLP", "XLU", "XLB", "XLRE", "XLC"]
        self.symbols = []
        for t in self.tickers:
            eq = self.AddEquity(t, Resolution.Daily)
            self.symbols.append(eq.Symbol)

        self.lookback = 63  # ~3 months of trading days
        self.top_n = 2

        self.Schedule.On(
            self.DateRules.MonthStart("XLK"),
            self.TimeRules.At(10, 0),
            self.Rebalance,
        )

    def Rebalance(self):
        returns = {}
        for sym in self.symbols:
            hist = self.History(sym, self.lookback, Resolution.Daily)
            if hist is None or hist.empty:
                continue
            try:
                closes = hist["close"]
            except Exception:
                continue
            if len(closes) < 2:
                continue
            first = float(closes.iloc[0])
            last = float(closes.iloc[-1])
            if first <= 0:
                continue
            returns[sym] = (last / first) - 1.0

        if not returns:
            return

        ranked = sorted(returns.items(), key=lambda kv: kv[1], reverse=True)
        winners = [sym for sym, _ in ranked[: self.top_n]]

        # Liquidate non-winners
        for sym in self.symbols:
            if sym not in winners and self.Portfolio[sym].Invested:
                self.Liquidate(sym)

        # Allocate equally among winners
        if winners:
            w = 1.0 / len(winners)
            for sym in winners:
                self.SetHoldings(sym, w)
