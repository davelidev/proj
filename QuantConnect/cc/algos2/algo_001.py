from AlgorithmImports import *


class Algo001(QCAlgorithm):
    """Sharpe-Ranked Sector Rotation: Hold top-3 of 11 sector ETFs by 63d Sharpe."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["XLK", "XLF", "XLE", "XLV", "XLY", "XLI", "XLP", "XLU", "XLB", "XLRE", "XLC"]
        self.symbols = []
        for t in self.tickers:
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.symbols.append(sym)

        self.lookback = 63
        self.top_n = 3
        self.rebalance_flag = False

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
            rets = (closes[1:] - closes[:-1]) / closes[:-1]
            std = rets.std()
            if std <= 0 or std != std:
                continue
            sharpe = rets.mean() / std
            scores[sym] = sharpe

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
