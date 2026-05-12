from AlgorithmImports import *


class Algo011(QCAlgorithm):
    """TQQQ gated by yield-curve flight-to-safety signal: TLT 30d return vs IEF 30d return."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol
        self.ief = self.AddEquity("IEF", Resolution.Daily).Symbol

        self.lookback = 30
        self.in_position = False

        self.SetWarmUp(40, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not (data.ContainsKey(self.tqqq) and data.ContainsKey(self.tlt) and data.ContainsKey(self.ief)):
            return

        hist = self.History([self.tlt, self.ief], self.lookback + 2, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            tlt_close = hist.loc[self.tlt]["close"]
            ief_close = hist.loc[self.ief]["close"]
        except Exception:
            return
        if len(tlt_close) < self.lookback + 1 or len(ief_close) < self.lookback + 1:
            return

        tlt_ret = (tlt_close.iloc[-1] / tlt_close.iloc[-self.lookback - 1]) - 1.0
        ief_ret = (ief_close.iloc[-1] / ief_close.iloc[-self.lookback - 1]) - 1.0
        spread = tlt_ret - ief_ret

        want_in = spread > 0
        if want_in and not self.in_position:
            self.SetHoldings(self.tqqq, 1.0)
            self.in_position = True
        elif not want_in and self.in_position:
            self.Liquidate()
            self.in_position = False
