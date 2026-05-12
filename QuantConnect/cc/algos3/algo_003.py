from AlgorithmImports import *
import numpy as np


class Algo003(QCAlgorithm):
    """Drawdown-Adjusted Rotation: top-2 by 252d return divided by |max drawdown|."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["QQQ", "SPY", "XLK", "XLY", "XLF", "XLV", "TLT", "GLD"]
        self.symbols = []
        for t in self.tickers:
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.symbols.append(sym)

        self.lookback = 252
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
            total_ret = (closes[-1] / closes[0]) - 1.0
            running_max = np.maximum.accumulate(closes)
            drawdowns = (closes - running_max) / running_max
            max_dd = abs(drawdowns.min())
            if max_dd <= 1e-6:
                continue
            scores[sym] = total_ret / max_dd

        if not scores:
            return
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        winners = [s for s, _ in ranked[: self.top_n]]

        for sym in self.symbols:
            if sym not in winners and self.Portfolio[sym].Invested:
                self.Liquidate(sym)

        weight = 1.0 / max(len(winners), 1)
        for sym in winners:
            self.SetHoldings(sym, weight)
