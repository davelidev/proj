from AlgorithmImports import *
import numpy as np


class Algo045(QCAlgorithm):
    """Mega-7 EW + own-basket 20d annualized vol < 30% gate."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]

        self.vol_threshold = 0.30
        self.in_market = False

        # Use first symbol for scheduling cadence
        self.Schedule.On(
            self.DateRules.EveryDay(self.symbols[0]),
            self.TimeRules.AfterMarketOpen(self.symbols[0], 30),
            self.R,
        )

    def R(self):
        hist = self.History(self.symbols, 21, Resolution.Daily)
        if hist is None or hist.empty:
            return

        # Build per-symbol log return series, then average them per day -> basket return.
        try:
            closes_df = hist['close'].unstack(level=0)
        except Exception:
            return

        # Drop columns with insufficient data
        closes_df = closes_df.dropna(axis=1, how='any')
        if closes_df.shape[0] < 21 or closes_df.shape[1] == 0:
            return

        log_close = np.log(closes_df.values)
        per_sym_log_rets = np.diff(log_close, axis=0)  # shape (20, n_syms)
        basket_rets = per_sym_log_rets.mean(axis=1)  # equal-weighted basket daily return
        vol = float(np.std(basket_rets) * np.sqrt(252))

        target_in = vol < self.vol_threshold
        if target_in == self.in_market:
            return

        if target_in:
            w = 1.0 / len(self.symbols)
            for s in self.symbols:
                self.SetHoldings(s, w)
        else:
            self.Liquidate()

        self.in_market = target_in
