from AlgorithmImports import *


class Algo082(QCAlgorithm):
    """Long-only TQQQ/SQQQ pair regime switch driven by 20-day QQQ return.
    Positive 20d → 100% TQQQ; Negative → 100% SQQQ. Daily check, trade on flip only."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sqqq = self.AddEquity("SQQQ", Resolution.Daily).Symbol

        self.lookback = 20
        self.current_regime = None  # "long", "short", or None

        self.SetWarmUp(self.lookback + 5, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        hist = self.History(self.qqq, self.lookback + 1, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            closes = hist["close"]
        except Exception:
            return
        if len(closes) < self.lookback + 1:
            return

        first = float(closes.iloc[0])
        last = float(closes.iloc[-1])
        if first <= 0:
            return
        ret = (last / first) - 1.0

        new_regime = "long" if ret > 0 else "short"

        if new_regime == self.current_regime:
            return

        # Regime flip — execute switch
        if new_regime == "long":
            if self.Portfolio[self.sqqq].Invested:
                self.Liquidate(self.sqqq)
            self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
            self.SetHoldings(self.sqqq, 1.0)

        self.current_regime = new_regime
