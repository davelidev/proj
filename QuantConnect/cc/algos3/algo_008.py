from AlgorithmImports import *


class Algo008(QCAlgorithm):
    """Equity-Bond-Gold Inverse-Vol Rotation Top 2 from a 6-asset universe."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["SPY", "TLT", "GLD", "DBC", "IEF", "QQQ"]
        self.symbols = []
        for t in self.tickers:
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.symbols.append(sym)

        self.lookback = 60
        self.top_n = 2

        self.Schedule.On(
            self.DateRules.MonthStart(self.symbols[0]),
            self.TimeRules.AfterMarketOpen(self.symbols[0], 30),
            self.Rebalance,
        )

    def Rebalance(self):
        scores = {}
        vols = {}
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
            total_ret = (closes[-1] / closes[0]) - 1.0
            scores[sym] = total_ret / std
            vols[sym] = std

        if not scores:
            return

        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        winners = [s for s, _ in ranked[: self.top_n]]

        for sym in self.symbols:
            if sym not in winners and self.Portfolio[sym].Invested:
                self.Liquidate(sym)

        # Inverse-vol weighting normalized to 1.0
        inv = {s: 1.0 / vols[s] for s in winners if vols.get(s, 0) > 0}
        total_inv = sum(inv.values())
        if total_inv <= 0:
            return
        for sym, iv in inv.items():
            w = iv / total_inv
            self.SetHoldings(sym, w)
