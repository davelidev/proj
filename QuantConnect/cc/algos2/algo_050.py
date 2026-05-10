from AlgorithmImports import *
import numpy as np


class Algo050(QCAlgorithm):
    """Mega-7 EW + adaptive vol gate: today's QQQ 20d vol < 1.2 x its 252d median."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.regime_mult = 1.2
        self.vol_window = RollingWindow[float](253)
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

        # Push today's vol observation, then compute median once full.
        self.vol_window.Add(vol)
        if not self.vol_window.IsReady:
            return

        vols = np.array([self.vol_window[i] for i in range(self.vol_window.Count)])
        median_vol = float(np.median(vols))
        if median_vol <= 0:
            return

        target_in = vol < (self.regime_mult * median_vol)
        if target_in == self.in_market:
            return

        if target_in:
            w = 1.0 / len(self.symbols)
            for s in self.symbols:
                self.SetHoldings(s, w)
        else:
            self.Liquidate()

        self.in_market = target_in
