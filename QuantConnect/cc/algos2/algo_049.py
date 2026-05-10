from AlgorithmImports import *
import numpy as np


class Algo049(QCAlgorithm):
    """Mega-7 EW + dual gate: QQQ 20d ann. vol < 25% AND ATR(14)/price < 1.8%."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.tickers]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.vol_threshold = 0.25
        self.atr_pct_threshold = 0.018  # 1.8%

        self.atr = self.ATR(self.qqq, 14, MovingAverageType.Wilders, Resolution.Daily)

        # Warmup so ATR has values from day 1 of trading.
        self.SetWarmUp(40, Resolution.Daily)

        self.in_market = False

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.R,
        )

    def R(self):
        if self.IsWarmingUp:
            return
        if not self.atr.IsReady:
            return

        hist = self.History(self.qqq, 21, Resolution.Daily)
        if hist.empty or len(hist) < 21:
            return
        closes = hist['close'].values
        log_rets = np.diff(np.log(closes))
        vol = float(np.std(log_rets) * np.sqrt(252))

        price = float(self.Securities[self.qqq].Price)
        if price <= 0:
            return
        atr_pct = float(self.atr.Current.Value) / price

        target_in = (vol < self.vol_threshold) and (atr_pct < self.atr_pct_threshold)
        if target_in == self.in_market:
            return

        if target_in:
            w = 1.0 / len(self.symbols)
            for s in self.symbols:
                self.SetHoldings(s, w)
        else:
            self.Liquidate()

        self.in_market = target_in
