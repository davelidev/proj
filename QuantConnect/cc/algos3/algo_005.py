from AlgorithmImports import *


class Algo005(QCAlgorithm):
    """Cross-Asset Momentum Cascade: EW only positive 6mo-return assets, else BIL."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["QQQ", "SPY", "TLT", "GLD"]
        self.symbols = []
        for t in self.tickers:
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.symbols.append(sym)

        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol

        self.lookback = 126  # ~6 months

        self.Schedule.On(
            self.DateRules.MonthStart(self.symbols[0]),
            self.TimeRules.AfterMarketOpen(self.symbols[0], 30),
            self.Rebalance,
        )

    def Rebalance(self):
        positive = []
        for sym in self.symbols:
            hist = self.History(sym, self.lookback + 1, Resolution.Daily)
            if hist.empty or "close" not in hist.columns:
                continue
            closes = hist["close"].values
            if len(closes) < self.lookback + 1:
                continue
            ret_6m = (closes[-1] / closes[0]) - 1.0
            if ret_6m > 0:
                positive.append(sym)

        if not positive:
            for sym in self.symbols:
                if self.Portfolio[sym].Invested:
                    self.Liquidate(sym)
            self.SetHoldings(self.bil, 1.0)
            return

        if self.Portfolio[self.bil].Invested:
            self.Liquidate(self.bil)

        for sym in self.symbols:
            if sym not in positive and self.Portfolio[sym].Invested:
                self.Liquidate(sym)

        n = len(positive)
        weight = 1.0 / n
        for sym in positive:
            self.SetHoldings(sym, weight)
