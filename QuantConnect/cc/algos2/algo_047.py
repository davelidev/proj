from AlgorithmImports import *
import numpy as np


class Algo047(QCAlgorithm):
    """Mega-7 + QQQ 20d vol < 25% gate + monthly inverse-vol (risk-parity) weights."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.vol_threshold = 0.25
        self.in_market = False

        self.weights = {s: 1.0 / len(self.symbols) for s in self.symbols}

        self.Schedule.On(
            self.DateRules.MonthStart(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 20),
            self.RecomputeWeights,
        )
        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.R,
        )

    def RecomputeWeights(self):
        # 60d std of daily log returns -> need 61 closes.
        inv_vol = {}
        for s in self.symbols:
            hist = self.History(s, 61, Resolution.Daily)
            if hist is None or hist.empty or len(hist) < 61:
                inv_vol[s] = 0.0
                continue
            closes = hist['close'].values
            log_rets = np.diff(np.log(closes))
            std = float(np.std(log_rets))
            inv_vol[s] = (1.0 / std) if std > 1e-9 else 0.0

        total = sum(inv_vol.values())
        if total <= 0.0:
            self.weights = {s: 1.0 / len(self.symbols) for s in self.symbols}
        else:
            self.weights = {s: v / total for s, v in inv_vol.items()}

        if self.in_market:
            self._apply_weights()

    def _apply_weights(self):
        for s, w in self.weights.items():
            self.SetHoldings(s, w)

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
            self._apply_weights()
        else:
            self.Liquidate()

        self.in_market = target_in
