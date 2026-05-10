from AlgorithmImports import *


class Algo010(QCAlgorithm):
    """TQQQ-or-bonds: Threshold-based regime switch using QQQ 50d return."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol  # signal only

        self.lookback = 50
        self.up_thresh = 0.05
        self.dn_thresh = -0.05

        self.current_regime = None  # "risk_on", "risk_off", "neutral"

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.CheckRegime,
        )

    def CheckRegime(self):
        hist = self.History(self.qqq, self.lookback + 1, Resolution.Daily)
        if hist.empty or "close" not in hist.columns:
            return
        closes = hist["close"].values
        if len(closes) < self.lookback + 1:
            return
        ret = (closes[-1] / closes[0]) - 1.0

        if ret > self.up_thresh:
            new_regime = "risk_on"
        elif ret < self.dn_thresh:
            new_regime = "risk_off"
        else:
            new_regime = "neutral"

        if new_regime == self.current_regime:
            return
        self.current_regime = new_regime

        if new_regime == "risk_on":
            if self.Portfolio[self.tlt].Invested:
                self.Liquidate(self.tlt)
            self.SetHoldings(self.tqqq, 1.0)
        elif new_regime == "risk_off":
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
            self.SetHoldings(self.tlt, 1.0)
        else:
            self.SetHoldings(self.tqqq, 0.5)
            self.SetHoldings(self.tlt, 0.5)
