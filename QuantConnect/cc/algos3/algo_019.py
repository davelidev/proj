from AlgorithmImports import *


class Algo019(QCAlgorithm):
    """Multi-horizon momentum vote on QQQ across 5d/10d/21d/63d/126d. >=4 positive: TQQQ. <=1 positive: TLT. Else flat."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.horizons = [5, 10, 21, 63, 126]
        self.state = "flat"  # "tqqq" / "tlt" / "flat"

        self.SetWarmUp(140, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not data.ContainsKey(self.qqq):
            return

        max_h = max(self.horizons)
        hist = self.History(self.qqq, max_h + 5, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            closes = hist["close"]
        except Exception:
            return
        if len(closes) < max_h + 1:
            return

        positives = 0
        for h in self.horizons:
            ret = (closes.iloc[-1] / closes.iloc[-h - 1]) - 1.0
            if ret > 0:
                positives += 1

        if positives >= 4:
            new_state = "tqqq"
        elif positives <= 1:
            new_state = "tlt"
        else:
            new_state = "flat"

        if new_state != self.state:
            if new_state == "tqqq":
                self.Liquidate(self.tlt)
                self.SetHoldings(self.tqqq, 1.0)
            elif new_state == "tlt":
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.tlt, 1.0)
            else:
                self.Liquidate()
            self.state = new_state
