from AlgorithmImports import *


class Algo012(QCAlgorithm):
    """TQQQ gated by credit-spread risk-on signal: HYG 20d return vs LQD 20d return."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.hyg = self.AddEquity("HYG", Resolution.Daily).Symbol
        self.lqd = self.AddEquity("LQD", Resolution.Daily).Symbol

        self.lookback = 20
        self.in_position = False

        self.SetWarmUp(30, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not (data.ContainsKey(self.tqqq) and data.ContainsKey(self.hyg) and data.ContainsKey(self.lqd)):
            return

        hist = self.History([self.hyg, self.lqd], self.lookback + 2, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            hyg_close = hist.loc[self.hyg]["close"]
            lqd_close = hist.loc[self.lqd]["close"]
        except Exception:
            return
        if len(hyg_close) < self.lookback + 1 or len(lqd_close) < self.lookback + 1:
            return

        hyg_ret = (hyg_close.iloc[-1] / hyg_close.iloc[-self.lookback - 1]) - 1.0
        lqd_ret = (lqd_close.iloc[-1] / lqd_close.iloc[-self.lookback - 1]) - 1.0
        spread = hyg_ret - lqd_ret

        want_in = spread > 0
        if want_in and not self.in_position:
            self.SetHoldings(self.tqqq, 1.0)
            self.in_position = True
        elif not want_in and self.in_position:
            self.Liquidate()
            self.in_position = False
