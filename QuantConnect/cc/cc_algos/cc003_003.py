from AlgorithmImports import *

class Aroon25Trend(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.aroon = self.AROON(self.qqq, 25, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(35, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.aroon.IsReady:
            return
        up = self.aroon.AroonUp.Current.Value
        dn = self.aroon.AroonDown.Current.Value

        if up > 70 and up > dn:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        elif dn > 70 and dn > up:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
