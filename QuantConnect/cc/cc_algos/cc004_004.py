from AlgorithmImports import *

class ThreeState_Donchian150(QCAlgorithm):
    """3-state with Aroon-25 + Donchian-150 midline (intermediate speed)."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.aroon = self.AROON(self.qqq, 25, Resolution.Daily)
        self.hi150 = self.MAX(self.qqq, 150, Resolution.Daily)
        self.lo150 = self.MIN(self.qqq, 150, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(170, Resolution.Daily)
        self.state = None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.aroon.IsReady and self.hi150.IsReady and self.lo150.IsReady):
            return
        up = self.aroon.AroonUp.Current.Value
        dn = self.aroon.AroonDown.Current.Value
        mid = (self.hi150.Current.Value + self.lo150.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        a_bull = up > 70 and up > dn
        d_bull = price > mid

        if a_bull and d_bull:
            ns, wt, wb = "BULL", 1.0, 0.0
        elif a_bull or d_bull:
            ns, wt, wb = "MIXED", 0.5, 0.5
        else:
            ns, wt, wb = "BEAR", 0.0, 1.0

        if ns != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = ns

    def OnData(self, data): pass
