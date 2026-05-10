from AlgorithmImports import *


class Algo087(QCAlgorithm):
    """
    TQQQ Triple-Confirmation Regime.

    Hold 100% TQQQ only when ALL THREE are true on QQQ:
        (a) 1-month return (21d) > 0
        (b) 3-month return (63d) > 0
        (c) 6-month return (126d) > 0
    Else flat.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.SetWarmUp(140, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.DailyCheck,
        )

    def _ret(self, closes, n):
        if len(closes) <= n:
            return None
        prev = closes[-n - 1]
        last = closes[-1]
        if prev <= 0:
            return None
        return last / prev - 1.0

    def DailyCheck(self):
        if self.IsWarmingUp:
            return

        history = self.History([self.qqq], 130, Resolution.Daily)
        if history.empty:
            return
        try:
            closes = history.loc[self.qqq]["close"].values
        except Exception:
            return
        if len(closes) < 127:
            return

        r1 = self._ret(closes, 21)
        r3 = self._ret(closes, 63)
        r6 = self._ret(closes, 126)
        if r1 is None or r3 is None or r6 is None:
            return

        gate_on = (r1 > 0) and (r3 > 0) and (r6 > 0)
        cur_w = self.Portfolio[self.tqqq].HoldingsValue / self.Portfolio.TotalPortfolioValue \
            if self.Portfolio.TotalPortfolioValue > 0 else 0.0

        if gate_on and cur_w < 0.95:
            self.SetHoldings(self.tqqq, 1.0)
        elif (not gate_on) and self.Portfolio[self.tqqq].Invested:
            self.SetHoldings(self.tqqq, 0.0)
