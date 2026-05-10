from AlgorithmImports import *
import numpy as np


class Algo043(QCAlgorithm):
    """Mega-7 fixed cap-weights + QQQ 20d annualized vol < 25% gate."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        # Fixed cap-style weights (sum=1.0)
        self.weights_by_ticker = {
            "AAPL": 0.20,
            "MSFT": 0.20,
            "NVDA": 0.15,
            "GOOGL": 0.15,
            "AMZN": 0.15,
            "META": 0.10,
            "TSLA": 0.05,
        }
        self.symbol_weights = {}
        for t, w in self.weights_by_ticker.items():
            sym = self.AddEquity(t, Resolution.Daily).Symbol
            self.symbol_weights[sym] = w

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.vol_threshold = 0.25
        self.in_market = False

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.R,
        )

    def R(self):
        hist = self.History(self.qqq, 21, Resolution.Daily)
        if hist.empty or len(hist) < 21:
            return
        closes = hist['close'].values
        log_rets = np.diff(np.log(closes))
        vol = float(np.std(log_rets) * np.sqrt(252))

        target_in = vol < self.vol_threshold
        if target_in == self.in_market:
            return

        if target_in:
            for sym, w in self.symbol_weights.items():
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()

        self.in_market = target_in
