from AlgorithmImports import *

class ThreeStateTQQQ(QCAlgorithm):
    """3-state sizing:
       full bull (Aroon AND Donchian-200 both bullish)  → 100% TQQQ
       mixed     (exactly one of the two bullish)       → 50% TQQQ + 50% BIL
       bear      (both bearish)                         → 100% BIL
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.aroon = self.AROON(self.qqq, 25, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.state = None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.aroon.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        up = self.aroon.AroonUp.Current.Value
        dn = self.aroon.AroonDown.Current.Value
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price

        aroon_bull = up > 70 and up > dn
        donch_bull = price > mid

        if aroon_bull and donch_bull:
            new_state = "BULL"
            w_tqqq, w_bil = 1.0, 0.0
        elif aroon_bull or donch_bull:
            new_state = "MIXED"
            w_tqqq, w_bil = 0.5, 0.5
        else:
            new_state = "BEAR"
            w_tqqq, w_bil = 0.0, 1.0

        if new_state != self.state:
            self.SetHoldings(self.tqqq, w_tqqq)
            self.SetHoldings(self.bil, w_bil)
            self.state = new_state

    def OnData(self, data): pass
