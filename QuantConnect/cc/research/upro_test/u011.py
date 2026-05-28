from AlgorithmImports import *
class U011(QCAlgorithm):
    """QQQ 126D price percentile > 50% → 100% UPRO; else cash. UPRO generalization of ensemble/011."""
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q    = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.upro = self.AddEquity("UPRO", Resolution.Daily).Symbol
        self.SetWarmUp(130, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q, 30), self.R)
    def R(self):
        if self.IsWarmingUp: return
        h = self.History(self.q, 126, Resolution.Daily)
        if h.empty or len(h) < 126: return
        closes = [float(x) for x in h["close"].values]
        lo, hi = min(closes), max(closes)
        if hi == lo: return
        pct = (closes[-1] - lo) / (hi - lo)
        if pct > 0.5:
            self.SetHoldings(self.upro, 1.0)
        else:
            self.Liquidate(self.upro)
    def OnData(self, d): pass
