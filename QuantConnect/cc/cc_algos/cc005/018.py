from AlgorithmImports import *

class ThreeState_MomentumAccel(QCAlgorithm):
    """3-state: 'BULL' when ROC(20) > 0 AND ROC(20) > ROC(20) from 10 days ago (accelerating)."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc   = self.ROC(self.qqq, 20, Resolution.Daily)
        self.roc_window = RollingWindow[float](11)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.roc.Updated += self._roc_updated
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(230, Resolution.Daily)
        self.state = None

    def _roc_updated(self, _, point):
        self.roc_window.Add(point.Value)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc.IsReady and self.roc_window.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        roc_now = self.roc_window[0]
        roc_10  = self.roc_window[10]
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        m_up    = roc_now > 0
        m_accel = roc_now > roc_10  # accelerating
        d_bull  = self.Securities[self.qqq].Price > mid

        bull = m_up and m_accel and d_bull
        partial = (m_up or d_bull) and not bull
        if bull: ns, wt, wb = "BULL", 1.0, 0.0
        elif partial: ns, wt, wb = "MIXED", 0.5, 0.5
        else: ns, wt, wb = "BEAR", 0.0, 1.0

        if ns != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = ns

    def OnData(self, data): pass
