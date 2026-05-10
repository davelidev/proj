from AlgorithmImports import *


class Algo075(QCAlgorithm):
    """
    Mega-5 (AAPL/MSFT/NVDA/GOOGL/AMZN) monthly with SMA200 gate and IBS dip overweight.

    Each month: hold only names whose price > 200d SMA. Among those, names with
    IBS < 0.1 today get double weight; rest single. Normalise to 1.0.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
        self.symbols = []
        self.smas    = {}
        self.ibs     = {}

        for t in self.tickers:
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.symbols.append(sym)
            self.smas[sym] = self.SMA(sym, 200, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.MonthStart(),
            self.TimeRules.AfterMarketOpen("AAPL", 30),
            self.Rebalance,
        )

    def OnData(self, data):
        for sym in self.symbols:
            bar = data.Bars.get(sym)
            if bar is not None and bar.High != bar.Low:
                self.ibs[sym] = (bar.Close - bar.Low) / (bar.High - bar.Low)

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        # ── Step 1: SMA200 gate ──────────────────────────────────────
        trending = []
        for sym in self.symbols:
            sma = self.smas[sym]
            if sma.IsReady and self.Securities[sym].Price > sma.Current.Value:
                trending.append(sym)

        if not trending:
            for sym in self.symbols:
                self.Liquidate(sym)
            return

        # ── Step 2: IBS-based weighting ───────────────────────────────
        weights = {}
        for sym in trending:
            ibs = self.ibs.get(sym, 0.5)
            weights[sym] = 2.0 if ibs < 0.1 else 1.0

        total_w = sum(weights.values())
        for sym in weights:
            weights[sym] /= total_w

        # ── Execute ──────────────────────────────────────────────────
        for sym in self.symbols:
            if sym not in trending:
                self.Liquidate(sym)

        for sym, w in weights.items():
            self.SetHoldings(sym, w)
