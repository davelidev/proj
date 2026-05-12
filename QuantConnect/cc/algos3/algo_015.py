from AlgorithmImports import *


class Algo015(QCAlgorithm):
    """TQQQ when TLT 50d return is negative (rates rising = risk-on growth tailwind); else flat."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol

        self.lookback = 50
        self.in_position = False

        self.SetWarmUp(60, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not (data.ContainsKey(self.tqqq) and data.ContainsKey(self.tlt)):
            return

        hist = self.History(self.tlt, self.lookback + 2, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            tlt_close = hist["close"]
        except Exception:
            return
        if len(tlt_close) < self.lookback + 1:
            return

        tlt_ret = (tlt_close.iloc[-1] / tlt_close.iloc[-self.lookback - 1]) - 1.0
        want_in = tlt_ret < 0

        if want_in and not self.in_position:
            self.SetHoldings(self.tqqq, 1.0)
            self.in_position = True
        elif not want_in and self.in_position:
            self.Liquidate()
            self.in_position = False
