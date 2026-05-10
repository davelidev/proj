from AlgorithmImports import *
import numpy as np


class Algo048(QCAlgorithm):
    """5x 3x-leveraged ETF basket EW + QQQ 20d annualized vol < 20% gate (tight)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["TQQQ", "TECL", "SOXL", "UPRO", "FAS"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.vol_threshold = 0.20
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
            w = 1.0 / len(self.symbols)  # 0.20 each, sum=1.0
            for s in self.symbols:
                self.SetHoldings(s, w)
        else:
            self.Liquidate()

        self.in_market = target_in
