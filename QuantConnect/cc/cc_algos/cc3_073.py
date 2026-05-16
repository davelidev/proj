from AlgorithmImports import *

class ThreeState_QQQSPYRatio(QCAlgorithm):
    """3-state via QQQ/SPY relative strength: 60-day ROC of the ratio."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.spy  = self.AddEquity("SPY",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc_q = self.ROC(self.qqq, 60, Resolution.Daily)
        self.roc_s = self.ROC(self.spy, 60, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.state = None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc_q.IsReady and self.roc_s.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        rs = self.roc_q.Current.Value - self.roc_s.Current.Value  # QQQ outperforming SPY?
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        rs_bull = rs > 0
        d_bull  = price > mid
        if rs_bull and d_bull: ns, wt, wb = "BULL", 1.0, 0.0
        elif rs_bull or d_bull: ns, wt, wb = "MIXED", 0.5, 0.5
        else: ns, wt, wb = "BEAR", 0.0, 1.0
        if ns != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = ns

    def OnData(self, data): pass
