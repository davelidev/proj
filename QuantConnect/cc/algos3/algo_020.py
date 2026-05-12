from AlgorithmImports import *
import math


class Algo020(QCAlgorithm):
    """TQQQ gated by 20d QQQ-TLT realized correlation: corr < -0.5 → 100% TQQQ; corr > 0 → flat."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol

        self.window = 20
        self.in_position = False

        self.SetWarmUp(40, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not (data.ContainsKey(self.qqq) and data.ContainsKey(self.tlt)):
            return

        hist = self.History([self.qqq, self.tlt], self.window + 5, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            qqq_close = hist.loc[self.qqq]["close"]
            tlt_close = hist.loc[self.tlt]["close"]
        except Exception:
            return
        if len(qqq_close) < self.window + 1 or len(tlt_close) < self.window + 1:
            return

        n = min(len(qqq_close), len(tlt_close))
        qqq_rets = []
        tlt_rets = []
        for i in range(1, n):
            qp = qqq_close.iloc[i - 1]
            qc = qqq_close.iloc[i]
            tp = tlt_close.iloc[i - 1]
            tc = tlt_close.iloc[i]
            if qp > 0 and tp > 0:
                qqq_rets.append((qc / qp) - 1.0)
                tlt_rets.append((tc / tp) - 1.0)
        if len(qqq_rets) < self.window or len(tlt_rets) < self.window:
            return

        q = qqq_rets[-self.window:]
        t = tlt_rets[-self.window:]
        m_q = sum(q) / len(q)
        m_t = sum(t) / len(t)
        cov = sum((q[i] - m_q) * (t[i] - m_t) for i in range(len(q))) / (len(q) - 1)
        var_q = sum((x - m_q) ** 2 for x in q) / (len(q) - 1)
        var_t = sum((x - m_t) ** 2 for x in t) / (len(t) - 1)
        if var_q <= 0 or var_t <= 0:
            return
        corr = cov / (math.sqrt(var_q) * math.sqrt(var_t))

        if corr < -0.5 and not self.in_position:
            self.SetHoldings(self.tqqq, 1.0)
            self.in_position = True
        elif corr > 0.0 and self.in_position:
            self.Liquidate()
            self.in_position = False
