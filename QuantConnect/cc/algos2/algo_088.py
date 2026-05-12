from AlgorithmImports import *


class Algo088(QCAlgorithm):
    """
    TQQQ vs TMF Monthly Best-Of (3x equity vs 3x bonds).

    Each month, hold whichever of {TQQQ, TMF} has the higher 3-month return.
    If both negative, hold cash.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tmf = self.AddEquity("TMF", Resolution.Daily).Symbol

        self.SetWarmUp(80, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.MonthStart(self.tqqq),
            self.TimeRules.AfterMarketOpen(self.tqqq, 30),
            self.MonthlyRebalance,
        )

    def _ret_3mo(self, sym):
        history = self.History([sym], 70, Resolution.Daily)
        if history.empty:
            return None
        try:
            closes = history.loc[sym]["close"].values
        except Exception:
            return None
        if len(closes) < 64:
            return None
        prev = closes[-64]
        last = closes[-1]
        if prev <= 0:
            return None
        return last / prev - 1.0

    def MonthlyRebalance(self):
        if self.IsWarmingUp:
            return

        r_tqqq = self._ret_3mo(self.tqqq)
        r_tmf = self._ret_3mo(self.tmf)

        if r_tqqq is None or r_tmf is None:
            return

        # If both negative -> cash
        if r_tqqq <= 0 and r_tmf <= 0:
            if self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 0.0)
            if self.Portfolio[self.tmf].Invested:
                self.SetHoldings(self.tmf, 0.0)
            return

        if r_tqqq >= r_tmf:
            if self.Portfolio[self.tmf].Invested:
                self.SetHoldings(self.tmf, 0.0)
            self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 0.0)
            self.SetHoldings(self.tmf, 1.0)
